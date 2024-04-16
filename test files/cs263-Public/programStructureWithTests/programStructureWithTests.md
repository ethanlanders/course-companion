Title: Structure of a Python Program with Tests
TOC: yes
Author: Thomas J. Kennedy


# Managing Expectations

The purpose of this lecture is to describe the structure of a codebase with
tests written using either the builtin Python [`unittest`
module](https://docs.python.org/3/library/unittest.html) or [the separate
PyTest](https://docs.pytest.org/) framework.

The types of tests, how to write tests (mechanically), and how to write tests
(conceptually) are covered in future modules (across multiple lectures).

**Before we discuss program structure... let us introduce unit tests,
integration tests and the TDD process.**


# What Types of Tests Can Be Expected?

*As a quick note... I am a strong proponent of discussing the Rust programming
language. While this is not a course in Rust... there are quite a few insights
to be gained through carefully curated referenced and snippets.*

The *Rust Programming Language* has two of (what I consider) to be the best
definitions regarding unit and integration tests.

\bExample{Unit Test Definition}

The purpose of unit tests is to test each unit of code in isolation from the
rest of the code to quickly pinpoint where code is and isn’t working as
expected.

*Retrieved from [The Rust Programming Language - Chapter
11](https://doc.rust-lang.org/book/ch11-03-test-organization.html)*

\eExample

\bExample{Integration Test Definition}

[Integration tests] use your library in the same way any other code would,
which means they can only call functions that are part of your library’s public
API. Their purpose is to test whether many parts of your library work together
correctly. Units of code that work correctly on their own could have problems
when integrated, so test coverage of the integrated code is important as well.

*Retrieved from [The Rust Programming Language - Chapter
11](https://doc.rust-lang.org/book/ch11-03-test-organization.html)*

\eExample

You can expect to see unit tests and integration tests throughout the course.
We will discuss how to write both types of tests in a future module. Writing
tests will include discussion of <a href="https://hamcrest.org/" target="_blank">Hamcrest Matchers</a>


# What is Test Driven Development?

Test Driven Development (TDD) is a workflow where tests drive development.
*Yes... I just defined TDD using the words "test," "drive," and "development."*
Let us try again... TDD can be described as a sequence of steps:

  1. Define the interface for a function or class. *Write the specification,
     not code.*

  2. Write the test code for the interfaces and specifications outlined in the
     previous step.

  3. Start implementing the code (i.e., writing the function and class logic).

  4. Run the test code after implementing a piece of code. *This does not need
     to be, nor should it be, an entire set of functions or an entire class.*

  5. If the tests for the selected code... 

     1. **Pass...** return to "step 3" and write the next piece of implementation
        code.

     2. **Fail...** revisit the *implementation*. Locate and correct any
        mistake(s) and re-run the tests. If the tests continue to fail, double
        check the test code for mistakes. **Repeat this step until the tests 
        pass.**


**Why did we just discuss TDD?** While TDD and testing is covered in a future
module... we are actually starting on "step 3" for most assignments and labs.


# Where Will the Tests Be Located?

The tests will be located in a `tests` subdirectory, e.g.,

\bExample{Python Program with Tests}
```
├── linkedlist.py
├── list_driver.py
└── tests
    └── test_linked_list.py
```
\eExample

Do not worry... linked lists in Python are a few modules away (and far less
tedious in Python than in C++ or Java)
