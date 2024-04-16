Title: Refactoring & Code Style
TOC: yes
Author: Thomas J. Kennedy


# Overview 

In the [previous lecture](doc:refactoring1TDD) we added tests to the paint
example. We will start with that code...
<a href="@gitRepoURL@/tree/main/Module-08/Painting-3-Tests" target="_blank">Module-08/Painting-3-Tests</a>.


# Automated Tools

Before we start refactoring let us...

  1. Run our code through `isort` to make sure that imports are listed in *the
     accepted order*

  2. Run our code through `black` to address formatting issues (e.g., line
     breaks, spaces, commas, line width)

  3. Run our code through `pylint` to get a report of issues we need to examine
     manually.


## isort

Since both of our *actual program logic* files contain a single import...
nothing needs to be changed.

\bExample{Imports - estimate_paint.py}

```python
import compute_paint
```

\eExample

\bExample{Imports - estimate_paint.py}

```python
import math
```

\eExample

However, our test code has a few issues...

\bExample{Imports - test_estimate_paint.py}

\bSplitColumns

**Original**

```python
import pytest

from hamcrest import *

from estimate_paint import get_report
```

\splitColumn

**After `isort`**

```python
import pytest
from hamcrest import *

from estimate_paint import get_report
```

\eSplitColumns

\eExample

\bExample{Imports - test_compute_paint.py}

**Original**

```python
import pytest

from hamcrest import *

from compute_paint import (wall_surface_area, gallons_required)
```

**After `isort`**

```python
import pytest
from hamcrest import *

from compute_paint import gallons_required, wall_surface_area
```

\eExample

In general... imports shold be organized by:

  1. imports for built-in modules (i.e, parts of the Python stnadard library) 

  2. imports for external libraries

  3. imports for other modules that are part of the project


## pylint

Wild card imports (e.g., `from hamcrest import *`) will be flagged by pylint.
us update our test imports once more...

\bExample{Imports - test_estimate_paint.py}

```python
import pytest
from hamcrest import assert_that, contains_string, string_contains_in_order
```

\eExample

\bExample{Imports - test_compute_paint.py}

```python

import pytest
from hamcrest import assert_that, close_to, equal_to

from compute_paint import gallons_required, wall_surface_area
```

\eExample

That is much better. The formal rule for wildcard imports is...

> *Do not pollute your modules namespace and import everything.*

However, the more pragmatic view is...

> *If you import everything... you will not remember what you are actually using
> from that module... nor will anyone else.*

Now let us run `pylint` on our codebase...

```console
python3.11 -m pylint compute_paint.py estimate_paint.py tests
```

Our report is not too bad...

```python
************* Module compute_paint
compute_paint.py:1:0: C0114: Missing module docstring (missing-module-docstring)
compute_paint.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
compute_paint.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module estimate_paint
estimate_paint.py:1:0: C0114: Missing module docstring (missing-module-docstring)
estimate_paint.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
estimate_paint.py:5:4: R1705: Unnecessary "else" after "return",
                              remove the "else" and de-indent the code inside it (no-else-return)
estimate_paint.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module test_estimate_paint
tests/test_estimate_paint.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests/test_estimate_paint.py:7:0: C0116: Missing function or method docstring (missing-function-docstring)
tests/test_estimate_paint.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
tests/test_estimate_paint.py:1:0: W0611: Unused import pytest (unused-import)
************* Module test_compute_paint
tests/test_compute_paint.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests/test_compute_paint.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
tests/test_compute_paint.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 7.31/10 (previous run: 7.31/10, +0.00)
```

> **Most examples of tools like `pylint` are disingenuous.** The author will say
> *look at how bad this code is and what `pylint` finds.* The focus should be on...
> 
>   1. here are the Python style rules
> 
>   2. let us follow those rules
> 
>   3. hey... `pylint` found a few things that we missed

Most of our issues come down to documentation...

  1. Our modules do not have docstrings

  2. Our functions were never fully documented

Let us start with the documentation for `compute_paint`.

\bExample{Documentation - compute_paint.py}

```python
"""
This module provides functions to compute how much paint is needed to paint a
room, including paint coverage and wall surface area.
"""

import math


def wall_surface_area(length: float, width: float) -> float:
    """
    Compute the surface area of all four walls in a room. For the purposes of
    this estimation... it is assumed that

      1. each wall is a rectangle with no doorways or windows
      2. there are four (4) walls in the room

    Args:
        length: room length
        width: room width

    Returns:
        Wall surface area for a single room
    """

    area_one_wall = length * width
    area_four_walls = 4 * area_one_wall

    return area_four_walls


def gallons_required(
    wall_area: float, min_coverage: float = 350, max_coverage: float = 400
) -> tuple[int, int]:
    """
    Compute the number of gallons of paint required for a given surface area.

    Args:
        wall_area: surface area to be covered
        min_coverage: minimum area covered by a gallon of paint
        max_coverage: maximum area covered by a gallon of paint

    Returns:
        minimum and maximum gallons of paint required rounded up to the next
        whole gallon.
    """

    max_gallons = math.ceil(wall_area / min_coverage)
    min_gallons = math.ceil(wall_area / max_coverage)

    return min_gallons, max_gallons
```

\eExample

That is much better. *(The documentation should have been there from the
beginning, but I left it off in preparation for this very discussion.)*

The documentation for `estimate_paint` can be written fairly quickly.

\bExample{Documentation - estimate_paint.py}

```python
"""
This program generates a summary that contains the amount of paint required to
paint a room (in gallons) and the cost of that paint.
"""

import compute_paint


def get_report(min_gallons: int, max_gallons: int, price_per_gallon: float) -> str:
    """
    Generate a summary of the amount of paint required to paint a room and the
    project cost of that paint.

    Args:
        min_gallons: estimate of the minimum amount of paint required
        max_gallons: estimate of the maximum amount of paint required

        price_per_gallon: cost for a single gallon of paint (e.g.,  for a
            single gallon or as part of a five gallon bucket)

    Returns:
        Summary of the estimated gallons of paint required if the min and max
        estimates are the same. Otherwise a report listing the min and max
        values is provided.
    """

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


if __name__ == "__main__":
    main()
```

\eExample

That just leaves us with...

```python
************* Module estimate_paint
estimate_paint.py:5:4: R1705: Unnecessary "else" after "return",
                              remove the "else" and de-indent the code inside it (no-else-return)
```

*Note that we will not be adding documentation to the test code.*

As a general rule code in the form...

```python
if condition
    return ...
else
    return ...
```

should be written as...

```python
if condition
    return ...

return ...
```

This *early return* or *guard* approach decreases the level of scope, but more
importantly makes it more clear that the special cases are handled first. The
*general path* can be identified at a glance. *This approach is common in Java
and Rust.*

Let us rewrite `get_report`.

```python
    if min_gallons == max_gallons:
        gallons = max_gallons
        cost = gallons * price_per_gallon

        return "\n".join(
            (
                f"You will need to buy {gallons} gallons of paint.",
                f"You will spend $ {cost:.2f}.",
            )
        )

    min_cost = min_gallons * price_per_gallon
    max_cost = max_gallons * price_per_gallon

    return "\n".join(
        (
            f"You will need to buy {min_gallons} to {max_gallons} gallons of paint.",
            f"You will spend $ {min_cost:.2f} to $ {max_cost:.2f}.",
        )
    )
```

## black

My go-to code reformatter is `black`. However, in this case neither
`compute_paint.py` nor `estimate_paint.py` would be changed. So... let us look
at our test code...

\bSidebar

`black` always adds a trailing comma after the last entry in a sequence. This
rule comes from tuple syntax (e.g., `(1)` is just the number one and `(1,)` is
a one-tuple that contains the value `1`).

\eSidebar

```diff
     assert_that(
         actual_report,
         string_contains_in_order(
-            "You will need to buy "
-            "4",
+            "You will need to buy " "4",
             " gallons of paint.",
             "\n",
             "You will spend",
-            "$ 140.40."
-        )
+            "$ 140.40.",
+        ),
     )
```

Our first test function in `test_estimate_paint.py` was missing a comma between
two strings.

```python
            "You will need to buy "
            "4",
```

`black` sees that as something that should be a single string. Let us manually
add the missing comma after the first line.

What do you know... I missed a comma in the second test function. Let us add
that one as well.


```diff
 def test_get_report_different_min_max():
     actual_report = get_report(min_gallons=10, max_gallons=14, price_per_gallon=32.50)
 
     assert_that(
         actual_report,
         string_contains_in_order(
-            "You will need to buy "
-            "10 to 14",
+            "You will need to buy " "10 to 14",
             " gallons of paint.",
             "\n",
             "You will spend",
-            "$ 325.00 to $ 455.00."
-        )
+            "$ 325.00 to $ 455.00.",
+        ),
     )
```

The issue in `test_compute_paint.py` is more subtle. We need a second blank
line between our test data and test function.

```diff
     (2, 2, 16),
     (10, 12, 480),
     (10.5, 10, 420),
 ]
 
+
 @pytest.mark.parametrize("length, width, surface_area", test_data)
 def test_wall_surface_area(length, width, surface_area):
     assert_that(wall_surface_area(length, width), close_to(surface_area, 1e-1))
```


## A Quick Breather

This lecture ended up longer than I had planned... but necessarily so.  The
complete examples can be found in
<a href="@gitRepoURL@/tree/main/Module-08/Painting-4-Style" target="_blank">Module-08/Painting-4-Style</a>.

We will continue working on this code in the next lecture.
