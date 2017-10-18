import random

def poker_simulator():
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
    player_2_hole_cards = cards[2:4]
    player_1_hand_strength = [0,0]
    player_2_hand_strength = [0,0]
    board = cards[4:10]
    #print(board)
    player_1_hand = player_1_hole_cards + board
    player_2_hand = player_2_hole_cards + board
    # Kolla efter flush
    suits_count_array = [0,0,0,0]
    flush_suit = -1
    for i in player_1_hand:
        suits_count_array[i[1]] += 1
    for i, suit in enumerate(suits_count_array):
        if suit >= 5:
            flush_suit = i
    
    flush_cards = [x[0] for x in player_1_hand if x[1] == flush_suit]
    if flush_cards != []:
        flush_cards.sort()
        flush_cards.reverse()

        # Kolla om det finns någon straight flush 
        straight_flush_counter = 0
        for a, b in zip(flush_cards[:-1], flush_cards[1:]):
            if a == b+1 or (a == 12 and b == 3):
                straight_flush_counter += 1
                if straight_flush_counter == 4:
                    if flush_cards[0] == flush_cards[1]+1 and flush_cards[1] == flush_cards [2]+1:
                        straight_flush_strength = flush_cards[0]
                    elif flush_cards[1] == flush_cards [2]+1 and flush_cards[2] == flush_cards[3]+1:
                        straight_flush_strength = flush_cards[1]
                    else:
                        straight_flush_strength = flush_cards[2]
                    player_1_hand_strength = [8, straight_flush_strength]
                    return player_1_hand_strength
            else:
                straight_flush_counter = 0

        if player_1_hand_strength[0] < 5:
            player_1_hand_strength[0] = 5
            player_1_hand_strength[1] = flush_cards[0]
            return player_1_hand_strength

    # Kolla efter saker som har med par att göra
    pairs = count_pairs(player_1_hand)
    largest_pair = -1
    largest_pair = -1
    largest_trips = -1
    second_largest_trips = -1
    for value, count in pairs.items():
        # Vi vill få fram de kort som vi har flest av men om det finns flera
        # med samma antal dubletter vill vi ha det med högsta värdet.
        if count == 2:
            if count > largest_pair:
                largest_pair = value
        if count == 3:
            second_largest_trips = largest_trips
            largest_trips = value
        if count == 4:
            # Quads
            player_1_hand_strength[0] = 7
            kicker = get_kicker(player_1_hand, [largest_pair])
            player_1_hand_strength[1] = kicker
            return player_1_hand_strength

    # Straight
    straight_counter = 0
    sorted_player_1_hand = [x[0] for x in sorted(player_1_hand, reverse=True)]
    for a, b in zip(sorted_player_1_hand[:-1], sorted_player_1_hand[1:]):
        if a == b+1 or (a == 12 and b == 3):
            straight_counter += 1
            if straight_counter == 4:
                if sorted_player_1_hand[0] == sorted_player_1_hand[1]+1 and sorted_player_1_hand[1] == sorted_player_1_hand [2]+1:
                    straight_strength = sorted_player_1_hand[0]
                elif sorted_player_1_hand[1] == sorted_player_1_hand [2]+1 and sorted_player_1_hand[2] == sorted_player_1_hand[3]+1:
                    straight_strength = sorted_player_1_hand[1]
                else:
                    straight_strength = sorted_player_1_hand[2]
                player_1_hand_strength = [4, straight_strength]
                return player_1_hand_strength
        else:
            straight_counter = 0

    if largest_trips != -1:
        
        if second_largest_trips != -1 or largest_pair != -1:
            # Full House
            player_1_hand_strength[0] = 6
            player_1_hand_strength[1] = [largest_trips]
            if second_largest_trips > largest_pair:
                player_1_hand_strength[1].append(second_largest_trips)
            else:
                player_1_hand_strength[1].append(largest_pair)

            return player_1_hand_strength
        else:
            # Three of a kind
            player_1_hand_strength[0] = 3
            kicker = get_kicker(player_1_hand, [largest_trips])
            player_1_hand_strength[1] = [kicker]
            second_kicker = get_kicker(player_1_hand, [largest_trips, kicker])
            player_1_hand_strength[1].append(second_kicker)
            return player_1_hand_strength
            
    elif largest_pair != -1:
        # Kolla om det finns mer än ett par
        second_pair = -1
        for value, count in pairs.items():
            if value != largest_pair and count == 2 and value > second_pair:
                second_pair = value

        if second_pair == -1:
            # pair
            player_1_hand_strength[0] = 1
            player_1_hand_strength[1] = [largest_pair]
            kicker = get_kicker(player_1_hand, [largest_pair])
            player_1_hand_strength[1].append(kicker)
            second_kicker = get_kicker(player_1_hand, [largest_pair, kicker])
            player_1_hand_strength[1].append(second_kicker)
            third_kicker = get_kicker(player_1_hand, [largest_pair, kicker, second_kicker])
            player_1_hand_strength[1].append(third_kicker)
            return player_1_hand_strength
        else:
            # Two pairs
            player_1_hand_strength[0] = 2
            player_1_hand_strength[1] = [largest_pair, second_pair]
            kicker = get_kicker(player_1_hand, [largest_pair, second_pair])
            player_1_hand_strength[1].append(kicker)
            return player_1_hand_strength

    # High card
    player_1_hand.sort(reverse=True)
    return [0, player_1_hand]

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

for _ in range(1000):
    print(poker_simulator())
