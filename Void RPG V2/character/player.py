import time
from random import randint
import threading
from pynput import keyboard

class Player():
    def __init__(self, _x, _y, _map, _window, _parent):
        self.y_dir_up = 0
        self.y_dir_down = 0
        self.x_dir_left = 0
        self.x_dir_right = 0
        self.x = _x
        self.y = _y
        self.real_x = 0
        self.read_y = 0
        self.map = _map
        self.window = _window
        self.parent = _parent
        #Temp
        self.listener = keyboard.Listener(on_press=self.keyPress, on_release=self.keyRelease)
        self.listener.start()
        self.player_move_loop = threading.Thread(target=self.mainloop)
        self.player_move_loop.start()
    def keyPress(self, key):
        try:
            if key.char.lower()=="z":
                try:
                    if self.y_dir_up==0:
                        self.y_dir_up=1
                except AttributeError:
                    self.y_dir_up=1
            elif key.char.lower()=="s":
                try:
                    if self.y_dir_down==0:
                        self.y_dir_down=1
                except AttributeError:
                    self.y_dir_down=1
            elif key.char.lower()=="q":
                try:
                    if self.x_dir_left==0:
                        self.x_dir_left=1
                except AttributeError:
                    self.x_dir_left=1
            elif key.char.lower()=="d":
                try:
                    if self.x_dir_right==0:
                        self.x_dir_right=1
                except AttributeError:
                    self.x_dir_right=1
        except AttributeError:
            pass
    def keyRelease(self, key):
        try:
            if key.char.lower()=="z":
                self.y_dir_up=0
            elif key.char.lower()=="s":
                self.y_dir_down=0
            elif key.char.lower()=="q":
                self.x_dir_left=0
            elif key.char.lower()=="d":
                self.x_dir_right=0
        except AttributeError:
            pass
    def mainloop(self):
        xinfos={"multiplier":1, "deceleration":False, "accel_nbre":1, "decel_nbre":1, "speed_lim":5, "accel_speed":2}
        yinfos={"multiplier":1, "deceleration":False, "accel_nbre":1, "decel_nbre":1, "speed_lim":5, "accel_speed":2}
        x_dir =  self.x_dir_right - self.x_dir_left
        y_dir =  self.y_dir_down - self.y_dir_up
        exec_time = 0
        #threading.Thread(target=self.calcPxPerSeconds).start()
        while self.parent.parent.graphic_engine_on == True:
            time.sleep(1/60 - exec_time)
            t1 = time.time()
            try:
                try:
                    last_x_dir = x_dir
                    last_y_dir = y_dir
                except UnboundLocalError:
                    last_x_dir = 0
                    last_y_dir = 0
                x_dir =  self.x_dir_right - self.x_dir_left
                y_dir =  self.y_dir_down - self.y_dir_up

                if last_x_dir!=x_dir:
                    xinfos["deceleration"], xinfos["decel_dir"] = True, last_x_dir
                    xinfos["decel_multiplier"] = xinfos["multiplier"]
                    xinfos["accel_nbre"], xinfos["decel_nbre"] = 1, 1
                    xinfos["multiplier"] = 1

                if last_y_dir!=y_dir:
                    yinfos["deceleration"], yinfos["decel_dir"] = True, last_y_dir
                    yinfos["decel_multiplier"] = yinfos["multiplier"]
                    yinfos["accel_nbre"], yinfos["decel_nbre"] = 1, 1
                    yinfos["multiplier"] = 1

                #Gestion de la deceleration
                if xinfos["deceleration"] == True and x_dir == 0:
                    xinfos["decel_nbre"] += 1
                    if xinfos["decel_multiplier"] > 1:
                        if xinfos["decel_nbre"] % randint(1, 2) == 0:
                            xinfos["decel_multiplier"] -= 0.10
                            self.x -= xinfos["decel_dir"] * xinfos["decel_multiplier"]
                        else:
                            self.x -= xinfos["decel_dir"] * xinfos["decel_multiplier"]
                    else:
                        xinfos["deceleration"] = False
                if yinfos["deceleration"] == True and y_dir == 0:
                    yinfos["decel_nbre"] += 1
                    if yinfos["decel_multiplier"] > 1:
                        if yinfos["decel_nbre"] % randint(1, 2) == 0:
                            yinfos["decel_multiplier"] -= 0.10
                            self.y -= yinfos["decel_dir"] * yinfos["decel_multiplier"]
                        else:
                            self.y -= yinfos["decel_dir"] * yinfos["decel_multiplier"]
                    else:
                        yinfos["deceleration"] = False

                #Acceleration dans tous les cas
                if x_dir != 0:
                    xinfos["accel_nbre"] += 1
                if xinfos["multiplier"] <= xinfos["speed_lim"] and xinfos["accel_nbre"] % xinfos["accel_speed"] == 0:
                    xinfos["multiplier"] += 0.2
                    self.x -= last_x_dir * xinfos["multiplier"]
                else:
                    self.x -= last_x_dir * xinfos["multiplier"]
                if y_dir != 0:
                    yinfos["accel_nbre"] += 1
                if yinfos["multiplier"] <= yinfos["speed_lim"] and yinfos["accel_nbre"] % yinfos["accel_speed"] == 0:
                    yinfos["multiplier"] += 0.2
                    self.y -= last_y_dir * yinfos["multiplier"]
                else:
                    self.y -= last_y_dir * yinfos["multiplier"]

                #Actualisation visuelle
                #print(self.x, self.y)
                if self.parent.parent.graphic_engine_on == True:
                    self.parent.wallpaper_canvas.coords(self.map, self.x, self.y)
                else:
                    break
                exec_time = time.time() - t1
                #print(time.time() - mesure)
            except AttributeError:
                pass
            except RuntimeError:
                pass
    def calcPxPerSeconds(self):
        while self.parent.parent.graphic_engine_on == True:
            x, y = self.x, self.y
            time.sleep(1)
            print(x - self.x, y - self.y)