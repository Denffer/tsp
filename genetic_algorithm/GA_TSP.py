import math, sys, matplotlib, random
import matplotlib.pyplot as plt

class City:
    def __init__(self, n, x, y):
        self.city_index = n
        self.x = x
        self.y = y

    def get_city_index(self):
        return self.city_index

    def get_X(self):
        return self.x

    def get_Y(self):
        return self.y

    def distanceTo(self, city):
        x_Distance = abs(self.get_X() - city.get_X())
        y_Distance = abs(self.get_Y() - city.get_Y())
        distance = math.sqrt( (x_Distance*x_Distance) + (y_Distance*y_Distance) )
        return distance

    def __repr__(self):
        #return " " + str(int(self.city_index)) + ":[" + str(self.get_X()) + "," + str(self.get_Y()) + "] "
        return str(int(self.city_index))

class TourManager:
   city_list = []

   def addCity(self, city):
      self.city_list.append(city)

   def getCity(self, index):
      return self.city_list[index]

   def numberOfCities(self):
      return len(self.city_list)


class Tour:
   def __init__(self, tourmanager, tour=None):
      self.tourmanager = tourmanager
      self.tour = []
      self.fitness = 0.0
      self.distance = 0
      if tour is not None:
         self.tour = tour
      else:
         for i in range(0, self.tourmanager.numberOfCities()):
            self.tour.append(None)

   def __len__(self):
      return len(self.tour)

   def __getitem__(self, index):
      return self.tour[index]

   def __setitem__(self, key, value):
      self.tour[key] = value

   def __repr__(self):
      geneString = "|"
      for i in range(0, self.tourSize()):
         geneString += str(self.getCity(i)) + "|"
      return geneString

   def generateIndividual(self):
      for cityIndex in range(0, self.tourmanager.numberOfCities()):
         self.setCity(cityIndex, self.tourmanager.getCity(cityIndex))
      random.shuffle(self.tour)

   def getCity(self, tourPosition):
      return self.tour[tourPosition]

   def setCity(self, tourPosition, city):
      self.tour[tourPosition] = city
      self.fitness = 0.0
      self.distance = 0

   def getFitness(self):
      if self.fitness == 0:
         self.fitness = 1/float(self.getDistance())
      return self.fitness

   def getDistance(self):
      if self.distance == 0:
         tourDistance = 0
         for cityIndex in range(0, self.tourSize()):
            fromCity = self.getCity(cityIndex)
            destinationCity = None
            if cityIndex+1 < self.tourSize():
               destinationCity = self.getCity(cityIndex+1)
            else:
               destinationCity = self.getCity(0)
            tourDistance += fromCity.distanceTo(destinationCity)
         self.distance = tourDistance
      return self.distance

   def tourSize(self):
       return len(self.tour)

   def containsCity(self, city):
       return city in self.tour


class Population:
   def __init__(self, tourmanager, populationSize, initialise):
       self.tours = []
       for i in range(0, populationSize):
           self.tours.append(None)

       if initialise:
           for i in range(0, populationSize):
               newTour = Tour(tourmanager)
               newTour.generateIndividual()
               self.saveTour(i, newTour)

   def __setitem__(self, key, value):
       self.tours[key] = value

   def __getitem__(self, index):
       return self.tours[index]

   def saveTour(self, index, tour):
       self.tours[index] = tour

   def getTour(self, index):
       return self.tours[index]

   def getFittest(self):
       fittest = self.tours[0]
       for i in range(0, self.populationSize()):
          if fittest.getFitness() <= self.getTour(i).getFitness():
             fittest = self.getTour(i)
       return fittest

   def populationSize(self):
       return len(self.tours)

class GA:
    def __init__(self, tourmanager):
        self.tourmanager = tourmanager
        self.mutationRate = 0.1
        self.tournamentSize = 100
        self.elitism = True

    def evolvePopulation(self, pop):
        newPopulation = Population(self.tourmanager, pop.populationSize(), False)
        elitismOffset = 0
        if self.elitism:
           newPopulation.saveTour(0, pop.getFittest())
           elitismOffset = 1

        for i in range(elitismOffset, newPopulation.populationSize()):
           parent1 = self.tournamentSelection(pop)
           parent2 = self.tournamentSelection(pop)
           child = self.crossover(parent1, parent2)
           newPopulation.saveTour(i, child)

        for i in range(elitismOffset, newPopulation.populationSize()):
           self.mutate(newPopulation.getTour(i))

        #print newPopulation.__dict__
        return newPopulation

    def crossover(self, parent1, parent2):
        child = Tour(self.tourmanager)

        #print "parent1:", parent1
        startPos = 11 # 12-1
        endPos = 23 # 24-1

        #print "parent1:", parent1
        #print "parent2:", parent2
        for i in range(0, child.tourSize()):
            if i >= startPos and i < endPos:
                child.setCity(i, parent1.getCity(i))
        #print child
        for i in range(0, parent2.tourSize()):
           if not child.containsCity(parent2.getCity(i)):
              for ii in range(0, child.tourSize()):
                 if child.getCity(ii) == None:
                    child.setCity(ii, parent2.getCity(i))
                    break
        #print child
        #print "-"*50
        return child

    # Insertion Muation
    def mutate(self, tour):

        mutation_list = []
        target_list = []

        for city_index in range(0, tour.tourSize()):
            if random.random() < self.mutationRate:
                mutation_list.append(city_index)
            else:
                target_list.append(city_index)

        for mutation in mutation_list:
            # insert to random place
            insert_position = int(len(target_list) * random.random())
            target_list.insert(insert_position, mutation)

        # get new city_list
        city_list = []
        for i in range(0, len(target_list)):
            city = tour.getCity(target_list[i])
            city_list.append(city)
        # set new city_list
        index = 0
        for city in city_list:
            tour.setCity(index, city)
            index += 1

    def tournamentSelection(self, pop):
        tournament = Population(self.tourmanager, self.tournamentSize, False)
        for i in range(0, self.tournamentSize):
           randomId = int(random.random() * pop.populationSize())
           tournament.saveTour(i, pop.getTour(randomId))
        fittest = tournament.getFittest()
        #print fittest
        return fittest

class DataLoader:
    def __init__(self):
        self.src = sys.argv[1]
        self.city_xy_list = []

    def get_source(self):
        with open(self.src, "r") as f:
            file_data = f.readlines()

        for line in file_data:
            line = line.strip().split(" ")
            line = [x for x in line if x != ""]
            self.city_xy_list.append([float(line[0]),float(line[1]), float(line[2])])

        return self.city_xy_list

class Plot:
    """ Plot output """

    def graph(self, distance_list):
        """ 20 generations as x-axis | total distance as y-axis """
        fig = plt.figure()
        plt.title("Genetic Algorithm Result")
        plt.xlabel("Generation")
        plt.ylabel("Total Distance")

        generation_index = [i for i in range(1,21)]
        line = plt.plot( generation_index, distance_list, color='navy', ls='-')

        # plot background lines
        ax = plt.gca()
        ax.yaxis.grid(color='gray', linestyle='--')

        #plt.legend(handles = [line1[0]], loc='best', numpoints=1)
        print "Saving graph to", "\033[1m" + "ga_result" + str(5) + ".png" + "\033[0m"
        print "-"*50
        fig.savefig("ga_result.png")

if __name__ == '__main__':
    """ program entry point """

    # Initalize tour
    tourmanager = TourManager()

    # Load data from data/bayg29.txt
    dataLoader = DataLoader()
    city_xy_list = dataLoader.get_source()

    # Create and add cities
    for city in city_xy_list:
        city = City(city[0], city[1], city[2])
        tourmanager.addCity(city)

    # Initialize population
    population = Population(tourmanager, 40, True);
    print "Initial distance: " + str(population.getFittest().getDistance())

    # Evolve population for 20 generations
    distance_list = []
    ga = GA(tourmanager)
    population = ga.evolvePopulation(population)
    for i in range(1, 21):
        population = ga.evolvePopulation(population)
        print "Generation", i, ":", str(population.getFittest()), "| Distance: " + str(population.getFittest().getDistance())
        distance_list.append(population.getFittest().getDistance())

    # Print final results
    print "Final distance: " + str(population.getFittest().getDistance())
    print "-"*50
    print "Solution:"
    print population.getFittest()
    print "-"*50

    # plot results
    plot = Plot()
    plot.graph(distance_list)

