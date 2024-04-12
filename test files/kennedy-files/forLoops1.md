Title: "for" Loops
TOC: yes
Author: Thomas J. Kennedy

# Python's "for" is not Count Based

The Python `for` loop is a range based or for each loop. If you come from C++
or Java... that is definitely... confusing.

We explored that for each loop a little in the [command line arguments
lecture](doc:clArgs). Let us take a step back... and examine a count based for
loop.


# A Quick Problem

Suppose that we want to output the even numbers between two (2) and one
hundred (100), including both 2 and 100, that are not divisible by four (4).

We would start with...

```python
def main():
    for num in range(2, 102, 2):
        print(f"{num:>3}")


if __name__ == "__main__":
    main()
```

The loop will grab every `num` starting at `2` and ending at `100`. At each
step `num` will be incremented by `2`. The next step is to add a conditional block to
skip numbers that are divisible by `4`

```python
def main():
    for num in range(2, 102, 2):
        if num % 4 != 0:
            print(f"{num:>3}")


if __name__ == "__main__":
    main()
```

Although my preference would be to flip the condition and `continue` (or skip)
to the next loop iteration.

```python
def main():
    for num in range(2, 102, 2):
        if num % 4 == 0:
            continue

        print(f"{num:>3}")


if __name__ == "__main__":
    main()
```

This decreases nesting (and is a useful trick for making code more readable).
Imagine a problem where instead of one (1) such check we have three (3) or four
(4) conditions to check.


# Reversing the Problem

Suppose that we want to output numbers starting at `100` and stopping at `2`. A
quick call to `reversed` will do the trick.

```python
def main():
    for num in reversed(range(2, 102, 2)):
        if num % 4 == 0:
            continue

        print(f"{num:>3}")


if __name__ == "__main__":
    main()
```


# Is That It?

That is it... for now. We will see `for` again in future lectures on input
files  and `list`.
