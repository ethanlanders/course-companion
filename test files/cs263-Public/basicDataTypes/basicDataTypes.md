Title: Basic Data Types & Variables
TOC: yes
Author: Thomas J. Kennedy


# Overview

Python has most of the basic datatypes that you will find in C++, Java, and
Rust... with one exception.

> The datatypes covered in this discussion focus on those that are commonly
> used (e.g., `int` in C++ or Java). It is not an exhaustive list.

| Description                      | Python  | C++           | Java      | Rust     |
| :--                              | :--     | :--           | :--       | :--:     |
| boolean value                    | `bool`  | `bool`        | `boolean` | `bool`   |
| 32-bit integer                   | `int`   | `int`         | `int`     | `i32`    |
| 64-bit floating point            | `float` | `double`      | `double`  | `f64`    |
| character                        |         | `char`        | `char`    | `char`   |
| null-terminated (C-style) string |         | `char*`       |           | `&str`   |
| string                           | `str`   | `std::string` | `String`  | `String` |

The Python `float` is technically more complicated than *just a 64-bit floating
point value*. However, a simplified perspective will work for now.

You probably noticed that Python does not have a character type (`char`).
In most code... a Python string (`str`) is used instead (albeit with only a
single letter at index zero).

The Python string (`str`) is analogous to a C++ `std::string` and Java `String`
(and Rust `String`). It is a full-fledged class with functions such as `len`,
`startswith`, and `replace`.


# Example Values

Let us take the first two columns from the comparison table...

| Description                      | Python  |
| :--                              | :--     |
| boolean value                    | `bool`  |
| 32-bit integer                   | `int`   |
| 64-bit floating point            | `float` |
| character                        |         |
| null-terminated (C-style) string |         |
| string                           | `str`   |

I think the description column (along with the rows where Python has no
equivalent type) can be removed and replaced with example values.

| Python  | Example Values     |
| :--     | :--:               |
| `bool`  | `True` or `False`  |
| `int`   | `7`, `0`, or `-40` |
| `float` | `3.14`             |
| `str`   | `"Sample String"`  |

Note that boolean values in Python are capitalized (i.e., `True` or `False`)
unlike C++, Java, and Rust (i.e., `true` and `false`). *This is one of **the**
common mistakes when learning Python)*


## bool

The `bool` type is normally found within a conditional block. However, the
ternary operator does exist in Python...

```python
is_blue = True if selected_color.title() == "Blue" else False
```

But... the expression itself is already a *boolean expressiion.*

```python
is_blue = selected_color.title() == "Blue"
```

## int

The integer type behaves in Python as it does in C++ and Java... complete with
integer division.


| Operation      | Expression | Result |
| :--            | :--:        | --:    |
| Addition       | `5 + 2`    | `7`    |
| Subtraction    | `7 - 12`   | `-5`   |
| Multiplication | `8 * 3`    | `24`   |
| Division       | `7 / 2`    | `3.5`  |
| Division       | `7 // 2`   | `3`    |
| Modulus        | `7 % 2`    | `1`    |
| Exponentiation | `8 ** 2`   | `64`   |

Take note of the two divisions. Python 3 (specifically [PEP
238](https://peps.python.org/pep-0238/))  introduced a dedicated `//` operator
for integer division.

Unlike most languages where a `pow` or `fpow` function is needed for
exponentiation... Python included the `**` operator.


## float

Python's <a href="https://docs.python.org/3/tutorial/floatingpoint.html" target="_blank">float type</a>
suffers from the same floating point precision issue as analogous types in
other languages. *(If you are truly curious... [CS 417, Computational Methods,
discusses why all floating point numbers suffer from precision
issues](https://www.cs.odu.edu/~tkennedy/cs417/f23/Public/precisionIntro).)*

`float` provides the same operators as `int`... with the exception of `//`.


## str

The `str` type will be covered [in a lecture during the next
module](doc:strings1). *If you are curious... feel free to look ahead.

