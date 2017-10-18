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

        # Kolla om det finns någomn straight flush 
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
                    # print ("Flush cards"+str(flush_cards))
                    # print("Straight flush")
                    # print(sorted(player_1_hand))
                    # print(player_1_hand_strength)
                    break #Break eftersom en straight flush upptäckts och vi inte behöver leta mer. 
            else:
                straight_flush_counter = 0
        # Kolla efter saker som har med par att göra
        pairs = count_pairs(player_1_hand)
        largest_pair = 0
        second_largest_pair = 0 # Behövs för att hitta Full House
        largest_pair_value = -1
        for value, count in pairs.items():
            # Vi vill få fram de kort som vi har flest av men om det finns flera
            # med samma antal dubletter vill vi ha det med högsta värdet.
            if count > largest_pair or (count == largest_pair and value > largest_pair_value):
                second_largest_pair = largest_pair
                largest_pair = count
                largest_pair_value = value

        if largest_pair == 4:
            # Quads
            player_1_hand_strength[0] = 7
            
            kicker = -1
            for card in player_1_hand:
                value = card[0]
                if value > kicker and value != largest_pair_value:
                    kicker = value
            
            player_1_hand_strength[1] = kicker
        elif largest_pair == 3:
            # TODO Fixa player_1_hand_strength[1].
            if second_largest_pair >= 2:
                # Full House
                player_1_hand_strength[0] = 6
            else:
                # Three of a kind
                player_1_hand_strength[0] = 3
                
        elif largest_pair == 2:
            # TODO Fixa player_1_hand_strength[1].

            # Kolla om det finns mer än ett par
            second_pair_value = -1
            for value, count in pairs.items():
                if value != largest_pair_value and count == 2 and value > second_pair_value:
                    second_pair_value = value

            if second_pair_value == -1:
                # pair
                player_1_hand_strength[0] = 1
            else:
                # Two pairs
                player_1_hand_strength[0] = 1



        if int(player_1_hand_strength[0]) < 5:
            player_1_hand_strength[0] = 5
            # while len(flush_cards) > 5:
            #     flush_cards.pop()   
            # # player_1_hand_strength[1] = sum(int(i) for i in flush_cards[0:6])
            # print("Flush")
            # print("Player 1 hand strength"+ str(player_1_hand_strength))
            # print("Flush cards"+ str(flush_cards))
    output = cards
    return output
    # return "player_1_cards: " + player_1_cards + "player_2_cards: " + player_2_cards

def count_pairs(card_list):
    card_pairs = {}
    for card in card_list:
        value = card[0]
        if value in card_pairs:
            card_pairs[value] += 1
        else:
            card_pairs[value] = 1
    return card_pairs
for _ in range(1000000):
    poker_simulator()