import random

def poker_simulator():
    cards_drawn = []
    first_card = random.randint(0, 51)
    first_card_value = first_card % 13
    first_card_suit = first_card % 4
    cards_drawn.append(first_card)
    second_card = random.randint(0, 51)
    while second_card in cards_drawn:
        second_card = random.randint(0, 51)
    second_card_value = second_card % 13
    second_card_suit = second_card % 4
    cards_drawn.append(second_card)
    third_card = random.randint(0, 51)
    while third_card in cards_drawn:
        third_card = random.randint(0, 51)
    third_card_value = third_card % 13
    third_card_suit = third_card % 4
    cards_drawn.append(third_card)
    fourth_card = random.randint(0, 51)
    while fourth_card in cards_drawn:
        fourth_card = random.randint(0, 51)
    fourth_card_value = fourth_card % 13
    fourth_card_suit = fourth_card % 4
    cards_drawn.append(fourth_card)
    player_1_cards = [[first_card_value, first_card_suit], [second_card_value, second_card_suit]]
    player_2_cards = [[third_card_value, third_card_suit], [fourth_card_value, fourth_card_suit]]
    player_1_cards_string = " ".join(str(x) for x in player_1_cards)
    player_2_cards_string = " ".join(str(x) for x in player_2_cards)
    output = "player_1_cards: " + player_1_cards_string + " player_2_cards: " + player_2_cards_string
    print(output)
    return output
    # return "player_1_cards: " + player_1_cards + "player_2_cards: " + player_2_cards

for _ in range(100):
    poker_simulator()