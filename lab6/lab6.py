# MIT 6.034 Lab 6: Neural Nets
# Written by 6.034 Staff

from nn_problems import *
from math import e
INF = float('inf')


#### Part 1: Wiring a Neural Net ###############################################

nn_half = [1]

nn_angle = [2, 1]

nn_cross = [2, 2, 1]

nn_stripe = [3, 1]

nn_hexagon = [6, 1]

nn_grid = [4, 2, 1 ]


#### Part 2: Coding Warmup #####################################################

# Threshold functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    return x >= threshold

import math
def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return 1 / (1 + math.exp(-steepness * (x - midpoint)))

def ReLU(x):
    "Computes the threshold of an input using a rectified linear unit."
    return max(0, x)

# Accuracy function
def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    difference = desired_output - actual_output
    return -.5 * difference * difference


#### Part 3: Forward Propagation ###############################################

def node_value(node, input_values, neuron_outputs):  # PROVIDED BY THE STAFF
    """
    Given 
     * a node (as an input or as a neuron),
     * a dictionary mapping input names to their values, and
     * a dictionary mapping neuron names to their outputs
    returns the output value of the node.
    This function does NOT do any computation; it simply looks up
    values in the provided dictionaries.
    """
    if isinstance(node, str):
        # A string node (either an input or a neuron)
        if node in input_values:
            return input_values[node]
        if node in neuron_outputs:
            return neuron_outputs[node]
        raise KeyError("Node '{}' not found in either the input values or neuron outputs dictionary.".format(node))
    
    if isinstance(node, (int, float)):
        # A constant input, such as -1
        return node
    
    raise TypeError("Node argument is {}; should be either a string or a number.".format(node))

def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""
    
    output = {}

    for node in net.topological_sort():
        total = 0
        for wire in net.get_wires(endNode = node):
            start_node = wire.startNode
            total += node_value(start_node, input_values, output) * wire.get_weight()

        output[node] = threshold_fn(total)

    return (output[net.get_output_neuron()], output)

#### Part 4: Backward Propagation ##############################################
import itertools

def gradient_ascent_step(func, inputs, step_size):
    """Given an unknown function of three variables and a list of three values
    representing the current inputs into the function, increments each variable
    by +/- step_size or 0, with the goal of maximizing the function output.
    After trying all possible variable assignments, returns a tuple containing:
    (1) the maximum function output found, and
    (2) the list of inputs that yielded the highest function output."""

    deltas = itertools.product([-step_size, 0, step_size], repeat=3)

    my_inputs = [(inputs[0] + a, inputs[1] + b, inputs[2] + c) for a,b,c in deltas]

    best = None
    for I in my_inputs:
        performance = func(*I)
        if best == None or performance > best[0]:
            best = (performance, I)

    return best

def get_back_prop_dependencies(net, wire):
    """Given a wire in a neural network, returns a set of inputs, neurons, and
    Wires whose outputs/values are required to update this wire's weight."""
    # The performance delta with respect to the wire depends on the the wire's input, output,
    #  and every wire/neuron that follows it.
    result = set([wire.startNode])

    queue = [wire]
    while queue:
        curr_wire = queue[0]
        queue = queue[1:]

        result.add(curr_wire)
        neuron = curr_wire.endNode

        if not neuron in result:
            result.add(neuron)

            for W in net.get_wires(startNode = neuron):
                if not W in result:
                    result.add(W)
                    queue.append(W)

    return result

def calculate_deltas(net, desired_output, neuron_outputs):
    """Given a neural net and a dictionary of neuron outputs from forward-
    propagation, computes the update coefficient (delta_B) for each
    neuron in the net. Uses the sigmoid function to compute neuron output.
    Returns a dictionary mapping neuron names to update coefficient (the
    delta_B values). """
    delta_B = {}

    for curr_neuron in reversed(net.topological_sort()):
        if net.is_output_neuron(curr_neuron):
            net_fitness = desired_output - neuron_outputs[curr_neuron]
            sigmoid_delta = neuron_outputs[curr_neuron] * (1 - neuron_outputs[curr_neuron])

            delta_B[curr_neuron] = net_fitness * sigmoid_delta
        else:
            weight = sum(delta_B[W.endNode]*W.weight for W in net.get_wires(startNode = curr_neuron))
            sigmoid_delta = neuron_outputs[curr_neuron] * (1 - neuron_outputs[curr_neuron])

            delta_B[curr_neuron] = weight * sigmoid_delta
        

    return delta_B

def update_weights(net, input_values, desired_output, neuron_outputs, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses the
    sigmoid function to compute neuron output.  Returns the modified neural net,
    with the updated weights."""
    delta_B = calculate_deltas(net, desired_output, neuron_outputs)

    for curr_neuron in net.neurons:
        for wire in net.get_wires(endNode = curr_neuron):
            old_weight = wire.get_weight()
            delta_weight = delta_B[curr_neuron] * node_value(wire.startNode, input_values, neuron_outputs)
            wire.set_weight(old_weight + delta_weight * r)

    return net

def back_prop(net, input_values, desired_output, r=1, minimum_accuracy=-0.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses the
    sigmoid function to compute neuron output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""
    # print('back_prop {} {} {} {} {}'.format(net, input_values, desired_output, r, minimum_accuracy))
    
    count = 0
    while True:
        net_output, neuron_outputs = forward_prop(net, input_values, sigmoid)
        if accuracy(desired_output, net_output) > minimum_accuracy:
            break
        deltas = calculate_deltas(net, desired_output, neuron_outputs)
        update_weights(net, input_values, desired_output, neuron_outputs, r)
        count = count + 1
        # print(count, net_output, desired_output, accuracy(desired_output, net_output))

    return (net, count)

#### Part 5: Training a Neural Net #############################################

ANSWER_1 = 29
ANSWER_2 = 40
ANSWER_3 = 9
ANSWER_4 = 104
ANSWER_5 = 28

ANSWER_6 = 1
ANSWER_7 = 'checkerboard'
ANSWER_8 = ['small', 'medium', 'large']
ANSWER_9 = 'B'

ANSWER_10 = 'D'
ANSWER_11 = ['A', 'C']
ANSWER_12 = ['A', 'E']


#### SURVEY ####################################################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
