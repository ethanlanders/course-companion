Title: Conditional Blocks & "while" Loops
TOC: yes
Author: Thomas J. Kennedy


# "if" & "else"

Python has `if`, `if`-`else`, and `if`-`elif`-`else` similar to most languages.
Suppose that we were to prompt a user for their favorite color.

\bSidebar

We all know that blue is the best color.

\eSidebar

```python
def main():
    color = input("What is your favorite color? ")

    if color.lower() == "blue":
        print("Blue is the best color.")

    else:
        print(f"{color.title()} is a color.")


if __name__ == "__main__":
    main()
```

We could be a little more fair...

```python
def main():
    color = input("What is your favorite color? ")
    color = color.lower()

    if color == "blue":
        print("Blue is the best color.")

    elif color == "purple" or color == "lavender":
        print(f"{color.title()} is a good choice.")

    else:
        print(f"{color.title()} is a color.")


if __name__ == "__main__":
    main()
```

Take note of the `elif` and the compound conditional. C++ and Java use...

  - `else if` instead of `elif`

  -  `&&` instead of `and`

  - `||` instead of `or`


# While You Wait...

Let us look at something a little more... objective. Consider the number guessing game.

> *Pick a number between 1 and 100.*

Let us start with some quick pseudocode

```python
def main():

    # while guess is not correct:
        # prompt "Is your number {guess}? (y/n): "

        # if answer is yes:
            # print "I win!"
            # exit

        # else answer is no:
            # prompt "Was my guess too high or too low? (h/l): "

            # if too high:
                # upper_limit = guess

            # else too low:
                # lower_limit = guess

            # next_guess = lower_limit + (upper_limit - lower_limit) // 2


if __name__ == "__main__":
    main()
```

Before we move on... I would like to move the guess logic to a separate
function...

```python
def get_next_guess(lower_limit, upper_limit) -> int:
    return lower_limit + (upper_limit - lower_limit) // 2
```

and get the next guess at the start of the loop...

```python
def main():

    lower_limit = 1
    upper_limit = 100

    # while guess is not correct:
        guess = get_next_guess(lower_limit, upper_limit)

        # prompt "Is your number {guess}? (y/n): "

        # if answer is yes:
            # print "I win!"
            # exit

        # else answer is no:
            # prompt "Was my guess too high or too low? (h/l): "

            # if too high:
                # upper_limit = guess

            # else too low:
                # lower_limit = guess


if __name__ == "__main__":
    main()
```

The user prompts can be added fairly quickly (based on previous lectures).

```python
def main():

    lower_limit = 1
    upper_limit = 100

    # while guess is not correct:
        guess = get_next_guess(lower_limit, upper_limit)

        answer = input("Is your number {guess}? (y/n):") 
        answer = answer.lower()[0]

        # if answer is yes:
            # print "I win!"
            # exit

        # else answer is no:
            answer = input("Was my guess too high or too low? (h/l)")
            answer = answer.lower()[0]

            # if too high:
                # upper_limit = guess

            # else too low:
                # lower_limit = guess


if __name__ == "__main__":
    main()
```

Take note of how the answers were processed...

```python
        answer = answer.lower()[0]
```

We want the first letter from the answer (i.e., `[0]`). We would also like to
accept an uppercase or lowercase letters. In this case... we converted the
letter to lowercase with `.lower()`.

We can use the same `answer` variable for both prompts.


# Adding the Loop and Conditions

We will start with a `while True:` (and replace it later). The conditional
blocks can be written alongside the loop condition.

```python
import sys


def get_next_guess(lower_limit, upper_limit) -> int:
    return lower_limit + (upper_limit - lower_limit) // 2


def main():

    lower_limit = 1
    upper_limit = 100

    while True:
        guess = get_next_guess(lower_limit, upper_limit)

        answer = input(f"Is your number {guess}? (y/n): ")
        answer = answer.lower()[0]

        if answer == "y":
            print("I win!")
            sys.exit(0)

        elif answer == "n":
            answer = input("Was my guess too high or too low? (h/l): ")
            answer = answer.lower()[0]

            if answer == "h":
                upper_limit = guess

            elif answer == "l":
                lower_limit = guess


if __name__ == "__main__":
    main()
```

Most of the pseudocode (e.g., `lower_limit = guess`) was actually valid Python.

**Do not use `sys.exit`.** A call to `sys.exit` should only occur if an error
occurs, and never from within a loop. Let us replace sys.exit` with `break` to
exit the loop.

```python
def get_next_guess(lower_limit, upper_limit) -> int:
    return lower_limit + (upper_limit - lower_limit) // 2


def main():

    lower_limit = 1
    upper_limit = 100

    while True:
        guess = get_next_guess(lower_limit, upper_limit)

        answer = input(f"Is your number {guess}? (y/n): ")
        answer = answer.lower()[0]

        if answer == "y":
            print("I win!")
            break

        elif answer == "n":
            answer = input("Was my guess too high or too low? (h/l): ")
            answer = answer.lower()[0]

            if answer == "h":
                upper_limit = guess

            elif answer == "l":
                lower_limit = guess


if __name__ == "__main__":
    main()
```

We should get rid of the break... by...

  1. initializing `guess` to `n`

  2. updating the loop condition

  3. removing `break`

```python
def get_next_guess(lower_limit, upper_limit) -> int:
    return lower_limit + (upper_limit - lower_limit) // 2


def main():
    lower_limit = 1
    upper_limit = 100

    answer = "n"
    while answer != "y":
        guess = get_next_guess(lower_limit, upper_limit)

        answer = input(f"Is your number {guess}? (y/n): ")
        answer = answer.lower()[0]

        if answer == "y":
            print("I win!")

        elif answer == "n":
            answer = input("Was my guess too high or too low? (h/l): ")
            answer = answer.lower()[0]

            if answer == "h":
                upper_limit = guess

            elif answer == "l":
                lower_limit = guess


if __name__ == "__main__":
    main()
```

I am much happier with that. 


# We are Done... For Now

The full code can be found in
<a href="@gitRepoURL@/tree/main/Module-05/While-Loop-1/guess.py" target="_blank">Module-05-While-Loop-1/guess.py</a>.
