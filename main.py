from Poker_simulator.poker_simulator import play_against, play_self

import random
import math
import plotly.offline as py
import plotly.graph_objs as go

class Neural_net_collection:
    def __init__(self, complexity, mutation_rate, network_count, load_networks=0):
        '''
        'complexity' is a list of how the nodes should be structured. 
        The form should be [2, a, b, c, 2] with the beginning being the 
        input 'a' 'b' & 'c' being the number of 
        nodes on each layer and the end should be the output 
        (always two for now too).
        '''
        self.network_count = 0
        self.mutation_rate = mutation_rate
        self.complexity = complexity
        self.nodes = self.generate_nodes()
        self.networks = self.generate_networks(load_amount=load_networks, total_amount=network_count)

    def generate_networks(self, load_amount, total_amount):
        networks = []
        while len(networks) < total_amount:
            if load_amount == 0:
                trans = self.random_transformation()
            else:
                trans = self.load_transformation()
                load_amount -= 1
            performance = 0
            networks.append({"weights": trans, "performance": performance, "id": self.network_count})
            self.network_count += 1

        return networks

    def generate_nodes(self):
        nodes = []
        for c in self.complexity:
            node_row = list(x for x in range(c))
            nodes.append(node_row)

        return nodes

    def save_best_network(self):
        filename = input("Where do you want to save it? ")
        # Structure the output format
        output = ""
        for row in self.networks[0]["weights"]:
            output += ','.join(str(weight) for weight in row)
            output += "\n"
        
        # Write the output
        write_file = open(filename, "w")
        write_file.write(output)

    def load_transformation(self):
        filename = input("Where did you save the network? ")
        saved_file = open(filename, "r")
        transformation = []
        for row in saved_file.readlines():
            transformation.append([])
            for weight in row.split(","):
                transformation[-1].append(float(weight))

        # Validate
        for index, (nodes_1, nodes_2) in enumerate(zip(self.complexity[1:], self.complexity[:1])):
            weight_count = nodes_1 * nodes_2
            if len(transformation[index]) != weight_count:
                print("Loaded network doesn't match 'complexity'")
                exit()

        return transformation

    def random_transformation(self):
        transformation = []
        for i in range(1, len(self.complexity)):
            transformation.append([])
            connections = self.complexity[i] * self.complexity[i-1]
            for _ in range(connections):
                transformation[i-1].append(random.uniform(-1.0, 1.0))

        return transformation

    def get_answer(self, transformation, param):
        # The first row of nodes are input data
        for i in range(len(self.nodes[0])):
            self.nodes[0][i] = param[i]

        # Calculate the value of every node
        for a in range(1, len(self.nodes)):
            trans_row = iter(transformation[a-1])
            node = self.nodes[a]
            for b in range(len(self.nodes[a])):
                node[b] = sum(map(lambda node, trans: node * trans, iter(self.nodes[a-1]), trans_row))

                # Normalize the value
                node[b] = math.tanh(node[b])


        # Choose output by looking at which of the two output
        # nodes has the highest value
        largest_value = 0
        output = 0
        for i, node_value in enumerate(self.nodes[-1]):
            if  largest_value < node_value:
                largest_value = node_value
                output = i
        return output

    def update_networks(self, iteration):
        # Kill the worst networks
        self.networks = sorted(self.networks, key=lambda x: x["performance"], reverse=True)
        self.print_networks(iteration)
        self.networks = self.networks[:(len(self.networks) // 2)]

        # Breed new networks
        for g in range(len(self.networks)):
            new_network = self.combine_transformations(random.choice(self.networks)["weights"], random.choice(self.networks)["weights"])
            self.networks.append({"weights": new_network, "performance": 0, "id": self.network_count})
            self.network_count += 1

    def print_networks(self, iteration):
        print("iteration " + str(iteration) + ": " + ', '.join(str(network["id"]) + ": " + str(network["performance"]) for network in self.networks))

    def reset_performance(self):
        # Set everyones performance to 0
        for network in self.networks:
            network["performance"] = 0

    def combine_transformations(self, trans_one, trans_two):
        new_trans = []
        for a in range(len(trans_one)):
            new_trans.append([])
            for one, two in zip(trans_one[a], trans_two[a]):
                mutation = random.uniform(-self.mutation_rate, self.mutation_rate)
                # Randomly choose connections between trans_one and trans_two
                new_trans[a].append(random.choice([one, two]) + mutation)
        return new_trans

    def test_best_network(self):
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
                        input_cards = [number for hand in sorted(given_cards) for number in hand]
                        answer = self.get_answer(self.networks[0]["weights"], input_cards)
                        suit_answers += 1
                        suit_answer_sum += answer
                answer = suit_answer_sum / suit_answers
                data[-1].append(answer)

        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        layout = go.Layout(
            title = "Heatmap " + str(self.networks[0]["id"]),
            xaxis = dict(
                type = "category",
            ),
            yaxis = dict(
                type = "category",
                scaleanchor = "x",
            ),
        )
        trace = go.Heatmap(z=data, x=cards, y=cards)
        fig = go.Figure(data=[trace], layout=layout)
        py.plot(fig, filename='basic-heatmap.html')

# Specify the seed to use. Useful for debugging.
random.seed(11)

# Create the normal net. Will fill itself with "random" (filtered) networks.
nn = Neural_net_collection(complexity=[4,40,20,10,2], load_networks=0, network_count=4, mutation_rate=1)

play_self(nn, iterations=40, blinds=20, print_debug=True)

nn.save_best_network()