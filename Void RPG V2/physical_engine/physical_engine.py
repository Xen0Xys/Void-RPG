import threading
import time
import json

class Point():
    def __init__(self, x, y):
        self.x, self.y = x, y
    def getPoint(self):
        return (self.x, self.y)
    def adjustPoint(self, x_adjust, y_adjust):
        self.x = self.x + x_adjust
        self.y = self.y + y_adjust
        return 0

class Collider():
    def __init__(self, args):
        try:
            NW = Point(args[0][0], args[0][1])
            NE = Point(args[1][0], args[1][1])
            SW = Point(args[2][0], args[2][1])
            SE = Point(args[3][0], args[3][1])
            self.corner_dict = {"NW" : NW,
                                "NE" : NE,
                                "SW" : SW,
                                "SE" : SE}
        except TypeError:
            self.corner_dict = None
        except IndexError:
            self.corner_dict = None
        
    def isCoordInCollider(self, coord):
        pass
        #...
    def isThereCollision(self, collider):
        if not isinstance(collider, Collider):
            return 1
        #...
    def adjustColliderCoords(self, x_adjust, y_adjust):
        for key in self.corner_dict.keys():
            self.corner_dict[key].adjustPoint(x_adjust, y_adjust)
        return self

class CornerManager():
    def __init__(self):
        CORNERFILE = "ressources/configuration/corners.json"
        self.textures_corner_dict = self.loadTexturesCorners(CORNERFILE)
    def loadTexturesCorners(self, file):
        with open(file, "r") as file:
            ct = json.loads(file.read())
        return ct
    def getDefaultCollider(self):
        pass
    def getCornerArgs(self, texture_index):
        try:
            return self.textures_corner_dict[texture_index]
        except KeyError:
            return 1

class PhysicalEngine(threading.Thread):
    def __init__(self, _chunck_loader, _graphic_engine):
        threading.Thread.__init__(self)
        self.corner_manager = CornerManager()
        self.graphic_engine = _graphic_engine
        self.chunck_loader = _chunck_loader
        self.global_matrix = self.chunck_loader.matrix
        self.texture_size = self.chunck_loader.texture_size
        self.size = (self.graphic_engine.options["x_window_size"], self.graphic_engine.options["y_window_size"])
    def loadChunckCollisions(self, chunck):
        chunck_matrix = chunck.matrix
        start_x = chunck.real_chunck_coords[0] // self.texture_size
        start_y = chunck.real_chunck_coords[1] // self.texture_size
        size_x = self.size[0] // self.texture_size
        size_y = self.size[1] // self.texture_size
        collision_list = []
        for y_collision in range(start_y, start_y + size_y):
            temp = []
            for x_collision in range(start_x, start_x + size_x):
                coord_x = x_collision * self.texture_size
                coord_y = y_collision * self.texture_size
                index_x = x_collision - start_x
                index_y = y_collision - start_y
                material = chunck_matrix[index_y][index_x]
                #print(material)
                ##Do loading here
                args = self.corner_manager.getCornerArgs(material)
                if args != 1:
                    temp.append(Collider(args))
            collision_list.append(temp)
        chunck.collision_list = [0]
    def listChunckWhoNeedLoadingCollisions(self):
        chunck_list = self.chunck_loader.chunck_list
        need_list = []
        for chunck_y in chunck_list:
            for chunck_x in chunck_y:
                if chunck_x.collision_list == []:
                    need_list.append(chunck_x)
        return need_list
    def run(self):
        while self.graphic_engine.graphic_engine_on:
            time.sleep(1/10)
            need_list = self.listChunckWhoNeedLoadingCollisions()
            for chunck in need_list:
                self.loadChunckCollisions(chunck)