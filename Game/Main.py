from tkinter import *
from time import sleep
import threading
from PIL import Image, ImageTk
import pygame.mixer
from random import randint
import shutil
import os

class PreInit(Tk):
    #Recuperation des donnees et creation de la fenetre
    def __init__(self):
        self.UnzipRessourcesFolder()
        self.InitWindow()
        self.GetMenuTextureList()
        self.GetMenuConfig()
    def UnzipRessourcesFolder(self):
        if not os.path.isdir("ressources"):
            import zipfile
            zip_ref = zipfile.ZipFile("ressources.zip", 'r')
            zip_ref.extractall("")
            zip_ref.close()
    def GetMenuTextureList(self):
        self.IntTxtrList={}
        file=open("ressources/textures/interface/textures.cfg", "r")
        content=file.read()
        file.close()
        content=content.replace(" ","")
        temp=content.split("\n")
        for item in temp:
            temp2=item.split("=")
            self.IntTxtrList[temp2[0]]=PhotoImage(file=temp2[1])
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
    def InitWindow(self):
        Tk.__init__(self)
        self.geometry("750x750+10+10")
        self.title("RPG")
        self.resizable(height=False, width=False)

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


class Init(SoundGestionnary):
    #Classement des donnees
    def __init__(self):
        SoundGestionnary.__init__(self)
    def AddToConfigList(self, arg):
        try:
            self.ConfigList.append(arg)
        except AttributeError:
            self.ConfigList=[]
            self.ConfigList.append(arg)

class OptionMenuMain():
    def __init__(self):
        pass
    def Start(self):
        self.Reset()
        self.MainCan = Canvas(self, width=750, height=750, bg="#9a9a9a", highlightthickness=0)
        self.MainCan.pack()
        self.CreateAllCan(330,90,230,10,self.IntTxtrList["option_title"], "")
        self.CreateAllCan(90,90,650,650,self.IntTxtrList["quitter"], "retour_menu")
        self.CreateAllCan(330,90,35,200,self.IntTxtrList["rotation"], "")
        self.CreateAllCan(330,90,35,350,self.IntTxtrList["one_image"], "")
        if self.canRotate==True:
            self.CreateAllCan(90,90,380,200,self.IntTxtrList["green"], "rotation")
        else:
            self.CreateAllCan(90,90,380,200,self.IntTxtrList["red"], "rotation")
        if self.oneImage==True:
            self.CreateAllCan(90,90,380,350,self.IntTxtrList["green"], "oneImage")
        else:
            self.CreateAllCan(90,90,380,350,self.IntTxtrList["red"], "oneImage")

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
        self.CreateAllCan(600,75,75,50,self.IntTxtrList["baniere"], "")
        self.CreateAllCan(50,50,610,680,self.IntTxtrList["option_wheel"], "option")
        self.CreateAllCan(220,75,30,600,self.IntTxtrList["fight"], "fight")
        self.CreateAllCan(50,50,680,680,self.IntTxtrList["quit_button"], "quit")
        if self.ConfigList[0]["save_1"]=="False":
            self.CreateAllCan(220,75,30,300,self.IntTxtrList["create"], "playOne")
        else:
            self.CreateAllCan(220,75,30,300,self.IntTxtrList["create"], "playOne_saved")
        if self.ConfigList[0]["save_2"]=="False":
            self.CreateAllCan(220,75,30,400,self.IntTxtrList["create"], "playTwn")
        else:
            pass
        if self.ConfigList[0]["save_3"]=="False":
            self.CreateAllCan(220,75,30,500,self.IntTxtrList["create"], "playThree")
        else:
            pass
    def CreateAllCan(self, canwidth, canheight, x, y, image, arg):
        self.CanList.append(Canvas(self.MainCan, width=canwidth, height=canheight, bg="#9a9a9a", highlightthickness=0))
        self.CanList[len(self.CanList)-1].place(x=x, y=y)
        self.CanList[len(self.CanList)-1].create_image(0,0, image=image, anchor=NW)
        self.CanList[len(self.CanList)-1].bind("<Button-1>", lambda arg1=None, arg2=arg:self.onClick(arg1, arg2))
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
            self.destroy()
        if arg=="option":
            self.PlaySound("option_button_sound")
            self.Start()
        if arg=="playOne":
            self.Played=(True, "Save_1")
            self.ConfigList[0]["save_1"]="True"
            self.mapX=10
            self.mapY=9
            self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
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
            except IndexError:
                pass
class ColliderObject():
    def __init__(self, xcord, ray):
        self.CreateColliderObject(xcord, ray)
    def CreateColliderObject(self, xcord, ray):
        self.cornerCoords={}
        self.cornerCoords={"top_left":xcord,
                           "top_right":((xcord[0]+ray), xcord[1]),
                           "bot_left":(xcord[0], (xcord[1]+ray)),
                           "bot_right":((xcord[0]+ray), (xcord[1]+ray))}
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
        returning=False
        for i in range(len(colliderlist)):
            if self.IsCollide(collider1, colliderlist[i]):
                returning=True
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
        isColliderList=["ap", "ao", "ar", "as", "aq", "aj", "ak", "ba", "bc", "bd", "be", "bf", "bh", "bi", "bb", "au", "av", "aw", "ax", "ay", "az", "aa"]
        for i in range(len(Matrice)):
            for j in range(len(Matrice[i])):
                if Matrice[i][j] in isColliderList:
                    ColliderList.append(ColliderObject((int(j*25), int(i*25)), 25))
        #print(ColliderList)
        returning = self.CheckMultipleColliders(newplayercollider, ColliderList)
        return returning

class TickGestionary(Collider):
    def __init__(self):
        self.main_loop_on=True
        threading.Thread(target=self.MainLoop).start()
    def MainLoop(self):
        global multiplier
        while self.main_loop_on==True:
            sleep(0.01)
            try:
                #print(self.x, self.y)
                if self.x>725 and self.canChangeMap:
                    self.canChangeMap=False
                    if not self.CheckMapChanging((self.mapX+1, self.mapY), ColliderObject((2, self.y+2), 21)):
                        if self.y<0:
                            self.y=0
                        elif self.y>750:
                            self.y=725
                        self.x=0
                        self.mapX+=1
                        self.move_on=False
                        self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
                        self.MainCan.coords(self.player, self.x, self.y)
                    else:
                        self.x-=(1.4*multiplier)
                        self.y-=(0*multiplier)
                        self.playerCollider=[ColliderObject((self.x+2, self.y+2), 21)]
                        canDecelerate=False
                    self.canChangeMap=True
                if self.x<0 and self.canChangeMap:
                    self.canChangeMap=False
                    if not self.CheckMapChanging((self.mapX-1, self.mapY), ColliderObject((727, self.y+2), 21)):
                        if self.y<0:
                            self.y=0
                        elif self.y>750:
                            self.y=725
                        self.x=725
                        self.mapX-=1
                        self.move_on=False
                        self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
                        self.MainCan.coords(self.player, self.x, self.y)
                    else:
                        self.x-=(xDir*multiplier)
                        self.y-=(yDir*multiplier)
                        self.playerCollider=[ColliderObject((self.x+2, self.y+2), 21)]
                        canDecelerate=False
                    self.canChangeMap=True
                if self.y>725 and self.canChangeMap:
                    self.canChangeMap=False
                    if not self.CheckMapChanging((self.mapX, self.mapY-1), ColliderObject((self.x+2, 2), 21)):
                        if self.x<0:
                            self.x=0
                        elif self.x>750:
                            self.x=725
                        self.y=0
                        self.mapY-=1
                        self.move_on=False
                        self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
                        self.MainCan.coords(self.player, self.x, self.y)
                    else:
                        self.x-=(xDir*multiplier)
                        self.y-=(yDir*multiplier)
                        self.playerCollider=[ColliderObject((self.x+2, self.y+2), 21)]
                        canDecelerate=False
                    self.canChangeMap=True
                if self.y<0 and self.canChangeMap:
                    self.canChangeMap=False
                    if not self.CheckMapChanging((self.mapX, self.mapY+1), ColliderObject((self.x+2, 727), 21)):
                        if self.x<0:
                            self.x=0
                        elif self.x>750:
                            self.x=725
                        self.y=725
                        self.mapY+=1
                        self.move_on=False
                        self.StartGraphicEngine("earth_{}_{}".format(self.mapX, self.mapY))
                        self.MainCan.coords(self.player, self.x, self.y)
                    else:
                        self.x-=(xDir*multiplier)
                        self.y-=(yDir*multiplier)
                        self.playerCollider=[ColliderObject((self.x+2, self.y+2), 21)]
                        canDecelerate=False
                    self.canChangeMap=True
            except AttributeError:
                    pass
            except NameError:
                pass

class Moving(Collider):
    def __init__(self, parent):
        self.move_on=False
        self.parent=parent
    def StartMove(self, xDir, yDir):
        global multiplier
        self.parent.canChangeMap=True
        self.move_on=True
        multiplier=1
        nbre=0
        canDecelerate=True
        while self.move_on and self.parent.can_move==True:
            try:
                #print("loading")
                sleep(.01)
                nbre+=1
                if multiplier<=2.2 and nbre%9==0:
                    multiplier+=0.2
                self.parent.x+=(xDir*multiplier)
                self.parent.y+=(yDir*multiplier)
                self.parent.playerCollider=[ColliderObject((self.parent.x+2, self.parent.y+2), 21)]

                if self.CheckMultipleColliders(self.parent.playerCollider[0], self.parent.ColliderList):
                    self.parent.x-=(xDir*multiplier)
                    self.parent.y-=(yDir*multiplier)
                    self.parent.playerCollider=[ColliderObject((self.parent.x+2, self.parent.y+2), 21)]
                    canDecelerate=False
                    #break
                else:
                    canDecelerate=True
                #print(self.parent.playerCollider[0].cornerCoords["top_left"], self.parent.x, self.parent.y)
                self.parent.MainCan.coords(self.parent.player, self.parent.x, self.parent.y)
                self.parent.playerCollider=[ColliderObject((self.parent.x+2, self.parent.y+2), 21)]
            except TclError:
                pass
        nbre=1
        while multiplier>1 and canDecelerate:
            try:
                sleep(.01)
                nbre+=1
                if nbre%randint(1, 2)==0:
                    multiplier-=0.10
                self.parent.x+=(xDir*multiplier)
                self.parent.y+=(yDir*multiplier)
                self.parent.playerCollider=[ColliderObject((self.parent.x+2, self.parent.y+2), 21)]
                if self.CheckMultipleColliders(self.parent.playerCollider[0], self.parent.ColliderList):
                    self.parent.x-=(xDir*multiplier)
                    self.parent.y-=(yDir*multiplier)
                    self.parent.playerCollider=[ColliderObject((self.parent.x+2, self.parent.y+2), 21)]
                    canDecelerate=False
                self.parent.MainCan.coords(self.parent.player, self.parent.x, self.parent.y)
                self.parent.playerCollider=[ColliderObject((self.parent.x+2, self.parent.y+2), 21)]
            except TclError:
                pass

class fight():
    def __init___(self):
        pass

class Player():
    def __init__(self):
        try:
            self.x=float(self.ConfigList[1]["x"])
            self.y=float(self.ConfigList[1]["y"])
            #stat
            self.PV=float(self.ConfigList[1]["PV"])
            self.Defense=float(self.ConfigList[1]["D"])
            self.Attack=float(self.ConfigList[1]["A"])
            self.MagicDefense=float(self.ConfigList[1]["MD"])
            self.MagicAttack=float(self.ConfigList[1]["MA"])
            self.Velocité=float(self.ConfigList[1]["Ve"])
            print(self.PV)
            print(self.Velocité)

        except IndexError:
            self.x=600.0
            self.y=500.0
            self.PV=100
            self.Defense=0
            self.Attack=2
            self.MagicDefense=0
            self.MagicAttack=0
            self.Velocité=100

        self.moveInstances={}
        self.playerImg = PhotoImage(file="ressources/textures/player/player_0.png")
        self.Init2()
    def Init2(self):
        self.player = self.MainCan.create_image(self.x, self.y, image=self.playerImg, anchor=NW)
        self.playerCollider=[ColliderObject((self.x, self.y), 25)]
    def PlayerEvt(self, evt, arg):
        #print(evt.keysym, arg)
        if arg=="KeyPress":
            if evt.keysym.lower()=="z":
                try:
                    if self.moveInstances["z"].move_on==False:
                        threading.Thread(target = self.moveInstances["z"].StartMove, args=(0, -1, )).start()
                except KeyError:
                    self.moveInstances["z"]=Moving(self)
                    threading.Thread(target = self.moveInstances["z"].StartMove, args=(0, -1, )).start()
            elif evt.keysym.lower()=="s":
                try:
                    if self.moveInstances["s"].move_on==False:
                        threading.Thread(target = self.moveInstances["s"].StartMove, args=(0, 1, )).start()
                except KeyError:
                    self.moveInstances["s"]=Moving(self)
                    threading.Thread(target = self.moveInstances["s"].StartMove, args=(0, 1, )).start()
            elif evt.keysym.lower()=="q":
                try:
                    if self.moveInstances["q"].move_on==False:
                        threading.Thread(target = self.moveInstances["q"].StartMove, args=(-1, 0, )).start()
                except KeyError:
                    self.moveInstances["q"]=Moving(self)
                    threading.Thread(target = self.moveInstances["q"].StartMove, args=(-1, 0, )).start()
            elif evt.keysym.lower()=="d":
                try:
                    if self.moveInstances["d"].move_on==False:
                        threading.Thread(target = self.moveInstances["d"].StartMove, args=(1, 0, )).start()
                except KeyError:
                    self.moveInstances["d"]=Moving(self)
                    threading.Thread(target = self.moveInstances["d"].StartMove, args=(1, 0, )).start()
        if arg=="KeyRelease":
            if evt.keysym.lower()=="z":
                self.moveInstances["z"].move_on=False
            elif evt.keysym.lower()=="s":
                self.moveInstances["s"].move_on=False
            elif evt.keysym.lower()=="q":
                self.moveInstances["q"].move_on=False
            elif evt.keysym.lower()=="d":
                self.moveInstances["d"].move_on=False

class GraphicEngine(Player):
    def __init__(self):
        self.isLoading=False
        self.Config()
    def StartGraphicEngine(self, filename):
        if self.isLoading==False:
            self.isLoading=True
            self.can_move=False
            self.filename=filename
            self.Reset()
            self.Init()
            try:
                self.moveInstances
                self.Init2()
            except AttributeError:
                Player.__init__(self)
            except RuntimeError:
                pass
            self.can_move=True
            self.isLoading=False
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
        isColliderList=["ap", "ao", "ar", "as", "aq", "aj", "ak", "ba", "bc", "bd", "be", "bf", "bh", "bi", "bb", "au", "av", "aw", "ax", "ay", "az", "aa"]
        for i in range(len(self.Matrice)):
            for j in range(len(self.Matrice[i])):
                if self.Matrice[i][j] in isColliderList:
                    self.ColliderList.append(ColliderObject((int(j*25), int(i*25)), 25))
        #print(self.ColliderList)
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
        self.MainFrame = Frame(self, bg="purple", width=750, height=750)
        self.MainFrame.place(x=0, y=0)
        self.MainCan = Canvas(self.MainFrame, highlightthickness=0, width=750, height=750)
        self.MainCan.place(x=0, y=0)
    def Load(self, file):
        try:
            file=open("ressources/maps/{}.map".format(file), "r")
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
        TickGestionary.__init__(self)
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
        dico={"x":self.x, "y":self.y, "mapX":self.mapX, "mapY":self.mapY, "PV":self.PV, "d":self.Defense, "A":self.attack, "MD":self.MagicDefense, "MA":self.MagicAttack, "Ve":self.Velocité}
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


main=Main()
