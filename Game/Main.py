"""
MIT License

Copyright (c) [2019] [CZEKAJ Tom, DUCHENE Guillaume]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from tkinter import *
from tkinter.font import Font
from time import sleep
import threading
from PIL import Image, ImageTk
import pygame.mixer
from random import randint
import shutil
import os
import json
import time

class LiveInfos(Tk):
    def __init__(self, parent):
        #self.Launch(parent)
        pass
    def Launch(self, parent):
        Tk.__init__(self)
        threading.Thread(target=self.StartConsole, args=(parent,)).start()
        self.launched=True
        self.mainloop()
        self.launched=False
    def StartConsole(self, parent):
        self.LoadStringsVars()
        self.LoadLabels()
        while parent.main_loop_on==True and self.launched==True:
            try:
                sleep(0.01)
                self.smapX.set(parent.mapX)
                self.smapy.set(parent.mapY)
            except AttributeError as e:
                print(e)
        try:
            self.destroy()
        except RuntimeError:
            pass
    def LoadStringsVars(self):
        self.smapX=StringVar()
        self.smapX.set("")
        self.smapy=StringVar()
        self.smapy.set("")
    def LoadLabels(self):
        Label(self, text="mapx :").place(x=10, y=10)
        Label(self, textvariable=self.smapX).place(x=70, y=10)

class IntegratedConsole():
    def __init__(self):
        self.args={}
        self.LinesList=[]
        with open("ressources/save/config/IntegratedConsole.cfg", "r") as file:
            content=file.read()
            temp=content.split("\n")
            for line in temp:
                temp2=line.split("=")
                self.args[temp2[0]]=temp2[1]
        if self.args["do_start"]=="True":
            threading.Thread(target=self.__RunConsole).start()
            sleep(.01)
    def __RunConsole(self):
        self.window=Tk()
        self.window.title("Console")
        self.window.geometry("750x400")
        self.linesCan = Canvas(self.window, width=750, height=400, bg="light grey")
        self.linesCan.pack()
        self.linesCan.bind("<Configure>", self.__onResize)
        self.window.mainloop()
    def __onResize(self, evt):
        #print(evt.x, evt.y)
        self.linesCan["width"]=self.window.winfo_width()
        self.linesCan["height"]=self.window.winfo_height()
        try:
            toAdd = (self.LinesList[len(self.LinesList)-1]["y_coord"]) - self.window.winfo_height()
        except IndexError:
            pass
        for text in self.LinesList:
            text["y_coord"]-= 20 + toAdd
            self.linesCan.coords(text["text_on_screen"], text["x_coord"], text["y_coord"])
    def ClosingConsole(self):
        if self.args["do_closing_on_window_closing"]=="True":
            with open("ressources/log/log.txt", "w") as file:
                content=""
                for line in self.LinesList:
                    content+=line["text"]+"\n"
                file.write(content)
            try:
                self.window.destroy()
            except RuntimeError:
                pass
            except AttributeError:
                pass
    def Console(self, arg, warn_type="CONSOLE"):
        line = "[{}] : {}".format(warn_type, arg)
        try:
            self.__AddLine(line)
        except AttributeError:
            pass
    def __AddLine(self, line):
        dico={"text":line, "x_coord":10, "y_coord":375}
        dico["text_on_screen"] = self.linesCan.create_text(dico["x_coord"], dico["y_coord"], text=dico["text"], anchor=W)
        for text in self.LinesList:
            text["y_coord"]-=20
            self.linesCan.coords(text["text_on_screen"], text["x_coord"], text["y_coord"])
        self.LinesList.append(dico)

class PreInit(Tk, IntegratedConsole):
    #Recuperation des donnees et creation de la fenetre
    def __init__(self):
        self.InitWindow()
        self.UnzipRessourcesFolder()
        self.CreateConsole()
        self.GetMenuTextureList()
        self.GetFightTextureList()
        self.GetMenuConfig()
        self.GetHousesConfig()
    def CreateConsole(self):
        self.console = IntegratedConsole()
        self.console.Console("Starting init")
    def UnzipRessourcesFolder(self):
        if not os.path.isdir("ressources"):
            import zipfile
            zip_ref = zipfile.ZipFile("ressources.zip", 'r')
            zip_ref.extractall("")
            zip_ref.close()
    def GetMenuTextureList(self):
        self.console.Console("Getting menu texture's list")
        self.IntTxtrList={}
        file=open("ressources/textures/interface/textures.cfg", "r")
        content=file.read()
        file.close()
        content=content.replace(" ","")
        temp=content.split("\n")
        for item in temp:
            temp2=item.split("=")
            self.IntTxtrList[temp2[0]]=PhotoImage(file=temp2[1])
        self.console.Console("Texture list get")
    def GetFightTextureList(self):
        self.console.Console("Getting fignt texture's list")
        self.FightTxtrList={}
        file=open("ressources/textures/fight/textures_fight.cfg", "r")
        content=file.read()
        file.close()
        content=content.replace(" ","")
        temp=content.split("\n")
        for item in temp:
            temp2=item.split("=")
            self.FightTxtrList[temp2[0]]=PhotoImage(file=temp2[1])
        self.console.Console("Texture list get")
    def GetMenuConfig(self):
        dico={}
        file=open("ressources/save/config/MenuMain.cfg", "r")
        content=file.read()
        file.close()
        content=content.replace(" ", "")
        temp=content.split("\n")
        for current in temp:
            if current!="":
                temp2=current.split("=")
                dico[temp2[0]]=temp2[1]
        self.AddToConfigList(dico)
    def GetPlayerData(self, location=""):
        dico={}
        file=open("ressources/save/{}/PlayerData.cfg".format(location), "r")
        content=file.read()
        file.close()
        content=content.replace(" ", "")
        temp=content.split("\n")
        for current in temp:
            if current!="":
                temp2=current.split("=")
                dico[temp2[0]]=temp2[1]
        self.AddToConfigList(dico)
    def GetHousesConfig(self):
        self.MapConfig={}
        file=open("ressources/environment/houses/houses_location.cfg")
        content=file.read()
        file.close()
        content=content.replace(" ", "")
        temp=content.split("\n")
        for current in temp:
            if current!="":
                temp2=current.split("=")
                self.MapConfig[temp2[0]]=temp2[1]
    def InitWindow(self):
        Tk.__init__(self)
        self.geometry("750x750+10+10")
        self.title("RPG")
        self.resizable(height=False, width=False)
        self.protocol("WM_DELETE_WINDOW", self.onWindowClosing)
    def onWindowClosing(self):
        self.destroy()

class SoundGestionnary():
    #Gestionnaire permettant de jouer ou stopper les differents sons du jeu
    def __init__(self):
        pygame.mixer.init()
    def PlaySound(self, sound):
        pygame.mixer.music.load("ressources/sounds/{}.mp3".format(sound))
        pygame.mixer.music.play(0)
    def StopLastSound(self):
        self.son.stop()
    def StopAllSounds(self):
        pygame.mixer.music.stop()

class Fight():
    def __init___(self):
        pass
    def Start_Fight(self, Ennemy=None):
        self.onFight=True
        self.Reset()
        self.PVE=1500000
        self.PVE_max=1500000
        self.defenceE=50
        self.manaE=100
        self.manaE_max=100
        self.SpeedE=1
        self.StrengthE=10
        self.Magic_AffinityE=10
        self.esquiveE=5
        self.statutE="RAS"
        self.esquive=5
        if self.Speed>=self.SpeedE:
            self.Reset_Visual()
        else:
            self.tour_enemie()
    def Reset_Visual(self):
        self.Reset()
        if self.statut=="Poison":
            self.PV=self.PV-(1/10*self.PV)
        print("a ton tour")
        self.statutE="RAS"
        self.MainCan = Canvas(self, width=750, height=750, bg="white", highlightthickness=0)
        self.MainCan.pack()
        self.CreateAllCan(100,40,10,640,self.FightTxtrList["arme_principale"], "arme_principale", self.onFightClick)
        self.CreateAllCan(100,40,10,680,self.FightTxtrList["arme_secondaire"], "arme_secondaire", self.onFightClick)
        self.CreateAllCan(100,40,110,640,self.FightTxtrList["magie"], "magie", self.onFightClick)
        self.CreateAllCan(100,40,110,680,self.FightTxtrList["defense"], "defense", self.onFightClick)
        self.CreateAllCan(100,40,210,640,self.FightTxtrList["sac"], "sac", self.onFightClick)
        self.CreateAllCan(100,40,210,680,self.FightTxtrList["fuite"], "fuite", self.onFightClick)
        self.font=Font(family="Helvetica",size=14)
        self.armureLabel=Label(self.MainCan, text="Armure: "+str(int(self.armure)),font=self.font, bg="white")
        self.armureLabel.place(x=600, y=590)
        self.armureELabel=Label(self.MainCan, text="Armure: "+str(int(self.defenceE)),font=self.font, bg="white")
        self.armureELabel.place(x=10, y=10)
        self.StatutLabel=Label(self.MainCan, text="statut:"+self.statut,font=self.font, bg="white")
        self.StatutLabel.place(x=600, y=550)
        self.PVLabel=Label(self.MainCan, text="PV: "+str(int(self.PV))+"/"+str(int(self.PV_Max)),font=self.font, bg="white")
        self.PVLabel.place(x=600, y=630)
        self.ManaLabel=Label(self.MainCan, text="Mana: "+str(int(self.Mana))+"/"+str(int(self.Mana_Max)),font=self.font, bg="white")
        self.ManaLabel.place(x=600, y=670)
        self.PVELabel=Label(self.MainCan, text="PV: "+str(int(self.PVE))+"/"+str(int(self.PVE_max)),font=self.font, bg="white")
        self.PVELabel.place(x=10, y=50)
        self.ManaELabel=Label(self.MainCan, text="Mana: "+str(int(self.manaE))+"/"+str(int(self.manaE_max)),font=self.font, bg="white")
        self.ManaELabel.place(x=10, y=90)
    def tour_enemie(self):
        self.Reset()
        if self.statutE=="stun":
            self.Reset_Visual()
        else:
            print("c'est a l'enemie de jouer")
            self.MainCan = Canvas(self, width=750, height=750, bg="white", highlightthickness=0)
            self.MainCan.pack()
            self.CreateAllCan(100,40,10,640,self.FightTxtrList["arme_principale"], "arme_principale", self.onFightClick)
            self.CreateAllCan(100,40,10,680,self.FightTxtrList["arme_secondaire"], "arme_secondaire", self.onFightClick)
            self.CreateAllCan(100,40,110,640,self.FightTxtrList["magie"], "magie", self.onFightClick)
            self.CreateAllCan(100,40,110,680,self.FightTxtrList["sac"], "sac", self.onFightClick)
            self.CreateAllCan(100,40,210,640,self.FightTxtrList["fuite"], "fuite", self.onFightClick)
            self.font=Font(family="Helvetica",size=14)
            self.armureLabel=Label(self.MainCan, text="Armure: "+str(int(self.armure)),font=self.font, bg="white")
            self.armureLabel.place(x=600, y=590)
            self.armureELabel=Label(self.MainCan, text="Armure: "+str(int(self.defenceE)),font=self.font, bg="white")
            self.armureELabel.place(x=10, y=10)
            self.StatutLabel=Label(self.MainCan, text="statut:"+self.statut,font=self.font, bg="white")
            self.StatutLabel.place(x=600, y=550)
            self.PVLabel=Label(self.MainCan, text="PV: "+str(int(self.PV))+"/"+str(int(self.PV_Max)),font=self.font, bg="white")
            self.PVLabel.place(x=600, y=630)
            self.ManaLabel=Label(self.MainCan, text="Mana: "+str(int(self.Mana))+"/"+str(int(self.Mana_Max)),font=self.font, bg="white")
            self.ManaLabel.place(x=600, y=670)
            self.PVELabel=Label(self.MainCan, text="PV: "+str(int(self.PVE))+"/"+str(int(self.PVE_max)),font=self.font, bg="white")
            self.PVELabel.place(x=10, y=50)
            self.ManaELabel=Label(self.MainCan, text="Mana: "+str(int(self.manaE))+"/"+str(int(self.manaE_max)),font=self.font, bg="white")
            self.ManaELabel.place(x=10, y=90)
            r=randint(0,100)
            if r<50:
                threading.Thread(target=self.heavy_attackE).start()
            else:
                threading.Thread(target=self.Basic_AttackE).start()



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
    def onAttaqueClick(self, evt, arg):
        if arg=="basic attack":
            self.Basic_Attack()
        if arg=="heavy attack":
            self.heavy_attack()
        if arg=="coup_de_bouclier":
            self.coup_de_bouclier()
        if arg=="protection_attaque_lourd":
            self.protection_attaque_lourd()
        if arg=="protection_attaque_legere":
            self.protection_attaque_legere()
        if arg=="retour":
            self.Reset_Visual()
    def onMagicClick(self, evt, arg):
        if arg=="retour":
            self.Start_Fight()

    def Fuite(self):
        if self.Speed>0.5: #0.5= vitesse de l'enemie
            self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
        else:
            pass
    def arme_principale(self):
        self.hand="principal"
        if self.Equipment["principal_hand"].type=="one_hand":
            self.CreateAllCan(100,40,10,640,self.FightTxtrList["attaque_1"], "basic attack", self.onAttaqueClick)
            self.CreateAllCan(100,40,10,680,self.FightTxtrList["attaque_2"], "heavy attack", self.onAttaqueClick)
            self.CreateAllCan(100,40,110,640,self.FightTxtrList["blanc"], "", self.onAttaqueClick)
            self.CreateAllCan(100,40,110,680,self.FightTxtrList["blanc"], "", self.onAttaqueClick)
            self.CreateAllCan(100,40,210,640,self.FightTxtrList["retour"], "retour", self.onAttaqueClick)
    def arme_secondaire(self):
        self.hand="secondary"
        if self.Equipment["secondary_hand"].type=="shield":
            self.CreateAllCan(100,40,10,640,self.FightTxtrList["attaque_1"], "coup_de_bouclier", self.onAttaqueClick)
            self.CreateAllCan(100,40,10,680,self.FightTxtrList["attaque_2"], "protection_attaque_lourd", self.onAttaqueClick)
            self.CreateAllCan(100,40,110,640,self.FightTxtrList["attaque_1"], "protection_attaque_legere", self.onAttaqueClick)
            self.CreateAllCan(100,40,110,680,self.FightTxtrList["blanc"], "", self.onAttaqueClick)
            self.CreateAllCan(100,40,210,640,self.FightTxtrList["retour"], "retour", self.onAttaqueClick)
        elif self.Equipment["secondary_hand"].type=="one_hand":
            self.CreateAllCan(100,40,10,640,self.FightTxtrList["attaque_1"], "basic attack", self.onAttaqueClick)
            self.CreateAllCan(100,40,10,680,self.FightTxtrList["attaque_2"], "heavy attack", self.onAttaqueClick)
            self.CreateAllCan(100,40,110,640,self.FightTxtrList["blanc"], "", self.onAttaqueClick)
            self.CreateAllCan(100,40,110,680,self.FightTxtrList["blanc"], "", self.onAttaqueClick)
            self.CreateAllCan(100,40,210,640,self.FightTxtrList["retour"], "retour", self.onAttaqueClick)
    def Magie(self):
        self.CreateAllCan(100,40,10,640,self.FightTxtrList["blanc"], "", self.onMagicClick)
        self.CreateAllCan(100,40,10,680,self.FightTxtrList["blanc"], "", self.onMagicClick)
        self.CreateAllCan(100,40,110,640,self.FightTxtrList["blanc"], "", self.onMagicClick)
        self.CreateAllCan(100,40,110,680,self.FightTxtrList["blanc"], "", self.onMagicClick)
        self.CreateAllCan(100,40,210,640,self.FightTxtrList["retour"], "retour", self.onMagicClick)
    def sac(self):
        self.tour_enemie


    def heavy_attack(self):
        self.chance_de_toucher=80
        r=randint(0,100)
        if self.hand=="principal":
            degats=(self.Equipment["principal_hand"].damage*self.Strength)+5
        else:
            degats=(self.Equipment["secondary_hand"].damage*self.Strength)+5
        if self.chance_de_toucher-self.esquiveE>r:
            if self.defenceE>degats:
                self.defenceE=self.defenceE-((95/100)*degats)
                self.PVE=self.PVE-((5/100)*degats)
            elif self.defenceE==0:
                self.defenceE=0
                self.PVE=self.PVE-degats
            elif 0<self.defenceE<degats:
                degatsvie=degats-self.defenceE
                self.defenceE=0
                self.PVE=self.PVE-degatsvie
            self.esquive=0
        else:
            self.PrintMessage("l'enemie a esquive")
        self.tour_enemie()

    def Basic_Attack (self):
        self.chance_de_toucher=100
        r=randint(0,100)
        if self.hand=="principal":
            degats=self.Equipment["principal_hand"].damage*self.Strength
        else:
            degats=self.Equipment["secondary_hand"].damage*self.Strength
        if self.chance_de_toucher-self.esquiveE>r:
            if self.defenceE>=degats:
                self.defenceE=self.defenceE-degats
            elif self.defenceE==0:
                self.PVE=self.PVE-degats
            elif 0<self.defenceE<degats:
                degatsvie=degats-self.defenceE
                self.defenceE=0
                self.PVE=self.PVE-degatsvie
        else:
            self.PrintMessage("l'enemie a esquive")
        self.tour_enemie()

    def coup_de_bouclier(self):
        self.chance_de_toucher=100
        r=randint(0,100)
        degats=self.Equipment["secondary_hand"].damage*self.Strength
        if self.chance_de_toucher-self.esquiveE>r:
            if self.defenceE>=degats:
                self.defenceE=self.defenceE-degats
            elif self.defenceE==0:
                self.PVE=self.PVE-degats
            elif 0<self.defenceE<degats:
                degatsvie=degats-self.defenceE
                self.defenceE=0
                self.PVE=self.PVE-degatsvie
        else:
            self.PrintMessage("l'enemie a esquive")
        r2=randint(0,100)
        if r2<=80:
            self.tour_enemie()
        else:
            self.PrintMessage("l'enemie est stun")
            self.statutE="stun"
            self.tour_enemie()

    def protection_attaque_lourd(self):
        self.protection_attaque_lourde=2
        self.protection_attaque_legere=0.5
        self.tour_enemie()


    def Heal(self):
        if self.Mana>0 and self.PV<100:
            self.PV=self.PV+(10)# 10= la puissance du sort
            self.Mana=self.Mana-(10)#10= cout en mana du sort
        else:
            pass
        if self.PV>100:
            self.PV=100
        self.Start_Fight()


    def heavy_attackE(self):
         print("attendez")
         sleep(5)
         self.chance_de_toucher=80
         r=randint(0,100)
         if self.chance_de_toucher-self.esquive>r:
            degats=(((5*self.StrengthE)+5)/self.protection_attaque_lourde)*self.protection_attaque_legere
            if self.armure>degats:
                self.armure=self.armure-((95/100)*degats)
                self.PV=self.PV-((5/100)*degats)
            elif self.armure==0:
                self.armure=0
                self.PV=self.PV-degats
            elif 0<self.armure<degats:
                degatsvie=degats-self.armure
                self.armure=0
                self.PV=self.PV-degatsvie
            self.esquiveE=0
         else:
            self.PrintMessage("l'enemie a rate")
         self.protection_attaque_lourde=1
         self.protection_attaque_legere=1
         self.Reset_Visual()


    def Basic_AttackE(self):
        print("attendez")
        sleep(5)
        self.chance_de_toucher=100
        r=randint(0,100)
        degats=((10*self.StrengthE)/self.protection_attaque_legere)*self.protection_attaque_lourde
        if self.chance_de_toucher-self.esquive>r:
            if self.armure>=degats:
                self.armure=self.armure-degats
            elif self.armure==0:
                self.statut="Poison"
                print("vous etes empoisonne")
                self.PV=self.PV-degats
            elif 0<self.armure<degats:
                degatsvie=degats-self.armure
                self.armure=0
                self.PV=self.PV-degatsvie
                self.statut="Poison"
                print("vous etes empoisonne")
        else:
            self.PrintMessage("vous avez esquive")
        self.Reset_Visual()



    def PrintMessage(self, msg):#Fonction que tu appelle
        threading.Thread(target=self.__PrintMessage, args=(msg,)).start()
    def __PrintMessage(self, msg):
        rateLabel=Label( text=msg,font=self.font, bg="white")
        rateLabel.place(x=375, y=375)
        sleep(5)
        rateLabel=Label( text="",font=self.font, bg="white")

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

class Init(SoundGestionnary, Fight):
    #Classement des donnees
    def __init__(self):
        SoundGestionnary.__init__(self)
        self.LoadItems()
        self.RenderItems()
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
    def RenderItems(self):
        for item in self.itemObjectList:
            item.texture=PhotoImage(file=item.texture_acces)
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
                obj.texture_acces=obj_dict["texture_acces"]
                return obj
        return obj_dict

class OptionMenuMain():
    def __init__(self):
        pass
    def Start(self):
        self.Reset()
        self.MainCan = Canvas(self, width=750, height=750, bg="#9a9a9a", highlightthickness=0)
        self.MainCan.pack()
        self.CreateAllCan(330,90,230,10,self.IntTxtrList["option_title"], "", self.onClick)
        self.CreateAllCan(90,90,650,650,self.IntTxtrList["quitter"], "retour_menu", self.onClick)
        self.CreateAllCan(330,90,35,200,self.IntTxtrList["rotation"], "", self.onClick)
        self.CreateAllCan(330,90,35,350,self.IntTxtrList["one_image"], "", self.onClick)
        if self.canRotate==True:
            self.CreateAllCan(90,90,380,200,self.IntTxtrList["green"], "rotation", self.onClick)
        else:
            self.CreateAllCan(90,90,380,200,self.IntTxtrList["red"], "rotation", self.onClick)
        if self.oneImage==True:
            self.CreateAllCan(90,90,380,350,self.IntTxtrList["green"], "oneImage", self.onClick)
        else:
            self.CreateAllCan(90,90,380,350,self.IntTxtrList["red"], "oneImage", self.onClick)
class MenuMain(OptionMenuMain):
    def __init__(self):
        OptionMenuMain.__init__(self)
        self.InitGUI()
    def ResetGUI(self):
        for i in self.winfo_children():
            i.destroy()
    def InitGUI(self):
        self.ResetGUI()
        self.title("Void - RPG")
        self.SetGUI()
        self.SetButtons()
    def SetGUI(self):
        self.MainCan = Canvas(self, width=750, height=750, bg="#9a9a9a", highlightthickness=0)
        self.MainCan.pack()
    def SetButtons(self):
        self.CanList=[]
        Label(self.MainCan, text="Coding : Czekaj Tom\nGraphics : Duchene Guillaume, Choin Anatole", bg="#9a9a9a", justify="left").place(x=1,y=712)
        self.CreateAllCan(600,75,75,50,self.IntTxtrList["baniere"], "", self.onClick)
        self.CreateAllCan(50,50,610,680,self.IntTxtrList["option_wheel"], "option", self.onClick)
        self.CreateAllCan(220,75,30,600,self.IntTxtrList["fight"], "fight", self.onClick)
        self.CreateAllCan(50,50,680,680,self.IntTxtrList["quit_button"], "quit", self.onClick)
        if self.ConfigList[0]["save_1"]=="False":
            self.CreateAllCan(220,75,30,300,self.IntTxtrList["create"], "playOne", self.onClick)
        else:
            self.CreateAllCan(220,75,30,300,self.IntTxtrList["create"], "playOne_saved", self.onClick)
        if self.ConfigList[0]["save_2"]=="False":
            self.CreateAllCan(220,75,30,400,self.IntTxtrList["create"], "playTwo", self.onClick)
        else:
            self.CreateAllCan(220,75,30,400,self.IntTxtrList["create"], "playTwo_saved", self.onClick)
        if self.ConfigList[0]["save_3"]=="False":
            self.CreateAllCan(220,75,30,500,self.IntTxtrList["create"], "playThree", self.onClick)
        else:
            self.CreateAllCan(220,75,30,500,self.IntTxtrList["create"], "playThree_saved", self.onClick)
    def CreateAllCan(self, canwidth, canheight, x, y, image, arg, funct):
        self.CanList.append(Canvas(self.MainCan, width=canwidth, height=canheight, bg="#9a9a9a", highlightthickness=0))
        self.CanList[len(self.CanList)-1].place(x=x, y=y)
        self.CanList[len(self.CanList)-1].create_image(0,0, image=image, anchor=NW)
        self.CanList[len(self.CanList)-1].bind("<Button-1>", lambda arg1=None, arg2=arg:funct(arg1, arg2))
    def onClick(self, evt, arg):
        if arg=="fight":
            self.Start_Fight()
        if arg=="retour_menu":
            self.InitGUI()
        if arg=="rotation":
            if self.canRotate==True:
                self.canRotate=False
                self.ConfigList[0]["rotation"]="False"
                self.SaveConfig()
                self.Start()
            else:
                self.canRotate=True
                self.ConfigList[0]["rotation"]="True"
                self.SaveConfig()
                self.Start()
        if arg=="oneImage":
            if self.oneImage==True:
                self.oneImage=False
                self.ConfigList[0]["one_image"]="False"
                self.SaveConfig()
                self.Start()
            else:
                self.oneImage=True
                self.ConfigList[0]["one_image"]="True"
                self.SaveConfig()
                self.Start()
        if arg=="quit":
            self.onWindowClosing()
        if arg=="option":
            self.PlaySound("option_button_sound")
            self.Start()
        if arg=="playOne":
            self.Played=(True, "Save_1")
            self.ConfigList[0]["save_1"]="True"
            self.mapX=10
            self.mapY=9
            self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
            TickGestionary.__init__(self)
        if arg=="playOne_saved":
            try:
                self.GetPlayerData(location="Save_1")
            except FileNotFoundError:
                content=""
                self.ConfigList[0]["save_1"]="False"
                for item in self.ConfigList[0].keys():
                    content+=item+"="+self.ConfigList[0][item]+"\n"
                file=open("ressources/save/config/MenuMain.cfg", "w")
                file.write(content)
                file.close()
                self.InitGUI()
            try:
                self.Played=(True, "Save_1")
                self.mapX=int(self.ConfigList[1]["mapX"])
                self.mapY=int(self.ConfigList[1]["mapY"])
                self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
                TickGestionary.__init__(self)
            except IndexError:
                pass
        if arg=="playTwo":
            self.Played=(True, "Save_2")
            self.ConfigList[0]["save_2"]="True"
            self.mapX=10
            self.mapY=9
            self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
            TickGestionary.__init__(self)
        if arg=="playTwo_saved":
            try:
                self.GetPlayerData(location="Save_2")
            except FileNotFoundError:
                content=""
                self.ConfigList[0]["save_2"]="False"
                for item in self.ConfigList[0].keys():
                    content+=item+"="+self.ConfigList[0][item]+"\n"
                file=open("ressources/save/config/MenuMain.cfg", "w")
                file.write(content)
                file.close()
                self.InitGUI()
            try:
                self.Played=(True, "Save_2")
                self.mapX=int(self.ConfigList[1]["mapX"])
                self.mapY=int(self.ConfigList[1]["mapY"])
                self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
                TickGestionary.__init__(self)
            except IndexError:
                pass
        if arg=="playThree":
            self.Played=(True, "Save_3")
            self.ConfigList[0]["save_3"]="True"
            self.mapX=10
            self.mapY=9
            self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
            TickGestionary.__init__(self)
        if arg=="playThree_saved":
            try:
                self.GetPlayerData(location="Save_3")
            except FileNotFoundError:
                content=""
                self.ConfigList[0]["save_3"]="False"
                for item in self.ConfigList[0].keys():
                    content+=item+"="+self.ConfigList[0][item]+"\n"
                file=open("ressources/save/config/MenuMain.cfg", "w")
                file.write(content)
                file.close()
                self.InitGUI()
            try:
                self.Played=(True, "Save_3")
                self.mapX=int(self.ConfigList[1]["mapX"])
                self.mapY=int(self.ConfigList[1]["mapY"])
                self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
                TickGestionary.__init__(self)
            except IndexError:
                pass

class ColliderObject():
    def __init__(self, xcord, ray, colType="", colliderEvt=None):
        self.CreateColliderObject(xcord, ray, colType, colliderEvt)
    def CreateColliderObject(self, xcord, ray, colEncode, colliderEvt):
        self.cornerCoords={}
        self.cornerCoords={"top_left":xcord,
                           "top_right":((xcord[0]+ray), xcord[1]),
                           "bot_left":(xcord[0], (xcord[1]+ray)),
                           "bot_right":((xcord[0]+ray), (xcord[1]+ray)),
                           "collider_encode": colEncode,
                           "collider_event": colliderEvt}
        #print(self.cornerCoords)

class Collider():
    def __init__(self):
        pass
    def IsCollide(self, collider2, collider1):
        returning=False
        coords1=collider1.cornerCoords["bot_right"]
        coords2=collider2.cornerCoords["top_left"]
        vecteur=(coords2[0]-coords1[0],coords2[1]-coords1[1])
        if vecteur[0]<=0 and vecteur[1]<=0:
            coords1=collider1.cornerCoords["top_left"]
            coords2=collider2.cornerCoords["bot_right"]
            vecteur=(coords2[0]-coords1[0],coords2[1]-coords1[1])
            if vecteur[0]>=0 and vecteur[1]>=0:
                returning=True

        return returning
    def CheckMultipleColliders(self, collider1, colliderlist):
        returning=(False, None)
        for i in range(len(colliderlist)):
            if self.IsCollide(collider1, colliderlist[i]):
                returning=(True, colliderlist[i].cornerCoords["collider_event"])
                #print(collider1.cornerCoords)
        if returning[1]!=None:
            self.functionToExecute=returning[1]
        else:
            self.functionToExecute=lambda: None
        return returning
    def CheckMapChanging(self, mapcoords, newplayercollider):
        #Loading
        try:
            file=open("ressources/maps/earth_{}_{}.map".format(mapcoords[0], mapcoords[1]), "r")
            content=file.read()
            file.close()
            temp1=content.split("\n")
            Matrice=[]
            for i in range(len(temp1)):
                temp=[]
                for j in range(0, len(temp1[i]), 2):
                    temp2=""
                    temp2+=temp1[i][j]
                    temp2+=temp1[i][j+1]
                    temp.append(temp2)
                Matrice.append(temp)
        except FileNotFoundError as e:
            return False
        #Collider Creating
        ColliderList=[]
        #self.isColliderList=["ap", "ao", "ar", "as", "aq", "aj", "ak", "ba", "bc", "bd", "be", "bf", "bh", "bi", "bb", "au", "av", "aw", "ax", "ay", "az", "aa"]
        for i in range(len(Matrice)):
            for j in range(len(Matrice[i])):
                if Matrice[i][j] in self.isColliderList:
                    ColliderList.append(ColliderObject((int(j*25), int(i*25)), 25, colType=Matrice[i][j]))
        #print(ColliderList)
        returning = self.CheckMultipleColliders(newplayercollider, ColliderList)
        return returning[0]

class TickGestionary(Collider):
    def __init__(self):
        self.main_loop_on=True
        threading.Thread(target=self.MainLoop).start()
        threading.Thread(target=self.MovingIA).start()
    def MainLoop(self):
        threading.Thread(target=LiveInfos, args=(self,)).start()
        xinfos={"multiplier":1, "deceleration":False, "accel_nbre":1, "decel_nbre":1}
        yinfos={"multiplier":1, "deceleration":False, "accel_nbre":1, "decel_nbre":1}
        while self.main_loop_on:
            sleep(.01)
            if self.onFight==False:
                t1=time.time()
                try:
                    try:
                        lastxdir = xdir
                        lastydir = ydir
                    except UnboundLocalError:
                        lastxdir = 0
                        lastydir = 0
                    xdir = -self.dirXm + self.dirXp
                    ydir = -self.dirYm + self.dirYp

                    if lastxdir!=xdir:
                        xinfos["deceleration"], xinfos["decel_dir"] = True, lastxdir
                        xinfos["decel_multiplier"]=xinfos["multiplier"]
                        xinfos["accel_nbre"], xinfos["decel_nbre"] = 1, 1
                        xinfos["multiplier"] = 1

                    if lastydir!=ydir:
                        yinfos["deceleration"], yinfos["decel_dir"] = True, lastydir
                        yinfos["decel_multiplier"]=yinfos["multiplier"]
                        yinfos["accel_nbre"], yinfos["decel_nbre"] = 1, 1
                        yinfos["multiplier"] = 1



                    #Gestion de la deceleration
                    if xinfos["deceleration"]==True:
                        xinfos["decel_nbre"]+=1
                        if xinfos["decel_multiplier"]>1:
                            if xinfos["decel_nbre"]%randint(1, 2)==0:
                                xinfos["decel_multiplier"]-=0.10
                                self.x+=xinfos["decel_dir"]*xinfos["decel_multiplier"]
                                if self.x<0:
                                    if self.CheckMapChanging((self.mapX-1, self.mapY), ColliderObject((self.x+750, self.y+2), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.x-=xinfos["decel_dir"]*xinfos["decel_multiplier"]
                                elif self.x>725:
                                    if self.CheckMapChanging((self.mapX+1, self.mapY), ColliderObject((self.x-750, self.y+2), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.x-=xinfos["decel_dir"]*xinfos["decel_multiplier"]
                                else:
                                    if self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.x-=xinfos["decel_dir"]*xinfos["decel_multiplier"]
                            else:
                                self.x+=xinfos["decel_dir"]*xinfos["decel_multiplier"]
                                if self.x<0:
                                    if self.CheckMapChanging((self.mapX-1, self.mapY), ColliderObject((self.x+750, self.y+2), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.x-=xinfos["decel_dir"]*xinfos["decel_multiplier"]
                                elif self.x>725:
                                    if self.CheckMapChanging((self.mapX+1, self.mapY), ColliderObject((self.x-750, self.y+2), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.x-=xinfos["decel_dir"]*xinfos["decel_multiplier"]
                                else:
                                    if self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.x-=xinfos["decel_dir"]*xinfos["decel_multiplier"]
                        else:
                            xinfos["deceleration"]=False

                    if yinfos["deceleration"]==True:
                        yinfos["decel_nbre"]+=1
                        if yinfos["decel_multiplier"]>1:
                            if yinfos["decel_nbre"]%randint(1, 2)==0:
                                yinfos["decel_multiplier"]-=0.10
                                self.y+=yinfos["decel_dir"]*yinfos["decel_multiplier"]
                                if self.y<0:
                                    if self.CheckMapChanging((self.mapX, self.mapY+1), ColliderObject((self.x+2, self.y+750), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.y-=yinfos["decel_dir"]*yinfos["decel_multiplier"]
                                elif self.y>725:
                                    if self.CheckMapChanging((self.mapX, self.mapY-1), ColliderObject((self.x+2, self.y-750), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.y-=yinfos["decel_dir"]*yinfos["decel_multiplier"]
                                else:
                                    if self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.y-=yinfos["decel_dir"]*yinfos["decel_multiplier"]
                                        self.functionToExecute()
                            else:
                                self.y+=yinfos["decel_dir"]*yinfos["decel_multiplier"]
                                if self.y<0:
                                    if self.CheckMapChanging((self.mapX, self.mapY+1), ColliderObject((self.x+2, self.y+750), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.y-=yinfos["decel_dir"]*yinfos["decel_multiplier"]
                                elif self.y>725:
                                    if self.CheckMapChanging((self.mapX, self.mapY-1), ColliderObject((self.x+2, self.y-750), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.y-=yinfos["decel_dir"]*yinfos["decel_multiplier"]
                                else:
                                    if self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                        self.y-=yinfos["decel_dir"]*yinfos["decel_multiplier"]
                                        self.functionToExecute()
                        else:
                            yinfos["deceleration"]=False

                    #Acceleration dans tous les cas
                    if xdir!=0:
                        xinfos["accel_nbre"]+=1
                    if xinfos["multiplier"]<=2.2 and xinfos["accel_nbre"]%8==0:
                        xinfos["multiplier"]+=0.2
                        self.x+=lastxdir*xinfos["multiplier"]
                        if self.x<0:
                            if self.CheckMapChanging((self.mapX-1, self.mapY), ColliderObject((self.x+750, self.y+2), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.x-=lastxdir*xinfos["multiplier"]
                        elif self.x>725:
                            if self.CheckMapChanging((self.mapX+1, self.mapY), ColliderObject((self.x-750, self.y+2), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.x-=lastxdir*xinfos["multiplier"]
                        else:
                            if self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.x-=lastxdir*xinfos["multiplier"]
                                self.functionToExecute()
                    else:
                        self.x+=lastxdir*xinfos["multiplier"]
                        if self.x<0:
                            if self.CheckMapChanging((self.mapX-1, self.mapY), ColliderObject((self.x+750, self.y+2), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.x-=lastxdir*xinfos["multiplier"]
                        elif self.x>725:
                            if self.CheckMapChanging((self.mapX+1, self.mapY), ColliderObject((self.x-750, self.y+2), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.x-=lastxdir*xinfos["multiplier"]
                        else:
                            if self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.x-=lastxdir*xinfos["multiplier"]
                                self.functionToExecute()


                    if ydir!=0:
                        yinfos["accel_nbre"]+=1
                    if yinfos["multiplier"]<=2.2 and yinfos["accel_nbre"]%8==0:
                        yinfos["multiplier"]+=0.2
                        self.y+=lastydir*yinfos["multiplier"]
                        if self.y<0:
                            if self.CheckMapChanging((self.mapX, self.mapY+1), ColliderObject((self.x+2, self.y+750), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.y-=lastydir*yinfos["multiplier"]
                        elif self.y>725:
                            if self.CheckMapChanging((self.mapX, self.mapY-1), ColliderObject((self.x+2, self.y-750), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.y-=lastydir*yinfos["multiplier"]
                        else:
                            if self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.y-=lastydir*yinfos["multiplier"]
                                self.functionToExecute()
                    else:
                        self.y+=lastydir*yinfos["multiplier"]
                        if self.y<0:
                            if self.CheckMapChanging((self.mapX, self.mapY+1), ColliderObject((self.x+2, self.y+750), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.y-=lastydir*yinfos["multiplier"]
                        elif self.y>725:
                            if self.CheckMapChanging((self.mapX, self.mapY-1), ColliderObject((self.x+2, self.y-750), 21)) or self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.y-=lastydir*yinfos["multiplier"]
                        else:
                            if self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.ColliderList)[0]:
                                self.y-=lastydir*yinfos["multiplier"]
                                self.functionToExecute()


                    #Changement de map
                    if self.x>730:
                        self.x=0
                        self.mapX+=1
                        self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
                    elif self.x<-5:
                        self.x=725
                        self.mapX-=1
                        self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
                    elif self.y>730:
                        self.y=0
                        self.mapY-=1
                        self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
                    elif self.y<-5:
                        self.y=725
                        self.mapY+=1
                        self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))

                    if self.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.IAColliderList)[0]:
                        self.functionToExecute()

                    #Actualisation visuelle
                    #print(xinfos)
                    #print(yinfos)
                    self.MainCan.coords(self.player, self.x, self.y)
                    t2=time.time()
                    #print(t2-t1)
                except AttributeError as e:
                    pass
                except RuntimeError as e:
                    pass
                except TclError as e:
                    pass
    def MovingIA(self):
        try:
            self.IAColliderList=[None]
            while self.main_loop_on:
                sleep(.01)
                for ia in self.IAList:
                    ia.Move()
                    for i in range(len(self.IAList)):
                        self.IAColliderList[i]=self.IAList[i].EnnemyCollider
        except RuntimeError:
            pass

class Moving(Collider):
    def __init__(self, parent):
        self.move_on=False
        self.parent=parent
    def StartMove(self, xDir, yDir):
        pass

class Player():
    def __init__(self):
        try:
            self.x=float(self.ConfigList[1]["x"])
            self.y=float(self.ConfigList[1]["y"])
            #Equipement
            self.Equipment={
            "principal_hand":self.itemObjectList[1],
            "secondary_hand":self.itemObjectList[2]
            }
            #stat
            self.PV=float(self.ConfigList[1]["PV"])
            self.Speed=float(self.ConfigList[1]["speed"])
            self.Magic_Affinity=float(self.ConfigList[1]["magic_affinity"])
            self.Strength=float(self.ConfigList[1]["strength"])
            self.Mana=float(self.ConfigList[1]["mana"])
            self.PV_Max=float(self.ConfigList[1]["PV_max"])
            self.Mana_Max=float(self.ConfigList[1]["mana_max"])
            self.defense=float(self.ConfigList[1]["defense"])
            self.statut="RAS"
            self.armure=self.defense+self.itemObjectList[0].prot
            self.protection_attaque_legere=1
            self.protection_attaque_lourde=1
        except IndexError:
            self.Equipment={
            "principal_hand":self.itemObjectList[1],
            "secondary_hand":self.itemObjectList[2]
            }
            self.x=600.0
            self.y=500.0
            self.PV=100
            self.Speed=1
            self.Strength=10
            self.Magic_Affinity=10
            self.Mana=100
            self.PV_Max=100
            self.Mana_Max=100
            self.defense=1.0
            self.statut="RAS"
            self.armure=self.defense+self.itemObjectList[0].prot
            self.protection_attaque_legere=1
            self.protection_attaque_lourde=1


        self.moveInstances={}
        self.playerImg = PhotoImage(file="ressources/textures/player/player_0.png")
        self.Init2()
    def Init2(self):
        self.dirYp, self.dirYm, self.dirXm, self.dirXp = 0, 0, 0, 0
        self.player = self.MainCan.create_image(self.x, self.y, image=self.playerImg, anchor=NW)
        self.playerCollider=[ColliderObject((self.x, self.y), 25)]
    def PlayerEvt(self, evt, arg):
        #print(evt.keysym, arg)
        if arg=="KeyPress":
            if evt.keysym.lower()=="z":
                try:
                    if self.dirYm==0:
                        self.dirYm=1
                except AttributeError:
                    self.dirYm=1
            elif evt.keysym.lower()=="s":
                try:
                    if self.dirYp==0:
                        self.dirYp=1
                except AttributeError:
                    self.dirYp=1
            elif evt.keysym.lower()=="q":
                try:
                    if self.dirXm==0:
                        self.dirXm=1
                except AttributeError:
                    self.dirXm=1
            elif evt.keysym.lower()=="d":
                try:
                    if self.dirXp==0:
                        self.dirXp=1
                except AttributeError:
                    self.dirXp=1
        if arg=="KeyRelease":
            if evt.keysym.lower()=="z":
                self.dirYm=0
            elif evt.keysym.lower()=="s":
                self.dirYp=0
            elif evt.keysym.lower()=="q":
                self.dirXm=0
            elif evt.keysym.lower()=="d":
                self.dirXp=0
            elif evt.keysym.lower()=="f":
                threading.Thread(target=self.Start_Fight).start()

class EnnemyIA():
    def __init__(self, x, y, parent):
        self.x=x
        self.y=y
        self.EnnemyCollider = ColliderObject((self.x+2, self.y+2), 21, colliderEvt=lambda arg=self:self.parent.Start_Fight(Ennemy=arg))
        self.maxX=(int(self.x/25)-2, int(self.x/25)+2)
        self.maxY=(int(self.y/25)-2, int(self.y/25)+2)
        self.MainCan=parent.MainCan
        self.parent=parent
        self.IAOn=True
        self.EnnemyImg=PhotoImage(file="ressources/textures/player/player_0.png")
        self.Ennemy = self.MainCan.create_image(self.x, self.y, image=self.EnnemyImg, anchor=NW)
    def Move(self):
        r=randint(0, 250)
        if r==5:
            dirX=randint(-1, 1)
            dirY=randint(-1, 1)
            if dirX!=0 and dirY!=0:
                r=randint(0, 1)
                if r==0:
                    self.StartMove(dirX, 0)
                else:
                    self.StartMove(0, dirY)
            elif dirX==0 and dirY==0:
                self.Move()
            else:
                self.StartMove(dirX, dirY)
    def StartMove(self, dirX, dirY):
        self.x+=dirX*25
        self.y+=dirY*25
        if (not self.maxX[0] < int(self.x/25) < self.maxX[1]) or self.parent.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.parent.ColliderList)[0]:
            self.x-=dirX*25
            self.y-=dirY*25
            self.Move()
        elif (not self.maxY[0] < int(self.y/25) < self.maxY[1]) or self.parent.CheckMultipleColliders(ColliderObject((self.x+2, self.y+2), 21), self.parent.ColliderList)[0]:
            self.x-=dirX*25
            self.y-=dirY*25
            self.Move()
        else:
            try:
                self.MainCan.coords(self.Ennemy, self.x, self.y)
                self.EnnemyCollider = ColliderObject((self.x+2, self.y+2), 21, colliderEvt=lambda arg=self:self.parent.Start_Fight(Ennemy=arg))
            except TclError:
                pass

class GraphicEngine(Player):
    def __init__(self):
        self.isLoading=False
        self.Config()
    def StartGraphicEngine(self, filename, isInMapLocation=True, houseInfos=""):
        if self.isLoading==False:
            self.isInMapLocation=isInMapLocation
            self.isLoading=True
            self.can_move=False
            self.filename=filename
            self.houseInfos=houseInfos
            self.Reset()
            self.Init()
            self.IAList=[]
            self.IAList.append(EnnemyIA(375, 500, self))
            try:
                self.moveInstances
                self.Init2()
            except AttributeError:
                Player.__init__(self)
            except RuntimeError:
                pass
            self.can_move=True
            self.isLoading=False
            self.onFight=False
    def Config(self):
        if self.ConfigList[0]["rotation"]=="True":
            self.canRotate=True
        else:
            self.canRotate=False
        if self.ConfigList[0]["one_image"]=="True":
            self.oneImage=True
        else:
            self.oneImage=False
    def Init(self):
        self.LoadTextureList()
        self.InitInterface()
        self.List=[]
        self.notRotateList=["ap", "au", "av", "aw", "ax", "ay", "as", "aq", "ar", "ao", "an", "am"]
        self.Load(self.filename)
        self.CreateAllColliders()
    def CreateAllColliders(self):
        self.ColliderList=[]
        temp=-1
        self.isColliderList=["ap", "ao", "ar", "as", "aq", "aj", "ak", "ba", "bc", "bd", "be", "bf", "bh", "bi", "bb", "au", "av", "aw", "ax", "ay", "az", "aa"]
        for i in range(len(self.Matrice)):
            for j in range(len(self.Matrice[i])):
                if self.Matrice[i][j] in self.isColliderList:
                    if self.DoCreateCollider(i, j, self.isColliderList):
                        try:
                            if self.Matrice[i][j] in ["ao", "bm"]:
                                temp+=1
                                self.ColliderList.append(ColliderObject((int(j*25), int(i*25)), 25, colliderEvt=lambda arg1="ressources/environment/houses/houses_map/"+self.MapConfig["earth_{}_{}-{}".format(self.mapX, self.mapY, temp)].split("*")[0], arg2=False, arg3=temp:self.StartGraphicEngine(arg1, isInMapLocation=arg2, houseInfos=arg3)))
                            else:
                                self.ColliderList.append(ColliderObject((int(j*25), int(i*25)), 25))
                        except KeyError as e:
                            self.ColliderList.append(ColliderObject((int(j*25), int(i*25)), 25))
        #print(self.ColliderList)
    def DoCreateCollider(self, i, j, isColliderList):
        temp=False
        try:
            if not self.Matrice[i+1][j] in isColliderList:
                temp=True
        except IndexError:pass
        try:
            if not self.Matrice[i-1][j] in isColliderList:
                temp=True
        except IndexError:pass
        try:
            if not self.Matrice[i][j+1] in isColliderList:
                temp=True
        except IndexError:pass
        try:
            if not self.Matrice[i][j-1] in isColliderList:
                temp=True
        except IndexError:pass
        return temp
    def InitMatrice(self):
        self.Matrice=[]
        for i in range(30):
            temp=[]
            for j in range(30):
                temp.append("00")
            self.Matrice.append(temp)
        self.ItemMatrice=[]
        for i in range(30):
            temp=[]
            for j in range(30):
                temp.append(None)
            self.ItemMatrice.append(temp)
        self.select=False
    def InitInterface(self):
        self.LoadTextures()
        self.InitMatrice()
        self.InitMainGui()
    def LoadTextures(self):
        self.TextureList=[]
        self.TextureEncode=[]
        for i in self.textureList.keys():
            if i!="00":
                self.TextureList.append(PhotoImage(file ='ressources/textures/map/{}'.format(self.textureList[i])))
                self.TextureEncode.append(i)
            else:
                pass
    def InitMainGui(self):
        self.MainFrame = Frame(self, bg="light grey", width=750, height=750)
        self.MainFrame.place(x=0, y=0)
        self.MainCan = Canvas(self.MainFrame, highlightthickness=0, width=750, height=750)
        self.MainCan.place(x=0, y=0)
    def Load(self, file):
        try:
            if self.isInMapLocation:
                self.house=-1
                file=open("ressources/maps/{}.map".format(file), "r")
                content=file.read()
                file.close()
            else:
                self.house=self.houseInfos
                file=open("{}.map".format(file), "r")
                content=file.read()
                file.close()
            temp1=content.split("\n")
            self.Matrice=[]
            for i in range(len(temp1)):
                temp=[]
                for j in range(0, len(temp1[i]), 2):
                    temp2=""
                    temp2+=temp1[i][j]
                    temp2+=temp1[i][j+1]
                    temp.append(temp2)
                self.Matrice.append(temp)
            self.LoadMatrice(self.Matrice)
        except FileNotFoundError as e:
            pass
    def LoadMatrice(self, matrice):
        self.MainCan.destroy()
        self.MainCan = Canvas(self.MainFrame, highlightthickness=0, width=750, height=750)
        self.MainCan.place(x=0, y=0)
        self.bind("<KeyPress>", lambda arg1=None, arg2="KeyPress":self.PlayerEvt(arg1, arg2))
        self.bind("<KeyRelease>", lambda arg1=None, arg2="KeyRelease":self.PlayerEvt(arg1, arg2))
        self.PlaceElements(matrice)
        self.PlaceConnectedTextures(matrice)
    def PlaceElements(self, matrice):
        if self.oneImage==True:
            if self.canRotate==True:
                self.RandomList=[1, 0, 3, 3, 0, 3, 3, 2, 2, 3, 3, 0, 3, 0, 1, 2, 2, 3, 3, 1]
                self.CreateTextures(matrice)
                self.LevelImage=self.CreateOnePicture(self.List)
                try:
                    self.MainCan.create_image(0, 0, image=self.LevelImage, anchor=NW)
                except RuntimeError:
                    pass

            else:
                for i in range(len(matrice)):
                    for j in range(len(matrice[i])):
                        if matrice[i][j]!="00":
                            indice=self.TextureEncode.index(matrice[i][j])
                            self.List.append(Image.open("ressources/textures/map/"+self.textureList[self.TextureEncode[indice]]))
                self.LevelImage=self.CreateOnePicture(self.List)
                self.MainCan.create_image(0, 0, image=self.LevelImage, anchor=NW)
        else:
            if self.canRotate==True:
                self.RandomList=[1, 0, 3, 3, 0, 3, 3, 2, 2, 3, 3, 0, 3, 0, 1, 2, 2, 3, 3, 1]
                self.CreateTextures(matrice)
                self.PhotoimageList=[]
                for i in range(len(self.List)):
                    try:
                        self.PhotoimageList.append(ImageTk.PhotoImage(self.List[i]))
                        self.MainCan.create_image((i%30)*25, (i//30)*25, image=self.PhotoimageList[i], anchor=NW)
                    except AttributeError:
                        pass
            else:
                for i in range(len(matrice)):
                    for j in range(len(matrice[i])):
                        if matrice[i][j]!="00":
                            indice=self.TextureEncode.index(matrice[i][j])
                            self.MainCan.create_image(j*25, i*25, image=self.TextureList[indice], anchor=NW)
    def CreateOnePicture(self, liste):
        self.result=Image.new("RGB", (750, 750))
        for i in range(len(liste)):
            self.result.paste(im=liste[i], box=(((i)%30)*25, ((i)//30)*25))
        try:
            return ImageTk.PhotoImage(self.result)
        except RuntimeError:
            pass
        except AttributeError:
            pass
    def CreateTextures(self, matrice):
        nbre=0
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                if matrice[i][j]!="00":
                    indice=self.TextureEncode.index(matrice[i][j])
                    if matrice[i][j] in self.notRotateList:
                        self.List.append(self.Rotate(0, indice))
                    else:
                        can=True
                        try:
                            if can==True and matrice[i-1][j]!=matrice[i][j]:
                                can=False
                        except:
                            pass
                        try:
                            if can==True and matrice[i+1][j]!=matrice[i][j]:
                                can=False
                        except:
                            pass
                        try:
                            if can==True and matrice[i][j-1]!=matrice[i][j]:
                                can=False
                        except:
                            pass
                        try:
                            if can==True and matrice[i][j+1]!=matrice[i][j]:
                                can=False
                        except:
                            pass

                        if can==True:
                            self.List.append(self.Rotate(self.RandomList[nbre%(len(self.RandomList)-1)], indice))
                            nbre+=1
                        else:
                            self.List.append(self.Rotate(0, indice))
    def PlaceConnectedTextures(self, matrice):
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                pass
    def Rotate(self, rotate, indice, null=False):
        if null==False:
            image = Image.open("ressources/textures/map/"+self.textureList[self.TextureEncode[indice]]).rotate(rotate*90)
            return image
        else:
            return None
    def LoadTextureList(self):
        global textureList, encodeList, txtrnameList
        txtrnameList=[]
        file=open("ressources/textures/map/textures.cfg", "r")
        content=file.read()
        file.close()
        content=content.replace(" ", "")
        content=content.replace("\n", "")
        content=content.split(";")
        self.textureList={}
        encodeList=[]
        for i in content:
            try:
                if i!="" or i[0]=="#":
                    temp=i.split("=")
                    self.textureList[temp[0]]=temp[1]
                    encodeList.append(temp[0])
                    if temp[1]!="NONE":
                        txtrnameList.append(temp[1])
            except IndexError:
                pass
    def LoadConnectedTextures(self):
        global connected_textureList
        file=open("ressources/config/connected_textureList.cfg", "r")
        content=file.read()
        file.close()
        content=content.replace(" ","")
        content=content.split("\n")
        connected_textureList={}
        for i in content:
            temp=i.split("=")
            connected_textureList[temp[0]]="ressources/connected_textures/"+temp[1]
    def Reset(self):
        self.MainCan.destroy()

class PostInit(MenuMain, GraphicEngine, TickGestionary):
    #Traitement des donnees et affichage du menu principal
    def __init__(self):
        MenuMain.__init__(self)
        GraphicEngine.__init__(self)
        StoppingGestionnary.__init__(self)
        self.ShowWindow()
    def ShowWindow(self):
        self.mainloop()



class InitGestionnary(PreInit, Init, PostInit):
    #Gere les differentes initialisations
    def __init__(self):
        self.StartInit()
    def StartInit(self):
        PreInit.__init__(self)
        Init.__init__(self)
        PostInit.__init__(self)

class StoppingGestionnary():
    def __init__(self):
        pass
    def StopGame(self):
        self.main_loop_on=False
        sleep(1)
        self.Save()
    def Save(self):
        try:
            if self.Played[0]==True:
                self.SaveFunct(self.Played[1])
        except AttributeError as e:
            pass
    def SaveFunct(self, filename):
        content=""
        for item in self.ConfigList[0].keys():
            content+=item+"="+self.ConfigList[0][item]+"\n"
        file=open("ressources/save/config/MenuMain.cfg", "w")
        file.write(content)
        file.close()
        #
        temp=self.CreatePlayerDataSaving()
        content=""
        for item in temp.keys():
            content+=item+"="+str(temp[item])+"\n"
        if not os.path.exists("ressources/save/"+filename):
            os.makedirs("ressources/save/"+filename)
        file=open("ressources/save/{}/PlayerData.cfg".format(filename), "w")
        file.write(content)
        file.close()
    def CreatePlayerDataSaving(self):
        dico={"x":self.x, "y":self.y, "mapX":self.mapX, "mapY":self.mapY, "PV":self.PV, "speed":self.Speed, "strength":self.Strength, "magic_affinity":self.Magic_Affinity, "mana":self.Mana, "PV_max":self.PV_Max, "mana_max":self.Mana_Max, "defense":self.defense, "house":-self.house}
        return dico
    def DelRessourcesFolder(self):
        shutil.rmtree("ressources")
    def SaveConfig(self):
        content=""
        for item in self.ConfigList[0].keys():
            content+=item+"="+self.ConfigList[0][item]+"\n"
        file=open("ressources/save/config/MenuMain.cfg", "w")
        file.write(content)
        file.close()

class Main(InitGestionnary, StoppingGestionnary):
    def __init__(self):
        InitGestionnary.__init__(self)
        self.StopGame()
        self.StopAllSounds()
        threading.Thread(target=self.console.ClosingConsole).start()



main=Main()
