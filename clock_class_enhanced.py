# simple clock class


class Clock:
    """Simple clock class
    Takes hours, minutes, seconds as ints
    Can be updated by time in the form of 'hh:mm:ss'"""

    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = self.minutes = self.seconds = 0
        if 0 <= hours <= 24:
            self.hours = hours
        if 0 <= minutes <= 59:
            self.minutes = minutes
        if 0 <= seconds <= 59:
            self.seconds = seconds

    def __str__(self):
        return '{} hours, {} minutes and {} seconds'\
            .format(self.hours, self.minutes, self.seconds)

    def __repr__(self):
        # return self.__str__()
        return "{}({}, {}, {})"\
            .format(self.__class__.__name__,
                    self.hours, self.minutes, self.seconds)

    def string_update(self, str):
        """
        Takes a string representation of time and updates the object
        :param str: "hh:mm:ss"
        :return: None
        """
        try:
            if self.is_valid(str):
                hours, minutes, seconds = [int(n) for n in str.split(':')]
                self.hours = hours
                self.minutes = minutes
                self.seconds = seconds
            else:
                raise ValueError("Invalid string")
        except Exception as e:
            print(e)

    def __add__(self, other):
        carry_minutes, seconds = divmod((self.seconds + other.seconds), 60)
        carry_hours, minutes = divmod((self.minutes + other.minutes), 60)
        carry_days, hours = divmod((self.hours + other.hours), 24)
        print('{} secs, {} carry mins, {} mins, {} carry hrs, {} hrs'.format(seconds, carry_minutes, minutes, carry_hours,
                                                                             hours))
        return Clock(hours + carry_hours, minutes + carry_minutes, seconds)

    @staticmethod
    def is_valid(clock_string):
        """
        Check that any 'clock_string' is valid (format should be hh:mm:ss)

        :param clock_string:
        :return:
        """
        try:
            hours, minutes, seconds = clock_string.split(":")
            if not (0 <= int(hours) <=23):
                return False
            if not (0 <= int(minutes) <= 59):
                return False
            if not (0 <= int(seconds) <= 59):
                return False
            return True
        except Exception as e:
            return False

    @classmethod
    def from_string(cls, clock_string):
        """
        make a Clock object from a string.

        :param clock_string:
        :return: New Clock instance
        """
        if cls.is_valid(clock_string):
            hours, minutes, seconds = clock_string.split(":")
            return cls(int(hours), int(minutes), int(seconds))


if __name__ == "__main__":

    c0 = Clock(25, 77, 99)
    c1 = Clock(23, 59, 10)
    c2 = Clock(9, 20, 00)

    c3 = c1 + c2
    c4 = c1.__add__(c2)

    print('c1: {}'.format(c1))
    print('c2: {}'.format(c2))
    print('c3: {}'.format(c3))
    c2.string_update('11:23:45')
    print('c2: {}'.format(c2))

    clock_string = "23:59:59"
    print("{} is {}".format(clock_string, str(Clock.is_valid(clock_string))))

    new_clock = None
    if Clock.is_valid(clock_string):
        new_clock = Clock.from_string(clock_string)

    print("new clock: {} has type: {}".format(new_clock, type(new_clock)))
