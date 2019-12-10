from views.main_menu_view import MainMenuView
from views.loading_view import LoadingView
from views.game_view import GameView
from tkinter.font import Font
from tkinter import *
import PIL.ImageTk
import PIL.Image
import json
import os

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
        MainMenuView(self, self.textures["ui"], self.options["x_window_size"], self.options["y_window_size"])
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
    def loadAllMap(self):
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
        pil_map.save("cache/temp.png")
        self.map = PhotoImage(file="cache/temp.png")
        self.displayMap()
    def loadAroundPlayer(self):
        #Load map all around player
        pass
    def displayMap(self):
        #Display map on screen
        GameView(self, self.options, None, self.textures, self.pil_textures, self.map)