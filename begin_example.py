import begin
import sys


@begin.start(auto_convert=True)
def main(a: 'First value' = 0.0, b: 'Second value' = 0.0):
    """ Add two numbers """
    print(a + b)
