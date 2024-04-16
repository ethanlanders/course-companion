Title: Code Documentation & Type Hints
TOC: yes
Author: Thomas J. Kennedy


Most of your code has probably had quite a few in-line comments. Inline
comments are not the focus of this discussion. The focus of this discussion is
documentation of classes, functions, and methods.


# A Few Starting Examples

I work in few different languages. Throughout my

  - C++ code you will find <a href="http://www.doxygen.nl/" target="_blank">Doxygen style comments</a>.
  - Java code you will find <a href="https://www.oracle.com/technetwork/java/javase/documentation/index-137868.html" target="_blank">Javadoc style comments</a>.
  - Python code you will find Pydoc style comments.
  - Rust code you will find <a href="https://doc.rust-lang.org/rust-by-example/meta/doc.html" target="_blank">Rustdoc style comments</a>.

You have definitely been told to "comment your code" in the past, but
(probably) in a less formal fashion. 

Let us start with a few selected documentation examples from my [CS
330](https://www.cs.odu.edu/~tkennedy/cs330/latest) and [CS
417](https://www.cs.odu.edu/~tkennedy/cs417/latest) notes.


## C++

Doxygen can be used for *C++*. Consider the following Doxygen Example:

\bExample{C++ Doxygen Documentation}

```cpp
/**
 * Retrieve the value stored in three selected Cells
 *
 * @param cell1Id numeric id representing the 1st desired cell
 * @param cell2Id numeric id representing the 2nd desired cell
 * @param cell3Id numeric id representing the 3rd desired cell
 *
 * @return value stored in the Cell
 *
 * @pre (cell1Id > 0 && cell1Id < 10) &&
 *      (cell2Id > 0 && cell2Id < 10) &&
 *      (cell3Id > 0 && cell3Id < 10)
 */
CellTriple get3Cells(int cell1Id, int cell2Id, int cell3Id) const;
```

\eExample


## Java

Javadoc can be used for Java. Consider the following Javadoc Example:

\bExample{Javadoc Documentation}

```java
/**
 * Multi-thread Coin Flip.
 *
 * @param numTrials # flips to simulate
 * @param numThreads number of threads to use
 *
 * @return Completed FlipTasks
 *
 * @throws InterruptedException if a thread is stopped prematurely
 */
public static FlipTask[] multiThread(long numTrials, int numThreads)
    throws InterruptedException
```

\eExample


## Python

Pydoc or Sphinx can be used for Python. Consider the following Pydoc Example:

\bExample{Python 3 Pydoc Documentation}

```python3
def parse_raw_temps(original_temps: TextIO,
                    step_size: int=30, units: bool=True) -> Iterator[Tuple[float, List[float]] ]:
    """
    Take an input file and time-step size and parse all core temps.

    :param original_temps: an input file
    :param step_size:      time-step in seconds
    :param units: True if the input file includes units and False if the file
                  includes only raw readings (no units)

    :yields: A tuple containing the next time step and a List containing _n_
             core temps as floating point values (where _n_ is the number of
             CPU cores)
    """
```
\eExample

I prefer the Sphinx/Google style for Python.

\bExample{Python 3 Sphinx/Google Style Documentation}

```python3
def parse_raw_temps(original_temps: TextIO,
                    step_size: int=30, units: bool=True) -> Iterator[Tuple[float, List[float]] ]:
    """
    Take an input file and time-step size and parse all core temps.

    Args:
        original_temps: an input file
        step_size: time-step in seconds
        units: True if the input file includes units and False if the file
            includes only raw readings (no units)

    Yields:
        A tuple containing the next time step and a List containing _n_
        core temps as floating point values (where _n_ is the number of
        CPU cores)
    """
```
\eExample


## Rust

\bExample{Rust Documentation}

```rust
///
/// Take a room and change the flooring
///
/// # Arguments
///
///   * `original` - House to change
///
/// # Returns
///
/// House with the updated flooring
///
fn upgrade_flooring(original: &House) -> House {
    //...
}
```

\eExample

Rust and Python have similar documentation styles (give or take some `markdown`
formatting). Since we only cover small snippets of Rust in this course (for
context), we will forgo a complete
<a href="https://doc.rust-lang.org/rustdoc/what-is-rustdoc.html" target="_blank">Rustdoc</a> discussion.


# Writing Good Documentation

All code should be properly *and fully* documented using a language appropriate
comment style. All functions (including parameters and return types) must be
documented.


## Documentation for a New Function

Suppose we have just finished writing a quick program to simulate a trick coin
(i.e., a coin where heads and tails are not equally probable).

```python
def one_flip(p):
    return True if random.random() < p else False


def main():

    num_flips = 8;

    for _i in range(0, num_flips):
        if one_flip(0.7):
           print("Heads")

        else:
            print("Tails")

if __name__ == "__main__":
    main()
```

The `one_flip` function needs a description.

```python
def one_flip(p):
    """
    Simulate a single coin flip.
    """
```

What does `p` represent? Does it represent the probability of heads or tails?

```python
def one_flip(p):
    """
    Simulate a single coin flip.

    Args:
        p: probability of heads in the range [0, 1]
    """
```


Now what about the return? We know that `bool` means a `true` or `false`. Which
one do I get for heads? Let us add an `@return`.

```python
def one_flip(p):
    """
    Simulate a single coin flip.

    Args:
        p: probability of heads in the range [0, 1]

    Returns:
        True if the result is heads and False if the result is tails
    """
```

There is no more ambiguity or guesswork. Both `p` and the possible return
values are documented.


## Function Type Hints


I am a stickler for <a href="https://www.python.org/dev/peps/pep-0484/" target="_blank">type hints...</a>

```python
def one_flip(p: float) -> bool:
    """
    Simulate a single coin flip.

    Args:
        p: probability of heads in the range [0, 1]

    Returns:
        True if the result is heads and False if the result is tails
    """
```

Now... we know that

  - `p` is a `float` (i.e., a real number) and not an `int`

  - `one_flip` returns a `bool` value

As general rules, forgo:

  - listing the types in the pydoc documentation and use type hints instead
  - including type hints if there is any possibility of ambiguity (e.g., using `-> None`)

It is possible to annotate variables. However, variables generally have more
context, e.g.,

  - A literal value is assigned to the variable.

    ```python
    price = 1.52
    ```

  - The variable stores the result of a function call (with an annotated return
    type)

    ```python
    new_price = discount_by_10_percent(price)
    ```
