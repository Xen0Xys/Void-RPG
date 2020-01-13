from chuncks.chunck import Chunck
import PIL.ImageTk
import PIL.Image
import time

class ChunckLoader():
    def __init__(self, _player_x, _player_y, _graphic_engine, _pil_textures, _matrix):
        self.options = _graphic_engine.options
        self.pil_textures = _pil_textures
        self.matrix = _matrix
        self.is_map_generating = False
        self.graphic_engine = _graphic_engine
        self.texture_size = self.graphic_engine.options["texture_size"]
    def startCheckLoop(self, _player):
        self.player = _player
        t = 0
        while self.graphic_engine.graphic_engine_on == True:
            time.sleep(1/60)
            self.x = -self.player.x + self.graphic_engine.options["x_window_size"] / 2
            self.y = -self.player.y + self.graphic_engine.options["y_window_size"] / 2
            if self.is_map_generating == False and t <= 0:
                if not self.chunck_list[2][2].isPlayerOnChunck(self.x, self.y):
                    t += 1
                    self.loadMapFromCenter(self.x, self.y)
                    self.player.setupNewMap(self.map)
    def getMatrixChunck(self, _coords, _size, _global_matrix):
        #Get matrix with coords and size
        matrix = []
        x_matrix_coord = int(_coords[0] / self.texture_size)
        y_matrix_coord = int(_coords[1] / self.texture_size)
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
            convert_map = PIL.ImageTk.PhotoImage(image=pil_map)
            return convert_map
        except RuntimeError as e:
            print(e)
            return 1
        print("End")
        print(time.time() - t1)
    def loadMapAroundPlayer(self, _center_x, _center_y):
        self.is_map_generating = True
        #Load 5 chuncks around playeroad 5 chuncks around player
        size = (self.options["x_window_size"], self.options["y_window_size"])
        #LoadingView(self, self.options["x_window_size"], self.options["y_window_size"])
        map_00_x = int(_center_x - self.options["x_window_size"] / 2) - 2 * self.options["x_window_size"]
        map_00_y = int(_center_y - self.options["y_window_size"] / 2) - 2 * self.options["y_window_size"]
        print("Map 00 is:", map_00_x)
        self.chunck_list = []
        for y_map in range(5):
            temp = []
            for x_map in range(5):
                matrix_chunck = self.getMatrixChunck((x_map * size[0], y_map * size[1]), (int(size[0] / self.texture_size), int(size[1] / self.texture_size)), self.matrix)
                temp.append(Chunck((int(size[0] / self.texture_size), int(size[1] / self.texture_size)), (x_map * map_00_x, y_map * map_00_y), matrix_chunck, (x_map, y_map), self.texture_size))
            self.chunck_list.append(temp)
        self.map = self.assembleMap(self.chunck_list)
        self.is_map_generating = False
        return self.map
    def loadMapFromCenter(self, _player_x, _player_y):
        self.is_map_generating = True
        size = (self.options["x_window_size"], self.options["y_window_size"])
        #Ici appeler le chunck sur lequel est le joueur pour avoir son centre
        center_x = _player_x
        center_y = _player_y
        chunck_00_x = - int((3 * size[0] - center_x) / (size[0]))
        chunck_00_y = - int((3 * size[1] - center_y) / (size[1]))
        chunck_list = []
        for chunck_y in range(chunck_00_y, chunck_00_y + 5):
            temp = []
            for chunck_x in range(chunck_00_x, chunck_00_x + 5):
                matrix_chunck = self.getMatrixChunck((chunck_x * size[0], chunck_y * size[1]), (int(size[0] / self.texture_size), int(size[1] / self.texture_size)), self.matrix)
                temp.append(Chunck((int(size[0] / self.texture_size), int(size[1] / self.texture_size)), (chunck_x * center_x, chunck_y * center_y), matrix_chunck, (chunck_x, chunck_y), self.texture_size))
            chunck_list.append(temp)
        self.map = self.assembleMap(self.chunck_list)
        self.is_map_generating = False
        return self.map