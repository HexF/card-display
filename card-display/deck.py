
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

    def __str__(self) -> str:
        return f"{self.full_value} of {self.suit.name} ({self.compact_value}{self.suit.compact})"


class CardDeck:
    """
    Represents a collection of cards, loaded from a deck file
    """

    def __init__(self, suits: list[CardSuit], cards: list[Card]):
        self.suits = suits
        self.cards = cards

    @staticmethod
    def from_string(deck_file_content: str, cards_file_content: str):
        """
        Load the deck from the deck file and cards listing file
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

        return CardDeck(list(suits), cards)

    def __str__(self) -> str:
        return "\n".join([str(card) for card in self.cards])


if __name__ == "__main__":
    deck = """deck1.txt
52
A,Ace
K,King
Q,Queen
J,Jack
T,Ten
9,Nine
8,Eight
7,Seven
6,Six
5,Five
4,Four
3,Three
2,Two
S,Spades
H,Hearts
D,Diamonds
C,Clubs"""
    cards = "ASKSQSJSTS9S8S7S6S5S4S3S2SAHKHQHJHTH9H8H7H6H5H4H3H2HADKDQDJDTD9D8D7D6D5D4D3D2DACKCQCJCTC9C8C7C6C5C4C3C2C"

    d = CardDeck.from_string(deck, cards)
    print(d)