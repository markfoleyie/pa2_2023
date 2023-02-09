import datetime
import os
import time
from functools import wraps, update_wrapper


def timer_log(func_to_decorate):
    @wraps(func_to_decorate)
    def my_wrapper(*args, **kwargs):
        # Make sure that the logfile exists and if not is created
        script_dir = os.path.dirname(__file__)
        cache_dir = os.path.join(script_dir, ".cache")
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        log_file = cache_dir + "/timerlog.txt"
        if not os.path.isfile(log_file):
            fh = open(log_file, "w")
            fh.write("Date/Time,Function,Start,End,Elapsed\n")
            fh.close()

        # Open log file
        fh = open(log_file, "a")

        # Get start time
        start = time.time()

        # Run original function
        result = func_to_decorate(*args, **kwargs)

        # Get end time
        end = time.time()

        # Write log
        fh.write(f"{datetime.datetime.now().isoformat()},{script_dir + __file__ + ':' + func_to_decorate.__name__},"
                 f"{start},{end},{end - start}\n"
                 )
        fh.close()

        return result

    return my_wrapper


class logit(object):
    _logfile = 'out.log'

    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        log_string = self.func.__name__ + " was called"
        print(log_string)

        # Get start time
        start = time.time()

        # Run original function
        result = self.func(*args, **kwargs)

        # Get end time
        end = time.time()

        # Open the logfile and append
        with open(self.get_log_file(), 'a') as opened_file:
            # Now we log to the specified logfile
            opened_file.write(f"{datetime.datetime.now().isoformat()},"
                              f"{self.script_dir + __file__ + ':' + self.func.__name__},{start},{end},{end - start}\n"
                              )
        # Now, send a notification
        self.notify()

        # return base func
        return result

    def notify(self):
        # logit only logs, no more
        pass

    def get_log_file(self):
        self.script_dir = os.path.dirname(__file__)
        cache_dir = os.path.join(self.script_dir, ".cache")
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        log_file = cache_dir + "/" + self._logfile
        if not os.path.isfile(log_file):
            fh = open(log_file, "w")
            fh.write("Date/Time,Function,Start,End,Elapsed\n")
            fh.close()

        return log_file


@timer_log
def dummy():
    print("in dummy")


def get_square_of_int(num):
    if not isinstance(num, int):
        return 0
    return num ** 2


get_square_of_int = timer_log(get_square_of_int)


@logit
def dummy2():
    """
    a random docstring
    :return:
    """
    print("In dummy2")


if __name__ == "__main__":
    print()
    dummy()
    dummy2()

    my_num = 3

    print(f"The square of {my_num} is {get_square_of_int(my_num)}")
