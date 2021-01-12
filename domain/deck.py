import random
from tkinter import *
from PIL import Image

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value


    def __repr__(self):
        return " of ".join((self.value, self.suit))

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value




class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in ["Spade", "Club", "Heart", "Diamond"] for value in
                      ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]]

    def shuffle_deck(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal_a_card(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)

    def __len__(self):
        return len(self.cards)


