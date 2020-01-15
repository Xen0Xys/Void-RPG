import time
from random import randint
import threading
from pynput import keyboard
from tkinter import *

class Player():
    def __init__(self, _x, _y, _map, _window, _parent):
        self.y_dir_up = 0
        self.y_dir_down = 0
        self.x_dir_left = 0
        self.x_dir_right = 0
        self.x = _x
        self.y = _y
        self.real_x = self.x + 2.5 * _window.options["x_window_size"]
        self.real_y = self.y + 2.5 * _window.options["y_window_size"]
        print(self.real_x, self.real_y)
        self.map = _map
        self.window = _window
        self.parent = _parent
        #Temp
    def start(self):
        self.player_loop = True
        self.listener = keyboard.Listener(on_press=self.keyPress, on_release=self.keyRelease)
        self.listener.start()
        self.player_move_loop = threading.Thread(target=self.mainloop)
        self.player_move_loop.start()
        #self.parent.game_view.getCanvas().create_image(self.x, self.y, image=self.map, anchor=NW)
    def setupNewMap(self, _pil_map):
        #self.player_loop = False
        #self.player_move_loop.join(1)
        for c in self.window.winfo_children():
            c.destroy()
        self.parent.game_view.wallpaper_canvas = Canvas(self.parent, width=self.parent.options["x_window_size"], height=self.parent.options["y_window_size"], bg="#9a9a9a", highlightthickness=0)
        self.parent.game_view.wallpaper_canvas.place(x=0, y=0)
        self.parent.game_view.picture = self.parent.game_view.wallpaper_canvas.create_image(0, 0, image=_pil_map, anchor=NW)
        """
        self.player_loop = True
        self.player_move_loop = threading.Thread(target=self.mainloop)
        self.player_move_loop.start()
        """
    def keyPress(self, key):
        try:
            if key.char.lower() == "z":
                try:
                    if self.y_dir_up == 0:
                        self.y_dir_up = 1
                except AttributeError:
                    self.y_dir_up = 1
            elif key.char.lower() == "s":
                try:
                    if self.y_dir_down == 0:
                        self.y_dir_down = 1
                except AttributeError:
                    self.y_dir_down = 1
            elif key.char.lower() == "q":
                try:
                    if self.x_dir_left == 0:
                        self.x_dir_left = 1
                except AttributeError:
                    self.x_dir_left = 1
            elif key.char.lower() == "d":
                try:
                    if self.x_dir_right == 0:
                        self.x_dir_right = 1
                except AttributeError:
                    self.x_dir_right = 1
        except AttributeError:
            pass
    def keyRelease(self, key):
        try:
            if key.char.lower() == "z":
                self.y_dir_up = 0
            elif key.char.lower() == "s":
                self.y_dir_down = 0
            elif key.char.lower() == "q":
                self.x_dir_left = 0
            elif key.char.lower() == "d":
                self.x_dir_right = 0
        except AttributeError:
            pass
    def mainloop(self):
        x_infos={"multiplier":1, "deceleration":False, "accel_nbre":1, "decel_nbre":1, "speed_lim":5, "accel_speed":2}
        y_infos={"multiplier":1, "deceleration":False, "accel_nbre":1, "decel_nbre":1, "speed_lim":5, "accel_speed":2}
        x_dir =  self.x_dir_right - self.x_dir_left
        y_dir =  self.y_dir_down - self.y_dir_up
        exec_time = 0
        #threading.Thread(target=self.calcPxPerSeconds).start()
        while self.parent.graphic_engine_on == True and self.player_loop == True:
            sleep_time = 1/60 - exec_time
            if sleep_time > 0:
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
                    x_infos["deceleration"], x_infos["decel_dir"] = True, last_x_dir
                    x_infos["decel_multiplier"] = x_infos["multiplier"]
                    x_infos["accel_nbre"], x_infos["decel_nbre"] = 1, 1
                    x_infos["multiplier"] = 1
                if last_y_dir!=y_dir:
                    y_infos["deceleration"], y_infos["decel_dir"] = True, last_y_dir
                    y_infos["decel_multiplier"] = y_infos["multiplier"]
                    y_infos["accel_nbre"], y_infos["decel_nbre"] = 1, 1
                    y_infos["multiplier"] = 1

                #Gestion de la deceleration
                if x_infos["deceleration"] == True:
                    x_infos["decel_nbre"] += 1
                    if x_infos["decel_multiplier"] > 1:
                        if x_infos["decel_nbre"] % 2 == 0:
                            x_infos["decel_multiplier"] -= 0.10
                            self.x -= x_infos["decel_dir"] * x_infos["decel_multiplier"]
                        else:
                            self.x -= x_infos["decel_dir"] * x_infos["decel_multiplier"]
                    else:
                        x_infos["deceleration"] = False
                if y_infos["deceleration"] == True:
                    y_infos["decel_nbre"] += 1
                    if y_infos["decel_multiplier"] > 1:
                        if y_infos["decel_nbre"] % 2 == 0:
                            y_infos["decel_multiplier"] -= 0.10
                            self.y -= y_infos["decel_dir"] * y_infos["decel_multiplier"]
                        else:
                            self.y -= y_infos["decel_dir"] * y_infos["decel_multiplier"]
                    else:
                        y_infos["deceleration"] = False

                #Acceleration dans tous les cas
                if x_dir != 0:
                    x_infos["accel_nbre"] += 1
                if x_infos["multiplier"] <= x_infos["speed_lim"] and x_infos["accel_nbre"] % x_infos["accel_speed"] == 0:
                    x_infos["multiplier"] += 0.2
                    self.x -= last_x_dir * x_infos["multiplier"]
                else:
                    self.x -= last_x_dir * x_infos["multiplier"]
                if y_dir != 0:
                    y_infos["accel_nbre"] += 1
                if y_infos["multiplier"] <= y_infos["speed_lim"] and y_infos["accel_nbre"] % y_infos["accel_speed"] == 0:
                    y_infos["multiplier"] += 0.2
                    self.y -= last_y_dir * y_infos["multiplier"]
                else:
                    self.y -= last_y_dir * y_infos["multiplier"]

                #Actualisation visuelle
                if self.parent.graphic_engine_on == True:
                    try:
                        self.parent.game_view.wallpaper_canvas.coords(self.parent.game_view.picture, self.x, self.y)
                    except TclError:
                        pass
                else:
                    break
                exec_time = time.time() - t1
            except RuntimeError:
                pass
    def calcPxPerSeconds(self):
        while self.parent.graphic_engine_on == True:
            x, y = self.x, self.y
            time.sleep(1)
            print(x - self.x, y - self.y)