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

def find_streets(sorted_cards, nostreets):
    rank_to_value = {
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

    def get_rank_value(card):
        return rank_to_value[card[0]]

    def is_street(ranks):
        unique_ranks = set(ranks)
        if len(unique_ranks) != 5:
            return False
        sorted_ranks = sorted(ranks)
        if sorted_ranks[-1] - sorted_ranks[0] == 4:
            for i in range(4):
                if sorted_ranks[i+1] - sorted_ranks[i] != 1:
                    break
            else:
                return True

        if sorted_ranks == [2, 3, 4, 5, 14]:
            return True

        return False

    combos = []
    n = len(sorted_cards)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                for l in range(k+1, n):
                    for m in range(l+1, n):
                        combo = [
                            sorted_cards[i], sorted_cards[j],
                            sorted_cards[k], sorted_cards[l],
                            sorted_cards[m]
                        ]
                        combos.append(combo)

    streets = []
    for combo in combos:
        ranks = [get_rank_value(card) for card in combo]
        if is_street(ranks) and not combo in nostreets:
            streets.append(combo)

    return streets

def find_flushes(sorted_cards, noflushes):
    suits_dict = {}
    for card in sorted_cards:
        suit = card[1]
        if suit not in suits_dict:
            suits_dict[suit] = []
        suits_dict[suit].append(card)

    flushes = []
    for suit, cards in suits_dict.items():
        if len(cards) < 5:
            continue

        n = len(cards)
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    for l in range(k+1, n):
                        for m in range(l+1, n):
                            combo = [
                                cards[i], cards[j],
                                cards[k], cards[l],
                                cards[m]
                            ]
                            if not combo in noflushes:
                                flushes.append(combo)
    
    return flushes

def find_fullhouses(cards, nofullhouses):
    trips = find_trips(cards, [])
    pairs = find_pairs(cards, [])
    complete = []
    for trip in trips:
        for pair in pairs:
            if trip[0][0] != pair[0][0] and not (trip, pair) in nofullhouses:
               complete.append((trip, pair))
    return complete

def find_quads(cards, noquads):
    pairs = find_pairs(cards, [])
    complete = []
    for i in range(len(pairs)):
       for j in range(i + 1, len(pairs)):
            if pairs[i][0][0] == pairs[j][0][0] and not ((pairs[i][0], pairs[i][1], pairs[j][0], pairs[j][1])) in noquads and pairs[i][0] != pairs[j][0] and  pairs[i][0] != pairs[i][1] and pairs[i][1] != pairs[j][0] and pairs[i][1] != pairs[j][1]:
                flag = True
                for compl in complete:
                    if compl[0][0] == pairs[i][0][0]:
                        flag = False
                for noquad in noquads:
                    if noquad[0][0] == pairs[i][0][0]:
                        flag = False
                if flag:
                    complete.append((pairs[i][0], pairs[i][1], pairs[j][0], pairs[j][1]))
    return complete

def find_streetflushes(cards, nostreetflush):
    streets = find_streets(cards, [])
    complete = []
    for street in streets:
        if street[0][1] == street[1][1] and street[1][1] == street[2][1] and street[2][1] == street[3][1] and street[3][1] == street[4][1] and not street in nostreetflush:
            complete.append(street)
    return complete

def find_royalflushes(cards, noroyalflushes):
    streetflushes = find_streetflushes(cards, [])
    complete = []
    for sf in streetflushes:
        if sf[0][0] == 'T' and sf[-1][0] == 'A' and not sf in noroyalflushes:
            complete.append(sf)
    return complete
 
print('Все пары игрока: ', find_pairs(sort_cards(userhand + table), find_pairs(sort_cards(table), [])))
print('Все пары бота: ', find_pairs(sort_cards(bothand + table),  find_pairs(sort_cards(table), [])))
print('Все сеты игрока: ', find_trips(sort_cards(userhand + table), find_trips(sort_cards(table), [])))
print('Все сеты бота: ', find_trips(sort_cards(bothand + table),  find_trips(sort_cards(table), [])))
print('Все две пары игрока: ', find_two_pairs(find_pairs(sort_cards(userhand + table), find_pairs(sort_cards(table), []))))
print('Все две пары бота: ', find_two_pairs(find_pairs(sort_cards(bothand + table), find_pairs(sort_cards(table), []))))
print('Все стриты игрока: ', find_streets(sort_cards(userhand + table), find_streets(sort_cards(table), [])))
print('Все стриты бота: ', find_streets(sort_cards(bothand + table), find_streets(sort_cards(table), [])))
print('Все флешы игрока: ', find_flushes(sort_cards(userhand + table), find_flushes(sort_cards(table), [])))
print('Все флешы бота: ', find_flushes(sort_cards(bothand + table), find_flushes(sort_cards(table), [])))
print('Все фуллхаусы игрока: ', find_fullhouses(sort_cards(userhand + table), find_fullhouses(sort_cards(table), [])))
print('Все фуллхаусы бота: ', find_fullhouses(sort_cards(bothand + table), find_fullhouses(sort_cards(table), [])))
print('Все каре игрока: ', find_quads(sort_cards(userhand + table), find_quads(sort_cards(table), [])))
print('Все каре бота: ', find_quads(sort_cards(bothand + table), find_quads(sort_cards(table), [])))
print('Все стритфлешы игрока: ', find_streetflushes(sort_cards(userhand + table), find_streetflushes(sort_cards(table), [])))
print('Все стритфлешы бота: ', find_streetflushes(sort_cards(bothand + table), find_streetflushes(sort_cards(table), [])))
print('Все роялфлешы игрока: ', find_royalflushes(sort_cards(userhand + table), find_royalflushes(sort_cards(table), [])))
print('Все роялфлешы бота: ', find_royalflushes(sort_cards(bothand + table), find_royalflushes(sort_cards(table), [])))
