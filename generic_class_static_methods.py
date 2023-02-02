class MyClass:
    number_of_instances = 0

    def __init__(self, *args, **kwargs):
        self.__class__.number_of_instances += 1
        for i in range(len(args)):
            self.__setattr__(f"_{str(i)}", args[i])
        for k, v in kwargs.items():
            self.__setattr__(f"_{k}", v)

    def method(self):
        return 'instance method called', self

    @classmethod
    def class_method(cls):
        return 'class method called', cls

    @classmethod
    def fac_method(cls):
        return cls('aa', 'bb', aaa=1, bbb=1)

    @staticmethod
    def staticmethod():
        return 'static method called'


if __name__ == "__main__":
    obj = MyClass()
    obj2 = MyClass.fac_method()

    print(MyClass.__class__)
    print(obj.__class__)

    print(obj.method())
    print(obj.class_method())
    print(obj.staticmethod())

    print(MyClass.method(obj))
    print(MyClass.class_method())
    print(MyClass.staticmethod())
    print(MyClass.method())
