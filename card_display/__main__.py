from card_display.games import Game
import inquirer
from card_display.utils import subclass_recursive


def validate_hand_count(answers, current):
    try:
        return answers["game"].max_hands_per_deck >= int(current) and int(current) > 0
    except ValueError:
        return False


# A list of questions to ask the user before starting
questions = [
    inquirer.List(
        "game",
        message="What game are we playing?",
        choices=[(klass.name, klass) for klass in subclass_recursive(Game)],
    ),
    inquirer.Text(
        "hand count",
        message="How many {game.name} hands would you like to deal?",
        validate=validate_hand_count,
    ),
]

# Ask the questions to the user
answers = inquirer.prompt(questions)

# Create a new instance of the selected game
game = answers["game"]()

# Get the hands delt to the user
hands = [list(game.deal_hand()) for _ in range(int(answers["hand count"]))]

for i, hand in enumerate(hands):
    print(f"Hand {i+1:02d}:  ", end="")

    for card in hand:
        print(card.unicode_suit_card, end=" ")

    print(f" Score: {game.calculate_hand_points(hand)}")
