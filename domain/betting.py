class BetException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Bet:
    def __init__(self, initial_money):
        self.balance = initial_money
        self.pot = 0

    def get_balance(self):
        return self.balance

    def get_pot(self):
        return self.pot

    def betting(self, amount):
        if amount > self.balance:
            raise BetException("You don't have enough money to bet that amount")
        self.balance -= amount
        self.pot = self.pot + 2 * amount

    def winning(self):
        self.balance += self.pot

    def draw(self):
        self.balance += self.pot // 2

    def new_game(self):
        self.pot = 0




