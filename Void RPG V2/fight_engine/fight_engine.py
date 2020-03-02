from tkinter import *
from fight_engine.items_spells_deserialiseur import ItemsSpellsDeserialiseur

class FightEngine():
    def __init__(self, _window, _window_options):
        self._window = _window
        self._window_options = _window_options
        self.fight = ItemsSpellsDeserialiseur()
        self.stats = self.fight.stats_for_player
        self.Equipment = self.fight.Equipment
        self.Spells_for_fight = self.fight.Spells_for_fight
        self.stats_enemie()
        print("eeeeeeeeeeeeeeeeee")
        self.startFightEngine(self._window, self._window_options)
    def stats_enemie(self):
        self.PVE=1500000
        self.PVE_max=1500000
        self.defenceE=50
        self.manaE=100
        self.manaE_max=100
        self.SpeedE=1
        self.StrengthE=3
        self.Magic_AffinityE=10
        self.esquiveE=5
        self.statutE="RAS"
    def startFightEngine(self, _window, _window_options):
        print("eeeeeeeeeeeeeeeeeeeeeeeee")
        self.fight_can = Canvas(_window, height=_window_options["y_window_size"], width=_window_options["x_window_size"], highlightthickness=0,bg="white")
        self.fight_can.place(x=0, y=0)
        self.fight_can.pack()
        print("e")
    def stopFightEngine(self, _window):
        self.fight_can.destroy()
