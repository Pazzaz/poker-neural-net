from Poker_simulator.poker_simulator import play_against, play_self

import random
import math


class Neural_net:
    def __init__(self, complexity):
        '''
        'complexity' is a list of how the nodes should be structured. 
        The form should be [2, a, b, c, 2] with the beginning being the 
        input (always two for now), 'a' 'b' & 'c' being the number of 
        nodes on each layer and the end should be the output 
        (always two for now too).
        '''
        self.complexity = complexity
        self.nodes = self.generate_nodes()
        self.genes = self.generate_genes(8)

    def generate_genes(self, amount):
        genes = []
        while len(genes) < amount:
            trans = self.random_transformation()
            performance = 0
            genes.append([trans, performance])

        return genes

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
            for b in range(len(self.nodes[a])):
                node = self.nodes[a]
                node[b] = 0
                for c in range(len(self.nodes[a-1])):
                    node[b] += self.nodes[a-1][c] * next(trans_row)

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
            # Kill the worst genes
            self.genes = sorted(self.genes, key=lambda x: x[1], reverse=True)
            self.genes = self.genes[:(len(self.genes) // 2)]

            # Print the performance and iteration for every gene
            print(', '.join(str(gene[1]) for gene in self.genes))
            print(',  '.join(str(gene[2]) for gene in self.genes))

            # Breed new genes
            random.shuffle(self.genes)
            for g in range(len(self.genes)):
                new_gene = self.combine_transformations(self.genes[g][0], self.genes[g+1][0])
                self.genes.append([new_gene, 0, a+1])

            # Test the genes
            for g in self.genes:
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
    
    def update_genes(self):
        # Kill the worst genes
        self.genes = sorted(self.genes, key=lambda x: x[1], reverse=True)
        self.genes = self.genes[:(len(self.genes) // 2)]

        # Print the performance and iteration for every gene
        print(', '.join(str(gene[1]) for gene in self.genes))

        # Set everyones performance to 0
        for gene in self.genes:
            gene[1] = 0

        # Breed new genes
        random.shuffle(self.genes)
        for g in range(len(self.genes)):
            new_gene = self.combine_transformations(self.genes[g][0], self.genes[g+1][0])
            self.genes.append([new_gene, 0])


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

# Create the normal net. Will fill itself with "random" (filtered) genes.
nn = Neural_net([14,8,8,2])
nn2 = Neural_net([14,8,8,2])

play_self(nn, 20, 20)
print("First is done practicing")
play_self(nn2, 20, 20)
print("Second is done practicing")

play_against(nn, nn2, 100, 20)