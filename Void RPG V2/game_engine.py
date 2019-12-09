from tkinter import *
import os
import json

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
            return options
        def loadOptions():
            with open("ressources/configuration/graphic_engine.json", "r") as file:
                json_content = json.loads(file.read())
            return json_content
        if os.path.exists("ressources/configuration/graphic_engine.json"):
            return createOptions()
        else:
            return loadOptions()

class GameEngine():
    def __init__(self):
        pass
    def startGameEngines(self):
        self.graphic_engine = GraphicEngine()


if __name__ == "__main__":
    engine = GameEngine()