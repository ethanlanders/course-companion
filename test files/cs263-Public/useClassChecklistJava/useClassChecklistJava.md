Title: Using the Java Class Checklist
Author: Thomas J. Kennedy
TOC: yes


This discussion will focus on the Java Class Checklist, specifically in how to
use the Java Class Checklist as a guide to write a *complete* Java Class.


# The Initial Class

Suppose you are working on a team, and one group member (the team smart aleck)
has written a *quick-and-dirty* `Cookbook` class.


```java
/**
 * A collection of Recipes. This class handles all logic
 * for a cookbook--e.g.,
 *   - Adding recipes
 *   - Printing recipes
 */
public class Cookbook {
    private static final int MAX_RECIPES = 100;

    private Recipe[] recipes;

    /**
     * Create a Cookbook that can contain at most MAX_RECIPES
     * recipes
     */
    public Cookbook()
    {
        //...
    }

    /**
     * Create a Cookbook that can contain at most _r_
     * recipes
     */
    public Cookbook(int r)
    {
        //...
    }

    /**
     * Add a Recipe
     *
     * @param toAdd new Recipe
     */
    public void addRecipe(Recipe toAdd)
    {
        //...
    }
}
```

You are responsible for the `Cookbook` class code review. What changes does
`Cookbook` need to be considered complete?

*Before reading the remainder of this document, take a few moments to think about what is missing.*

---

# Initial Observations

We know based on the Cross-Language Class Checklist that `Cookbook` is
incomplete.

^^^[What observations can we make?]

  - Interface completeness
    - Do I need an *Iterator* to access `Recipe`s?
  -   **Big 3?** and `clone`
  - `equals`
  - `hashCode`
  - `toString`

^^^

# Starting with toString

The `toString` method is the most natural function (i.e., it has a clear
purpose). There will always be a need to output a custom object. In C++ this is
handled by `operator<<` paired with `display`. In Java output (more aptly
generating a human readable string) is handled by `toString`


```java
    /**
     * List each Recipe, seperating them with a blank line followed by "---"
     * and a second blank line.
     */
    @Override
    public String toString()
    {
        //...
    }
```

Note the `@Override` decorator. The `toString` method is provided by the Java
`Object` base class (which outputs the memory address of the object). I need to
mark `Cookbook.toString` as overridden.

Normally I would forgo Javadoc documentation for an override function. However,
the documentation must always establish the *rules* of a function. In this
case, I need to know what `toString` will output.


# Tackling equals and hashCode

The Java `equals` function is equivalent to the C++ `operator==`. The two serve
the same purpose (i.e., to check two objects for equivalence).


```Java
    /**
     * Compare two recipes based on the recipes they contain, ignoring the
     * the order of the recipes.
     *
     * @param rhs object against which to compare
     *
     * @return true if both this and rhs are Cookbooks with the same recipes
     */
    @Override
    public boolean equals(Object rhs)
    {
        //...
    }
```

In C++, `operator<` is usually paired with `operator==` based on requirements
of the C++ STL. Java is similar. The `equals` and `hashCode` functions are
all-but-required to be paired together. Both functions must follow the same
rules. In this case, both `equals` and `hashCode` are based purely on the
`Recipe` objects contained in a `Cookbook`.


```Java
    /**
     * Compute the hashcode by adding all recipe hashcodes together.
     *
     * @return integer hashcode
     */
    @Override
    public int hashCode()
    {
        //...
    }
```


# Interface Completeness

The initial `Cookbook` class has an `addRecipe` function. If the class allows
`Recipe`s to be added, removal of `Recipe`s should probably be possible too.


```Java
    /**
     * Remove a Recipe
     *
     * @param toRemove index of Recipe to remove
     */
    public void removeRecipe(int toRemove)
    {
        //...
    }
```


# Big-3 and clone

In Java the C++ Big-3 become a single Java `clone` function. I need to be able
to create a deep copy. Adding clone requires two changes. First, I need to
modify the initial class line:

```java
public class Cookbook
    implements Cloneable
```

The `implements Cloneable` indicates that this class overrides the `clone`
method:

```Java
    /**
     * Create a deep copy.
     */
    @Override
    public Cookbook clone()
    {
        //...
    }
```

This `clone` method takes the place of a Copy Constructor.


# Iterators

A `Cookbook` has multiple `Recipe`s. What design pattern allows us to iterator
over a collection? *The Iterator Pattern.*

Similar to `clone`, we must implement an interface. This time the interface is
templated (with Generics):

```Java
public class Cookbook
    implements Cloneable, Iterable<Recipe>
```

The `Iterable` interface requires that an `iterator` function be provided.

```Java
    /**
     * This depends on implementation decisions (e.g., selected data structure).
     */
    @Override
    public Iterator<Recipe> iterator()
    {
        //...
    }
```

# Putting the Pieces Together

We have discussed the flaws in the *initial Cookbook class*. Putting the code
snippets together is a good opportunity to practice a little Java. I will leave
writing the full, complete, and corrected `Cookbook` class as an exercise to
the reader.




















