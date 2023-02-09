"""
Extended Exercise in OO design and development

In this exercise running over the next several weeks we are going to collectively build an OO system of moderate
complexity in Python.

We will address a small piece of the system each week.

Predator-Prey Problem

We consider the simulation of a natural habitat. For this purpose you might consider a simulation to be
something like a single player game whereby you set up certain parameters and the computer plays it out based on these.

In our habitat, you have two kinds of animal – predators (think of wolves) and prey (think of moose). Predators must
eat prey to survive. Prey try to avoid being eaten. Both can breed and move position. The simulation shows the dynamic
interaction of these two populations. Typically both groups have a fixed birthrate. The prey usually breed faster than
the predators, allowing for a growing prey population. As the prey population increases it can support a growing number
of predators which, in turn leads to a decreasing prey population. Around this time the predator population grows too
large for the prey to support and thus declines. This leads to a recovery in the prey population and so the cycle
repeats. This cycle of growth and decay continues.

Our example is based on a study which looked at the interaction of wolves and moose on Isle Royale in Lake
Superior. Being an island, Isle Royale is isolated from the mainland so, for our purposes, we can consider
it a closed world.

Rules

The habitat updates itself in units of time called clock ticks. During one tick, each animal gets to do something.

All animals are give an opportunity to move into an adjacent space, if an empty space can be found. One move per clock
tick is allowed.

Both predators and prey can reproduce. Each animal is assigned a fixed breed time. If it is still alive after
breed-time ticks of the clock, it will reproduce. It does this by finding an adjacent space and copies itself to that
space, hence increasing its population by one. The animal's breed-time is then reset to zero. An animal can breed, at
most, once per clock tick.

The predators must eat. They have a fixed starve time. If they cannot find prey to eat before starve-time clock
ticks, they die.

When a predator eats, it moves into an adjacent space, formerly occupied by the prey that it has just eaten. The prey
is removed and the predator's starve-time reset to zero. Eating counts as a predator's move during the clock tick.

At the end of every clock tick, each animal's local event clock is updated. All animals' breed time are decremented
and all predators' starve-times are decremented.

I intend expanding this text with a new piece of the puzzle each week. The rules above describe the whole problem but
for now I want you to consider it as a series of discrete pieces. Week by week we can discuss this in class until we
gradually build out a complete solution.

To think about:
* What classes do you need?
* What methods do these classes need to realise the solution?
* Do any of the classes inherit from other classes?
* Do we need abstract class(es)?
* How might we represent the island?
* How might we populate the island?
* How do we model behaviour?
"""

import random

class Island:
    def __init__(self, grid_size=10, predator_count=5, prey_count=20):
        """
        Set up the Island -> square grid of size 'grid_size'. Initialize grid to all 0's, then fill with animals.

        :param grid_size:
        """
        if not isinstance(grid_size, int):
            self._grid_size = 10
        else:
            self._grid_size = grid_size

        # This is a short way to create the grid using a 'list comprehension'. This creates a list
        # 0*n or [0 for i in range(n)] and duplicates this list within an outer list -
        # newList*n or [[0 for i in range(n)] for j in range(n)]
        self._grid = [[0 for i in range(self._grid_size)] for j in range(self._grid_size)]

        # Make a dictionary of the numbers we want for each type. This will be used later to create both types in
        # one method.
        if not isinstance(predator_count, int):
            predator_count = 5
        if not isinstance(prey_count, int):
            prey_count = 20
        self._animal_numbers = {"Predator": predator_count, "Prey": prey_count}

    def init_animals(self):
        ''' Put some initial animals on the island'''

        # Iterate through the dictionary and make instances
        # 'k' is the class name - Predator or Prey, a key in the dictionary. Its associated value is the count
        # There is an element of uncertainty here. An ATTEMPT is made to create an animal each time but if the
        # space is already occupied then we pass on silently. This means that we could end up with fewer animals
        # then initially specified.

        for k in self._animal_numbers:
            for i in range(self._animal_numbers[k]):
                # Generate random integers for x & y. These must be valid grid locations.
                x = random.randint(0, self._grid_size - 1)
                y = random.randint(0, self._grid_size - 1)
                if not self._grid[x][y]:
                    # globals() returns a dictionary that represents the current global namespace.
                    # The keys of this dictionary are globally defined names, and each corresponding value is
                    # the value for that name. Thus, globals()[k](island=self, x=x, y=y) makes an instance of 'k'
                    # where k is a Predator or Prey. This trick avoids duplicating the code for predators and prey.
                    # We then add the animal to the grid.

                    self._grid[x][y] = globals()[k](self, x, y)
                    # self.register(globals()[k](self, x, y))


    def __str__(self):
        """
        Return a string representation of the Island -> formatted cartesian x-y grid.
        Origin should be on bottom left of display.

        :return:
        """
        return f""

class Animal:
    pass

class Predator(Animal):
    pass

class Prey(Animal):
    pass


def main():
    pass


if __name__ == "__main__":
    main()
