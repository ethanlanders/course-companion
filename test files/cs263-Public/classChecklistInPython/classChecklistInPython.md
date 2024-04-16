Title: The Python Class Checklist
TOC: yes
Author: Thomas J. Kennedy


# Overview

The class checklist can be though of as a set of emergent properties (or, if
you think as the table as a single entity, an emergent property). Let us start
with a comparison of C++, Java, Python, and Rust. *There is quite a
bit of information in the table. Focus on the Python column.*


| C++                                   | Java                                | Python 3                      | Rust                         |
| :------------------------             | :------------------------------     | :---------------              | :----                        |
| Default Constructor                   | Default Constructor                 | `__init__`                    | `new()` or Default trait     |
| Copy Constructor                      | `clone` and/or Copy Constructor     | `__deepcopy__`                | `Clone` trait                |
| Destructor                            |                                     |                               |                              |
|                                       | `finalize` (deprecated/discouraged) | `__del__`                     | `Drop` trait                 |
| Assignment Operator (=)               |                                     |                               |                              |
| Accessors (Getters)                   | Accessors (Getters)                 | Accessors (`@property`)       | Accessors (Getters)          |
| Mutators (Setters)                    | Mutators (Setters)                  | Setters (`@attribute.setter`) | Mutators (setters)           |
| Swap                                  |                                     |                               |                              |
| Logical Equivalence Operator (==)     | `equals`                            | `__eq__`                      | `std::cmp::PartialEq` trait  |
| Less-Than / Comes-Before Operator (<) | `hashCode`                          | `__hash__`                    | `std::cmp::PartialOrd` trait |
| `std::hash` *(actual hashing)*        | `hashCode`                          | `__hash__`                    | `std::hash::Hash` trait      |
| Stream Insertion Operator (<<)        | `toString`                          | `__str__`                     | `std::fmt::Display` trait    |
|                                       |                                     | `__repr__`                    | `std::fmt::Debug` trait      |
| `begin()` and `end()`                 | `iterator`                          | `__iter__`                    | `iter()` and `iter_mut()`    |

For this discussion... we will focus on the Python column (since our focus is
on learning Python). However, the **Python Class Checklist** emerges out of how
object-oriented code is written (e.g., needing to compare two user-defined
objects).



# Reducing Scope

Let is *extract* the Python column from the table...

| Python 3                      |
| :---------------              |
| `__init__`                    |
| `__deepcopy__`                |
| &nbsp;                        |
| `__del__`                     |
| &nbsp;                        |
| Accessors (`@property`)       |
| Setters (`@attribute.setter`) |
| &nbsp;                        |
| `__eq__`                      |
| `__hash__`                    |
| `__hash__`                    |
| `__str__`                     |
| `__repr__`                    |
| `__iter__`                    |

Let us also remove the empty rows (along with the duplicated `__hash__`)...

| Python 3                      |
| :---------------              |
| `__init__`                    |
| `__deepcopy__`                |
| `__del__`                     |
| Accessors (`@property`)       |
| Setters (`@attribute.setter`) |
| `__eq__`                      |
| `__hash__`                    |
| `__str__`                     |
| `__repr__`                    |
| `__iter__`                    |

That is a bit more manageable... even if it is still as clear as mud.


# Adding Some Clarity

Let us add a brief description column.

| Description                                                               | Python 3                      |
| :----                                                                     | :---------------              |
| Create a "default" or "empty" object                                      | `__init__`                    |
| Create an identical (yet distinct) copy of an object                      | `__deepcopy__`                |
| Define resources that need to be "closed" before deallocation             | `__del__`                     |
| Access a pseudo-private data member                                       | Accessors (`@property`)       |
| Update a pseudo-private data member                                       | Setters (`@attribute.setter`) |
| Compare two objects                                                       | `__eq__`                      |
| Compute a number that can be used to store an object in a `dict` or `set` | `__hash__`                    |
| Generate a human readable string for output                               | `__str__`                     |
| Generate a string for debugging output                                    | `__repr__`                    |
| Allow access to entries in a collection                                   | `__iter__`                    |

The biggest **mistake** one can make is to say... **I must include all of these
in my class.** This is a checklist... every item must be considered based on
the nature of the class to be implemented.

*Note that `__init__` defines how to initialize an object after `__new__` has
actually created the object.* In this course (at least for now)... we will
ignore `__new__`. It is one of those functions that you usually should **not**
define.


# Private, Public, and Dunder

While there is no true private in Python, name mangling through dunder names is
constantly abused to fake it, e.g.,

```python
class Point:
    def __init__():

        self.__x = 0
        self.__y = 0

def main():

    pnt = Point()

    print(pnt.x)
    pnt._Point__x = 1

 
if __name__ == "__main__":
    main()
```

Note that the reason for name mangling is to avoid naming collisions (e.g.,
between base and derived classes, especially when multiple inheritance is
involved).
