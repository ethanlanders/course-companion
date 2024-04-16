Title: NumPy & Multi-Dimension Arrays
TOC: yes
Author: Thomas J. Kennedy


# Perspective

Matrices are often used to solve systems of simultaneous linear equations. In
Linear Algebra... Gaussian Elimination is one of the first techniques taught.
*Note that while this discussion focuses on a matrix solver... you are not
expected to have a Linear Algebra background.*

**The `main` function is omitted intentionally.** One of the lessons, alongside
NumPy, will be on refactoring code. The `main` function will be introduced near
the end of this lecture.


# Pseudocode

The pseudocode for a matrix solver can be broken into four (4) pieces.

  1. Pivot
  2. Scale
  3. Eliminate
  4. Backsolve

Note that *pivot* is included in the driver function.

\bExample{Top Level Pseudocode}

```
# Let `matrix_A` be an n by n matrix with an augmented vector in col n
def solve(matrix_A):

    # Iterate through all rows
    for every i in 0 to n-1:

        # Pivot
        idx <- find_largest_row_by_col(A, col_index, num_rows)
        swap_row(A, i, idx)

        scale(A, i, num_cols, A[i][i])
        A[i][i] = 1

        eliminate(A, i, num_rows)
```
\eExample

\bExample{Scale}

```
def scale_row(A, row_idx, num_cols, s):

    for every j in 0 to num_cols:
        A[row_idx][j] = A[row_idx][j] / s

```

\eExample


\bExample{Eliminate}

```
def eliminate(A, src_row_idx, num_cols, num_rows):

    start_col <- src_row_idx

    for every i in (src_row_idx + 1) to num_rows:

        s <- A[i][start_col]

        for every j in start_col to num_cols:
            A[i][j] = A[i][j] - s * A[src_row_idx][j]

        A[i][start_col] = 0

```

\eExample

\bExample{Backsolve}

```
def back_solve(matrix):

    augColIdx <- matrix.cols()  # the augmented column
    lastRow = matrix.rows() - 1

    for i in lastRow down to 1:
        for j <- (i - 1) down to 0:
            s <- matrix[j][i]

            matrix[j][i] -= (s * matrix[i][i])
            matrix[j][augCol] -= (s * matrix[i][augColIdx])
```

\eExample


# Implementing the Solver

The initial implementation will use `np.array` objects. However, the
implementation will forgo most NumPy functions, relying heavily on
vanilla Python.


## What About Best Practices?

The initial implementation will be **rough** or **crude**. It will work. It
will get the job done. The implementation will need **a lot** of clean up. The
follow-up implementations will incorporate Python conventions with some NumPy
functionality.


## The Driver

The first piece of pseudocode can be written, in Python, in a `solve_matrix`
function...

```python
def solve_matrix(matrix_XTX, matrix_XTY):
    """
    Solve a matrix and return the resulting solution vector
    """

    # Get the dimensions (shape) of the XTX matrix
    num_rows, num_columns = matrix_XTX.shape

    # Placeholder until the interfaces for each function are defined
    for i in range(0, num_rows):
        pass
```

Note the use of the `.shape` tuple to retrieve the number of rows and columns
in `matrix_XTX`.


## Pivot

The pivot operation can be completed in two steps:

  1. look down the current column and find the row with the largest value in
     that column
  2. swap the *largest row* with the *current row* 

The pseudocode, coincidentally, is also two lines...

```
    idx <- find_largest_row_by_col(A, col_index, num_rows)
    swap_row(A, i, idx)
```

A naive implementation is more than two lines.

```python
def find_largest_row_by_col(matrix, col_index):
    num_rows, _ = matrix.shape

    i = col_index
    largest_idx = i
    current_col = i
    for j in range(i + 1, num_rows):
        if matrix[largest_idx, i] < matrix[j, current_col]:
            largest_idx = j

    return largest_idx


def swap_rows(matrix_XTX, matrix_XTY, largest_idx, i):
    if largest_idx != i:
        matrix_XTX[[i, largest_idx], :] = matrix_XTX[[largest_idx, i], :]
        matrix_XTY[[i, largest_idx]] = matrix_XTY[[largest_idx, i]]
```

### Indices - Row and Column

NumPy provides extensions to the Python index syntax. Consider...

```python
matrix[largest_idx, i]
```

This excerpt specifies that a value is being retrieved from row `largest_idx`
and column `i` within that row.


### Indices - Entire Rows

Consider the somewhat intimidating... 

```python
matrix_XTX[[i, largest_idx], :]
```

This line grabs the rows at two indices (i.e., `i` and `largest_idx`) and every
column within those rows.


## Scale

The scale pseudocode calls for a loop.

```
def scale_row(A, row_idx, num_cols, s):

    for every j in 0 to num_cols:
        A[row_idx][j] = A[row_idx][j] / s
```

However, we can use NumPy's broadcast mechanic to scale every column within a
row.

```python
def scale_row(matrix_XTX, matrix_XTY, i):
    scaling_factor = matrix_XTX[i, i]
    matrix_XTX[i, :] /= scaling_factor
    matrix_XTY[i] /= scaling_factor
```


## Eliminate

The eliminate logic takes the current row and subtracts it from every
subsequent row.

```
def eliminate(A, src_row_idx, num_cols, num_rows):

    start_col <- src_row_idx

    for every i in (src_row_idx + 1) to num_rows:

        s <- A[i][start_col]

        for every j in start_col to num_cols:
            A[i][j] = A[i][j] - s * A[src_row_idx][j]

        A[i][start_col] = 0

```

The pseudocode starts of by accessing the `.shape` property and discards the
number of columns (since we only need the number of rows).


```python
def eliminate(matrix_XTX, matrix_XTY, i):
    num_rows, _ = matrix_XTX.shape

    for row_i in range(i + 1, num_rows):
        s = matrix_XTX[row_i][i]

        matrix_XTX[row_i] = matrix_XTX[row_i] - s * matrix_XTX[i]
        matrix_XTY[row_i] = matrix_XTY[row_i] - s * matrix_XTY[i]
```

Note how we take row `i`, multiply every value in the row by `s` and then
subtract it from row `row_i`. **Have you noticed a pattern varaible names
(specifically indices)? They are anything but self-documenting.** These naming
issues will be part of our follow-up refactoring discussion. 


## Backsolve

The backsolve operation is the final step. Now that we have worked our way to
the last row of the matrix (and ended up with an upper triangular matrix)... we
can work our way back up.

```
def back_solve(matrix):

    augColIdx <- matrix.cols()  # the augmented column
    lastRow = matrix.rows() - 1

    for i in lastRow down to 1:
        for j <- (i - 1) down to 0:
            s <- matrix[j][i]

            matrix[j][i] -= (s * matrix[i][i])
            matrix[j][augCol] -= (s * matrix[i][augColIdx])
```

The pseudocode once again seems to differ from the implementation. The
pseudocode has a single matrix while the implementation has two. The why will
be discussed during the follow-up refactoring discussion.

```python
def _backsolve(matrix_XTX, matrix_XTY):

    num_rows, _ = matrix_XTX.shape

    for i in reversed(range(1, num_rows)):
        for j in reversed(range(0, i)):
            s = matrix_XTX[j, i]

            matrix_XTX[j, i] -= (s * matrix_XTX[i, i])
            matrix_XTY[j] -= (s * matrix_XTY[i])
```

Take note of the leading underscore. By convention... any function that starts
with a "`_`" is to be treated as an implementation detail.


# What About `main`?

As promised... we will discuss the main function. Before `solve` is ever called
we set up some input data.

```python
    # Set up input data points, X, Y, and XT
    points = [(0., 0.), (1., 1.), (2., 4.)]
```

We have three input points for which we would like to compute a polynomial of
best fit. The polynomial will be of degree two (2) and take the form...

$$
\hat{\varphi} = c_0 + c_1 x + c_2 x^2
$$

where $c_0$, $c_1$, and $c_2$ are the unknowns for which we are solving.


The $X$ matrix is defined as...

```python
    # Set up X, Y, and XT matrices 
    matrix_X = np.array([[1., 0., 0.],
                         [1., 1., 1.],
                         [1., 2., 4.]])
```

The $Y$ matrix is defined as...

```python
    matrix_Y = np.array([0,
                         1,
                         4])
```

The transpose of $X$ (i.e. $X^T$) can be obtined using NumPy's `transpose`
method.

```python
    matrix_XT = matrix_X.transpose()
```

We need to perform two matrix multiplications. My preference is to call
`np.matmul`.

```python
    # Compute XTX and XTY
    matrix_XTX = np.matmul(matrix_XT, matrix_X)
    matrix_XTY = np.matmul(matrix_XT, matrix_Y)
```

However, some NumPy code will use the `@` operator, e.g.,

```python
    matrix_XTX = matrix_XT @ matrix_X
```

The `print_matrices` function is used for debugging. However, it should be
replaced with the `pprint` module.

```python
    print_matrices(matrix_XTX, matrix_XTY)
```

The rest of main is just outputting the results.

```python
    print()
    print("{:-^40}".format("Solution"))
    solution = solve_matrix(matrix_XTX, matrix_XTY)
    print(solution)
```

# But... What is the Output?

If you run the [code from this
lecture](@gitRepoURL@/blob/main/Module-11/least_squares_initial.py) using

```sh
python3.11 least_squares_initial.py
```

you will obtain, as output...

> **Sample Output**
>
> ```
> ******************XTX*******************
> [[ 3.  3.  5.]
>  [ 3.  5.  9.]
>  [ 5.  9. 17.]]
> 
> ******************XTY*******************
> [ 5.  9. 17.]
> 
> ----------------Solution----------------
> [0. 0. 1.]
> ```

We can make the output a little more readable...

```
0.0 + 0.0·x + 1.0·x²
```

The trick is to replace...

```python
    print(solution)
```

with

```python
    print(np.polynomial.Polynomial(solution))
```

which uses the [NumPy `Polynomial`
class](https://numpy.org/doc/stable/reference/routines.polynomials.html) to
generate more *presentable* output.


# Where is the Refactoring?

Refactoring the code from this discussion will a separate lecture (i.e., the
very next lexture).
