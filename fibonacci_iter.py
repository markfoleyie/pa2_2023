# This example is taken from 'Dive Into Python 3', copyright (c) 2009, Mark Pilgrim, All rights reserved.

class Fib:
    '''iterator that yields numbers in the Fibonacci sequence

    To build an iterator from scratch, Fib needs to be a class, not a function.

    The __iter__() method is called whenever someone calls iter(fib). (A for loop will call this automatically,
    but you can also call it yourself manually.) After performing beginning-of-iteration initialization (in this case,
    resetting self.a and self.b, our two counters), the __iter__() method can return any object that implements a
    __next__() method. In this case (and in most cases), __iter__() simply returns self, since this class implements its
    own __next__() method.

    The __next__() method is called whenever someone calls next() on an iterator of an instance of a class.

    When the __next__() method raises a StopIteration exception, this signals to the caller that the iteration is
    exhausted. Unlike most exceptions, this is not an error; it’s a normal condition that just means that the iterator
    has no more values to generate. If the caller is a for loop, it will notice this StopIteration exception and
    gracefully exit the loop. (In other words, it will swallow the exception.) This little bit of magic is actually the
    key to using iterators in for loops.

    To spit out the next value, an iterator’s __next__() method simply returns the value. Do not use yield here;
    that’s a bit of syntactic sugar that only applies when you’re using generators. Here you’re creating your own
    iterator from scratch; use return instead.
    '''

    def __init__(self, max):
        self.max = max

    def __iter__(self):
        self.a = 0
        self.b = 1
        return self

    def __next__(self):
        fib = self.a
        if fib > self.max:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        return fib


if __name__ == '__main__':
    for n in Fib(1000):
        print(n, end=' ')