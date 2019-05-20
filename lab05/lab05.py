import neuron

image_1 = [
    0,0,1,0,0,
    0,0,1,0,0,
    0,1,0,1,0,
    0,1,0,1,0,
    0,1,1,1,0,
    1,1,0,1,1,
    1,0,0,0,1,
    1,0,0,0,1
]

image_2 = [
    0,1,1,1,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,1,1,1,0
]

image_3 = [
    1,1,1,1,1,
    1,1,0,0,0,
    1,1,0,0,0,
    1,1,1,1,1,
    1,1,1,1,1,
    1,1,0,0,0,
    1,1,0,0,0,
    1,1,0,0,0
]

image_4 = [-1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,1,-1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,1,-1,-1,1,-1,-1,-1,-1,1,-1,-1]

test_image = [
    1,1,1,1,1,
    1,0,0,0,0,
    0,0,0,0,0,
    1,0,0,1,0,
    1,1,1,0,1,
    0,0,0,0,0,
    1,0,0,0,0,
    1,0,0,0,0
]

def main():
    # I = 5
    # J = 8
    # neuron_num = I*J # = K
    L = [image_1, image_2, image_3, image_4]
   
# КОСТЫЛЬ ОН
    for image in L:
        index = 0
        for _ in image:
            if _ == 0: image[index] = -1
            index += 1
    
    index_ = 0
    for _ in test_image:
        if _ == 0: test_image[index_]  = -1
        index_ += 1

# КОСТЫЛЬ ОФФ

    weights = []
    neuron_layer = learning_process(weights, L)
    recognize_image( test_image, neuron_layer, 10, L)


def recognize_image(image, neuron_layer, era_num, L):
    first_y_init(neuron_layer, image)
    previous_y = image.copy()
    for ep_num in range(era_num):
        output = []
        for neuron_i in neuron_layer:
            neuron_i.previous_y_init()
            neuron_i.net_init(previous_y)
            output.append(neuron_i.y_init())
        previous_y = output

        for l in L:
            if output == l:
                print("Я УЗНАЛ! УЗНАЛ ЗА", ep_num,"ЭПОХ!")
                for str in range(5, len(l), 5):
                    print(l[str-5:str])
                print("Output:", output)
                return
    
    print("Не, ну это дичь какая-то, я не знаю что это")

    

def learning_process(weights, L):
    weights_init(weights, L)
    neuron_layer = []
    # инициализация весов
    for _ in range(len(L[0])):
         neuron_layer.append( neuron.Hopfield_neuron(weights=weights[_]) )
    return neuron_layer


def weights_init(weights, L):
    for k_m in range(len(L[0])):
        weights_k = [] # вектор-вес K-го нейрона
        for k_n in range(len(L[0])): # инициализация вектора
            w_mn = 0
            if k_m != k_n:
                for l in L:
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