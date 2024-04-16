Title: The Basic Python Data Structures
TOC: yes
Author: Thomas J. Kennedy


# What is Considered Basic?

When I work in Python, I generally focus on three core (fundamental) data
structures (or specialized variations from the `collections` module).

| Python | C++                          | Java                | Rust                           |
| :----- | :----                        | :----               | :----                          |
| `list` | `std::list` or `std::vector` | `java.util.List`    | `std::collections::LinkedList` |
| `dict` | `std::unordered_map`         | `java.util.HashMap` | `std::collections::HashMap`    |
| `set`  | `std::unordered_set`         | `java.util.HashSet` | `std::collections::HashSet`    |

Take note of the correspondence to C++ and Java. While you will encounter
**generators** and **tuples** in Python... they will be defined in the latter
part of this lecture. 


## list

A `list` is a collection of values. We could have a list of prime numbers...

```python
prime_numbers = [1, 2, 3, 5, 7, 11, 13, 17, 19]
```

or names...

```python
names = ["Thomas", "Jay", "Joe"]
```

Python lists are not restricted to storing a single type of data. For example,
we can store a string and a `float` in the same list.

```python
random_things = ["Python", 3.11]
```

## set

A `set` is similar to a `list`, except entries must be unique. If we were to
store a bunch of colors...

```python
some_colors = {"Blue", "Red", "Green", "Cyan", "Teal"}
some_colors.add("Blue")
some_colors.add("Red")
some_colors.add("Teal")
```

the last three lines would have no effect, since `"Blue"`, `"Red"`, and
`"Teal"` are already in the set.


## dict

The usual definition of a `dict` (what Java would call a `HashMap` and C++
would call an `unordered_map`) is...

> *A dictionary (hashmap) is a collection of key-value pairs where each entry can
> be located in amortized constant time.*

We can think of a `dict` as a lookup table where finding a value can be done
quickly. Suppose you needed to track the favourite colors for a group of
people...

```python
favourite_colors = {
    "Thomas": "Blue",
    "Jessica": "Purple",
    "Angela": "Pink"
}
```

We could retrieve and print my (Thomas's) favorite color with...

```python
print(favourite_colors["Thomas"])
```

We can think of a `dict` as *an array where the index can be a key that we want
to match to some value*.


# What is a Generator?

A generator is a *lazily-evaluated list*. Unlike a list where all the values
are known, a generator's values are computed on demand.

For example, the list...

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

contains the values `1` through `10` and uses 10 `int`s worth of space. Imagine
if we had one (1) billion numbers. A generator expression defines how to create
(or construct) each value, but only creates a value when specifically asked to
do so.

The `range` function is one such generator. Consider the following snippet.

```python
numbers = range(1, 100)

print(next(numbers))
print(next(numbers))
print(next(numbers))
```

The snippet would generate (as output)...

```
1
2
3
```

The remaining values would never be generated. **A generator is ideal when we
do not need every value all at once.** You have seen this with the Python `for`
loop...

```python
for num in range(1, 100):
    print(num)
```

We want to loop output the numbers `1` through `99` one at a time. Not only do
we only need one number at a time... once we have output each number we can
discard it.


# What is a Tuple?

A <a href="https://docs.python.org/3.11/tutorial/datastructures.html#tuples-and-sequences" target="_blank">`tuple`</a>
can be thought of as an immutable list. Suppose we had the heading for a program...

```python
["Generators and Lists", "Thomas J. Kennedy"]
```

where we want to store the title and author's name. This list will never be
updated (i.e., it will not change while the code is running). The tuple form...

```python
("Generators and Lists", "Thomas J. Kennedy")
```

allows us to loop over the data as before... but fixes the size of the tuple at
two (2) entries. The tuple can not have additional data stored within it (or
have data removed from it).


