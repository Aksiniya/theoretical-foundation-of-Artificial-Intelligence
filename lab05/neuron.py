import matplotlib.pyplot as plt
import math
import matplotlib.pyplot as plt

class one_neuron:
    def __init__(self, weights=[], input_set = [], net = 0, y = 0):
        self.weights = weights
        self.input_set = input_set
        self.net = 0
        self.y = 0

    def weights_init(self, weights):
        self.weights = weights

    def input_set_init(self, input_):
        self.input_set = input_

    def net_init(self):
        net = 0
        for i in range( len(self.weights) ):
            net += self.weights[i] * self.input_set[i]
        self.net = net
        return net

    def y_init(self):
        self.y = self.net
        return self.y

    def print_weights(self, signs = 1):
        print("[ ", end="")
        for w in self.weights: print("%.{0}f".format(signs) % w, end = " ")
        print("]", end = "")


class Hopfield_neuron(one_neuron):
    def __init__(self, weights=[], input_set = [], net = 0, y = 0, previous_y = 0):
        self.weights = weights
        self.input_set = input_set
        self.net = net
        self.y = y
        self.previous_y = previous_y

    def previous_y_init(self):
        self.previous_y = self.y

    def y_init(self):
        if self.net > 0:
            self.y = 1
        elif self.net < 0:
            self.y = -1
        else:
            self.y = self.previous_y
        return self.y

    def y_init_by_value(self, value):
        self.y = value

    def net_init(self, previous_y_vector):
        sum_net = 0
        for w_ind in range(len(self.weights)):
            sum_net += self.weights[w_ind] * previous_y_vector[w_ind]
        self.net = sum_net
        return sum_net
