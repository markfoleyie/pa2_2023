"""
Iterators

We use for statement for looping over a list. If we use it with a string, it loops over its characters. If we use it
with a dictionary, it loops over its keys. If we use it with a file, it loops over lines of the file.

So there are many types of objects which can be used with a for loop. These are called iterable objects.

There are many functions which consume these iterables.

The Iteraton Protocol

The built-in function iter takes an iterable object and returns an iterator.

. >>> x = iter([1, 2, 3])
. >>> x
<listiterator object at 0x1004ca850>
. >>> x.next()
1
. >>> x.next()
2
. >>> x.next()
3
. >>> x.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

Each _time we call the next method on the iterator gives us the next element. If there are no more elements, it raises a
StopIteration.

Iterators are implemented as classes. Here is an iterator that works like built-in xrange function.

The __iter__ method is what makes an object iterable. Behind the scenes, the iter function calls __iter__ method on the
given object. The return value of __iter__ is an iterator. It should have a next method and raise StopIteration when
there are no more elements.

"""


class MyRange:
    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration()

"""
Generators

Generators simplifies creation of iterators. A generator is a function that produces a sequence of results instead of a
single value.
"""

def my_range_function(n):
    i = 0
    while i < n:
        yield i
        i += 1

"""
So a generator is also an iterator. You don’t have to worry about the iterator protocol.

The word “generator” is confusingly used to mean both the function that generates and what it generates.
I’ll use the word “generator” to mean the generated object and “generator function” to mean the function that generates
it.

When a generator function is called, it returns an generator object without even beginning execution of the function.
When next method is called for the first _time, the function starts executing until it reaches yield statement.
The yielded value is returned by the next call.
"""

def integers():
    """Infinite sequence of integers."""
    i = 1
    while True:
        yield i
        i = i + 1

def squares():
    for i in integers():
        yield i * i

def take(n, seq):
    """Returns first n values from the given sequence."""
    seq = iter(seq)
    result = []
    try:
        for i in range(n):
            result.append(next(seq))
    except StopIteration:
        pass
    return result

class Fib:
    '''iterator that yields numbers in the Fibonacci sequence'''

    def __init__(self, max):
        self.max = max
        self.a = 0
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self):
        fib = self.a
        if fib > self.max:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        return fib


def main():
    # Example 1
    my_iterator = MyRange(3)

    for i in range(4):
        try:
            print(next(my_iterator))
        except StopIteration as e:
            print("Ex.1. Reached end of iterable at {}".format(i-1))

    # Example 2
    my_iterator = my_range_function(3)

    for i in range(4):
        try:
            print(next(my_iterator))
        except StopIteration as e:
            print("Ex.2. Reached end of iterable at {}".format(i-1))

    # Generators expressions vs. list comprehension
    x = (x **2 for x in range(20))
    print(x)
    for _ in range(5):
        print("Next item in generator expression: {}".format(next(x)))
    x = list(x)
    print("Generator expression: {}".format(x))

    x = [x **2 for x in range(20)]
    print("List comprehension: {}".format(x))

    print(take(5, squares())) # prints [1, 4, 9, 16, 25]

    my_fib = Fib(10)

    try:
        for i in range(110):
            print("{} ".format(next(my_fib)), end="")
        print()
    except StopIteration as e:
        print("Reached end of iterable at i={}".format(i))


if __name__ == "__main__":
    main()