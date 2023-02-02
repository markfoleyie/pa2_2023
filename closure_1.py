# Python program to illustrate
# closures
def outerFunction(text):
    def innerFunction():
        print(text)

    # Note we are returning function
    # WITHOUT parenthesis
    return innerFunction


if __name__ == '__main__':
    myFunction = outerFunction('Hey!')
    myFunction()
