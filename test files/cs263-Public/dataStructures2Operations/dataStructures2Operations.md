Title: Working with Python's list
TOC: yes
Author: Thomas J. Kennedy


# Overview & Basic Operations

The `list` is one of most commonly used data structures in Python. The basic
operations include:

  1. `append` to add an entry to the end of a list

  2. `extend` to add multiple values from another `list` (or other `Iterable`).

  3. `insert` to add an entry in the middle of a `list`

  4. `count` to find the number of occurrences of  specific value within a
     `list`.


## List Slicing & Indices

The `list` provides a *slicing* syntax that allows not just one value, but a
range of values to be retrieved. If we needed to print the first ten (10)
values of a list...

```python
print(some_list[:10])
```

would the items from index zero (0) through nine (9), inclusive. Even more
powerful is *negative indexing*. We can grab the last element with...

```python
print(some_list[:-1])
```

We could even grab every third element between indices seven (7) and fifteen
(15), not including fifteen (15).

```python
print(some_list[7:15:3])
```

Of course... some of this seems like a *solution in search of a problem*, at
least in isolation.


## Common Operations

Python provides `min`, `max`, `sum`, and `sort` operations. *(While there are
more functions, e.g., `filter`, we will focus on the basics.)*


# Case Study

While the mechanics, syntax, and flexibility of lists can be interesting... we
actually want to solve a problem. Suppose that we have a list of words in a
file named *words.txt*.

\bExample{words.txt}

```
C++
Java
Python
loop
Lua
Perl
PHP
Wikipedia
.NET
Rust
Minecraft
Persona
Scratch
HTML
ZFlip 3
RaspberryPi
Steam Deck
CSS
JavaScript
``` 
\eExample

A few of these *words* are noun phrases (i.e., more than one word).


## A Simple Start

Let us start by outputting a sorted list of words.

\bExample{process_words.py - First Attempt}

The full code can be found in the course [GitHub
Repository](@gitRepoURL@/tree/main/Module-06/Example-1/process_words.py)

```python
def main():
    word_filename = sys.argv[1]

    with open(word_filename, "r") as word_file:
        words = [line.strip() for line in word_file]

    for word in sorted(words):
        print(f"|{word}|")


if __name__ == "__main__":
    main()
```
\eExample

When the program is run using...

```console
python3.11 process_words.py words.txt
```

it generates the following output...

```console
||
|.NET|
|C++|
|CSS|
|HTML|
|Java|
|JavaScript|
|Lua|
|Minecraft|
|PHP|
|Perl|
|Persona|
|Python|
|RaspberryPi|
|Rust|
|Scratch|
|Steam Deck|
|Wikipedia|
|ZFlip 3|
|loop|
```

The vertical pipe characters (i.e., '`|`') are used to confirm that all leading
and trailing whitespace has been removed. **Do you notice a problem?** The
words are sorted lexicographically.

> *A lexicographical sort uses a defined ordering to arrange (sort) data.
> Unlike *alphabetical order* which is restricted to an alphabet, a
> lexicographical sort can apply any ordering which allows uppercase letters,
> lowercase letters, numbers and symbols to be included.*
>
> *We could even apply a lexicographical sort to the Unicode character set which
> included letters from (almost) every language (and emoji).*

In most cases... our intention would be for words to be sorted with case being
ignored.

We just need to add a `key` argument to the `sorted` function call.

```python
    for word in sorted(words, key=lambda word: word.lower()):
        print(f"|{word}|")
``` 

Take note of the lambda function. This is a one-off function that takes a
single string (`word`) and converts it to lowercase (`word.lower()`) before
comparing it to other words.

While this will work for English words... [the notion of case in other
languages can be interesting](https://docs.python.org/3/library/stdtypes.html?highlight=lower#str.casefold).
The Pythonic approach is to use `casefold`.

```python
    for word in sorted(words, key=lambda word: word.casefold()):
        print(f"|{word}|")
``` 

However, the code can actually written more succinctly as

```python
    for word in sorted(words, key=str.casefold):
        print(f"|{word}|")
``` 

We do not need a full lambda function. Since Python treats functions as
first-class objects... we can pass in a reference to the function we wish to
have invoked on each string. *(In C++ this would usually be achieved function
pointer and/or templates.)*

The updated `process_words.py` can be found in the course [GitHub
Repository](@gitRepoURL@/tree/main/Module-06/Example-2/process_words.py)


## Filtering Words

Now that we can sort words... suppose that we want to

  1. skip the blank word (i.e., `||`) in the output.

  2. skip noun phrases (i.e., any line that contains a space between two or
     more words, numbers, or symbols (e.g., *Steam Deck*).

  3. ignore any word that contains a `.`, `+`, or `-`

We might be tempted to rewrite...

```python
    # Grab all tokens that are not an empty string
    words = [word for word in words if word]

    # Grab all words that do not contain a space
    words = [word for word in words if " " not in word]

    # Grab all words that do not contain a ., +, or -
    words = [word for word in words if "." not in word and "+" not in word and "-" not in word]
```

A smart alec might even rewrite the last list comprehension to be a nested list
comprehension.

```python
    # Grab all words that do not contain a ., +, or -
    symbol_blacklist = [".", "+", "-"]
    words = [word for word in words if all(symbol not in word for symbol in symbol_blacklist)]
```

But this is not `r/iamverysmart` or `r/programmerhumour`. We are writing Python
code and PEP 20 says...

> - *Readability counts*
>
> - *Simple is better than complex.*
>
> - *If the implementation is hard to explain, it's a bad idea.*

Let us rethink the overuse of list comprehensions.


## Refactoring

Let us rewrite the code so that `main` calls an `apply_word_filters` function.

\bExample{Updated main}

```python
def main():
    word_filename = sys.argv[1]

    with open(word_filename, "r") as word_file:
        words = [line.strip() for line in word_file]

    filtered_words = apply_word_filters(words)
    for word in sorted(filtered_words, key=str.casefold):
        print(f"|{word}|")
```

\eExample

\bExample{apply_word_filters}

```python
def apply_word_filters(words: Iterable[str]) -> Iterable[str]:
    """
    Take a collection of words and apply the following filters:

       1. skip empty strings

       2. skip noun phrases (i.e., any token that contains a space between two
          or more words, numbers, or symbols (e.g., Steam Deck).

       3. ignore any word that contains a ., +, or -
    """

    # Grab all tokens that are not an empty string
    words = [word for word in words if word]

    # Grab all words that do not contain a space
    words = [word for word in words if " " not in word]

    # Grab all words that do not contain a ., +, or -
    symbol_blacklist = [".", "+", "-"]
    words = [word for word in words if all(symbol not in word for symbol in symbol_blacklist)]

    return words
```

\eExample

The first list comprehension is follows the Python convection for an empty
string check.

```python
    words = [word for word in words if word]
```

While C++ or Java programmers might write something along the lines of...

```python
    words = [word for word in words if len(word) > 0]
```

most code reviews and linting tools would flag it. The second comprehension

```python
    # Grab all words that do not contain a space
    words = [word for word in words if " " not in word]
```

is good "as is." While one might be tempted to rewrite it as...

```python
    # Grab all words that do not contain a space
    words = [word for word in words if word.find(" ") >= 0]
```

the official [`str.find`
documentation](https://docs.python.org/3/library/stdtypes.html#str.find)
indicates that `in` is the *accepted* approach.

That just leaves the final list comprehension.

```python
    symbol_blacklist = [".", "+", "-"]
    words = [word for word in words if all(symbol not in word for symbol in symbol_blacklist)]
```

I think a `not`-`any`-`in` approach would be more readable.

```python
    words = [
        word for word in words if not any(symbol in word for symbol in symbol_blacklist)
    ]
```

That leaves us with a (more-or-less) final filter function.

\bExample{apply_word_filters}

```python
DEFAULT_SYMBOL_BLACKLIST = (".", "+", "-")


def apply_word_filters(
    words: Iterable[str], symbol_blacklist: tuple[str] = DEFAULT_SYMBOL_BLACKLIST
) -> Iterable[str]:
    """
    Take a collection of words and apply the following filters:

       1. skip empty strings

       2. skip noun phrases (i.e., any token that contains a space between two
          or more words, numbers, or symbols (e.g., Steam Deck).

       3. ignore any word that contains a ., +, or -
    """

    words = [word for word in words if word]

    words = [word for word in words if " " not in word]

    words = [
        word for word in words if not any(symbol in word for symbol in symbol_blacklist)
    ]

    return words
```

\eExample

Take note of the subtle change to `symbol_blacklist`. If a function uses a blacklist...

  1. That blacklist should be passed in as an argument.

  2. If there is a default (or fallback) blacklist it should be provided as a
     default argument.

  3. A `tuple` should be used for the default since constants should be immutable.


The updated `process_words.py` can be found in the course [GitHub
Repository](@gitRepoURL@/tree/main/Module-06/Example-3/process_words.py)


## Are We Done with Filtering?

Yes... we are done with filtering words. Let us actually do some analysis
(i.e., work in `main`). Suppose that we want to output the following table...

\bExample{Desired Table}
```console
| CSS                | Lua                |
| HTML               | PHP                |
| Java               | CSS                |
| JavaScript         | Java               |
| loop               | loop               |
| Lua                | Perl               |
| Minecraft          | Rust               |
| Perl               | HTML               |
| Persona            | Python             |
| PHP                | Persona            |
| Python             | Scratch            |
| RaspberryPi        | Wikipedia          |
| Rust               | Minecraft          |
| Scratch            | JavaScript         |
| Wikipedia          | RaspberryPi        |
```
\eExample

We would take our existing loop...

```python
    for word in sorted(filtered_words, key=str.casefold):
        print(f"|{word}|")
```

and separate the sort operation.

```python
    words_sorted_lex = sorted(filtered_words, key=str.casefold)
    words_sorted_len = sorted(filtered_words, key=len)
```

Note how the sorted list from the loop is now stored in variable
(`words_sorted_lex` where `lex` is an abbreviation for lexicographical). There
is now a second list (`words_sorted_len`) where words are sorted by length.

The loop becomes...

```python
    for word_lhs, word_rhs in zip(words_sorted_lex, words_sorted_len):
        print(f"| {word_lhs:<18} | {word_rhs:<18} |")
```

Take note of `zip`. The `zip` function takes two `Iterable` collections and
retrieves corresponding pairs of items (e.g., `words_sorted_lex[0]`,
`words_sorted_len[0]`). *And... we happen to know that our two word lists have
equal length.*

The output is a little f-string formatting magic.


## What About min and max?

Suppose that we wanted to grab the three longest words from `words_sorted_len`.
Since the list is sorted by length... we can simply grab the last three (3) entries.

```python
    print()
    print("Top 3 Longest Words:")
    print()
    for word in words_sorted_len[-1:-4:-1]:
        print(f"  {word}")
```

Take not of the indices in `words_sorted_len[-1:-4:-1]`. We are...

  1. Grabbing all elements from the last index (`[-1`)

  2. down to, but not including, (`:-4:`)

  3. going backwards (`:-1]`)

That is about as *clear as mud*. I would prefer...

```python
    for word in reversed(words_sorted_len[-3:]):
        print(f"  {word}")
```

This is a bit more clear. We are starting at the *third from last entry* and
reversing the order, i,e., $-3, -2, -1$ becomes $-1, -2, -3$.

Now suppose that we want the longest word and shortest word that start with a
each letter.

[Keep in mind that `min` and `max` return the first value
encountered](https://docs.python.org/3.11/library/functions.html?highlight=min#min)
(e.g., if two words with equal length are both the shortest, `min` would return
the first one encountered). 

Let us start with finding the longest words.

\bExample{Finding the Longest Words}
```python
    for letter in ascii_lowercase:
        try:
            longest_word = max(
                (word for word in filtered_words if word.lower().startswith(letter)),
                key=len,
            )

        except ValueError as _err:
            # There were no words that started with "letter"
            # There is nothing to output
            continue

        print(f"  ({letter}) - {longest_word}")
```
\eExample

The `string` module provides the set of lowercase letters in `ascii_lowercase`.
We start by grabbing each letter.

```python
    for letter in ascii_lowercase:
```

We *attempt* look for the longest word that starts with `letter`

```python
        try:
            longest_word = max(
                (word for word in filtered_words if word.lower().startswith(letter)),
                key=len,
            )
```

If there are no letters that start with `letter`... we skip to the next loop iteration.

```python
        except ValueError as _err:
            # There were no words that started with "letter"
            # There is nothing to output
            continue
```

If a word... we output both `letter` and the word.

```python
        print(f"  ({letter}) - {longest_word}")
```

Identifying the shortest words is near identical (using `min` instead of `max`).

\bExample{Finding the Shortest Words}
```python
    for letter in ascii_lowercase:
        try:
            longest_word = max(
                (word for word in filtered_words if word.lower().startswith(letter)),
                key=len,
            )

        except ValueError as _err:
            # There were no words that started with "letter"
            # There is nothing to output
            continue

        print(f"  ({letter}) - {longest_word}")
```
\eExample

The two loops are very similar. With some care...

  1. we could refactor the two loops into a reusable function. 

  2. we could refactor the two loops into a single loop that reuses the list
     containing words that start with `letter`. 

*However, I will leave both options as exercises to the reader (i.e., you).*


# The Finished Code

The final version of `process_words.py` can be found in the course [GitHub
Repository](@gitRepoURL@/tree/main/Module-06/Example-4/process_words.py)




