import random

def game(net_1, net_2, iterations, blinds):
    for i in range(iterations):
        for gene_from_1 in net_1.genes:
            for gene_from_2 in net_2.genes:
                for _ in range(500):
                    cards_drawn = []
                    cards = []
                    for i in range(9):
                        card = random.randint(0, 51)
                        while card in cards_drawn:
                            card = random.randint(0, 51)
                        card_value = card % 13
                        card_suit = card % 4
                        cards.append([card_value, card_suit])
                        cards_drawn.append(card)

                    player_1_hole_cards = cards[0:2]
                    board = cards[4:10]
                    player_1_hand = player_1_hole_cards + board
                    player_2_hole_cards = cards[2:4]
                    player_2_hand = player_2_hole_cards + board
                    flattened_player_1_hand = [number for hand in player_1_hand for number in hand]
                    player_1_answer = net_1.get_answer(gene_from_1[0], flattened_player_1_hand)
                    if player_1_answer != 0:
                        flattened_player_2_hand = [number for hand in player_1_hand for number in hand]
                        player_2_answer = net_2.get_answer(gene_from_2[0], flattened_player_2_hand)
                        if player_2_answer != 0:
                            player_1_result = evaluate_hand(player_1_hand)
                            player_2_result = evaluate_hand(player_2_hand)
                            if player_1_result > player_2_result:
                                gene_from_1[1] += blinds
                                gene_from_2[1] -= blinds
                            else:
                                gene_from_1[1] -= blinds
                                gene_from_2[1] += blinds
                    
                        else:
                            gene_from_1[1] += 1
                            gene_from_2[1] -= 1

                    else:
                        gene_from_1[1] -= 0.5
                        gene_from_2[1] += 0.5

        net_1.update_genes()
        net_2.update_genes()
                
                    
                

def evaluate_hand(hand):
    hand_strength = [0,0]
    # Kolla efter flush
    suits_count_array = [0,0,0,0]
    flush_suit = -1
    for i in hand:
        suits_count_array[i[1]] += 1
    for i, suit in enumerate(suits_count_array):
        if suit >= 5:
            flush_suit = i
    
    flush_cards = [x[0] for x in hand if x[1] == flush_suit]
    if flush_cards != []:
        # Kolla om det finns någon straight flush 
        flush_cards = sorted(flush_cards, reverse=True)
        if 12 in flush_cards:
            # Esset kan räknas som lägre än 2 i en stege
            flush_cards.append(-1)
        straight_flush_counter = 0
        for a, b in zip(flush_cards[:-1], flush_cards[1:]):
            if a == b+1:
                straight_flush_counter += 1
                if straight_flush_counter == 4:
                    if flush_cards[0] == flush_cards[1]+1 and flush_cards[1] == flush_cards [2]+1:
                        straight_flush_strength = flush_cards[0]
                    elif flush_cards[1] == flush_cards [2]+1 and flush_cards[2] == flush_cards[3]+1:
                        straight_flush_strength = flush_cards[1]
                    else:
                        straight_flush_strength = flush_cards[2]
                    hand_strength = [8, straight_flush_strength]
                    return hand_strength
            elif a != b:
                straight_flush_counter = 0

        if hand_strength[0] < 5:
            hand_strength[0] = 5
            hand_strength[1] = flush_cards[0]
            return hand_strength

    # Kolla efter saker som har med par att göra
    pairs = count_pairs(hand)
    largest_pair = -1
    largest_pair = -1
    largest_trips = -1
    second_largest_trips = -1
    for value, count in pairs.items():
        if count == 2:
            if count > largest_pair:
                largest_pair = value
        if count == 3:
            second_largest_trips = largest_trips
            largest_trips = value
        if count == 4:
            # Quads
            hand_strength[0] = 7
            kicker = get_kicker(hand, [largest_pair])
            hand_strength[1] = kicker
            return hand_strength

    # Straight
    straight_counter = 0
    sorted_hand = [x[0] for x in hand]
    sorted_hand = sorted(sorted_hand, reverse=True)
    if 12 in sorted_hand:
        sorted_hand.append(-1)
    for a, b in zip(sorted_hand[:-1], sorted_hand[1:]):
        if a == b+1:
            straight_counter += 1
            if straight_counter == 4:
                if sorted_hand[0] == sorted_hand[1]+1 and sorted_hand[1] == sorted_hand [2]+1:
                    straight_strength = sorted_hand[0]
                elif sorted_hand[1] == sorted_hand [2]+1 and sorted_hand[2] == sorted_hand[3]+1:
                    straight_strength = sorted_hand[1]
                else:
                    straight_strength = sorted_hand[2]
                hand_strength = [4, straight_strength]
                return hand_strength
        elif a != b:
            straight_counter = 0

    if largest_trips != -1:
        
        if second_largest_trips != -1 or largest_pair != -1:
            # Full House
            hand_strength[0] = 6
            hand_strength[1] = [largest_trips]
            if second_largest_trips > largest_pair:
                hand_strength[1].append(second_largest_trips)
            else:
                hand_strength[1].append(largest_pair)

            return hand_strength
        else:
            # Three of a kind
            hand_strength[0] = 3
            kicker = get_kicker(hand, [largest_trips])
            hand_strength[1] = [kicker]
            second_kicker = get_kicker(hand, [largest_trips, kicker])
            hand_strength[1].append(second_kicker)
            return hand_strength
            
    elif largest_pair != -1:
        # Kolla om det finns mer än ett par
        second_pair = -1
        for value, count in pairs.items():
            if value != largest_pair and count == 2 and value > second_pair:
                second_pair = value

        if second_pair == -1:
            # pair
            hand_strength[0] = 1
            hand_strength[1] = [largest_pair]
            kicker = get_kicker(hand, [largest_pair])
            hand_strength[1].append(kicker)
            second_kicker = get_kicker(hand, [largest_pair, kicker])
            hand_strength[1].append(second_kicker)
            third_kicker = get_kicker(hand, [largest_pair, kicker, second_kicker])
            hand_strength[1].append(third_kicker)
            return hand_strength
        else:
            # Two pairs
            hand_strength[0] = 2
            hand_strength[1] = [largest_pair, second_pair]
            kicker = get_kicker(hand, [largest_pair, second_pair])
            hand_strength[1].append(kicker)
            return hand_strength

    # High card
    hand.sort(reverse=True)
    return [0, hand]

def count_pairs(card_list):
    card_pairs = {}
    for card in card_list:
        value = card[0]
        if value in card_pairs:
            card_pairs[value] += 1
        else:
            card_pairs[value] = 1
    return card_pairs

def get_kicker(hand, exclude):
    kicker = -1
    for card in hand:
        value = card[0]
        if value > kicker and value not in exclude:
            kicker = value
    
    return kicker