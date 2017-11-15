from Poker_simulator.poker_simulator import play_against, play_self

import random
import math

class Neural_net_collection:
    def __init__(self, complexity):
        '''
        'complexity' is a list of how the nodes should be structured. 
        The form should be [2, a, b, c, 2] with the beginning being the 
        input 'a' 'b' & 'c' being the number of 
        nodes on each layer and the end should be the output 
        (always two for now too).
        '''
        self.network_count = 0
        self.complexity = complexity
        self.nodes = self.generate_nodes()
        self.networks = self.generate_networks(8)

    def generate_networks(self, amount):
        networks = []
        while len(networks) < amount:
            trans = self.random_transformation()
            performance = 0
            networks.append([trans, performance, self.network_count])
            self.network_count += 1

        return networks

    def generate_nodes(self):
        nodes = []
        for c in self.complexity:
            node_row = list(x for x in range(c))
            nodes.append(node_row)

        return nodes

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

    def train(self, iterations):
        for a in range(iterations):
            # Kill the worst networks
            self.networks = sorted(self.networks, key=lambda x: x[1], reverse=True)
            self.networks = self.networks[:(len(self.networks) // 2)]

            # Print the performance and iteration for every network
            print(', '.join(str(network[1]) for network in self.networks))
            print(',  '.join(str(network[2]) for network in self.networks))

            # Breed new networks
            random.shuffle(self.networks)
            for g in range(len(self.networks)):
                new_network = self.combine_transformations(self.networks[g][0], self.networks[g+1][0])
                self.networks.append([new_network, 0, a+1])

            # Test the networks
            for g in self.networks:
                performance = 0
                for c in range(1000):
                    number_1 = random.randint(0, 10)
                    number_2 = random.randint(0, 10)
                    result = self.get_answer(g[0], [number_1, number_2])
                    if (number_1 + number_2) > 10:
                        if result == 1:
                            performance += 1
                        else:
                            performance -= 1
                    else:
                        if result == 1:
                            performance -= 1
                        else:
                            performance += 1
                g[1] = performance
    
    def update_networks(self):
        # Kill the worst networks
        self.networks = sorted(self.networks, key=lambda x: x[1], reverse=True)
        self.networks = self.networks[:(len(self.networks) // 2)]

        # Breed new networks
        for g in range(len(self.networks)):
            new_network = self.combine_transformations(random.choice(self.networks)[0], random.choice(self.networks)[0])
            self.networks.append([new_network, 0, self.network_count])
            self.network_count += 1

    def reset_performance(self):
        # Set everyones performance to 0
        for network in self.networks:
            network[1] = 0

    def combine_transformations(self, trans_one, trans_two):
        new_trans = []
        for a in range(len(trans_one)):
            new_trans.append([])
            for one, two in zip(trans_one[a], trans_two[a]):
                mutation = random.uniform(-0.1, 0.1)
                # Randomly choose connections between trans_one and trans_two
                new_trans[a].append(random.choice([one, two]) + mutation)
        return new_trans

# Specify the seed to use. Useful for debugging.
random.seed(11)

# Create the normal net. Will fill itself with "random" (filtered) networks.
nn = Neural_net_collection([14,8,8,2])
nn2 = Neural_net_collection([14,8,8,2])

play_self(nn, 50, 20)
print("TESTING")
play_self(nn, 20, 20, False)
print("First is done practicing")
play_self(nn2, 20, 20, False)
print("Second is done practicing")

play_against(nn, nn2, 100, 20)