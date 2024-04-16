Title: Structure of a Basic Python Program
TOC: yes
Author: Thomas J. Kennedy


# Python Terminology

The term *dunder* refers to any item that is both preceded and
followed by two underscores.

If you are familiar with operator overloading in C++...

```cpp
bool operator==(const Book& lhs, const Book& rhs);
```

...or methods such as `equals`, `toString`, and `hashCode` in Java... the
so-called Python dunder functions can be considered analogous (but not quite
equivalent).

Our first example is the  dunder main (i.e., `__main__`) block.


# If `__main__`

The last chunk is what tells the Python interpreter what to run.

```python
if __name__ == "__main__":
    some_driver_function()
```

This allows us to run our script directly. If we import the Python script into
a larger program... the `__name__ == "__main__"` will evaluate to `False`.
This will allow us to call our functions from a larger program without having
to rewrite any code.

The implications and importance of `if __name__ == "__main__"` cannot be fully
discussed until we have, at the very least, discussed functions, modules, and
imports later in the course.


# A Little Better Than "Hello World"

Most programming introductions include a program that, as its name "Hello
World" suggests prints...

```
Hello World
```

I abhor such examples. Let us do something *slightly* better.

\loadlisting{print_name.py}

This program outputs a hardcoded name (in this case *Tom*). I encourage you to
type up the program and replace "Tom" with your name.

*Note that `print`, f-strings, and variables will be covered in the next
module.*


# Module `docstring`

The multi-line ~~comment~~ string at the top of the file is known as a module
docstring.

```python
"""
This is a short example module that contains a single driver function and
outputs a hardcoded name.
"""
```

It provides a brief overview of the modules as
a whole. While our current program is quite simple... such documentation
becomes quite useful when we start working with functions grouped into modules.

While some resources might call this block a comment... it is actually a
multi-line string literal. Python does not have true multi-line comments.






