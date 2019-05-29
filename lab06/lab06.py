import json
import math
import random

class Coordinate():
    def __init__(self, coordinate_X=0, coordinate_Y=0):
        self.coordinate_X = coordinate_X
        self.coordinate_Y = coordinate_Y

    def distance(self, other_coordinate):
        return math.sqrt((other_coordinate.coordinate_X - self.coordinate_X)**2 + (other_coordinate.coordinate_Y - self.coordinate_Y)**2)

# просто точка с именем
class Object_in_map:
    def __init__(self, name="", coordinate=Coordinate()):
        self.name = name
        self.coordinate = coordinate

    def print(self):
        print(self.name, self.coordinate.coordinate_X, self.coordinate.coordinate_Y)

# точка с доп. параметром
class point_object_in_map(Object_in_map):
    def __init__(self, name="", coordinate=Coordinate(), cluster_name=""):
        Object_in_map.__init__(self, name=name, coordinate=coordinate)
        self.cluster_name = cluster_name

# функция по развертке json для посольств в Москве
def embassy_deserialization(full_path_to_json):
    with open(full_path_to_json, "r",  encoding = "Windows-1251") as read_file:
        data = json.load(read_file)
    clusters = []
    for embassy in data:
        coordinates = Coordinate(embassy["geoData"]["coordinates"][0],embassy["geoData"]["coordinates"][1])
        clusters.append(Object_in_map(embassy["Name"], coordinates))
    return clusters

# функция по развертке json парковок в Москве. Каждый раз возвращает разный вектор с limit парковками
def parking_deserialization(full_path_to_json, limit):
    with open(full_path_to_json, "r",  encoding = "Windows-1251") as read_file:
        data = json.load(read_file)

    if (len(data) < limit):
        print("Ошибка: указанный размер выборки превышает размер данных.\nБудут возвращены все данные, а не выборка.")
        limit = len(data)

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
        parkings.append(point_object_in_map(data[parking_index]["ParkingName"], coordinates, data[parking_index]["AdmArea"]))
        # print (data[parking_index])
        current_index += 1
    return parkings

# функция по развертке json учебных учреждений в Москве. Каждый раз возвращает разный вектор школ с количеством школ = limit
def college_deserialization(full_path_to_json, limit):
    with open(full_path_to_json, "r",  encoding = "Windows-1251") as read_file:
        data = json.load(read_file)
    colleges = []
    current_index = 0

    # Обработка несистематизированных данных
    new_data = []
    for d in data:
        geoData = d["geoData"]
        cent_exist = "center" in geoData
        if (cent_exist):
            new_data.append(d)
    data = new_data

    if (len(data) < limit):
        print("Ошибка: Указанный размер выборки превышает размер данных.\nБудут возвращены все данные, а не выборка.")
        limit = len(data)

    # Получить рандомные индексы таким образом, чтобы они не повторялись.
    rand_indexes = {}
    while (len(rand_indexes) < limit):
        rand_indexes[random.randint(0, len(data)-1)] = " "
        
    for college_index in rand_indexes.keys():
        if (current_index >= limit):
            break
        c = data[college_index]["geoData"]["center"][0]
        coordinates = Coordinate(c[0], c[1])
        colleges.append(point_object_in_map(data[college_index]["InstitutionsAddresses"][0]["FullName"], coordinates, data[college_index]["InstitutionsAddresses"][0]["AdmArea"]))
        current_index += 1
    return colleges

class Kohonen_neuron:
    def __init__(self, weights=[], input_set = [], net = 0):
        self.weights = weights 
        self.input_set = input_set
        self.net = net

    def output(self):
        return math.sqrt((self.weights[0] - self.input_set[0])**2 + (self.weights[1] - self.input_set[1])**2)

    def print_weights(self, signs = 1):
        print("[ ", end="")
        for w in self.weights: print("%.{0}f".format(signs) % w, end = " ")
        print("]", end = "")

# Функция получает на вход выход нс и преобразует его в бинарный
def competition_function(vector):
    output_binary_vector = []
    min_value = min(vector) # минимальное расстояние
    for _ in vector:
        if (_ == min_value):
            output_binary_vector.append(1)
        else:
            output_binary_vector.append(0)
    return output_binary_vector

# подача на вход нс (layer) вектора input_set
def get_output_y_vector(input_set, layer):
    y_vector = []
    for neuron_i in range(len(layer)):
        layer[neuron_i].input_set = input_set
        y_vector.append(layer[neuron_i].output())
    return competition_function(y_vector) # бинарный выход

def districts_deserialization():
    json_districts = {'Центральный административный округ': [55.750000, 37.616670],
                          'Северный административный округ': [55.838384, 37.525765],
                          'Северо-Восточный административный округ': [55.863894, 37.620923],
                          'Восточный административный округ': [55.787710, 37.775631],
                          'Юго-Восточный административный округ': [55.692019, 37.754583],
                          'Южный административный округ': [55.610906, 37.681479],
                          'Юго-Западный административный округ': [55.662735, 37.576178],
                          'Западный административный округ': [55.728003, 37.443533],
                          'Северо-Западный административный округ': [55.829370, 37.451546],
                          'Зеленоградский административный округ': [55.987583, 37.194250],
                          'Троицкий административный округ': [55.355771, 37.146990],
                          'Новомосковский административный округ': [55.558121, 37.370724]
                          }

    admArea = []
    for key in json_districts.keys():
        coord = Coordinate(json_districts[key][1], json_districts[key][0])
        admArea.append(Object_in_map(key, coord))
    return admArea


def main():
    clusters = districts_deserialization()
    print("Введите полный путь до json со школами:")
    path_to_colleges = input()
    print("Введите количество школ для кластеризации:")
    num_of_schools = input()
    colleges = college_deserialization(path_to_colleges, int(num_of_schools))

    kohonen_layer = []
    for cluster in clusters:
        weights = [cluster.coordinate.coordinate_X, cluster.coordinate.coordinate_Y]
        kohonen_layer.append(Kohonen_neuron(weights))

    result_cluster_distribution = []
    for _ in clusters:
        result_cluster_distribution.append([_.name])

    for college in colleges:
        input_set = [college.coordinate.coordinate_X, college.coordinate.coordinate_Y]
        binary_output = get_output_y_vector(input_set, kohonen_layer)
        # print (binary_output)
        for index in range(len(binary_output)):
            if binary_output[index] == 1:
                result_cluster_distribution[index].append(college)

    wrong_counter = 0
    for clust in result_cluster_distribution:
        clust_name = clust[0]
        print(clust_name)
        for college_index in range(1, len(clust)):
            print(clust[college_index].name, "\t|",clust[college_index].cluster_name)
            if clust[college_index].cluster_name != clust_name:
                wrong_counter += 1
        print("--------------")
    print("Процент ошибки:", round(( wrong_counter / len(colleges) ) * 100, 1 ) , "%" )
    
main()