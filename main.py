import sys
import time
from typing import List

from GenetickyAlgoritmus import generate_cities, clone_list, city, fitness, genome_to_cities, \
    run_evolution
from ZakazanePrehladavaniie import run_tabu_search
import matplotlib.pyplot as plt


def draw_graf(cities: List[city]):
    x = []
    y = []
    for i in cities:
        x.append(i.get_x())
        y.append(i.get_y())

    plt.plot(x, y, color='red', linestyle='dashed', linewidth=2,
             marker='o', markersize=6, markerfacecolor='blue',
             markeredgecolor='blue')
    for o in range(len(cities)-1):
        plt.annotate(f"{str(o+1)}: {cities[o].get_num()}", xy=(x[o], y[o]))
    plt.grid()
    plt.show()


def draw_fitness_stats_gen(f_stats: list[int]):
    x = []
    y = []
    for i in range(len(f_stats)):
        x.append(200 * i)
        y.append(f_stats[i])

    plt.plot(x, y, color='red', linestyle='dashed', linewidth=2,
             marker='o', markersize=6, markerfacecolor='blue',
             markeredgecolor='blue')
    for o in range(len(f_stats) - 1):
        plt.annotate(f"{str(y[o])}", xy=(x[o], y[o]))
    plt.grid()
    plt.show()


def draw_fitness_stats_zp(f_stats: list[int]):
    x = []
    y = []
    for i in range(len(f_stats)):
        x.append(i)  # x is the number of the step
        y.append(f_stats[i])  # y is the min distance that tabu search founded for some city

    plt.plot(x, y, color='red', linestyle='dashed', linewidth=2,
             marker='o', markersize=6, markerfacecolor='blue',
             markeredgecolor='blue')
    for o in range(len(f_stats) - 1):
        plt.annotate(f"{str(y[o])}", xy=(x[o], y[o]))
    plt.grid()
    plt.show()


def main():
    # vygenerujeme dve mapy mest, prvu pre 20 mest a prve opakovanie testu
    # druhu pre 30 mest a druhe opakovanie testu
    cities_20 = generate_cities(20, 200, 200)
    cities_30 = generate_cities(30, 200, 200)
    for o in range(2):
        if o == 0:
            print("==================================================\n"
                  "Genetic algorithm tests for 20 cities has been started"
                  "\n=================================================\n")
        else:
            print("==================================================\n"
                  "Genetic algorithm tests for 30 cities has been started"
                  "\n=================================================\n")
        start_gen = time.time()  # zapiseme startovaci cas testovania genetickeho algoritmu
        graph_gen1 = []
        m_stats1 = []
        graph_gen2 = []
        m_stats2 = []
        max_d1 = 99999999
        max_d2 = 99999999
        for i in range(6):
            # prve 3 opakovania sme skusame prvy typ selekcie genetickeho algoritmu
            if i < 3:
                if o == 0:
                    # v dalsom riadku prebehne evolucia riesenia na 20 mest zapiseme vysledky do jednotlivych premennych
                    g_graph, g_stats = run_evolution(cities_20, 20 * 200, False)
                else:
                    g_graph, g_stats = run_evolution(cities_30, 30 * 200, False)
                if max_d1 > fitness(g_graph):
                    max_d1 = fitness(g_graph)
                    graph_gen1 = g_graph
                    m_stats1 = g_stats
            # a druhe 3 opakovania skusame druhy typ selekcie
            else:
                if o == 0:
                    g_graph, g_stats = run_evolution(cities_20, 20 * 200, True)
                else:
                    g_graph, g_stats = run_evolution(cities_30, 30 * 200, True)
                if max_d2 > fitness(g_graph):
                    max_d2 = fitness(g_graph)
                    graph_gen2 = g_graph
                    m_stats2 = g_stats

        # kreslime grafy ku najlepsim rieseniam
        draw_graf(graph_gen1)
        draw_fitness_stats_gen(m_stats1)
        draw_graf(graph_gen2)
        draw_fitness_stats_gen(m_stats2)
        end_gen = time.time() - start_gen

        if o == 0:
            print("==================================================\n"
                  "Genetic algorithm tests for 20 cities has been finished\n"
                  f"Time of the tests in seconds: {end_gen}"
                  "\n=================================================\n")
            print("==================================================\n"
                  "Tabu Search tests for 20 cities has been started"
                  "\n=================================================\n")
        else:
            print("==================================================\n"
                  "Genetic algorithm tests for 30 cities has been finished\n"
                  f"Time of the tests in seconds: {end_gen}"
                  "\n=================================================\n")
            print("==================================================\n"
                  "Tabu Search tests for 30 cities has been started"
                  "\n=================================================\n")


        start_zp = time.time()
        if o == 0:
            cities_tabu = clone_list(cities_20)
            # pre 20 mest zobereme banned list limit 35 percent z celkoveho poctu mest
            banned_limit = 35
        else:
            # pre 30 mest zobereme banned list limit 50 percent z celkoveho poctu mest
            cities_tabu = clone_list(cities_30)
            banned_limit = 50

        # tak isto ako aj geneticky algoritmus skusame pre rozny pocet mest nas algoritmus
        z_graph, z_stats = run_tabu_search(cities_tabu, banned_limit)
        draw_graf(z_graph)
        # draw_fitness_stats_gen(z_stats)
        end_zp = time.time() - start_zp
        #vypiseme vysledky genetickeho algoritmu a zakazaneho prehladavania
        if o == 0:
            print("==================================================\n"
                  "Tabu Search tests for 20 cities has been finished\n"
                  f"Time of the test in seconds: {end_zp}"
                  "\n=================================================\n"
                  f"Drawn Genetic Algorithm (first type) "
                  f"solution distance for 20 cities in km is {int(fitness(graph_gen1))}\n"
                  f"Drawn Genetic Algorithm (first type) "
                  f"solution way for 20 cities is {genome_to_cities(graph_gen1)}\n"
                  f"Drawn Genetic Algorithm (second type) "
                  f"solution distance for 20 cities in km is {int(fitness(graph_gen2))}\n"
                  f"Drawn Genetic Algorithm (second type) "
                  f"solution way for 20 cities is {genome_to_cities(graph_gen2)}\n"
                  f"Drawn Tabu Search solution distance for 20 cities in km is {int(fitness(z_graph))}\n"
                  f"Drawn Tabu Search solution way for 20 cities is {genome_to_cities(z_graph)}\n"
                  )
        else:
            print("==================================================\n"
                  "Tabu Search tests for 30 cities has been finished\n"
                  f"Time of the test in seconds: {end_zp}"
                  "\n=================================================\n"
                  f"Drawn Genetic Algorithm (first type) "
                  f"solution distance for 30 cities in km is {int(fitness(graph_gen1))}\n"
                  f"Drawn Genetic Algorithm (first type) "
                  f"solution way for 30 cities is {genome_to_cities(graph_gen1)}\n"
                  f"Drawn Genetic Algorithm (second type) "
                  f"solution distance for 30 cities in km is {int(fitness(graph_gen2))}\n"
                  f"Drawn Genetic Algorithm (second type) "
                  f"solution way for 30 cities is {genome_to_cities(graph_gen2)}\n"
                  f"Drawn Tabu Search solution distance for 30 cities in km is {int(fitness(z_graph))}\n"
                  f"Drawn Tabu Search solution way for 30 cities is {genome_to_cities(z_graph)}\n"
                  )



if __name__ == "__main__":
    main()

