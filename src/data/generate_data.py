# import packages
import random
import pandas as pd
from itertools import combinations
from multiprocessing import Pool

# create collection with all 54 cards
all_cards = {
    "circle": [1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14],
    "triangle": [1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14],
    "cross": [1, 2, 3, 5, 7, 10, 11, 13, 14],
    "square": [1, 2, 3, 5, 7, 10, 11, 13, 14],
    "star": [1, 2, 3, 4, 5, 7, 8],
    "whot": [20, 20, 20, 20, 20]
}


# create deck
def deck():
    deck = []
    for shape, numbers in all_cards.items():
        for num in numbers:
            deck.append((shape, num))
    return deck


# method to deal cards to players
def deal_cards(deck):
    hand_size = random.randint(1, 4)
    hands_player = random.sample(deck, k=hand_size)
    for card in hands_player:
        deck.remove(card)
    return hands_player


# method to deal call cards
def deal_call_card(deck):
    call_card = random.choice(deck)
    deck.remove(call_card)
    return call_card


# method to help simulate requesting a suit when the call card is a 20.
def get_requested_suit(hand):
    for card in hand:
        if card[0] != "whot":
            return card[0]
    return "circle"  # default if all player cards are whot cards


# method to pad players hand if they have less than 4 cards
def pad_hand(player_hand):
    while len(player_hand) < 4:
        player_hand.append(("none", 0))
    return player_hand


# method to simulate the rules of the game for a valid play
def get_valid_action(hand, call_card, requested_suit, special_state):
    call_card_shape, call_card_rank = call_card

    if special_state == "GENERAL_MARKET":
        return "go market"

    if special_state in ("PICK_TWO", "PICK_THREE"):
        for card in hand:
            _, rank = card
            if rank == call_card_rank:
                return f"{card[0]} {card[1]}"
        return "go market"

    if special_state == "WHOT":
        for card in hand:
            shape, _ = card
            if shape == requested_suit or shape == "whot":
                return f"{card[0]} {card[1]}"
        return "go market"

    if special_state == "NONE":
        for card in hand:
            shape, rank = card
            if shape == call_card_shape or rank == call_card_rank or shape == "whot":
                return f"{card[0]} {card[1]}"
        return "go market"


# method to determine next valid play given player cards and call card. used for combination generation
def get_valid_action_comb(player_cards, call_card):
    for card in player_cards:
        if card[1] in (2, 3, 14, 20):
            return "go market"
        if card[0] == call_card[0] or card[1] == call_card[1]:
            return card
    return "go market"


def process_data(plays):
    data = []
    for play in plays:
        row_data = []
        for card in play["cards"]:
            row_data.append(" ".join([str(card_value) for card_value in card]))
        row_data.append(" ".join([str(card_value) for card_value in play["played"]]))
        if isinstance(play["action"], tuple):
            row_data.append(" ".join([str(card_value) for card_value in play["action"]]))
        else:
            row_data.append(play["action"])
        data.append(row_data)
    return data


def generate_all_combs():
    all_combinations = []

    for combination in combinations(deck(), 4):
        all_combinations.append(combination)

    plays = []
    for cards in all_combinations:
        for call_card in deck():
            if call_card not in cards:
                plays.append({
                    "cards": cards,
                    "played": call_card,
                    "action": get_valid_action_comb(cards, call_card)
                })

    with Pool() as p:
        results = p.map(process_data, [plays[i:i + 1000] for i in range(0, len(plays), 1000)])

    data = [row for result in results for row in result]

    df = pd.DataFrame(data, columns=[*[f'Card {i + 1}' for i in range(4)] + ['Call Card', 'Action']])
    df["Requested Suit"] = "NONE"
    df["Special State"] = "NONE"
    return df


def generate_additional_rows(num_rows):
    rows = []
    for num in range(num_rows):
        card_deck = deck()
        player_hands = deal_cards(card_deck)
        call_card = deal_call_card(card_deck)

        if call_card[1] == 20:
            special_state = "WHOT"
        elif call_card[1] in (2, 5, 14):
            special_state = random.choice(
                ["NONE", {2: "PICK_TWO", 5: "PICK_THREE", 14: "GENERAL_MARKET"}[call_card[1]]])
        else:
            special_state = "NONE"
        requested_suit = "NONE"
        if special_state == "WHOT":
            requested_suit = get_requested_suit(player_hands)

        action = get_valid_action(player_hands, call_card, requested_suit, special_state)
        padded_player_hands = pad_hand(player_hands.copy())
        padded_player_hands = [f"{card[0]} {card[1]}" for card in padded_player_hands]
        row = padded_player_hands + [f"{call_card[0]} {call_card[1]}"] + [requested_suit, special_state, action]
        rows.append(row)

    # create column names
    columns = [f"Card {i + 1}" for i in range(len(padded_player_hands))] + ["Call Card", "Requested Suit",
                                                                            "Special State",
                                                                            "Action"]
    df = pd.DataFrame(data=rows, columns=columns)
    return df


if __name__ == "__main__":
    df_combination = generate_all_combs()
    df_random = generate_additional_rows(5000000)

    df = pd.concat([df_combination, df_random], ignore_index=True)
    #df.to_csv("data/whot_dataset.csv")
