
class PlayerStatsForFight():
    def __init__(self, itemObjectList, spellsObjectList):

        self.Equipment={
            "principal_hand":itemObjectList[1],
            "secondary_hand":itemObjectList[0]
            }
        self.Spells_for_fight={
            "first_spell":spellsObjectList[2],
            "second_spell":None,
            "third_spell":None,
            "fourth_spell":None
            }
        print(self.Equipment["principal_hand"].name)
        self.PV=100
        self.Speed=1
        self.Strength=10
        self.Magic_Affinity=10
        self.Mana=100
        self.PV_Max=100
        self.Mana_Max=100
        self.defense=1.0
        self.statut="RAS"
        self.armure=self.defense+self.Equipment["principal_hand"].prot+self.Equipment["secondary_hand"].prot
        self.protection_attaque_leger=1
        self.protection_attaque_lourde=1
        self.magic_def=self.Equipment["principal_hand"].magic_prot+self.Equipment["secondary_hand"].magic_prot
        self.dicoCreation()
        self.stats_player = self.stats
    def dicoCreation(self):
        self.stats = {"PV":self.PV, "speed":self.Speed, "Strength":self.Strength, "Maffinity":self.Magic_Affinity, "Mana":self.Mana, "PV_max":self.PV_Max, "Mana_max":self.Mana_Max, "defense":self.defense, "statut":self.statut, "armure":self.armure, "M_defense":self.magic_def}
        print(self.stats.get("PV"))
        return  self.stats
