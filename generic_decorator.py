from functools import wraps, update_wrapper


def my_decorator(func_to_decorate):
    @wraps(func_to_decorate)
    def my_wrapper(*args, **kwargs):
        """
        Docstring for my_wrapper.
        Any extra work needed before the wrapped function goes here

        :param args:
        :param kwargs:
        :return:
        """
        print("In wrapper, wrapping {}".format(func_to_decorate.__name__))
        # The wrapped function is executed
        result = func_to_decorate(*args, **kwargs)
        # Any work needed after the wrapped function goes here
        print("Still in wrapper, returning wrapped {}"
              .format(func_to_decorate.__name__))
        # The result of the execution of the wrapped function is returned
        return result

    # The wrapped function is returned
    return my_wrapper


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
    return "random string"


if __name__ == "__main__":
    res = add2nums(3, 4)
    res2 = get_random_sting()

    print(f"{res}\n{res2}")
    print(f"add2nums: {add2nums.__name__}, {add2nums.__doc__}")
