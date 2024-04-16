Title: Refactoring & Adding Functionality
TOC: yes
Author: Thomas J. Kennedy


# Where is Next?

We would like to continue the example from the previous lecture, i.e.,
<a href="@gitRepoURL@/tree/main/Module-08/Painting-4-Style" target="_blank">Module-08/Painting-4-Style</a>.
We will doing two things during this lecture:

  1. Tweaking the existing code

  2. Adding user input

  3. Adding new functionality


# Starting with "main"

Let us start in `main` within the `estimate_paint` module.

\bExample{Before Changes - main}

```python
def main():
    """
    This is the driver logic for the program. The length, width, and price per
    gallon are currently hardcoded.

    TODO: add user input
    """
    # Dimensions in feet
    length = 50
    width = 40

    # Price in dollars
    price_per_gallon = 49.95

    area = compute_paint.wall_surface_area(length, width)

    min_required, max_required = compute_paint.gallons_required(area)

    summary = get_report(min_required, max_required, price_per_gallon)
    print(summary)
```

\eExample

I would like to actually have the user enter some values. Let us add a
`gather_input` function that checks `sys.argv` for command line arguments and
prompts the user in the case where no such arguments were supplied.


\bExample{New Function - gather_input}

```python
def gather_input(args: list[str]) -> tuple[float, float, float]:
    """
    Check the supplied `args` for three (3) user supplied arguments (for a
    total length of 4). If three arguments were not supplied then prompt the
    used for length (in feet), width (in feet), and price per gallon.

    Args:
        args: command line arguments to process

    Returns:
        a three-tuple in the form (length, width, price_per_gallon)
    """

    # Command Line Arguments were supplied
    if len(args) == 4:
        length = float(args[1])
        width = float(args[2])

        price_per_gallon = float(args[3])

    else:
        length = float(input("Enter the room length: "))
        width = float(input("Enter the room width: "))

        price_per_gallon = float(input("Enter the cost per gallon of paint:  "))

    return length, width, price_per_gallon
```

\eExample

`main` can now retrieve the values by calling `gather_input` and unpacking
the values from the returned three-tuple.

```python
    length, width, price_per_gallon = gather_input(sys.argv)
```

Take note of how `sys.argv` was passed into `gather_inputs` as an argument.
This decision was based on two criteria:

  1. Testing is easier.

  2. Accessing global variables (along with global variables themselves)
     should be minimized.


# Writing New Tests

Let us add a couple tests for this new `gather_inputs` function:

  1. One for input from `sys.argv`.

    ```python
    def test_gather_input_cli_arg():
        length, width, unit_cost = gather_input([None, "40", "50", "49.95"])
        assert_that(length, close_to(40, 1e-3))
        assert_that(width, close_to(50, 1e-3))
        assert_that(unit_cost, close_to(49.95, 1e-3))
    ```

    1. We start by creating a list with four (4) entries. The `None` represents
       where the program name would be located.

    2. We unpack `length`, `width`, and `unit_cost` from the returned
       three-tuple.

    2. We check that `length`, `width`, and `unit_cost` are within `0.001` of
       their expected values/

  2. One for input from `sys.stdin` (i.e., from `input`).

    ```python
    def test_gather_input_input(monkeypatch):
        faked_input = StringIO("40\n50\n49.95\n")
        monkeypatch.setattr("sys.stdin", faked_input)

        length, width, unit_cost = gather_input([])
        assert_that(length, close_to(40, 1e-3))
        assert_that(width, close_to(50, 1e-3))
        assert_that(unit_cost, close_to(49.95, 1e-3))
    ```

    1. We start by creating a `StringIO` object that contains the length,
       width, and price inputs, separated by newlines (`\n`)

    2. We use `monkeypatch` to replace `sys.stdin` (i.e., intercept calls to
       `input`)

    3. We unpack `length`, `width`, and `unit_cost` from the returned
       three-tuple.

    4. We check that `length`, `width`, and `unit_cost` are within `0.001` of
       their expected values/

**We should technically handle parsing errors. However, that will be discussed
in a separate lecture and separate example.**



# Painting More Coats

I imagine that you have been wondering how *someone who used to work as a
painter* wrote a program that assumes a room can be painted in one coat. Two
(2) coats is always the minimum (unless it is a rental property).

Let us update the program to give us estimates for two (2), three (3), and, if
we are unlucky, four (4) coats. Let us start with what we would like to see for...

```console
python3.11 estimate_paint.py 10 12 49.95
```

\bExample{Desired Output}
```console
For 2 coats...
  You will need to buy 3 gallons of paint.
  You will spend $ 149.85.

For 3 coats...
  You will need to buy 4 to 5 gallons of paint.
  You will spend $ 199.80 to $ 249.75.

For 4 coats...
  You will need to buy 5 to 6 gallons of paint.
  You will spend $ 249.75 to $ 299.70.

```
\eExample

We can actually generate this report with a few changes (that are all within
`estimate_paint.py`). Let us think about coverage...

  1. A 10 foot by 12 foot room has 480 square feet of wall to cover

  2. A gallon of paint covers 350 to 400 square feet

  3. One coat requires 2 gallons of paint (since paint must be bought in whole gallons)

  4. Two (2) coats requires 480 square feet to be covered twice... which is
     equivalent to 960 square feet

  5. Three (3) coats requires 480 square feet to be covered thrice... which is
     equivalent to 1,440 square feet

  6. Four (4) coats requires 480 square feet to be covered four times... which is
     equivalent to 1,920 square feet

We can just call the `compute_paint.gallons_required` function for each of
these values and then pass the result to `estimate_paint.get_report`!


## Updating "main"

Let us start by introducing two global constants:

```python
MIN_COATS: int = 2  # Minimum number of paint coats
MAX_COATS: int = 4  # Maximum number of paint coats
```

We can then add a `for` loop to `main`...

```python
    length, width, price_per_gallon = gather_input(sys.argv)
    area = compute_paint.wall_surface_area(length, width)

    for num_coats in range(MIN_COATS, MAX_COATS + 1):
        total_area_painted = area * num_coats

        print(f"For {num_coats} coats...")

        min_required, max_required = compute_paint.gallons_required(total_area_painted)
        summary = get_report(min_required, max_required, price_per_gallon, indent=2)
        print(summary)
        print()
```

Take note of how we

  1. only call `wall_surface_area` one time

  2. compute `total_area_painted` by taking the number of coats (`num_coats`)
     and multiplying the `area` for a single coat

  3. Output a quick header with 

    ```python
            print(f"For {num_coats} coats...")
    ```

  4. Pass an `indent` named argument to `get_report`


## Updating "get_report"

We would like to indent each line of the report. The `indent argument will
default to zero (0). Afer a quick update to the function signature and
documentation...

```python
def get_report(min_gallons: int, max_gallons: int, price_per_gallon: float, indent: int = 0) -> str:
    """
    Generate a summary of the amount of paint required to paint a room and the
    project cost of that paint.

    Args:
        min_gallons: estimate of the minimum amount of paint required
        max_gallons: estimate of the maximum amount of paint required

        price_per_gallon: cost for a single gallon of paint (e.g.,  for a
            single gallon or as part of a five gallon bucket)

        indent: number of spaces by which to indent each line of the report

    Returns:
        Summary of the estimated gallons of paint required if the min and max
        estimates are the same. Otherwise a report listing the min and max
        values is provided.
    """
```

We can move on to building the actual indent string...

```python
    indent = " " * indent
```

and adding it to each f-string...

```python
    if min_gallons == max_gallons:
        gallons = max_gallons
        cost = gallons * price_per_gallon

        return "\n".join(
            (
                f"{indent}You will need to buy {gallons} gallons of paint.",
                f"{indent}You will spend $ {cost:.2f}.",
            )
        )

    min_cost = min_gallons * price_per_gallon
    max_cost = max_gallons * price_per_gallon

    return "\n".join(
        (
            f"{indent}You will need to buy {min_gallons} to {max_gallons} gallons of paint.",
            f"{indent}You will spend $ {min_cost:.2f} to $ {max_cost:.2f}.",
        )
    )
```

# That is "The End"

The only thing left to do is to run `isort` and `black` one last time. The
final code can be found
<a href="@gitRepoURL@/tree/main/Module-08/Painting-5-Adding" target="_blank">Module-08/Painting-5-Adding</a>.
