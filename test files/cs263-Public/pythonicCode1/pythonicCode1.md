Title: Pythonic Code & "Good" Code
TOC: yes
Author: Thomas J. Kennedy


# Python Enhancement Proposals (PEPs)

There are quite a few *"rules"* when writing Pythonic code... starting with two
*Python Enhancement Proposals:*

  - Style - <a href="https://www.python.org/dev/peps/pep-0008/" target="_blank">PEP 8</a>
  - Zen of Python - <a href="https://www.python.org/dev/peps/pep-0020/" target="_blank">PEP 20</a>

While both of these are an interesting read... you do not need to read either
document in its entirety. *I prefer to reserve such reading for Friday nights.
(Sadly, I am not entirely joking.)*


# Community Style Conventions

Many rules come from the Python community...

  1. Always have an `if __name__ == "__main__"`.

    We discussed the mechanics in [the basic program structure
    notes](doc:programStructureBasic). The impact on Python modules and
    `import` statements will be part of future lectures.

  2. Use f-strings over `.format` where possible.

    A lot of this comes down to readability. Consider...

    ```python
    total_cost = sum(prices)
    print("total_cost= {.2f}".format(total_cost))
    ```

    which would output something along the lines of...

    ```
    total_cost=7.53
    ```

    The f-string version would be written as...

    ```python
    total_cost = sum(prices)
    print(f"{total_cost=:.2f}")
    ```

    The f-string variant outputs the same result with less (and more readable)
    code. The formatting sytax will be discussed in upcoming modules.

  3. Use `with` context managers.

    Think about all the times that you opened a file and forgot to close it (or
    a socket). Context managers prevent that problem from occurring (Java has
    incorporated its own version of the mechanic). If you are eager to learn this
    topic in particular... take a peek at [the introduction to context
    managers](doc:contextManagers).

  4. Write pydoc style documentation.

    This deals with documentation of functions and classes... not inline
    comments. The [code documentation lecture](doc:codeDocumentation1) from the
    upcoming *Python Basics I - Variables & Functions* will cover a few
    examples and conventions

  5. Use functions and modules.

    Separate your code into multiple smaller functions that can each be
    evaluated (by a programmer) and tests (by an automated test suite) for
    correctness. *This is related to the no monolithic function rules covered in
    most design discussions.*

  6. Avoid global variables.

    If you need to track state... pass data as explicit arguments into
    functions or make use of an appropriate design pattern (e.g., the Singleton
    pattern).

  7. Do not always use object-oriented design.

    Sometimes procedural style or functional style code can be written more
    quickly, generate more performant code, and result in less boilerplate code.

    **Of course... sometimes mixing paradigms is the best approach.**

  8. Do not forget about the <a href="https://wiki.python.org/moin/GlobalInterpreterLock" target="_blank">Python GIL</a>.


# General (Language Agnostic) Rules

The usual software engineering practices apply in Python (as one might expect).

  1. Follow Test Driven Development (TDD).

    Always have a set of automated tests that can be used to evaluate the
    correctness of your code. A full description of Test Driven Development (TDD)
    can be found in a [future lecture](doc:tdd1)

  2. **Use top down design**, and **do not write monolithic functions.**

    These are the conceptual companion to "**Use functions and modules.**"

  4. Use a code linter or style checker (e.g., pylint or black).

    Always have a tool double check your code style or, in the case of
    <a href="https://black.readthedocs.io/en/stable/" target="_blank">black</a>, fix it for you.

  5. Use self-documenting names.

    If a comment is required to clarify what a variable, function, or class
    represents... a more apt name should be selected.

  6. Remember *S.O.L.I.D.* and *D.R.Y.*

    These are both standard design idioms.

    - **SOLID** breaks down as...

        - **S - Single Responsibility Principle**
  
            Every class, module, or interface has one responsibility (i.e., purpose).
  
        - **O - Open/Closed Principle**
  
            It should be possible to extend a class, module, or function without
            modifying the original code.
  
        - **L - Liskov Substitution**
  
            If I write a function to work with an `class`, or `interface`, any object that
            provides or specializes that `class` or `interface` should work. Think about
  
            - Using `istream` instead of `ifstream` or `std::cin` in C++
            - Using `ostream` instead of `ofstream` or `std::cout` in C++.
            - Replacing `ArrayList<String>` with `List<String>` in the Java.
            - Replacing `.stream()` with `.parallelStream()` in the Java.
            - The Java `Runnable` interface.
            - The Java `Listener` interface.
  
        - **I - Interface Segregation**
  
            Fight the urge to throw in the kitchen sink. Focus on creating problem
            specific interfaces, not monolithic kitchen-sink-interfaces. *This requires
            us to codify how to decompose a large problem (high-level design).*
  
        - **D - Dependency Inversion**
  
            Modules should not directly handle low-level calls and operations. Consider
            the C `FILE*` vs the C++ `ofstream` and `ifstream`.

    - **D.R.Y.** is arguably more memorable. It stands for...

        - **D**o not (or don't)
        - **R**epeat
        - **Y**ourself

  7. Iterators are magic.

    This is an interesting one... However, we will see more of what this means
    when we start writing `for` loops in an upcoming module.
