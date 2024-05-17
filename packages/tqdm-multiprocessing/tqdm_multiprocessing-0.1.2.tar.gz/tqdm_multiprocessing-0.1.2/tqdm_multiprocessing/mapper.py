#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import logging
import time
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Callable, Hashable, Iterable, Iterator, List, Optional, Type, TypeVar, Union, cast

from tqdm import tqdm


logger = logging.getLogger(__name__)


A = TypeVar("A")
T = TypeVar("T", bound=Hashable)
PoolExecutor = Union[ProcessPoolExecutor, ThreadPoolExecutor]


@dataclass
class ConcurrentMapper:
    r"""Helper for mapping a function over an iterable using multiprocessing with tqdm support. Mapping over
    very large inputs should be well supported, with responsive progress bar updates throughout.

    Args:
        threads:
            If ``True``, use :class:`ThreadPoolExecutor`, otherwise use :class:`ProcessPoolExecutor`.
            When ``jobs == 0``, a :class:`ThreadPoolExecutor` will be used regardless of the value of ``threads``.

        jobs:
            Number of worker threads/processes to use. Can be set to zero to disable concurrency.

        ignore_exceptions:
            If ``True``, ignore exceptions that are raised when mapping over an iterable.

        chunksize:
            Chunk size for jobs that are submitted to the pool. See :class:`ProcessPoolExecutor` documentation
            for more info.

        timeout:
            Timeout in seconds for tasks

        exception_callback:
            Optional callback to be called if a worker encounters an exception

        unroll_iterators:
            If ``True``, an iterator returned by the map function will be unrolled into the final result.

    Examples::

        >>> iterable = list(range(5))
        >>> func = lambda x, y: x+y
        >>> with ConcurrentMapper() as mapper:
        >>>     mapper.create_bar(desc="Processing", total=len(iterable))
        >>>     result = mapper(func, iterable, y=1)
        >>> print(result)
        [1, 2, 3, 4, 5]
    """

    threads: bool = False
    jobs: Optional[int] = None
    ignore_exceptions: bool = False
    chunksize: int = 1
    timeout: Optional[float] = None
    exception_callback: Optional[Callable[[Future], Any]] = None
    unroll_iterators: bool = True

    _pool: Optional[PoolExecutor] = field(init=False, repr=False, default=None)
    _bar: Optional[tqdm] = field(init=False, repr=False, default=None)

    def __post_init__(self):
        if self.chunksize < 1:
            raise ValueError(f"`chunksize` must be >= 1, got {self.chunksize}")
        if self.jobs is not None and self.jobs < 0:
            raise ValueError(f"`jobs` must be >= 0, got {self.jobs}")

    def __enter__(self) -> "ConcurrentMapper":
        logger.debug(f"Creating pool of type {self.pool_type}")
        jobs = self.jobs if self.jobs is None or self.jobs > 0 else 1
        self._pool = self.pool_type(jobs)
        return self

    def create_bar(self, *args, **kwargs) -> tqdm:
        r"""Create a tqdm progress bar. Args are forwarded to the tqdm bar.
        Override with custom bar creation logic if desired.
        """
        self._bar = self._create_bar(*args, **kwargs)
        return self._bar

    def _create_bar(self, *args, **kwargs) -> tqdm:
        return tqdm(*args, **kwargs)

    def close_bar(self) -> None:
        if self._bar is not None:
            self._bar.close()
        self._bar = None

    def __call__(self, fn: Callable[..., A], iterable: Iterable, *args, **kwargs) -> Iterator[A]:
        if self._pool is None:
            raise RuntimeError("Pool not initialized. Please use `with ConcurrentMapper() as mapper` to init a pool.")

        chunks = self._get_chunks(iterable, chunksize=self.chunksize)
        results = self._map(
            partial(self._process_chunk, fn),
            chunks,
            *args,
            unroll_iterators=self.unroll_iterators,
            **kwargs,
        )
        return self._chain_from_iterable_of_lists(results)

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self._pool is not None
        self._pool.shutdown(wait=True)
        self.close_bar()

    def _force_kill_processes(self) -> None:
        r"""Without this method, KeyboardInterrupt doesn't seem to kill worker processes"""
        if isinstance(self._pool, ProcessPoolExecutor):
            for pid, proc in self._pool._processes.items():  # type: ignore
                logger.debug(f"Terminating PID {pid}")
                proc.terminate()

    @property
    def pool_type(self) -> Type[PoolExecutor]:
        return ThreadPoolExecutor if self.threads or self.jobs == 0 else ProcessPoolExecutor

    @classmethod
    def done_callback(cls, bar: Optional[tqdm], future: Future) -> None:
        logger.debug(f"Finished job with future {future}")
        if ex := future.exception():
            logger.error(ex, exc_info=True)

        if bar is not None:
            result = future.result()
            bar.update(len(result))

    def _map(self, fn: Callable[..., A], iterable: Iterable, *args, **kwargs) -> Iterator[A]:
        if self.timeout is not None:
            end_time = self.timeout + time.monotonic()

        assert self._pool is not None
        fs: List[Future] = []
        logger.debug("Submitting tasks")
        for i in iterable:
            f = self._pool.submit(fn, i, *args, **kwargs)
            if self._bar is not None:
                f.add_done_callback(lambda _f: self.done_callback(self._bar, _f))
            fs.append(f)
        logger.debug(f"Submitted {len(fs)} tasks")

        # Yield must be hidden in closure so that the futures are submitted
        # before the first iterator value is required.
        def result_iterator():
            try:
                # reverse to keep finishing order
                fs.reverse()
                while fs:
                    future = fs.pop()
                    try:
                        # Careful not to keep a reference to the popped future
                        if self.timeout is None:
                            yield self._result_or_cancel(future)
                        else:
                            yield self._result_or_cancel(future, end_time - time.monotonic())
                    except (KeyboardInterrupt, SystemExit) as ex:
                        logger.debug(f"Caught {type(ex)}, terminating processes")
                        self._force_kill_processes()
                        raise
                    except Exception as ex:
                        if self.exception_callback is not None:
                            self.exception_callback(future)
                        if self.ignore_exceptions:
                            logger.info(f"Ignored exception {ex} for {future}")
                        else:
                            raise
            finally:
                for future in fs:
                    future.cancel()

        return cast(Iterator, result_iterator())

    def _result_or_cancel(self, fut: Future, timeout: Optional[float] = None):
        try:
            try:
                return fut.result(timeout)
            finally:
                fut.cancel()
        finally:
            # Break a reference cycle with the exception in self._exception
            del fut

    @classmethod
    def _get_chunks(cls, iterable: Iterable[T], chunksize: int) -> Iterator[Iterable[T]]:
        """Iterates over zip()ed iterables in chunks."""
        it = iter(iterable)
        while True:
            chunk = tuple(itertools.islice(it, chunksize))
            if not chunk:
                return
            yield chunk

    @classmethod
    def _process_chunk(cls, fn, chunk, *args, unroll_iterators: bool = True, **kwargs):
        """Processes a chunk of an iterable passed to map.
        Runs the function passed to map() on a chunk of the
        iterable passed to map.
        This function is run in a separate process.
        """
        result: List[Any] = []
        for c in chunk:
            r = fn(c, *args, **kwargs)
            if isinstance(r, Iterator):
                if unroll_iterators:
                    result = result + list(r)
                else:
                    raise TypeError("Function passed to map() must not return an iterator")
            else:
                result.append(r)
        return result

    @classmethod
    def _chain_from_iterable_of_lists(cls, iterable: Iterable[List[A]]) -> Iterator[A]:
        """
        Specialized implementation of itertools.chain.from_iterable.
        Each item in *iterable* should be a list.  This function is
        careful not to keep references to yielded objects.
        """
        for element in iterable:
            element.reverse()
            while element:
                yield element.pop()
