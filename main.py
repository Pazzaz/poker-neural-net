from poker_simulator import play_against, play_self
from neural import NeuralNetCollection
import numpy
import random

numpy.random.seed(11)
random.seed(11)
# Create the network.
nn = NeuralNetCollection(complexity=[52,40,2], load_networks=0, network_count=12, mutation_rate=0.5)

play_self(nn, iterations=5, blinds=20, print_debug=True)
