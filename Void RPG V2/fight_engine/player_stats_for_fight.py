
class PlayerStatsForFight():
    def __init__(self, itemObjectList, spellsObjectList):
        self.Equipment={
            "principal_hand":self.itemObjectList[1],
            "secondary_hand":self.itemObjectList[0]
            }
        self.Spells_for_fight={
            "first_spell":self.spellsObjectList[2],
            "second_spell":None,
            "third_spell":None,
            "fourth_spell":None
            }
        print(Equipment["principal_hand"].name)
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        self.PV=100
        self.Speed=1
        self.Strength=10
        self.Magic_Affinity=10
        self.Mana=100
        self.PV_Max=100
        self.Mana_Max=100
        self.defense=1.0
        self.statut="RAS"

