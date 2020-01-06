from tkinter import *
import threading
import time

class GameView():
    """Display game view"""
    def __init__(self, _parent, _graphic_engine_options, _player, _textures_list, _pil_textures_list,  _map_picture):
        #Map setup
        self.parent = _parent
        self.graphic_engine_options = _graphic_engine_options
        self.map_picture = _map_picture
        self.screen_size = (_graphic_engine_options["x_window_size"], _graphic_engine_options["y_window_size"])
        self.map_x, self.map_y = self.screen_size[0] * (-2), self.screen_size[1] * (-2)
        print(self.map_x, self.map_y)
        self.resetUI()
        self.setupElements()
        #Player setup
        self.player = _player
    def start(self):
        self.player.start()
    def resetUI(self):
        for i in self.parent.winfo_children():
            i.destroy()
    def setupElements(self):
        self.wallpaper_canvas = Canvas(self.parent, width=self.graphic_engine_options["x_window_size"], height=self.graphic_engine_options["y_window_size"], bg="#9a9a9a", highlightthickness=0)
        self.wallpaper_canvas.place(x=0, y=0)
        self.picture = self.wallpaper_canvas.create_image(0, 0, image=self.map_picture, anchor=NW)
        #threading.Thread(target=self.moveLoop, args=(-3000, -8000, )).start()
    def moveLoop(self, x, y):
        for i in range(5000):
            time.sleep(.01)
            self.wallpaper_canvas.coords(self.picture, x + i, y + i / 2)
    def getCanvas(self):
        print("here")
        return self.wallpaper_canvas
    def loadMapGestionnary(self):
        while self.parent.graphic_engine_on == True:
            pass