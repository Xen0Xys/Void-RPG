import threading
import time

class Collider():
    def __init__(self):
        pass
    def isCoordInCollider(self, coord):
        pass
        #...
    def isThereCollision(self, collider):
        if not isinstance(collider, Collider):
            return "Error"
        #...

class PhysicalEngine(threading.Thread):
    def __init__(self, _chunck_loader, _graphic_engine):
        threading.Thread.__init__(self)
        self.graphic_engine = _graphic_engine
        self.chunck_loader = _chunck_loader
        self.global_matrix = self.chunck_loader.matrix
        self.texture_size = self.chunck_loader.texture_size
        self.size = (self.graphic_engine.options["x_window_size"], self.graphic_engine.options["y_window_size"])
    def loadChunckCollisions(self, chunck):
        chunck_matrix = chunck.matrix
        start_x = chunck.real_chunck_coords[0] // self.texture_size
        start_y = chunck.real_chunck_coords[1] // self.texture_size
        size_x = self.size[0]
        size_y = self.size[1]
        for y_collision in range(start_y, start_y + size_y):
            for x_collision in range(start_x, start_x + size_x):
                pass
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