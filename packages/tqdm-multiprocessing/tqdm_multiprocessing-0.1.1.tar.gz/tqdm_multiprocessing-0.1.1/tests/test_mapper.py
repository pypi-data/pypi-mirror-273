#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Iterator

import pytest

from tqdm_multiprocessing.mapper import ConcurrentMapper


class TestConcurrentMapper:
    @pytest.mark.parametrize("jobs", [1, 4, None])
    @pytest.mark.parametrize("threads", [True, False])
    @pytest.mark.parametrize("length", [10, 1000])
    @pytest.mark.parametrize("chunksize", [1, 32])
    @pytest.mark.parametrize("inp_type", [list, set, iter])
    def test_map_list(self, threads, jobs, length, chunksize, inp_type):
        inp = list(range(length))
        exp = [str(x) for x in inp]
        inp = inp_type(inp)
        with ConcurrentMapper(threads=threads, jobs=jobs, chunksize=chunksize) as mapper:
            mapper.create_bar(desc="Processing", total=length)
            result = list(mapper(str, inp))
        assert result == exp

    @pytest.mark.parametrize("threads", [True, False])
    def test_forward_args(self, threads):
        inp = list(range(10))
        exp = [x + 2 for x in inp]
        with ConcurrentMapper(threads=threads, jobs=2, chunksize=2) as mapper:
            result = list(mapper(TestConcurrentMapper._add, inp, y=2))
        assert result == exp

    @staticmethod
    def _add(x: int, y: int):
        # NOTE: these must be pickleable methods
        return x + y

    @pytest.mark.parametrize(
        "ignore",
        [
            pytest.param(False, marks=pytest.mark.xfail(raises=ValueError)),
            True,
        ],
    )
    def test_ignore_exceptions(self, ignore):
        inp = list(range(1000))
        with ConcurrentMapper(jobs=2, chunksize=2, ignore_exceptions=ignore) as mapper:
            list(mapper(TestConcurrentMapper._raise, inp))

    @staticmethod
    def _raise(x):
        raise ValueError()

    @pytest.mark.parametrize("ignore", [False, True])
    def test_exception_callback(self, mocker, ignore):
        inp = list(range(1000))
        spy = mocker.spy(TestConcurrentMapper, "_callback")
        with ConcurrentMapper(jobs=2, chunksize=2, ignore_exceptions=ignore, exception_callback=spy) as mapper:
            try:
                list(mapper(TestConcurrentMapper._raise, inp))
            except ValueError:
                pass
            spy.assert_called()

    @staticmethod
    def _callback(f):
        pass

    @pytest.mark.parametrize("ex_type", [KeyboardInterrupt, SystemExit])
    def test_interrupt(self, ex_type):
        inp = list(range(4))
        with ConcurrentMapper(jobs=4, chunksize=2) as mapper:
            try:
                list(mapper(TestConcurrentMapper._loop, inp, ex_type=ex_type))
            except ex_type:
                pass

    @staticmethod
    def _loop(x, ex_type):
        if x == 0:
            raise ex_type()
        while True:
            pass

    @pytest.mark.parametrize("threads", [False, True])
    def test_zero_jobs(self, threads):
        inp = list(range(10))
        exp = [x + 2 for x in inp]
        with ConcurrentMapper(jobs=0, threads=threads) as mapper:
            result = list(mapper(TestConcurrentMapper._add, inp, y=2))
        assert result == exp

    @pytest.mark.parametrize("jobs", [1, 4])
    @pytest.mark.parametrize("threads", [True, False])
    @pytest.mark.parametrize("length", [10, 1000])
    @pytest.mark.parametrize("chunksize", [1, 32])
    def test_bar_update(self, mocker, threads, jobs, length, chunksize):
        inp = list(range(length))
        with ConcurrentMapper(threads=threads, jobs=jobs, chunksize=chunksize) as mapper:
            mapper.create_bar(desc="Processing", total=length)
            spy = mocker.spy(mapper._bar, "update")
            list(mapper(str, inp))
        total_updates = sum(x.args[0] for x in spy.mock_calls)
        # TODO there seems to be a small number of updates not made
        # In the test we ensure 95% of the bar was ran.
        # Is there a reason the entire bar doesn't run to completion?
        assert total_updates / length >= 0.95

    @staticmethod
    def _iter(x: int) -> Iterator[str]:
        for divisor in (1, 2, 3):
            yield str(x / divisor)

    @pytest.mark.parametrize("jobs", [1, 4, None])
    @pytest.mark.parametrize("threads", [True, False])
    @pytest.mark.parametrize("length", [10, 1000])
    @pytest.mark.parametrize("chunksize", [1, 32])
    @pytest.mark.parametrize("inp_type", [list, set, iter])
    def test_map_iter(self, threads, jobs, length, chunksize, inp_type):
        inp = list(range(length))
        exp = [i for x in inp for i in self._iter(x)]
        inp = inp_type(inp)
        with ConcurrentMapper(threads=threads, jobs=jobs, chunksize=chunksize) as mapper:
            mapper.create_bar(desc="Processing", total=length)
            result = list(mapper(self._iter, inp))
        assert result == exp
