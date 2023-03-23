#!/usr/bin/env python

"""Predator-Prey Simulation
   four classes are defined: animal, predator, prey, and island where island is where the simulation is taking place,
   i.e. where the predator and prey interact (live). A list of predators and prey are instantiated, and
   then their breeding, eating, and dying are simulated.
"""
import random, pygame, sys, os
from pygame.locals import *
import matplotlib.pyplot as plt

import time


def my_timer(func_to_decorate):
    def my_wrapper(*args, **kwargs):
        print("In wrapper, wrapping {}".format(func_to_decorate.__name__))
        t1 = time.time()
        result = func_to_decorate(*args, **kwargs)
        t2 = time.time()
        print("Still in wrapper, returning wrapped {}. Runtime: {:7f}".format(func_to_decorate.__name__, t2 - t1))
        return result

    return my_wrapper


class Island:
    """Island
       n X n grid where zero value indicates not occupied."""

    def __init__(self, grid_size, prey_cnt=0, predator_cnt=0):
        '''Initialize grid to all 0's, then fill with animals
        '''

        # Make a dictionary of the numbers we want for each type. This will be used later to create both types in
        # one method.
        self.animal_numbers = {"Predator": predator_cnt, "Prey": prey_cnt}

        self.grid_size = grid_size

        # This is a short way to create the grid using a 'list comprehension'. This creates a list
        # 0*n or [0 for i in range(n)] and duplicates this list within an outer list -
        # newList*n or [[0 for i in range(n)] for j in range(n)]
        self.grid = [[0 for i in range(self.grid_size)] for j in range(self.grid_size)]

        # We move the method to create the initial population of the island to the Island class as it is more
        # appropriate to have it here rather than as a stand-alone function.
        self.init_animals(prey_cnt, predator_cnt)

    def __str__(self):
        '''String representation for printing.
           (0,0) will be in the lower left corner.
        '''
        s = "\n"
        for j in range(self.grid_size - 1, -1, -1):  # print row size-1 first
            s += "{:^4}".format(j) + "| "
            for i in range(self.grid_size):  # each row starts at 0
                if not self.grid[i][j]:
                    # print a '.' for an empty space
                    s += "{:^4}".format(".")
                else:
                    # print the char X or O representing the animal
                    s += "{:^4}".format(str(self.grid[i][j]))
            s += "\n"

        s += "{:^4}".format("----") * (self.grid_size + 1) + "\n"
        s += "{:^4}| ".format(" ")
        for i in range(self.grid_size):
            s += "{:^4}".format(i)
        s += "\n"
        return s

    def __repr__(self):
        return self.__str__()

    def init_animals(self, preyCnt, predatorCnt):
        ''' Put some initial animals on the island'''

        # Iterate through the dictionary and make instances
        # 'k' is the class name - Predator or Prey, a key in the dictionary. Its associated value is the count
        # There is an element of uncertainty here. An ATTEMPT is made to create an animal each time but if the
        # space is already occupied then we pass on silently. This means that we could end up with fewer animals
        # then initially specified.

        for k in self.animal_numbers:
            for i in range(self.animal_numbers[k]):
                # Generate random integers for x & y. These must be valid grid locations.
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                if not self.grid[x][y]:
                    # globals() returns a dictionary that represents the current global namespace.
                    # The keys of this dictionary are globally defined names, and each corresponding value is
                    # the value for that name. Thus, globals()[k](island=self, x=x, y=y) makes an instance of 'k'
                    # where k is a Predator or Prey. This trick avoids duplicating the code for predators and prey.
                    # We then add the animal to the grid.

                    # self.grid[x][y] = globals()[k](self, x, y)
                    self.register(globals()[k](self, x, y))

    def clear_all_moved_flags(self):
        ''' Animals have a moved flag to indicated they moved this turn.
        Clear that so we can do the next turn
        '''

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if isinstance(self.grid[x][y], Animal):
                    self.grid[x][y].moved = False

    def register(self, animal):
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal):
        self.grid[animal.x][animal.y] = 0


class Animal:
    ''' This is our generic animal class. We use this because most of the values and methods such as location,
    move, breed etc. are common to both predators and prey.
    '''

    def __init__(self, island, x=0, y=0, s="A"):
        '''Initialize the animals and their positions
        '''
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def update_state(self):
        '''Update state variables such as breed clock and starve clock, Prey only updates its local breed clock
        '''
        self.breed_clock -= 1


    def check_grid(self, type_looking_for=int):
        ''' Look in the 8 directions from the animal's location
        and return the first location that presently has an object
        of the specified type. Return 0 if no such location exists
        '''
        result = 0

        # Animal.move_attempts is a class variable, Its value is specified at the start of the program and doesn't
        # change.
        for i in range(Animal.move_attempts):
            # We have a defined number attempts to move 1 space in a random direction
            x = self.x + random.randint(-1, 1)
            y = self.y + random.randint(-1, 1)
            if (not 0 <= x < self.island.grid_size) or (not 0 <= y < self.island.grid_size):
                # Must stay on the island (a valid grid ref)
                continue
            if isinstance(self.island.grid[x][y], type_looking_for):
                result = (x, y)
                break
        return result


    def move(self):
        '''Move to an open, neighboring position '''
        if not self.moved:
            location = self.check_grid(int)
            if location:
                print("{} ({},{}) -> ({},{})".format(self.name, self.x, self.y, location[0], location[1]))
                # self.island.grid[self.x][self.y] = 0  # remove from current spot
                self.island.remove(self)
                self.x = location[0]  # new coordinates
                self.y = location[1]
                # self.island.grid[self.x][self.y] = self
                self.island.register(self)
                self.moved = True


    def breed(self):
        ''' Breed a new Animal.If there is room in one of the 8 locations place the new animal there.
        Otherwise you have to wait.'''
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                print("{} ({},{}) -> ({},{}) *".format(self.name, self.x, self.y, location[0], location[1]))
                self.breed_clock = self.breed_time
                self.island.grid[location[0]][location[1]] = self.__class__(self.island, x=location[0], y=location[1])


class Prey(Animal):
    ''' This is the prey class which is a specialisation of animal.
    '''

    def __init__(self, island, x=0, y=0, s="O"):
        # Note this idiom for invoking the super class initializer. It could be considered more generic and therefore
        # slightly more elegant than the invoking this by the superclass name. Note that you don't need self with this.
        super().__init__(island, x, y, s)

        # breed_clock is the local counter. It gets its initial value from breed_time which doesn't change.
        self.breed_clock = Prey.breed_time

        # Keep track of overall population
        Prey.population += 1


class Predator(Animal):
    ''' This is the predator class, a specialisation of animal.
    '''

    def __init__(self, island, x=0, y=0, s="X"):
        super().__init__(island, x, y, s)
        # starveClock is the local counter. It gets its initial value from starveTime which doesn't change.
        self.starve_clock = Predator.starve_time
        # breed_clock is the local counter. It gets its initial value from breed_time which doesn't change.
        self.breed_clock = Predator.breed_time

        # Keep track of overall population
        Predator.population += 1


    def update_state(self):
        '''Update state variables such as breed clock and starve clock, Prey only updates its local breed clock
        '''
        Animal.update_state(self)

        if self.starve_clock <= 0:
            # Predator starves to death
            print("{} ({},{}) -> ***** +".format(self.name, self.x, self.y))
            self.island.remove(self)
            # self.island.grid[self.x][self.y] = 0
            Predator.population -= 1


    def eat(self):
        ''' Predator looks in one of the 8 adjacent locations for Prey. If found moves to that location,
        updates the starve clock, removes the Prey.
        '''
        if not self.moved:
            location = self.check_grid(Prey)
            if location:
                print("{} ({},{}) -> ({},{}) +".format(self.name, self.x, self.y, location[0], location[1]))
                self.island.remove(self)
                # self.island.grid[self.x][self.y] = 0  # remove from current spot
                self.x = location[0]  # new coordinates
                self.y = location[1]
                self.island.register(self)
                # self.island.grid[self.x][self.y] = self
                self.starve_clock = Predator.starve_time
                self.moved = True
                Prey.population -= 1
            else:
                # Failure to eat
                self.starve_clock -= 1


#
# The program runs from here
#

@my_timer
def main_cui():
    ''' Main simulation. Sets defaults, runs event loop, plots at the end
    '''

    # Initial values. User can change these.
    PREDATOR_BREED_TIME = 6
    # No. of clock ticks or runs through the loop a predator must wait before it can breed
    PREY_BREED_TIME = 3
    # No. of clock ticks or runs through the loop a prey must wait before it can breed
    PREDATOR_STARVE_TIME = 3
    # Predator must eat within this no. of ticks or starve
    NUMBER_PREDATORS = 30
    # Initial no. of predators on the island
    NUMBER_PREY = 150
    # Initial no. of prey on the island
    GRID_SIZE = 60
    # Size of the island - it will be a square 2x2 grid
    CLOCK_TICKS = 500
    # No. of clock ticks or times we go around the main loop
    MOVE_ATTEMPTS = 10
    # No. of attempts to find an adjacent space to move/breed/eat

    # Class variables - these values apply to all objects of the class.
    Animal.move_attempts = MOVE_ATTEMPTS
    Predator.breed_time = PREDATOR_BREED_TIME
    Predator.starve_time = PREDATOR_STARVE_TIME
    Prey.breed_time = PREY_BREED_TIME

    # Population class variables
    Predator.population = 0
    Prey.population = 0

    # Maintain lists of population cycles. Can be used later for graphing
    predator_list = []
    prey_list = []


    # Make an island
    my_island = Island(GRID_SIZE, NUMBER_PREY, NUMBER_PREDATORS)


    # event loop.
    # For all the ticks, for every x,y location.
    # If there is an animal there, try eat, move, breed and clockTick
    for i in range(CLOCK_TICKS):
        print(my_island)
        print("Predator population: {}, Prey population: {}".format(Predator.population, Prey.population))
        # important to clear all the moved flags!
        my_island.clear_all_moved_flags()

        # Get everyone to move if possible.
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if isinstance(my_island.grid[x][y], Animal):
                    animal = my_island.grid[x][y]

                    # For now the only method that works is move(). We can of course 'run' the others even they don't
                    # DO anything (yet!)
                    if isinstance(animal, Predator):
                        animal.eat()
                    animal.move()
                    animal.breed()
                    animal.update_state()

        prey_list.append(Prey.population)
        predator_list.append(Predator.population)

        if Prey.population == 0:
            print("Lost Prey population, quitting...")
            break
        if Predator.population == 0:
            print("Lost Predator population, quitting...")
            break


    # State of the island at the end of the run
    print(my_island)
    print("Ran for {} clock ticks. Predator population: {}, Prey population: {}".format(i + 1, Predator.population,
                                                                                        Prey.population))

    plt.plot(prey_list)
    plt.plot(predator_list)
    # plt.show()
    filename = ".cache/pred_prey_plot_{}.svg".format(random.randint(0,999999))
    plt.savefig(filename)


def main_pygame():
    ''' Main simulation. Sets defaults, runs event loop, plots at the end
    '''

    # Initial values. User can change these.
    PREDATOR_BREED_TIME = 6
    # No. of clock ticks or runs through the loop a predator must wait before it can breed
    PREY_BREED_TIME = 3
    # No. of clock ticks or runs through the loop a prey must wait before it can breed
    PREDATOR_STARVE_TIME = 3
    # Predator must eat within this no. of ticks or starve
    NUMBER_PREDATORS = 15
    # Initial no. of predators on the island
    NUMBER_PREY = 80
    # Initial no. of prey on the island
    GRID_SIZE = 65
    # Size of the island - it will be a square 2x2 grid
    CLOCK_TICKS = 500
    # No. of clock ticks or times we go around the main loop
    MOVE_ATTEMPTS = 10
    # No. of attempts to find an adjacent space to move/breed/eat

    # Class variables - these values apply to all objects of the class.
    Animal.move_attempts = MOVE_ATTEMPTS
    Predator.breed_time = PREDATOR_BREED_TIME
    Predator.starve_time = PREDATOR_STARVE_TIME
    Prey.breed_time = PREY_BREED_TIME

    # Population class variables
    Predator.population = 0
    Prey.population = 0

    # Maintain lists of population cycles. Can be used later for graphing
    predator_list = []
    prey_list = []

    # Make an island
    my_island = Island(GRID_SIZE, NUMBER_PREY, NUMBER_PREDATORS)

    # Size in pixels of each grid square
    ELEMENT_SIZE = 10

    SCREEN_WIDTH = GRID_SIZE * ELEMENT_SIZE
    SCREEN_HEIGHT = (GRID_SIZE * ELEMENT_SIZE) + 50

    # Define the colors we will use in RGB format
    BLACK = (  0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (  0, 0, 255)
    GREEN = (  0, 255, 0)
    RED = (255, 0, 0)

    animal_colour = {'Predator': RED, 'Prey': GREEN}

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Predator/Prey Simulation')
    msg_font = pygame.font.Font('/usr/share/fonts/truetype/abyssinica/AbyssinicaSIL-Regular.ttf',15)

    for i in range(CLOCK_TICKS):
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)

        # All drawing code happens inside the main loop.
        screen.fill(WHITE)

        my_island.clear_all_moved_flags()

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                pygame.draw.rect(screen, BLACK, [x * ELEMENT_SIZE, y * ELEMENT_SIZE, ELEMENT_SIZE, ELEMENT_SIZE], 1)
                if isinstance(my_island.grid[x][y], Animal):
                    animal = my_island.grid[x][y]
                    if isinstance(animal, Predator):
                        colour = animal_colour['Predator']
                        animal.eat()
                    else:
                        colour = animal_colour['Prey']

                    animal.move()
                    animal.breed()
                    animal.update_state()

                    pygame.draw.rect(screen, colour, [(x * ELEMENT_SIZE)+1, (y * ELEMENT_SIZE)+1, ELEMENT_SIZE-2, ELEMENT_SIZE-2])

        msg = "Tick: {}. Predator population: {}, Prey population: {}".format(i + 1, Predator.population,Prey.population)
        msg_line = msg_font.render(msg,False,BLUE)
        msg_rect = msg_line.get_rect()
        msg_rect.topleft = (50, SCREEN_HEIGHT-30)
        screen.blit(msg_line, msg_rect)

        pygame.display.flip()

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                quit_game(i)
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    quit_game(i)

        prey_list.append(Prey.population)
        predator_list.append(Predator.population)

        if Prey.population == 0:
            print("Lost Prey population, quitting...")
            break
        if Predator.population == 0:
            print("Lost Predator population, quitting...")
            break

    quit_game(i)


def quit_game(i):
    print("Ran for {} clock ticks. Predator population: {}, Prey population: {}".format(i + 1, Predator.population,
                                                                                        Prey.population))
    pygame.quit()

    # plt.plot(prey_list)
    # plt.plot(predator_list)
    # # plt.show()
    # filename = ".cache/pred_prey_plot_{}.svg".format(random.randint(0,999999))
    # plt.savefig(filename)


    sys.exit()


if __name__ == "__main__":
    '''When the Python interpreter reads a source file, it executes all of the code found in it. Before
    executing the code, it will define a few special variables. For example, if the python interpreter
    is running that module (the source file) as the main program, it sets the special __name__ variable
    to have a value "__main__". If this file is being imported from another module, __name__ will be set
    to a different value. For example, this means that you can import to IDLE and run functions separately
    which may be useful for testing'''
    main_pygame()
    # main_cui()
