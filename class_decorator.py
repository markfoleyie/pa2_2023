import uuid


def set_class_name_and_id(klass):
    klass.name = str(klass)
    klass.random_id = uuid.uuid4()
    return klass


@set_class_name_and_id
class SomeClass:
    def __str__(self):
        return f"Class: {self.__class__.__name__}, Randon Id: {self.random_id}"


if __name__ == '__main__':
    my_class = SomeClass()
    print(my_class)
