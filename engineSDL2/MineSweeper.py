from sdl2 import *
import sdl2
import sdl2.ext as sdl2ext

import Golem

#RESOURCES = sdl2ext.Resources(__file__, "resources")

class MineWindow(Golem.Window):
    def __init__(self):
        Golem.Window.__init__(self)
        self.s = 0
        #self.load()
    def load(self):
        
        #sp = Golem.property.BasicButton(self)
        #self.scene.add(sp)
        
        #spriteSurfDefault = Golem.create_new_surface(size = (32,32), name = "sprite", color = (50, 5, 5))
        #spriteSurfOver = Golem.create_new_surface(size = (32,32), name = "sprite_over", color = (215, 5, 5))
        #spriteSurfHeld = Golem.create_new_surface(size = (32,32), name = "sprite_held", color = (115, 5, 5))
        #theme = Golem.property.ButtonThemeFactory.genTheme(spriteSurfDefault, spriteSurfOver)
        #Draw_Round(spriteSurfDefault, 2, 2, 28, 28, 5, (186, 189, 182))
        
        #theme = Golem.property.ButtonThemeFactory.genTheme(Golem.loadSurface("golem.png"), Golem.loadSurface("g1.png"))
        #sp.setTheme(theme)
        #sp.SetSurface("sprite", spriteSurfDefault)
        print("window created")
        
        sp = Golem.property.BasicButton(self)
        spriteSurfDefault = Golem.create_new_surface(size = (32,32), name = "sprite", color = (50, 5, 5))
        spriteSurfOver = Golem.create_new_surface(size = (32,32), name = "sprite_over", color = (215, 5, 5))
        spriteSurfHeld = Golem.create_new_surface(size = (32,32), name = "sprite_held", color = (115, 5, 5))
        theme = Golem.property.create_button_theme(spriteSurfDefault, spriteSurfOver, spriteSurfHeld)
        
        sp.setTheme(theme)
        self.scene.add(sp)
