import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

hands = [
    "AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
    "AKo", "KK", "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
    "AQo", "KQo", "QQ", "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
    "AJo", "KJo", "QJo", "JJ", "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s",
    "ATo", "KTo", "QTo", "JTo", "TT", "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s",
    "A9o", "K9o", "Q9o", "J9o", "T9o", "99", "98s", "97s", "96s", "95s", "94s", "93s", "92s",
    "A8o", "K8o", "Q8o", "J8o", "T8o", "98o", "88", "87s", "86s", "85s", "84s", "83s", "82s",
    "A7o", "K7o", "Q7o", "J7o", "T7o", "97o", "87o", "77", "76s", "75s", "74s", "73s", "72s",
    "A6o", "K6o", "Q6o", "J6o", "T6o", "96o", "86o", "76o", "66", "65s", "64s", "63s", "62s",
    "A5o", "K5o", "Q5o", "J5o", "T5o", "95o", "85o", "75o", "65o", "55", "54s", "53s", "52s",
    "A4o", "K4o", "Q4o", "J4o", "T4o", "94o", "84o", "74o", "64o", "54o", "44", "43s", "42s",
    "A3o", "K3o", "Q3o", "J3o", "T3o", "93o", "83o", "73o", "63o", "53o", "43o", "33", "32s",
    "A2o", "K2o", "Q2o", "J2o", "T2o", "92o", "82o", "72o", "62o", "52o", "42o", "32o", "22",
]

COLORS = {
    "raise": "red",
    "call": "yellow",
    "fold": "grey"
}

OVERALL_COMBOS = 1326 # Total number of possible starting hands
DISTINCT_HANDS = 169  # Total number of distinct starting hands

# Reshape the hands into a 13x13 grid
hands_grid = np.array(hands).reshape(13, 13)

# input to range constructor will be dictorionary with keys as hands and values as a dict of frequencies with the appropriate action.
"""
range = {"AA": {'raise': 0.5, 'call': 0.5}, "AKs": {'raise': 0.8, 'call': 0.2}, ...}
"""

def generate_range(hand_actions, title=""):
    """
    Generate a 13x13 grid based on input actions for each hand and visualize it as a heatmap.
    Args:
        hand_actions (dict): Dictionary with hands as keys and actions as values.
                            Example: {"AA": {"raise": 1.0, "call": 0.0, "fold": 0.0}}
        title (str): Title for the heatmap.
    """
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 10))  # Extend width to accommodate the legend

    for idx, hand in enumerate(hands_grid.flatten()):
        row, col = divmod(idx, 13)  # Map linear index to 2D grid
        if hand in hand_actions:
            actions = hand_actions[hand]
            x, y = col - 0.5, row - 0.5

            # Draw each action proportionally
            bottom = y

            total = sum(actions.values())
            if total < 1: 
                actions['fold'] = 1 - total  # Fill the rest with fold action

            for action, freq in actions.items():
                if freq > 0:  # Only plot if the frequency is greater than 0
                    height = freq
                    ax.add_patch(plt.Rectangle(
                        (x, bottom), 1, height, facecolor=COLORS[action], edgecolor='black', lw=0.5
                    ))
                    bottom += height
        else: # If the hand is not in the input, fill it with a default color
            ax.add_patch(plt.Rectangle((col - 0.5, row - 0.5), 1, 1, facecolor=COLORS["fold"], edgecolor='black', lw=0.5))

    # Add text annotations for hands
    for idx, hand in enumerate(hands):
        row, col = divmod(idx, 13)
        ax.text(col, row, hand, ha="center", va="center", fontsize=10)

    # Format the axes
    ax.set_xticks(range(13))
    ax.set_yticks(range(13))
    ax.set_xticklabels(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"], fontsize=12)
    ax.set_yticklabels(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"], fontsize=12)
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-0.5, 12.5)
    ax.set_title(title, fontsize=16)
    ax.invert_yaxis()

    # Add legend for the colors
    import matplotlib.patches as mpatches
    legend_patches = [
        mpatches.Patch(color=color, label=action.capitalize())
        for action, color in COLORS.items()
    ]
    ax.legend(handles=legend_patches, loc="upper right", title="Actions", bbox_to_anchor=(1.2, 1))

    plt.tight_layout()
    plt.show()

def hand_combos_multiplier(hand):
    if len(hand) == 2: 
        return 6
    elif hand[2] == 's':
        return 4
    return 12

def range_percent_by_actions(hand_actions, action='raise'):
    total = 0
    for hand, frequencies in hand_actions.items(): 
        if (frequencies[action] > 0): 
            total += hand_combos_multiplier(hand)*frequencies[action]
    return (total/OVERALL_COMBOS)*100, total

def range_percent_by_all_actions(hand_actions): 
    # Returns the percent of the combos in the range that perform certain actions relative to the total number of combinations
    raise_percent, raise_combos = range_percent_by_actions(hand_actions, 'raise')
    call_percent, call_combos = range_percent_by_actions(hand_actions, 'call')
    fold_percent = 100 - raise_percent - call_percent
    fold_combos = OVERALL_COMBOS - raise_combos - call_combos
    overall_percent, overall_combos = (raise_combos + call_combos)/OVERALL_COMBOS*100, raise_combos + call_combos
    return {
        'raise': {'percent': raise_percent, 'combos': raise_combos},
        'call': {'percent': call_percent, 'combos': call_combos},
        'fold': {'percent': fold_percent, 'combos': fold_combos},
        'overall': {'percent': overall_percent, 'combos': overall_combos}
    }

def range_hand_distribution(hand_actions, actions_list=['raise', 'call']):
    # Explores the ranks of all hands in the range
    # Returns the summary_stats (mean, min, max, etc.), average hand percentile, and the ranks dataframe
    hands = set()
    for hand, actions in hand_actions.items(): 
        for action in actions_list:
            if actions[action] > 0: 
                hands.add(hand)

    ranks = pd.read_csv('../results/preflop_equity.csv')
    ranks = ranks[ranks['hand'].isin(hands)]
    summary_stats = ranks['Rank'].describe()
    return summary_stats, ranks

def average_range_rank(hand_actions, actions_list=['raise', 'call']): 
    # Returns the weighted average rank of all hands in the range considering the frequencies of actions
    ranks = []
    hand_ranks = pd.read_csv('../results/preflop_equity.csv')
    for hand, actions in hand_actions.items(): 
        for action, frequency in actions.items(): 
            if frequency > 0 and action in actions_list: 
                hand_rank = hand_ranks[hand_ranks['hand'] == hand]
                ranks.append(hand_rank['Rank']*frequency)
    return np.mean(ranks) 

def percent_range_high_card(hand_actions):
    # checks the percentage of the range that is K or A high+
    # PFR generally indicates that the range is skewed towards high card hands-
    # and we want to connect with A and K high boards.  
    total = 0
    total_range_combos = range_percent_by_all_actions(hand_actions)['overall']['combos']
    for hand, action in hand_actions.items(): 
        freq = action['raise'] + action['call']
        if 'A' in hand or 'K' in hand: 
            total += hand_combos_multiplier(hand)*freq
    return (total/total_range_combos)*100


# need to start thinking about comparisons between ranges
# will use the preflop matchups equities to compare equities between ranges

def range_comparison_percent_dominated(hand_actions_1, hand_actions_2): 
    # Given two ranges, calculate the percentage of hands that are dominated by one range over the other
    return NotImplemented