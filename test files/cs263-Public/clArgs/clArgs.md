Title: Command Line Arguments
TOC: yes
Author: Thomas J. Kennedy


# Better than C++ and Java

The first time that you work with command line arguments in Python... one might
write...

```python
import sys


def main():
    for idx in range(1, len(sys.argv)):
        print(f"Argument #{idx:>3} was {sys.argv[idx]}")


if __name__ == "__main__":
    main()
```

*Note that `idx` is my usual loop counter. It is short for "index." I prefer to reserve `i` for mathematical code.*

Similar to C++... `sys.argv[0]` is the program itself. 

```cpp
#include <iostream>
#include <iomanip>

using namespace std;


int main(const int argc, const char* const* argv)
{
    for (int idx = 1; idx < argc; ++idx) {
        cout << "Argument #" 
             << right << setw(3) << idx
             << " was "
             << argv[idx]
             << '\n';
    }
}
```

However, if you are familiar with Java... you are used to `args[0]` as the
first user supplied argument.

```java
public class CLIDemo
{
    public static void main(String[] args)
    {
        for (int idx = 1; idx < args.length; ++idx) {
            System.out.printf("Argument %3d was %s%n", idx, args[idx])
        }
    }
}
```


# That is Not Quite Pythonic

However, Python `for` loops are usually for-each (a.k.a range based), not index
based. Let us try rewriting the loop


```python
import sys


def main():
    for idx, arg in enumerate(sys.argv):
        print(f"Argument #{idx:>3} was {arg}")


if __name__ == "__main__":
    main()
```

But... that is not quite right! We want to skip `argv[0]`.

```python
import sys


def main():
    for idx, arg in enumerate(sys.argv[1:], start=1):
        print(f"Argument #{idx:>3} was {arg}")


if __name__ == "__main__":
    main()
```

Take note of the `sys.argv[1:]`. Since the arguments are stored as a `list`...
we can make use of Python's slice syntax to *every entry starting from index
`1`.* We will discuss list slicing [in a future
lecture](doc:dataStructures2Operations).

The `enumerate` trick allows us to get an index alongside the actual data.


# Wait... "for" is not Count Based?

The Python `for` loop is a range based or for each loop. However, we will
discuss the `for` loop [in a follow-up lecture](doc:forLoops1).
