from itertools import combinations

import eval7
import numpy as np

from neural import get_answer

deck = eval7.Deck()

def play_against(net_1, net_2, iterations, blinds, hands, learning=True):
    """
    Play two different NeuralNetCollections against eachother.
    """
    for i in range(iterations):
        for network_from_1 in net_1.networks:
            for network_from_2 in net_2.networks:
                play_game(network_from_1, network_from_2, blinds, hands)
                # Switch places
                play_game(network_from_2, network_from_1, blinds, hands)
        if learning:
            net_1.update_networks(i)
            net_2.update_networks(i)
        else:
            net_1.print_networks(i)
            net_2.print_networks(i)

        net_1.reset_performance()
        net_2.reset_performance()
    answer = input("Do you want to save the networks? y/n ")
    if answer == "y":
        net_1.save_best_network()
        net_2.save_best_network()


def play_self(network_collection, iterations, blinds, hands, learning=True, print_debug=False):
    """
    Let the different networks inside a NeuralNetCollection play against
    eachother. For every iteration, each network will play against every other
    network inside its NeuralNetCollection.
    """
    for i in range(iterations):
        for first_network, second_network in combinations(network_collection.networks, 2):
            play_game(first_network, second_network, blinds, hands)
            # Switch places
            play_game(second_network, first_network, blinds, hands)
        if learning:
            network_collection.update_networks(i)
        else:
            network_collection.print_networks(i)

        network_collection.reset_performance()
        if print_debug:
            network_collection.test_best_network()
        

def play_game(network_1, network_2, blinds, hands):
    for _ in range(hands):

        # Draw and distribute cards
        cards = deck.sample(9)
        p1_hole_cards = cards[0:2]
        p2_hole_cards = cards[2:4]
        board = cards[4:9]
        p1_cards = p1_hole_cards + board
        p2_cards = p2_hole_cards + board

        # Create the input to p1: a 52 value array filled with zeroes and two indices
        # where the value is 1. These two indices corresponds to p1_hole_cards.
        p1_input = np.zeros(52)
        card_id_1 = p1_hole_cards[0].rank + p1_hole_cards[0].suit * 13
        card_id_2 = p1_hole_cards[1].rank + p1_hole_cards[1].suit * 13
        p1_input[card_id_1] = 1
        p1_input[card_id_2] = 1
        p1_answer = get_answer(network_1["weights"], p1_input)
        
        if p1_answer != 0:

            p2_input = np.zeros(52)
            card_id_1 = p2_hole_cards[0].rank + p2_hole_cards[0].suit * 13
            card_id_2 = p2_hole_cards[1].rank + p2_hole_cards[1].suit * 13
            p2_input[card_id_1] = 1
            p2_input[card_id_2] = 1
            p2_answer = get_answer(network_2["weights"], p2_input)
        
            if p2_answer != 0:
                p1_eval = eval7.evaluate(p1_cards)
                p2_eval = eval7.evaluate(p2_cards)
                if p1_eval > p2_eval:
                    network_1["performance"] += blinds
                    network_2["performance"] -= blinds
                elif p1_eval < p2_eval:
                    network_1["performance"] -= blinds
                    network_2["performance"] += blinds
        
            else:
                # Player 2 folded
                network_1["performance"] += 1
                network_2["performance"] -= 1

        else:
            # Player 1 folded
            network_1["performance"] -= 0.5
            network_2["performance"] += 0.5
