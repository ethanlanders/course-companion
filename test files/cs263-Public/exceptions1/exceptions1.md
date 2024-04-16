Title: Basic Exceptions
TOC: yes
Author: Thomas J. Kennedy

In most courses you are told to *assume all input is well formed*. You are told
to write minimal (if any) error handling code.


# What is an Exception?

As exception can interupt the execution flow of a program. In the case of a
try-except block...

```python
try:
    raw_string = input("Enter a year: ")
    year = int(raw_string)

except ValueError as _err:
    print(f'"{raw_string}" is not a valid year')
```

we essentially have an if-else analogue. The `try` block is the *good* path and
the `except` block is the *bad* path.


# Why so Specific?

You may have noticed that the try-catch block only handles the `ValueError`
exception. Let us rewrite the code with a bare exception.

```python
try:
    raw_string = input("Enter a year: ")
    year = int(raw_string)

except:
    print(f'"{raw_string}" is not a valid year')
```

Run the code and press `ctrl-c` to force exit. You will see the following...

> ```
> Enter a year. ^CTraceback (most recent call last):
>   File "/home/tkennedy/Courses/Reviews/cs263/Module-07/exception_ex_1.py", line 4, in main
>     raw_string = input("Enter a year. ")
> 
> KeyboardInterrupt
> 
> During handling of the above exception, another exception occurred:
> 
> Traceback (most recent call last):
>   File "/home/tkennedy/Courses/Reviews/cs263/Module-07/exception_ex_1.py", line 12, in <module>
>     main()
>   File "/home/tkennedy/Courses/Reviews/cs263/Module-07/exception_ex_1.py", line 8, in main
>     print(f'"{raw_string}" is not a valid year')
> 
> UnboundLocalError: cannot access local variable 'raw_string' where it is not associated with a value
> ```

We caught the `KeyboardInterrupt`. Our intention was to handled malformed year
input, but we wrote code that handles every possible exception that can occur.
Let us only handle `ValueError`s...

```python
try:
    raw_string = input("Enter a year: ")
    year = int(raw_string)

except ValueError:
    print(f'"{raw_string}" is not a valid year')
```

Our output is now...

> ```
> Enter a year: ^CTraceback (most recent call last):
>   File "/home/tkennedy/Courses/Reviews/cs263/Module-07/exception_ex_2.py", line 12, in <module>
>     main()
>   File "/home/tkennedy/Courses/Reviews/cs263/Module-07/exception_ex_2.py", line 4, in main
>     raw_string = input("Enter a year: ")
> 
> KeyboardInterrupt
> ```

While this example might demonstrate a small inconvenience... imagine debugging
that in a larger program within function that is multiple function calls deep.


# What is the "as" For?

That leaves the `as _err`. Sometimes you want to perform further handling of an
error. *For the moment... let us acknowledge that additional handling is
possible while deferring further discussion.*

```python
def main():

    try:
        raw_string = input("Enter a year: ")
        year = int(raw_string)

    except ValueError as _err:
        print(f'"{raw_string}" is not a valid year')


if __name__ == "__main__":
    main()
```

The underscore indicates that, by convention the `_err` variable while named...
is not used. *In general a variable that starts with an underscore is
understood to be needed syntacticly, but is not used in the code.* An example
of this is shown in the following code snippet.

```python
for _ in range(1, 4):
    print("Hello!)
```

The loop prints `"Hello!`" four (4) times. While a variable is need to control
the loop, the actual loop count is never used.
