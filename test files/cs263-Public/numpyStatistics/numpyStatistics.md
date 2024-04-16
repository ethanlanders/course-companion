Title: NumPy - Statistics
TOC: yes
Author: Thomas J. Kennedy


# Overview

NumPy provides a number of operations that are useful for statistics, including
`min`, `max`, and `mean`. The NumPy implementations are more performant that
the vanilla Python equivalents.


# An Example Problem

Suppose we need to compute some grade statistics for the following data.

| Name     | Homework 1 | Homework 2 | Exam 1 | Exam 2 |
| :------- | ----:      | ----:      | ----:  | ----:  |
| John     | 100        | 98         | 100    | 90     |
| Tom      | 100        | 0          | 70     | 90     |
| Bob      | 100        | 70         | 90     | 80     |

The first step is to convert the table into...

  - a list of exercises

    ```python
    exercises = ["Homework 1", "Homework 2", "Exam 1", "Exam 2"]
    ```

  - a list of names

    ```python
    students = ["John", "Tom", "Bob"]
    ```

  - a NumPy `ndarray` to store grades by student (row) vs exercise (column)

    ```python
    grades = np.array([[100., 98, 100., 90.],
                       [100.,  0., 70., 90.],
                       [100., 70., 90., 80.]])
    ```


# NumPy Operations and Axis

NumPy provides a number of [statistics
operations](https://numpy.org/doc/stable/reference/arrays.ndarray.html#array-methods)
that can be applied by axis. For a two-dimensional `ndarray` there are two
choices:

  - by row (student)

    ```python
    avg_by_student = grades.mean(axis=1)
    min_by_student = grades.min(axis=1)
    max_by_student = grades.max(axis=1)
    ```

    |   Name   | Avg  | Min  |  Max  |
    |:---------|-----:|-----:|------:|
    | John     | 97.0 | 90.0 | 100.0 |
    | Tom      | 65.0 |  0.0 | 100.0 |
    | Bob      | 85.0 | 70.0 | 100.0 |

  - by column (exercise)

    ```python
    avg_by_exercise = grades.mean(axis=0)
    max_by_exercise = grades.max(axis=0)
    std_by_exercise = grades.std(axis=0)
    ```

    |   Exercise   |  Avg  |  Max  | Std Dev  |
    |:-------------|------:|------:|---------:|
    | Homework 1   | 100.0 | 100.0 |      0.0 |
    | Homework 2   |  56.0 |  98.0 |     41.2 |
    | Exam 1       |  86.7 | 100.0 |     12.5 |
    | Exam 2       |  86.7 |  90.0 |      4.7 |


Take note of the `axis` keyword argument. For a 2-D `ndarray` a zero (`0`)
indicates analysis by column and a one (`1`) indicates analysis by row.
