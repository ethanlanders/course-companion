Title: Exceptions & File Parsing
TOC: yes
Author: Thomas J. Kennedy

%define <\bracketHack> {} {}

# A Less Than Cliché Problem

Suppose that we have an input file that contains information about
two-dimensional shapes.

\bExample{inputShapes.txt}

```
Triangle; 4 4 4
Right Triangle; 4 5
Right Triangle; 4 five
Equilateral Triangle; 3
Equilateral Triangle 3
Equilateral Triangle; 3 3 3

Square; 9
Circle; 5
1337 Haxor; 1 lol i broke it
Ellipse;
```

\eExample

Let us write a <a href="@gitRepoURL@/tree/main/Module-07/exception_ex_4.py" target="_blank">quick program to parse the file</a>.

```python
from typing import TextIO
import sys


def parse_shape_file(input_file: TextIO) -> list[tuple[str, list[float]]\bracketHack{}]:

    for line in input_file:
        # Remove leading and trailing whitespace
        line = line.strip()

        if not line:
            continue

        print(line)

    return []


def main():

    with open(sys.argv[1], "r") as shape_file:
        shape_data = parse_shape_file(shape_file)


if __name__ == "__main__":
    main()
```

Take note of how the main function retrieves the input filename from
`sys.argv[1]`. I am not happy with the current `main` function...

```python
def main():

    with open(sys.argv[1], "r") as shape_file:
        shape_data = parse_shape_file(shape_file)
```

If the user...

  1. Supplies an invalid filename (e.g., to a file that does not exist), we
     will encounter a `FileNotFound` exception.

  2. Does not supply a filename, we encounter an `IndexError` exception.
     will encounter a `FileNotFound` exception.

Neither of these exceptions is handled. Let us start with the `IndexError`.

```python
    try:
        shape_filename = sys.argv[1]

    except IndexError as _err:
        print("Usage: exception_ex_5.py INPUT_FILENAME")
        sys.exit(1)

    with open(shape_filename, "r") as shape_file:
        shape_data = parse_shape_file(shape_file)
```

That is much better. We first attempt to retrieve the filename within a
try-except block. If no filename was provided... we output a *usage message*
and exit. However, we still have the invalid file issue, e.g., 

> ```console
> python3.11 exception_ex_5.py doesNotExist.txt
>
> Traceback (most recent call last):
>   File "exception_ex_5.py", line 33, in <module>
>     main()
>   File "exception_ex_5.py", line 28, in main
>     with open(shape_filename, "r") as shape_file:
> 
> FileNotFoundError: [Errno 2] No such file or directory: 'doesNotExist.txt'
> ```

A quick second try-except block can handle the issue...

```python

def main():

    try:
        shape_filename = sys.argv[1]

    except IndexError as _err:
        print("Usage: exception_ex_5.py INPUT_FILENAME")
        sys.exit(1)

    try:
        with open(shape_filename, "r") as shape_file:
            shape_data = parse_shape_file(shape_file)

    except FileNotFoundError as err:
        print(err)
        sys.exit(2)
```

Note how `err` is printed. At the end of the day... the final line of the
stacktrace is what we want. We can just output the `FileNotFoundError`'s
message.

> ```console
> python3.11 exception_ex_6.py doesNotExist.txt
> [Errno 2] No such file or directory: 'doesNotExist.txt'
> ```

The files
<a href="@gitRepoURL@/tree/main/Module-07/exception_ex_5.py" target="_blank">exception_ex_5.py</a> and
<a href="@gitRepoURL@/tree/main/Module-07/exception_ex_6.py" target="_blank">exception_ex_6.py</a> contain
the updated code with the addition of the first and second try-except blocks,
respectively.


# What About Parsing the File

Do not worry... we will start parsing the input file shortly. Keep in mind that
these first two exceptions (i.e., `IndexError` and `FileNotFoundError`) are two
of the most common exceptions when dealing with files and command line
arguments. However, too many programmers rush to *the fun part* and say *"I
will write that error handling later."* The error handling is oft never
written.

*Yes... I have worked quite hard to rid myself of this very habit.* Learn from
my mistakes.

Let us take a moment to review the entire file (after all the updates).

```python
from typing import TextIO
import sys


def parse_shape_file(input_file: TextIO) -> list[tuple[str, list[float]]\bracketHack{}]:

    for line in input_file:
        # Remove leading and trailing whitespace
        line = line.strip()

        if not line:
            continue

        print(line)

    return []


def main():

    try:
        shape_filename = sys.argv[1]

    except IndexError as _err:
        print("Usage: exception_ex_5.py INPUT_FILENAME")
        sys.exit(1)

    try:
        with open(shape_filename, "r") as shape_file:
            shape_data = parse_shape_file(shape_file)

    except FileNotFoundError as err:
        print(err)
        sys.exit(2)


if __name__ == "__main__":
    main()
```

I think that `main` is good enough for us to focus in `parse_shape_file`.


# The Actual Parsing

Let us start by changing the return type. A `list` of `tuple`s is probably not
the best choice. Once the shape names and correspoing numbers are retrieved
their will probably be follow-up validation (e.g., checking that the numbers
are non-negative). Let us switch from a function that returns a `list`...

```python
def parse_shape_file(input_file: TextIO) -> list[tuple[str, list[float]]\bracketHack{}]:
```

to a function that `yield`s values as `Generator`.

```python
def parse_shape_file(input_file: TextIO) -> Generator[tuple[str, list[float]], None, None]:
```

And... let us add some pydoc documentation...

```python
def parse_shape_file(input_file: TextIO) -> Generator[tuple[str, list[float]], None, None]:
    """
    Take each line from a given file (or file-like object) and split it into a
    tuple in the form

      (name, [val_1, val_2, ...])

    If a line is invalid (e.g., contains non-numeric values after the
    semicolon)... skip the line.
    """
```

*Note that this does require a change in main*...

```python
        with open(shape_filename, "r") as shape_file:
            shape_data = parse_shape_file(shape_file)
```

must be rewritten as...

```python
        with open(shape_filename, "r") as shape_file:
            shape_data = list(parse_shape_file(shape_file))
```


## The Initial Loop

Let us start with a basic loop. We want to:

  1. Grab a line
  2. Strip (remove) leading and trailing whitespace from the line
  3. If the line is blank (i.e., empty)... skip it and continue to the next
     line

```python
    for line in input_file:
        # Remove leading and trailing whitespace
        line = line.strip()

        if not line:
            continue
```

We need to split each line at the semicolon (i.e., '`;`'). If the line does not
contain a semicolon... it is malformed. Let us throw a `ValueError`.

```python
        try:
            name, the_rest = line.split(";")
        except ValueError as _err:
            print(f"Missing ';' -> \"{line}\" is malformed.", file=sys.stderr) 
            continue
```

Take note of how the output is written to `sys.stderr`. In practice this is a
recoverable error. If we were using a logger (as production code should) this
message would be output at the *Warning* level. It is an error... but an error
from which we can recover (by skipping the line). *We want to separate error
output from actual output*.

Now...we want to parse the rest of the line (i.e., `the_rest`). Let us...


   1. Remove any leading whitespace.

    ```python
            the_rest = the_rest.lstrip()
    ```

  2. Split on whitespace to get a list.

    ```python 
            the_rest = the_rest.split()
    ```

  3. Try to convert every list entry into a float.

    ```python
            numbers = [float(val) for val in the_rest]
    ```

  4. Handle the case where a `val` is not a number.

    ```python
            try:
                numbers = [float(val) for val in the_rest]
            except ValueError as err:
                print(f"{err} -> \"{line}\" is malformed.", file=sys.stderr)
                continue
    ```

  5. ~~Return~~ `yield` `name` and `numbers` as a tuple. 

    ```python
            yield (name, numbers)
    ```

# Revising the Loop?

Let us take a look at the complete `parse_shape_file` function.

```python
def parse_shape_file(input_file: TextIO) -> Generator[tuple[str, list[float]], None, None]:
    """
    Take each line from a given file (or file-like object) and split it into a
    tuple in the form

      (name, [val_1, val_2, ...])

    If a line is invalid (e.g., contains non-numeric values after the
    semicolon)... skip the line.
    """

    for line in input_file:
        # Remove leading and trailing whitespace
        line = line.strip()

        if not line:
            continue

        try:
            name, the_rest = line.split(";")
        except ValueError as _err:
            print(f"Missing ';' -> \"{line}\" is malformed.", file=sys.stderr)
            continue

        the_rest = the_rest.lstrip()
        the_rest = the_rest.split()

        try:
            numbers = [float(val) for val in the_rest]
        except ValueError as err:
            print(f"{err} -> \"{line}\" is malformed.", file=sys.stderr)
            continue

        yield (name, numbers)
```

One might be tempted to combinethe two `try-except` blocks. Even though the two
exceptions are both `ValueError`s... they occur for different reasons. Our goal
is to maintain context that can be logged (even though logging is a topic for a
future module).

**Let us leave the loop "as is" for now.


# Returning to "main"

Let us tweak `main` a little more. While `parse_shape_file` is intended for use
in a larger program... we can still take a quick look at the output. Let us add
a single `print` statement at the end of `main`

```python
    try:
        with open(shape_filename, "r") as shape_file:
            shape_data = list(parse_shape_file(shape_file))

    except FileNotFoundError as err:
        print(err)
        sys.exit(2)

    print(shape_data)
```

Take note of where the `print` statement is located. It is outside the

  1. `try-except` block because we only have data if `shape_file` was opened
    successfully

  2. `with` context manager because we are done with the input file.

This organization clearly documents that we only output `shape_data` after we
have **finsihed** reading the input file.

Unfortunately, the output leaves much to be desired. The `list` version of
`repr` does output the list of `tuple`s in a form that captures the content.

\bExample{Output with repr}

```console
could not convert string to float: 'five' -> "Right Triangle; 4 five" is malformed.
Missing ';' -> "Equilateral Triangle 3" is malformed.
could not convert string to float: 'lol' -> "1337 Haxor; 1 lol i broke it" is malformed.
[('Triangle', [4.0, 4.0, 4.0]), ('Right Triangle', [4.0, 5.0]), ('Equilateral Triangle', [3.0]),
('Equilateral Triangle', [3.0, 3.0, 3.0]), ('Square', [9.0]), ('Circle', [5.0]), ('Ellipse', [])]
```

\eExample

*The last two lines are actual output as a single line. I added a line break
for readability.* Let us switch to a `PrettyPrinter` from the [pprint
module](https://docs.python.org/3/library/pprint.html). Let us start with the
import statement.

```python
import pprint as pp
```

The convention is refer to the `pprint` module with the `pp` abreviation. We
can then replace

```python
    print(shape_data)
```

with

```python
    pp.pprint(shape_data, indent=2, width=72)
```

Take note of the two keyword arguments:

  - `indent` is the number of spaces to indent each level of the `list`

  - `width` is the maximum width of a line before output moves to the next line


The `pprint` output is much more readily parsed (by a human).


\bExample{Output with pprint}

```console
could not convert string to float: 'five' -> "Right Triangle; 4 five" is malformed.
Missing ';' -> "Equilateral Triangle 3" is malformed.
could not convert string to float: 'lol' -> "1337 Haxor; 1 lol i broke it" is malformed.
[ ('Triangle', [4.0, 4.0, 4.0]),
  ('Right Triangle', [4.0, 5.0]),
  ('Equilateral Triangle', [3.0]),
  ('Equilateral Triangle', [3.0, 3.0, 3.0]),
  ('Square', [9.0]),
  ('Circle', [5.0]),
  ('Ellipse', [])]
```

\eExample

I think that is a good stopping point. The [final example (exception_ex_7) can
be accessed in the course example
repository.](@gitRepoURL@/tree/main/Module-07/exception_ex_7.py)
