from tkinter import *
import os
import json
import threading
import time

class EventListner():
    def __init__(self):
        pass


class MenuMain():
    def __init__(self, _parent, _ui_textures_list, _size_x, _size_y):
        self.parent = _parent
        self.ui_textures_list = _ui_textures_list
        self.size_x = _size_x
        self.size_y = _size_y
        self.InitGUI()
    def ResetGUI(self):
        for i in self.parent.winfo_children():
            i.destroy()
    def InitGUI(self):
        self.ResetGUI()
        self.parent.title("Void - RPG")
        self.SetGUI()
        self.SetButtons()
    def SetGUI(self):
        self.MainCan = Canvas(self.parent, width=self.size_x, height=self.size_y, bg="#9a9a9a", highlightthickness=0)
        self.MainCan.pack()
    def SetButtons(self):
        self.CanList=[]
        Label(self.MainCan, text="Coding : Czekaj Tom\nGraphics : Duchene Guillaume, Choin Anatole", bg="#9a9a9a", justify="left").place(x=1,y=712)
        self.CreateAllCan(600,75,75,50,self.ui_textures_list["baniere"], "", self.onClick)
        self.CreateAllCan(50,50,610,680,self.ui_textures_list["option_wheel"], "option", self.onClick)
        #self.CreateAllCan(220,75,30,600,self.ui_textures_list["fight"], "fight", self.onClick)
        self.CreateAllCan(50,50,680,680,self.ui_textures_list["quit_button"], "quit", self.onClick)
        self.CreateAllCan(220,75,30,300,self.ui_textures_list["create"], "playOne", self.onClick)
        self.CreateAllCan(220,75,30,400,self.ui_textures_list["create"], "playTwo", self.onClick)
        self.CreateAllCan(220,75,30,500,self.ui_textures_list["create"], "playThree", self.onClick)
    def CreateAllCan(self, canwidth, canheight, x, y, image, arg, funct):
        self.CanList.append(Canvas(self.MainCan, width=canwidth, height=canheight, bg="#9a9a9a", highlightthickness=0))
        self.CanList[len(self.CanList)-1].place(x=x, y=y)
        self.CanList[len(self.CanList)-1].create_image(0,0, image=image, anchor=NW)
        self.CanList[len(self.CanList)-1].bind("<Button-1>", lambda arg1=None, arg2=arg:funct(arg1, arg2))
    def onClick(self, evt, arg):
        if arg=="quit":
            #self.parent.onWindowClosing()
            pass
        if arg=="playOne":
            pass

class GraphicEngine(Tk):
    def __init__(self, _graphic_engine_options=None):
        super().__init__()
        if _graphic_engine_options == None:
            self.options = self.loadGraphicEngineOptions()
        else:
            self.options = _graphic_engine_options
        self.textures = self.loadTextures()
        menu = MenuMain(self, self.textures["ui"], self.options["x_window_size"], self.options["y_window_size"])
    def showWindow(self):
        self.mainloop()
    def loadGraphicEngineOptions(self):
        def createOptions():
            options = {}
            #Init all options here
            options["x_window_size"] = 300
            options["y_window_size"] = 300
            with open("ressources/configuration/graphic_engine.json", "w") as file:
                file.write(json.dumps(options, indent=4))
            return options
        def loadOptions():
            with open("ressources/configuration/graphic_engine.json", "r") as file:
                json_content = json.loads(file.read())
            return json_content
        if not os.path.exists("ressources/configuration/graphic_engine.json"):
            return createOptions()
        else:
            return loadOptions()
    def loadTextures(self):
        with open("ressources/configuration/textures.json", "r") as file:
            json_content = json.loads(file.read())
        textures = {}
        for category in json_content.keys():
            textures[category] = {}
            for content in json_content[category].keys():
                if json_content[category][content] != "NONE":
                    try:
                        textures[category][content] = PhotoImage(file="ressources/textures/{}/{}".format(category, json_content[category][content]))
                    except TclError as e:
                        print(e)
        return textures

class GameEngine():
    def __init__(self):
        self.startGameEngines()
    def startGameEngines(self):
        self.graphic_engine = GraphicEngine()
        self.graphic_engine.showWindow()

if __name__ == "__main__":
    engine = GameEngine()