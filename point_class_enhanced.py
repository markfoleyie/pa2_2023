#!/usr/bin/python3

import math


class Point:
    """
    Class to make an instance of a Cartesian point
    """

    def __init__(self, x=0, y=0):
        """
        Initializes values for the x & y coordinates

        :param x:
        :param y:
        """
        self._x = x
        self._y = y

    def __str__(self):
        return "Point({},{})".format(self._x, self._y)

    def __repr__(self):
        return "{}({},{})".format(self.__class__.__name__, self._x, self._y)
        # return self.__str__()

    def distance(self, other_point):
        """
        Computes the distance between two points based on Pythagoras' theorem.

        :param other_point:
        :return: distance value
        """
        if not isinstance(other_point, self.__class__):
            # raise TypeError("{} is not a valid Point object".format(str(other_point)))
            return "ERROR: {} is not a valid Point object".format(str(other_point))
        return math.sqrt(((abs(self._x - other_point._x)) ** 2) + ((abs(self._y - other_point._y)) ** 2))

    def __add__(self, other_point):
        if not isinstance(other_point, self.__class__):
            # raise TypeError("{} is not a valid Point object".format(str(other_point)))
            return "ERROR: {} is not a valid Point object".format(str(other_point))
        return Point(self._x + other_point._x, self._y + other_point._y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, some_input):
        self._x *= some_input

    @property
    def y(self):
        return self._y


if __name__ == "__main__":
    point1 = Point(2, 3)
    point2 = Point(4, 8)
    point3 = point1 + point2
    int1 = 5

    print(point1, point2, point3)
    print("Distance from {} to {} is {}".format(point1, point2, point1.distance(point2)))
    print("Distance from {} to {} is {}".format(point1, int1, point1.distance(int1)))
