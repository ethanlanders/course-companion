Title: PEP 20 - The Zen of Python
TOC: yes
Author: Thomas J. Kennedy


The Python language maintains a set of Python Enhancement Proposals (PEPs). If
you are curious... The full index of PEPs can be accessed at
<https://peps.python.org/pep-0000/>.


# The Zen of Python

For the moment, we are only interested in **PEP 20 - The Zen of Python**.

\bSidebar

*I am partial to number fourteen (14).* The rule is a reference to famous
Computer Scientist [Edsger W.
Dijkstra](https://en.wikipedia.org/wiki/Edsger_W._Dijkstra) who is responsible
for [Dijkstra's
algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm).

This shortest path algorithm is a staple of algorithms courses... which means
you will cover it at some point in your course work.

\eSidebar

> 88. Beautiful is better than ugly.
> 88. Explicit is better than implicit.
> 88. Simple is better than complex.
> 88. Complex is better than complicated.
> 88. Flat is better than nested.
> 88. Sparse is better than dense.
> 88. Readability counts.
> 88. Special cases aren't special enough to break the rules.
> 88. Although practicality beats purity.
> 88. Errors should never pass silently.
> 88. Unless explicitly silenced.
> 88. In the face of ambiguity, refuse the temptation to guess.
> 88. There should be one-- and preferably only one --obvious way to do it.
> 88. Although that way may not be obvious at first unless you're Dutch.
> 88. Now is better than never.
> 88. Although never is often better than *right* now.
> 88. If the implementation is hard to explain, it's a bad idea.
> 88. If the implementation is easy to explain, it may be a good idea.
> 88. Namespaces are one honking great idea -- let's do more of those!
>
> *Reproduced from <https://peps.python.org/pep-0020/>.*


# What do the Rules Mean?

A few of these rules can be discussed from the perspective of an introductory
programming course (i.e., your earliest programming coursework).

  - Beautiful is better than ugly.
  
  - Explicit is better than implicit.

In general programming courses emphasize meaningful (or self-documenting) names
for variables, functions, and classes. (While the importance of naming applies
to concepts such as enumerated types and namespaces... we will forgo an
exhaustive list.)

  - Readability counts.

Code should not require continuous inline comments. For example...

```python
def main():
    # Point 1
    x1 = 1.0
    y1 = 1.0
    
    # Point 2
    x2 = 2.0
    y2 = 2.0

    # Compute the differences "x2 - x1" and "y2 = y1"
    diff_x = x2 - x2
    diff_y = y2 - y1

    # Compute the distance using the euclidean distance formula
    r = sqrt(diff_x ** 2 + diff_y ** 2)

    # Output the distance to two (2) decimal places
    print(f"The distance is {r:.2f}.")


if __name__ == "__main__":
    main()
```

is what someone more familiar with C++


^^^[C++ Version]

```cpp
#include <iostream>
#include <iomanip>
#include <cmath>


using namespace std;

int main(const int argc, const char* const* argv)
{
	// Point 1
	double x1 = 1.0;
	double y1 = 1.0;
	
	// Point 2
	double x2 = 2.0;
	double y2 = 2.0;

	// Compute the differences "x2 - x1" and "y2 = y1"
	const double diff_x = x2 - x2;
	const double diff_y = y2 - y1;

	// Compute the distance using the euclidean distance formula
	const double r = Math.sqrt((diff_x * diff_x) + (diff_y * diff_y));

	// Set fixed decimal formatting (2 places)
	cout.precision(2);
	cout.setf(ios::fixed);

	// Output the distance
	cout << "The distance is " << r << "\n";

	return 0;
}
```
^^^

or Java

^^^[Java Version]

```java
public class PointDistance
{
	public static void main(String... args)
	{
		// Point 1
		double x1 = 1.0;
		double y1 = 1.0;
		
		// Point 2
		double x2 = 2.0;
		double y2 = 2.0;

		// Compute the differences "x2 - x1" and "y2 = y1"
		double diff_x = x2 - x2;
		double diff_y = y2 - y1;

		// Compute the distance using the euclidean distance formula
		double r = Math.sqrt((diff_x * diff_x) + (diff_y * diff_y));

		// Output the distance to two (2) decimal places
		System.out.printf("The distance is %.2f.%n", r);
	}
}
```
^^^

might write.

However, our focus is on Python. The Python code can be rewritten/refactored
more readily based on the

  - *Zen of Python* ~~rules~~ guidelines
  - *Batteries Included* philosophy of the Python language

Let us address both unnecessary comments (particularly regarding outputting to
two decimal places and comments due to poor naming. Code along the lines of

```python
from typing import Tuple

def point_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Compute the distance between two points using the well-known euclidean
    distance formula:

      sqrt((x2 - x1)^2 + (y2 - y1)^2)

    Args:

      p1 - first point
      p2 - second points
    """

    diff_x = p2[0] - p1[0]
    diff_y = p2[1] - p1[1]

    return sqrt(diff_x ** 2 + diff_y ** 2)


def main():
    # Define two points
    point_1 = (1.0, 1.0)
    point_2 = (2.0, 2.0)

    # Compute and output the distance
    distance = point_distance(point_1, point_2)
    print(f"The distance is {distance:.2f}.")


if __name__ == "__main__":
    main()
```

would be much better. *These types of issues will be discussed in future
lectures.*

  -  Special cases aren't special enough to break the rules.
  -  Although practicality beats purity.

Most *best practice* or *good style* discussions gloss over (or outright
ignore) that programming rules are (to quote a well-known move franchise) *more
guidelines than actual rules.*

Style rules and best practices **must** be applied from perspective of

> Why does this rule exist?

and not rote memorization.


# Python Includes Batteries

For many languages external libraries are usually required for *common
operations*. However, <a href="https://www.python.org/dev/peps/pep-0206/#id3" target="_blank">Python includes batteries</a>.
We are interested in the first two paragraphs of the philosophy...

>
> The Python source distribution has long maintained the philosophy of
> “batteries included” – having a rich and versatile standard library which is
> immediately available, without making the user download separate packages. This
> gives the Python language a head start in many projects.
> 
> However, the standard library modules aren't always the best choices for a job.
> Some library modules were quick hacks (e.g. `calendar`, `commands`), some were
> designed poorly and are now near-impossible to fix (`cgi`), and some have been
> rendered obsolete by other, more complete modules (`binascii` offers the same
> features as the `binhex`, `uu`, `base64` modules). This PEP describes a list of
> third-party modules that make Python more competitive for various application
> domains, forming the Python Advanced Library.
>
> *Reproduced from <https://www.python.org/dev/peps/pep-0206/#id3>.*

Like many Python programmers... I have made frequent use of quite a few of
these built-in libraries for lecture examples and course administration (e.g.,
updating dates from semester to semester).

| Operation                                 | Built-in Python Module |
| :---------------------------------------- | :------------------    |
| Working with zip files                    | `import zipfile`       |
| Working with gzipped files                | `import gzip`          |
| Reading, writing, or generating JSON      | `import json`          |
| Converting objects to JSON                | `import json`          |
| Serializing objects and data structures   | `import pickle`        |
| Working with time                         | `import time`          |
| Working with dates and time               | `import datetime`      |
| Working with SQLite                       | `import sqlite3`       |
| Using advanced command line arguments     | `import argparse`      |


## Third-Party (External) Libraries & pip

When external libraries are required, the Python `pip` utility and a
`requirements.txt` can be used for all dependency and configuration management.

In C/C++ we hope for a Linux environment (or Docker). In Java... Gradle is a
popular build and configuration management tool. In Rust... Cargo handles
dependency and configuration management.


