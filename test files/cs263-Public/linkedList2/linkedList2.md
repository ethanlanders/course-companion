Title: Building a Linked List - Part 2
TOC: yes
Author: Thomas J. Kennedy


# What is the Goal?

In the [previous lecture](doc:linkedList1)... we left of with a
[`LinkedList` class and an initial test
suite](@gitRepoURL@/tree/main/Module-10-Linked-List/Example-1). However, we
never identified an end goal. Why build a Linked List class?

  1. We need a case study for interfaces with an emphasis on abstract base
     classes.

  2. One should always know how to build an iterator.

  3. Contrived examples are never fun... we need a non-trivial example to
     discuss how to add support for `extend` functionality, the `in` keyword.

     *The contrived examples note refers to the cliché polymorphism "animals
     eat" inheritance hierarchy that is common to most OOP texts.*

Let us state our goal succinctly...

> **We want a `LinkedList` class that can be used as a drop-in replacement for
> the built-in Python `list`.**


# Okay... What Comes First?

An `Iterator` is the first piece of the puzzle. Our current implementation
allows us to store data, but not retrieve that data. In fact... `__str__` is
the only way to see the stored data.

Let us start with two abstract base classes from the Python [`collections.abc`
module](https://docs.python.org/3/library/collections.abc.html#module-collections.abc):

  - `Iterator` - this abstract base class (ABC) is used to traverse a data
    structure without having to worry about the specific data structure. Think
    of this as a general notion of *position*.

  - `Iterable` - this ABC indicates that a class provides an iterator.


We will need to 

  1. tweak our code to include
  
    ```python
    import collections.abc
    ```
  
  2. tweak the beginning of the class definition
  
    ```python
    class LinkedList(collections.abc.Iterable)
    ```
  
  3. add an inner `Iterator` after `Node`
  
    ```python
        class Iterator(collections.abc.Iterator):
            pass
    ```


# Implementing an Iterator

Let us put everything together.

^^^[Draft Linked List Class]
```python
class LinkedList(collections.abc.Iterable):
    @dataclass
    class Node:
        data: Any = None
        next_node: Node = None

    class Iterator(collections.abc.Iterator):
        def __init__(self, starting_node=None):
            self.current_node = starting_node

        def __next(self):
            raise StopIteration()

    def __init__(self):
        self.head: Node = None
        self.tail: Node = None
        self.length: int = 0

    def __append_first(self, val):
        """
        Add the very first node
        """

        new_node = LinkedList.Node(val)

        self.head = new_node
        self.tail = new_node

        self.length = 1

    def __append_general(self, val):
        """
        Add every node other than the first node
        """

        new_node = LinkedList.Node(val)

        # Add the new node after the current tail
        self.tail.next_node = new_node

        # The new node is now the tail
        self.tail = new_node

        self.length += 1

    def append(self, val: Any) -> None:
        """
        Add a piece of data (entry) to the end of the list. If the list is
        currently empty, this new entry will be both the first and last entry
        in the list.

        Args:
            val: piece of data to store
        """

        if not self.head:
            self.__append_first(val)

        else:
            self.__append_general(val)

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> LinkedList.Iterator:
        return LinkedList.Iterator()

    def __str__(self) -> str:
        """
        Iterate through the LinkedList and print each individual Node
        with an index.
        """

        output_str = ""
        idx = 0

        it = self.head

        while it:
            output_str += f"Node #{idx:} contains {it.data}\n"

            it = it.next_node
            idx += 1

        return output_str

```
^^^

Let us start with the `Iterator`.

```python
    class Iterator(collections.abc.Iterator):
        def __init__(self, starting_node=None):
            self.current_node = starting_node

        def __next__(self):
            raise StopIteration()
```

You probably noticed the earlier typo (i.e., `__next` instead of `__next__`).
That was the first fix.

Take note of the class itself. The `__init__` method takes a single argument
`starting_node` which defaults to `None`. The `self.current_node` data member
will be used to keep track of the position as we move through a list.

```python
        def __next__(self):
            raise StopIteration()
```

When an `Iterator` runs out of entries (i.e., reaches the end of a collection)
a `StopIteration` error is used to stop the loop (e.g., `for val in
collection`) or `next` being used to retrieve data from the container.

In our case...

```python
        def __next__(self):
            if not self.current_node:
                raise StopIteration()
```

the first step is to check if `self.current_node` is `Node`. If it is... there
is no more data left. Otherwise we need to:

  1. Create a temporary reference to data within the current node

  2. Move to the next node

  3. Return the temporary reference

```python
        def __next__(self):
            if not self.current_node:
                raise StopIteration()

            value = self.current_node.data

            # Move to the next node
            self.current_node = self.current_node.next_node

            return value
```

Once `LinkedList.__next__` implementation is complete. The
`LinkedList.__iter__` method is a one liner.

```python
    def __iter__(self) -> LinkedList.Iterator:
        return LinkedList.Iterator(starting_node=self.head)
```

I have opted to use the explicit keyword argument here... for readability.


# The Iterator was the Key

The next few updates to `LinkedList` will focus on functionality that was
either:

  1. difficult to implement without a `LinkedList.Iterator`

  2. near impossible to implement without a basic understanding of iterators.


## Rewriting Dunder str

Now that we have an `Iterator` the `__str__` method can be changed from a
`while` loop...

```python
        output_str = ""
        idx = 0

        it = self.head

        while it:
            output_str += f"Node #{idx:} contains {it.data}\n"

            it = it.next_node
            idx += 1

        return output_str
```

to a `for` loop...

```python
        output_str = ""

        for idx, data in enumerate(self):
            output_str += f"Node #{idx:} contains {data}\n"

        return output_str
```

We can replace this with a generator expression combined with a call to
`"\n".join`. This change will solve both the string concatenation issue and the
trailing newline issue.

```python
        return "\n".join(
            f"Node #{idx:} contains {data}" for idx, data in enumerate(self)
        )
```

The final implementation of `__str__` can (and should) be done in one line.


## Comparing for Equality

We can now add a `__eq__` method to compare two `LinkedList`s for equality. You
will note that this `LinkedList` discussion has relaxed the *pydoc
documentation for every method* rule. Remember...

  1. **practicality beats purity** - the purpose of most functions is captured
     by their names and arguments (e.g., `append` which mirrors the
     `list.append` method).

  2. **readability counts** - additional *redundant* documentation can make
     code less readable, especially if there happen to be typos.

Just like `__str__`, `__eq__` needs explicit documentation to capture not the
purpose of the function, but the actual criteria used to check for equality.

```python
    def __eq__(self, rhs: LinkedList) -> bool:
        """
        Compare two LinkedList objects for equality based on the elements in
        each list. The two lists must:

            1. Have the same number of elements
            2. Contain identical elements
            3. Contain the identical elements in the same order
        """
```

We will start with two checks...


```python
        if not isinstance(rhs, LinkedList):
            return False
```

Let us restrict the comparison to two `LinkedList` objects. If `rhs` is another
type... it cannot be equal to a `LinkedList`. *(While it is possible to relax
this requirement... we will not do so here.)*

```python
        if len(self) != len(rhs):
            return False

        return False
```

The next check is the length. Two `LinkedList` objects (i.e., `self` and `rhs`)
cannot be equal if they contain different numbers of elements. The final
`return False` is a placeholder for the remaining check.

If we make it past the length check... we know that the two lists contain the
same number of elements. Since we have the `LinkedList.Iterator`... we can use
`zip` to step through both lists simultaneously.

```python
        for lhs_datum, rhs_datum in zip(self, rhs):
            if lhs_datum != rhs_datum:
                return False

        return True
```

Note the loop... as soon as we encounter a pair of elements that are not
equal... we can stop:

  1. To confirm the equality of two lists... we need only find a single pair of
     entries that differ. While there may be more... it does not matter if one
     value differs of multiple values differ.

  2. To confirm that two lists are equal... every pair of values must be equal.

The `any` or `all` keywords can both be used to simplify the loop.

  1. If `any` pair of values (i.e., `lhs_datum, rhs_datum`) is not equal return False.

    ```python
            if any(lhs_datum != rhs_datum for lhs_datum, rhs_datum in zip(self, rhs)):
                return False

            return True
    ```

  2. Return whether all pairs of values **are** equal

    ```python
            return all(lhs_datum == rhs_datum for lhs_datum, rhs_datum in zip(self, rhs))
    ```

My preference, in this case, is for the latter option (i.e., `all`).


## Now for Copying

Let us now implement the `__deepcopy__` method. We would like the ability to
create an identical copy of a list *with a separate* copy of all data.

```python
    def __deepcopy__(self, memo) -> LinkedList:

        list_copy = LinkedList()
        for entry in self:
            list_copy.append(copy.deepcopy(entry))

        return list_copy
```

Now that we have our own iterator... we can write functions that examine or
retrieve data more quickly (as you may have noticed with `__str__` and
`__eq__`).

Note that literal values (such as `int` and `str`) do not actually get copied.
All references to a `7` will reference the same `7`. The copy logic is intended
for **mutable** objects (e.g., `list`, or user-defined classes/objects).


# Adding Data with "extend"

The `list` class provides an `extend` method that allows multiple values to be
added *at the same time* instead of *one at a time* with multiple calls to
`append`. 

```python
    def extend(self, collection: collections.abc.Iterable) -> None:
        """
        Take every value in collection, create a new Node, and append it to
        this list
        """

        for value in collection:
          self.append(value)
```

> Yes... the `extend` method is using a for loop **and** calling `append` within
> the loop. We will discuss how to optimize this function in the next lecture.

Did you notice how `collection` is an `Iterable`? It does not matter where the
data comes from (e.g., generator or `list`). If we can iterate over the data...
our loop can handle it.


# Adding Debugging Output

`LinkedList` provides a `__str__` for *human readable* (i.e., production
output). We need a `__repr__` which provides debugging output... ideally this
output takes the form of Python code that can recreate an identical object.

Consider...

```python
ll = LinkedList()
ll.append(2)
ll.append(3)
ll.append(5)
ll.append(7)

print(f"{ll!r}")
```

This code should generate, as output...

>
> **Expected Output**
>
> ```
> LinkedList(2, 3, 5, 7)
> ```

Let us add `__repr__` to `LinkedList`.

```python
    def __repr__(self) -> str:

        inner_data_str = ", ".join(f"{datum!r}" for datum in self)

        return f"LinkedList({inner_data_str})"
```

However, our constructor does not support arguments... and we want to supply
multiple arguments. First... let us make a subtle change...

```python
    def __repr__(self) -> str:

        inner_data_str = ", ".join(f"{datum!r}" for datum in self)

        return f"LinkedList(({inner_data_str}))"
```

Take note of the double parens in `LinkedList((...))`. We are going to update
`__init__` to accept an `Iterable`... and a `tuple` is iterable!

>
> **Updated Output**
>
> ```
> LinkedList((2, 3, 5, 7))
> ```


# Updating dunder init

The `__init__` signature will mirror that of `append`:

```python
    def __init__(self, initial_data: collections.abc.Iterable = None):
        self.head: Node = None
        self.tail: Node = None
        self.length: int = 0

        # Use extend to add any starting data
        if initial_data:
            self.extend(initial_data)
```

The only addition to the function body is a conditional block that calls
`extend` if starting data was provided.


# The Code So Far...

The current (complete) `LinkedList` class from this example can be found (along
with a test suite) in [Module-10-Linked-List/Example-2 in the Example Code
Repository](@gitRepoURL@/tree/main/Module-10-Linked-List/Example-2).

Now that we have a reasonably complete `LinkedList`... we can discuss some
refactoring and the Python protocol mechanic. But... that will be the next
lecture.
