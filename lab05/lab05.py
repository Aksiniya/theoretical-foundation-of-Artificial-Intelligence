import neuron
import json
# input_images = [ [ -1 , -1 , 1 , -1 , -1 , -1 , 1 , 1 , -1 , -1 , 1 , -1 , 1 , -1 , -1 , -1 , -1 , 1 , -1 , -1 , -1 , -1 , 1 , -1 , -1 , -1 , -1 , 1 , -1 , -1 , -1 , -1 , 1 , -1 , -1 , 1 , 1 , 1 , 1 , 1 ] , [ -1 , 1 , 1 , 1 , -1 , 1 , -1 , -1 , -1 , 1 , 1 , -1 , -1 , -1 , 1 , -1 , -1 , -1 , 1 , -1 , -1 , -1 , 1 , -1 , -1 , -1 , 1 , -1 , -1 , -1 , 1 , -1 , -1 , -1 , 1 , 1 , 1 , 1 , 1 , 1 ] , [ -1 , -1 , 1 , -1 , -1 , -1 , 1 , 1 , 1 , -1 , 1 , -1 , 1 , -1 , 1 , -1 , 1 , 1 , 1 , -1 , 1 , -1 , 1 , -1 , 1 , -1 , 1 , 1 , 1 , -1 , 1 , -1 , 1 , -1 , 1 , -1 , -1 , 1 , -1 , -1 ] ]
# recognizable_image = [-1,1,1,1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1,-1,-1,-1,1,1,1,1,-1]



def main():

    print("Введите вектор образов, а затем искаженный образ:")
    # input_images_from_console = ()
    input_images = json.loads(input())
    # print(input_images)
    # print("Введите искаженный образ:")
    recognizable_image = json.loads(input())
    # print(recognizable_image)

    weights = []
    neuron_layer = learning_process(weights, input_images)
    recognize_image( recognizable_image, neuron_layer, 10, input_images)


def recognize_image(image, neuron_layer, era_num, input_images):
    first_y_init(neuron_layer, image)
    previous_y = image.copy()
    for ep_num in range(1, era_num):
        output = []
        for neuron_i in neuron_layer:
            neuron_i.previous_y_init()
            neuron_i.net_init(previous_y)
            output.append(neuron_i.y_init())
        previous_y = output

        for l in input_images:
            if output == l:
                print("Распознано. Эпохи: ", ep_num )
                for str in range(5, len(l), 5):
                    print(l[str-5:str])
                print("Output:", output)
                return
    
    print("Я не знаю что это.")
    print("Химера: ", output)

    

def learning_process(weights, input_images):
    weights_init(weights, input_images)
    neuron_layer = []
    # инициализация весов
    for _ in range(len(input_images[0])):
         neuron_layer.append( neuron.Hopfield_neuron(weights=weights[_]) )
    return neuron_layer


def weights_init(weights, input_images):
    for k_m in range(len(input_images[0])):
        weights_k = [] # вектор-вес K-го нейрона
        for k_n in range(len(input_images[0])): # инициализация вектора
            w_mn = 0
            if k_m != k_n:
                for l in input_images:
                    w_mn += l[k_n] * l[k_m]
            weights_k.append(w_mn)
        weights.append(weights_k)

def first_y_init(layer, input):
    index = 0
    for neuron_i in layer:        
        neuron_i.input_set_init(input)
        neuron_i.y_init_by_value(input[index])
        index += 1


main()