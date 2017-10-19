import random
import itertools

def poker_simulator(hand):
    hand_strength = [0, 0]
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
                    hand_strength = [8, straight_flush_strength]
                    return hand_strength
            else:
                straight_flush_counter = 0

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
    sorted_hand = [x[0] for x in sorted(hand, reverse=True)]
    for a, b in zip(sorted_hand[:-1], sorted_hand[1:]):
        if a == b+1 or (a == 12 and b == 3):
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
        else:
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

def get_hands():
    cards = []
    for i in range(52):
        value = i % 13
        suit = i % 4
        cards.append([value, suit])
    hands = itertools.combinations(cards, 7)
    return hands
    

# royal_flush = 0
# straight_flush = 0
# quads = 0
# full_house = 0
# flush = 0
# straight = 0
# threes = 0
# two_pair = 0
# pair = 0
# high_card = 0
distribution = [0,0,0,0,0,0,0,0,0]
total = 0
hands = get_hands()
for hand in hands:
    result = poker_simulator(list(hand))
    distribution[result[0]] += 1
    total += 1
    print(total)

print("Straight + Royal flush: " + str(distribution[8]) + " " + str(distribution[8] * 100 / total))
print("Quads: " + str(distribution[7]) + " " + str(distribution[7] * 100 / total))
print("Full house: " + str(distribution[6]) + " " + str(distribution[6] * 100 / total))
print("Flush: " + str(distribution[5])  + " " + str(distribution[5] * 100 / total))
print("Straight: " + str(distribution[4])  + " " + str(distribution[4] * 100 / total))
print("Threes: " + str(distribution[3])  + " " + str(distribution[3] * 100 / total))
print("Two pair: " + str(distribution[2])  + " " + str(distribution[2] * 100 / total))
print("Pair: " + str(distribution[1])  + " " + str(distribution[1] * 100 / total))
print("High card: " + str(distribution[0])  + " " + str(distribution[0] * 100 / total))