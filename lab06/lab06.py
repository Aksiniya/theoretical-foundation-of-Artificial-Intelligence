import json
import math
import random

class Coordinate():
    def __init__(self, coordinate_X=0, coordinate_Y=0):
        self.coordinate_X = coordinate_X
        self.coordinate_Y = coordinate_Y

    def distance(self, other_coordinate):
        return math.sqrt((other_coordinate.coordinate_X - self.coordinate_X)**2 + (other_coordinate.coordinate_Y - self.coordinate_Y)**2)

class Object_in_map:
    def __init__(self, name="", coordinate=Coordinate()):
        self.name = name
        self.coordinate = coordinate

    def print(self):
        print(self.name, self.coordinate.coordinate_X, self.coordinate.coordinate_Y)

class Parking_in_map(Object_in_map):
    def __init__(self, name="", coordinate=Coordinate(), cluster_name=""):
        Object_in_map.__init__(self, name=name, coordinate=coordinate)
        self.cluster_name = cluster_name


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
        parkings.append(Object_in_map(data[parking_index]["ParkingName"] + " ( " + data[parking_index]["AdmArea"] + " )", coordinates))
        # print (data[parking_index])
        current_index += 1
    return parkings

class Kohonen_neuron:
    def __init__(self, weights=[], input_set = [], net = 0, cluster=Object_in_map()):
        self.weights = weights 
        self.input_set = input_set
        self.net = net
        self.cluster = cluster        

    def output(self):
        return math.sqrt((self.weights[0] - self.input_set[0])**2 + (self.weights[1] - self.input_set[1])**2)

    def print_weights(self, signs = 1):
        print("[ ", end="")
        for w in self.weights: print("%.{0}f".format(signs) % w, end = " ")
        print("]", end = "")

def competition_function(vector):
    output_binary_vector = []
    min_value = min(vector)
    for _ in vector:
        if (_ == min_value):
            output_binary_vector.append(1)
        else:
            output_binary_vector.append(0)
    return output_binary_vector

def get_output_y_vector(input_set, layer):
    y_vector = []
    for neuron_i in range(len(layer)):
        layer[neuron_i].input_set = input_set
        y_vector.append(layer[neuron_i].output())
    return competition_function(y_vector)

def distrits_deserialization():
    json_districts = {'Центральный административный округ': [55.750000, 37.616670],
                          'Северный административный округ': [55.838384, 37.525765],
                          'Северо-Восточный административный округ': [55.863894, 37.620923],
                          'Восточный административный округ': [55.787710, 37.775631],
                          'Юго-Восточный административный округ': [55.692019, 37.754583],
                          'Южный административный округ': [55.610906, 37.681479],
                          'Юго-Западный административный округ': [55.662735, 37.576178],
                          'Западный административный округ': [55.728003, 37.443533],
                          'Северо-Западный административный округ': [55.829370, 37.451546],
                        #   'Зеленоградский административный округ': [55.987583, 37.194250],
                        #   'Троицкий административный округ': [55.355771, 37.146990],
                        #   'Новомосковский административный округ': [55.558121, 37.370724]
                          }

    districts = []
    for key in json_districts.keys():
        coord = Coordinate(json_districts[key][1], json_districts[key][0])
        districts.append(Object_in_map(key, coord))
    return districts


def main():
    # clusters = embassy_deserialization("/Users/macbook/Desktop/Учебная/ИТИБ/Лабораторная 6/посольства-в-Москве.json")
    parkings = parking_deserialization("/Users/macbook/Desktop/Учебная/ИТИБ/Лабораторная 6/парковки.json", 200)
    clusters = distrits_deserialization()

    kohonen_layer = []
    for cluster in clusters:
        weights = [cluster.coordinate.coordinate_X, cluster.coordinate.coordinate_Y]
        kohonen_layer.append(Kohonen_neuron(weights))

    result_cluster_distribution = []
    for _ in clusters:
        result_cluster_distribution.append([_.name])

    for parking in parkings:
        input_set = [parking.coordinate.coordinate_X, parking.coordinate.coordinate_Y]
        binary_output = get_output_y_vector(input_set, kohonen_layer)
        # print (binary_output)
        for index in range(len(binary_output)):
            if binary_output[index] == 1:
                result_cluster_distribution[index].append(parking)


    for clust in result_cluster_distribution:
        print(clust[0])
        for park_index in range(1, len(clust)):
            print(clust[park_index].name)
        print("--------------")
                
main()