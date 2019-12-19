from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk
from time import sleep
import threading

def LoadTextureList():
    global textureList, encodeList, txtrnameList
    txtrnameList=[]
    file=open("ressources/textures/map/textures.cfg", "r")
    content=file.read()
    file.close()
    content=content.replace(" ", "")
    content=content.replace("\n", "")
    content=content.split(";")
    textureList={}
    encodeList=[]
    for i in content:
        try:
            if i!="" or i[0]=="#":
                temp=i.split("=")
                textureList[temp[0]]=temp[1]
                encodeList.append(temp[0])
                if temp[1]!="NONE":
                    txtrnameList.append(temp[1])
        except IndexError:
            pass
def Init():
    global launchTime
    launchTime=0
def Load():
    global root
    LoadTextureList()
    root = Interface()

class Interface(Tk):
    def __init__(self):
        global launchTime
        Tk.__init__(self)
        self.InitInterface()
        if launchTime==0:
            launchTime+=1
            self.InitLastLoad
        else:
            try:
                self.Load(lastLoad)
            except AttributeError:
                pass
            except NameError:
                pass
            launchTime+=1
        self.mainloop()
    def InitLastLoad(self):
        global lastLoad
        lastLoad=""
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
        self.geometry("960x610+10+10")
        self.title("Map Creator")
        self.resizable(width=False, height=False)
        self.LoadTextures()
        self.InitMatrice()
        self.InitMainGui()
    def LoadTextures(self):
        self.TextureList=[]
        self.base_texture_list = []
        self.TextureEncode=[]
        for i in encodeList:
            if i!="00":
                try:
                    
                    image = Image.open("ressources/textures/map/{}".format(textureList[i]))
                    self.base_texture_list.append(ImageTk.PhotoImage(image))
                    tk_image = ImageTk.PhotoImage(image.resize((17, 17)))
                    self.TextureList.append(tk_image)
                    self.TextureEncode.append(i)
                except TclError:
                    def temp():
                        try:
                            sleep(.5); self.txtVar.set("Des textures sont manquantes ou ';' manquant"); sleep(5); self.txtVar.set("")
                        except RuntimeError: pass
                    threading.Thread(target=temp).start()
            else:
                pass
    def TexturePalet(self):
        nbre=14
        for i in range(len(self.base_texture_list)):
            can=Canvas(self.TextureFrame, width=25, height=25, bg="black", highlightthickness=0)
            can.place(x=(i%nbre)*30+10, y=((i//nbre)*30)+10)
            can.bind("<Button-1>", lambda arg1=None, arg2=i:self.onClickPalet(arg1, arg2))
            can.create_image(0,0, image = self.base_texture_list[i], anchor=NW)
        self.PreviewScreen=Canvas(self.TextureFrame, width=100, height=100, bg="red", highlightthickness=0)
        self.PreviewScreen.place(x=25, y=400)
        self.nameTxt=StringVar()
        Label(self.TextureFrame, textvariable=self.nameTxt, bg="black", fg="white").place(x=25, y=379)
    def InitMainGui(self):
        self.MainFrame = Frame(self, bg="purple", width=510, height=510)
        self.MainFrame.place(x=0, y=0)
        self.MainCan = Canvas(self.MainFrame, highlightthickness=0, width=510, height=510, bg="grey")
        self.MainCan.place(x=0, y=0)
        self.TextureFrame = Frame(self, bg="black", width=450, height=525)
        self.TextureFrame.place(x=510, y=0)
        self.OptFrame = Frame(self, bg="green", width=960, height=100)
        self.OptFrame.place(x=0, y=510)
        self.InitOptScreen()
        self.TexturePalet()
        self.MainCan.bind("<Button-1>", self.onClickPlacing)
        self.bind("<space>", self.onClickPlacing)
    def InitOptScreen(self):
        parent=self.OptFrame
        self.SelectVar=StringVar()
        self.SelectVar.set("Select Zone (disable)")
        Button(parent, command=self.Select, textvariable=self.SelectVar).place(x=10, y=10)
        Label(self.OptFrame, text="Nom du fichier (Pour chargement ou sauvegarde), sans l'extension (ex: \"exempleMap1\")").place(x=10, y=40)
        self.FileName=StringVar()
        self.FileName.set("")
        Entry(self.OptFrame, textvariable=self.FileName).place(x=10, y=70)
        Button(self.OptFrame, text="Save", command=self.Save).place(x=150, y=10)
        Button(self.OptFrame, text="Reload", command=self.Reload).place(x=200, y=10)
        Button(self.OptFrame, text="Load", command=self.Load).place(x=250, y=10)
        Button(self.OptFrame, text="View map", command=self.StartView).place(x=300, y=10)
        police=Font(family="Helveltica", underline=1, size=18)
        self.txtVar=StringVar()
        Label(self.OptFrame, textvariable=self.txtVar, font=police, fg="red", bg="green").place(x=150, y=65)
    def StartView(self):
        temp=Viewer()
        temp.Start()
    def onClickPalet(self, evt, arg):
        self.actualTxtr=self.TextureList[int(arg)]
        self.actualKey=int(arg)
        photo = Image.open("ressources/textures/map/"+textureList[self.TextureEncode[self.actualKey]])
        resolution = (100,100)
        self.imgPreview = ImageTk.PhotoImage(photo.resize(resolution))
        self.PreviewScreen.create_image(0, 0, image=self.imgPreview, anchor=NW)
        self.nameTxt.set(txtrnameList[arg])
    def onClickPlacing(self, evt):
        if evt.x<=750 and evt.y<=750:
            try:
                encodage=self.TextureEncode[self.actualKey]
                if self.select==True:
                    
                    if self.click[0]==2:
                        if self.click[1]<=evt.x:
                            if self.click[2]<=evt.y:
                                for i in range(self.click[2]//17, evt.y//17+1):
                                    for j in range(self.click[1]//17, evt.x//17+1):
                                        self.ItemMatrice[j][i]=self.MainCan.create_image(j*17, i*17, image = self.actualTxtr, anchor=NW)
                                        self.Matrice[i][j]=encodage
                            else:
                                for i in range(evt.y//17, self.click[2]//17+1):
                                    for j in range(self.click[1]//17, evt.x//17+1):
                                        self.ItemMatrice[j][i]=self.MainCan.create_image(j*17, i*17, image = self.actualTxtr, anchor=NW)
                                        self.Matrice[i][j]=encodage
                        elif self.click[2]<=evt.y:
                            for i in range(self.click[2]//17, evt.y//17+1):
                                for j in range(evt.x//17, self.click[1]//17+1):
                                    self.ItemMatrice[j][i]=self.MainCan.create_image(j*17, i*17, image = self.actualTxtr, anchor=NW)
                                    self.Matrice[i][j]=encodage
                        else:
                            for i in range(evt.y//17, self.click[2]//17+1):
                                for j in range(evt.x//17, self.click[1]//17+1):
                                    self.ItemMatrice[j][i]=self.MainCan.create_image(j*17, i*17, image = self.actualTxtr, anchor=NW)
                                    self.Matrice[i][j]=encodage
                        self.click[0]=1
                        self.LoadMatrice(self.Matrice)
                    else:
                        self.click[0]+=1
                        self.click[1] = evt.x
                        self.click[2] = evt.y
                else:
                    #Do change here 540
                    """
                    self.actualTxtr = ImageTk
                    print(self.actualTxtr)
                    photo = self.actualTxtr
                    resolution = (17, 17)
                    self.actualTxtr_resize = ImageTk.PhotoImage(photo.resize(resolution))
                    self.ItemMatrice[evt.y//17][evt.x//17]=self.MainCan.create_image(evt.x//17*17, evt.y//17*17, image = self.actualTxtr, anchor=NW)
                    self.Matrice[evt.y//17][evt.x//17]=encodage
                    """
                    self.ItemMatrice[evt.y//17][evt.x//17]=self.MainCan.create_image(evt.x//17*17, evt.y//17*17, image = self.actualTxtr, anchor=NW)
                    self.Matrice[evt.y//17][evt.x//17]=encodage
            except AttributeError:
                pass
    def Select(self):
        try:
            if self.select==True:
                self.select=False
                self.click=[1, 0, 0]
                self.SelectVar.set("Select Zone (disable)")
            else:
                self.select=True
                self.click=[1, 0, 0]
                self.SelectVar.set("Select Zone (enable)")
        except:
            self.select=True
            self.click=[1, 0, 0]
    def Save(self):
        if self.FileName.get()!="":
            final=""
            for i in range(len(self.Matrice)):
                for j in range(len(self.Matrice[i])):
                    final+=self.Matrice[i][j]
                final+="\n"
            file=open("ressources/maps/{}.map".format(self.FileName.get()), "w")
            file.write(final)
            file.close()
        else:
            pass
    def Load(self, fileName=""):
        global lastLoad
        try:
            if fileName=="":
                lastLoad=self.FileName.get()
                file=open("ressources/maps/{}.map".format(self.FileName.get()), "r")
            else:
                file=open("ressources/maps/{}.map".format(fileName), "r")
                lastLoad=fileName
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
        except FileNotFoundError:
            threading.Thread(target=self.AfficheMessage).start()
    def AfficheMessage(self):
        try:
            self.txtVar.set("File Not Found")
            sleep(4)
            self.txtVar.set("")
        except RuntimeError:
            pass
    def LoadMatrice(self, matrice):
        self.MainCan.destroy()
        self.MainCan = Canvas(self.MainFrame, highlightthickness=0, width=750, height=750)
        self.MainCan.place(x=0, y=0)
        self.MainCan.bind("<Button-1>", self.onClickPlacing)
        self.PlaceElements(matrice)
    def PlaceElements(self, matrice):
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                if matrice[i][j]!="00":
                    indice=self.TextureEncode.index(matrice[i][j])
                    self.MainCan.create_image(j*17, i*17, image=self.TextureList[indice], anchor=NW)
    def Reload(self):
        self.destroy()
        Load()



class Viewer():
    def Start(self):
        self.LoadTextures()
        threading.Thread(target=self.CreateMap).start()
    def LoadTextures(self):
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
        for key in self.textureList.keys():
            if key!="00":
                self.textureList[key]=Image.open("ressources/textures/map/{}".format(self.textureList[key]))
                self.textureList[key]=self.textureList[key].resize((4, 4))

    def CreateMap(self):
        self.result=Image.new("RGB", (600, 600))
        for y in range(20):
            for x in range(20):
                try:
                    file=open("ressources/maps/earth_{}_{}.map".format(x, y), "r")
                    content=file.read()
                    file.close()
                    img = self.CreateMapPicture(content)
                    self.result.paste(im=img, box=(x*30, 570-(y*30)))
                except FileNotFoundError:
                    pass
                except AttributeError:
                    pass
                except ValueError:
                    pass

        self.result.save("image.png")
        self.result.show()
    def CreateMapPicture(self, content):
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
        #Image a retourner
        result=Image.new("RGB", (30, 30))
        for i in range(len(self.Matrice)):
            for j in range(len(self.Matrice[i])):
                if self.Matrice[i][j]!="00" and self.Matrice[i][j]!=[]:
                    image = self.textureList[self.Matrice[i][j]]
                    #image=image.resize((4, 4))
                    result.paste(im=image, box=(j, i))
                    #print(str(i), str(j))
        #result.show()
        return result




Init()
Load()
