from tkinter import *
from fight_engine.items_spells_deserialiseur import ItemsSpellsDeserialiseur

class FightEngine():
    def __init__(self, _window, _window_options,texture_fight ):
        self.fight_ui_texture_list = texture_fight
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
        self.fight_can = Canvas(_window, height=_window_options["y_window_size"], width=_window_options["x_window_size"], highlightthickness=0,bg="white")
        self.fight_can.place(x=0, y=0)
        self.fight_can.pack()
        self.MainCan()
    def MainCan(self):
        pass
    def Reset(self):
        self.fight_can.destroy()
        self.startFightEngine
    def createCustomCanvas(self, canwidth, canheight, x, y, image, arg, funct):
        self.CanList.append(Canvas(self.MainCan, width=canwidth, height=canheight, bg="#9a9a9a", highlightthickness=0))
        self.CanList[len(self.CanList)-1].place(x=x, y=y)
        self.CanList[len(self.CanList)-1].create_image(0,0, image=image, anchor=NW)
        self.CanList[len(self.CanList)-1].bind("<Button-1>", lambda arg1=None, arg2=arg:funct(arg1, arg2))
    def stopFightEngine(self, _window):
        self.fight_can.destroy()
