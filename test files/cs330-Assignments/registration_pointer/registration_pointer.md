Title: Course Registration (Pointer)
Author: Thomas J. Kennedy
TOC: yes

%define <\printTTZ> <ex> {330}

Read these [general instructions on turning in assignments](doc:submitting)
for this course.

# The Story So Far...

This semester we have had two assignments:

  - [Assignment 1 - Linked Lists](doc:registration_llist)
  - [Assignment 2 - Iterators](doc:registration_iterator)

In both Assignment 1 and Assignment 2 you worked in the `Schedule` class (mainly
`Schedule.cpp`). This assignment focuses on the `Student` class.


# Why Use More Pointers?

You will be working with raw Schedule pointers (i.e., `Schedule*`) within
`Student`. You are probably asking: *Why do we need a `Schedule` pointer 
in `Student`?*.

> In the next assignment you will apply dynamic binding and virtual functions.
> While this (third) assignment is the last one based on the *Course
> Registration* problem... the next assignment will require you to work with:
> 
>   1. pointers
>   2. copy constructors
>   3. destructors
>   4. assignment operators

This assignment serves as both a review of pointers (e.g., the dereference
operator) and the Big-3 (i.e., the Copy Constructor, Destructor, and Assignment
Operator).

There are tweaks throughout the codebase, including

  - `Schedule.h` and `Schedule.cpp`
  - `Student.h` and `Student.cpp`


# The Problem

**This assignment deals with the same problem as
[Assignment 2](doc:registration_iterator).**


## Input

The program reads data from two files, _students-0x.txt_ and _requests-0x.txt_.
File extensions on Linux may be arbitrary--i.e., this file could have been
named with _.dat_ as the extension.

The first file, *students-0x.txt*, lists names of students.

\bExample{students-0x.txt}
```
Jon Snow
John Smith
Bob Jones
David Jones
Tommy Oliver
Tom Smith
```
\eExample

You may assume a valid input file--i.e., that no two students share a name. The
second file, *requests-0x.txt*, contains a list of enrollment requests.

\bExample{requests-01.txt}
```
Jon Snow; CS\printTTZ{} 12345 3
Jon Snow; CS\printTTZ{} 12345 3
Jon Snow; CS300 34567 3
John Smith; CS355 45678 3
John Smith; CS\printTTZ{} 12345 3
John Smith; CS\printTTZ{} 23456 3
John Smith; CS300 34567 3
Bob Jones; CS300 34567 3
Bob Jones; CS355 45678 3
Bob Jones; CS\printTTZ{} 12345 3
Bob Jones; CS300 34567 3
Bob Jones; CS361 34569 3
Bob Jones; IT310 78192 3
Bob Jones; Stat330 78195 3
David Jones; CS\printTTZ{} 12345 3
Tom Smith; CS\printTTZ{} 12345 3
Tommy Oliver; CS665 56789 3
```
\eExample

## Output

The output consists of three reports written to standard output,
one after the other.

1. A report listing of all student names.

2. A report listing of all enrollment requests.

3. Finally, a detailed report is printed, listing data for each student:
    * Name
    * Schedule
    * Total Credit hours

If the program is run with the _students-01.txt_ and _requests-01.txt_ as input,
the following output should be generated:

\bExample{Sample Output}
```
Student List
------------------------------------------------------------
 Jon Snow
 John Smith
 Bob Jones
 David Jones
 Tommy Oliver
 Tom Smith

Enrollment Request Log
------------------------------------------------------------
Jon Snow        WAS     enrolled in CS\printTTZ{}
Jon Snow        WAS NOT enrolled in CS\printTTZ{}
Jon Snow        WAS     enrolled in CS300
John Smith      WAS     enrolled in CS355
John Smith      WAS     enrolled in CS\printTTZ{}
John Smith      WAS NOT enrolled in CS\printTTZ{}
John Smith      WAS     enrolled in CS300
Bob Jones       WAS     enrolled in CS300
Bob Jones       WAS     enrolled in CS355
Bob Jones       WAS     enrolled in CS\printTTZ{}
Bob Jones       WAS NOT enrolled in CS300
Bob Jones       WAS     enrolled in CS361
Bob Jones       WAS NOT enrolled in IT310
Bob Jones       WAS NOT enrolled in Stat330
David Jones     WAS     enrolled in CS\printTTZ{}
Tom Smith       WAS     enrolled in CS\printTTZ{}
Tommy Oliver    WAS     enrolled in CS665

Student Schedule Report
------------------------------------------------------------
 Jon Snow
  - 3 credits - CS\printTTZ{} (CRN 12345)
  - 3 credits - CS300 (CRN 34567)
  (6 Total Credits)

 John Smith
  - 3 credits - CS355 (CRN 45678)
  - 3 credits - CS\printTTZ{} (CRN 12345)
  - 3 credits - CS300 (CRN 34567)
  (9 Total Credits)

 Bob Jones
  - 3 credits - CS300 (CRN 34567)
  - 3 credits - CS355 (CRN 45678)
  - 3 credits - CS\printTTZ{} (CRN 12345)
  - 3 credits - CS361 (CRN 34569)
  (12 Total Credits)

 David Jones
  - 3 credits - CS\printTTZ{} (CRN 12345)
  (3 Total Credits)

 Tommy Oliver
  - 3 credits - CS665 (CRN 56789)
  (3 Total Credits)

 Tom Smith
  - 3 credits - CS\printTTZ{} (CRN 12345)
  (3 Total Credits)

```
\eExample

The easiest way to see generate the expected output is to run the sample
executable solution I have provided. The input files and inventory size are
named as command-line parameters.

For example, if the sample data above is kept in students-01.txt and
requests-01.txt, to run this program, type:

```sh
./register students-01.txt requests-01.txt
```

I have provided a second requests file (i.e., _requests-02.txt_). Run the command:

```sh
./register students-01.txt requests-02.txt
```

and examine the results. Compare the results generated by your solution to the
 provided solution (i.e., apply your **head-to-head testing** skills).


# Your Tasks

One of the most important skills in our craft is interpreting error messages.
Remember the ones you receive when you attempt to compile the unmodified code.
**These messages will disappear once you implement the Big-3 (or until you
introduce stub-functions as placeholders).**

The key abstractions employed in this program are *Course*, *Student*, and
*Schedule*. Complete ADT implementations have been provided for `Course` and
`Schedule`.

A partial implementation has been provided for *Student*. Your task is to
finish the Schedule ADT.

\bSidebar

This assignment is smaller than the previous two (in terms of code and number
of new concepts). Most of your time will be spent reviewing the basics of
pointers.

*Spend the time reviewing.* Practice with pointers. You will need to use
pointers (in one form or another) for the reminder of the semester.

\eSidebar

You must implement the:

  1. Second Constructor (i.e., `Student(std::string n)`
  2. Copy Constructor (i.e., `Student(const Student& src)`)
  3. Destructor
  4. Assignment Operator
    - Note this is already provided and complete. Refer to our discussions of
      the copy-and-swap method.
    - Once you have completed the Copy Constructor, Destructor, and `swap` you
      are done with the Big-3.
  5. `swap`
  6. `display`

*Refer to the comments in each function for additional detail.*

Employ your **Head-to-Head Testing Skills** from CS 250.


## Two Main Functions?

As you look through the provided code, you will find two main functions: one in
`register.cpp` (as expected) and one in `TestScheduleAndStudent.cpp`. **If you
are creating a project in your IDE do not include both in your project
settings**.  You will need to either create two targets in your project
settings, or rely on the makefile.

You should probably run the tests on a Linux machine... You can compile the
main program (\emph{register}) and test driver \emph{testScheduleAndStudent}) with

```sh
make
```

You can then run `register` as described [above](#output). You can run the test
driver with:

```sh
./testScheduleAndStudent
```

If you implemented everything correctly you will see:

\bExample{All Tests Pass}
```
Schedule Tests:
  PASSED -> testAppendNoCheck
  PASSED -> testGetCredits
  PASSED -> testWouldExceedCreditLimit
  PASSED -> testAlreadyInSchedule
  PASSED -> testOutputWithOneCourse

Student Tests:
  PASSED -> testDefaultConstructor
  PASSED -> testNameArgConstructor
  PASSED -> testCopyConstructor
  PASSED -> testAssignmentOp
  PASSED -> testSwap
  PASSED -> testDisplay
```
\eExample

If you see _FAILED_ you must revisit revisit the corresponding function(s).
There is a mistake in your code.


# Mechanics


## IDEs and Command Line Arguments

(On a Windows system, you would omit the "./". If you are running from
Code::Blocks or a similar development environment, you may need to
review how to
[supply command-line parameters](https://www.cs.odu.edu/~zeil/cs333/latest/Public/supplyingInputsLab/)
to a running program.) Note that Eclipse provides the option to configure command line arguments.



# Files

Files for this assignment appear in
[this directory](./Public/)
or, if you are logged in to a CS Dept Linux server, in
`~tkennedy/Assignments/cs330/registration_pointer`.



# Grading

Grading for this assignment will be as follows:

* Submitting code that compiles and links properly: 10%
* Submitted Schedule.cpp passes all tests: 90%


## Test Cases (Unit Tests and System Tests)

The tests are broken into:

  - Test 000 - _(Unit Test)_ Confirm testDefaultConstructor _PASSED_
  - Test 001 - _(Unit Test)_ Confirm testNameArgConstructor _PASSED_
  - Test 002 - _(Unit Test)_ Confirm testCopyConstructor _PASSED_
  - Test 003 - _(Unit Test)_ Confirm testAssignmentOp _PASSED_
  - Test 004 - _(Unit Test)_ Confirm testSwap _PASSED_
  - Test 005 - _(Unit Test)_ Confirm testDisplay _PASSED_
  - Test 006 - _(System Test)_ Run the entire program and check the output
    (ignoring formatting and spacing).
  - Test 007 - _(System Test)_ Run the entire program and check the output
    (**including** formatting and spacing).

# Submitting

**You will submit only _Student.cpp_.**

Note that your submitted code must compile correctly--on our Linux Servers
--with the other code in that directory, using the compilation commands
generated by the provided makefile. Do not alter any of the other source code
files, nor change the Scheduler interface in such a way that it can only be
compiled with some other compiler or some other sequence of commands.


To submit your assignment, use the button below. You will receive a preliminary
grade via email (to your ODU email account) and will also be able to check your
grade from the course web page *Grades* button.  This preliminary grade report
will include any compilation errors encountered when compiling your code.


\submitButton{@websiteBase@/@sem@/Assts/registration_pointer/registration_pointer.ini}

