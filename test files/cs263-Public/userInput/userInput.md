Title: User Input & Standard Input
TOC: yes
Author: Thomas J. Kennedy


# Simpler Than C++ & Java

To prompt the user for input Python, one need only use the `input` function,
e.g.,

```python
def main():

    color = input("Enter your favorite color: ")


if __name__ == "__main__":
    main()
```

Both C++...

```cpp
int main(const int argc, const char* const* argv)
{
    std::string color;
    
    std::cout << "Enter your favorite color: "
    std::cin >> color;

    return 0;
}
```

and Java...

```java
    public static void main(String... args)
    {
        Scanner inputStream = new Scanner(System.in);
        String color = null;

        System.out.print("Enter your favorite color: ");
        color = inputStream.next();
    }
```

require more steps.


# Only Strings?

You are probably a bit concerned that I only demonstrated how to retrieve user
input as a string. In Python (similar to Java and Rust), all user input is read
in as a string that we then convert. *C++ is a bit more interesting with its
Stream Extraction Operator (`operator>>`).*

Consider the following code snippet.

```python
def main():

    price = input("What is the price of your favorite lunch? ")
    frequency = input("How many times a week do you have that lunch? ")

    price = float(price)
    frequency = int(frequency)

    print(f"On average you spend {price * frequency:.2f}")


if __name__ == "__main__":
    main()
```

Python actually lets us change the type of a variable... so `price` can start
off as a `str` before be replaced with its parsed `float` value. We can
actually simplify the code...

```python
def main():

    price = float(input("What is the price of your favorite lunch? "))
    frequency = int(input("How many times a week do you have that lunch? "))

    print(f"On average you spend {price * frequency:.2f}")


if __name__ == "__main__":
    main()
```

We do not need to store the raw string values. We can (and in this case) should
convert them immediately.


# Computation in the Output

I bet that you found the output statement (at least) a little surprising.

```python
    print(f"On average you spend {price * frequency:.2f}")
```

The Python
<a href="https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals" target="_blank">f-string</a>
provides quite a bit of convenience... including embedding a larger expression.
A more complete discussion of f-strings will be covered in an [upcoming
lecture](doc:fstrings1).

