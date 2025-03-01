import random


suits = [
    'H',
    'D',
    'C',
    'S'
]
denomination = [
    'A',
    'K',
    'Q',
    'J',
    'T',
    '9',
    '8',
    '7',
    '6',
    '5',
    '4',
    '3',
    '2'
]
deck = [denom + suit for denom in denomination for suit in suits]
table = []

def get_card_from_deck():
    card = random.choice(deck)
    deck.remove(card)
    return card

userhand = [get_card_from_deck(), get_card_from_deck()]
bothand = [get_card_from_deck(), get_card_from_deck()]
table = [get_card_from_deck(), get_card_from_deck(), get_card_from_deck(), get_card_from_deck(), get_card_from_deck()]
print('Карты в колоде: ', deck)
print('Карты игрока: ', userhand)
print('Карты бота: ', bothand)
print('Карты на столе: ', table)

def comare_denomination_bigger(frst_card, scnd_card):
    frst_denom, scnd_denom = frst_card[0], scnd_card[0]
    if denomination.index(frst_denom) < denomination.index(scnd_denom):
        return frst_card
    else:
        return scnd_card

bigger_userhand = comare_denomination_bigger(userhand[0], userhand[1])
bigger_bothand = comare_denomination_bigger(bothand[0], bothand[1])

def sort_cards(cards):
    for i in range(1, len(cards)):
        key = cards[i]
        j = i - 1
        while j >= 0 and denomination.index(key[0]) > denomination.index(cards[j][0]):
            cards[j + 1] = cards[j]
            j -= 1
        cards[j + 1] = key
    return cards

def find_pairs(cards, nopairs):
    rank_groups = {}
    for card in cards:
        rank = card[0] 
        if rank not in rank_groups:
            rank_groups[rank] = []
        rank_groups[rank].append(card)
    
    pairs = []
    for group in rank_groups.values():
        n = len(group)
        for i in range(n):
            for j in range(i + 1, n):
                if not (group[i], group[j]) in nopairs:
                     pairs.append((group[i], group[j]))
    
    return pairs

def find_two_pairs(pairs):
    complete = []
    if len(pairs) > 1:
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                complete.append((pairs[i], pairs[j]))
    return complete 

def find_trips(cards, notrips):
    rank_groups = {}
    for card in cards:
        rank = card[0]
        if rank not in rank_groups:
            rank_groups[rank] = []
        rank_groups[rank].append(card)
    
    trips = []
    for group in rank_groups.values():
        n = len(group)
        if n >= 3:
            for i in range(n):
                for j in range(i+1, n):
                    for k in range(j+1, n):
                        if not (group[i], group[j], group[k]) in notrips:
                            trips.append((group[i], group[j], group[k]))
    
    return trips

def find_street(cards, nostreets):
    ranks = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    values = []
    pre_compl = []
    for card in cards:
        values.append(ranks.get(card[:-1], 0))
    uniq_val = sorted(list(set(values)))
    if len(uniq_val) >= 5:
        if 14 in uniq_val and 2 in uniq_val and 3 in uniq_val and 4 in uniq_val and 5 in uniq_val:
            pre_compl.append([14, 2, 3, 4, 5])
        if len(uniq_val) == 5 and uniq_val[0] + 1 == uniq_val[1] and uniq_val[1] + 1 == uniq_val[2] and uniq_val[2] + 1 == uniq_val[3] and uniq_val[3] + 1 == uniq_val[4]:
            pre_compl.append([uniq_val[0], uniq_val[1], uniq_val[2], uniq_val[3], uniq_val[4]])
        elif len(uniq_val) == 6:
            if uniq_val[0] + 1 == uniq_val[1] and uniq_val[1] + 1 == uniq_val[2] and uniq_val[2] + 1 == uniq_val[3] and uniq_val[3] + 1 == uniq_val[4]:
                pre_compl.append([uniq_val[0], uniq_val[1], uniq_val[2], uniq_val[3], uniq_val[4]])
            if uniq_val[1] + 1 == uniq_val[2] and uniq_val[2] + 1 == uniq_val[3] and uniq_val[3] + 1 == uniq_val[4] and uniq_val[4] + 1 == uniq_val[5]:
                pre_compl.append([uniq_val[1], uniq_val[2], uniq_val[3], uniq_val[4], uniq_val[5]])
        elif len(uniq_val) == 7:
            if uniq_val[0] + 1 == uniq_val[1] and uniq_val[1] + 1 == uniq_val[2] and uniq_val[2] + 1 == uniq_val[3] and uniq_val[3] + 1 == uniq_val[4]:
                pre_compl.append([uniq_val[0], uniq_val[1], uniq_val[2], uniq_val[3], uniq_val[4]])
            if uniq_val[1] + 1 == uniq_val[2] and uniq_val[2] + 1 == uniq_val[3] and uniq_val[3] + 1 == uniq_val[4] and uniq_val[4] + 1 == uniq_val[5]:
                pre_compl.append([uniq_val[1], uniq_val[2], uniq_val[3], uniq_val[4], uniq_val[5]])
            if uniq_val[2] + 1 == uniq_val[3] and uniq_val[3] + 1 == uniq_val[4] and uniq_val[4] + 1 == uniq_val[5] and uniq_val[5] + 1 == uniq_val[6]:
                pre_compl.append([uniq_val[2], uniq_val[3], uniq_val[4], uniq_val[5], uniq_val[6]])
 
print('Все пары игрока: ', find_pairs(sort_cards(userhand + table), find_pairs(sort_cards(table), [])))
print('Все пары бота: ', find_pairs(sort_cards(bothand + table),  find_pairs(sort_cards(table), [])))
print('Все сеты игрока: ', find_trips(sort_cards(userhand + table), find_trips(sort_cards(table), [])))
print('Все сеты бота: ', find_trips(sort_cards(bothand + table),  find_trips(sort_cards(table), [])))
print('Все две пары игрока: ', find_two_pairs(find_pairs(sort_cards(userhand + table), find_pairs(sort_cards(table), []))))
print('Все две пары бота: ', find_two_pairs(find_pairs(sort_cards(bothand + table), find_pairs(sort_cards(table), []))))
