Title: Using the C++ Class Checklist
Author: Thomas J. Kennedy
TOC: yes


This discussion will focus on the C++ Class Checklist, specifically in how to
use the C++ Class Checklist as a guide to write a *complete* C++ Class.


# The Initial Class

A smart aleck claims that following class is complete:

```cpp
/**
 * A collection of Recipes. This class handles all logic
 * for a cookbook--e.g.,
 *   - Adding recipes
 *   - Printing recipes
 */
class Cookbook {
    private:
        static const int MAX_RECIPES;

        Recipe* recipes;

    public:
        typedef Recipe* iterator;
        typedef const Recipe* const_iterator;

        /**
         * Create a Cookbook that can contain at most MAX_RECIPES
         * recipes
         */
        Cookbook();

        /**
         * Create a Cookbook that can contain at most _r_
         * recipes
         */
        Cookbook(int r);

        /**
         * Add a Recipe
         *
         * @param to_add new Recipe
         */
        void addRecipe(Recipe &to_add);
};
```

You are responsible for the `Cookbook` class code review. What changes does
`Cookbook` need to be considered complete?

*Before reading the remainder of this document, take a few moments to think
about what is missing.*

---

# Initial Observations

We know based on the C++ Class Checklist that `Cookbook` is incomplete.

Is this class **complete**?

^^^[What observations can we make?]

  - Interface completeness
  - Const Correctness
  - Big 3
  - Logical Operators
  - Stream Insertion Operator
  - Style
    - Prefer type aliases over typedefs
    - Missing `@param`s in Doxygen documentation
    - Missing `@return`s in Doxygen documentation
    - Missing `@pre`s in Doxygen documentation
    - Missing `@post`s in Doxygen documentation

^^^


## Documentation

In larger programs proper and complete documentation is important. This is an
ideal time to force ourselves into the habit of properly documenting code. I
will use a *Javadoc / Doxygen* style for C++. Other languages have their own
conventions (e.g., Pydoc in Python, Rustdoc in Rust, and Javadoc in Java).

We will address the missing documentation [in
situ](https://www.merriam-webster.com/dictionary/in%20situ) as we discuss each
function.


## Typedefs vs Aliases

Let us start by replacing the two
<a href="https://en.cppreference.com/w/cpp/language/typedef" target="_blank">typedefs</a>

```cpp
    public:
        typedef Recipe* iterator;
        typedef const Recipe* const_iterator;
```

with <a href="https://en.cppreference.com/w/cpp/language/type_alias" target="_blank">type aliases</a>

```cpp
    public:
        using iterator       = Recipe*;
        using const_iterator = const Recipe*;
```


# Starting with display and Output

The `operator<<` method is the most natural function (i.e., it has a clear
purpose). There will always be a need to output a custom object. In C++ this is
handled by `operator<<`, which we usually pair with `display`.

The `operator<<(std::ostream& outs, const Cookbook& toPrint`) function can not
be written as a member function. It must either be written as a `friend` function
or an external function. Let us only use `friend` functions when
absolutely necessary.

We will start with the `display ` member function.

```cpp
        /**
         * Display the Cookbook with each recipe separated by `\n---\n`.
         *
         * @param outs output destination (e.g., cout or a file)
         */
        void display(std::ostream& outs) const;
```

The stream insertion operator (informally called the output operator) is little
more than an `inline`d wrapper function.

```cpp
inline
std::ostream& operator<<(std::ostream& outs, const Cookbook& prt)
{
    prt.display(outs);
    return outs;
}
```

We can forgo documentation on this function. Its arguments, return type, and
name all follow standard C++ convention and practice.


# Tackling operator== and operator<

The C++ `operator==` compares two objects for equivalence.


```Java
    /**
     * Compare two cookbooks based on the recipes they contain, ignoring the
     * the order of the recipes.
     *
     * @param rhs object against which to compare
     *
     * @return true if both this and rhs are Cookbooks with the same recipes
     */
     bool operator==(const Cookbook& rhs) const;
```

In C++, `operator<` is usually paired with `operator==` based on requirements
of the C++ STL. Both functions must follow the same
rules. In this case, both `operator==` and `operator<` are based purely on the
`Recipe` objects contained in a `Cookbook`.

```cpp
    /**
     * Less than (comes-before) Operator
     *
     * Compare two cookbooks based on the recipes they contain, ignoring the
     * the order of the recipes.
     *
     *  - If lhs has fewer recipes than rhs, lhs < rhs.
     *  - If lhs and rhs have the same number of recipes, sort each set of
     *    recipes then compare each pair of recipes, basing lhs < rhs on the
     *    first set of non-equal recipes.
     *
     * @param rhs Cookbook against which to compare
     *
     * @return true if both `this` should be listed before `rhs`
     */
    bool operator<(const Cookbook& rhs) const;

```

The documentation is more verbose than I would like. However, it captures the
rules for comparison explicitly (i.e., there is no ambiguity in how the
comparison must be performed). Verbosity can be addressed in a later revision.


## Const Correctness

Let us take another look at `operator==` and `operator<`.

```cpp
    bool operator==(const Cookbook& rhs) const;

    bool operator<(const Cookbook& rhs) const;
```

Take note of how `const` appears twice in each method. The first `const`

```cpp
const Cookbook& rhs
```

applies to the argument. The `rhs` (right-hand side) is passed by *constant
reference*. This gives us direct read-only access to the `rhs` cookbook. The use
of `const` guarantees that `rhs` will no be changed during either comparison.

The second `const` (at the end of each function) serves a similar purpose. It
(i.e., `) const;`) guarantees that `this` Cookbook remains unchanged.

Can you imagine writing

```cpp

    Cookbook simple;
    Cookbook notSimple;

    // Do some stuff
    // ...

    cout << simple << "\n";

    if (simple == notSimple) {
        cout << "simple and notSimple are the same" << "\n";
    }

    cout << simple << "\n";
```

and getting different output for `simple` the second time?

## rel_ops and The Spaceship Operator

Notice how we did not write functions for `<=`, `>`, `>=`, or `!=`? The compiler
will take `operator==` and `operator<` and build the them for us, if we add

```C++
using std::rel_ops;
```

C++20 plans to deprecate this with the spaceship operator, `operator<=>`.
However, the spaceship operator (three-way comparison operator) requires its own
(separate) discussion, in a future lecture.


# Interface Completeness

The initial `Cookbook` class has an `addRecipe` function. If the class allows
`Recipe`s to be added, removal of `Recipe`s should probably be possible too.


```cpp
    /**
     * Remove a Recipe.
     *
     * @param to_remove recipe to remove from the cookbook
     *
     * @pre `to_remove` is present in the cookbook. If `to_remove` is not
     *  part of this cookbook, this method becomes a no-op (it completes
     *  silently after performing no removal).
     */
    void removeRecipe(const Recipe& to_remove);
```

This method can probably be written more elegantly with iterators. However, I
will leave that approach as an exercise to the reader.


# Iterators

A `Cookbook` has multiple `Recipe`s. What design pattern allows us to iterator
over a collection? *The Iterator Pattern.*

We already have the iterators:

```cpp
    public:
        using iterator       = Recipe*;
        using const_iterator = const Recipe*;
```

We need to add `begin` and `end` functions. We need one set for the *read-write*
iterator (i.e., `iterator`) and one set for the *read-only* iterator (i.e.,
`const_iterator`).

```cpp
        /**
         * First Recipe
         */
        iterator begin();

        /**
         * End of Recipe Collection
         */
        iterator end();

        /**
         * First Recipe
         */
        const_iterator begin() const;

        /**
         * End of Recipe Collection
         */
        const_iterator end() const;
```

We could forgo documentation for these four functions. However, it is always
a good idea to document over what we are iterating (e.g., `Recipe` objects).


# Big-3 & Deep Copies

Unless explicitly not required, we need to guarantee that deep copies are
performed. We want to copy the data referenced by pointers (deep copy). We do
not want to copy the pointers themselves (shallow copy).

We also need to guarantee memory cleanup (i.e., memory deallocation). If we call
`new`, or `calloc`, or `malloc`, we need to corresponding calls to `delete` or
`free` are called.

That leads us to the copy constructor and, the familiar, destructor.

```cpp
    /**
     * Copy Constructor.
     *
     * @param src Cookbook to copy
     */
    Cookbook(const Cookbook& src);

    /**
     * Destructor
     */
    ~Cookbook();
```

The Copy Constructor handles pass-by-value (a.k.a pass-by-copy). We need to
handle assignment, e.g.,

```cpp
    Cookbook simpleCookbook;
    Cookbook aCopy;

    // Do stuff
    // ...

    aCopy = simpleCookbook;
```

This is handled by the assignment operator.

```cpp
    /**
     * Assignment Operator
     */
    Cookbook& operator=(const Cookbook& rhs);
```

This is often naively implemented by copying-and-pasting code.

```cpp
Cookbook& Cookbook::operator=(const Cookbook& rhs)
{
    if (*this != &rhs) {
        // Copy-and-paste destructor logic
        // ...

        // Copy-and-paste copy constructor logic
    }

    return *this;
}
```

## The Copy-and-Swap Idiom

The *Copy-and-Swap Idiom* addressed the D.R.Y (Don't Repeat Yourself) principle.
First, we need to change from pass-by-reference

```cpp
    /**
     * Assignment Operator
     */
    Cookbook& operator=(const Cookbook& rhs);
```

to pass-by-copy

```cpp
    /**
     * Assignment Operator
     */
    Cookbook& operator=(Cookbook rhs);
```

The change to pass-by-value forces an implicit call to the Copy Constructor.
After adding a quick swap function (which we will implement as a `friend`
function)...

```cpp
    friend
    void swap(Cookbook& lhs, Cookbook& rhs);
```

we can finish the revising `operator=`.

```cpp
Cookbook& Cookbook::operator=(Cookbook rhs)
{
    swap(*this, rhs);

    return *this;
}
```

The calls to the Copy Constructor (when creating `rhs`) and the destructor
(after the swap) now happen implicitly. We also get a swap function out of it!


# Putting the Pieces Together

^^^[Corrected Cookbook]

```cpp
using std::rel_ops;

class Cookbook {
    private:
        static const int MAX_RECIPES;

        Recipe* recipes;

    public:
        using iterator       = Recipe*;
        using const_iterator = const Recipe*;

        /**
         * Create a Cookbook that can contain at most MAX_RECIPES
         * recipes.
         */
        Cookbook();

        /**
         * Create a Cookbook that can contain at most _r_
         * recipes.
         */
        Cookbook(int r);

        /**
         * Copy Constructor.
         *
         * @param src Cookbook to copy
         */
        Cookbook(const Cookbook& src);

        /**
         * Destructor.
         */
        ~Cookbook();

        /**
         * Add a Recipe.
         *
         * @param to_add new Recipe
         */
        void addRecipe(const Recipe& to_add);

        /**
         * Remove a Recipe.
         *
         * @param to_remove recipe to remove from the cookbook
         *
         * @pre `to_remove` is present in the cookbook. If `to_remove` is not
         *  part of this cookbook, this method becomes a no-op (it completes
         *  silently after performing no removal).
         */
        void removeRecipe(const Recipe& to_remove);

        /**
         * Assignment Operator
         */
        Cookbook& operator=(Cookbook rhs);

        /**
         * Compare two cookbooks based on the recipes they contain, ignoring the
         * the order of the recipes.
         *
         * @param rhs Cookbook against which to compare
         *
         * @return true if both this and rhs are Cookbooks with the same recipes
         */
        bool operator==(const Cookbook& rhs) const;

        /**
         * Less than (comes-before) Operator
         *
         * Compare two cookbooks based on the recipes they contain, ignoring the
         * the order of the recipes.
         *
         *  - If lhs has fewer recipes than rhs, lhs < rhs.
         *  - If lhs and rhs have the same number of recipes, sort each set of
         *    recipes then compare each pair of recipes, basing lhs < rhs on the
         *    first set of non-equal recipes.
         *
         * @param rhs Cookbook against which to compare
         *
         * @return true if both `this` should be listed before `rhs`
         */
        bool operator<(const Cookbook& rhs) const;

        /**
         * First Recipe.
         */
        iterator begin();

        /**
         * End of Recipe Collection
         */
        iterator end();

        /**
         * First Recipe.
         */
        const_iterator begin() const;

        /**
         * End of Recipe Collection.
         */
        const_iterator end() const;

        /**
         * Display the Cookbook with each recipe separator by `\n---\n`.
         *
         * @param outs output destination (e.g., cout or a file)
         */
        void display(std::ostream& outs) const;

        /**
         * Swap two Cookbooks.
         *
         * @param lhs first cookbook
         * @param rhs second cookbook
         */
        friend
        void swap(Cookbook& lhs, Cookbook& rhs);
};

inline
std::ostream& operator<<(std::ostream& outs, const Cookbook& prt)
{
    prt.display(outs);
    return outs;
}
```

^^^

# Modern C++ (i.e., C++20 & Move Semantics)

C++20 adds [the spaceship (three-way comparison)
operator](https://en.cppreference.com/w/cpp/language/operator_comparison#Three-way_comparison),
[default
comparisons](https://en.cppreference.com/w/cpp/language/default_comparisons),
and quite a few other mechanics. **For now we want to focus on the basics**. We
will revisit these additions in a later lecture.

Move semantics center around *lvalues* and *rvalues*. It is extremely useful to
understand these two concepts. However, they are beyond the scope of this
discussion.

## Big-5

Move semantics turn the Big-3 into the Big-5. The whole notion of move semantics
centers around transient (i.e., temporary) copies.

The Big-3 (and `swap`) from our checklist...

\bExample{Big-3 and Swap}
```C++
        /**
         * Copy Constructor.
         *
         * @param src Cookbook to copy
         */
        Cookbook(const Cookbook& src);

        /**
         * Destructor.
         */
        ~Cookbook();

        /**
         * Assignment Operator
         */
        Cookbook& operator=(const Cookbook& rhs);

        /**
         * Swap two Cookbooks.
         *
         * @param lhs first cookbook
         * @param rhs second cookbook
         */
        friend
        void swap(Cookbook& lhs, Cookbook& rhs);
```
\eExample

would become the Big-5 (and swap).

\bExample{Big-5 and Swap}
```C++
        /**
         * Copy Constructor.
         *
         * @param src Cookbook to copy
         */
        Cookbook(const Cookbook& src);

        /**
         * Move Copy Constructor.
         *
         * @param src Cookbook to copy
         */
        Cookbook(Cookbook&& src);

        /**
         * Destructor.
         */
        ~Cookbook();

        /**
         * Assignment Operator
         */
        Cookbook& operator=(const Cookbook& rhs);

        /**
         * Move Assignment Operator
         */
        Cookbook& operator=(Cookbook&& rhs);

        /**
         * Swap two Cookbooks.
         *
         * @param lhs first cookbook
         * @param rhs second cookbook
         */
        friend
        void swap(Cookbook& lhs, Cookbook& rhs);
```
\eExample

**The implementation, which requires a discussion of move semantics and
rvalues, is technically outside the scope of this lecture.** The remainder of
this section (i.e., **The Big-5**) is optional reading,

The rules of the Big-3 still apply. The *Copy Constructor* and *Copy Assignment
Operator* guarantee deep copies. However, there are a few cases, where we know
an object is a transient copy (i.e., immediately after we copy it, it will be
deleted anyway). Instead of wasting a copy, move semantics allow data to be
stolen.

Consider the `Book` example class. We know that `std::string` uses dynamic memory
interally (as do IngredientList and InstructionList). Instead of copying data
in cases where the original will be deleted, we are going to move (i.e.,
*steal*) the data.

```cpp
Book::Book(Book&& src)                                                                                                  
    :title(std::move(src.title)),                                                                                          
     ingredients(std::move(src.ingredients)),                                                                              
     instructions(std::move(src.ingredients)                                                                                
{                                                                                                                          
}                                                                                                                          
```
                                                                                                                           
`std::move` does what its name suggests, it moves data. Think of it as copying
pointers to the new Book, then setting the internal pointers in `src` (e.g., in
`src.title`) to `nullptr`.
                                                                                                                         
This guarantees that:                                                                                                        

  - `src` still exists                                                                                                        
  - all `src` data is in a valid "zero state"                                                                                  
  - when `src`'s destructor is called it has no data to delete
  - all data has been relocated to the new `Book`

We still end up with two objects.


## The Big-0

There is an alternative to the Big-3 and Big-5, called the Big-0. The Big-0 will
be covered in a future lecture.


---

# Practice the Process (A Second Example)

The same smart aleck presents the following `Recipe` class:

```cpp
typedef std::vector<Ingredient> IngredientList;
typedef std::vector<std::string> InstructionList;

/**
 * This class contains all information pertaining to a Recipe
 */
class Recipe {
    private:
        std::string     title;
        IngredientList  ingredients;
        InstructionList instructions;

    public:

        /**
         * Create an empty Recipe--I can cook this.
         */
        Recipe();

        /**
         * Create a Recipe with a title
         */
        Recipe(std::string title);

        /**
         * Add Ingredients
         */
        void addIngredients(IngredientList add);

        /**
         * Add Instructions
         */
        void addInstructions(InstructionList add);

        /**
         * Retrieve the title
         */
        std::string getTitle();

        /**
         * Change the title
         */
        void setTitle(std::string title);
};
```

Practice the code review process we followed for the previous `Cookbook` class.

^^^[What observations can we make?]

  - Interface completeness
  - Const Correctness
  - Big 3
  - Logical Operators
  - Stream Insertion Operator

^^^

---

^^^[Corrected Recipe]

```cpp
using std::rel_ops;

// Let us switch to type aliases
using IngredientList  = std::vector<Ingredient>;
using InstructionList = std::vector<std::string>;

class Recipe {
    private:
        std::string     title;
        IngredientList  ingredients;
        InstructionList instructions;

    public:
        /**
         * Create an empty Recipe--I can cook this.
         */
        Recipe();

        /**
         * Create a Recipe with a title
         */
        Recipe(std::string title);

        /**
         * Copy Constructor
         */
        Recipe(const Recipe& src);

        /**
         * Destructor
         */
        ~Recipe();

        /**
         * Add Ingredients
         */
        void addIngredients(const IngredientList& add);

        /**
         * Add Instructions
         */
        void addInstructions(const InstructionList& add);

        /**
         * Retrieve the title
         */
        std::string getTitle() const;

        /**
         * Change the title
         */
        void setTitle(std::string title);

        /**
         * Retrieve a copy of the Ingredient list
         */
        IngredientList getIngredients() const;

        /**
         * Retrieve a copy of the Instruction list
         */
        InstructionList getInstructions() const;

        /**
         * Assignment Operator
         */
        Recipe& operator=(const Recipe& rhs);

        /**
         * Logical Equivalence Operator
         */
        bool operator==(const Recipe& rhs) const;

        /**
         * Less than (comes-before) Operator
         */
        bool operator<(const Recipe& rhs) const;
};

std::ostream& operator<<(std::ostream& outs, const Recipe& prt);
```

^^^
