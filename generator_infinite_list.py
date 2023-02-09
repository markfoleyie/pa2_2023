"""Generating an infinite sequence will require the use of a generator, since your computer memory is finite"""

import sys


def infinite_sequence(max_digits):
    try:
        num = 0
        while True:
            if len(str(num)) < max_digits:
                yield num
                num += 1
            else:
                raise StopIteration
    except StopIteration:
        print(f"Sequence stops when length of return number reaches {max_digits}.")


if __name__ == "__main__":
    nums_squared_lc = [num ** 2 for num in range(50000)]
    nums_squared_gc = (num ** 2 for num in range(50000))

    print(f"Size of nums_squared_lc is {sys.getsizeof(nums_squared_lc)} bytes.")
    print(f"Size of nums_squared_gc is {sys.getsizeof(nums_squared_gc)} bytes.")

    for i in infinite_sequence(7):
        print(i, end=" ")
