from pathlib import Path
from textwrap import dedent
import pytest
from card_display.deck import Card, CardDeck, CardSuit


def interleave(*lists):
    """
    Interleave all the lists, so lists like:
        ACEG
        BDFH
    becomes
        ABCDEFGH
    """
    return [val for tup in zip(*lists) for val in tup]


SUITS = [
    CardSuit("S", "Spades"),
    CardSuit("H", "Hearts"),
    CardSuit("D", "Diamonds"),
    CardSuit("C", "Clubs"),
]

CARD_NAMES = [
    ("A", "Ace"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
    ("6", "Six"),
    ("7", "Seven"),
    ("8", "Eight"),
    ("9", "Nine"),
    ("T", "Ten"),
    ("J", "Jack"),
    ("Q", "Queen"),
    ("K", "King"),
]

CARDS = [Card(suit, compact, full) for compact, full in CARD_NAMES for suit in SUITS]

LOAD_CASES = [
    (
        dedent(
            """\
            deck1.txt
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
            C,Clubs
            """
        ),
        "ASKSQSJSTS9S8S7S6S5S4S3S2SAHKHQHJHTH9H8H7H6H5H4H3H2HADKDQDJDTD9D8D7D6D5D4D3D2DACKCQCJCTC9C8C7C6C5C4C3C2C",
        {repr(card) for card in CARDS},
    ),
    (
        dedent(
            """\
            deck51.txt
            51
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
            C,Clubs
            """
        ),
        "ASKSQSJSTS9S8S7S6S5S4S3S2SAHKHQHJHTH9H8H7H6H5H4H3H2HADKDQDJDTD9D8D7D6D5D4D3D2DACKCQCJCTC9C8C7C6C5C4C3C",
        {
            repr(card) for card in CARDS
            if repr(card) != "Two of Clubs (2C)"
        },
    )
]

class TestCardSuit:
    suit_spades = CardSuit("S", "Spades")
    suit_hearts = CardSuit("H", "Hearts")

    suit_potato = CardSuit("P", "Potato")

    def test_suit_listing(self):
        assert self.suit_spades.deck_listing == "S"
        assert self.suit_hearts.deck_listing == "H"

    def test_suit_compact_repr(self):
        assert self.suit_spades.compact == "S"
        assert self.suit_hearts.compact == "H"

    def test_suit_name(self):
        assert self.suit_spades.name == "Spades"
        assert self.suit_hearts.name == "Hearts"

    def test_suit_card_unicode_codepoint_base(self):
        assert self.suit_spades.unicode_card_codepoint == 0x1F0A1
        assert self.suit_hearts.unicode_card_codepoint == 0x1F0B1

        with pytest.raises(TypeError):
            self.suit_potato.unicode_card_codepoint

    def test_suit_unicode_char(self):
        assert self.suit_spades.unicode_suit_char == "♠"
        assert self.suit_hearts.unicode_suit_char == "♥"

        with pytest.raises(TypeError):
            self.suit_potato.unicode_suit_char


class TestCard:
    card = CARDS[0]

    def test_repr(self):
        assert repr(self.card) == "Ace of Spades (AS)"

    @pytest.mark.parametrize(
        "card, expect_char",
        list(zip(CARDS, "🂡🂱🃁🃑🂢🂲🃂🃒🂣🂳🃃🃓🂤🂴🃄🃔🂥🂵🃅🃕🂦🂶🃆🃖🂧🂷🃇🃗🂨🂸🃈🃘🂩🂹🃉🃙🂪🂺🃊🃚🂫🂻🃋🃛🂬🂼🃌🃜🂭🂽🃍🃝🂮🂾🃎🃞")),
    )
    def test_unicode_card(self, card: Card, expect_char: str):
        assert card.unicode_card == expect_char

    @pytest.mark.parametrize(
        "card, compact",
        list(zip(CARDS, interleave(*[[a[0] for a in CARD_NAMES]] * len(SUITS)))),
    )
    def test_unicode_suit_card(self, card: Card, compact: str):
        assert card.unicode_suit_card == card.suit.unicode_suit_char + compact

    @pytest.mark.parametrize(
        "card, compact",
        list(zip(CARDS, interleave(*[[a[0] for a in CARD_NAMES]] * len(SUITS)))),
    )
    def test_suit_card(self, card: Card, compact: str):
        assert card.unicode_suit_card == card.suit.unicode_suit_char + compact


class TestClassDeck:
    deck = CardDeck(
        suits=SUITS,
        cards=[
            Card(suit, compact, full) for compact, full in CARD_NAMES for suit in SUITS
        ],
    )

    def test_shuffe_randomize(self):
        "Ensure the deck actually gets randomized"

        # Store the old order of cards as a copy
        old_order = self.deck.cards[::]

        # shuffle deck
        self.deck.shuffle()

        new_order = self.deck.cards[::]

        assert any(
            [repr(a) != repr(b) for a, b in zip(old_order, new_order)]
        ), "The deck did not get randomized"

    def test_deal_card(self):
        card_count = len(self.deck.cards)

        seen_cards = []

        for _ in range(card_count):
            # deal a card
            card = self.deck.deal_card()

            # ensure the card has not been seen before
            assert card not in seen_cards
            seen_cards.append(card)

    @pytest.mark.parametrize("deal_count", [n + 1 for n in range(52)])
    def test_deal_n_cards(self, deal_count: int):
        loop_times = len(self.deck.cards) // deal_count

        remaining_cards = len(self.deck.cards) - loop_times * deal_count

        seen_cards = set()

        for _ in range(loop_times):
            cards = set(self.deck.deal_cards(deal_count))

            # Ensure we haven't seen any of the cards previously
            assert len(seen_cards.intersection(cards)) == 0
            for card in cards:
                seen_cards.add(card)

        assert len(seen_cards) == deal_count * loop_times
        assert len(self.deck.cards) == remaining_cards

    @pytest.mark.parametrize(
        "deal_count, expect_error, expected_cards",
        [
            (-1, ValueError, 0),
            (0, ValueError, 0),
            (53, IndexError, 52),
        ],
    )
    def test_dealy_cards_bound(
        self, deal_count: int, expect_error: type[Exception], expected_cards: int
    ):
        with pytest.raises(expect_error):
            assert len(list(self.deck.deal_cards(deal_count))) == expected_cards

    @pytest.mark.parametrize("deck_file_content, cards_file_content, card_names", LOAD_CASES)
    def test_deck_loading_str(
        self, deck_file_content: str, cards_file_content: str, card_names: set[str]
    ):
        deck = CardDeck.from_string(deck_file_content, cards_file_content)

        actual_card_names = set(repr(card) for card in deck.cards)
        assert len(actual_card_names.intersection(card_names)) == len(card_names)

    @pytest.mark.parametrize("deck_file_content, cards_file_content, card_names", LOAD_CASES)
    def test_deck_loading_file(
        self, deck_file_content: str, cards_file_content: str, card_names: set[str], tmp_path: Path
    ):
        deck_file = tmp_path / "deck.txt"
        card_file = tmp_path / deck_file_content.splitlines()[0]

        deck_file.write_text(deck_file_content)
        card_file.write_text(cards_file_content)
        
        deck = CardDeck.from_file(deck_file)

        actual_card_names = set(repr(card) for card in deck.cards)
        print(LOAD_CASES)
        assert len(actual_card_names.intersection(card_names)) == len(card_names)
       
