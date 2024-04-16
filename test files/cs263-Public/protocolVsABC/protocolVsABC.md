Title: Protocol vs Abstract Base Class
TOC: yes
Author: Thomas J. Kennedy


# A Clear Difference

I spent quite a bit time reading Python
<a href="https://peps.python.org/pep-0544/#generic-protocols" target="_blank">PEP 544</a> after the 
<a href="https://docs.python.org/3/library/typing.html?highlight=protocols#protocols" target="_blank">Typing Module documentation</a>.
Let us take a quick look at the *Rational and Goals* section of PEP 544.

\bExample{PEP 544 - Rational and Goals}

**This passage was retrieved from <https://peps.python.org/pep-0544/#rationale-and-goals>.**

Currently, <a href="https://peps.python.org/pep-0484/" target="_blank">PEP 484</a> and the
`typing` module <a href="https://peps.python.org/pep-0544/#typing" target="_blank">\[typing\]</a> define abstract base
classes for several common Python protocols such as `Iterable` and
`Sized`. The problem with them is that a class has to be explicitly
marked to support them, which is unpythonic and unlike what one would
normally do in idiomatic dynamically typed Python code. For example,
this conforms to <a href="https://peps.python.org/pep-0484/" target="_blank">PEP 484</a>:

```python
from typing import Sized, Iterable, Iterator

class Bucket(Sized, Iterable[int]):
    ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[int]: ...
```

The same problem appears with user-defined ABCs: they must be explicitly
subclassed or registered. This is particularly difficult to do with
library types as the type objects may be hidden deep in the
implementation of the library. Also, extensive use of ABCs might impose
additional runtime costs.

The intention of this PEP is to solve all these problems by allowing
users to write the above code without explicit base classes in the class
definition, allowing `Bucket` to be implicitly considered a subtype of
both `Sized` and `Iterable[int]` by static type checkers using
structural <a href="https://peps.python.org/pep-0544/#wiki-structural" target="_blank">\[wiki-structural\]</a>
subtyping:

```python
from typing import Iterator, Iterable

class Bucket:
    ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[int]: ...

def collect(items: Iterable[int]) -> int: ...
result: int = collect(Bucket())  # Passes type check
```

Note that ABCs in `typing` module already provide structural behavior at
runtime, `isinstance(Bucket(), Iterable)` returns `True`. The main goal
of this proposal is to support such behavior statically. The same
functionality will be provided for user-defined protocols, as specified
below. The above code with a protocol class matches common Python
conventions much better. It is also automatically extensible and works
with additional, unrelated classes that happen to implement the required
protocol.

\eExample

Now for the important question... *How would we explain this passage in casual
conversation?* Well... let us find out!


# What Do We Know?

We know that given a base class (e.g., `Shape`) that any derived class (e.g.,
`Rectangle`) must explicitly inherit from the base class. Consider... the
following `Shape` class.

```python
from typing import Protocol


class Shape(Protocol):
    """
    Shape in a 2-D Cartesian Plane
    """

    def name(self) -> str:
        raise NotImplementedError()

    def area(self) -> float:
        raise NotImplementedError()

    def perimeter(self) -> float:
        raise NotImplementedError()
```

Take note of the three methods:

  - `name` - which requires a class to return the name of the .
  - `area` - which  requires a class to implement an area computation.
  - `perimeter` - which  requires a class to implement a perimeter computation.

A `Rectangle` class could be written as...

```python
@dataclass
class Rectangle:
    length: float = 1
    width: float = 1

    def name(self) -> str:
        return "Rectangle"

    def area(self) -> float:
        return self.length * self.height

    def perimeter(self) -> float:
        return 2 * (self.length + self.height)
```

Okay... What is the difference? The first line of the `Rectangle` class differs:

```python
class Rectangle(Shape):
```

versus

```python
class Rectangle:
```

We no longer need to explicitly mark `Rectangle` as inheriting from `Shape`.


# What is the Benefit?

We can write code along the lines of...


```python
def get_largest_area_by_shape_name(shapes: list[Shape]) -> tuple[str, float]:
    """
    Given a list of shapes:

      1. Identify a set of shape names
      2. find the largest area for each name
    """

    pass
```

The function does not need to know about the specific classes involved, just
that those classes provide `name` and `area`.


# That Sounds Like an Abstract Base Class

That is an accurate assessment. However, a Protocol can be defined independent
of the class definitions (e.g., you could define a `Protocol` and have it apply
to classes written as part of a separate module or library.

Alex Martelli (Fellow of the Python Software Foundation) summarizes the notion
in a [post on Google
Groups.](https://groups.google.com/g/comp.lang.python/c/CCs2oJdyuzc/m/NYjla5HKMOIJ)

> In other words, don't check whether it IS-a duck: check whether it
> QUACKS-like-a duck, WALKS-like-a duck, etc, etc, depending on exactly what
> subset of duck-like behaviour you need to play your language-games with. If the
> argument fails this specific-ducklyhood-subset-test, then you can shrug, ask
> "why a duck?" (at least, you can if you're a Marx Brothers fan and have
> memorized "Cocoanuts"' script; Monty Python one-true-wayists will have to find
> their own simile here), and move on to the next set of tests (why-a-no- chicken
> immediately comes to mind, but then one would have to ask why it crosses the
> road, so I think we'd better snip it).
> 
> ...
> 
> Besides, "explicit is better than implicit", goes one of Python's mantras. Just
> let the client-code explicitly TELL you which kind of argument they are passing
> you (and doing so through a named argument is simple and readable), and your
> work drops to zero, while removing no useful functionality whatever from the
> client.  As a little vig, you also avoid trouble in case what the client wants
> to pass is some tricky object that behaves EITHER as a file connection OR as a
> db connection (etc, etc) -- not all that likely, but, who knows.

This gets us closer to **Interface Segregation (the 'I' in SOLID)**. It is
much better to define the specific type of behavior we want instead of for a
thing.

