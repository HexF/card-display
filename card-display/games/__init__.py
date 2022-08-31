import abc
from pathlib import Path
from typing import Generator, List
from ..deck import Card, CardDeck


# Abstract Base Class

class Game(abc.ABC):
    hand_count: int
    deck_file: str

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
    hand_count = 3
    deck_file = "bridge1.txt"


    def calculate_hand_points(self, cards: List[Card]):
        return len(cards)

if __name__ == "__main__":
    print(list(BridgeGame().deal_hand()))