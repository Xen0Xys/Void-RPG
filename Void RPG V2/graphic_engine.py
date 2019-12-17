from views.main_menu_view import MainMenuView
from views.loading_view import LoadingView
from views.game_view import GameView
from tkinter.font import Font
from tkinter import *
import PIL.ImageTk
import PIL.Image
import threading
import time
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
            try:
                pil_map = PIL.Image.open("cache/earth_{}_{}.png".format(self.chunck_coords[0], self.chunck_coords[1]))
            except FileNotFoundError:
                pil_map = PIL.Image.new("RGB", ((self.size[0] * 25), (self.size[1] * 25)))
                for y in range(self.size[1]):
                    for x in range(self.size[0]):
                        if self.matrix[y][x] != "00":
                            loaded = False
                            while loaded == False:
                                try:
                                    pil_map.paste(im=_pil_textures_list["map"][self.matrix[y][x]], box=(x * 25, y * 25))
                                    loaded = True
                                except AttributeError:
                                    pass
                pil_map.save("cache/earth_{}_{}.png".format(self.chunck_coords[0], self.chunck_coords[1]))
            self.map = pil_map
            self.chunck_loaded = True
            return pil_map
        return self.map
    def getChunck(self, _pil_textures_list):
        try:
            return self.map
        except FileNotFoundError:
            return self.generateChunck(_pil_textures_list, force=True)
    

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
            return loadOptions()
    def loadMatrix(self):
        #Load matrix from json file
        map_name = "earth"
        with open("ressources/maps/{}.json".format(map_name), "r") as file:
            matrix = json.loads(file.read())
        return matrix
    def saveGraphicEngineConfiguration(self):
        #Save graphic engine configuration
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
        #Get matrix with coords and size
        matrix = []
        x_matrix_coord = int(_coords[0] / 25)
        y_matrix_coord = int(_coords[1] / 25)
        for y in range(_size[1]):
            temp = []
            for x in range(_size[0]):
                temp.append(_global_matrix[y_matrix_coord + y][x_matrix_coord + x])
            matrix.append(temp)
        return matrix
    def loadMapAroundPlayer(self, _center_x, _center_y):
        #Load 5 chuncks around player
        size = (self.options["x_window_size"], self.options["y_window_size"])
        LoadingView(self, size[0], size[1])
        map_00_x = int(_center_x - self.options["x_window_size"] / 2) - 2 * self.options["x_window_size"]
        map_00_y = int(_center_y - self.options["y_window_size"] / 2) - 2 * self.options["y_window_size"]
        chunck_list = []
        for y_map in range(5):
            temp = []
            for x_map in range(5):
                matrix_chunck = self.getMatrixChunck((map_00_x + x_map * size[0], map_00_y + y_map * size[1]), (int(size[0] / 25), int(size[1] / 25)), self.matrix)
                temp.append(Chunck((int(size[0] / 25), int(size[1] / 25)), (x_map * map_00_x, y_map * map_00_y), matrix_chunck, (x_map, y_map)))
            chunck_list.append(temp)
        self.assembleMap(chunck_list)
        self.displayMap()
    def isAllMapGenerated(self, _chunck_list):
        for y in range(len(_chunck_list)):
            for x in range(len(_chunck_list[y])):
                if _chunck_list[y][x].chunck_loaded == False:
                    return False
        return True
    def assembleMap(self, _chunck_list):
        #assemble map with chunck objects
        t1 = time.time()
        size = (self.options["x_window_size"], self.options["y_window_size"])
        pil_map = PIL.Image.new("RGB", (size[0] * 5, size[1] * 5))
        for y in range(5):
            for x in range(5):
                #threading.Thread(target=_chunck_list[y][x].generateChunck, args=(self.pil_textures, )).start()
                _chunck_list[y][x].generateChunck(self.pil_textures)
        while self.isAllMapGenerated(_chunck_list) == False:
            time.sleep(1 / 60)
        for y in range(5):
            for x in range(5):
                chunck = _chunck_list[y][x].getChunck(self.pil_textures)
                pil_map.paste(im=chunck, box=(x * size[0], y * size[1]))
        pil_map.save("cache/temp.png")
        self.map = PIL.ImageTk.PhotoImage(image=pil_map)
        print("End")
        print(time.time() - t1)
        
    def displayMap(self):
        #Display map on screen
        GameView(self, self.options, None, self.textures, self.pil_textures, self.map)