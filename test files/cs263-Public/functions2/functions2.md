Title: Functions & Modules
TOC: yes
Author: Thomas J. Kennedy


# Continuing...

In [the previous lecture](doc:functions1) we developed a program to compute how
many gallons of paint would be required to paint a room. We ended up with two
functions. Let us separate the driver (`main`) and computation functions into two files:

  1. `main` will remain in `estimate_paint.py`

  2. the computation functions will be moved to a new file named
     `compute_paint.py`


# Separating the Code

Let us start by moving the computation functions

\bExample{compute_paint.py}

```python
import math


def compute_wall_surface_area(length: float, width: float) -> float:

    area_one_wall = length * width
    area_four_walls = 4 * area_one_wall

    return area_four_walls


def determine_gallons_required(
    wall_area: float, min_coverage: float = 350, max_coverage: float = 400
) -> tuple[int, int]:

    max_gallons = math.ceil(wall_area / min_coverage)
    min_gallons = math.ceil(wall_area / max_coverage)

    return min_gallons, max_gallons
```
\eExample

\bExample{estimate_paint.py}

```python
from compute_paint import *


def main():
    # Dimensions in feet
    length = 50
    width = 40

    # Price in dollars
    price_per_gallon = 49.95

    area = compute_wall_surface_area(length, width)

    gallons_required = determine_gallons_required(area)

    min_required, max_required = gallons_required
    min_cost = min_required * price_per_gallon
    max_cost = max_required * price_per_gallon

    print(f"You will need to buy {min_required} to {max_required} gallons of paint.")
    print(f"You will spend $ {min_cost:.2f} to $ {max_cost:.2f}")


if __name__ == "__main__":
    main()
```

\eExample

Take note of the **wildcard import**.

```python
from compute_paint import *
```

These types of imports should always be avoided. The general rule (regardless
of language) is *import what you need and nothing extra.*

Let us import the two functions that we are actually using...

```python
from compute_paint import (compute_wall_surface_area, determine_gallons_required)
```

# Renaming the Functions

Since the module (i.e., `compute_paint`) contains the two functions... their
names are a little redundant...

  - `compute_paint.compute_wall_surface_area`
  - `compute_paint.determine_gallons_required`

If we import the module and use the fully qualified function names...

  - `compute_paint.wall_surface_area`
  - `compute_paint.gallons_required`

the module name becomes part of the documentation!

Let us tweak main...

\bExample{estimate_paint.py - Updated Imports}

```python
import compute_paint


def main():
    # Dimensions in feet
    length = 50
    width = 40

    # Price in dollars
    price_per_gallon = 49.95

    area = compute_paint.wall_surface_area(length, width)

    gallons_required = compute_paint.gallons_required(area)

    min_required, max_required = gallons_required
    min_cost = min_required * price_per_gallon
    max_cost = max_required * price_per_gallon

    print(f"You will need to buy {min_required} to {max_required} gallons of paint.")
    print(f"You will spend $ {min_cost:.2f} to $ {max_cost:.2f}")


if __name__ == "__main__":
    main()
```

\eExample

We can also use tuple unpacking to rewrite...

```python
    gallons_required = compute_paint.gallons_required(area)

    min_required, max_required = gallons_required
```

as one line...

```python
    min_required, max_required = compute_paint.gallons_required(area)
```

We should also add the missing period in the second `print` statement...

```python
    print(f"You will spend $ {min_cost:.2f} to $ {max_cost:.2f}.")
```


# Fixing the Output

I do not like the output...

  1. There should be a `get_report` function that returns a `str` that we then
     output.

  2. There is no logic for the case where the minimum and maximum required
     gallons of paint are the same

Let us start with where to place the new function... `estimate_paint.py`. The
output logic is program specific. Let us establish the practice of separating
computational logic from output (and input) logic. 

\bExample{get_report}
```python
def get_report(min_gallons: int, max_gallons: int, price_per_gallon: float) -> str:
    min_cost = min_gallons * price_per_gallon
    max_cost = max_gallons * price_per_gallon

    return "\n".join(
        (
            f"You will need to buy {min_gallons} to {max_gallons} gallons of paint.",
            f"You will spend $ {min_cost:.2f} to $ {max_cost:.2f}.",
        )
    )
```
\eExample

Take note of the `"\n".join((...))`. We are taking a tuple of two strings
(`tuple[str]`) and inserting a newline (`"\n"`) between them. The `join`
function comes up quite a bit in Python.

Now... let us add a conditional block to check if `min_gallons == max_gallons`.

\bExample{get_report - Updated}
```python
def get_report(min_gallons: int, max_gallons: int, price_per_gallon: float) -> str:
    if min_gallons == max_gallons:
        gallons = max_gallons
        cost = gallons * price_per_gallon

        return "\n".join(
            (
                f"You will need to buy {gallons} gallons of paint.",
                f"You will spend $ {cost:.2f}.",
            )
        )

    else:
        min_cost = min_gallons * price_per_gallon
        max_cost = max_gallons * price_per_gallon

        return "\n".join(
            (
                f"You will need to buy {min_gallons} to {max_gallons} gallons of paint.",
                f"You will spend $ {min_cost:.2f} to $ {max_cost:.2f}.",
            )
        )

```
\eExample


# Done... for the Moment

For the moment... let us  consider this example complete. We will revisit it in
a few modules for a *code review* discussion.

The final code can be found in
<a href="@gitRepoURL@/tree/main/Module-03/Painting-2" target="_blank">Module-03/Painting-2</a>.
