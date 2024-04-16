Title: NumPy & Multi-Dimension Arrays - Refactoring
TOC: yes
Author: Thomas J. Kennedy


# Where Did We Leave Off?

In [the previous lecture](doc:numpyMatrixExample) we implemented a matrix
solver using NumPy. We left off with a discussion of the `main` function.

```python
def main():

    # Set up input data points, X, Y, and XT
    points = [(0., 0.), (1., 1.), (2., 4.)]

    # Set up X, Y, and XT matrices 
    matrix_X = np.array([[1., 0., 0.],
                         [1., 1., 1.],
                         [1., 2., 4.]])

    matrix_Y = np.array([0,
                         1,
                         4])

    matrix_XT = matrix_X.transpose()

    # Compute XTX and XTY
    matrix_XTX = np.matmul(matrix_XT, matrix_X)
    matrix_XTY = np.matmul(matrix_XT, matrix_Y)

    print_matrices(matrix_XTX, matrix_XTY)

    print()
    print("{:-^40}".format("Solution"))
    solution = solve_matrix(matrix_XTX, matrix_XTY)
    print(solution)
```


# Where to Start?

I would like to start with `points`, `matrix_X`, and `matrix_Y`. The convention
here is not truly snake case. However, the `X` and `Y` are the names used in
mathematical notations. The compromise you see here is to prefix them both
with `matrix_`.

So... the names will be left alone. However, `points` is an issue. While the
points captured in the list of tuples do serve as the source of our data...
they are never actually used. We can fix that by changing

```python
    # Set up input data points, X, Y, and XT
    points = [(0., 0.), (1., 1.), (2., 4.)]

    # Set up X, Y, and XT matrices 
    matrix_X = np.array([[1., 0., 0.],
                         [1., 1., 1.],
                         [1., 2., 4.]])
```

to 

```python
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0)]

    x_values = [x for x, _ in points]
    x_values = np.array(x_values)
    x_values_squared = x_values ** 2
    matrix_X = np.column_stack((np.ones(len(points)), x_values, x_values_squared))
```

The first change was to each point. I believe that `.0` is more natural than
just a decimal point.

The first real change was to how `matrix_X` is defined:

  1. `x_values` starts of a list comprehension to grab just the `x` value of
     each point.

  2. `x_values` is turned into an `np.array`

  3. `x_values_squared` uses NumPy's broadcast functionality to square each
     entry. 

  4. `np.ones(len(points))` creates an `np.array` with three (3) ones (which
     matches the number of points).

  5. `np.ones(len(points))`, `x_values`. and `x_values_squared` are placed into
     a tuple

  6. The tuple is passed to `cp.column_stack` which uses the three arrays as
     column zero, column one, and column two, respectively.

The `Y` matrix is a one liner.

```python
    matrix_Y = np.array([y for _, y in points])
```

This time a list comprehension was used to grab the y value of each point.

**We could factor this setup out into a `get_matrices` function.** However, we
do want to refactor more than just `main`.


## The `main` Function So Far

Let us take a moment to examine `main` with the changes made thus far.

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

    matrix_XT = matrix_X.transpose()

    # Compute XTX and XTY
    matrix_XTX = np.matmul(matrix_XT, matrix_X)
    matrix_XTY = np.matmul(matrix_XT, matrix_Y)

    print_matrices(matrix_XTX, matrix_XTY)

    print()
    print("{:-^40}".format("Solution"))
    solution = solve_matrix(matrix_XTX, matrix_XTY)
    print(np.polynomial.Polynomial(solution))
```

Make note of the last line. The use of `np.polynomial.Polynomial` was mentioned
at the end of the previous lecture.


## Merging the Matrices

While there is quite a bit of refactoring to perform in general. I would like
to rewrite the code to work with a single augmented matrix (that is one where
`matrix_XTY` is added as the last column of `matrix_XTX`).

```python
    matrix_XTY = matrix_XTY.reshape(matrix_XTX.shape[0], 1)
    matrix_augmented = np.hstack((matrix_XTX, matrix_XTY))
```

These two lines are tricky. We want to take `matrix_XTY` which contains three
`float`s...

```
[ 5.  9. 17.]
```

and turn it into a `list` of `list`s that each contain one `float`...

```
[[ 5.]
 [ 9.]
 [17.]]
```

The reshape line takes care of this by getting the number of rows in
`matrix_XTX` and reshaping `matrix_XTY` from *one row of three values* into
*three rows which each contain one (1) value*. 

The second line uses `np.hstack` to append the corresponding entries to each
row of `matrix_XTX`. This yields our final `main` (for now)...

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

    matrix_XT = matrix_X.transpose()

    # Compute XTX and XTY
    matrix_XTX = np.matmul(matrix_XT, matrix_X)
    matrix_XTY = np.matmul(matrix_XT, matrix_Y)

    print_matrices(matrix_XTX, matrix_XTY)

    matrix_XTY = matrix_XTY.reshape(matrix_XTX.shape[0], 1)
    matrix_augmented = np.hstack((matrix_XTX, matrix_XTY))
    print(matrix_augmented)

    solution = solve_matrix(matrix_augmented)

    print()
    print("{:-^40}".format("Solution"))
    print(np.polynomial.Polynomial(solution))
```

Of course... now we need to rewrite `solve_matrix` to work with a single
augmented matrix.


# Updating the Solver

Now... this is the fun part. The `solve_matrix` function needs be rewritten to
work with an augmented matrix. That means...

```python
def solve_matrix(matrix_XTX, matrix_XTY):
    """
    Solve a matrix and return the resulting solution vector
    """

    # Get the dimensions (shape) of the XTX matrix
    num_rows, num_columns = matrix_XTX.shape
```

needs have three immediate changes made.

  1. The function must accept a single augmented matrix.

    ```python
    def solve_matrix(matrix_augmented: np.array) -> np.array:
    ```

    Take note of the addition of *type hints*. The solve function both accepts
    an `np.array` and returns an `np.array`.

  2. The docstring must be rewritten.

    ```python
        """
        Solve a matrix and return the resulting solution vector

        Args:
            matrix_augmented: an n-by-n matrix with a vector augmented in the
            right-most column

        Returns:
            constants c_0, c_1, c_2, ... c_n depending on the number of rows in the
            supplied matrix
        """
    ```

  3. We need to retrieve the number of rows in the matrix, but we can ignore
     the number of columns.

    ```python
        # Get the number of rows in the matrix
        num_rows, _ = matrix_augmented.shape
    ```


## The Solver Loop

Let us rewrite the solver loop to use `current_row_idx` instead of `i` as the
loop counter.

```python
    for current_row_idx in range(0, num_rows):
        # Find column with largest entry
        largest_idx = find_largest_row_by_col(matrix_augmented, current_row_idx)

        # Swap
        current_col = current_row_idx
        swap_rows(matrix_augmented, largest_idx, current_col)

        # Scale
        scale_row(matrix_augmented, current_row_idx)

        # Eliminate
        eliminate(matrix_augmented, current_row_idx)

    _backsolve(matrix_augmented)
```

I also took the opportunity to update each function call within the loop. *Note
that the functions invoked (called) within the loop still need to be updated.
This change temporarily breaks the code.*


### Updating swap_rows

When we run the code (in its current form) the following error is generated:

```
TypeError: swap_rows() missing 1 required positional argument: 'i'
```

While updating swap rows could be our next step... I want to look at the
preceding lines of code...

```python
    for current_row_idx in range(0, num_rows):
        # Find column with largest entry
        largest_idx = find_largest_row_by_col(matrix_augmented, current_row_idx)

        # Swap
        current_col = current_row_idx
        swap_rows(matrix_augmented, largest_idx, current_col)
```

These first four lines (not including the blank line) are really one operation.
Both `largest_idx` and `current_col` are used *exclusively* as arguments to
`swap_rows`.

Let us combine these operations into a single new function named
`swap_current_row_with_largest_row`.

```python
def swap_current_row_with_largest_row(matrix: np.array, current_idx: int) -> None:
    """
    Find the row (starting with the current row) with the largest entry in the
    column with the same index as the current row (e.g., matrix[1,1]). Consider
    only rows below the current one.

    Args:
        matrix: augmented matrix to update

        current_idx: current row (and column) index
    """
```

Let us make a point of writing pydoc documentation and type hints for any new
or updated functions.

The first part of the function will be an updated version of the *find largest
column entry logic.*

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

For the moment... we will stick with a loop. In a future tweak... this loop
will be replace with some NumPy *magic*. The next step is to add the *swap*
logic.

```python
    # If the current row is not the largest row then swap
    if largest_idx != current_idx:
        matrix[[current_idx, largest_idx], :] = matrix[[largest_idx, current_idx], :]
```

With those changes... our solver loop no longer requires comments... since the
function calls are now self documenting.

```python
    for current_row_idx in range(0, num_rows):
        swap_current_row_with_largest_row(matrix_augmented, current_row_idx)
        scale_row(matrix_augmented, current_row_idx)
        eliminate(matrix_augmented, current_row_idx)
```


### Updating scale_row

The `scale_row` method can be updated fairly quickly.

```python
def scale_row(matrix: np.array, current_row_idx: int) -> None:
    """
    Scale every entry of the current row by the value of the corresponding
    column (e.g., matrix[2,2])
    """

    scaling_factor = matrix[current_row_idx, current_row_idx]
    matrix[current_row_idx, :] /= scaling_factor
```

The function itself (barring the renamed variables) is same as before, but with
a single scale operation instead of two.


### And Now... eliminate

The `eliminate` function can now be written as...

```python
def eliminate(matrix: np.array, current_row_idx: int) -> None:
    """
    Subract multiples of the current rows from all rows below it. Once this
    function completes all rows below this one will contain zero in the
    "current_row_idx" column
    """

    num_rows, _ = matrix.shape

    for row_i in range(current_row_idx + 1, num_rows):
        scaling_factor = matrix[row_i][current_row_idx]

        matrix[row_i] = matrix[row_i] - scaling_factor * matrix[current_row_idx]
```

Take note of the variables that were renamed. Let us be sure to replace any
single letter variable names with more descriptive identifiers.


### Finally... `_backsolve`

The last function is `_backsolve`.

```python
def _backsolve(matrix: np.array) -> None:
    """
    Back solve the matrix by performing the necessary row scale and subtraction
    operations to obtain a diagonal matrix with ones on the diagonal.

    The augmented column will contain the solution.

    Args:
        matrix: augmented matrix
    """
    num_rows, _ = matrix.shape

    for i in reversed(range(1, num_rows)):
        for j in reversed(range(0, i)):
            scaling_factor = matrix[j, i]

            matrix[j, i] -= scaling_factor * matrix[i, i]
            matrix[j, -1] -= scaling_factor * matrix[i, -1]
```

Since this function starts with an upper-triangular matrix... we know that for
each row every column to the left of index "`i`" is zero. This means we only
need to subtract column "`i`" and the augmented column from each row above row
"`i`".

We can actually combine the two lines using *NumPy magic*.

```python
           matrix[j, [i, -1]] -= scaling_factor * matrix[i, [i, -1]]
```

The `matrix[j, [i, -1]]` specifies that we want to retrieve **only** column
"`i`" and the last column (i.e., `-1`) from row "`j`".


## Back to the Solve Loop

We need to make one final edit to the `solve_matrix` function. Yes... I know
that the return happens after the loop. But... I needed a section heading
(naming things is hard).

The previous return statement no longer works.

```python
    return matrix_augmented
```

We do not want to return the entire matrix. We only need the last column...

```python
    return matrix_augmented[:, -1].flatten()
```

Notice the `.flatten()`? We do not want an array of arrays, e.g.,

```
[[0], [0], [1]]
```

We want to remove the inner level or arrays and end up with...

```
[0, 0, 1]
```

## Where is the Code?

The <a href="@gitRepoURL@/blob/main/Module-11/least_squares_better_1.py" target="_blank">refactored code can be accessed directly here</a>.
You will notice a small change in the output logic.

```python
    print("{:*^40}".format("XTX"))
    print(matrix_XTX)

    print()
    print("{:*^40}".format("XTY"))
    print(matrix_XTY)

    print()
    print("{:*^40}".format("XTX|XTY"))
    print(matrix_augmented)

    solution = solve_matrix(matrix_augmented)

    print()
    print("{:-^40}".format("Solution"))
    print(np.polynomial.Polynomial(solution))
```

The `print_matrices` function has been removed. All output logic (which now
includes the augmented matrix) happens directly in `main`.

> **Current Output**
>
> ```
> ******************XTX*******************
> [[ 3.  3.  5.]
>  [ 3.  5.  9.]
>  [ 5.  9. 17.]]
> 
> ******************XTY*******************
> [[ 5.]
>  [ 9.]
>  [17.]]
> 
> ****************XTX|XTY*****************
> [[ 3.  3.  5.  5.]
>  [ 3.  5.  9.  9.]
>  [ 5.  9. 17. 17.]]
> 
> ----------------Solution----------------
> 0.0 + 0.0·x + 1.0·x²
> ```


# Where is the NumPy Magic?

There is still a bit of tweaking left. There are a few places where NumPy can
both simplify the code and make the code more performant. **However, that will
be covered in the next lecture.**
