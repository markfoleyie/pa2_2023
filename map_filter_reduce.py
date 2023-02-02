"""
Python includes a number of functions for functional programming.
The map() function takes the form map(function, iterable) and applies function to each item in iterable to return an
iterable map object.
items = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, items))

The filter() function takes the form filter(function or None, iterable) and filters the items in iterable based on
the result returned by function . This will return an iterable filter object.
number_list = range(-5, 5)
less_than_zero = list(filter(lambda x: x < 0, number_list))
# Output: [-5, -4, -3, -2, -1]

reduce() is a really useful function for performing some computation on a list and returning the result. It applies a rolling computation to sequential pairs of values in a list. For example, if you wanted to compute the product of a list of integers.
from functools import reduce
product = reduce((lambda x, y: x * y), [1, 2, 3, 4])
# Output: 24
"""

items = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, items))

number_list = range(-5, 5)
less_than_zero = list(filter(lambda x: x < 0, number_list))

from functools import reduce
product = reduce((lambda x, y: x * y), [1, 2, 3, 4])

pass