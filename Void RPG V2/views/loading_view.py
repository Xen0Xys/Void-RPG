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
        police = Font(family="Oldania ADF Std", size=20)
        Label(self.parent, text = "Loading...", anchor=W, font=police).place(x=self.size_x / 2 - self.size_x / 20, y=self.size_y / 2)