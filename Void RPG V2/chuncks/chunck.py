import PIL.ImageTk
import PIL.Image

class Chunck():
    def __init__(self, _size, _canvas_coords, _matrix, _chunck_coords):
        self.map = None
        self.matrix = _matrix
        self.size = _size
        self.real_coords = _canvas_coords
        self.chunck_coords = _chunck_coords
        self.chunck_loaded = False
    def generateChunck(self, _pil_textures_list, force=False):
        if (self.chunck_loaded == False) or (force == True):
            try:
                pil_map = PIL.Image.open("cache/earth_{}_{}.png".format(self.chunck_coords[0], self.chunck_coords[1]))
            except FileNotFoundError:
                pil_map = PIL.Image.new("RGB", ((self.size[0] * 25), (self.size[1] * 25)))
                for y in range(self.size[1]):
                    for x in range(self.size[0]):
                        if self.matrix[y][x] != "00":
                            loaded = False
                            while loaded == False:
                                try:
                                    pil_map.paste(im=_pil_textures_list["map"][self.matrix[y][x]], box=(x * 25, y * 25))
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
    def isPlayerOnChunck(self, player_x, player_y):
        pass