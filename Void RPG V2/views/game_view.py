from tkinter.font import Font
from tkinter import *
import threading
import time

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
        threading.Thread(target=self.moveLoop, args=(-3000, -8000, )).start()
    def moveLoop(self, x, y):
        for i in range(500000):
            time.sleep(.01)
            self.wallpaper_canvas.coords(self.picture, x + i, y + i / 2)