import PIL.ImageTk
import PIL.Image

class Chunck():
    def __init__(self, _size, _canvas_coords, _matrix, _chunck_number, _texture_size):
        self.collision_list = []
        self.map = None
        self.texture_size = _texture_size
        self.matrix = _matrix
        self.size = _size
        self.real_coords = _canvas_coords
        self.chunck_number = _chunck_number
        self.chunck_loaded = False
        self.real_chunck_coords = self.getRealChunckCoords(self.chunck_number[0], self.chunck_number[1], self.size[0], self.size[1])
        self.chunck_center = self.getCenter(self.size[0], self.size[1], self.real_chunck_coords[0], self.real_chunck_coords[1])
        """
        print(self.chunck_center)
        print(self.real_chunck_coords)
        print(self.chunck_number)
        print("-----------------")
        """
    def isPlayerOnChunck(self, _player_x, _player_y):
        size_x = self.size[0] * self.texture_size
        size_y = self.size[1] * self.texture_size
        if self.real_chunck_coords[0] < _player_x < self.real_chunck_coords[0] + size_x:
            if self.real_chunck_coords[1] < _player_y < self.real_chunck_coords[1] + size_y:
                return True
        return False
    def getCenter(self, _size_x, _size_y, _real_x, _real_y):
        center_x = int(_real_x + (_size_x * self.texture_size / 2))
        center_y = int(_real_y + (_size_y * self.texture_size / 2))
        return (center_x, center_y)
    def getRealChunckCoords(self, _x_chunck, _y_chunck, _size_x, _size_y):
        return (int(_x_chunck * _size_x * self.texture_size / (self.texture_size // 25)), int(_y_chunck * _size_y * self.texture_size / (self.texture_size // 25)))
    def generateChunck(self, _pil_textures_list, force=False):
        if (self.chunck_loaded == False) or (force == True):
            try:
                pil_map = PIL.Image.open("cache/earth_{}_{}.png".format(self.chunck_coords[0], self.chunck_coords[1]))
            except FileNotFoundError:
                pil_map = PIL.Image.new("RGB", ((self.size[0] * self.texture_size), (self.size[1] * self.texture_size)))
                for y in range(self.size[1]):
                    for x in range(self.size[0]):
                        if self.matrix[y][x] != "00":
                            loaded = False
                            while loaded == False:
                                try:
                                    pil_map.paste(im=_pil_textures_list["map"][self.matrix[y][x]], box=(x * self.texture_size, y * self.texture_size))
                                    loaded = True
                                except AttributeError:
                                    pass
                pil_map.save("cache/earth_{}_{}.png".format(self.chunck_coords[0], self.chunck_coords[1]))
            self.map = pil_map
            self.chunck_loaded = True
            return pil_map
        return self.map
    def getChunck(self, _pil_textures_list):
        try:
            return self.map
        except FileNotFoundError:
            return self.generateChunck(_pil_textures_list, force=True)