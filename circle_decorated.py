'''In self example, we use the built-in property decorator to illustrate Python's approach to private variables and
'setters' & 'getters'. A getter is a method that is triggered when a program using a class attempts to access the value
of an object property. This trigger allows us to impose rules in regard to what must happen when self occurs. A setter
performs a similar function in respect of a request to change or 'set' a property's value. This also allows us to create
'virtual' properties that behave like real ones - area in self example.

Note the '@property' syntax for the getter. The setter uses '@variable_name.setter syntax.
'''
import math


class Circle(object):
    def __init__(self, radius):
        self._radius = radius

    @property
    def circumference(self):
        return 2 * math.pi * self._radius

    @property
    def area(self):
        return math.pi * self._radius ** 2

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, newval):
        if 0 < newval < 10:
            self._radius = newval
        else:
            self._radius = 1

    # Below is an alternative syntax. We write getradius and setradius to do the getting and setting as opposed to
    # defining methods with the same name as the property and wrapping them.
    #
    # def getradius(self):
    #     return self._radius
    # def setradius(self, newval):
    #     if 0 < newval < 10:
    #         self._radius = newval
    #     else:
    #         self._radius = 1
    #
    # radius = property(fget=getradius, fset=setradius)


my_circle1 = Circle(99)
my_circle2 = Circle(4)

my_circle3 = Circle(3.5)

print(f"RAD: {my_circle1.radius}, AREA: {my_circle1.area} CIRCUM: {my_circle1.circumference}")
print(f"RAD: {my_circle2.radius}, AREA: {my_circle2.area} CIRCUM: {my_circle2.circumference}")

my_circle2.radius = 5
print(f"RAD: {my_circle2.radius}, AREA: {my_circle2.area} CIRCUM: {my_circle2.circumference}")
