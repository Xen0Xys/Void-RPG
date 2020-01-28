from tkinter import *
from fight_engine.items_spells_deserialiseur import ItemsSpellsDeserialiseur

class FightEngine():
    def __init__(self, _window, _window_options):
        self.fight = ItemsSpellsDeserialiseur()
    def startFightEngine(self, _window, _window_options):
        self.fight_can = Canvas(_window, height=_window_options["y_window_size"], width=_window_options["x_window_size"], highlightthickness=0,bg="purple")
        self.fight_can.place(x=0, y=0)
        print("e")
    def stopFightEngine(self, _window):
        self.fight_can.destroy()
