Title: NumPy - Creating Arrays
TOC: yes
Author: Thomas J. Kennedy


# Overview

There are two main ways to initialize NumPy arrays:

  1. Directly in NumPy (e.g., setting everything to zero)
  2. Converting a Python `list` (or similar) structure


# Array from Scratch

NumPy arrays can be...

  - Initialized to all zeroes

    ```python
        array_size = 8
        zeroes_array = np.zeros(array_size)
        print(zeroes_array)
    ```

  - Initialized to all ones

    ```python
        array_size = 12
        ones_array = np.ones(array_size)
        print(ones_array)
    ```

  - Allocated and left uninitialized

    ```python
        # Contents are "whatever happens to be in memory"
        array_size = 16
        unitialized_array = np.empty(array_size)
        print(unitialized_array)
    ```


# Array from a List or Tuple 

Creating an array from an existing list seems straightforward...

```python
    python_list = [2, 4, 8, 16, 32, 64]
    np_array = np.array(python_list)
    print(np_array)
```

However, the resulting array will store `int`s. To create an array of
`float`s... a decimal point must be included after each number.

```python
    python_list = [2., 4., 8., 16., 32., 64.]
    np_array = np.array(python_list)
    print(np_array)
```

You can also be explicit by using the `dtype` keyword argument...

```python
    python_list = [2, 4, 8, 16, 32, 64]
    np_array = np.array(python_list, dtype=np.double)
    print(np_array)
```

# Multiple Dimensions

It is possible to create a matrix (or even a tensor) by providing a multi-level
list, e.g.,

```python
    matrix = [
        [3, 2],
        [2, 5]
    ]

    matrix = np.array(matrix, dtype=np.double)
```


