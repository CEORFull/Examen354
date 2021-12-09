import numpy as np, random, operator, pandas as pd
import array
import json

#Create class to handle "cities"

class Location:
    def __init__(self,x):
        self.x = x
    
    
    def distanceCalculator(self, loc, distances):
        distance = distances[self.x][loc.x]
        return distance
    
    def __repr__(self):
        return "(" + str(self.x) + ")"
    
    #Create a fitness function

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self, distances):
        if self.distance ==0:
            rDist = 0
            if self.route[0].x == 0:
                for i in range(0, len(self.route)):
                    fromCity = self.route[i]
                    toCity = None
                    if i + 1 < len(self.route):
                        toCity = self.route[i + 1]
                    else:
                        toCity = self.route[0]
                    rDist += fromCity.distanceCalculator(toCity, distances)
                self.distance = rDist
            
                return self.distance
            else:
                return 1000
            
    
    def routeFitness(self, distances):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance(distances))
        return self.fitness
    
    #Create our initial population
#Route generator
#This method randomizes the order of the cities, this mean that this method creates a random individual.
def createRoute(locList):
    route = random.sample(locList, len(locList))
    return route


#Create first "population" (list of routes)
#This method created a random population of the specified size.

def initialPopulation(popSize, locList):
    population = []
    
    for i in range(0, popSize):
        population.append(createRoute(locList))
    
        
    return population


#Create the genetic algorithm
#Rank individuals
#This function takes a population and orders it in descending order using the fitness of each individual
def rankRoutes(population, distances):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness(distances)
    return sorted(fitnessResults.items(), reverse=True)



#Create a selection function that will be used to make the list of parent routes

def routeSelection(populationRank, elitismSize):
    selectedRoutes = []
    df = pd.DataFrame(np.array(populationRank), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, elitismSize):
        selectedRoutes.append(populationRank[i][0])
        
    for i in range(0, len(populationRank) - elitismSize):
        fixedPointer = 100 * random.random()
        for i in range(0, len(populationRank)):
            if fixedPointer <= df.iat[i,3]:
                selectedRoutes.append(populationRank[i][0])
                break

    return selectedRoutes



#Create mating pool

def matingPool(population, selectedRoutes):
    matingpool = []
    
    for i in range(0, len(selectedRoutes)):
        index = selectedRoutes[i]
        matingpool.append(population[index])
        
    return matingpool




#Create a crossover function for two parents to create one child
def breed(parent1, parent2):
    child = []
    subchild1 = []
    subchild2 = []
    
    gene1 = int(random.random() * len(parent1))
    gene2 = int(random.random() * len(parent1))
    
    startPoint = min(gene1, gene2)
    endPoint = max(gene1, gene2)

    for i in range(startPoint, endPoint):
        subchild1.append(parent1[i])
        
    for i in parent2:
        if i not in subchild1:
            subchild2.append(i)
            
    child = subchild1 + subchild2
    return child

#Create function to run crossover over full mating pool

def breedPopulation(matingpool, elitismSize):
    children = []
    fillerLength = len(matingpool) - elitismSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,elitismSize):
        children.append(matingpool[i])
    
    for i in range(0, fillerLength):
        children.append(breed(pool[i], pool[len(matingpool)-i-1]))
    return children




#Create function to mutate a single route
def mutation(individual, mutationRate):
    for swap in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swap]
            city2 = individual[swapWith]
            
            individual[swap] = city2
            individual[swapWith] = city1
    return individual



#Create function to run mutation over entire population

def mutationPopulation(population, mutationRate):
    mutatedPopulation = []
    
    for individual in range(0, len(population)):
        mutatedIndividual = mutation(population[individual], mutationRate)
        mutatedPopulation.append(mutatedIndividual)
    return mutatedPopulation



#Put all steps together to create the next generation

def createNewGeneration(currentPopulation, elitismSize, mutationRate, distances):
    populationRanked = rankRoutes(currentPopulation,distances)
    selectionResults = routeSelection(populationRanked, elitismSize)
    matingpool = matingPool(currentPopulation, selectionResults)
    children = breedPopulation(matingpool, elitismSize)
    nextGeneration = mutationPopulation(children, mutationRate)
    return nextGeneration


#Final step: create the genetic algorithm

def implementGeneticAlgorithm(population, populationSize, elitismSize, mutationRate, generations, distances):
    pop = initialPopulation(populationSize, population)
    print("Distancia inicial> " + str(1/rankRoutes(pop, distances)[0][1]) )
    progress = []
    
    progress.append(1/rankRoutes(pop, distances)[0][1])
    
    for i in range(0, generations):
        pop = createNewGeneration(pop, elitismSize, mutationRate, distances)
        while pop[rankRoutes(pop, distances)[0][0]][0].x != 0:
            pop = createNewGeneration(pop, elitismSize, mutationRate, distances)
        

        progress.append(1 / rankRoutes(pop,distances)[0][1])
        print('Generación ' + str(i) + " Distancia mínima: " + str(progress[i]) + " Recorrido: " + str(pop[rankRoutes(pop, distances)[0][0]]))
        
    print("Distancia final: " + str(1/rankRoutes(pop, distances)[0][1]))
    bestRouteIndex = rankRoutes(pop, distances)[0][0]
    bestRoute = pop[bestRouteIndex]
    print("-----------------------------------")
    print(bestRoute)
    print("-----------------------------------")
    print(progress)

#Running the genetic algorithm
#Create list of cities

with open("matriz.json", "r") as tsp_data:
    agente = json.load(tsp_data)
    
locList = []

distancias = agente["Distancias"]
IND_SIZE = agente["Cantidad"]



for i in range(IND_SIZE):
    locList.append(Location(i))
    
print (locList)
implementGeneticAlgorithm(population=locList, populationSize=100, elitismSize=20, mutationRate=0.02, generations=50, distances = distancias)