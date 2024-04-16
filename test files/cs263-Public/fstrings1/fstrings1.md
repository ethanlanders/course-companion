Title: Basic F-Strings
TOC: yes
Author: Thomas J. Kennedy


# Whirlwind Introduction

You will find (or have found) that I tend to make use of *whirlwind
introductions*. The f-string (or formatted string literal) lends itself well to
such an introduction (i.e., looking at an example and working top down).


## Case Study

Let us take a look a familiar code snippet (i.e., one from the lecture on user
input).

```python
def main():

    price = float(input("What is the price of your favorite lunch? "))
    frequency = int(input("How many times a week do you have that lunch? "))

    print(f"On average you spend {price * frequency:.2f}")


if __name__ == "__main__":
    main()
```



## A Single Line

We only interested in a single line.

```python
    print(f"On average you spend {price * frequency:.2f}")
```

Let us break this line down.

  1. `f"` - the 'f' before the opening quote indicates that this is an f-string

  2. `"On average you spend ` - this is treated as a normal string literal

  3. `{price * frequency:.2f}` - this is where the f-string *magic* happens

    1. `price * frequency` - the values stored in the `price` and `frequency`
       varaibles are retrieved and a multiplication is performed

    2. the colon separates the expression from the formatting specification

    3. the `.2` indicates that we want two decimal places to be output

    4. the `f` indicates that we have a floating point value


# A Few Quick Examples

Let us examine a few quick examples.


## An Integer

Suppose that we wanted to output an integer (`val`) and right justify it within
three spaces.

```python
    val = 7
    print(f"{val:>3}")
```

The `>` indicates right alignment.


## A Floating Point Number

Suppose that we wanted to output `price_per_gallon` and have it rounded to two
decimal places.

```python
    price_per_gallon = 7.552
    print(f"{price_per_gallon:>4.2f}")
```

The `.2f` handles the rounding and the `>4` handles the right alignment.


## A String

Suppose that we want to output `color` as a centered title.

```python
    color = "blue"
    print(f"{color.title():^80}")
```

The `^` (caret) indicates center alignment. 


# What About the "format" Function?

The `.format` function predates f-strings and, while it does have a few use
cases, is should be avoided when an f-string can be used. Let us rewrite our
previous three (3) examples to use `.format`.


```python
    val = 7
    print("{>3}".format(val))
```

```python
    price_per_gallon = 7.552
    print("{4.2f}".format(price_per_gallon))
```

```python
    color = "blue"
    print("{^80}".format(color.title()))
```

The formatting syntax (more aptly grammar) are the same (which makes sense
considering f-string syntax was based on that of `.format`).


# What About C "printf" Style output?

The `printf` style output predates both f-strings and `.format`. With the
exception of logging output... this method of output formatting should be
avoided in modern Python code. The official Python docs even refer to this
method as ["old string
formatting"](https://docs.python.org/3/tutorial/inputoutput.html#old-string-formatting).

Let us rewrite our running examples one last time.

```python
    val = 7
    print("% 3d" % val)
```

```python
    price_per_gallon = 7.552
    print("% 4.2f" % price_per_gallon)
```

The string example is impossible to write with `printf` style formatting. We
have to fall back on invoking (calling) `str` functions.

```python
    color = "blue"
    print(color.title().center(80))
```
