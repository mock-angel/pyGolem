from sdl2 import *

import Golem
import property

class Texture:
    def __init__(self, sdl_texture = None, surface = NOne):
        self.SDLTexture = sdl_texture
        self.surface = surface
    def getSDL(self):
        return self.SDLTexture
    
    def updateTexture(self):
        "Creates a new texture"
        if self.surface.buffer:
            if (self.surface != None):
                createdTexture = SDL_CreateTextureFromSurface( self.m_renderTarget, self.SDLSurface)
                if (createdTexture != None): self.SDLTexture = createdTexture
                
            self.surface.buffer = False
            
class Surface:
    def __init__(self ):
        self.pairedTexture = None
        self.__buffer = True
        self.SDLSurface = None
        
        self.surfaceLock = multithreading.Lock()
        self.property = None
        
    def draw(self, surface):
        pass
        
    def getTexture(self):
        return self.pairedTexture
        
    def updateTexture(self):
        """create pairedTexture if update is required."""
        if self.pairedTexture == None:
            self.pairedTexture = Texture()
             
        self.pairedTexture.updateTexture() 
        
    def getSDL(self):
        return self.SDLSurface
        
    def apply(self):
        self.buffer = True
        
        
#class Fabric:
#    def __init__(self):

'''
class SurfaceFactory:
    def __init__(self):
        pass
    
    def createSurface()
'''   
    
