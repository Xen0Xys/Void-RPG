from tkinter import *
from random import randint
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
        self.startFightEngine(self._window, self._window_options, self.fight_ui_texture_list)
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
    def startFightEngine(self, _window, _window_options, fight_ui_texture_list):
        self.CanList=[]
        self.fight_ui_texture_list = fight_ui_texture_list
        self.fight_can = Canvas(_window, height=_window_options["y_window_size"], width=_window_options["x_window_size"], highlightthickness=0,bg="white")
        self.fight_can.place(x=0, y=0)
        self.fight_can.pack()
        self.MainCan()


    def onFightClick(self, evt, arg):
        if arg=="arme_principale":
            self.arme_principale()
        if arg=="arme_secondaire":
            self.arme_secondaire()
        if arg=="magie":
            self.Magie()
        if arg=="sac":
            self.sac()
        if arg=="fuite":
            self.Fuite()



    def arme_principale(self):
        self.hand="principal"
        if self.Equipment["principal_hand"].type_of_items=="batte":
            self.firstAttackInterface("batte")
        elif self.Equipment["principal_hand"].type_of_items=="sword":
            self.firstAttackInterface("sword")
        elif self.Equipment["principal_hand"].type_of_items=="axes":
            self.firstAttackInterface("axes")
        elif self.Equipment["principal_hand"].type_of_items=="dagger":
            self.firstAttackInterface("dagger")
        elif self.Equipment["principal_hand"].type_of_items=="hammer":
            self.firstAttackInterface("hammer")
        elif self.Equipment["principal_hand"].type_of_items=="whip":
            self.firstAttackInterface("whip")

    def arme_secondaire(self):
        self.hand="secondary"
        if self.Equipment["principal_hand"].type_of_items=="batte":
            self.second_attack_interface("batte")
        elif self.Equipment["principal_hand"].type_of_items=="sword":
            self.second_attack_interface("sword")
        elif self.Equipment["principal_hand"].type_of_items=="axes":
            self.second_attack_interface("axes")
        elif self.Equipment["principal_hand"].type_of_items=="dagger":
            self.second_attack_interface("dagger")
        elif self.Equipment["principal_hand"].type_of_items=="hammer":
            self.second_attack_interface("hammer")
        elif self.Equipment["principal_hand"].type_of_items=="whip":
            self.second_attack_interface("whip")

    def firstAttackInterface(self, type_of_items):
        if type_of_items == "batte":
            print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            self.createCustomCanvas(100, 40, 10, 515,self.fight_ui_texture_list["attaque_1"], "battingStrike", self.onAttackWhitBatClick)
            self.createCustomCanvas(100, 40, 10, 575,self.fight_ui_texture_list["attaque_2"], "homeRunStrike", self.onAttackWhitBatClick)
            self.createCustomCanvas(100,40,110,640,self.fight_ui_texture_list["attaque_3"], "skullBreach", self.onAttackWhitBatClick)
            self.createCustomCanvas(100,40,110,680,self.fight_ui_texture_list["attaque_4"], "legBreakage", self.onAttackWhitBatClick)
            print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        elif type_of_items == "sword":
            self.createCustomCanvas(100,40,10,640,self.fight_ui_texture_list["attaque_1"], "flankStroke", self.onAttackWhitSwordClick)
            self.createCustomCanvas(100,40,10,680,self.fight_ui_texture_list["attaque_2"], "riposte", self.onAttackWhitSwordClick)
            self.createCustomCanvas(100,40,110,640,self.fight_ui_texture_list["attaque_3"], "weakPointHit", self.onAttackWhitSwordClick)
            self.createCustomCanvas(100,40,110,680,self.fight_ui_texture_list["attaque_4"], "sequenceOfBlows", self.onAttackWhitSwordClick)
        elif type_of_items == "axes":
            self.createCustomCanvas(100,40,10,640,self.fight_ui_texture_list["attaque_1"], "basicAttack", self.onAttackWhitAxesClick)
            self.createCustomCanvas(100,40,10,680,self.fight_ui_texture_list["attaque_2"], "shieldBreaking", self.onAttackWhitAxesClick)
            self.createCustomCanvas(100,40,110,640,self.fight_ui_texture_list["attaque_3"], "decapitation", self.onAttackWhitAxesClick)
            self.createCustomCanvas(100,40,110,680,self.fight_ui_texture_list["attaque_4"], "berserkAttack", self.onAttackWhitAxesClick)
        elif type_of_items == "dagger":
            self.createCustomCanvas(100,40,10,640,self.fight_ui_texture_list["attaque_1"], "knifeStabbing", self.onAttackWhitDaggerClick)
            self.createCustomCanvas(100,40,10,680,self.fight_ui_texture_list["attaque_2"], "sneakAttack", self.onAttackWhitDaggerClick)
            self.createCustomCanvas(100,40,110,640,self.fight_ui_texture_list["attaque_3"], "bloodyAttack", self.onAttackWhitDaggerClick)
            self.createCustomCanvas(100,40,110,680,self.fight_ui_texture_list["attaque_4"], "deadlyBlow", self.onAttackWhitDaggerClick)
        elif type_of_items == "hammer":
            self.createCustomCanvas(100,40,10,640,self.fight_ui_texture_list["attaque_1"], "simpleHit", self.onAttackWhitHammerClick)
            self.createCustomCanvas(100,40,10,680,self.fight_ui_texture_list["attaque_2"], "stun", self.onAttackWhitHammerClick)
            self.createCustomCanvas(100,40,110,640,self.fight_ui_texture_list["attaque_3"], "boneBreaker", self.onAttackWhitHammerClick)
            self.createCustomCanvas(100,40,110,680,self.fight_ui_texture_list["attaque_4"], "rotatingAttack", self.onAttackWhitHammerClick)
        elif type_of_items == "whip":
            self.createCustomCanvas(100,40,10,640,self.fight_ui_texture_list["attaque_1"], "whiplash", self.onAttackWhitWhipClick)
            self.createCustomCanvas(100,40,10,680,self.fight_ui_texture_list["attaque_2"], "laceration", self.onAttackWhitWhipClick)
            self.createCustomCanvas(100,40,110,640,self.fight_ui_texture_list["attaque_3"], "disarmament", self.onAttackWhitWhipClick)
            self.createCustomCanvas(100,40,110,680,self.fight_ui_texture_list["attaque_4"], "multipleStrikes", self.onAttackWhitWhipClick)

    def onAttackWhitBatClick(self, evt, arg):
        if arg == "battingStrike":
            self.battingStrike()
        elif arg == "homeRunStrike":
            self.homeRunStrike()
        elif arg == "skullBreach":
            self.skullBreach()
        elif arg == "legBreakage":
            self.legBreakage()
    def battingStrike(self):
        a = randint(1,100)
        if a < 90:
            if self.defenceE > 0:
                self.defenceE = self.defenceE-self.stats.get("Strength")*self.Equipment["principal_hand"].damage
                if self.defenceE < 0:
                    self.defenceE = 0
            else:
                self.PVE = self.PVE-self.stats.get("Strength")*self.Equipment["principal_hand"].damage
    def homeRunStrike(self): 
        a = randint(1,100)
        if a < 50:
            if self.defenceE > 0:
                self.defenceE = self.defenceE-(self.stats.get("Strength")*self.Equipment["principal_hand"].damage)*2*self.stats.get("Strength")
                if self.defenceE < 0:
                    self.defenceE = 0
            else:
                self.PVE = self.PVE-self.stats.get("Strength")*self.Equipment["principal_hand"].damage
    def skullBreach(self):
        a = randint(1,100)
        if a < 90:
            if self.defenceE > 0:
                self.defenceE = self.defenceE-(self.stats.get("Strength")*self.Equipment["principal_hand"].damage)
                if self.defenceE < 0:
                    self.defenceE = 0
            else:
                self.PVE = self.PVE-(self.stats.get("Strength")*self.Equipment["principal_hand"].damage)
                if 25<a<35:
                    self.statutE = "skullBreach"
    def legBreakage(self):
        a = randint(1,100)
        if a < 90:
            if self.defenceE > 0:
                self.defenceE = self.defenceE-(self.stats.get("Strength")*self.Equipment["principal_hand"].damage)
                if self.defenceE < 0:
                    self.defenceE = 0
            else:
                self.PVE = self.PVE-(self.stats.get("Strength")*self.Equipment["principal_hand"].damage)
                if 25<a<35:
                    self.statutE = "leg_Break"

    def onAttackWhitSwordClick(self, evt, arg):
        if arg == "flankStroke":
            self.flankStroke()
        elif arg == "riposte":
            self.riposte()
        elif arg == "weakPointHit":
            self.weakPointHit()
        elif arg == "sequenceOfBlows":
            self.b = 0
            self.nombre_de_fois_attack=0
            self.sequenceOfBlows()
    def flankStroke(self):
        a = randint(1,100)
        if a < 90:
            if self.defenceE > 0:
                self.defenceE = self.defenceE-self.stats.get("Strength")*self.Equipment["principal_hand"].damage
                if self.defenceE < 0:
                    self.defenceE = 0
            else:
                self.PVE = self.PVE-self.stats.get("Strength")*self.Equipment["principal_hand"].damage
    def riposte(self):
        self.statut = "riposte"
    def weakPointHit(self):
        pass
    def sequenceOfBlows(self):
        a = randint(1,100)
        self.nombre_de_fois_attack +=1
        if a < 90-self.b:
            self.b -= 20
            if self.defenceE > 0:
                self.defenceE = self.defenceE-((self.stats.get("Strength")*self.Equipment["principal_hand"].damage)+self.b*2)
                if self.defenceE < 0:
                    self.defenceE = 0
            else:
                self.PVE = self.PVE-self.stats.get("Strength")*self.Equipment["principal_hand"].damage
            if self.nombre_de_fois_attack < 3:
                self.sequenceOfBlows()
    def onAttackWhitAxesClick(self, evt, arg):
        if arg == "basicAttack":
            self.basicAttack()
        elif arg == "shieldBreaking":
            self.shieldBreaking()
        elif arg == "decapitation":
            self.decapitation()
        elif arg == "berserkAttack":
            self.berserkAttack()
    def basicAttack(self):
        a = randint(1,100)
        if a < 90:
            if self.defenceE > 0:
                self.defenceE = self.defenceE-self.stats.get("Strength")*self.Equipment["principal_hand"].damage
                if self.defenceE < 0:
                    self.defenceE = 0
            else:
                self.PVE = self.PVE-self.stats.get("Strength")*self.Equipment["principal_hand"].damage
    def shieldBreaking(self):
        pass
    def decapitation(self):
        pass
    def berserkAttack(self):
        pass

    def onAttackWhitDaggerClick(self, evt, arg):
        if arg == "knifeStabbing":
            self.knifeStabbing()
        elif arg == "sneakAttack":
            self.sneakAttack()
        elif arg == "bloodyAttack":
            self.bloodyAttack()
        elif arg == "deadlyBlow":
            self.deadlyBlow()
    def knifeStabbing(self):
        pass
    def sneakAttack(self):
        pass
    def bloodyAttack(self):
        pass
    def deadlyBlow(self):
        pass

    def onAttackWhitHammerClick(self, evt, arg):
        if arg == "simpleHit":
            self.simpleHit()
        elif arg == "stun":
            self.stun()
        elif arg == "boneBreaker":
            self.boneBreaker
        elif arg == "rotatingAttack":
            self.rotatingAttack()
    def simpleHit(self):
        a = randint(1,100)
        if a < 90:
            if self.defenceE > 0:
                self.defenceE = self.defenceE-self.stats.get("Strength")*self.Equipment["principal_hand"].damage
                if self.defenceE < 0:
                    self.defenceE = 0
            else:
                self.PVE = self.PVE-self.stats.get("Strength")*self.Equipment["principal_hand"].damage
    def stun(self):
        pass
    def boneBreaker(self):
        pass
    def rotatingAttack(self):
        pass

    def onAttackWhitWhipClick(self, evt, arg):
        if arg == "whiplash":
            self.whiplash()
        elif arg == "laceration":
            self.laceration()
        elif arg == "disarmament":
            self.disarmament()
        elif arg == "multipleStrikes":
            self.multipleStrikes()
    def whiplash(self):
        pass
    def laceration(self):
        pass
    def disarmament(self):
        pass
    def multipleStrikes(self):
        pass


    def MainCan(self):
        print(self._window_options)
        self.createCustomCanvas(100, 40, 10, 515, self.fight_ui_texture_list["arme_principale"], "arme_principale", self.onFightClick)
        self.createCustomCanvas(100, 40, 10, 575, self.fight_ui_texture_list["arme_secondaire"], "", self.onFightClick)
    def Reset(self):
        self.fight_can.destroy()
        self.startFightEngine()
    def createCustomCanvas(self, canwidth, canheight, x, y, image, arg, funct):
        self.CanList.append(Canvas(self.fight_can, width=canwidth, height=canheight, bg="#9a9a9a", highlightthickness=0))
        self.CanList[len(self.CanList)-1].place(x=x, y=y)
        self.CanList[len(self.CanList)-1].create_image(0,0, image=image, anchor=NW)
        self.CanList[len(self.CanList)-1].bind("<Button-1>", lambda arg1=None, arg2=arg:funct(arg1, arg2))
    def stopFightEngine(self, _window):
        self.fight_can.destroy()
