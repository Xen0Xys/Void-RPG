import time
from random import randint
import threading

class Player():
    def __init__(self, _x, _y, _map, _window, _parent):
        self.dirYm = 0
        self.dirYp = 0
        self.dirXm = 0
        self.dirXp = 0
        self.x = _x
        self.y = _y
        self.map = _map
        self.window = _window
        self.parent = _parent
        #Temp
        #self.window.bind("<KeyPress>", lambda arg1=None, arg2="KeyPress":self.move(arg1, arg2))
        #self.window.bind("<KeyRelease>", lambda arg1=None, arg2="KeyRelease":self.move(arg1, arg2))
        self.main_loop_on = True
        threading.Thread(target=self.mainloop).start()
    def move(self, evt, arg):
        if arg=="KeyPress":
            if evt.keysym.lower()=="z":
                try:
                    if self.dirYm==0:
                        self.dirYm=1
                except AttributeError:
                    self.dirYm=1
            elif evt.keysym.lower()=="s":
                try:
                    if self.dirYp==0:
                        self.dirYp=1
                except AttributeError:
                    self.dirYp=1
            elif evt.keysym.lower()=="q":
                try:
                    if self.dirXm==0:
                        self.dirXm=1
                except AttributeError:
                    self.dirXm=1
            elif evt.keysym.lower()=="d":
                try:
                    if self.dirXp==0:
                        self.dirXp=1
                except AttributeError:
                    self.dirXp=1
        if arg=="KeyRelease":
            if evt.keysym.lower()=="z":
                self.dirYm=0
            elif evt.keysym.lower()=="s":
                self.dirYp=0
            elif evt.keysym.lower()=="q":
                self.dirXm=0
            elif evt.keysym.lower()=="d":
                self.dirXp=0
    def mainloop(self):
        xinfos={"multiplier":1, "deceleration":False, "accel_nbre":1, "decel_nbre":1, "speed_lim":2.2, "accel_speed":8}
        yinfos={"multiplier":1, "deceleration":False, "accel_nbre":1, "decel_nbre":1, "speed_lim":2.2, "accel_speed":8}
        xdir = -self.dirXm + self.dirXp
        ydir = -self.dirYm + self.dirYp
        while self.main_loop_on:
            time.sleep(.01)
            try:
                try:
                    lastxdir = xdir
                    lastydir = ydir
                except UnboundLocalError:
                    lastxdir = 0
                    lastydir = 0
                xdir = -self.dirXm + self.dirXp
                ydir = -self.dirYm + self.dirYp

                if lastxdir!=xdir:
                    xinfos["deceleration"], xinfos["decel_dir"] = True, lastxdir
                    xinfos["decel_multiplier"]=xinfos["multiplier"]
                    xinfos["accel_nbre"], xinfos["decel_nbre"] = 1, 1
                    xinfos["multiplier"] = 1

                if lastydir!=ydir:
                    yinfos["deceleration"], yinfos["decel_dir"] = True, lastydir
                    yinfos["decel_multiplier"]=yinfos["multiplier"]
                    yinfos["accel_nbre"], yinfos["decel_nbre"] = 1, 1
                    yinfos["multiplier"] = 1

                #Gestion de la deceleration
                if xinfos["deceleration"]==True:
                    xinfos["decel_nbre"]+=1
                    if xinfos["decel_multiplier"]>1:
                        if xinfos["decel_nbre"]%randint(1, 2)==0:
                            xinfos["decel_multiplier"]-=0.10
                            self.x-=xinfos["decel_dir"]*xinfos["decel_multiplier"]
                        else:
                            self.x-=xinfos["decel_dir"]*xinfos["decel_multiplier"]
                    else:
                        xinfos["deceleration"]=False
                if yinfos["deceleration"]==True:
                    yinfos["decel_nbre"]+=1
                    if yinfos["decel_multiplier"]>1:
                        if yinfos["decel_nbre"]%randint(1, 2)==0:
                            yinfos["decel_multiplier"]-=0.10
                            self.y-=yinfos["decel_dir"]*yinfos["decel_multiplier"]
                        else:
                            self.y-=yinfos["decel_dir"]*yinfos["decel_multiplier"]
                    else:
                        yinfos["deceleration"]=False

                #Acceleration dans tous les cas
                if xdir!=0:
                    xinfos["accel_nbre"]+=1
                if xinfos["multiplier"]<=xinfos["speed_lim"] and xinfos["accel_nbre"]%xinfos["accel_speed"]==0:
                    xinfos["multiplier"]+=0.2
                    self.x-=lastxdir*xinfos["multiplier"]
                else:
                    self.x-=lastxdir*xinfos["multiplier"]
                if ydir!=0:
                    yinfos["accel_nbre"]+=1
                if yinfos["multiplier"]<=yinfos["speed_lim"] and yinfos["accel_nbre"]%yinfos["accel_speed"]==0:
                    yinfos["multiplier"]+=0.2
                    self.y-=lastydir*yinfos["multiplier"]
                else:
                    self.y-=lastydir*yinfos["multiplier"]

                #Actualisation visuelle
                print(self.x, self.y)
                self.parent.wallpaper_canvas.coords(self.map, self.x, self.y)
            except AttributeError as e:
                pass
            except RuntimeError as e:
                pass