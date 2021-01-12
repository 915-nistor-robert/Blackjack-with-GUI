from domain.betting import Bet
from domain.deck import Deck
from domain.hand import Hand


class Game:
    def check_for_blackjack(self, hand_value):
        if hand_value == 21:
            return True
        return False

    def check_if_is_over(self, hand_value):
        if hand_value > 21:
            return True
        return False

