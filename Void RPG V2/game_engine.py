from tkinter import *
import os
import json
import threading

class GraphicEngine(Tk):
    def __init__(self, _graphic_engine_options=None):
        super().__init__()
        if _graphic_engine_options == None:
            self.loadGraphicEngineOptions()
        else:
            self.options = _graphic_engine_options
    def loadGraphicEngineOptions(self):
        def createOptions():
            options = {}
            #Init all options here
            options["x_window_size"] = 300
            options["y_window_size"] = 300
            return options
        def loadOptions():
            with open("ressources/configuration/graphic_engine.json", "r") as file:
                json_content = json.loads(file.read())
            return json_content
        if not os.path.exists("ressources/configuration/graphic_engine.json"):
            return createOptions()
        else:
            return loadOptions()
    def loadingView(self):
        self.geometry("{}x{}".format(self.options["x_window_size"], self.options["y_window_size"]))

class GameEngine():
    def __init__(self):
        self.startGameEngines()
    def startGameEngines(self):
        self.graphic_engine = GraphicEngine()
        self.graphic_engine.mainloop()


if __name__ == "__main__":
    engine = GameEngine()