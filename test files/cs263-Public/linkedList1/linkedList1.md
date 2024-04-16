Title: Building a Linked List - Part 1
TOC: yes
Author: Thomas J. Kennedy


# Yep... Linked Lists

You have *almost certainly* worked with Linked Lists in previous coursework. In
C++ they are one of the first places that pointers are used in a meaningful
way. In both C++ and Java, Linked Lists are the cliché *lets build it* examples.

We will use Linked Lists as an opportunity to discuss a few topics, including
dataclasses and Iterators.


# The Node

The Node is the *building block* of any Linked List.

  - `data` will refer to the value being stored
  - `next_node` will refer to the `Node` that contains the next piece of data

```python
class Node:
    def __init__(self, data: Any = None)
        self.data = data
        self.next_node = None
```

Note that the second data is often referred to as `next` or `link` in most
implementations. Unfortunately, `next` is a reserved keyword in Python. The use
of `link` is not, from my perspective, specific enough. 

*Note that... what we are discussing is a Singly Linked List.* In other types
of Linked Lists (e.g., Doubly Linked Lists or Skip Lists) each `Node`
references multiple other `Node`s. The use of `link` in those cases would be
ambiguous (which means we should not encourage its use here).


## Refining the Node

If we return to the `Node` class...

```python
class Node:
    def __init__(self, data: Any = None)
        self.data = data
        self.next_node = None
```

We might be tempted to rewrite it as...

```python
class Node:
    def __init__(self, data: Any = None)
        self.__data = data
        self.__next_node = None

    @property
    def data(self) -> Any:
        return self.__data

    @data.setter
    def data(self, val: Any):
        return self.__data = val

    @property
    def next_node(self) -> Node:
        return self.__next_node

    @next_node.setter
    def next_node(self, val: Node):
        return self.__next_node = val
```

This would allow us to add some validation logic anytime `__next_node` or
`__data` is updated. *Note that the focus with the double underscore (dunder)
naming is to avoid naming collisions. Despite a few Python tutorials... the
double underscore does **not** truly restrict access*.

However, `Node` is an implementation detail. It will actually be defined within
the scope of a larger `LinkedList` class.

```python
class LinkedList:
    class Node:
        def __init__(self, data: Any = None)
            self.__data = data
            self.__next_node = None

        @property
        def data(self) -> Any:
            return self.__data

        @data.setter
        def data(self, val: Any):
            return self.__data = val

        @property
        def next_node(self) -> Node:
            return self.__next_node

        @next_node.setter
        def next_node(self, val: Node):
            return self.__next_node = val
```

## Node as a Data Class

`Node` is an implementation detail. It will not be part of our *public API*
(i.e., client/external code will not create `Node`s nor use them directly).
This is an excellent opportunity for a `dataclass` demonstration.

```python
class LinkedList:
    @dataclass
    class Node:
        data: Any = None
        next_node: Node = None
```

The `@dataclass` decorator will handle generating a `__init__` for us. While a
few other functions are generated... `__repr__` is the only other one that we
care about. We will never need to compare two `Node`s directly.

```python
class LinkedList:
    @dataclass(eq=False)
    class Node:
        data: Any = None
        next_node: Node = None
```

Note that by default `@dataclass` generates...

  - `__init__`
  - `__repr__`
  - `__eq__`

Here... we have disabled the generation of `__eq__` and left [the other settings
(listed in the Python documentation)
alone](https://docs.python.org/3/library/dataclasses.html#module-contents).


# Onward to the Linked List

Now we can start defining the `LinkedList` class. Let us start with a few
placeholder functions. *Note that each of these functions will end with `pass`
which is the syntactic equivalent of empty brackets (`{}`) in C++ or Java.*

```python
class LinkedList:
    @dataclass
    class Node:
        data: Any = None
        next_node: Node = None

    def __init__(self):
        self.head: Node = None
        self.tail: Node = None
        self.length: int = 0
```

Ah... I almost forgot to define what our `LinkedList` uses as data members
(attributes) and write a constructor. This definition includes three data
members:

  - `head` which is the first `Node` in the list
  - `tail` which is the last `Node` in the list
  - `length` which is the number of nodes in the list

When a new `LinkedList` is created... it is empty (i.e., has no data stored in
it). This initial state is defined as

  - `head = None`
  - `tail = None`
  - `length = 0`

Since there is no data... there are no `head` or `tail` nodes (or any nodes).


## Now that the Constructor is Done...

We need to be able to add data to the list...

```python
    def append(self, val: Any) -> None:
        pass
```

The function is named `append` to mirror the naming of the Python `list`.
Next... we need to ensure the size of the list can be retrieved...

```python
    def __len__(self) -> int:
        return self.length
```

Note that `__len__` is a one liner. It is also the dunder function that `len()`
invokes behind the scenes.


## Let us Add Output

Let us add a `__str__` that outputs the value stored in each node, preceded by
a numeric index.

```python
    def __str__(self) -> str:
        """
        Iterate through the LinkedList and print each individual Node
        with an index.
        """
```

*Note that `__str__` does not truly make sense for this class.* However, we
will discuss **why** and **what is appropriate** in a follow-up lecture.


# The Full Interface

Let us collect the entire `LinkedList` class into a single listing.

```python
class LinkedList:
    @dataclass
    class Node:
        data: Any = None
        next_node: Node = None

    def __init__(self):
        self.head: Node = None
        self.tail: Node = None
        self.length: int = 0

    def append(self, val: Any) -> None:
        pass

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        """
        Iterate through the LinkedList and print each individual Node
        with an index.
        """
```

There are quite a few methods missing, e.g.,

  - `extend`
  - `__contains__`
  - `__eq__`

However, we have enough to start implementation. Discussion of the missing
methods will be tabled until a future lecture.


# Implementation

Let us start with `append`. This method is responsible for:

  1. Taking a piece of data
  2. Creating a new `Node`
  3. Adding the new `Node` to the end of the `LinkedList`
  4. Keeping `self.tail` up to date (i.e., always referencing the last node)
  5. Incrementing the `Node` count


```python
    def append(self, val: Any) -> None:
        """
        Add a piece of data (entry) to the end of the list. If the list is
        currently empty, this new entry will be both the first and last entry
        in the list.

        Args:
            val: piece of data to store
        """

        #  If the list is currently empty... this is the first Node
        if not self.head:
            new_node = LinkedList.Node(val)

            self.head = new_node
            self.tail = new_node

            self.length = 1

        else:
            new_node = LinkedList.Node(val)

            # Add the new node after the current tail
            self.tail.next_node = new_node

            # The new node is now the tail
            self.tail = new_node

            self.length += 1
```

We could have used the early return trick...

```python
        #  If the list is currently empty... this is the first Node
        if not self.head:
            new_node = LinkedList.Node(val)

            self.head = new_node
            self.tail = new_node

            self.length = 1
            return

        # General case (every node after the first node)
        new_node = LinkedList.Node(val)

        # Add the new node after the current tail
        self.tail.next_node = new_node

        # The new node is now the tail
        self.tail = new_node

        self.length += 1
```

However, I believe that runs afoul of the [Zen of
Python](doc:perspectivePEP20)...

> *Readability counts.*
>
> and
>
> *If the implementation is hard to explain, it's a bad idea.*

In this instance... the early return actually makes the code less readable.
While an early `return` can be useful... this is a non-value-returning method.
**Let us stick with the first implementation.**


## Let Us Tweak "append"

However, I would like to split the `append` method into three methods:

  - `append` - this will remain the *public* method

  - `__append_first` - this will be called (invoked) when we add the first node

  - `__append_general` - this will be invoked when we add every node after the
    first

While the dunder (double underscore) is oft abused to *pretend* to make
something private...

  1. One underscore indicates that a function is an implementation detail and
     should not (without good reason) be used outside the class.

  2. Two underscores add *name mangling* to the mix. To call `__append_first`
     outside of `LinkedList` one would need to write
     _LinkedList__append_first`. 

```python
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
```

The motivation for this change will become more clear in a follow-up lecture.
For now... just make a mental note.


## And... Output!

Recall that `__str__` does not really make sense for a `LinkedList`. While we
are about to implement a quick `__str__`... the method will be replaced in a
follow-up lecture.

```python
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

There are a few things wrong with the implementation of `__str__`:

  1. String concatenation is used. Python strings are immutable. Every time we
     "add" to the string a new string is created.

  2. There are two iteration variables (`idx` and `it`). We should be using
     `enumerate` along with an actual `Iterator` to make the code more Pythonic.

  3. The output format is debugging specific. Think about all the code in

      - Java that used a `LinkedList` or `ArrayList`

      - C++ that used a `std::vector` or `std::list`

     All output logic was program specific. The data structure never provided a
     *production output* function.

**However, we will explore these issues in a follow-up lecture.**


# The Code So Far...

The current (complete) `LinkedList` class from this example can be found (along
with a test suite) in [Module-10-Linked-List/Example-1 in the Example Code
Repository](@gitRepoURL@/tree/main/Module-10-Linked-List/Example-1).
