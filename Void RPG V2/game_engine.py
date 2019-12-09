from tkinter import *

class GraphicEngine(Tk):
    def __init__(self, _option_list = None):
        super().__init__()
        if _option_list == None:
            self.options = self.loadGraphicEngineOptions()
        else:
            self.options = _option_list
    def loadGraphicEngineOptions(self):
        return {}
        

class GameEngine():
    def __init__(self):
        pass
    def startGameEngines(self):
        self.graphic_engine = GraphicEngine()


if __name__ == "__main__":
    engine = GameEngine()