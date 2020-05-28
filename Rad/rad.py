from sdl2 import *
import sdl2
import sdl2.ext as sdl2ext

import Golem

class RadWindow(Golem.Window):
    def __init__(self, *t_):
        Golem.Window.__init__(self, *t_)
        self.mode = "OPENGL"
        
    def load(self):
        pass
