Title: Basics of Functions
TOC: yes
Author: Thomas J. Kennedy


# Overview

Functions serve a few purposes, e.g.,

  1. code reuse

  2. readability

  3. maintainability

  4. separation of problems

\bSidebar

You will find that I have some opinions regarding paint brands. My first job
was working for a painting contractor. *I have forgone naming a specifc paint
brand here.*

\eSidebar

You have heard most of this rationale before. Let us come up with a problem.
How about... painting a house. Suppose that you want to write a program that...

  1. Takes length and width of a room

    - *We use four rectangular walls as an estimate and ignore doorways and
      soffets.*

  2. Computes the surface area of the walls

  3. Determines how many gallons of paint are needed

  4. Determines the cost, taking into account that only whole gallons can be
     purchased.

    - *Technically quarts can be purchased for some paints, but the color formula
    often differs.*

    - *We will also ignore the possibilty of five (5) gallon buckets.*

We will assume that

  1. one gallon will cover 350 to 400 square feet (sq. ft.)

  2. trim (e.g., baseboard, doorjambs, and windowsills are covered by on-hand
     trim paint)

  3. doors will not be painted


# Getting Started

Our draft main function would likely start off as...

```python
def main():
    # Dimensions in feet
    length = 12
    width = 10

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

Our stub computation functions would start off by returning a variant of
`-1`...

```python
def compute_wall_surface_area(length, width):
    return -1


def determine_gallons_required(wall_area):
    return -1, -1
```

We know that one does no buy negative gallons of paint. Take note of the second
function. It will return a two-tuple where the first entry is the minimum
number of gallons and the second entry is the maximum number of gallons


# Ambiguity

Let us add type hints to the functions. While type hints are not required (nor
do they provide a performance benefit)... they do provide documentation. We
will know (at a glance) what type of data each function expects for each
argument and what type of data each function returns.

```python
def compute_wall_surface_area(length: float, width: float) -> float:
    return -1


def determine_gallons_required(wall_area: float) -> tuple[float, float]:
    return -1, -1
```

Let us also modify the second function to accept the `min_coverage` and
`max_coverage` as arguments.

```python
def determine_gallons_required(
    wall_area: float, min_coverage: float = 350, max_coverage: float = 400
) -> tuple[float, float]:

    return -1, -1
```

Take note of the default argument values. If you come from C++... this mechanic
is familiar. In Java... you would end up writing three functions...

  1. one function that sets defaults for `min_coverage` and `max_coverage`
  2. one function that sets defaults for `max_coverage`
  3. one function that requires all three (3) arguments


# Implementation

We can implement the first function fairly quickly...

```python
def compute_wall_surface_area(length: float, width: float) -> float:
    
    area_one_wall = length * width
    area_four_walls = 4 * area_one_wall

    return area_four_walls
```

The logic is *compute the area of one wall and multiply by 4*.

> We should really be documenting these functions with pydoc documentation.
> However, that is a topic for a future lecture.

The second function can be implemented fairly quickly too...

```python
def determine_gallons_required(
    wall_area: float, min_coverage: float = 350, max_coverage: float = 400
) -> tuple[float, float]:

    max_gallons = math.ceil(wall_area / min_coverage)
    min_gallons = math.ceil(wall_area / max_coverage)

    return min_gallons, max_gallons
```

Note the use of the `math.ceil` function to *round* to the next integer. And...
we have a mistake. We should be returning a `tuple` of `int`s...

```python
def determine_gallons_required(
    wall_area: float, min_coverage: float = 350, max_coverage: float = 400
) -> tuple[int, int]:
```

That is much better.


# But...

If we run the program *as is*...

```console
You will need to buy 2 to 2 gallons of paint.
You will spend $ 99.90 to $ 99.90
```

we see that for a small room the min and max gallons of paint are the same. A
*10 by 12* room is fairly small (about the size of my home office). Let us try
something more along the lines of a great room... *50 by 40*.

```console
You will need to buy 20 to 23 gallons of paint.
You will spend $ 999.00 to $ 1148.85
```

It would be nice to test this program more thoroughly... and clean up `main`.
However, we will go through that process in a future module. For now... we have
reached good stopping point.

The final code can be found in
<a href="@gitRepoURL@/tree/main/Module-03/Painting-1" target="_blank">Module-03/Painting-1</a>.
