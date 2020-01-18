from sdl2 import *
import sdl2
import sdl2.ext as sdl2ext

import Golem
from Tile import GameScene
#RESOURCES = sdl2ext.Resources(__file__, "resources")

#class GameScene(Golem.property.Scene):
#    def __init__(self, t_window):
#        Golem.property.Scene.__init__(self, t_window)
#        
#        self.setSceneName = "Gamr Page - Play!"
#        default = Golem.create_new_surface(size = (152, 62), name = "sprite", color = (50, 5, 5))
#        hover = Golem.create_new_surface(size = (152, 62), name = "sprite", color = (50, 200, 5))
#        pressed = Golem.create_new_surface(size = (152, 62), name = "sprite", color = (200, 5, 5))
#        self.bt_theme = bt_theme = Golem.property.create_button_theme(default, hover, pressed)
#        
#        sp = Golem.property.BasicButton(self.window)
#        sp.theme = bt_theme
#        self.add(sp)
#        sp.m_rect.center = 100, 100

class MainScene(Golem.property.Scene):
    def __init__(self, t_window):
        Golem.property.Scene.__init__(self, t_window)
        self.scale_size = (186, 186)
        self.setSceneName = "Stating Page - Field Size Selection"
        default = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 5, 5))
        hover = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 200, 5))
        pressed = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (200, 5, 5))
        theme = Golem.property.create_button_theme(default, hover, pressed)
        
        
        surf_8x8 = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 5, 5))
        surf_16x16 = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 5, 5))
        surf_30x16 = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 5, 5))
        surf_custom = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 5, 5))
        
        
        theme = Golem.property.create_button_theme(default, hover, pressed)
        
        bt_8x8 = self.make_selection_button((-1, -1), theme, None, None)
        bt_16x16 = self.make_selection_button((1, -1), theme, None, None)
        bt_30x16 = self.make_selection_button((-1, 1), theme, None, None)
        bt_custom = self.make_selection_button((1, 1), theme, None, None)
        
        self.add(bt_8x8)
        self.add(bt_16x16)
        self.add(bt_30x16)
        self.add(bt_custom)
    
    def make_selection_button(self, cell_xy, theme, callback, params):
        cell_x, cell_y = cell_xy
        cx = self.window.size[0]/2 + cell_x * (self.scale_size[0]/2 + 9)
        cy = self.window.size[1]/2 + cell_y * (self.scale_size[1]/2 + 9)
        print (cx, cy)
        bt = Golem.property.BasicButton(self.window)
        bt.theme = theme
        bt.force_apply()
        bt.rect.center = cx, cy
#        bt.hide()
        return bt
        
class MineWindow(Golem.Window):
    def __init__(self, *t_):
        Golem.Window.__init__(self, *t_)
        self.s = 0
        #self.load()
    def load(self):
        
        print("window created")
        
        sp = Golem.property.BasicButton(self)
        
        # Create themes.
        default_mine = Golem.create_new_surface(size = (32,32), name = "sprite", color = (50, 5, 5))
        default_hover_mine = Golem.create_new_surface(size = (32,32), name = "sprite", color = (215, 5, 5))
        default_pressed_mine = Golem.create_new_surface(size = (32,32), name = "sprite", color = (50, 200, 58))
        
        default_theme = Golem.property.create_button_theme(default_mine, default_hover_mine, default_pressed_mine)
        
        
        mine_exploded = Golem.create_new_surface(size = (32,32), name = "sprite_over", color = (215, 5, 5))
        theme = Golem.property.create_button_theme(default_mine, default_hover_mine, default_pressed_mine)
        sp.theme = theme
        i_d_main = self.scene.createScene(MainScene)
        i_d_game_scene = self.scene.createScene(GameScene)
        
        self.scene.switchScene(i_d_game_scene)
        self.scene.addTo(sp, i_d_game_scene)
        self.scene.switchScene(i_d_main)
        #self.scene.switchScene(i_d_main)
        #self.scene.switchScene(i_d)
        
#    def create_tiles(self):
#        
#        grp = Golem.SpriteGroup()
#        for r in range(self.rows):
#            for c in range(self.columns):
#                tile = Tile(r, c)
#                grp.add(tile)
