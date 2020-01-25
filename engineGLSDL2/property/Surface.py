# Surface.py
"""
    This is a modifying library. 
    It extends the SDL_Surface objects after its been created.
"""
from sdl2 import *

import Golem
import property

#class Texture:
#    def __init__()
def bind(instance, func, as_name=None):
    """
    Bind the function *func* to *instance*, with either provided name *as_name*
    or the existing name of *func*. The provided *func* should accept the 
    instance as the first argument, i.e. "self".
    """
    if as_name is None:
        as_name = func.__name__
    bound_method = func.__get__(instance, instance.__class__)
    setattr(instance, as_name, bound_method)
    return bound_method
    
class Surface():
    def __init__(self, size):
        surf = Golem.create_new_surface(size)
        surf.__init__(surf)
        Surface.wrap(surf)
        self.surf = surf
    def convert(self):
        return self.surf
        
    def wrap(self):
        Surface.init(self)
        Surface.bind(self)
        
    def getTexture(self, t_renderer):
        newTexture = SDL_CreateTextureFromSurface( t_renderer, self )
        
        if not newTexture:
            print("Unable to create texture from {}! SDL Error: {}".format(bpath.c_str(), SDL_GetError()) )
        
        return newTexture
        
    def init(self):
        # This is where the texture of the surface sits.
        self.pairedTexture = None
        
        # Decides if the texture needs to get updated.
        self.__buffer = True
        
        # THis is where the SDL_Surface sits.
        self.SDLSurface = None
        
        # apply() will update the buffer.
        self.bufferTexture = None
        
        #Surface.bind(self)
        
    def bind(self, external = None):
        if external: self = external
        
        bind(self, Surface.blit)
        bind(self, Surface.get_rect)
        bind(self, Surface.getTexture)
        
    def blit(self, surface):
        pass
    
    def get_rect(self):
        pass

