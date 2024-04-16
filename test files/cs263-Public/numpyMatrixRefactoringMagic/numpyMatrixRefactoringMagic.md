Title: NumPy & Multi-Dimension Arrays - NumPy Magic
TOC: yes
Author: Thomas J. Kennedy


# Where are We?

In [the previous lecture](doc:numpyMatrixExampleRefactoring), we have just
finished refactoring the *Least Squares Approximation Solver.*

This lecture will focus on a second *refactoring pass* through the solver code.
The [code generated in this lecture can be accessed on
GitHub](@gitRepoURL@/blob/main/Module-11/least_squares_better_2.py).


# Back to main

I am not entirely satisfied with `main`.

```python
def main():
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0)]

    # Compute X
    x_values = [x for x, _ in points]
    x_values = np.array(x_values)
    x_values_squared = x_values ** 2
    matrix_X = np.column_stack((np.ones(len(points)), x_values, x_values_squared))

    # Compute Y
    matrix_Y = np.array([y for _, y in points])
```

The first list (i.e., `points`) represents our input data. We end up creating
`x_values` and `y_values` based on these points. If this were part of a larger
application... the points would come from an input file. Let us introduce a new
function that takes the points and returns two lists.

```python
def get_x_and_y_values(points: list[tuple[float, float]]) -> tuple[np.array, np.array]:
    """
    Take a list of points and return a list of x values and a list of y values
    """

    x_values = [x for x, _ in points]
    x_values = np.array(x_values)

    y_values = np.array([y for _, y in points])

    return x_values, y_values
```

The logic for splitting the points into two `np.array` objects should its own
function.


## Getting x_values and y_values

We can still improve this function. If we take...

```python
    x_values = [x for x, _ in points]
    x_values = np.array(x_values)
```

the lines can be combined into one...

```python
    x_values = np.array([x for x, _ in points])
```

We can make the same tweak to the line for `y_values`.

```python
    y_values = np.array([y for _, y in points])
```

The final function ends up as two lines (not including the return).

```python
def get_x_and_y_values(points: list[tuple[float, float]]) -> tuple[np.array, np.array]:
    """
    Take a list of points and return a list of x values and a list of y values
    """

    x_values = np.array([x for x, _ in points])
    y_values = np.array([y for _, y in points])

    return x_values, y_values
```

But... we can make the process a little cleaner with `hsplit`. Why not convert
the points to an `np.array` with...

```python
np.array(points)
```

and the split the columns into two lists...

```python
    x_values, y_values = np.hsplit(np.array(points), 2)
```

Note that the `2` indicates a split into two (2) `np.array` objects (one for
each column).

The real final function is actually...

```python
def get_x_and_y_values(points: list[tuple[float, float]]) -> tuple[np.array, np.array]:
    """
    Take a list of points and return a list of x values and a list of y values
    """

    x_values, y_values = np.hsplit(np.array(points), 2)

    return x_values, y_values
```


## Back to main

The output in main is a bit tricky. While `.format` is useful, we need to
center string literals for titles.

```python
    print("{:*^40}".format("XTX"))
```

I believe the string `.center` member function is a more readable and
self-documenting choice.

```python
    print("XTX".center(40, "*"))
```

Let us make that change to every heading and finalize main...

```python
def main():
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0)]

    x_values, y_values = get_x_and_y_values(points)

    # Compute X and XT
    x_values_squared = x_values ** 2
    matrix_X = np.column_stack((np.ones(len(points)), x_values, x_values_squared))

    matrix_XT = matrix_X.transpose()

    # Compute Y
    matrix_Y = y_values

    # Compute XTX and XTY
    matrix_XTX = np.matmul(matrix_XT, matrix_X)
    matrix_XTY = np.matmul(matrix_XT, matrix_Y)

    # Construct augmented XTX|XTY matrix 
    matrix_XTY = matrix_XTY.reshape(matrix_XTX.shape[0], 1)
    matrix_augmented = np.hstack((matrix_XTX, matrix_XTY))

    print("XTX".center(40, "*"))
    print(matrix_XTX)

    print()
    print("XTY".center(40, "*"))
    print(matrix_XTY)

    print()
    print("XTX|XTY".center(40, "*"))
    print(matrix_augmented)

    solution = solve_matrix(matrix_augmented)

    print()
    print("Solution".center(40, "*"))
    print(np.polynomial.Polynomial(solution))
```


# Looking at solve_matrix

The `solve_matrix` itself is little more than a loop where other functions are
invoked.

```python
def solve_matrix(matrix_augmented: np.array) -> np.array:
    """
    Solve a matrix and return the resulting solution vector

    Args:
        matrix_augmented: an n-by-n matrix with a vector augmented in the
        right-most column

    Returns:
        constants c_0, c_1, c_2, ... c_n depending on the number of rows in the
        supplied matrix
    """

    # Get the number of rows in the matrix
    num_rows, _ = matrix_augmented.shape

    for current_row_idx in range(0, num_rows):
        swap_current_row_with_largest_row(matrix_augmented, current_row_idx)
        scale_row(matrix_augmented, current_row_idx)
        eliminate(matrix_augmented, current_row_idx)

    _backsolve(matrix_augmented)

    return matrix_augmented[:, -1].flatten()
```

**There is no refactoring left in this top-level function.**


## Swapping the Largest Row

The `swap_current_row_with_largest_row` can be simplified with some NumPy
**magic**. Let us take another look at the *find largest row* logic.

```python
    num_rows, _ = matrix.shape

    # Find the row with the largest column entry
    row_idx = current_idx
    largest_idx = row_idx
    current_col = current_idx
    for j in range(row_idx + 1, num_rows):
        if matrix[largest_idx, row_idx] < matrix[j, current_col]:
            largest_idx = j
```

The first three lines are variable declarations and definitions. However, the
loop itself can be replaced with a call to `argmax`. This function (i.e.,
`argmax`) will return the position (index) of the largest entry in an
`np.array`.

```python
        largest_idx = idx + np.argmax(matrix[idx:, :], axis=0)[idx]
```

Well... that code snippet is clear (as mud). Let us break the code into pieces:

  - `axis=0` - find the maximum entry in each column.

  - `matrix_augmented[idx:, :]` - search every column in every row, starting at row "`idx`".

  - '[idx]' - our interest lies with the row for the largest entry in column "`idx`".

  - `idx + np.argmax(` - the search started at row "`idx`" (which is treated as
    index 0). We need to *shift* back to the full set of rows.

That allows us to replace an entire loop with three lines.

```python
    # Find the row with the largest column entry
    idx = current_idx
    largest_idx = idx + np.argmax(matrix[idx:, :], axis=0)[idx]

    # If the current row is not the largest row then swap
    if largest_idx != current_idx:
        matrix[[current_idx, largest_idx], :] = matrix[[largest_idx, current_idx], :]
```

The remainder of the function can remain unchanged.


# Being Persnickety 

The `scale_row` function makes use of `/=`.

```python
    scaling_factor = matrix[current_row_idx, current_row_idx]
    matrix[current_row_idx, :] /= scaling_factor
```

I would prefer for the division operation to be a multiplication. This can be
done with...

```python
    scaling_factor = matrix[current_row_idx, current_row_idx]
    scaling_factor = np.reciprocal(scaling_factor)
```

or...

```python
    scaling_factor = np.reciprocal(matrix[current_row_idx, current_row_idx])
```

Let us make use of the latter option. The end result is...

```python
def scale_row(matrix: np.array, current_row_idx: int) -> None:
    """
    Scale every entry of the current row by the value of the corresponding
    column (e.g., matrix[2,2])
    """

    scaling_factor = np.reciprocal(matrix[current_row_idx, current_row_idx])
    matrix[current_row_idx, :] *= scaling_factor
```

# The End... For Real This Time

This is the end of the refactoring journey. The [final code can be accessed on
GitHub](@gitRepoURL@/blob/main/Module-11/least_squares_better_2.py).
