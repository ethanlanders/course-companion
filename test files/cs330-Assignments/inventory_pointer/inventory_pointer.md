Title: Item Inventory (Pointers)
Author: Thomas J. Kennedy
TOC: yes

Read these [general instructions on turning in assignments](doc:submitting) for
this course.


# The Story So Far...

This semester we have had two assignments:

  - [Assignment 1 - Linked Lists](doc:inventory_llist)
  - [Assignment 2 - Iterators](doc:inventory_iterator)

In both Assignment 1 and Assignment 2 you worked in the `Inventory` class (mainly
`Inventory.cpp`). This assignment focuses on the `ItemStack` class.


# Why Use More Pointers?

You will be working with raw Item pointers (i.e., `Item*`) within
`ItemStacks`. You are probably asking: *Why do we need a pointer in an
ItemStack?*. In the next assignment you will apply dynamic binding and virtual
functions.

*This assignment is an intermediate step.* We are:

  1. Setting up the codebase to leverage dynamic binding in next assignment.
  2. Addressing a few lingering rough edges throughout the codebase.

There are tweaks throughout the codebase, including

  - `Inventory.h` and `Inventory.cpp`
  - `Item.h` and `Item.cpp`
  - `ItemStack.h` and `ItemStack.cpp`

---

# The Problem

**This assignment deals with the same problem as
[Assignment 2](doc:inventory_iterator).**


## Input

The program reads data from two files, *itemsList-0x.txt* and
*inventoryList-0x.txt*.  File extensions on Linux may be arbitrary--i.e., these
files could have been named with *.dat* as the extensions.

The first file, *itemsList-0x.txt*, lists all possible items.
Each line represents one item in the form *id name*.

\bExample{Sample itemsList-0x.txt}

```
0 Air
1 HP Potion
2 MP Potion
5 Iron Ore
3 Bow Tie
4 Dirt
6 Diamond Ore
7 Iron Ingot
8 Diamond
9 Diamond Block
```

\eExample

The second file, *inventoryList-0x.txt*, lists each individual
inventory--or storage chest--followed by a list of items.

\bExample{Sample inventoryList-0x.txt}

```
# 5
- 1 10
- 2  5
- 3  2
# 6
- 4  3
- 5 27
- 6 44
- 7 55
- 8  1
- 9  4
- 4  3
# 2
- 2  5
- 9  4
- 8  1
- 5  2
- 10 5
```
\eExample

Each line preceded by *#* denotes the start of a new inventory. Each line
preceded by *-* denotes an item. The program creates a new inventory each time
a *#* is encountered.

When a *-* is encountered, a stack of items, ItemStack, is created. The
*ItemStack* is placed in the *Inventory* based on the following rules:

 1. If the Inventory is empty, store the ItemStack, and `return true`.
 2. If the Inventory is not empty, examine the Inventory.
    * If a matching ItemStack is found, merge the two ItemStacks and `return
      true`.
    * If no matching ItemStack is found, store the new ItemStack and `return
      true`.
 3. If the Inventory is full, `return false`.

Through the magic of abstraction, this is not one function, but four (4)
functions in total. Yes, it does seem unnecessary at first. However, each
function does one thing and only one thing. This is an exercise in
understanding the thought process behind abstraction, interfaces, and the
`S`/`O` in `S.O.L.I.D` (with some C++ code) in a multi-ADT program.

Most of your time will be spent on understanding the abstractions (and
interfaces) as opposed to spamming cobblestone blocks... I mean C++ code.


## Output

The output consists of three reports written to standard output,
one after the other.

1. A report listing items that were stored or discarded.

2. A report listing all valid items.

3. Finally, a detailed report is printed. listing data for each inventory:
    * Maximum Capacity--i.e., total slots.
    * Utilized Capacity--i.e., occupied slots
    * Listing of all items.

If the program is run with the provided input files, the following output
should be generated...

\bExample{Sample Output}
```
Processing Log:
 Stored (10) HP Potion
 Stored ( 5) MP Potion
 Stored ( 2) Bow Tie
 Stored ( 3) Dirt
 Stored (27) Iron Ore
 Stored (44) Diamond Ore
 Stored (55) Iron Ingot
 Stored ( 1) Diamond
 Stored ( 4) Diamond Block
 Stored ( 3) Dirt
 Stored ( 5) MP Potion
 Stored ( 4) Diamond Block
 Discarded ( 1) Diamond
 Discarded ( 2) Iron Ore

Item List:
   0 Air
   1 HP Potion
   2 MP Potion
   3 Bow Tie
   4 Dirt
   5 Iron Ore
   6 Diamond Ore
   7 Iron Ingot
   8 Diamond
   9 Diamond Block

Storage Summary:
 -Used 3 of 5 slots
  (10) HP Potion
  ( 5) MP Potion
  ( 2) Bow Tie

 -Used 6 of 6 slots
  ( 6) Dirt
  (27) Iron Ore
  (44) Diamond Ore
  (55) Iron Ingot
  ( 1) Diamond
  ( 4) Diamond Block

 -Used 2 of 2 slots
  ( 5) MP Potion
  ( 4) Diamond Block

```
\eExample



# Your Tasks

One of the most important skills in our craft is interpreting error messages.
Remember the ones you receive when you attempt to compile and run the
unmodified code.

The key abstractions employed in this program are `Item`, `ItemStack`, and
`Inventory`. Complete ADT implementations have been provided for `Item` and
`Inventory`.

A partial implementation has been provided for the `ItemStack`.  Your task is
to finish the update `ItemStack` ADT.

\bSidebar

This assignment is smaller than the previous two (in terms of code and number
of new concepts). Most of your time will be spent reviewing the basics of
pointers.  *Spend the time reviewing.* Practice with pointers. You will need to
use pointers (in one form or another) for the reminder of the semester.

\eSidebar

You must implement the:

  1. Copy Constructor
  2. Destructor
  3. Assignment Operator
    - Note this is already provided and complete. Refer to our discussions of
      the copy-and-swap method.
    - Once you have completed the Copy Constructor, Destructor, and `swap` you
      are done with the Big-3.
  4. Logical Equivalence (i.e., `operator==`).
  5. Less-Than (i.e., `operator<`).
  6. `swap`

*Refer to the comments in each function for additional detail.*

Employ your **Head-to-Head Testing Skills** from CS 250.


# Mechanics

## Running the Program

If the sample data is kept in files itemList-01.txt and
inventoryList-01.txt, then to run this program, do:

```sh
./storage itemList-01.txt inventoryList-01.txt
```

(On a Windows system, you would omit the "./". If you are running from
Code::Blocks or a similar development environment, you may need to
review how to
[supply command-line parameters](https://www.cs.odu.edu/~zeil/cs333/latest/Public/supplyingInputsLab/)
to a running program.)


## Three Main Functions?

As you look through the provided code, you will find three main functions: one
in `storage.cpp` (as expected), one in `TestInventory.cpp`, and one in
`TestItemStack.cpp`. **If you are creating a project in your IDE do not include
both in your project settings**.  You will need to either create multiple
targets in your project settings, or rely on the makefile.

You should probably run the tests on a Linux machine... You can compile the
main program (\emph{storage}) and test drivers (\emph{testInventory} and
\emph{testItemStack}) with

```sh
make
```

\bSidebar

Take note of the semicolon (`;`) after `testInventory`. This is a standard
Linux trick to run two commands back-to-back.

\eSidebar

You can then run `storage` as described [above](#output). You can run the
`Inventory` and `ItemStack` test drivers with:

```sh
./testInventory; ./testItemStack 
```

You may want to run...

```sh
make clean; make; ./testInventory; ./testItemStack 
```

to delete all executables and `.o` files, compile everything from scratch, and
then run all the tests *in one fell swoop.*

If you implemented everything correctly you will see:

> ```
> Inventory:
>   PASSED -> testDefaultConstructor
>   PASSED -> testConstructorSizeN
>   PASSED -> testAddItemStackNoCheck
>   PASSED -> testAddItemWithDuplicateItems
>   PASSED -> testAddItemAfterFull
>   PASSED -> testCopyConstructorForEmpty
>   PASSED -> testCopyConstructor
>   PASSED -> testAssignmentOperator
>   PASSED -> testDisplay
> ItemStack:
>   PASSED -> testDefaultConstructor
>   PASSED -> testSecondConstructor
>   PASSED -> testCopyConstructor
>   PASSED -> testAssignment
>   PASSED -> testAddItems
>   PASSED -> testAddItemsFrom
>   PASSED -> testLogicalEquivalence
>   PASSED -> testLessThan
>   PASSED -> testDisplay
>   PASSED -> testSwap
> 
> ```

If you see _FAILED_ you must revisit revisit the corresponding function(s).
There is a mistake somewhere in your code. **Where should you look? Pay close
attention to the line immediately before *FAILED*... use that as a starting
point.**

**Remember to ask questions if you get stuck.**


## Segmentation Faults & Getting Started

Since `ItemStack`'s `item` data member is a pointer

```cpp
Item* item;
```

segmentation faults are a consideration. If you download, compile and run the
tests, without implementing anything, you will receive test output similar
to:

> ```sh
> Inventory:
>   PASSED -> testDefaultConstructor
>   PASSED -> testConstructorSizeN
> [1]    21524 segmentation fault (core dumped)  ./testInventory
> ItemStack:
> [1]    21526 segmentation fault (core dumped)  ./testItemStack
> ```

**Here is a free hint**. Go to the Copy Constructor and add

```cpp
    this->item = src.item->clone();
```

This line will create a deep copy of `src.item`. Once you have made that
one-line addition, recompile everything and run

```sh
./testInventory; ./testItemStack
```

again. You should see:

> ```
> Inventory:
>   PASSED -> testDefaultConstructor
>   PASSED -> testConstructorSizeN
> FAILURE: testAddItemStackNoCheck:89 -> (*(it++) == stacksToAdd[0])
>   FAILED -> testAddItemStackNoCheck
> FAILURE: testAddItemWithDuplicateItems:126 -> (*(it++) == stacksToAdd[0])
>   FAILED -> testAddItemWithDuplicateItems
> FAILURE: testAddItemAfterFull:172 -> (*(it++) == stacksToAdd[0])
>   FAILED -> testAddItemAfterFull
>   PASSED -> testCopyConstructorForEmpty
> FAILURE: testCopyConstructor:268 -> (aCopy == source)
>   FAILED -> testCopyConstructor
> FAILURE: testAssignmentOperator:305 -> (aCopy == source)
>   FAILED -> testAssignmentOperator
> FAILURE: testDisplay:204 -> (bagString.find(stacksAsStrings[0]) != std::string::npos)
>   FAILED -> testDisplay
> ItemStack:
>   PASSED -> testDefaultConstructor
>   PASSED -> testSecondConstructor
> FAILURE: testCopyConstructor:70 -> (aCopy.size() == 9002)
>   FAILED -> testCopyConstructor
> FAILURE: testAssignment:91 -> (aCopy.size() == 9002)
>   FAILED -> testAssignment
>   PASSED -> testAddItems
>   PASSED -> testAddItemsFrom
> FAILURE: testLogicalEquivalence:142 -> (stack1 == stack2)
>   FAILED -> testLogicalEquivalence
> FAILURE: testLessThan:164 -> (stack3 < stack1)
>   FAILED -> testLessThan
>   PASSED -> testDisplay
> FAILURE: testSwap:198 -> (stack1.getItem().getName() == "Ice")
>   FAILED -> testSwap
> ```

**There is nothing wrong with `Inventory`.** `Inventory` is dependent on
`ItemStack`. Until `ItemStack` is complete you will see failures in
`testInventory`.


# Files

Files for this Assignment appear in [this directory](./Public/) or, if you are
logged in to a CS Dept Linux server, in

```
~tkennedy/Assignments/cs330/inventory_pointer
```


# Grading

Grading for this assignment will be as follows:

* Submitting code that compiles and links properly: 10%
* Submitted ItemStack.cpp passes all tests: 90%


## Test Cases (Unit Tests and System Tests)

The tests are broken into:

  - Test 000 - *(Unit Test)* - Confirm testCopyConstructor *PASSED*
  - Test 001 - *(Unit Test)* - Confirm testAssignment *PASSED*
  - Test 002 - *(Unit Test)* - Confirm testLogicalEquivalence *PASSED*
  - Test 003 - *(Unit Test)* - Confirm testLessThan *PASSED*
  - Test 004 - *(Unit Test)* - Confirm testSwap *PASSED*
  - Test 005 - *(System Test)* - Run the entire program and check the output
    (ignoring formatting and spacing).
  - Test 006 - *(System Test)* - Run the entire program and check the output
    (**including** formatting and spacing).
  - Test 007 - *(Memory Leak Test)* - Run the entire program and check for memory
    leaks. *This confirms your `ItemStack` destructor actually deletes `item`.


# Submitting

Files to Submit:

  - ItemStack.cpp--i.e., your version of the ItemStack ADT Implementation.

Your submitted code must compile correctly--on our Linux servers
(`linux.cs.odu.edu`) with the other code (as provided), using the compilation
commands generated by the provided makefile. Do not alter any of the other
source code files, nor change the Inventory interface in such a way that it can
only be compiled with some other compiler or some other sequence of commands.

To submit your assignment, use the button below. You will receive a preliminary
grade via email (to your ODU email account) and will also be able to check your
grade from the course web page *Grades* button.

\submitButton{@websiteBase@/@sem@/Assts/inventory_pointer/inventory_pointer.ini}


