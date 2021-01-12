class InputException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Validator:
    def validate_money(self, amount):
        if not amount.isdigit() or int(amount) < 0:
            raise InputException("The amount of money need to be a positive integer!")

    def validate_bet(self, amount, balance):
        if not amount.isdigit() or int(amount) < 0:
            raise InputException("The amount of money need to be a positive integer!")
        if int(amount) > balance:
            raise InputException("You don't have enough money to bet that amount!")

    def validate_yes_or_no_decision(self, decision):
        if decision == 'y':
            return True
        elif decision == 'n':
            return False
        else:
            raise InputException("The answear must be 'y' or 'n'!")

    def validate_deal_option(self, decision):
        if decision not in ['hit', 'stall']:
            raise InputException("You must choose hit or stall!")
