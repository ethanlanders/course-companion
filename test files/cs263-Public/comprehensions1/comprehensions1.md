Title: Comprehensions - An Overview
TOC: yes
Author: Thomas J. Kennedy


The next few discussions will include [list
comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions),
dictionary comprehensions and set comprehensions.


# What is a Comprehension?

At a fundamental level... a *comprehension* is a succinct notation for building
a list (or other data structure).

Suppose we need to generate a list that contains every number from one to ten
(1 to 10)...

```python
def generate_list():
    numbers = []

    for value in range(1, 11):
        numbers.append(value)

    return numbers
```

The function starts of by creating an empty list. Within the loop `append` is
called to add each new `value`. As a final step... the list (i.e., `numbers`)
is returned. In practice... this function can be replaced by a single line.

```python
    numbers = [value for value in range(1, 11)]
```

If you have worked with `range` before... even the list comprehension is too
much code...

```python
    numbers = list(range(1, 11))
```

The `list` function can convert the *Generator* produced by range into a list.
Well... this is a very simple case. What if... we needed a list of all numbers:

  - between 1 and 1000
  - **not** divisible by 3

The loop form would be something along the lines of...

```python
    numbers = []

    for value in range(1, 1001):
        if value % 3 != 0:
            numbers.append(value)
```

The list comprehension would be

```python
    numbers = [value for value in range(1, 1001) if value % 3 != 0]
```


# Word Counts & Comparing to C++ and Java

Suppose we have a list of programming terms and want to create a second list
containing the length of each term. We might take the usual C, C++, or Java
approach:

\bExample{Word Count - Boring C++ Loop}

```cpp
using std::string;
using std::vector;


int main(int argc, char** argv)
{
    vector<string> some_terms {"Hello", "world", "with", "for", "while", "int"};
    vector<int> term_lengths(some_terms.size(), 0);

    for (int i = 0; i < term_lengths.size(); i++) {
        term_lengths[i] = some_terms[i].size();
    }

    return 0;
}
```

\eExample

and translate it into Python:

\bExample{Word Count - Boring Python Loop}

```python
def main():
    some_terms = ["Hello", "world", "with", "for", "while", "int"]

    term_lengths = []

    for term in some_terms:
        term_lengths.append(len(term))


if __name__ == "__main__":
    main()
```

\eExample

The Python version can (and should) use a list comprehension.

\bExample{Word Count - Fun Python Loop}

```python
def main():
    some_terms = ["Hello", "world", "with", "for", "while", "int"]

    term_lengths = [len(term) for term in some_terms]


if __name__ == "__main__":
    main()
```

\eExample

Depending on how many terms we have... a generator expression might be more
appropriate:

\bExample{Word Count - Really Fun Python Loop}

```python
def main():
    some_terms = ["Hello", "world", "with", "for", "while", "int"]

    term_lengths = (len(term) for term in some_terms)


if __name__ == "__main__":
    main()
```

\eExample


## Modern C++ and std::transform

Modern C++11 and newer provide the `std::transform` method. Combined with
`lambda functions` we can take the original C++ code... and rewrite it as

\bExample{Word Count - C++ `std::transform`}

```cpp
using std::string;
using std::vector;


int main(int argc, char** argv)
{
    vector<string> some_terms {"Hello", "world", "with", "for", "while", "int"};
    vector<int> term_lengths;

    std::transform(some_terms.begin(), some_terms.end(), std::back_inserter(term_lengths),
                   [](const string& t) -> int {
                       return t.size();
                   });

    return 0;
}
```

\eExample


## Java and the Stream API

Java has the `java.util.stream` package, which provides similar functionality
to Python comprehensions and C++ `std::transform`. However, in Java, we would
end up dealing with the `Integer` wrapper class if we wanted to use a non-array
data structure.

\bExample{Word Count - Java Streams}

```java
import java.util.Arrays;
import java.util.List;

public class IntStreamDemo
{
    public static void main(String... args)
    {
        List<String> some_terms = Arrays.asList("Hello", "world", "with",
                                                "for", "while", "int");

        int[] term_lengths = some_terms.stream()
                           .mapToInt(s -> s.length())
                           .toArray();
    }
}
```

\eExample

**The Python implementation is the most succinct, approachable, and readable.**

