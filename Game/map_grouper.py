from PIL import Image, ImageTk
import json

class Viewer():
    def Start(self):
        self.LoadTextures()
        self.CreateMapPicture()
    def LoadTextures(self):
        txtrnameList=[]
        file=open("ressources/textures/map/textures.cfg", "r")
        content=file.read()
        file.close()
        content=content.replace(" ", "")
        content=content.replace("\n", "")
        content=content.split(";")
        self.textureList={}
        encodeList=[]
        for i in content:
            try:
                if i!="" or i[0]=="#":
                    temp=i.split("=")
                    self.textureList[temp[0]]=temp[1]
                    encodeList.append(temp[0])
                    if temp[1]!="NONE":
                        txtrnameList.append(temp[1])
            except IndexError:
                pass
        for key in self.textureList.keys():
            if key!="00":
                self.textureList[key]=Image.open("ressources/textures/map/{}".format(self.textureList[key]))
                self.textureList[key]=self.textureList[key].resize((4, 4))
    def CreateMapPicture(self):
        rs = createJsonFileFromMapContent(getAllMapContent())
        self.Matrice=[]
        print(len(rs), len(rs[0]))
        for y in range(600):
            temp=[]
            for x in range(600):
                try:
                    temp.append(rs[y][x])
                except IndexError:
                    pass
            self.Matrice.append(temp)
        result=Image.new("RGB", (600, 600))
        print(len(self.Matrice), len(self.Matrice[0]))
        for i in range(len(self.Matrice)):
            for j in range(len(self.Matrice[i])):
                if self.Matrice[i][j]!="00":
                    try:
                        image = self.textureList[self.Matrice[i][j]]
                        #image=image.resize((4, 4))
                        result.paste(im=image, box=(j, i))
                        #print(str(i), str(j))
                    except KeyError:
                        pass
        #self.result.save("image.png")
        result.show()



def returnVoidList():
    void_list = []
    for _ in range(30):
        temp = []
        for _ in range(30):
            temp.append("00")
        void_list.append(temp)
    return void_list


def getAllMapContent():
    map_dict = {}
    for y in range(20):
        for x in range(20):
            try:
                file = open("ressources/maps/earth_{}_{}.map".format(x, y), "r")
                ct = file.read()
                file.close()
                map_list = serializeMapFile(ct)
                map_dict["{}_{}".format(x, y)] = map_list
            except FileNotFoundError:
                map_dict["{}_{}".format(x, y)] = returnVoidList()
    return map_dict

def serializeMapFile(_map_content):
    #Ok
    map_content_split = _map_content.split("\n")
    map_list = []
    for y_map in range(30):
        temp = []
        for x in range(0, 60, 2):
            #print(y_map, map_content_split[y_map], x, x + 2)
            temp.append(map_content_split[y_map][x : x + 2])
        map_list.append(temp)
    return map_list

def createJsonFileFromMapContent(_all_map_content):
    all = []
    for map_y in range(20):
        for col_number in range(30):
            temp = []
            for map_x in range(20):
                result = _all_map_content["{}_{}".format(map_x, 19 - map_y)][col_number]
                for item in result:
                    temp.append(item)
            all.append(temp)
    return all


rs = createJsonFileFromMapContent(getAllMapContent())

file = open("ALL_MAP.json", "w")
file.write(json.dumps(rs, indent=4))
file.close()

v = Viewer()
v.Start()