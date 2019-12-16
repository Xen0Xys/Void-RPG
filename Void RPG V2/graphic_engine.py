from views.main_menu_view import MainMenuView
from views.loading_view import LoadingView
from views.game_view import GameView
from tkinter.font import Font
from tkinter import *
import PIL.ImageTk
import PIL.Image
import json
import os

"""
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
        pil_map.save("cache/temp.png") #To much RAM (1.7Go)
        self.map = PhotoImage(file="cache/temp.png")#To much RAM (1.7Go)
        self.displayMap()
    def createPILPicture(self, _matrice):
        pil_map = PIL.Image.new("RGB", ((len(_matrice[0]) * 25), (len(_matrice) * 25)))
        for y in range(len(_matrice)):
            for x in range(len(_matrice[y])):
                if _matrice[y][x] != "00":
                    pil_map.paste(im=self.pil_textures["map"][_matrice[y][x]], box=(x * 25, y * 25))
        return pil_map
    def loadAroundPlayer(self, _player_x, _player_y):
        #Load map all around player
        LoadingView(self, self.options["x_window_size"], self.options["y_window_size"])
        map_name = "earth"
        with open("ressources/maps/{}.json".format(map_name), "r") as file:
            map_matrice = json.loads(file.read())
        matrice = []
        coords_00_x = int(_player_x - self.options["x_window_size"] / 2)
        coords_00_y = int(_player_y - self.options["y_window_size"] / 2)
        for y in range(int(len(map_matrice) / 25 + 1)):
            temp = []
            for x in range(int(len(map_matrice[y]) / 25 + 1)):
                temp.append(map_matrice[y + coords_00_y][x + coords_00_x])
            matrice.append(temp)
        self.map = PIL.ImageTk.PhotoImage(self.createPILPicture(matrice))
        self.displayMap()
"""

class Chunck():
    def __init__(self, _size, _canvas_coords, _matrix, _chunck_coords):
        self.map = None
        self.matrix = _matrix
        self.size = _size
        self.real_coords = _canvas_coords
        self.chunck_coords = _chunck_coords
        self.chunck_loaded = False
    def generateChunck(self, _pil_textures_list, force=False):
        if (self.chunck_loaded == False) or (force == True):
            pil_map = PIL.Image.new("RGB", ((len(self.matrix[0]) * 25), (len(self.matrix) * 25)))
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    if self.matrix[y][x] != "00":
                        pil_map.paste(im=_pil_textures_list["map"][self.matrix[y][x]], box=(x * 25, y * 25))
            self.map = PIL.ImageTk.PhotoImage(pil_map)
            return self.map
        return self.map
    

class GraphicEngine(Tk):
    def __init__(self, _graphic_engine_options=None):
        #Initialize game engine
        super().__init__()
        if _graphic_engine_options == None:
            self.options = self.loadGraphicEngineOptions()
        else:
            self.options = _graphic_engine_options
        self.textures, self.pil_textures = self.loadTextures()
        self.matrix = self.loadMatrix()
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
            return loadOptions() #DO CHANGE HERE
    def loadMatrix(self):
        map_name = "earth"
        with open("ressources/maps/{}.json".format(map_name), "r") as file:
            matrix = json.loads(file.read())
        return matrix
    def saveGraphicEngineConfiguration(self):
        with open("ressources/configuration/graphic_engine.json", "w") as file:
            file.write(json.dumps(self.options, indent=4))
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
    def getMatrixChunck(self, _coords, _size, _global_matrix):
        matrix = []
        x_matrix_coord = int(_coords[0] / 25)
        y_matrix_coord = int(_coords[1] / 25)
        for y in range(_size[1]):
            temp = []
            for x in range(_size[0]):
                temp.append(_global_matrix[y + y_matrix_coord][x + x_matrix_coord])
            matrix.append(temp)
        return matrix
    def loadMapAroundPlayer(self, _center_x, _center_y):
        size = (self.options["x_window_size"], self.options["y_window_size"])
        map_00_x = int(_center_x - self.options["x_window_size"] / 2) - 2 * self.options["x_window_size"]
        map_00_y = int(_center_y - self.options["y_window_size"] / 2) - 2 * self.options["y_window_size"]
        for y_map in range(5):
            temp = []
            for x_map in range(5):
                temp.append(Chunck(size, (x_map * map_00_x, y_map * map_00_y), self.getMatrixChunck((map_00_x, map_00_y), size, self.matrix), (map_00_x, map_00_y)))
    def assembleMap(self, _chunck_list):
        size = (self.options["x_window_size"], self.options["y_window_size"])
        pil_map = PIL.Image.new("RGB", (size[0] * 5, size[1] * 5))
        for y in range(5):
            for x in range(5):
                _chunck_list[y][x].generateChunck()
                pil_map.paste(im=None, box=(x * size[0], y * size[1]))
    def displayMap(self):
        #Display map on screen
        GameView(self, self.options, None, self.textures, self.pil_textures, self.map)