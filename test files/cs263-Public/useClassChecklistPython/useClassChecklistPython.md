Title: Using the Python Class Checklist
TOC: yes
Author: Thomas J. Kennedy


This discussion will focus on the Python Class Checklist, specifically in how to
use the Python Class Checklist as a guide to write a *complete* Python Class.


# The Initial Class

Suppose you are working on a team, and one group member (the team smart aleck)
has written a *quick-and-dirty* `Cookbook` class.


```python
class Cookbook:
    """
    A collection of Recipes. This class handles all logic
    for a cookbook--e.g.,
      - Adding recipes
      - Printing recipes
    """

    MAX_RECIPES = 100;

    def __init__(self):
        self.recipes = []

    def add_recipe(self, to_add):
        pass
```

You are responsible for the `Cookbook` class code review. What changes does
`Cookbook` need to be considered complete?

*Before reading the remainder of this document, take a few moments to think about what is missing.*


# Initial Observations

We know based on the Cross-Language Class Checklist that `Cookbook` is
incomplete.

^^^[What observations can we make?]

  - Interface completeness, e.g.,
    - Do I need an *Iterator* to access `Recipe`s?
  - Missing...
    - `__deepcopy__`
    - `__eq__`
    - `__hash__`
    - `__str__`

^^^

# Starting with "dunder str"


The `__str__` (dunder str) method is the most natural function (i.e., it has a clear
purpose). There will always be a need to output a custom object. 

```python
    def __str__(self) -> str:
        """ 
        List each Recipe, seperating them with a blank line followed by "---"
        and a second blank line.
        """
        pass
```


I often forgo pydoc documentation for a *dunder* function. However,
the documentation must always establish the *rules* of a function. In this
case, I need to know what `__str__` will output.


# Tackling "dunder equals" and "dunder hashcode"


The `__eq__` method defines how to take two objects and compare them for
equivalence. Similar to Java (but different from C++) the `rhs` argument can be
any type. It is not restricted to a `Cookbook`.

\bExample{Implementation Note}

The first step in implementing the `__eq__` method is usually an *instance of*
check. In the case of `Cookbook` it does not make sense to compare `self` (a
`Cookbook`) to `rhs` if `rhs` is not a Cookbook.

```python
    if not isinstance(rhs, Cookbook):
        return False
```

\eExample


```python
    def __eq__(self, rhs: Any) -> bool:
        """ 
        Compare two cookbooks based on the recipes they contain, ignoring the
        the order of the recipes.
       
        Returns: 
            True if both this and rhs are Cookbooks with the same recipes and
            False otherwise
        """

        return False
```

The `__eq__` and `__hash__` functions are all-but-required to be paired
together. Both functions must follow the same rules. In this case, both
`__eq__` and `__hash__` are based purely on the `Recipe` objects contained in a
`Cookbook.


```python
    def __hash__(self) -> int:
        """
        Compute the hashcode by combining all recipe hashcodes together.
        """

        return 0
```


# Interface Completeness

The initial `Cookbook` class has an `addRecipe` function. If the class allows
`Recipe`s to be added, removal of `Recipe`s should probably be possible too.


```python
    def add_recipe(self, to_add: Recipe):
        """
        Add a Recipe to the Cookbook.

        Args:
            to_add recipe to store

        Raises:
            CookbookFull (to be implemented) error if adding this recipe would
            reuslt in more than MAX_RECIPES stored in this Cookbook
        """ 

        pass

    def remove_recipe(self, to_remove: Recipe):
        """
        Remove a Recipe.

        Args:
            to_remove Recipe to remove

        Raises:
            KeyError if no matching Recipe is found in the Cookbook
        """

        pass
```

For most classes that store a collection of objects... I would recommend
something similar to renaming...

  - `add_recipe` to `append`
  - `remove_recipe` to `remove`

However, I am not sure in this case. Unlike a `list` or `set`... a `Cookbook`
is more than just a collection/container. *Let us stick with the original names
(for now).*


# Iterators

We need to be able to access each recipe. Condsider how most programs will end
up outputting each `Recipe` or updating a `Recipe`.

```python
    def __iter__(self) -> Iterator[Recipe]:
        return iter(recipes)
```

Note that we will end up storing `Recipe`s is a `list` or similar container.
The `iter` function allows us to retrieve that collection's iterator and use it
as if it were our own.


# Making a Copy

Copies in Python can be tricky. If we were storing literals or immutable types (e.g., `int`, `float`, or `str`) we could (in quite a few cases) forgo implementing a `__deepcopy__` for a class. However, we are storing `Recipe` objects (which will likely be mutable). We need to guarantee that if a `Cookbook` is copied that the copy contains identical and **independent** copies of all `Recipe` objects.

*Note that the `memo` argument is required. It is used for cases where an entry (object) might be encountered multiple times during a copy operation.*


```python
    def __deepcopy__(self, memo) -> Cookbook:
        cpy = Cookbook()

        for recipe in self:
            cpy.add_recipe(copy.deepcopy(recipe))

        return cpy
```

Note that the provided implementation can be improved in a few ways (e.g., by
accessing `cpy.recipes` directly). However, this approach captures the logic in
a *close-to-pseudocode* form. The actual implementation will come later.


# Putting the Pieces Together

We have discussed the flaws in the *initial Cookbook class*. Putting the code
snippets together is a good opportunity to practice a little Python. I will
leave writing the full, complete, and corrected `Cookbook` class as an exercise
to the reader.

