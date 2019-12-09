"""
MIT License

Copyright (c) [2019] [CZEKAJ Tom aka Xen0Xys, DUCHENE Guillaume aka Gunmar]

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import PIL.Image
import PIL.ImageTk
from tkinter.font import Font
from tkinter import *
import threading
import json
import os

class EventListner():
    def __init__(self):
        pass

class MenuMain():
    def __init__(self, _parent, _ui_textures_list, _size_x, _size_y):
        self.parent = _parent
        self.ui_textures_list = _ui_textures_list
        self.size_x = _size_x
        self.size_y = _size_y
        self.initUI()
    def resetUI(self):
        for i in self.parent.winfo_children():
            i.destroy()
    def initUI(self):
        self.resetUI()
        self.parent.title("Void - RPG")
        self.setUI()
        self.setButtons()
    def setUI(self):
        self.MainCan = Canvas(self.parent, width=self.size_x, height=self.size_y, bg="#9a9a9a", highlightthickness=0)
        self.MainCan.pack()
    def setButtons(self):
        self.CanList=[]
        police = Font(family="Oldania ADF Std", size=10)
        Label(self.MainCan, text="Coding : Czekaj Tom, Duchêne Guillaume\nGraphics : Duchêne Guillaume, Choin Anatole", bg="#9a9a9a", justify="left", font=police).place(x=3,y=585)
        self.createCustomCanvas(600, 75, 12.5, 50, self.ui_textures_list["baniere"], "", self.onClick)
        self.createCustomCanvas(50, 50, 495, 560, self.ui_textures_list["option_wheel"], "option", self.onClick)
        self.createCustomCanvas(50, 50, 560, 560, self.ui_textures_list["quit_button"], "quit", self.onClick)
        self.createCustomCanvas(220, 75, 30, 200, self.ui_textures_list["create"], "playOne", self.onClick)
        self.createCustomCanvas(220, 75, 30, 300, self.ui_textures_list["create"], "playTwo", self.onClick)
        self.createCustomCanvas(220, 75, 30, 400, self.ui_textures_list["create"], "playThree", self.onClick)
    def createCustomCanvas(self, canwidth, canheight, x, y, image, arg, funct):
        self.CanList.append(Canvas(self.MainCan, width=canwidth, height=canheight, bg="#9a9a9a", highlightthickness=0))
        self.CanList[len(self.CanList)-1].place(x=x, y=y)
        self.CanList[len(self.CanList)-1].create_image(0,0, image=image, anchor=NW)
        self.CanList[len(self.CanList)-1].bind("<Button-1>", lambda arg1=None, arg2=arg:funct(arg1, arg2))
    def onClick(self, evt, arg):
        if arg=="quit":
            self.parent.onWindowClosing()
            pass
        if arg=="playOne":
            self.parent.loadMap()

class LoadingView():
    def __init__(self, _parent):
        self.parent = _parent
        self.resetUI()
    def resetUI(self):
        for i in self.parent.winfo_children():
            i.destroy()
    def setupUI(self):
        pass


class GraphicEngine(Tk):
    def __init__(self, _graphic_engine_options=None):#Initialize game engine
        super().__init__()
        if _graphic_engine_options == None:
            self.options = self.loadGraphicEngineOptions()
        else:
            self.options = _graphic_engine_options
        self.textures, self.pil_textures = self.loadTextures()
        self.protocol("WM_DELETE_WINDOW", self.onWindowClosing)
        MenuMain(self, self.textures["ui"], self.options["x_window_size"], self.options["y_window_size"])
    def onWindowClosing(self):
        #Closing window event
        self.destroy()
    def showWindow(self):
        self.resizable(width=False, height=False)
        self.mainloop()
    def loadGraphicEngineOptions(self):
        #Load all graphic engine options
        def createOptions():
            #Generate default options
            options = {}
            #Init all options here
            options["x_window_size"] = 625
            options["y_window_size"] = 625
            options["progressive_map_generation"] = False
            with open("ressources/configuration/graphic_engine.json", "w") as file:
                file.write(json.dumps(options, indent=4))
            return options
        def loadOptions():
            #Load options from file
            with open("ressources/configuration/graphic_engine.json", "r") as file:
                json_content = json.loads(file.read())
            return json_content
        #Execute good function in good case
        if not os.path.exists("ressources/configuration/graphic_engine.json"):
            return createOptions() 
        else:
            return createOptions() #DO CHANGE HERE
    def loadTextures(self):
        #Load textures from json file and png pictures
        with open("ressources/configuration/textures.json", "r") as file:
            json_content = json.loads(file.read())
        textures = {}
        pil_textures = {}
        for category in json_content.keys():
            textures[category] = {}
            pil_textures[category] = {}
            for content in json_content[category].keys():
                if json_content[category][content] != "NONE":
                    try:
                        textures[category][content] = PhotoImage(file="ressources/textures/{}/{}".format(category, json_content[category][content]))
                        pil_textures[category][content] = PIL.Image.open("ressources/textures/{}/{}".format(category, json_content[category][content]))
                    except TclError as e:
                        print(e)
        return textures, pil_textures
    def loadMap(self):
        LoadingView(self)
        map_name = "earth"
        self.pil_map = PIL.Image.new("RGB", (15000, 15000))
        if self.options["progressive_map_generation"] == False:
            with open("ressources/maps/{}.json".format(map_name), "r") as file:
                map_matrice = json.loads(file.read())
            for y in range(len(map_matrice)):
                for x in range(len(map_matrice[y])):
                    if map_matrice[y][x] != "00":
                        self.pil_map.paste(im=self.pil_textures["map"][map_matrice[y][x]], box=(x * 25, y * 25))
        self.map = PIL.ImageTk.PhotoImage(self.pil_map)
        self.displayMap()
    def loadAroundPlayer(self):
        pass
    def displayMap(self):
        print("display_map")


class GameEngine():
    def __init__(self):
        self.startGameEngines()
    def startGameEngines(self):
        self.graphic_engine = GraphicEngine()
        self.graphic_engine.showWindow()

if __name__ == "__main__":
    engine = GameEngine()