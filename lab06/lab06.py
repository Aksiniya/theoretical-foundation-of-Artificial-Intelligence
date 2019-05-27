import json
import math
import random

class Coordinate():
    def __init__(self, coordinate_X, coordinate_Y):
        self.coordinate_X = coordinate_X
        self.coordinate_Y = coordinate_Y

    def distance(self, other_coordinate):
        return math.sqrt((other_coordinate.coordinate_X - self.coordinate_X)**2 + (other_coordinate.coordinate_Y - self.coordinate_Y)**2)

class Object_in_map:
    def __init__(self, name, coordinate):
        self.name = name
        self.coordinate = coordinate

    def print(self):
        print(self.name, self.coordinate.coordinate_X, self.coordinate.coordinate_Y)

def embassy_deserialization(full_path_to_json):
    with open(full_path_to_json, "r",  encoding = "Windows-1251") as read_file:
        data = json.load(read_file)
    clusters = []
    for embassy in data:
        coordinates = Coordinate(embassy["geoData"]["coordinates"][0],embassy["geoData"]["coordinates"][1])
        clusters.append(Object_in_map(embassy["Name"], coordinates))
    return clusters

def parking_deserialization(full_path_to_json, limit):
    with open(full_path_to_json, "r",  encoding = "Windows-1251") as read_file:
        data = json.load(read_file)
    parkings = []
    current_index = 0

    # Получить рандомные индексы таким образом, чтобы они не повторялись.
    parking_rand_indexes = {}
    while (len(parking_rand_indexes) < limit):
        parking_rand_indexes[random.randint(0, len(data)-1)] = "_"
        
    for parking_index in parking_rand_indexes.keys():
        if (current_index >= limit):
            break
        coordinates = Coordinate(data[parking_index]["geoData"]["center"][0][0],data[parking_index]["geoData"]["center"][0][1])
        parkings.append(Object_in_map(data[parking_index]['ParkingName'], coordinates))
        # print (data[parking_index])
        current_index += 1
    return parkings
