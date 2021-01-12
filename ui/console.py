import traceback

from domain.betting import Bet
from domain.deck import Deck
from domain.hand import Hand


class Console:
    def __init__(self, game, validators):
        self.game = game
        self.validators = validators

    def ui_initialise_balance(self):
        initial_money = input("How much money you want to play with?\n")
        self.validators.validate_money(initial_money)
        return Bet(int(initial_money))

    def ui_display_hand(self, hand):
        for card in hand.cards:
            print(card)
        print("Value: ", hand.get_value())


    def ui_display_initial_dealer_hand(self, dealer_hand):
        print("Hidden")
        print(dealer_hand.cards[1])


    def ui_play_dealer_turn(self):
        print("_________DEALER'S HAND__________")
        self.ui_display_hand(self.dealer_hand)
        while self.dealer_hand.get_value() < 16 or self.dealer_hand.get_value() < self.player_hand.get_value():
            self.dealer_hand.add_card(self.deck.deal_a_card())
            print("_________DEALER'S HAND__________")
            self.ui_display_hand(self.dealer_hand)

    def ui_place_bet(self):
        bet = input("How much do you want to bet?\n")
        self.validators.validate_bet(bet, self.bet.balance)
        self.bet.betting(int(bet))

    def deal_2_cards_to_both_players(self):
        for card_dealt in range(2):
            self.player_hand.add_card(self.deck.deal_a_card())
            self.dealer_hand.add_card(self.deck.deal_a_card())

    def ui_play_players_turn(self):
        if not self.game.check_for_blackjack(self.player_hand.get_value()):
            while True:
                try:
                    dealer_option = input("Do you want to hit or stall?\n")
                    self.validators.validate_deal_option(dealer_option)
                    break
                except Exception as error:
                    print(error)
            while dealer_option == 'hit' and self.player_hand.get_value() < 21:
                self.player_hand.add_card(self.deck.deal_a_card())
                print("________PLAYER'S HAND________")
                self.ui_display_hand(self.player_hand)

                if not self.game.check_if_is_over(
                        self.player_hand.get_value()) and not self.game.check_for_blackjack(
                    self.player_hand.get_value()):
                    while True:
                        try:
                            dealer_option = input("Do you want to hit or stall?\n")
                            self.validators.validate_deal_option(dealer_option)
                            break
                        except Exception as error:
                            print(error)

                if self.game.check_for_blackjack(self.player_hand.get_value()):
                    print('You have Blackjack')

    def ui_check_if_player_is_over(self):
        if self.game.check_if_is_over(self.player_hand.get_value()):
            print("You went over! You lost", self.bet.get_pot() / 2, "$", "! HAHAHAHA")
            print("Your current balance is:", self.bet.get_balance())
            while True:
                try:
                    decision = input("Play again? y/n\n")
                    playing = self.validators.validate_yes_or_no_decision(decision)
                    break
                except Exception as error:
                    print(error)
            self.bet.new_game()
            return playing

    def ui_game_result(self):
        if self.game.check_if_is_over(self.dealer_hand.get_value()):

            print("Dealer went over! You won", self.bet.get_pot(), "$", "!!! Here's a cake")
            self.bet.winning()
            print("Your current balance is:", self.bet.get_balance())
            while True:
                try:
                    decision = input("Play again? y/n\n")
                    playing = self.validators.validate_yes_or_no_decision(decision)
                    break
                except Exception as error:
                    print(error)
            self.bet.new_game()
        elif self.dealer_hand.get_value() == self.player_hand.get_value():
            print("It's a draw!")
            self.bet.draw()
            print("Your current balance is:", self.bet.get_balance())
            while True:
                try:
                    decision = input("Play again? y/n\n")
                    playing = self.validators.validate_yes_or_no_decision(decision)
                    break
                except Exception as error:
                    print(error)
            self.bet.new_game()
        else:

            print("You lost", self.bet.get_pot() / 2, "$!")
            print("Your current balance is:", self.bet.get_balance())
            while True:
                try:
                    decision = input("Play again? y/n\n")
                    playing = self.validators.validate_yes_or_no_decision(decision)
                    break
                except Exception as error:
                    print(error)
            self.bet.new_game()

        return playing

    def start(self):
        playing = True
        while True:
            try:
                self.bet = self.ui_initialise_balance()
                break
            except Exception as ex:
                print(ex)

        while playing:
            try:
                self.deck = Deck()
                self.deck.shuffle_deck()

                self.player_hand = Hand()
                self.dealer_hand = Hand(dealer=True)

                self.ui_place_bet()

                self.deal_2_cards_to_both_players()


                print("_________DEALER'S HAND__________")
                self.ui_display_initial_dealer_hand(self.dealer_hand)
                print("________PLAYER'S HAND________")
                self.ui_display_hand(self.player_hand)


                self.ui_play_players_turn()


                decision = self.ui_check_if_player_is_over()
                if decision is not None:
                    playing = decision
                else:
                    self.ui_play_dealer_turn()

                    playing = self.ui_game_result()
            except Exception as ex:
                print(ex)
                traceback.print_exc()

# TODO: notify when having blackjack!

# TODO: move display players hand and dealers hand in UI

