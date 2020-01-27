import os
import json

class Spells():
    def __init__(self):
        self.name=""
        self.damage=0
        self.magic_damages=0
        self.durability=0
        self.mana_consumation=0
        self.prot=0
        self.magic_prot=0
        self.drop_proba=0
        self.type=""
        self.effet=""
        self.texture_acces=""
        self.texture=None

class Item():
    def __init__(self):
        self.name=""
        self.damage=0
        self.magic_damages=0
        self.durability=0
        self.mana_consumation=0
        self.prot=0
        self.magic_prot=0
        self.drop_proba=0
        self.type=""
        self.texture_acces=""
        self.texture=None



class ItemsSpellsDeserialiseur():
    def __init__(self):
        self.LoadItems()
        self.LoadSpells()
        print(self.spellsObjectList[0].name)
    def AddToConfigList(self, arg):
        try:
            self.ConfigList.append(arg)
        except AttributeError:
            self.ConfigList=[]
            self.ConfigList.append(arg)
    def LoadItems(self):
        self.itemObjectList=[]
        folderList = os.listdir("ressources/items")
        for folder_name in folderList:
            with open("ressources/items/{}/root.json".format(folder_name), "r") as file:
                self.itemObjectList.append(json.load(file, object_hook=self.Deserialiseur))
    def Deserialiseur(self, obj_dict):
        if "__class__" in obj_dict:
            if obj_dict["__class__"] == "Item":
                obj = Item()
                obj.name=obj_dict["name"]
                obj.damage=obj_dict["damage"]
                obj.magic_damages=obj_dict["magic_damages"]
                obj.durability=obj_dict["durability"]
                obj.mana_consumation=obj_dict["mana_consumation"]
                obj.prot=obj_dict["prot"]
                obj.magic_prot=obj_dict["magic_prot"]
                obj.drop_proba=obj_dict["drop_proba"]
                obj.type=obj_dict["type"]
                obj.type_of_items=obj_dict ["type_of_items"]
                obj.texture_acces=obj_dict["texture_acces"]
                return obj
        return obj_dict
    def LoadSpells(self):
        self.spellsObjectList=[]
        folderList = os.listdir("ressources/spells")
        for folder_name in folderList:
            with open("ressources/spells/{}/root.json".format(folder_name), "r") as file:
                self.spellsObjectList.append(json.load(file, object_hook=self.Deserialiseur_Spells))
    def Deserialiseur_Spells(self, obj_dict):
        if "__class__" in obj_dict:
            if obj_dict["__class__"] == "Spells":
                obj = Spells()
                obj.name=obj_dict["name"]
                obj.damage=obj_dict["damage"]
                obj.magic_damages=obj_dict["magic_damages"]
                obj.durability=obj_dict["durability"]
                obj.mana_consumation=obj_dict["mana_consumation"]
                obj.prot=obj_dict["prot"]
                obj.magic_prot=obj_dict["magic_prot"]
                obj.drop_proba=obj_dict["drop_proba"]
                obj.type=obj_dict["type"]
                obj.effet=obj_dict["effet"]
                obj.texture_acces=obj_dict["texture_acces"]
                return obj
        return obj_dict

main = ItemsSpellsDeserialiseur()

