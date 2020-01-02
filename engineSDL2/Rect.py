
import ctypes
from sdl2 import *
class Rect(SDL_Rect):
    def __init__(self, t_xy = (0, 0), t_wh = (0, 0)):
        SDL_Rect.__init__(self)
        self.x = ctypes.c_int();
        self.y = ctypes.c_int();
        self.w = ctypes.c_int();
        self.h = ctypes.c_int();
    def copy(self):
        r = Rect()
        r.x, r.y = ctypes.c_int(self.x), ctypes.c_int(self.y)
        r.w, r.h = ctypes.c_int(self.w), ctypes.c_int(self.h)
        return r
        
    def move(self, t_x, t_Y):
        self.x += t_x
        self.y += t_y
        
    def makeCenter(t_cx, t_cy):
        self.x = ctypes.c_int(t_cx - self.w/2);
        self.y = ctypes.c_int(t_cy - self.h/2);
        
    def lock(self):
        pass
        
    def unlock(self):
        pass
    
    def dissolve(self):
        self.x = ctypes.c_int();
        self.y = ctypes.c_int();
        self.w = ctypes.c_int();
        self.h = ctypes.c_int();
