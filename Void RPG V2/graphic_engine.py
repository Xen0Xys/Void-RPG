from physical_engine.physical_engine import PhysicalEngine
from chuncks.chunck_loader import ChunckLoader
from views.main_menu_view import MainMenuView
from views.game_view import GameView
from character.player import Player
from tkinter import *
import PIL.ImageTk
import PIL.Image
import threading
import time
import json
import os


class GraphicEngine(Tk):
    def __init__(self, _graphic_engine_options=None):
        #Initialize game engine
        super().__init__()
        self.graphic_engine_on = True
        self.save_number = 0
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
        try:
            while self.chunck_loader.is_map_generating == True:
                time.sleep(.1)
        except AttributeError:
            pass
        self.graphic_engine_on = False
        try:
            self.game_view.player.player_move_loop.join(1)
        except AttributeError:
            pass

        #Save game
        if not os.path.exists("saves"):
            os.mkdir("saves")
        with open("saves/{}".format(str(self.save_number)), "w") as f:
            f.write(self.createDataToSave())
        

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
            options["x_window_size"] = 600
            options["y_window_size"] = 600
            options["progressive_map_generation"] = False
            options["texture_size"] = 25
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
        size = self.options["texture_size"]
        for category in json_content.keys():
            textures[category] = {}
            pil_textures[category] = {}
            for content in json_content[category].keys():
                if json_content[category][content] != "NONE":
                    try:
                        textures[category][content] = PhotoImage(file="ressources/textures/{}/{}".format(category, json_content[category][content]))
                        pil_textures[category][content] = PIL.Image.open("ressources/textures/{}/{}".format(category, json_content[category][content])).resize((size, size))
                    except TclError as e:
                        print(e)
        return textures, pil_textures
    def loadMap(self, options):
        x, y = options["player_x"], options["player_y"]
        self.screen_size = (self.options["x_window_size"], self.options["y_window_size"])
        self.map_x = self.screen_size[0] * (-1.5) - x % self.screen_size[0]
        self.map_y = self.screen_size[1] * (-1.5) - y % self.screen_size[1]
        coef_x = x // self.screen_size[0] * self.screen_size[0]
        coef_y = y // self.screen_size[1] * self.screen_size[1]
        self.chunck_loader = ChunckLoader(x, y, self, self.pil_textures, self.matrix, (coef_x, coef_y))
        self.map = self.chunck_loader.loadMapFromCenter(x, y)
        self.player = Player(self.map_x, self.map_y, self.map, self, self, self.textures["fight_ui"])
        threading.Thread(target=self.chunck_loader.startCheckLoop, args=(self.player, )).start()
        self.physical_engine = PhysicalEngine(self.chunck_loader, self)
        self.physical_engine.start()
        self.displayMap()
    def displayMap(self):
        #Display map on screen
        try:
            self.game_view = GameView(self, self.options, self.player, self.textures, self.pil_textures, self.map)
            self.game_view.start()
        except AttributeError:
            return 1
    def createDataToSave(self):
        data_dict = {}
        data_dict["x_player_coord"] = self.player.x
        data_dict["y_player_coord"] = self.player.y
        return json.dumps(data_dict)