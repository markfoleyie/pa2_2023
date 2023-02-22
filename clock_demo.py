class Clock:
    total_clocks = 0

    def __init__(self, h, m, s):
        self.increment_count()
        self.h = h
        self.m = m
        self.s = s

    def __str__(self):
        return "{}:{}:[}".format(self.h, self.m, self.s)

    @classmethod
    def increment_count(cls):
        cls.total_clocks += 1

    @classmethod
    def clock_from_str(cls, in_str):
        my_str = in_str.split(":")
        h, m, s = my_str[0], my_str[1], my_str[2]
        return cls(h, m, s)

    @staticmethod
    def is_valid_str(in_str):
        try:
            h, m, s = in_str.split(":")
            h, m, s = int(h), int(m), int(s)
            return True
        except:
            return False

    @classmethod
    def print_str(cls, in_str):
        if cls.is_valid_str(in_str):
            print(in_str)
        else:
            print("Rubbish")


def main():
    my_clock = Clock(23, 59, 30)
    my_clock_2 = Clock.clock_from_str("20:34:50")
    print(Clock.is_valid_str("12:20:10"))


if __name__ == "__main__":
    main()
