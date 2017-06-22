import os, sys, re, math
import numpy as np

class Greedy:
    """ This program aims to calculate the distance among cities by greedy method"""

    def __init__(self):
        self.src_cities = sys.argv[1]
        self.entry_point = 19
        self.path = []
        self.cities = []
        self.dst = "result.txt"

    def get_city_list(self):
        """ Get cities from argv[1] """

        with open(self.src_cities, "r") as f:
            content = f.readlines()

        city_list = []
        for line in content:
            line = line.strip().split(" ")
            line = [x for x in line if x != ""]
            city_list.append({int(line[0]): [float(line[1]), float(line[2])]})

        #print city_list
        return city_list

    def run(self):
        """ initialize """
        city_list = self.get_city_list()
        entry_dict = city_list[self.entry_point-1]
        city_list.pop(self.entry_point-1)

        self.greedy(city_list, entry_dict)

    def greedy(self, city_list, entry_dict):
        """ core """

        cordinate = entry_dict.values()
        x1 = cordinate[0][0]
        y1 = cordinate[0][1]

        current_city = entry_dict.keys()[0]
        shortest_path = 0
        for city_dict in city_list:
            city_num = str(city_dict.keys()[0])
            # print "Calculating the distance between city" + city_num + " and city" + str(current_city)
            cordinate = city_dict.values()
            x2 = cordinate[0][0]
            y2 = cordinate[0][1]

            distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            if shortest_path == 0:
                shortest_path = distance
                shortest_city = city_num
            elif distance < shortest_path:
                shortest_path = distance
                shortest_city = city_num
            else:
                pass

        self.path.append(shortest_path)
        self.cities.append(shortest_city)
        print "Shortest City:", shortest_city, "| Shortest distance:", shortest_path
        for city in city_list:
                if int(shortest_city) == int(city.keys()[0]):
                    entry_dict = city
                    index = city_list.index(city)
                    city_list.pop(index)

        #print city_list
        if len(city_list) > 0:
            self.greedy(city_list, entry_dict)

    def render(self):
        """ print result """
        print "Path:", self.path
        print "Total Distance:", sum(self.path)
        print "City:", self.cities

if __name__ == '__main__':
    greedy = Greedy()
    greedy.run()
    greedy.render()

