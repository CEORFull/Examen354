import array
import random
import json

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


with open("matriz.json", "r") as tsp_data:
    agente = json.load(tsp_data)

distance_map = agente["Distancias"]
IND_SIZE = agente["Cantidad"]

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def agenteViajero(individual):
    if individual[0] == 0 and individual[-1] == 5:
        distance = distance_map[individual[-1]][individual[0]]
        for gene1, gene2 in zip(individual[0:-1], individual[1:]):
            distance += distance_map[gene1][gene2]
            
        return distance,
    else:
        return 1000,

toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", agenteViajero)

def main():
    random.seed(200)

    pop = toolbox.population(n=1000)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 50, stats=stats, 
                        halloffame=hof)

    return pop, stats, hof

if __name__ == "__main__":
        pop, stats, hof = main()
        print("El viajero debe seguir la ruta: ")
        print(f'{agente[f"{hof[0][0]}"]}-{agente[f"{hof[0][1]}"]}-{agente[f"{hof[0][2]}"]}-{agente[f"{hof[0][3]}"]}-{agente[f"{hof[0][4]}"]}-{agente[f"{hof[0][5]}"]}')
        print(f"Para caminar solo {agenteViajero(hof[0])[0]} km")
    