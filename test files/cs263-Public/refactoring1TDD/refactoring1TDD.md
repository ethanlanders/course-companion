Title: Refactoring & Regression Testing
TOC: yes
Author: Thomas J. Kennedy


# Looking Back...

In [a lecture during Module 3](doc:functions2) we discussed a paint example,
i.e., <a href="@gitRepoURL@/tree/main/Module-03/Painting-2" target="_blank">Module-03/Painting-2</a>. We
would like to refactor the code... and fix a few implementation and style quirks.


# Adding Tests

Before we refactor the example... let us write a few tests. This is an
opportunity to introduce regression testing. We are going to...

  1. Develop a set of tests for the current code.

  2. Refactor the code.

  3. Run the tests and confirm that nothing has *gone wrong.*

  4. Repeat step 2 and step 3.


Let us start by introducing two test files.

```console
├── compute_paint.py
├── estimate_paint.py
└── tests
    ├── test_compute_paint.py
    └── test_estimate_paint.py
```

We have one test file for `compute_paint.py` and one file for
`estimate_paint.py`.


## Writing the Tests

Let us start with the `compute_paint` module. There are two functions that need
tests:

```python
def wall_surface_area(length: float, width: float) -> float:
    area_one_wall = length * width
    area_four_walls = 4 * area_one_wall
```

and

```python
def gallons_required(
    wall_area: float, min_coverage: float = 350, max_coverage: float = 400
) -> tuple[int, int]:
```

Let us start with `wall_surface_area`...

```python
import pytest

from hamcrest import *

from compute_paint import (wall_surface_area, gallons_required)
```

We need to import:

  1. `pytest` as our testing framework

  2. `hamcrest` for matchers (to write our checks)

  3. `wall_surface_area` and `gallons_required` so that we can use (call/invoke) them



## Introducing Hamcrest Matchers


Each *test* takes the form of a function with *assertions*. Instead of the
built-in Python `assert` or `unittest` module's `assertTrue` or
`assertFalse`... we are using `assert_that`.

If you come from a Java background you may be familiar with [Hamcrest
Matchers](https://hamcrest.org/). Instead of writing a boolean expression in the
form...

```python
assertTrue(num_books == 20)
```

we would like to write something closer to a sentence...

```python
assert_that(num_books, equal_to(20))
```

or

```python
assert_that(num_books, is_(equal_to(20)))
```

The `is_` is purely syntactic sugar (i.e., it exists purely for readability).

```python
    assert_that(wall_surface_area(10, 12), close_to(480, 1e-1))
    assert_that(wall_surface_area(10.5, 10), close_to(420, 1e-1))
```


## Back to Writing Tests

We know that `wall_surface_area`

  1. takes the length and width of a room

  2. returns the total surface area of all four walls

  3. uses `4 * length * width` to compute the surface area


Writing tests is a fairly quick endeavor...

```python
def test_wall_surface_area():
    assert_that(wall_surface_area(1, 1), equal_to(4))
    assert_that(wall_surface_area(1, 2), equal_to(8))
    assert_that(wall_surface_area(2, 2), equal_to(16))
```

However, wall measurements are seldom a nice whole numbers. Walls are usually
something closer to *8 feet 5 inches* than an even *8 feet*. Let us write a
couple *floating point number checks*.

```python
    assert_that(wall_surface_area(10, 12), close_to(480, 1e-1))
    assert_that(wall_surface_area(10.5, 10), close_to(420, 1e-1))
```

Take note of how we are checking for a value within a certain tolerance (e.g., a
number that is within `0.1` of `480` instead of exactly 480). Keep in mind that
`1e-1` is scientific notation for `0.01`.


## Parametrizing the Test

Each check is the same with the exception of the input (length and width) and
expected result (total surface area). We can define a three-tuple (3-tuple) in the form...

```python
test_data = [
    (1, 1, 4),
    (1, 2, 8),
    (2, 2, 16),
    (10, 12, 480),
    (10.5, 10, 420),
]
```

where the first entry is length, the second entry is width, and the final entry
is the expected surface area.

We can then tell `pytest` to run the test once for each tuple using...

```
@pytest.mark.parametrize("length, width, surface_area", test_data)
def test_wall_surface_area(length, width, surface_area):
    assert_that(wall_surface_area(length, width), close_to(surface_area, 1e-1))
```

The first line (`@pytest.mark.parametrize(...)`) tells `pytest` to how to
unpack each tuple. The function itself then needs to be modified to accept
three arguments.

We can now *get away with* a single assertion.

> A [parametrized
> test](https://docs.pytest.org/en/7.1.x/how-to/parametrize.html) is ideal when
> you want to rerun the same test for different inputs.


## Testing the Second Function

We still need to test `gallons_required`. Let us start with a draft...

```python
def test_gallons_required():
    lower, upper = gallons_required(wall_area=1)
    assert_that(lower, equal_to(1))
    assert_that(upper, equal_to(1))

    lower, upper = gallons_required(wall_area=10)
    assert_that(lower, equal_to(1))
    assert_that(upper, equal_to(1))

    lower, upper = gallons_required(wall_area=100)
    assert_that(lower, equal_to(1))
    assert_that(upper, equal_to(1))

    lower, upper = gallons_required(wall_area=1_000)
    assert_that(lower, equal_to(3))
    assert_that(upper, equal_to(3))

    lower, upper = gallons_required(wall_area=1_050)
    assert_that(lower, equal_to(3))
    assert_that(upper, equal_to(3))

    lower, upper = gallons_required(wall_area=1_200)
    assert_that(lower, equal_to(3))
    assert_that(upper, equal_to(4))
```

We start each *check* by invoking `gallons_required` and unpacking the returned
`tuple` into `lower` and `upper`.

However, we need two checks. Separate checks would make sense if we were
dealing with `float` values. But...  `gallons_required` returns a `tuple[int,
int]` (i.e., two `int` values).

We can simplify our `test_gallons_required` function to...

```python
def test_gallons_required():
    assert_that(gallons_required(wall_area=1), equal_to((1, 1)))
    assert_that(gallons_required(wall_area=10), equal_to((1, 1)))
    assert_that(gallons_required(wall_area=100), equal_to((1, 1)))
    assert_that(gallons_required(wall_area=1_000), equal_to((3, 3)))
    assert_that(gallons_required(wall_area=1_050), equal_to((3, 3)))
    assert_that(gallons_required(wall_area=1_200), equal_to((3, 4)))
```

The trick is recognizing the fact that `tuple`s can be compared directly in Python.


# Testing Strings

The tests for `test_estimate_paint.py` will require a different perspective. We
will need to keep in mind:

  1. `get_report` can generate two (2) different reports depending on whether
     `min_gallons == max_gallons`.

  2. comparing two entire strings (expected/correct vs actual) is seldom the
     best approach.

  3. the content of the generated string along with the order of that content
     should ~~usually~~ almost always form the basis of any test.


## Checking the First Case

Let us start by examining the first case (i.e., `min_gallons == max_gallons`).

```python
    actual_report = get_report(min_gallons=4, max_gallons=4, price_per_gallon=35.10)
```

The correct output is known to be...

```console
You will need to buy 4 gallons of paint.
You will spend $ 140.40.
```

One might start by saying...

  1. `4` must appear since that is the correct number of gallons.

    ```python
    assert_that(actual_report, contains_string("4"))
    ```

  2. `140.40` must appear since that is the correct cost.

    ```python
    assert_that(actual_report, contains_string("140.40"))
    ```

However, that does not really capture what we expect... we expect to see a `4`
and then (later in the report) `140.40`.

```python
    assert_that(actual_report, string_contains_in_order("4", "$ 140.40."))
```

That is a better check. However, we know the content of the report...

```python
    assert_that(
        actual_report,
        string_contains_in_order(
            "You will need to buy "
            "4",
            " gallons of paint.",
            "\n",
            "You will spend",
            "$ 140.40."
        )
    )
```

We should (in this case) since the report content is known check for the values
that we expect along with the fixed content (including line breaks).


## Checking the Second Case

The second case can be checked with...

```python
def test_get_report_different_min_max():
    actual_report = get_report(min_gallons=10, max_gallons=14, price_per_gallon=32.50)

    assert_that(
        actual_report,
        string_contains_in_order(
            "You will need to buy "
            "10 to 14",
            " gallons of paint.",
            "\n",
            "You will spend",
            "$ 325.00 to $ 455.00."
        )
    )
```

Take note of how different values were selected. While we could parametrize
this test and check for different values... this function (`get_report`) does
not compute `min_gallons` or `max_gallons`. The values are passed in. We just
need to check the two branches (i.e., `if` and `else`).


# Taking Stock

The two complete test files can be found in
<a href="@gitRepoURL@/tree/main/Module-08/Painting-3-Tests" target="_blank">Module-08/Painting-3-Tests</a>
within the *tests* directory.

The [next lecture](doc:refactoring2Style) will start the actual refactoring and
code review.
