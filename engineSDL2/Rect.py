
import ctypes
from sdl2 import *
class Rect(SDL_Rect):
    def __init__(self, t_xy = (0, 0), t_wh = (0, 0)):
        SDL_Rect.__init__(self)
        # TODO: find why without c_int is also working..
#        self.x = ctypes.c_int();
#        self.y = ctypes.c_int();
#        self.w = ctypes.c_int();
#        self.h = ctypes.c_int();
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.m_center = None
        
    def copy(self):
        r = Rect()
#        r.x, r.y = ctypes.c_int(self.x), ctypes.c_int(self.y)
#        r.w, r.h = ctypes.c_int(self.w), ctypes.c_int(self.h)
        r.x, r.y = self.x, self.y
        r.w, r.h = self.w, self.h
        return r
        
    def move(self, t_x, t_y):
        self.x += t_x
        self.y += t_y
        return self
    
    def move_cp(self, t_x, t_y):
        r = self.copy()
        r.x += t_x
        r.y += t_y
        return r
    
    def clamp(self, rect):
        pass
    
    def clamp_cp(self, rect):
        r = self.copy()
        r.clamp(rect)
    
    def clip(self, rect):
        pass
    
    def clip_cp(self, rect):
        r = self.copy()
        r.clip(rect)
    
    def union(self, rect):
        pass
    
    def union_cp(self, rect):
        r = self.copy()
        r.union(rect)
    
    def unionall(self, rect):
        pass
    
    def unionall_cp(self, rect):
        r = self.copy()
        r.unionall(rect)
    
    def fit(self):
        r = Rect()
        return r
        
    def normalize(self):
        """correct negative sizes"""
    
    def contains(self, rect):
        """test if one rectangle is inside another"""
        pass
    
    def collidepoint(self, point):
        pass
    
    def collidelist(self, li):
        pass
    
    def collidelistall(self, li):
        pass
    
    def collidedict(self, di):
        pass
    
    def collidedictall(self, di):
        pass
    def make_center(t_cx, t_cy):
        self.center = (t_cx, t_cy)
        return self
        
    @property
    def center(self):
        return self.m_center
    
    @property
    def top(self):
        return self.y
        
    @property
    def left(self):
        return self.y
    
    @top.setter
    def top(self, t_top):
        self.y = t_top
    
    @top.setter
    def left(self, t_left):
        self.x = t_left
        
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
    
    
    @property
    def height(self):
        return self.h
    
    @top.setter
    def height(self, t_height):
        self.h = t_height
    
    @property
    def width(self):
        return self.w
    
    @top.setter
    def width(self, t_width):
        self.w = t_width
    
    def lock(self):
        pass
        
    def unlock(self):
        pass
    
    def dissolve(self):
        self.x = ctypes.c_int();
        self.y = ctypes.c_int();
        self.w = ctypes.c_int();
        self.h = ctypes.c_int();
    
