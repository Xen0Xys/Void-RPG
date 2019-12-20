from tkinter.font import Font
from tkinter import *

class LoadingView():
    """Display loading view"""
    def __init__(self, _parent, _size_x, _size_y):
        self.parent = _parent
        self.size_x = _size_x
        self.size_y = _size_y
        self.resetUI()
        self.setupUI()
        print("UI setuped")
    def resetUI(self):
        for i in self.parent.winfo_children():
            i.destroy()
    def setupUI(self):
        bg_color = "grey"
        can = Canvas(self.parent, height=self.size_y, width=self.size_x, highlightthickness=0,bg=bg_color)
        can.pack()
        police = Font(family="Oldania ADF Std", size=20)
        Label(can, text = "Loading...", anchor=W, font=police, bg=bg_color).place(x=self.size_x / 2 - self.size_x / 20, y=self.size_y / 2)