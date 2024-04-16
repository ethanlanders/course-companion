Title: NumPy - Broadcasting
TOC: yes
Author: Thomas J. Kennedy


# Getting Started

The next couple snippets are extracted from
<a href="@gitRepoURL@/blob/main/Module-11/broadcasting.py" target="_blank">broadcasting.py</a>.


# Loops & Comprehensions

In Python... each element of a list must be updated one at a time. If a list of
prices needed to be reduced by 10%, each one would need to be multiplied by 0.9
within a loop...

```python
    prices = [1.00, 2.95, 8.40, 3.50, 3.30, 16.91]

    for idx in range(len(prices)):
        price[idx] *= 0.9
```

or using a [list comprehension](doc:comprehensions1)...

```python
    prices = [1.00, 2.95, 8.40, 3.50, 3.30, 16.91]
    prices = [0.9 * price for price in prices]

    print(prices)
```

# NumPy Broadcasting

NumPy's broadcasting mechanic allows us to write a simple `prices *= 0.9`.

```python
    prices = np.array([1.00, 2.95, 8.40, 3.50, 3.30, 16.91])
    prices *= 0.9

    print(prices)

    print()
    print("*" * 80)
    print()
```

The obvious benefit is less typing. The more important one is optimization.
NumPy's core is implemented in C. The official NumPy Documentation provides a
succinct overview in its [Why is NumPy
Fast?](https://numpy.org/doc/stable/user/whatisnumpy.html#why-is-numpy-fast)
section. 


# Benchmarks & Performance

How much faster is NumPy? Let us run a quick using <a href="@gitRepoURL@/blob/main/Module-11/benchmark_broadcasting.py" target="_blank">benchmark_broadcasting.py</a>.

```python
    num_values = 1000000
    num_runs = 100

    def op_wrapper_py():
        prices = range(1, num_values, 1)
        prices = [0.9 * price for price in prices]

    py_list = timeit.timeit(op_wrapper_py, number=num_runs)

    def op_wrapper_np():
        prices = np.arange(0, num_values, 1, dtype=np.float64)
        prices[:] *= 0.9

    np_array = timeit.timeit(op_wrapper_np, number=num_runs)

    print(f"Python Time: {py_list:.4f}")
    print(f"NumPy Time : {np_array:.4f}")
```

On a Core i7-6700k... For 1 million numbers, run 100 times... The NumPy code is
a little over 10 times faster than the pure Python code.

|        | Time (sec) |
| :---   | ---:       |
| Python | 5.1248     |
| NumPy  | 0.3168     |

