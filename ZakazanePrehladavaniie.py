from random import choices, randint, randrange, random, sample, choice
from typing import List, Tuple
import math


class city:
    # num is the serial number of the city, we set it when cities are being generated
    num = int()
    x = int()
    y = int()

    def set_num(self, num):
        self.num = num

    def get_num(self):
        return self.num

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def __init__(self, x, y):
        self.set_y(y)
        self.set_x(x)


Cities = List[city]


# creating new object of the list[city] type with the same values
def clone_list(starter: Cities) -> Cities:
    new_cities = []
    for c in starter:
        new_cities.append(c)
    return new_cities


# function to find distance between two selected cities
def calculate_dist(start: city, finish: city) -> float:
    cat1 = abs(finish.get_x() - start.get_x())
    cat2 = abs(finish.get_y() - start.get_y())
    hypo = (cat1**2) + (cat2**2)
    return abs(math.sqrt(hypo))


# function to find the fitness value of the whole way
def sol_fitness(v: Cities) -> float:
    distance = 0

    for i, c in enumerate(v):
        if i == int(len(v) - 1):
            break
        else:
            distance += calculate_dist(c, v[i+1])

    return distance


def find_best(starter: city, cities: Cities, banned: Cities, banned_limit: int) -> Tuple[city, int]:
    best_dist = sol_fitness(cities) * 10
    best_city = cities[0]
    # in cycle, we are checking every city from the list
    for i in cities:
        # if the city is banned then we just skip this iteration of the cycle
        if i in banned or i == starter:
            continue
        # else we calculate distance to that city and if it is shorter than the shortest distance - we substitute it
        else:
            new_dist = calculate_dist(starter, i)
            if best_dist > new_dist:
                best_dist = new_dist
                best_city = i
    # after we found the best result - we add it to the banned list
    banned.append(best_city)
    if len(banned) > ((len(cities)/100)*banned_limit):  # if list is bigger then the limit - we pop the first element
        banned.pop(0)
    return best_city, int(best_dist)


def swapPositions(cities: Cities, city1: city, city2: city) -> Cities:
    if city1 == city2:
        return cities
    # popping both the elements from list
    first_ele = cities.index(city1)
    second_ele = cities.index(city2)
    cities.remove(city1)
    cities.remove(city2)

    # inserting in each other positions
    cities.insert(first_ele, city2)
    cities.insert(second_ele, city1)

    return cities


# simple function for parsing cities permutation to the string in the correct form
def var_to_cities(v: Cities) -> List[str]:
    res = []
    for i, c in enumerate(v):
        s = str(c.get_num()) + ": " + str(c.get_x()) + ", " + str(c.get_y())
        res.append(s)
    return res


def run_tabu_search(cities: Cities, banned_limit: int) -> Tuple[Cities, list[int]]:

    f_stats = []
    banned = [cities[0]]
    for i in range(len(cities)-1):
        # best - is the best found city with the shortest distance to our actual city
        # fit - is the distance between actual city and the best
        best, fit = find_best(cities[i], cities, banned, banned_limit)
        f_stats.append(fit)
        # after we found city to swap - swap it with the next city of the actual city
        cities = swapPositions(cities, cities[i+1], best)
    cities.append(cities[0])

    print(f'starting list of the cities: {var_to_cities(cities)}')
    print(f"number of cities: {int(len(cities) - 1)}")
    print(f"distance of the solution in km: {int(sol_fitness(cities))}")
    print(f"the best solution: {var_to_cities(cities)}")

    return cities, f_stats



