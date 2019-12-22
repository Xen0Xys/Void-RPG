"""
MIT License

Copyright (c) [2019] [CZEKAJ Tom aka Xen0Xys, DUCHENE Guillaume aka Gunmar]

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from graphic_engine import GraphicEngine
import sys
import os

class EventListner():
    def __init__(self):
        pass

class GameEngine():
    def __init__(self):
        self.startGameEngines()
    def startGameEngines(self):
        self.createCacheFolder()
        self.graphic_engine = GraphicEngine()
        self.graphic_engine.showWindow()
        self.graphic_engine.saveGraphicEngineConfiguration()
        self.clearCacheFolder()
        sys.exit(0)
    def createCacheFolder(self):
        if not os.path.exists("cache"):
            os.mkdir("cache")
    def clearCacheFolder(self):
        file_list = os.listdir("cache/")
        for file in file_list:
            ctn = True
            while ctn == True:
                try:
                    os.remove("cache/{}".format(file))
                    ctn = False
                except PermissionError:
                    pass

if __name__ == "__main__":
    engine = GameEngine()