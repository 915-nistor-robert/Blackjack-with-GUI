import traceback

from domain.game import Game
from domain.validators import Validator
from ui.console import Console
from ui.gui import Gui

validators = Validator()
blackjack = Game()

gui_option = input('1 - If you want a console based game, 2 - If you want a GUI based game\n')
if gui_option == '1':
    console = Console(blackjack, validators)
    console.start()
else:
    gui = Gui(blackjack, validators)
    gui.start()

