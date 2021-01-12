import unittest
from unittest.mock import patch

from domain.betting import Bet, BetException
from domain.deck import Card, Deck
from domain.game import Game
from domain.hand import Hand
from domain.validators import Validator, InputException


class TestDeck(unittest.TestCase):
    def test_card(self):
        suit = "Spades"
        value = "A"
        card = Card(suit, value)
        self.assertEqual(card.get_suit(), suit)
        self.assertEqual(card.get_value(), value)

        expected_string = 'A of Spades'
        self.assertEqual(expected_string, str(card))


    def test_deck(self):
        deck = Deck()

        shuffled_deck = deck.shuffle_deck()
        self.assertNotEqual(deck, shuffled_deck)

        card_dealt = deck.deal_a_card()

        suit = card_dealt.get_suit()
        value = card_dealt.get_value()
        card = Card(suit, value)

        self.assertEqual(str(card_dealt), str(card))

class TestHand(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.deck.shuffle_deck()
        blackjack_hand = Hand()
        blackjack_hand.add_card(self.deck.deal_a_card())
        card = blackjack_hand.get_card(0)

    def test_calculate_value(self):
        card_1 = Card('Spades', 'A')
        card_2 = Card('Hearts', 'J')
        card_3 = Card('Diamonds', '5')
        card_4 = Card('Clubs', '10')

        blackjack_hand = Hand()
        blackjack_hand.add_card(card_1)

        self.assertEqual(blackjack_hand.get_value(), 11)

        blackjack_hand.add_card(card_2)
        self.assertEqual(blackjack_hand.get_value(), 21)

        blackjack_hand.add_card(card_3)
        self.assertEqual(blackjack_hand.get_value(), 16)

        blackjack_hand.add_card(card_4)
        self.assertEqual(blackjack_hand.get_value(), 26)


    def test_display(self):
        card_1 = Card('Spades', 'A')
        card_2 = Card('Hearts', 'J')
        card_3 = Card('Diamonds', '5')

        blackjack_hand = Hand()
        blackjack_hand.add_card(card_1)
        blackjack_hand.add_card(card_2)
        blackjack_hand.add_card(card_3)



# @patch('builtins.print')
# def test_greet(mock_print):
#     # The actual test
#     greet('John')
#     mock_print.assert_called_with('Hello ', 'John')
#     greet('Eric')
#     mock_print.assert_called_with('Hello ', 'Eric')

class TestBet(unittest.TestCase):
    def setUp(self):
        self.bet = Bet(1000)

    # def test_getters(self):
    #     pot = self.bet.get_pot()
    #     balance = self.bet.get_balance()

    def test_betting(self):
        self.bet.betting(10)
        pot = self.bet.get_pot()
        balance = self.bet.get_balance()

        self.assertEqual(pot, 20)
        self.assertEqual(balance, 990)

        self.assertRaises(BetException, self.bet.betting, 1000)

    def test_winning(self):
        self.bet.betting(10)

        self.bet.winning()
        self.assertEqual(self.bet.get_balance(), 1010)

    def test_draw(self):
        self.bet.betting(10)

        self.bet.draw()
        self.assertEqual(self.bet.get_balance(), 1000)

    def test_new_game(self):
        self.bet.betting(100)

        self.bet.new_game()

        self.assertEqual(self.bet.get_pot(), 0)

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_check_for_blackjack(self):
        self.assertTrue(self.game.check_for_blackjack(21))
        self.assertFalse(self.game.check_for_blackjack(20))

    def test_check_if_is_over(self):
        self.assertTrue(self.game.check_if_is_over(25))
        self.assertFalse(self.game.check_if_is_over(20))



class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validators = Validator()

    def test_validate_money(self):
        self.validators.validate_money('10')
        self.assertRaises(InputException, self.validators.validate_money,'a')
        self.assertRaises(InputException, self.validators.validate_money, '-10')

    def test_validate_bet(self):
        self.validators.validate_bet('10', 100)
        self.assertRaises(InputException, self.validators.validate_bet, 'a',100)
        self.assertRaises(InputException, self.validators.validate_bet, '-10', 100)
        self.assertRaises(InputException, self.validators.validate_bet, '100', 10)

    def test_validate_yes_or_no_decision(self):
        self.validators.validate_yes_or_no_decision('y')
        self.validators.validate_yes_or_no_decision('n')

        self.assertRaises(InputException, self.validators.validate_yes_or_no_decision, 'yes')

    def test_validate_deal_option(self):
        self.validators.validate_deal_option('hit')
        self.assertRaises(InputException, self.validators.validate_deal_option, 'h')

