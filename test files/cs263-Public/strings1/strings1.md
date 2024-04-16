Title: String Manipulation & Comparison
TOC: yes
Author: Thomas J. Kennedy


# Strings!

The Python string (i.e., `str`) provides [quite a few
methods](https://docs.python.org/3/library/stdtypes.html#string-methods). While
an exhaustive list is a good *cheat sheet* to have... we can always bookmark
the official `str` docs. For this lecture... we will start with:

  - `str.startswith` - returns `True` if a string starts with a specified prefix string.
  - `str.endswith` - returns `True` if a string ends with a specified suffix string.
  - `str.capitialize` - returns a new string with the first letter capitalized.
  - `str.title` - returns a new string with each word capitalized.
  - `str.upper` - returns a new string with each letter in uppercase.
  - `str.lower` - returns a new string with each letter in lowercase.
  - `str.split` - split a string at each occurrence of a given substring.
  - `str.splitlines` - split a string at every line ending.

There are quite a few more methods, but these are the ones that we will use
most often.


# A Quick First Example

I often find myself outputting headings in my example code. In C++ and Java...
I have dedicated `utilities` modules. However, Python does not require one
write a dedicated *header* module.

Suppose that we wanted to output a heading

```python
    text = "Strings Are Fun!"
```

that is:

  1. 72 characters wide
  2. centered
  3. preceded by a border consisting of dashes (i.e., `-`)
  4. followed by a border consisting of dashes (i.e., `-`)

Centering a string can be done with...

```python
    width = 72
    text = "Strings Are Fun!".center(width)
```

Take note of the width variable. Since we will be using the value `72` in
multiple places... we want *"what 72 is"* to unambiguous.

If you come from C++ or Java... your first instinct might be to create a new
string or use some array trickery. However, this is Python...

```python
    border = "-" * width
```

Python allows us to repeat a string by *multiplying* the string by an integer.
*(I prefer Rust's `.repeat` syntax.)*

Well... now we can put everything together.

```python
def header_demo():

    width = 72
    border = "-" * width

    text = "Strings Are Fun!".center(width)

    print(border)
    print(text)
    print(border)


if __name__ == "__main__":
    header_demo()
```

Although... I would refactor this code into a reusable function.

```python
def get_heading(text: str, width: int, divider: str = "-") -> str:
    border = "-" * width

    return "\n".join(
        (
            border,
            "Strings Are Fun!".center(width),
            border
        )
    )


def main():
    heading = get_heading(text="Strings Are Fun!", width=72)
    print(heading)


if __name__ == "__main__":
    main()
```

This is a  perfect to introduce the `.join` method. The method takes a
collection of values (e.g., a `list` or `tuple`) and places the specified
string (e.g., `\n` or `, `) between them.

*You may be wondering if the same result can be achieved with an f-string.*
Yes... it is possible. However, an f-string only works if we have a one-line
title.


# A Second Example

Suppose that we are implementing a crude answer checker for a fill-in-the-blank
question. Consider the following question.

> A class defines the structure of a type of thing (e.g., `Book`) while an ______
> is an actual thing (e.g., a book on a shelf).

We might start of with a function in the form...

```python
def check_fill_in_the_blank(correct_answer: str, supplied_answer: str) -> bool:
    if supplied_answer == correct_answer:
        return True
    else
        return False
```

and then rewrite it as...

```python
def check_fill_in_the_blank(correct_answer: str, supplied_answer: str) -> bool:
    if supplied_answer == correct_answer:
        return True

    return False
```

before finally settling on...

```python
def check_fill_in_the_blank(correct_answer: str, supplied_answer: str) -> bool:
    return supplied_answer == correct_answer
```

A naive string equality check would work. However, we know that misspellings
are common on exams and quizzes. Let us convert both answers to lowercase.

```python
def check_fill_in_the_blank(correct_answer: str, supplied_answer: str) -> bool:
    return supplied_answer.lower() == correct_answer.lower()
```

Let us shorten the variable names and grab the length of the correct answer
with `len`.

```python
def check_fill_in_the_blank(correct_answer: str, supplied_answer: str) -> bool:
    supplied = supplied_answer.lower()
    correct = correct_answer.lower()

    correct_length = len(correct)

    return supplied == correct
```

How about we set the criteria as:

  1. Grab the length of the correct answer.
  2. Compare the first `length // 2` letters of the correct answer and student answer
  3. Compare the last `length // 2` letters of the correct answer and student answer
  4. Award credit if the first or last `length // 2` letter match


```python
def check_fill_in_the_blank(correct_answer: str, supplied_answer: str) -> bool:
    supplied = supplied_answer.lower()
    correct = correct_answer.lower()

    num_required_chars = len(correct) // 2

    if supplied.startswith(correct[:num_required_chars]):
        return True

    if supplied.endswith(correct[-num_required_chars:]):
        return True

    return False
```

The slice syntax will be covered when we get to `list` in a later lecture.
However, for now let us note that...

  - `correct[:num_required_chars]` - starts at zero (0) and grabs every
    character up to (but not including) `num_required_chars`

  - `correct[-num_required_chars:]` - starts at `-num_required_chars` and
    grabs everything up through the end of `correct`


We should also account for the penchant of students to get carried away on such
questions (e.g., write a full sentence when only a word or two was needed).


```python
def check_fill_in_the_blank(correct_answer: str, supplied_answer: str) -> bool:
    supplied = supplied_answer.lower()
    correct = correct_answer.lower()

    num_required_chars = len(correct) // 2

    if supplied.startswith(correct[:num_required_chars]):
        return True

    if supplied.endswith(correct[-num_required_chars:]):
        return True

    if correct in supplied:
        return True

    return False
```

This handles the case where we expected *"object"* as an answer, but the student
wrote something along the lines of *"The correct answer is object."*

Note the use of `in` to check for the occurrence of a substring.


# Is That It?

We have reached a good stopping point for now. We will see more string
manipulation when we discuss working with files.
