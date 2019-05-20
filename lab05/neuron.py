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

    def net_init(self):
        sum_net = 0
        for w in self.weights:
            sum_net += w * self.previous_y
        self.net = sum_net
        return sum_net

def make_plot(plot_dict, ax, name, xlabel_name, y_label_name):
    for k in plot_dict:
        ax.scatter(k, plot_dict[k], c='b')
        if (k != 1):
            ax.plot([ k-1,  k], [plot_dict[k-1], plot_dict[k]], 'c')
    ax.grid(True)
    ax.set(xlabel=xlabel_name, ylabel=y_label_name, title=name)

def make_plot_line(plot_dict, ax, name = "", xlabel_name = "", y_label_name = "" ):
    x = sorted(plot_dict.keys())
    y = [ plot_dict[i] for i in x] #plot_dict.values()

    ax.plot(x, y)
    ax.set(xlabel=xlabel_name, ylabel=y_label_name, title=name)
    ax.grid()

def make_plot_point(plot_dict, ax, name = "", xlabel_name = "", y_label_name = "" ):
    x = sorted(plot_dict.keys())
    y = [ plot_dict[i] for i in x] #plot_dict.values()

    for key in plot_dict.keys():
        ax.plot(key, plot_dict[key], 'bo')

    ax.plot(x, y)
    ax.set(xlabel=xlabel_name, ylabel=y_label_name, title=name)
    ax.grid()

def print_note(note):
    count_of_eq = int((40-len(note))/2)
    print("="*count_of_eq, end="")
    print(" " + note + " ", end = "")
    print("="*count_of_eq, end="")
    if (len(note)%2 == 1): print("=", end = "")
    print()