Title: The C++ and Java Class Checklists
TOC: yes
Author: Thomas J. Kennedy



# Class Checklist as a Collection of Emergent Properties

The class checklist can be though of as a set of emergent
properties (or, if you think as the table as a single entity, an emergent
property).

Depending on your programming background you will be familiar with C++, Java
(maybe both C++ and Java). Select (based on your background) either the C++ or
Java column. Compare it to the Python column.

| C++                                   | Java                              | Python 3                     | Rust                       |
| :------------------------             | :------------------------------   | :---------------             | :----                      |
| Default Constructor                   | Default Constructor               | `__init__`                   | `new()` or Default trait   |
| Copy Constructor                      | Clone and/or Copy Constructor     | `__deepcopy__`               | Clone trait                |
| Destructor                            |                                   |                              |                            |
|                                       | finalize (deprecated/discouraged) | `__del__`                    | Drop trait                 |
| Assignment Operator (=)               |                                   |                              |                            |
| Accessors (Getters)                   | Accessors (Getters)               | Accessors (`@property`)      | Accessors (Getters)        |
| Mutators (Setters)                    | Mutators (Setters)                | Setters (`@attribute.setter`) | Mutators (setters)         |
| Swap                                  |                                   |                              |                            |
| Logical Equivalence Operator (==)     | equals                            | `__eq__`                     | std::cmp::PartialEq trait  |
| Less-Than / Comes-Before Operator (<) | hashCode                          | `__hash__`                   | std::cmp::PartialOrd trait |
| Stream Insertion Operator (<<)        | toString                          | `__str__`                    | std::fmt::Display trait    |
|                                       |                                   | `__repr__`                   | std::fmt::Debug trait      |
| `begin()` and `end()`                 | `iterator`                        | `__iter__`                   | `iter()` and `iter_mut()`  |

  1. Think about why so many parallels exist between languages that support
     Object Oriented Programming (OOP).

  2. Think about the rule **Every Constructor must intialize every attribute
     (data member).**

  3. Think about [Resource Acquisition is Initialization (RAII) as defined by
     cppreference.com](https://en.cppreference.com/w/cpp/language/raii):

     *Resource Acquisition Is Initialization or RAII, is a C++ programming
     technique[1][2] which binds the life cycle of a resource that must be
     acquired before use (allocated heap memory, thread of execution, open
     socket, open file, locked mutex, disk space, database
     connection—anything that exists in limited supply) to the lifetime of an
     object.*  

    - The Python `with` context management mechanic is an example of RAII.

  3. Think about output in the context of

     - `operator<<` in C++
     - `toString` in Java
     - `__str__` in Python 3
     - `std::fmt::Display::fmt` in Rust


# Focusing on C++ & Java

Let us take our Class Checklist Comparison Table and focus only on C++ and Java.

\bExample{C++ &amp; Java Class Checklist Table}

| C++                                   | Java                              |
| :------------------------             | :------------------------------   |
| **Default Constructor**               | **Default Constructor**           |
| **Copy Constructor**                  | **Clone and/or Copy Constructor** |
| Destructor                            |                                   |
|                                       | finalize (deprecated/discouraged) |
| Assignment Operator (=)               |                                   |
| **Accessors (Getters)**               | **Accessors (Getters)**           |
| **Mutators (Setters)**                | **Mutators (Setters)**            |
| Swap                                  |                                   |
| Logical Equivalence Operator (==)     | equals                            |
| Less-Than / Comes-Before Operator (<) | hashCode                          |
| Stream Insertion Operator (<<)        | toString                          |
|                                       |                                   |
| `begin()` and `end()`                 | `iterator`                        |

\eExample

If we look at the table... four rows (listed in bold) are immediately familiar:

  1. **Default Constructor** - all objects need to be initialized to some
     default state.

  2. **Copy Constructor & `clone`** - it must be possible to copy all objects.

    `clone` allows dynamic binding to be leveraged (which is the standard in
Java).

  3. **Accessors & Mutators** - the principles of encapsulation still apply.

The only difference between C++ and Java for each of these items is syntax. The
mechanics and conceptual approach are the same (barring a few pedantic
differences).

\bExample{C++ &amp; Java Class Checklist Table - The Remainder I}

| C++                                   | Java                              |
| :------------------------             | :------------------------------   |
| Destructor                            |                                   |
|                                       | finalize (deprecated/discouraged) |
| Assignment Operator (=)               |                                   |
| Swap                                  |                                   |
| Logical Equivalence Operator (==)     | equals                            |
| Less-Than / Comes-Before Operator (<) | hashCode                          |
| Stream Insertion Operator (<<)        | toString                          |
|                                       |                                   |
| `begin()` and `end()`                 | `iterator`                        |

\eExample


If we strip out the four bolded rows, we are left with nine (9) rows. Let us
tackle a few...

  1. **Destructor vs `finalize`** - In C++ the destructor guarantees memory
     deallocation (e.g., calls to `delete` or `delete[]`).

     It is also common to shoehorn in some RAII (e.g., closing a file).
     However, `finalize` is not equivalent or analogous to Destructors (in the
     general case).

  2. **Assignment Operator** - Object variables in Python (and Java) behave a
     lot like C++ smart pointers (mostly like `std::shared_ptr`). Python (or
     Java) Garbage collection handles the rest.

  3. **Swap** - In Python (and Java) object variables are functionally fancy
     pointers. A Python (or Java) swap is conceptually a pointer swap.


We are left with...

\bExample{C++ &amp; Java Class Checklist Table - The Remainder II}

| C++                                   | Java                              |
| :------------------------             | :------------------------------   |
| Logical Equivalence Operator (==)     | equals                            |
| Less-Than / Comes-Before Operator (<) | hashCode                          |
| Stream Insertion Operator (<<)        | toString                          |
|                                       |                                   |
| `begin()` and `end()`                 | `iterator`                        |

\eExample

The next two rows are (in my opinion) more interesting:

  1. `operator==` vs `equals` - barring a few mechanical differences these two
     functions are equivalent.

  2. `operator<` and `hashCode` are **not** equivalent. However, they do serve
     similar purposes in each language's built-in libraries.

We are now left with:

  1. `operator<<` vs `toString` - these are both output functions (albeit with
     a few subtle differences).

  2. `begin` and `end` vs `iterator` - iterators are the focus of a separate
     lecture.

