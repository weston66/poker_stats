import pandas as pd
import numpy as np
import itertools
import random

#ANALYZING THE COMBINATIONS OF BOARDS
#option to set testing seed
#random.seed(5)
rand = random.randint(0, 2598960)
print(rand)

#BUILD THE DECK
#the deckl is populated by parsing the numbers list and the suits list into the decks array
numbers = list(range(2,15))
suits = ['H', 'S', 'C', 'D']
deck = []

for i in numbers:
    for s in suits:
        card = s+str(i)
        deck.append(card)

#CREATE ARRAY OF ALL POSSIBLE HAND OUTCOMES OF 5 CARDS
#52! / (5! * (52-5)!) = 2,598,960 possible unique outcomes
all_possible_boards = []
for i in itertools.combinations(deck, 5):
    all_possible_boards.append(i)

#SEPERATE SUITS AND VALUES
def get_suit_value(hand):
    value = []
    suit = []
    i = 0
    while i<5:
        suit.append(hand[i][0])
        value.append(int(hand[i][1:]))
        i += 1
    return suit, value

#COUNT SUITS AND VALUES FREQUENCY
#ONLY RETURNS THE FREQUENCY FOR CALUCULATIONS
def count_suit_value(suit, value):
    value_count = []
    for n in set(value):
        value_count.append(int(value.count(n)))

    value_count_max = max(value_count)

    suit_count = []
    for m in set(suit):
        suit_count.append(suit.count(m))

    suit_count_max = max(suit_count)

    return value_count_max, suit_count_max

#IDENTIFYERS OF ALL POSSIBLE HAND COMBINDATIONS IN ORDER BEST TO WORST
#royal flush, straight flush, quads, full house, flush, straight, three of a kind, two pair, pair, high card
def best_combination(value, suit, value_count_max, suit_count_max):
    combo = ""
    if suit_count_max == 5: #flush containing combinations: flush, straight flush, royal flush        
        #special case where ace is low
        if sorted(value) == [2, 3, 4, 5, 14]:
            combo = "Straight Flush"
        else:
            i = 1
            while i < 5:
                if (sorted(value)[i] == sorted(value)[i-1]+1) == True:
                    if i == 4:
                        if sorted(value)[i] == 14:
                            combo = "Royal Flush"
                        else:
                            combo = "Straight Flush"
                        i += 1
                    else:
                        i += 1
                else:
                    combo = "Flush" 
                    break

    #check all non-flush combinations for best combo of hands
    #if value frequency is 1: highcard or straight, 2: pair or two pair, 3: three of a kind or full house, 4:quads
    else:
        #count the pair, we will use this in conjuction with the value_max_count to determine combo        
        pair_count = []
        if len(set(value)) != 5:
            for p in set(value):
                if value.count(p) == 2:
                    pair_count.append(int(p))

        #check quads
        if value_count_max == 4:
            combo = "Quads"

        #check full house if not then three of a kind
        elif value_count_max == 3:
            if len(pair_count) == 1:
                combo = "Full House"
            else:
                combo = "Three of a Kind"
        
        #check two pair if not then one pair
        elif value_count_max == 2:
            if len(pair_count) == 2:
                combo = "Two Pair"
            else:
                combo = "Pair"

        #check straight if not then high card
        else:
            i = 1
            while i < 5:
                if (sorted(value)[i] == sorted(value)[i-1]+1) == True or sorted(value) == [2, 3, 4, 5, 14]:
                    if i == 4:
                        combo = "Straight"
                        i += 1
                    else:
                        i += 1
                else:
                    combo = "High Card"
                    break
    return combo

#SCORING MOD
def scoring(combo, suit, value):
    if combo == "High Card": #score 1<x<15
        score = sorted(value, reverse=True)[0] + sorted(value, reverse=True)[1]/100 + sorted(value, reverse=True)[2]/1000 
        + sorted(value, reverse=True)[3]/10000 + sorted(value, reverse=True)[4]/100000
    
    elif combo == "Pair": #score 15<x<28
        pair = []
        no_pair = []
        for i in value:
            if value.count(i) == 2:
                if i not in pair:
                    pair.append(i)
                else:
                    pass
            else:
                no_pair.append(i)

        score = 13 + pair[0] + sorted(no_pair, reverse=True)[0]/100 + sorted(no_pair, reverse=True)[1]/1000 + sorted(no_pair, reverse=True)[2]/10000
    
    elif combo == "Two Pair": #score 28<x<41
        pair = []
        no_pair = []
        for i in value:
            if value.count(i) == 2:
                if i not in pair:
                    pair.append(i)
                else:
                    pass
            else:
                no_pair.append(i)

        score = 26 + sorted(pair, reverse=True)[0] + sorted(pair, reverse=True)[1]/100 + sorted(no_pair, reverse=True)[0]/1000

    elif combo == "Three of a Kind": # score 41<x<54
        threes = []
        no_threes = []
        for i in value:
            if value.count(i) == 3:
                if i not in threes:
                    threes.append(i)
                else:
                    pass
            else:
                no_threes.append(i)

        score = 39 + threes[0] + sorted(no_threes, reverse=True)[0]/100 + sorted(no_threes, reverse=True)[1]/1000

    elif combo == "Straight": #just high card in the range from 5 to A(14): score 54<=x<63
        if sorted(value) == [2, 3, 4, 5, 14]:
            score = 54
        else:
            score = 49 + max(value)
    
    elif combo == "Flush": #same as high card: score 63<x<76
        score = 61 + sorted(value, reverse=True)[0] + sorted(value, reverse=True)[1]/100 + sorted(value, reverse=True)[2]/1000 
        + sorted(value, reverse=True)[3]/10000 + sorted(value, reverse=True)[4]/100000

    elif combo == "Full House": # score 76<x<89
        threes = []
        pair = []
        for i in value:
            if value.count(i) == 3:
                if i not in threes:
                    threes.append(i)
                else:
                    pass
            else:
                pair.append(i)

        score = 74 + threes[0] + pair[0]/100

    elif combo == "Quads": # score 89<x<102
        quads = []
        high = []
        for i in value:
            if value.count(i) == 4:
                if i not in quads:
                    quads.append(i)
                else:
                    pass
            else:
                high.append(i)
        score = 87 + quads[0] + high[0]/100

    elif combo == "Straight Flush": #straight in the new range: score 102<=x<111
        if sorted(value) == [2, 3, 4, 5, 14]:
            score = 102
        else:
            score = 97 + max(value)

    else: #Royal Flush
        score = 112 #max score 112

    return score

#tester goods
# h=all_possible_boards[rand]
# print(h)

# suit = get_suit_value(h)[0]
# value = get_suit_value(h)[1]
# print(get_suit_value(h))

# value_count_max = count_suit_value(get_suit_value(h)[0], get_suit_value(h)[1])[0]
# suit_count_max = count_suit_value(get_suit_value(h)[0], get_suit_value(h)[1])[1]
# print(value_count_max)
# print(suit_count_max)

# print(best_combination(value, suit, value_count_max, suit_count_max))

# TESTER FUNCTION USED TO RUN ALL POSSIBLE HAND COMBOS
def tester(hand):
    suit, value = get_suit_value(hand)
    value_count_max, suit_count_max = count_suit_value(suit, value)
    combo = best_combination(value, suit, value_count_max, suit_count_max)
    score = scoring(combo, suit, value)

    return hand, combo, score

# CREATE A ARRAY OF [[COMBO], [SCORE]] FOR ANALYSIS
score_and_combo = []
for boards in all_possible_boards:
    score_and_combo.append(tester(boards))

#print(score_and_combo[:10])

# MAKE A PD DATAFRAME FOR DATA ANALYSIS
hand_stats = pd.DataFrame({'Hand':score_and_combo[0], 'Combo':score_and_combo[1], 'Score':score_and_combo[2]})
print(hand_stats.head())