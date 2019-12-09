from tkinter import *
import os
import json
import threading
import time

class GraphicEngine(Tk):
    def __init__(self, _graphic_engine_options=None):
        super().__init__()
        if _graphic_engine_options == None:
            self.loadGraphicEngineOptions()
        else:
            self.options = _graphic_engine_options
    def showWindow(self):
        self.mainloop()
    def loadGraphicEngineOptions(self):
        def createOptions():
            options = {}
            #Init all options here
            options["x_window_size"] = 300
            options["y_window_size"] = 300
            with open("ressources/configuration/graphic_engine.json", "w") as file:
                file.write(json.dumps(options, indent=4))
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
        self.graphic_engine.showWindow()

"""
def algo():
    with open("ressources/configuration/textures.cfg", "r") as file:
        content = file.read()
    ct_spt = content.split("\n")
    next_ = []
    for line in ct_spt:
        try:
            if line[0] != "#":
                next_.append(line)
        except IndexError:
            pass
    term = []
    for line in next_:
        term.append(line[:len(line) - 1])
    dico = {}
    dico["map"] = {}
    for line in term:
        s = line.split("=")
        dico["map"][s[0]] = s[1]
    with open("ressources/configuration/textures.json", "w") as file:
        file.write(json.dumps(dico, indent=4))
"""

if __name__ == "__main__":
    engine = GameEngine()