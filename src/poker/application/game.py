from ..domain.entities import Card, Deck, Suit, Rank


class DeckService:
    def __init__(self) -> None:
        self.deck = Deck(cards=[Card(rank=r, suit=s) for s in Suit for r in Rank])
        self.deck.shuffle()

    def deal(self) -> Card:
        return self.deck.deal()
