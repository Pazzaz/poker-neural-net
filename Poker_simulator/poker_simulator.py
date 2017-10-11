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
    player_1_hand_strength = 8
    player_2_hand_strength = 8
    board = cards[4:10]
    #print(board)
    player_1_hand = player_1_hole_cards + board
    player_2_hand = player_2_hole_cards + board
    # count_spades = 0
    # count_hearts = 0
    # count_diamonds = 0
    # count_clubs = 0
    suits_count_array = [0,0,0,0]
    flush_suit = -1
    for i in player_1_hand:
        suits_count_array[i[1]] += 1
    for i, suit in enumerate(suits_count_array):
        if suit >= 5:
            flush_suit = i
    
    flush_cards = [x[0] for x in player_1_hand if x[1] == flush_suit]
    if flush_cards is not None:
        flush_cards.sort()
        flush_cards.reverse()
        straight_flush_counter = 0
        for a, b in zip(flush_cards[:-1], flush_cards[1:]):
            if a == b+1:
                straight_flush_counter += 1
                if straight_flush_counter == 4:
                    player_1_hand_strength = 0
                    print(sorted(player_1_hand))
                    break
            else:
                straight_flush_counter = 0
        if player_1_hand_strength > 3:
            player_1_hand_strength = 3

        # if i[1] == 0:
        #     count_spades += 1
        # elif i[1] == 1:
        #     count_hearts += 1
        # elif i[1] == 2:
        #     count_diamonds += 1
        # elif i[1] == 3:
        #     count_clubs += 1
        # if count_spades >= 5 or count_hearts >= 5 or count_diamonds >= 5 or count_clubs >= 5

    # first_card = random.randint(0, 51)
    # first_card_value = first_card % 13
    # first_card_suit = first_card % 4
    # cards_drawn.append(first_card)
    # second_card = random.randint(0, 51)
    # while second_card in cards_drawn:
    #     second_card = random.randint(0, 51)
    # second_card_value = second_card % 13
    # second_card_suit = second_card % 4
    # cards_drawn.append(second_card)
    # third_card = random.randint(0, 51)
    # while third_card in cards_drawn:
    #     third_card = random.randint(0, 51)
    # third_card_value = third_card % 13
    # third_card_suit = third_card % 4
    # cards_drawn.append(third_card)
    # fourth_card = random.randint(0, 51)
    # while fourth_card in cards_drawn:
    #     fourth_card = random.randint(0, 51)
    # fourth_card_value = fourth_card % 13
    # fourth_card_suit = fourth_card % 4
    # cards_drawn.append(fourth_card)
    # player_1_cards = [[first_card_value, first_card_suit], [second_card_value, second_card_suit]]
    # player_2_cards = [[third_card_value, third_card_suit], [fourth_card_value, fourth_card_suit]]
    # player_1_cards_string = " ".join(str(x) for x in player_1_cards)
    # player_2_cards_string = " ".join(str(x) for x in player_2_cards)
    # output = "player_1_cards: " + player_1_cards_string + " player_2_cards: " + player_2_cards_string
    output = cards
    return output
    # return "player_1_cards: " + player_1_cards + "player_2_cards: " + player_2_cards

for _ in range(1000000):
    poker_simulator()