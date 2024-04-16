Title: Python Style & PEP 8
TOC: yes
Author: Thomas J. Kennedy


# Overview & Quotes

This document is based on [PEP 8 – Style Guide for Python
Code](https://peps.python.org/pep-0008/). There will be quite a few quoted
passages (albeit with commentary). Any text block shown in

> This is a short quote.

or

\bExample{Example Quote}

This is a quoted passage.

\eExample

is a passage extracted from [PEP 8 – Style Guide for Python
Code](https://peps.python.org/pep-0008/).


# Passage of Interest - PEP 8 Introduction

Let us start with the [last paragraph of the PEP 8
Introduction](https://peps.python.org/pep-0008/#introduction).

> Many projects have their own coding style guidelines. In the event of any
> conflicts, such project-specific guides take precedence for that project.

You will find the Python code for this course (along with code in other
courses) follow the standard PEP 8 style quite closely. You will find
exceptions with mathematical notations, e.g., when naming matrices and vectors
for Least Squares Approximation.

| Math Notation | Python Variable |
| :--           | :--             |
| $X$           | `math_X`        |
| $X^T$         | `math_XT`       |
| $Y$           | `math_Y`        |
| $X^{T}X$      | `math_XTX`      |
| $X^{T}Y$      | `math_XTY`      |

I have adopted the convention of... *if the notation comes from a discipline
then prepend the discipline to the variable name.* For example, the Newton's
Gravitational Constant "$G$" would become `physics_G`.


# Indentation & Spacing

The standard Python convention is four (4) spaces for each level of indentation
(using spaces, not tabs).

You will find that eighty (80) characters is the maximum line length in most
Python code that I write. Take a minute to read through the quoted passage from
[PEP 8 - Maximum Line
Length](https://peps.python.org/pep-0008/#maximum-line-length).

\bExample{PEP 8 - Maximum Line Length (Excerpt)}

Limit all lines to a maximum of 79 characters.

For flowing long blocks of text with fewer structural restrictions (docstrings
or comments), the line length should be limited to 72 characters.

Limiting the required editor window width makes it possible to have several
files open side by side, and works well when using code review tools that
present the two versions in adjacent columns.

The default wrapping in most tools disrupts the visual structure of the code,
making it more difficult to understand. The limits are chosen to avoid wrapping
in editors with the window width set to 80, even if the tool places a marker
glyph in the final column when wrapping lines. Some web based tools may not
offer dynamic line wrapping at all.

...

The preferred way of wrapping long lines is by using Python’s implied line
continuation inside parentheses, brackets and braces. Long lines can be broken
over multiple lines by wrapping expressions in parentheses. These should be
used in preference to using a backslash for line continuation.

\eExample


# Blank Lines

The standard convention is to...

  - add two blank lines after every function

  - add only one line after each method (i.e., function within a class)

Python does recommend that blank lines be used to separate logical sections
within a function, e.g.,

```python
def main():
    """
    Compute the area of a room and the cost of
    flooring for the room
    """

    # Construct the house within the build function
    house = build_house()

    print(house)

    # Upgrade the flooring in a second duplicate house
    duplicate_house = upgrade_flooring(house)

    print(f"house == duplicate_house -> {house == duplicate_house}")
    print(f"&house == &duplicate_house -> {house is duplicate_house}")
    print()

    print(house)
    print(duplicate_house)

    # Get all the flooring costs with a 10% discount
    costs = [discount_flooring(room) for room in duplicate_house]

    for room_cost in costs:
        print(f"{room_cost:.2f}")

    total = sum(costs)
    min_c = min(costs)
    max_c = max(costs)

    print(f"Total: {total:.2f}")
    print(f"Min  : {min_c:.2f}")
    print(f"Max  : {max_c:.2f}")
```


# Spaces in Expressions

There are quite a few best practices for spaces within a line, e.g., after a
comma. 

The <a href="https://peps.python.org/pep-0008/#pet-peeves" target="_blank">Pet Peeves section of PEP 8</a>
summarizes a few rules (most of which you will find are considered best
practices in C++, Java, and Rust).

\bExample{Selected Pet Peeves}

Avoid extraneous whitespace in the following situations:

  - Immediately inside parentheses, brackets or braces

  - Between a trailing comma and a following close [sic]  parenthesis

  - Immediately before a comma, semicolon, or colon:

  - Immediately before the open parenthesis that starts the argument list of a
    function call

  - More than one space around an assignment (or other) operator to align it
    with another:

\eExample

The full list is quite a bit longer (and includes examples). However, like many
of these conventions... the omitted guidelines will be demonstrated in the
lecture examples.


# Variables, Functions, and Classes

All code within the lecture examples, example code, and assignment code will be
follow these conventions:

  - Variables will be named in snake case, e.g., 

    ```python
    some_var = 42
    ```

  - Constants will be the only global variables.

  - Constants will be named in *all caps* with words separated by underscores,
    e.g.,

    ```python
    SPEED_OF_LIGHT: int = 299_792_458
    ```

  - functions and methods will be named in snake case, e.g., 

    ```python
    def compute_polynomial(x_values: list[float], y_values: list[float]) -> np.polynomial Polynomial:
        pass
    ```

  - Classes will be named using Pascal Case, e.g.,

    ```python
    @dataclass
    class Cookbook:
        title: str
        author: Author
        recipes: list[Recipe] = field(default_factory=list)
    ```

# Are We Going to Discuss the Whole Thing?

No... we are not going to go through the entire PEP 8 document. Our discussion
has covered enough to get started. The remaining best practices and conventions
will be covered throughout the remainder of the course.
