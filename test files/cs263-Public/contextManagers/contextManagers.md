Title: Context Managers
TOC: yes
Author: Thomas J. Kennedy


# Motivation

Python provides the `with` statement (construct). This allows the setup and
teardown involved in using resources (e.g., files, sockets, and database
connections) to be handled elsewhere.

This has two main benefits:

  1. There is less boilerplate code.
  2. It is impossible to forget to close/deallocate a resource.

The `with` construct can be used with many types of resources (e.g., files and
network sockets). For this lecture we will focus purely on file IO.


# Writing to a File

Suppose that we want to output the numbers one (1) through ninety-nine (99) to
a file... along with whether the number is even or odd.

To generate such a file, one might write:

> **Python File IO - Basic**
> 
> ```python
> text_file = open("even_or_odd_file.txt", "w")
> 
> for number in range(1, 100):
>     even_or_odd = "even" if number % 2 == 0 else "odd"
>     text_file.write(f"{number} - {even_or_odd}\n")
> ```

Did you notice the missing `fclose(text_file)`?

> **Python File IO - Add `close`**
>
> ```python
> text_file = open("even_or_odd_file.txt", "w")
> 
> for number in range(1, 100):
>     even_or_odd = "even" if number % 2 == 0 else "odd"
>     text_file.write(f"{number} - {even_or_odd}\n")
>
> close(text_file)
> ```

One small `with` allows the file close operation can be handled automatically.

> **Python File IO - Using `with`**
> 
> ```python
> with open("even_or_odd_file.txt", "w") as text_file:
>     for number in range(1, 100):
>         even_or_odd = "even" if number % 2 == 0 else "odd"
>         text_file.write(f"{number} - {even_or_odd}\n")
> ```

Note the indentation. The file is closed as soon as the indented block under
`with` ends.


# Writing to a Gzipped Text File

This also works for other types of files--including compressed files.

> **Python File IO - Using `with` and `gzip`**
> 
> ```python
> import gzip
> 
> with gzip.open("even_or_odd_file.txt.gz", "wt") as text_file:
>     for number in range(1, 100):
>         text_file.write(f"{number} - {even_or_odd}\n")
> ```


# Reading from a File

As one might expect... the `with` context manager can be used when reading data
from a file. 

> ```python
> import sys
> import pprint as pp
> 
> 
> def main():
>     input_filename = sys.argv[1]
> 
>     with open(input_filename, "r") as input_file:
>         for line in input_file:
>             line = line.strip()
> 
>             # Skip blank lines
>             if not line:
>                 continue
> 
>             tokens = line.split()
> 
>             pp.pprint(tokens, indent=2)
> 
> 
> if __name__ == "__main__":
>     main()
> ```

This code snippet is one that I found myself writing quite a bit for debugging
purposes. The code will:

  1. Open a file
  2. Read each line
  3. Skip blank lines
  4. Split a line into tokens (essentially words)
  5. Use the Python  [Pretty
     Printer](https://docs.python.org/3.11/library/pprint.html) to output a
     readable list of tokens for each line
