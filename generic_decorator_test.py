from generic_decorator import my_decorator
from generic_logging_decorator import timer_log, logit


@my_decorator
def add2nums(a, b):
    """
    docstring for add2nums
    :param a:
    :param b:
    :return: a+b
    """
    return a + b


@my_decorator
def get_random_sting():
    """
    Just returns random string
    :return: see above
    """
    return "random string"


@timer_log
def dummy():
    print("in dummy")


@logit
def dummy2():
    """
    a random docstring
    :return:
    """
    print("In dummy2")


if __name__ == "__main__":
    res = add2nums(3, 4)
    res2 = get_random_sting()
    res4 = add2nums(b=99, a=10)

    print(f"{res}\n{res2}")
    print(f"add2nums: {add2nums.__name__}, {add2nums.__doc__}")

    print()
    dummy()
    dummy2()
