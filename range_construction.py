import matplotlib.pyplot as plt
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

# Reshape the hands into a 13x13 grid
hands_grid = np.array(hands).reshape(13, 13)

# input to range constructor will be dictorionary with keys as hands and values as a dict of frequencies with the appropriate action.
"""
range = {"AA": {'raise': 0.5, 'call': 0.5}, "AKs": {'raise': 0.8, 'call': 0.2}, ...}
"""

def generate_range(hand_actions, title="Poker Hands Heatmap with Actions"):
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

def range_percent_overall(hand_actions): 
    hand_types = {'pocket_pair': 0, 'suited': 0, 'offsuit': 0}
    for hand in hand_actions.keys():
        if (len(hand) == 2): 
            hand_types['pocket_pair'] = hand_types.get('pocket_pair', 0) + 1
        elif (hand[2] == 's'):
            hand_types['suited'] = hand_types.get('suited', 0) + 1
        else:
            hand_types['offsuit'] = hand_types.get('offsuit', 0) + 1
    
    combos = hand_types['pocket_pair']*6 + hand_types['suited']*4 + hand_types['offsuit']*12
    return (combos/OVERALL_COMBOS)*100, combos

def range_percent_by_actions(hand_actions, action='raise'):
    total = 0
    for hand, frequencies in hand_actions.items(): 
        if (frequencies[action] > 0): 
            hand_combos = 12
            if (len(hand) == 2): 
                hand_combos = 6
            elif (hand[2] == 's'): 
                hand_combos = 4
            total += hand_combos*frequencies[action]
    return (total/OVERALL_COMBOS)*100, total

def range_distribution(): 
    return NotImplemented

# need to start thinking about comparisons between ranges

def range_comparison_percent_dominated(hand_actions_1, hand_actions_2): 
    # Given two ranges, calculate the percentage of hands that are dominated by one range over the other
    return NotImplemented