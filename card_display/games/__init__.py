import abc
from pathlib import Path
from typing import Generator, List
from card_display.deck import Card, CardDeck


class Game(abc.ABC):
    hand_count: int
    """The number of cards in a singular hand"""

    deck_file: str
    """The filename of the deck to lad"""

    name: str
    """The name of the game"""

    max_hands_per_deck: int
    """The maximum number of hands which can be played out of a single deck.
    Typically this is the number of cards divided by the number of hands"""

    def __init__(self):
        self.deck = CardDeck.from_file(Path(__file__).parent / self.deck_file)

    def deal_hand(self) ->  Generator[None, Card, None]:
        """
        Deals a hand of hand_count size
        """
        for card in self.deck.deal_cards(self.hand_count):
            yield card

    @abc.abstractmethod
    def calculate_hand_points(self, cards: List[Card]):
        pass

class BridgeGame(Game):
    name = "Bridge"
    hand_count = 10
    deck_file = "bridge1.txt"
    max_hands_per_deck = 52//10


    def calculate_hand_points(self, cards: List[Card]):
        return len(cards)
        

class OtherBridgeGame(Game):
    name = "Other Bridge"
    hand_count = 10
    deck_file = "bridge1.txt"
    max_hands_per_deck = 52//10


    def calculate_hand_points(self, cards: List[Card]):
        return len(cards)
        

if __name__ == "__main__":
    print(list(BridgeGame().deal_hand()))