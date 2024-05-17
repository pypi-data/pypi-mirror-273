# TQDM Multiprocessing

Helper repository for running parallelized tasks on a large number of inputs with responsive progress bars via tqdm.

## Usage

```python
iterable = list(range(5))
func = lambda x, y: x+y
with ConcurrentMapper(jobs=8, threads=False) as mapper:
     mapper.create_bar(desc="Processing", total=len(iterable))
     result = mapper(func, iterable, y=1)
 print(result) # [1, 2, 3, 4, 5]
```
