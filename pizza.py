from abc import abstractmethod, ABCMeta
import math


class BasePizza(metaclass=ABCMeta):
    default_ingredients = ["cheese", ]

    @abstractmethod
    def get_radius(self):
        pass

    @classmethod
    @abstractmethod
    def get_ingredients(cls):
        return cls.default_ingredients


class Pizza(BasePizza):
    brand = "My Pizza Co."

    def __init__(self, size, ingredients="tomatoes"):
        self._size = size
        if ingredients:
            self.ingredients = self.get_ingredients(ingredients)
        else:
            self.ingredients = super().get_ingredients()

    def get_ingredients(self, ingredients):
        return super().get_ingredients().append(ingredients)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def get_size(self):
        return self._size

    ##Comment out this method to show how an abstract method in the parent class must be implemented
    def get_radius(self):
        return self.size

    @staticmethod
    def mix_ingredients(x, y):
        return x + y

    @staticmethod
    def compute_circumference(radius):
        return math.pi * (radius ** 2)

    @classmethod
    def compute_volume(cls, height, radius):
        # example of a static method calling a 'static' method but needing to know its class.
        return height * cls.compute_circumference(radius)

    @classmethod
    def get_brand(cls):
        return cls.brand

    @classmethod
    def from_leftovers(cls):
        """
        factory method
        :return:
        """
        return cls(20, "random cheese" + "Peelings" + "rotten tomatoes")


if __name__ == "__main__":
    try:
        rubbish = Pizza.from_leftovers()
        print(Pizza.get_size)  # get_size() is not tied to any particular object. Therefore, it is treated as a
        # normal function.
        try:
            print(Pizza.get_size())  # Python will raise an error if we try to call it directly.
        except Exception as e:
            print(f"{e}")
        print(Pizza.get_size(
            Pizza(42)))  # Works, not very convenient: we have to refer to the class every _time we want to call
        # one of its methods.
        print(Pizza(42).get_size())  # Works, we can access get_size() from any Pizza instance, and, better still,
        # Python will automatically pass the object itself to the method’s self parameter.
        m = Pizza(42).get_size
        print(m())  # As long as you have a reference to the bound method, you do not even have
        # to keep a reference to your Pizza object. Moreover, if you have a reference
        # to a method but you want to find out which object it is bound to, you can
        print(m.__self__)  # just check the method’s __self__ property,
    except Exception as e:
        print("{}".format(e))
