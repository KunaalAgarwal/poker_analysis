import random
from treys import Card

deck = [
    "2c", "2d", "2h", "2s", "3c", "3d", "3h", "3s", "4c", "4d", "4h", "4s", 
    "5c", "5d", "5h", "5s", "6c", "6d", "6h", "6s", "7c", "7d", "7h", "7s", 
    "8c", "8d", "8h", "8s", "9c", "9d", "9h", "9s", "Tc", "Td", "Th", "Ts", 
    "Jc", "Jd", "Jh", "Js", "Qc", "Qd", "Qh", "Qs", "Kc", "Kd", "Kh", "Ks", 
    "Ac", "Ad", "Ah", "As"
]

def assign_placeholder_suits(hand): 
    suits = ['s', 'h', 'd', 'c']

    suit1 = suits[random.randint(0,3)]

    if 's' in hand: return [f"{hand[0]}{suit1}", f"{hand[1]}{suit1}"]

    else:
        suits.remove(suit1)        
        suit2 = suits[random.randint(0,2)]
        return [f"{hand[0]}{suit1}", f"{hand[1]}{suit2}"]
    

def ensure_unique_suits(*hands):
    """
    Ensures that each card across all given hands has a unique (rank + suit).
    If a collision is found, it reassigns the suit to one that's free.
    
    :param hands: Any number of lists (or tuples) representing hands, e.g.
                  hand1 = ["As", "Kd"], hand2 = ["Ad", "Ks"]
    :return: A list of the updated hands (or you can unpack the list).
    """
    suits = ['s', 'h', 'd', 'c']   # All possible suits
    used_cards = set()            # Tracks full 'rank+suit' combos in use
    
    updated_hands = []
    for hand in hands:
        updated_hand = []
        for card in hand:
            # If the exact card is already used, find a new suit for its rank
            if card in used_cards:
                # Suppose the rank is everything except the last character, which is suit
                # If your rank naming is always 1 char, e.g. 'A', 'K', 'Q', '9', etc.
                # Then you can do rank = card[0].
                # But if you have ranks like '10', do: rank = card[:-1]
                
                rank = card[0]  # adjust if your rank is more than 1 char
                # Find an available suit for this rank
                available_suits = [suit for suit in suits 
                                   if f"{rank}{suit}" not in used_cards]
                
                if available_suits:
                    new_card = f"{rank}{available_suits[0]}"
                    updated_hand.append(new_card)
                    used_cards.add(new_card)
                else:
                    # No suits left for this rank; fallback to the original card
                    # or handle it however you prefer
                    updated_hand.append(card)
            else:
                # Card is not in use, so add it
                updated_hand.append(card)
                used_cards.add(card)
        
        updated_hands.append(updated_hand)
    
    return updated_hands

def cards_to_treys(hand):
    # converts ['As','Kh'] to Treys format
    return [Card.new(card) for card in hand]