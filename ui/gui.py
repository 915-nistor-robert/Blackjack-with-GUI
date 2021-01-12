from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial

from domain.betting import Bet
from domain.deck import Deck
from domain.hand import Hand


class Gui:
    def __init__(self, game, validators):
        self.bet = Bet(1000)
        self.game = game
        self.validators = validators
        self.bet_window = Tk()
        self.bet_window.geometry('500x500')

    def hit_button_pressed(self):
        """
        This function:
            - deals a card to the player
            - displays it
            - checks if the player went over
                - in this case a message is shown and the turn is over
            - checks if the player has a blackjack
                - in this case a message is shown to tell the player to hit stand for the dealer to play his hand
        :return:
        """
        card = self.deck.deal_a_card()
        self.player_hand.add_card(card)
        self.ui_deal_card(card, self.player_card_frame)
        self.player_hand_value.set(self.player_hand.get_value())
        if self.game.check_if_is_over(self.player_hand.get_value()):
            self.ui_dealer_wins('You went over!')
        if self.game.check_for_blackjack(self.player_hand.get_value()):
            Message(self.game_window, bg='green', fg='white',
                    text='You have blackjack, press STAND to let dealer play!', relief=RAISED).place(x=20, y=400)

    def ui_dealer_wins(self, reason):
        """
        This function:
            - shows a messagebox that tells the player why he lost
            - asks him to play again
        :param reason: the reason why he lost ex: went over, dealer hand is better
        :return:
        """
        reason = (reason + '\nDo you want to play again?')
        if messagebox.askokcancel(title='You lost!', message=reason):
            self.bet.new_game()
            self.game_window.destroy()
        else:
            quit()

    def ui_player_wins(self, reason):
        """
        This function:
            - shows a messagebox that tells the player why he won
            - asks him to play again
        :param reason: the reason why he won ex: dealer went over
        :return:
        """
        reason = (reason + '\nDo you want to play again?')
        if messagebox.askokcancel(title='You won!', message=reason):
            self.bet.new_game()
            self.game_window.destroy()
        else:
            quit()

    def quick_bet(self, amount):
        """
        This functions is called when the button quick bet is pressed
        :param amount:
        :return:
        """
        self.bet.betting(amount)
        self.create_game()

    def ui_draw(self):
        """
        This functions:
            - shows a messagebox that tells the player that the game its a draw
            - asks the player to play again
        :return:
        """
        if messagebox.askokcancel(title="It's a draw", message='Draw!\nDo you want to play again?'):
            self.bet.new_game()
            self.game_window.destroy()
        else:
            quit()

    def ui_deal_card(self, card, frame):
        """
        This function:
            - displays a given card to a given frame
        :param card: the card given
        :param frame: the frame the card will be displayed
        :return:
        """
        card = Image.open(
            r'D:\Python Problems\Blackjackk\cards\{}_{}.png'.format(card.get_value(), card.get_suit().lower()))
        self.cards_images.append(ImageTk.PhotoImage(card))

        Label(frame, image=self.cards_images[-1], relief=RAISED).pack(side=LEFT)

    def stand_button_pressed(self):
        """
        This function basically lets the dealer play
        While the dealer hand is worse than the player's hand
        the dealer will draw cards and checks if in the process
        the dealer went over or has a better or equal hand than the player then print the game result
         :return:
        """
        self.dealer_hand_value.set(self.dealer_hand.get_value())
        while self.dealer_hand.get_value() < 16 or self.dealer_hand.get_value() < self.player_hand.get_value():
            card = self.deck.deal_a_card()
            self.dealer_hand.add_card(card)
            self.ui_deal_card(card, self.dealer_card_frame)
            self.dealer_hand_value.set(self.dealer_hand.get_value())
        if self.game.check_if_is_over(self.dealer_hand.get_value()):
            self.bet.winning()
            self.ui_player_wins('Dealer went over!')
        elif self.player_hand.get_value() == self.dealer_hand.get_value():
            self.bet.draw()
            self.ui_draw()
        else:
            self.ui_dealer_wins('You lost!')

    def place_bet_pressed(self):
        """
        This function:
            - is called when the press bet button is pressed
            - places a bet equal to the amount the player wrote in the bet entry
        :return:
        """
        try:
            self.validators.validate_bet(self.bet_amount_entry.get(), self.bet.get_balance())
            self.bet.betting(int(self.bet_amount_entry.get()))
            self.create_game()
        except Exception as error:
            messagebox.showinfo('Error', str(error))

    def create_game(self):
        """
        This functions:
            - creates the actual game GUI
        :return:
        """
        self.game_window = Toplevel(self.bet_window, bg="green")
        self.game_window.geometry('500x500')
        self.game_window.title('Blackjack')

        self.cards_images = []

        self.deck = Deck()
        self.deck.shuffle_deck()

        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.dealer_hand_value = IntVar()
        self.player_hand_value = IntVar()

        card_frame = Frame(self.game_window, relief="sunken", borderwidth=30, background="green")
        card_frame.grid(row=5, column=0, sticky="ew", columnspan=5, rowspan=2)

        self.dealer_card_frame = Frame(card_frame, background="green", height=100, width=100)
        self.dealer_card_frame.grid(row=5, column=1, sticky="ew", rowspan=2)

        self.player_card_frame = Frame(card_frame, background="green")
        self.player_card_frame.grid(row=7, column=1, sticky="ew", rowspan=2)

        self.dealer_hand_value.set('x')
        self.player_hand_value.set(0)
        card_dealt = self.deck.deal_a_card()
        self.player_hand.add_card(card_dealt)
        self.ui_deal_card(card_dealt, self.player_card_frame)
        card_dealt = self.deck.deal_a_card()
        self.player_hand.add_card(card_dealt)
        self.ui_deal_card(card_dealt, self.player_card_frame)
        card_dealt = self.deck.deal_a_card()
        self.dealer_hand.add_card(card_dealt)
        self.ui_deal_card(card_dealt, self.dealer_card_frame)

        if self.game.check_for_blackjack(self.player_hand.get_value()):
            Message(self.game_window, bg='green', fg='white',
                    text='You have blackjack, press STAND to let dealer play!', relief=RAISED).place(x=20, y=400)

        Button(self.game_window, text='HIT', bg='black', fg='white', relief='raised',
               command=self.hit_button_pressed).place(x=0, y=285)
        Button(self.game_window, text='STAND', bg='red', fg='white', relief='raised',
               command=self.stand_button_pressed).place(x=35, y=285)

        self.player_hand_value = IntVar()
        self.player_hand_value.set(self.player_hand.get_value())
        Label(self.game_window, bg='green', fg='white', font='Oswald 12', text='Hand value:').place(x=0, y=315)
        Label(self.game_window, bg='green', fg='white', font='Oswald 12', textvariable=self.player_hand_value).place(
            x=100, y=315)
        Label(self.game_window, bg='green', fg='white', font='Oswald 12', text='Dealer value:').place(x=0, y=345)
        Label(self.game_window, bg='green', fg='white', font='Oswald 12', textvariable=self.dealer_hand_value).place(
            x=105, y=345)

        balance_string = ('BALANCE: ' + str(self.bet.get_balance()))
        Label(self.game_window, bg='green', fg='white', font='Oswald 12', text=str(balance_string)).place(x=150, y=285)
        pot_string = ("POT: " + str(self.bet.get_pot()))
        Label(self.game_window, bg='green', fg='white', font='Oswald 12', text=pot_string).place(x=150, y=310)

    def start(self):
        """
        This function makes the GUI for the betting system and
        starts the game by asking the player how much he want to bet on the hand
        :return:
        """
        self.bet_window.title('Bet')
        self.bet_window.geometry('500x200')

        background_image = PhotoImage(file=r'D:\Python Problems\Blackjackk\blackjack_wp.png')
        background_label = Label(self.bet_window, image=background_image, bd=0)
        background_label.pack(fill=BOTH, expand=YES)

        Label(self.bet_window, bg='black', fg='white', text="Enter the amount of the bet!", font='none 12 bold').place(
            x=20, y=0)
        self.bet_amount_entry = Entry(self.bet_window, width=30, bg="white")
        self.bet_amount_entry.place(x=300, y=5)

        Button(self.bet_window, bg='black', fg='white', text="PLACE BET", font='none 12',
               command=(self.place_bet_pressed)).place(x=20, y=30)

        Button(self.bet_window, bg='red', fg='white', text='QUICK BET 50', font='none 10',
               command=partial(self.quick_bet, 50)).place(x=20, y=70)
        Button(self.bet_window, bg='red', fg='white', text='QUICK BET 100', font='none 10',
               command=partial(self.quick_bet, 100)).place(x=150, y=70)
        Button(self.bet_window, bg='red', fg='white', text='QUICK BET 200', font='none 10',
               command=partial(self.quick_bet, 200)).place(x=280, y=70)

        self.bet_window.mainloop()
