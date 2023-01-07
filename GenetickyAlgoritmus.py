import time
from random import choices, randint, randrange, random, sample, choice
from typing import List, Tuple
import math


class city:
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


Genome = List[city]
Population = List[Genome]

# creating new object of the list[city] type with the same values
def clone_list(starter: Genome) -> Genome:
    new_cities = []
    for c in starter:
        new = city(c.get_x(), c.get_y())
        new.set_num(c.get_num())
        new_cities.append(new)
    return new_cities

# get the fitness value to be the first city of the list
def check_first_city(c: city) -> int:
    y = 200 - c.get_y()
    x = 200 - c.get_x()
    return x+y


def generate_cities(length: int, x: int, y: int) -> List[city]:
    c = []
    for Y in range(y):  # generating every possible position for city
        for X in range(x):
            c.append(city(X, Y))
    # randomly choosing cities from the map XxY km
    cities = sample(c, k=length)  # randomly choosing k cities that do not repeat

    temp = []
    temp = sorted(
        cities,
        key=lambda ci: check_first_city(ci),
        reverse=True
    )
    # setting the closest city to the 0,0 pint the first city of the list
    cities = swap_obj(cities, cities[0], temp[0])
    n = 1
    for i in cities:
        i.set_num(n)
        n += 1
    return cities


def generate_genome(cities: List[city]) -> Genome:
    new_cities = clone_list(cities)  # cloning a list with same values but new objects
    variations = new_cities[1:]  # creating a list where the starting and the ending are the same
    res = [new_cities[0]]
    # randomly choosing cities from the list of the generated cities
    res += sample(variations, k=len(variations))
    return res


def generate_population(size: int, cities: List[city]) -> Population:
    return [generate_genome(cities) for _ in range(size)]


# function to find distance between two selected cities
def calculate_dist(start: city, finish: city) -> float:
    # we find the distance between two cities using the Pythagorean theorem
    cat1 = finish.get_x() - start.get_x()
    cat2 = finish.get_y() - start.get_y()
    hypo = cat1 ** 2 + cat2 ** 2
    return abs(math.sqrt(hypo))


def fitness(genome: Genome) -> float:
    distance = 0
    # basically find distance between current and next city and just add it to the sum of the distances
    for i, c in enumerate(genome):
        if i == int(len(genome) - 1):
            break
        else:
            distance += calculate_dist(c, genome[i + 1])

    return distance


def swap_obj(cities: Genome, city1: city, city2: city) -> Genome:
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


def cycle_crossover(a: Genome, b: Genome) -> Genome:
    num_a = []
    num_b = []
    used_i = [1]
    indexes = [0]
    res = [a[0]]
    index = 1
    cycle_ended = False

    for i in range(len(a)):
        num_a.append(a[i].get_num())
        num_b.append(b[i].get_num())

    for p in range(len(a)-1):

        indexes.append(index)  # add index to the used indexes
        if not cycle_ended:  # if we didn't finish our first cycle of substitution of the cities
            used_i.append(a[index].get_num())  # add added city to the list of used cities
            res.insert(index, a[index])  # then add city with the index we found
            index = num_a.index(b[index].get_num())  # find index of the city from the opposite genome in current genome
            if a[index].get_num() in used_i:  # if founded city has already been substituted
                index = 1  # then we set index to the beginning
                while index in indexes:  # if index was used then we seek for the first unused
                    index += 1
                cycle_ended = True  # and set cycle of substitution as finished
        else:  # if cycle of substitution haas been finished
            used_i.append(b[index].get_num())  # add added city to the list of used cities
            res.insert(index, b[index])  # then we add to our result genome for all of the
            # free positions cities from the b genome
            while index in indexes:
                index += 1
    return res


def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))  # randomly choose first index
        while index == 0 or index == len(genome):  # if it doesn't fit our specific conditions - repick it
            index = randrange(len(genome))
        if index == 1:
            index2 = 2
        elif index == len(genome)-1:
            index2 = index - 1
        else:
            # choose second index randomly and check if it isn't equal to first one
            index2 = randrange(len(genome))
            while index2 == 0 or index2 == len(genome) or index2 == index:
                index2 = randrange(len(genome))

        if random() <= probability:
            # swap cities with the probability of the 50%
            genome = swap_obj(genome, genome[index], genome[index2])

    return genome

# simple function for parsing cities permutation to the string in the correct form
def genome_to_cities(genome: Genome) -> List[str]:
    res = []
    for i, c in enumerate(genome):
        s = str(c.get_num()) + ": " + str(c.get_x()) + ", " + str(c.get_y())
        res.append(s)
    return res


def run_evolution(cities: List[city], generation_limit: int, type_of_selection: bool) -> Tuple[Genome, list[int]]:
    start_ev = time.time()
    end_ev = 0
    fitness_stats = []
    population = generate_population(10, cities)
    elitis = int((len(population[0]) / 100) * 15)
    max_way = 0
    best_way = fitness(population[0])
    best_gen = 0
    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda genome: fitness(genome),
            reverse=False
        )
        if i % 300 == 0:
            fitness_stats.append(int(fitness(population[0])))
        if max_way < fitness(population[len(population) - 1]):
            max_way = fitness(population[len(population) - 1])
        if best_way > fitness(population[0]):
            best_way = fitness(population[0])
            best_gen = i
            end_ev = time.time() - start_ev

        next_generation = []
        for u in range(elitis):
            next_generation.append(clone_list(population[u]))

        for j in range((len(population) - elitis)):
            parent1 = population[0]
            parent2 = population[j + 1]
            offspring_a = cycle_crossover(parent1, parent2)
            offspring_a = mutation(offspring_a)
            # in default type of selection we are taking offspring without a check
            if type_of_selection is True:  # but in different type of selection where we are comparing mutated parent2
                offspring_b = mutation(parent2)  # to the crossed over and mutated offspring to select the best of them
                if fitness(offspring_b) < fitness(offspring_a):  # the best genome remains
                    offspring_a = offspring_b
            next_generation.append(offspring_a)

        population = next_generation

    population = sorted(
        population,
        key=lambda genome: fitness(genome),
        reverse=False
    )
    population[0].append(population[0][0])

    print(f'starting list of the cities: {genome_to_cities(cities)}')
    print(f"number of generations: {int(generation_limit)}")
    print(f"number of cities: {int(len(population[0]) - 1)}")
    print(f"distance of the slowest solution in km: {int(max_way)}")
    print(f"distance of the solution without the last city in km: {int(best_way)}")
    print(f"distance of the solution in km: {int(fitness(population[0]))}")
    print(f"solution has been found in: {end_ev} seconds on generation number {best_gen}")
    print(f"the best solution: {genome_to_cities(population[0])}")

    print("\n=============================\n=============================\n")

    return population[0], fitness_stats






