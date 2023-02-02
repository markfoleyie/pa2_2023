"""
First call_me of Subclass calls super().call_me(), which happens to refer to LeftSubclass.call_me().
LeftSubclass.call_me() then calls super().call_me(), but in self case, super() is referring to RightSubclass.call_me().
Pay particular attention to self; the super call is not calling the method on the superclass of LeftSubclass
(which is BaseClass ), it is calling RightSubclass, even though it is not a parent of LeftSubclass! This is the next
method, not the parent method. RightSubclass then calls BaseClass and the super calls have ensured each method in the
class hierarchy is executed once.
"""


class BaseClass:
    num_base_calls = 0

    def call_me(self):
        print("Calling method on Base Class")
        self.num_base_calls += 1


class LeftSubclass(BaseClass):
    num_left_calls = 0

    def call_me(self):
        super().call_me()
        print("Calling method on Left Subclass")
        self.num_left_calls += 1


class RightSubclass(BaseClass):
    num_right_calls = 0

    def call_me(self):
        super().call_me()
        print("Calling method on Right Subclass")
        self.num_right_calls += 1


class Subclass(LeftSubclass, RightSubclass):
    num_sub_calls = 0

    def call_me(self):
        super().call_me()
        print("Calling method on Subclass")
        self.num_sub_calls += 1


if __name__ == "__main__":
    s = Subclass()
    s.call_me()
    print(s.num_sub_calls, s.num_left_calls, s.num_right_calls, s.num_base_calls)
    print(Subclass.mro())
