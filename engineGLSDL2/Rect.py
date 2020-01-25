
import ctypes
from sdl2 import *
class Rect(SDL_Rect):
    def __init__(self, t_xy = (0, 0), t_wh = (0, 0)):
        SDL_Rect.__init__(self)
        # TODO: find why without c_int is also working..
        self.x = ctypes.c_int();
        self.y = ctypes.c_int();
        self.w = ctypes.c_int();
        self.h = ctypes.c_int();
#        self.x = 0
#        self.y = 0
#        self.w = 0
#        self.h = 0
        self.m_center = None
        
    def copy(self):
        r = Rect()
        r.x, r.y = ctypes.c_int(self.x), ctypes.c_int(self.y)
        r.w, r.h = ctypes.c_int(self.w), ctypes.c_int(self.h)
        return r
        
    def move(self, t_x, t_y):
        self.x += t_x
        self.y += t_y
        return self
        
    def makeCenter(t_cx, t_cy):
        self.center = (t_cx, t_cy)
        return self
        
    @property
    def center(self):
        return self.m_center
    
    @center.setter
    def center(self, t_cxy):
        (t_cx, t_cy) = t_cxy
        t_cx = int(t_cx)
        t_cy = int(t_cy)
        self.m_center = t_cxy
        self.x = ctypes.c_int(t_cx - self.w//2);
        self.y = ctypes.c_int(t_cy - self.h//2);
#        self.x = t_cx - (self.w//2);
#        self.y = t_cy - (self.h//2);

    def lock(self):
        pass
        
    def unlock(self):
        pass
    
    def dissolve(self):
        self.x = ctypes.c_int();
        self.y = ctypes.c_int();
        self.w = ctypes.c_int();
        self.h = ctypes.c_int();
