from views.main_menu_view import MainMenuView
from views.game_view import GameView
from tkinter import *
import PIL.ImageTk
import PIL.Image
import threading
import time
import json
import os

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
    def isPlayerOnChunck(self, player_x, player_y):
        pass

class ChunckLoader():
    def __init__(self, _player_x, _player_y, _graphic_engine_options, _pil_textures, _matrix):
        self.options = _graphic_engine_options
        self.pil_textures = _pil_textures
        self.matrix = _matrix
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
    def isAllMapGenerated(self, _chunck_list):
        for chunck_y in _chunck_list:
            for chunck in chunck_y:
                if chunck.chunck_loaded == False:
                    return False
        return True
    def assembleMap(self, _chunck_list):
        #assemble map with chunck objects
        t1 = time.time()
        size = (self.options["x_window_size"], self.options["y_window_size"])
        pil_map = PIL.Image.new("RGB", (size[0] * 5, size[1] * 5))
        for y in range(5):
            for x in range(5):
                _chunck_list[y][x].generateChunck(self.pil_textures)
        while self.isAllMapGenerated(_chunck_list) == False:
            time.sleep(1 / 60)
        for y in range(5):
            for x in range(5):
                chunck = _chunck_list[y][x].getChunck(self.pil_textures)
                pil_map.paste(im=chunck, box=(x * size[0], y * size[1]))
        pil_map.save("cache/temp.png")
        try:
            return PIL.ImageTk.PhotoImage(image=pil_map)
        except RuntimeError:
            return 1
        print("End")
        print(time.time() - t1)
    def loadMapAroundPlayer(self, _center_x, _center_y):
        #Load 5 chuncks around playeroad 5 chuncks around player
        size = (self.options["x_window_size"], self.options["y_window_size"])
        #LoadingView(self, self.options["x_window_size"], self.options["y_window_size"])
        map_00_x = int(_center_x - self.options["x_window_size"] / 2) - 2 * self.options["x_window_size"]
        map_00_y = int(_center_y - self.options["y_window_size"] / 2) - 2 * self.options["y_window_size"]
        chunck_list = []
        for y_map in range(5):
            temp = []
            for x_map in range(5):
                matrix_chunck = self.getMatrixChunck((map_00_x + x_map * size[0], map_00_y + y_map * size[1]), (int(size[0] / 25), int(size[1] / 25)), self.matrix)
                temp.append(Chunck((int(size[0] / 25), int(size[1] / 25)), (x_map * map_00_x, y_map * map_00_y), matrix_chunck, (x_map, y_map)))
            chunck_list.append(temp)
        return self.assembleMap(chunck_list)
    def startLoadingLoop(self):
        pass



class GraphicEngine(Tk):
    def __init__(self, _graphic_engine_options=None):
        #Initialize game engine
        super().__init__()
        self.graphic_engine_on = True
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
        self.graphic_engine_on = False
        try:
            self.game_view.player.player_move_loop.join(1)
        except AttributeError:
            pass
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
    def loadMap(self, options):
        x, y = options["player_x"], options["player_y"]
        self.chunck_loader = ChunckLoader(x, y, self.options, self.pil_textures, self.matrix)
        map = self.chunck_loader.loadMapAroundPlayer(x, y)
        self.displayMap(map)
    def displayMap(self, map):
        #Display map on screen
        try:
            self.game_view = GameView(self, self.options, None, self.textures, self.pil_textures, map)
        except AttributeError:
            return 1