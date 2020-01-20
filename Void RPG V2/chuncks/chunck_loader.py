from chuncks.chunck import Chunck
import PIL.ImageTk
import PIL.Image
import time

class ChunckLoader():
    def __init__(self, _player_x, _player_y, _graphic_engine, _pil_textures, _matrix, _coefs):
        self.options = _graphic_engine.options
        self.pil_textures = _pil_textures
        self.matrix = _matrix
        self.is_map_generating = False
        self.graphic_engine = _graphic_engine
        self.texture_size = self.graphic_engine.options["texture_size"]
        self.x_coef = _coefs[0]
        self.y_coef = _coefs[1]
    def startCheckLoop(self, _player):
        ###Mettte en place les coefs des le chargement
        self.player = _player
        size = (self.graphic_engine.options["x_window_size"], self.graphic_engine.options["y_window_size"])
        t = 0
        while self.graphic_engine.graphic_engine_on == True:
            time.sleep(1/60)
            self.x = ((size[0] * (-1.5) - self.player.x) + self.x_coef) / (self.texture_size // 25)
            self.y = ((size[1] * (-1.5) - self.player.y) + self.y_coef) / (self.texture_size // 25)
            print(int(self.x), int(self.y), int(self.player.x), int(self.player.y), self.chunck_list[2][2].real_chunck_coords[0], (self.chunck_list[2][2].real_chunck_coords[0] + size[0]) / (self.texture_size // 25), self.chunck_list[2][2].real_chunck_coords[1], (self.chunck_list[2][2].real_chunck_coords[1] + size[1]) / (self.texture_size // 25), self.is_map_generating)
            if self.is_map_generating == False and t <= 10:
                if not self.chunck_list[2][2].isPlayerOnChunck(self.x, self.y):
                    print("Round number :", t)
                    t += 1
                    if self.chunck_list[2][1].isPlayerOnChunck(self.x, self.y):
                        self.is_map_generating = False
                        self.loadMapFromCenter(self.x, self.y, self.chunck_list[2][1])
                        self.x_coef -= size[0]
                        self.player.x -= size[0]
                    elif self.chunck_list[2][3].isPlayerOnChunck(self.x, self.y):
                        self.is_map_generating = False
                        self.loadMapFromCenter(self.x, self.y, self.chunck_list[2][3])
                        self.x_coef += size[0]
                        self.player.x += size[0]
                    elif self.chunck_list[1][2].isPlayerOnChunck(self.x, self.y):
                        self.is_map_generating = False
                        self.loadMapFromCenter(self.x, self.y, self.chunck_list[1][2])
                        self.y_coef -= size[1]
                        self.player.y -= size[1]
                    elif self.chunck_list[3][2].isPlayerOnChunck(self.x, self.y):
                        self.is_map_generating = False
                        self.loadMapFromCenter(self.x, self.y, self.chunck_list[3][2])
                        self.y_coef += size[1]
                        self.player.y += size[1]
                    else:
                        self.loadMapFromCenter(self.x, self.y)
                        self.player_x = size[0] * (-1.5) - self.x
                        self.player_y = size[1] * (-1.5) - self.y
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
    def loadMapFromCenter(self, _player_x, _player_y, _current_chunck=None):
        self.is_map_generating = True
        size = (self.options["x_window_size"], self.options["y_window_size"])
        #Ici appeler le chunck sur lequel est le joueur pour avoir son centre
        if _current_chunck != None:
            center_x = _current_chunck.chunck_center[0]
            center_y = _current_chunck.chunck_center[1]
        else:
            center_x = int(_player_x)
            center_y = int(_player_y)
        chunck_00_x = (center_x - 2 * size[0]) // size[0]
        chunck_00_y = (center_y - 2 * size[1]) // size[1]
        chunck_list = []
        for chunck_y in range(chunck_00_y, chunck_00_y + 5):
            temp = []
            for chunck_x in range(chunck_00_x, chunck_00_x + 5):
                print(chunck_x * size[0], chunck_y * size[1])
                matrix_chunck = self.getMatrixChunck((chunck_x * size[0], chunck_y * size[1]), (int(size[0] / self.texture_size), int(size[1] / self.texture_size)), self.matrix)
                temp.append(Chunck((int(size[0] / self.texture_size), int(size[1] / self.texture_size)), (chunck_x * center_x, chunck_y * center_y), matrix_chunck, (chunck_x, chunck_y), self.texture_size))
            chunck_list.append(temp)
        self.chunck_list = chunck_list
        self.map = self.assembleMap(self.chunck_list)
        self.is_map_generating = False
        return self.map