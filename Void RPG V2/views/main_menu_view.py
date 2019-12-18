from views.loading_view import LoadingView
from tkinter.font import Font
from tkinter import *
import threading
import time

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
            #threading.Thread(target=LoadingView, args=(self.parent, self.parent.options["x_window_size"], self.parent.options["y_window_size"], )).start()
            LoadingView(self.parent, self.parent.options["x_window_size"], self.parent.options["y_window_size"])
            #self.parent.loadMapAroundPlayer(1250, 1250)
            threading.Thread(target=self.parent.loadMapAroundPlayer, args=(1250, 1250, )).start()