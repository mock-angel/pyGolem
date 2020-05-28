from sdl2 import *
import ctypes
import Golem
import World
#World = World.World

class Panel():
    def __init__():
        pass
    
    def render(self):
        pass


class ViewPort(Golem.property.Sprite):
    def __init__(self, window):
        Golem.property.Sprite.__init__(self, window)
        self.width = int(1920/2)
        self.height = int(1080/2)
        self.load()
    def load(self):
        self.surface = Golem.property.Surface((self.width, self.height)).convert()
        SDL_FillRect(self.surface, None,  SDL_MapRGB(self.surface.contents.format, 69, 69, 69))
        self.SetSurface("default", self.surface)
        self.texture = self.surface.getTexture(self.m_renderTarget)
        self.setTexture( self.texture )
        
    def draw(self, surface):
        pass
    
    def render(self):
        Golem.property.Sprite.render(self)
        
class SandBoxWorld(World.World):
    def __init__(self, window):
        #self.game_view = GameView()
        self.view_port = ViewPort(window)
        
    def draw(self):
        print("hello")
    
    def render(self):
        World.World.render(self)
        self.view_port.render()
        # render in order
#        self.game_view.render()
#        self.panels.render()
        #self.TimeLine.draw()
        
class SandBox(Golem.Window):
    def __init__(self):
        Golem.Window.__init__(self)
        self.mode = "RENDER"
    
    def load(self):
        self.world = SandBoxWorld(self)
#        self.render = self.world.render
#        self.draw = self.world.draw
#        
    def draw(self):
        #self.world.draw(self.window_surface)
        self.world.draw()
        
    def render(self):
        self.world.render()
