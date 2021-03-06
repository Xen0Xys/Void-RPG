from views.loading_view import LoadingView
from tkinter.font import Font
from tkinter import *
import threading
import json
import os

class MainMenuView():
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
        self.createCustomLabel(3, 560, "Coding : Czekaj Tom, Duchêne Guillaume\nGraphics : Duchêne Guillaume, Choin Anatole", police)
        #Label(self.MainCan, text="Coding : Czekaj Tom, Duchêne Guillaume\nGraphics : Duchêne Guillaume, Choin Anatole", bg="#9a9a9a", justify="left", font=police).place(x=3,y=585)
        self.createCustomCanvas(600, 75, 0, 50, self.ui_textures_list["baniere"], "", self.onClick)
        self.createCustomCanvas(50, 50, 470, 535, self.ui_textures_list["option_wheel"], "option", self.onClick)
        self.createCustomCanvas(50, 50, 535, 535, self.ui_textures_list["quit_button"], "quit", self.onClick)
        if os.path.exists("saves/save_1.json"):
            self.createCustomCanvas(220, 75, 30, 200, self.ui_textures_list["one_image"], "load_1", self.onClick)
        else:
            self.createCustomCanvas(220, 75, 30, 200, self.ui_textures_list["create"], "play_1", self.onClick)
        if os.path.exists("saves/save_2.json"):
            pass
        else:
            self.createCustomCanvas(220, 75, 30, 300, self.ui_textures_list["create"], "play_2", self.onClick)
        if os.path.exists("saves/save_3.json"):
            pass
        else:
            self.createCustomCanvas(220, 75, 30, 400, self.ui_textures_list["create"], "play_3", self.onClick)
    def createCustomCanvas(self, canwidth, canheight, x, y, image, arg, funct):
        modulate_x = x + (self.size_x - 600) / 4
        modulate_y = y + (self.size_y - 600) / 4
        self.CanList.append(Canvas(self.MainCan, width=canwidth, height=canheight, bg="#9a9a9a", highlightthickness=0))
        self.CanList[len(self.CanList)-1].place(x=modulate_x, y=modulate_y)
        self.CanList[len(self.CanList)-1].create_image(0,0, image=image, anchor=NW)
        self.CanList[len(self.CanList)-1].bind("<Button-1>", lambda arg1=None, arg2=arg:funct(arg1, arg2))
    def createCustomLabel(self, x, y, text, police):
        modulate_x = x + (self.size_x - 600) / 4
        modulate_y = y + (self.size_y - 600) / 4
        Label(self.MainCan, text=text, bg="#9a9a9a", justify="left", font=police).place(x=modulate_x,y=modulate_y)
    def loadSave(self, save_number):
        with open("saves/save_{}.json".format(str(save_number)), "r") as file:
            ct = json.loads(file.read())
        return ct
    def onClick(self, evt, arg):
        DEFAULT_X = 10
        DEFAULT_Y = 10
        if arg=="quit":
            self.parent.onWindowClosing()
        #Creating game
        elif arg=="play_1":
            self.parent.save_number = 1
            options = {}
            #Temp
            options["player_x"] = DEFAULT_X
            options["player_y"] = DEFAULT_Y
            #
            LoadingView(self.parent, self.parent.options["x_window_size"], self.parent.options["y_window_size"])
            threading.Thread(target=self.parent.loadMap, args=(options, )).start()
        elif arg=="play_2":
            self.parent.save_number = 2
            options = {}
            #Temp
            options["player_x"] = DEFAULT_X
            options["player_y"] = DEFAULT_Y
            #
            LoadingView(self.parent, self.parent.options["x_window_size"], self.parent.options["y_window_size"])
            threading.Thread(target=self.parent.loadMap, args=(options, )).start()
        elif arg=="play_3":
            self.parent.save_number = 3
            options = {}
            #Temp
            options["player_x"] = DEFAULT_X
            options["player_y"] = DEFAULT_Y
            #
            LoadingView(self.parent, self.parent.options["x_window_size"], self.parent.options["y_window_size"])
            threading.Thread(target=self.parent.loadMap, args=(options, )).start()
        #Loading
        elif arg=="load_1":
            self.parent.save_number = 1
            options = self.loadSave(1)
            LoadingView(self.parent, self.parent.options["x_window_size"], self.parent.options["y_window_size"])
            threading.Thread(target=self.parent.loadMap, args=(options, )).start()
        elif arg=="load_2":
            self.parent.save_number = 2
            options = self.loadSave(2)
            LoadingView(self.parent, self.parent.options["x_window_size"], self.parent.options["y_window_size"])
            threading.Thread(target=self.parent.loadMap, args=(options, )).start()
        elif arg=="load_3":
            self.parent.save_number = 3
            options = self.loadSave(3)
            LoadingView(self.parent, self.parent.options["x_window_size"], self.parent.options["y_window_size"])
            threading.Thread(target=self.parent.loadMap, args=(options, )).start()