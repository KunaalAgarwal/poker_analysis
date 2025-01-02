"""
Flop classifications: 

Suit: 
- Monotone: all one suit
- Two-tone: presence of two suits (pigeonholed to make a front door flush draw) 
- Rainbow: presence of three suits

Pair: 
- Paired: presence of a pair
- Trips: presence of three of a kind on board

Connectivity: considers wheel draws where Ace is low and high.
- Highly connected: at least two pairwise comparisons of 2-rank differences (multiple straight draws and many combos)
- Moderately connected: one parwise comparison of 2-rank differences (single straight draw, fewer combos)
- Disconnected: no pairwise comparisons within 2-ranks of each other (no straight draw, no combos)

High card:
- Ace high
- King high

Also include wetness metric to evaluate flops. Considers drawing potential of the flops and uses the classifications from suits and connectivity. 

Wetness metric:
- Suits: 
    - Monotone: 2
    - Two-tone: 1
    - Rainbow: 0
- Conncetivity:
    - Highly connected: 2
    - Moderately connected: 1
    - Disconnected: 0

Wetness = Suits + Connectivity
-  Categorical from 0 to 4. 
-  >=2 is relatively wet, <2 is relatively dry.


Dynamic metric: considering the ability of the best made hands to change on the turn and river.
- Combination of wetness, pair/trips, and low-card flops (top-pair is highly dynamic).
- Pairing factor: 
    - Paired: 1
    - Trips: 2
- Low-card factor:
    -  High card <=9: 1

Dynamics = Wetness + Pairing factor + low-card factor
"""

import itertools

valid_suits = ['c', 'h', 'd', 's']
valid_ranks_mappings = {'A': [1, 14], '2': [2], '3': [3], '4': [4], '5': [5], '6': [6], '7': [7], 
                        '8': [8], '9': [9], 'T': [10], 'J': [11], 'Q': [12], 'K': [13]}
valid_ranks = list(valid_ranks_mappings.keys())

suit_score_mapping = {'Rainbow': 0, 'Two-tone': 1, 'Monotone': 2 }
connectivity_score_mapping = {'Disconnected': 0, 'Moderately connected': 1, 'Highly connected': 2}
pair_factor_mapping = {'Unpaired': 0, 'Paired': 1, 'Trips': 2}

def analyze_board_suits(board):   
    suits = set([card[1] for card in board])
    for suit in suits: 
        if suit not in valid_suits: 
            raise ValueError(f"Invalid suit: {suit}")
    suit_class = 'Rainbow'
    if (len(suits) == 1): suit_class = 'Monotone'
    elif (len(suits) == 2): suit_class = 'Two-tone'
    return suit_class
    
def analyze_board_connectivity(board):
    board_ranks = set([card[0] for card in board])
    for rank in board_ranks: 
        if rank not in valid_ranks: 
            raise ValueError(f"Invalid rank: {rank}")
    rank_class = 'Disconnected'
    connected_combos = 0
    for combination in itertools.combinations(board_ranks, 2): 
        if 'A' in combination: 
            if '2' in combination: connected_combos += 1
            elif 'K' in combination: connected_combos += 1
            elif 'Q' in combination: connected_combos += 1
        elif abs(valid_ranks_mappings[combination[0]][0] - valid_ranks_mappings[combination[1]][0]) <= 2: 
            connected_combos += 1

    if connected_combos >= 2: rank_class = 'Highly connected'
    elif connected_combos == 1: rank_class = 'Moderately connected'
    return rank_class

def analyze_board_pairing(board): 
    board_ranks = set([card[0] for card in board])
    if len(board_ranks) == 2: return 'Paired'
    if len(board_ranks) == 1: return 'Trips'
    return 'Unpaired'

def determine_dynamic_score(board): 
    suit_score = suit_score_mapping[analyze_board_suits(board)]
    rank_score = connectivity_score_mapping[analyze_board_connectivity(board)]
    pair_factor = pair_factor_mapping[analyze_board_pairing(board)]    

    board_ranks = [card[0] for card in board]
    low_card_factor = 0
    if max(board_ranks) <= '9': low_card_factor = 1

    return 1.5*suit_score + 1.5*rank_score + pair_factor + 0.75*low_card_factor

# board =  ['As', 'Ts', 'Td']
# print(analyze_board_suits(board))
# print(analyze_board_connectivity(board))
# print(analyze_board_pairing(board))
# print(determine_dynamic_score(board))