Title: Building a Linked List - Part 3
TOC: yes
Author: Thomas J. Kennedy


# What About Our Goal?

The previous lecture focused on adding functionality to our `LinkedList`
implementation with the end goal of building a **drop-in replacement for
`list`.**

We are close... for the moment we need:

  1. `__contains__` to support the `in` keyword for search, e.g.,

    ```python
    if 7 in example_list:
        print('"7" was found!)
    ```

  2. `__add__` to add two `LinkedList` objects together

    ```python
    ll_1 = LinkedList(range(1, 7))
    ll_2 = LinkedList(range(20, 30))

    ll_3 = ll_1 + ll_2
    ```


## Start with Dunder add

Let us start with `__add__`. After all... it is built on what we have learned
while writing:

  - `append`
  - `extend`
  - `__init__`

We can actually implement `__add__` in ~~three~~ four lines (counting is hard)...

```python
    def __add__(self, other: collections.abc.Iterable) -> LinkedList:
        new_ll = LinkedList()
        new_ll.extend(self)
        new_ll.extend(other)

        return new_ll
```

However, we do not need to start with an empty `LinkedList`. We can actually
use the constructor to grab the first batch of data.

```python
    def __add__(self, other: collections.abc.Iterable) -> LinkedList:
        new_ll = LinkedList(self)
        new_ll.extend(other)

        return new_ll
```

Now... we actually have three lines (not counting the blank line)!

> *Even though we have not explicity referenced running a `LinkedList` test
> suite... the `test_add` function caught a few mistakes with a tweaked
> `extend` implementation (which will be discussed later in this lecture).*

Did you notice that `other` has `Iterable` listed as its type? There is no
reason to restrict `__add__` to two `LinkedList` objects. If we can iterate
over something... we can grab its data.


## Add Support for "in"

Since `in` returns `True` if a value in found within a collection... a
sequential search should be our initial choice. *(Since we have a linked
list... a sequentail search is our only choice.)*

```python
    def __contains__(self, value_to_find: Any) -> bool:
        for entry in self:
            if entry == value_to_find:
                return True

        return False
```

While the initial implementation is correct... why not use `any`?

```python
    def __contains__(self, value_to_find: Any) -> bool:
        return any(entry == value_to_find for entry in self)
```

If you have read the docs... you will know that this implementation is similar
to what is produced automatically...

> For objects that don't define `__contains__()`, the membership test first tries
> iteration via `__iter__()`...
>
> *Retrieved from <https://docs.python.org/3/reference/datamodel.html#object.__contains__>*

However, our implementation does give us a baseline... in case we decide to
implement a doubly linked list or a skip list in the future.


# Let Us Refactor

Now... it is time to start refactoring. Let us start with `__str__`.


## Remove Dunder str

While,
`__str__` does produce output and was used for debugging... we now have
`__repr__`. Keep in mind that...

  - `__str__` is meant to generate *presentable* production output

  - `__repr__` is meant to generate debugging output for developers

`LinkedList` is intended to be a used as a drop-in replacement for `list`
across multiple programs. It is a safe assumption that each of those programs
will have a different output specification. And... those programs can now
access the stored data through `LinkedList.Iterator`.

**Let us remove `__str__`.**


## Dunder repr Has a Bug

The `test_linked_list.py` test suite contains checks for `__str__` through use
of `has_string` and `string_contains_in_order` matchers. If a class does not
have a `__str__` these checks examine the output of `__repr__`.

```python
    assert_that(empty_list, has_string("LinkedList()"))
```

In the case of an empty list... we would expect that `__repr__` returns 

```console
"LinkedList()"
```

However, we end up with...

```console
"LinkedList(())"
```

A quick *early return* is the (in my opinion) most ideal solution.

```python
    def __repr__(self) -> str:
        if not self:
            return "LinkedList()"

        inner_data_str = ", ".join(f"{datum!r}" for datum in self)

        return f"LinkedList(({inner_data_str}))"
```

If the list is empty... we can just return a call to `LinkedList()`.


# Tweaking Node Creation

The `append` logic has always bothered me. When analyzing computation
complexity... we look at time vs space (i.e., runtime vs memory):

  - Do we want to use more memory and decrease runtime?

  - Do we want to use less memory at the cost of increased runtime?

Conditional blocks (e.g., `if`) have a cost. Let us revisit `append`.

```python
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
```

We know for a fact that `if not self.head` will only evaluate to `True` when
the very first `Node` is created. What if... we added an **unused** first Node?

```python
    def append(self, val: Any) -> None:
        """
        Add a piece of data (entry) to the end of the list.

        Args:
            val: piece of data to store
        """

        self.__append_general(val)
```

As long as `__init__` always adds the *placeholder first `Node`*... `append`
will always have access to a *tail `Node`*.

```python
    def __init__(self, initial_data: collections.abc.Iterable = None):
        self.head: Node = None
        self.tail: Node = None
        self.length: int = 0  # Do not include the "buffer" Node

        self.__append_first(None)

        # Use extend to add any starting data
        if initial_data:
            self.extend(initial_data)
```

**We need to update `__iter__` to *skip* to the second `Node`.**

```python
    def __iter__(self) -> LinkedList.Iterator:
        second_node = self.head.next_node
        return LinkedList.Iterator(starting_node=second_node)
```

And... the length is wrong. *(Note that `test_linked_list.py` is being run
after making each change to identify any oversights).* Let us return to
`__init__` and move the `__append_first` logic.

```python
    def __init__(self, initial_data: collections.abc.Iterable = None):
        self.head: Node = None
        self.tail: Node = None
        self.length: int = 0  # Do not include the "buffer" Node

        new_node = LinkedList.Node(data=None)

        self.head = new_node
        self.tail = new_node

        self.length = 1

        # Use extend to add any starting data
        if initial_data:
            self.extend(initial_data)
```

Ah... `self.length` was being set to `1`. Note that `length` should only be
updated when data is stored.

```python
    def __init__(self, initial_data: collections.abc.Iterable = None):
        self.head: Node = None
        self.tail: Node = None
        self.length: int = 0  # Do not include the "buffer" Node

        new_node = LinkedList.Node(data=None)

        self.head = new_node
        self.tail = new_node

        # Use extend to add any starting data
        if initial_data:
            self.extend(initial_data)
```

*Let us finally fix a type annotation mistake...*

```python
    def __init__(self, initial_data: collections.abc.Iterable = None):
        self.head: LinkedList.Node = None
        self.tail: LinkedList.Node = None
```

And... I think `__init__` is good enough now. Any further changes would, in my
opinion, decrease readabilty. 

Let us remove `__append_general` and move all of its logic into `append`.


# One More Type Annotation

There is one more type annotation to fix, `next_node: Node`.

```python
    @dataclass
    class Node:
        data: Any = None
        next_node: Node = None
```

Let us use `Self` instead of writing `LinkedList.Node`.

```python
    @dataclass
    class Node:
        data: Any = None
        next_node: Self = None
```


# That is "The End"

While we could continue tweaking our implementation... we are starting to
encounter diminishing returns. Our changes thus far have:

  1. increased readability
  2. decreased complexity
  3. fixed bugs
  4. brought us in line with the Python Class Checklist

If our concern were performance... we would actually be implementing our
`LinkedList` in C or C++ and providing Python bindings (similar to what NumPy
and Pandas do).

The final (complete) `LinkedList` class can be found (along with a test suite)
in [Module-10-Linked-List/Example-3 in the Example Code
Repository](@gitRepoURL@/tree/main/Module-10-Linked-List/Example-3).
