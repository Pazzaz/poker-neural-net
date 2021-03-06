import os
import random
from datetime import datetime

import numpy as np
import plotly.graph_objs as go
import plotly.offline as py


class NeuralNetCollection:
    def __init__(self, complexity, mutation_rate, network_count, load_networks=0):
        """
        Called when creating a new collection of networks. `complexity` is the structure of the
        hidden layers inside a single network. The form should be [k, a, b, c, ...] with 'n'
        being the input, 'a 'b' & 'c' being the number of nodes on each layer. The last layer
        is how many different values the output can be.
        """

        # network_count is the total amount of networks created for this NeuralNetCollection
        # over its lifetime. Its value is used as ids for new networks.
        self.network_count = 0

        self.print_path = "output/" + str(datetime.now().date())
        self.mutation_rate = mutation_rate
        self.complexity = complexity
        self.networks = self.generate_networks(load_amount=load_networks, total_amount=network_count)

    def generate_networks(self, load_amount, total_amount):
        networks = []
        while len(networks) < total_amount:
            if load_amount != 0:
                # You still have to load some networks from disc.
                weights = self.load_weights()
                load_amount -= 1
            else:
                weights = self.random_weights()
            performance = 0
            networks.append({"weights": weights, "performance": performance, "id": self.network_count})
            self.network_count += 1

        return networks

    def save_best_network(self):
        """Will save the weights of the best network of this NeuralNetCollection."""

        filename = input("Where do you want to save it? ")
        # Structure the output format
        output = ""
        for row in self.networks[0]["weights"]:
            output += ','.join(str(weight) for weight in list(row.flatten()))
            output += "\n"
        
        # Write the output
        write_file = open(filename, "w")
        write_file.write(output)

    def load_weights(self):
        filename = input("Where did you save the network? ")
        saved_file = open(filename, "r")
        weights = []
        for row in saved_file.readlines():
            weights.append([])
            for weight in row.split(","):
                weights[-1].append(float(weight))

        # Validate
        for index, (nodes_1, nodes_2) in enumerate(zip(self.complexity[1:], self.complexity[:-1])):
            weight_count = nodes_1 * nodes_2
            if len(weights[index]) != weight_count:
                print("Loaded network doesn't match 'complexity'")
                exit()
            weights[index] = np.array(weights[index]).reshape((nodes_1, nodes_2))

        return weights

    def random_weights(self):
        weights = []
        for i in range(1, len(self.complexity)):
            weights.append(np.random.uniform(-1, 1, (self.complexity[i], self.complexity[i-1])))

        return weights


    def update_networks(self, iteration):
        # Sort the networks by performance and print information about them.
        self.networks = sorted(self.networks, key=lambda x: x["performance"], reverse=True)
        self.print_networks(iteration)
        
        # Kill the worst networks
        self.networks = self.networks[:(len(self.networks) // 2)]

        # Breed new networks
        for g in range(len(self.networks)):
            # Mix the weights of two randomly chosen (alive) networks to create a new set of weights.
            new_weights = self.mix_weights(random.choice(self.networks)["weights"], random.choice(self.networks)["weights"])

            self.networks.append({"weights": new_weights, "performance": 0, "id": self.network_count})
            self.network_count += 1

    def print_networks(self, iteration):
        # Prints the performance of the networks in the form
        # "iteration n: x: xp, y: yp, z: zp"
        # where n is the variable 'iteration',
        # x, y & z are the individual networks' id and
        # xp, yp & zp are their respective performances.
        print("iteration " + str(iteration) + ": " + ', '.join(str(network["id"]) + ": " + str(network["performance"]) for network in self.networks))

    def reset_performance(self):
        # Set all networks performance to 0
        for network in self.networks:
            network["performance"] = 0

    def mix_weights(self, weights_one, weights_two):
        new_weights = []
        for (weight_row_1, weight_row_2) in zip(weights_one, weights_two):
            # Use an array filled with 0s and 1s to decide which array to take
            # some value from, for a specificindex. 0 corresponds to a value from
            # weight_row_1 and 1 to a value from weight_row_2.
            choise_mask = np.random.randint(low=0, high=2, size=weight_row_1.shape)
            mixed = np.choose(choise_mask, [weight_row_1, weight_row_2])

            # Add some mutation too
            mutation = np.random.uniform(low=-self.mutation_rate, high=self.mutation_rate, size=weight_row_1.shape)
            new_weights.append(mixed + mutation)
        return new_weights

    def test_best_network(self):
        """
        Use plotly to generate a heatmap. The heatmap shows how the best network reacts when given
        different card combinations where a value of 0 is that it folds when given that combination,
        regardless of the suits of the cards and a value of 1 is that it always bets when given that
        combination. Values inbetween mean its answer depends on the suit.
        """
        data = []
        for a in range(13):
            data.append([])
            for b in range(13):
                suit_answers = 0
                suit_answer_sum = 0
                for suit_a in range(4):
                    for suit_b in range(4):
                        if a == b and suit_a == suit_b:
                            continue
                        given_cards = [[a, suit_a], [b, suit_b]]
                        input_cards = np.zeros(52)
                        input_cards[a + suit_a * 13] = 1
                        input_cards[b + suit_b * 13] = 1
                        answer = get_answer(self.networks[0]["weights"], input_cards)
                        suit_answers += 1
                        suit_answer_sum += answer
                answer = suit_answer_sum / suit_answers
                data[-1].append(answer)

        axis_labels = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        layout = go.Layout(
            title = "Heatmap " + str(self.networks[0]["id"]),
            xaxis = dict(
                type = "category", # Prevent the axis labels from being treated as numbers
            ),
            yaxis = dict(
                type = "category",
                scaleanchor = "x", # Make the heatmap square
            ),
        )
        trace = go.Heatmap(z=data, x=axis_labels, y=axis_labels, zmin=0.0, zmax=1.0)
        fig = go.Figure(data=[trace], layout=layout)

        if not os.path.isdir("output"):
            os.makedirs(self.print_path)

        if not os.path.isdir(self.print_path):
            os.makedirs(self.print_path)
        dest = self.print_path + "/" + str(self.networks[0]["id"]) + '.html'
        py.plot(fig, filename=dest, auto_open=False)

def get_answer(weights, param):
    # The first row of nodes are input data
    node_row_former = param

    # Calculate the value of every node, in every row, from the beginning to the end.
    for weight_row in weights:
        node_row_former = np.tanh(np.multiply(weight_row, node_row_former).sum(axis=1))


    # Choose output by looking at which of the two output
    # nodes has the highest value
    return np.argmax(node_row_former)
