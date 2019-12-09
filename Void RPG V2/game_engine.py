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
import time
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
            threading.Thread(target=self.parent.loadMap).start()

class LoadingView():
    """Display loading view"""
    def __init__(self, _parent, _size_x, _size_y):
        self.parent = _parent
        self.size_x = _size_x
        self.size_y = _size_y
        self.resetUI()
        self.setupUI()
    def resetUI(self):
        for i in self.parent.winfo_children():
            i.destroy()
    def setupUI(self):
        police = Font(family="Oldania ADF Std", size=20)
        Label(self.parent, text = "Loading...", anchor=W, font=police).place(x=self.size_x / 2 - self.size_x / 20, y=self.size_y / 2)

class GameView():
    """Display game view"""
    def __init__(self, _parent, _graphic_engine_options, _player_information, _textures_list, _pil_textures_list,  _map_picture):
        self.parent = _parent
        self.graphic_engine_options = _graphic_engine_options
        self.map_picture = _map_picture
        self.resetUI()
        self.setupElements()
    def resetUI(self):
        for i in self.parent.winfo_children():
            i.destroy()
    def setupElements(self):
        self.wallpaper_canvas = Canvas(self.parent, width=self.graphic_engine_options["x_window_size"], height=self.graphic_engine_options["y_window_size"], bg="#9a9a9a", highlightthickness=0)
        self.wallpaper_canvas.place(x=0, y=0)
        self.picture = self.wallpaper_canvas.create_image(-3000, -8000, image=self.map_picture, anchor=NW)
        #threading.Thread(target=self.moveLoop, args=(-3000, -8000, )).start()
    def moveLoop(self, x, y):
        for i in range(500000):
            time.sleep(.01)
            self.wallpaper_canvas.coords(self.picture, x + i, y + i / 2)

class GraphicEngine(Tk):
    def __init__(self, _graphic_engine_options=None):
        #Initialize game engine
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
        self.geometry("{}x{}".format(self.options["x_window_size"], self.options["y_window_size"]))
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
        #Load map PIL picture
        LoadingView(self, self.options["x_window_size"], self.options["y_window_size"])
        map_name = "earth"
        pil_map = PIL.Image.new("RGB", (15000, 15000))
        if self.options["progressive_map_generation"] == False:
            with open("ressources/maps/{}.json".format(map_name), "r") as file:
                map_matrice = json.loads(file.read())
            for y in range(len(map_matrice)):
                for x in range(len(map_matrice[y])):
                    if map_matrice[y][x] != "00":
                        pil_map.paste(im=self.pil_textures["map"][map_matrice[y][x]], box=(x * 25, y * 25))
        #self.map = PIL.ImageTk.PhotoImage(pil_map)
        pil_map.save("temp.png")
        self.map = PhotoImage(file="temp.png")
        self.displayMap()
    def loadAroundPlayer(self):
        #Load map all around player
        pass
    def displayMap(self):
        #Display map on screen
        GameView(self, self.options, None, self.textures, self.pil_textures, self.map)


class GameEngine():
    def __init__(self):
        self.startGameEngines()
    def startGameEngines(self):
        self.graphic_engine = GraphicEngine()
        self.graphic_engine.showWindow()

if __name__ == "__main__":
    engine = GameEngine()