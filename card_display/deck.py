
from pathlib import Path
import random
from typing import Generator

class CardSuit:
    """
    Represents a card suit
    """


    def __init__(self, compact_repr: str, full_repr: str):
        """
        Initializes a card suit
        """

        self.compact_repr = compact_repr
        self.full_repr = full_repr

    @property
    def deck_listing(self):
        """
        The value used in the deck listing
        """
        return self.compact_repr

    @property
    def compact(self):
        """
        The compact version of the card suit
        """
        return self.compact_repr

    @property
    def name(self):
        """
        The name of the suit
        """
        return self.full_repr
        

class Card:
    """
    Represents a single card, with a suit and value
    """


    def __init__(self, suit: CardSuit, compact_value: str, full_value: str):
        self.suit = suit
        self.compact_value = compact_value
        self.full_value = full_value       

    def __repr__(self) -> str:
        return f"{self.full_value} of {self.suit.name} ({self.compact_value}{self.suit.compact})"


class CardDeck:
    """
    Represents a collection of cards, loaded from a deck file
    """

    def __init__(self, suits: list[CardSuit], cards: list[Card]):
        self.suits = suits
        self._cards = cards

        self.shuffle()


    def shuffle(self):
        """
        Collect back all the delt cards back into the deck, then shuffle the deck
        """

        self.cards = self._cards[::] # copy the list of cards
        random.shuffle(self.cards)  # shuffle all the cards

    def deal_card(self) -> Card:
        """
        Return a singular card from the deck
        """
        return self.cards.pop()

    def deal_cards(self, n) -> Generator[None, Card, None]:
        """
        Return n cards from the deck
        """
        for _ in range(n):
            yield self.deal_card()


    @classmethod
    def from_string(cls, deck_file_content: str, cards_file_content: str):
        """
        Load the deck from the deck file content and cards listing file content
        """

        # Get the individual lines from the deck file


        cards_file_name, card_count, *suit_values = deck_file_content.splitlines()

        # Get the number of cards required
        card_count = int(card_count)

        # Store a list of all possible suits
        possible_suits = [
            CardSuit(compact_repr, full_repr)
            for compact_repr, full_repr in [line.split(",") for line in suit_values]
        ]

        possible_suits_dict = {
            suit.deck_listing: suit
            for suit in possible_suits
        }

        # Create each card
        cards = [
            Card(possible_suits_dict[suit], possible_suits_dict[value].compact, possible_suits_dict[value].name)
            for value, suit in [
                (cards_file_content[2*i:2*i+1], cards_file_content[2*i+1:2*i+2])
                for i in range(card_count)
            ]
        ]

        # Get all used suits
        suits = {
            card.suit
            for card in cards
        }

        return cls(list(suits), cards)

    @classmethod
    def from_file(cls, file_path: Path):
        """
        Load the deck from the file at the given path
        """

        deck_file_contents = file_path.read_text()
        cards_file_name = deck_file_contents.splitlines()[0]

        card_file = file_path.parent / cards_file_name
        cards_file_contents = card_file.read_text()

        return cls.from_string(deck_file_contents, cards_file_contents)




        

    def __str__(self) -> str:
        return "\n".join([str(card) for card in self.cards])


if __name__ == "__main__":
    d = CardDeck.from_file(Path(__file__).parent / "games" / "bridge1.txt")
    

    for card in d.deal_cards(5):
        print(card)