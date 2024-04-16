Title: Procedural, Object-Oriented & Functional Programming
TOC: yes
Author: Thomas J. Kennedy


# Overview

There are generally three styles of code found in Python.
  
  - Procedural
  - Object Oriented
  - Functional

A single codebase may use one paradigm or a combination of paradigms.


# One Program... Three Paradigms

Suppose that we want to take three (3) points and compute the distance
(i.e., $\sqrt{x^2 + y^2}$) from the origin for each point.

## Procedural

The procedural approach would

  1. create three points (`point1`, `point2`, and `point3`) as `tuple`s
  2. place the three points in a list
  3. loop over the list, compute each distance, and output each distance

```python

def main():
    point1 = (0, 5)
    point2 = (8, 3)
    point3 = (1, 7)

    points = [point1, point2, point3]

    for point in points:
        print(sqrt(point[0] ** 2 + point[1] ** 2))

if __name__ == "__main__":
    main()

```

We can probably get rid of the three (3) point variables... and store
everything in the list immediately.

```python

def main():
    points = [(0, 5), (8, 3), (1, 7)]

    for point in points:
        print(sqrt(point[0] ** 2 + point[1] ** 2))

if __name__ == "__main__":
    main()

```

This procedural approach tends to be how most *quick* Python programs are
written.


## Object Oriented

If we wanted to take the class-based approach... we would start with a class...

\bSidebar

A <a href="https://docs.python.org/3/library/dataclasses.html" target="_blank">dataclass</a> would be
ideal here. However, dataclasses are outside the scope of this lecture.

\eSidebar

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self)
        return sqrt(self.x ** 2 + self.y ** 2)
```

The `main` function would be near identical...

```python
def main():
    points = [Point(0, 5), Point(8, 3), Point(1, 7)]

    for point in points:
        print(point.magnitude())

if __name__ == "__main__":
    main()
```

A proper discussion of object oriented Python would require explanation of the
[rules of a class checklist](doc:classChecklistInPython)... But, those are topics
for future discussion.


## Functional

The functional approach would look at everything a list (more aptly, something
that behaves like a list).

```python
def main():
    points = [(0, 5), (8, 3), (1, 7)]

    distances = [sqrt(point[0] ** 2 +  point[1] ** 2) for point in points]

    shortest_distance = min(distances)
    largest_distance  = max(distances)
    average_distance  = sum(distances) / len(points)
```

Note how the distances are stored in a second list.


# Concessions

Each piece of code could be improved. However, these improvements would require
familiarity with topics such as *generator expressions* and dunder functions
(which are covered in later modules).

