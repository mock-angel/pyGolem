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
    """
        Contains 4 buttons to choose 3 different tilesets.
        A custom button to create custom game.
    """
    def __init__(self, t_window):
        Golem.property.Scene.__init__(self, t_window)
        
        self.font = Golem.property.Font()
        self.font.updateFont()
        
        self.text  = Golem.property.TextWall()
        self.init_buttons()
        
    def init_buttons(self):
        
        font = self.font
        text = self.text
        
        self.scale_size = (186, 186)
        self.setSceneName = "Stating Page - Field Size Selection"
        default = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 5, 5))
        hover = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 200, 5))
        pressed = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (200, 5, 5))
        theme = Golem.property.create_button_theme(default, hover, pressed)
        
        default = Golem.loadSurface("button/selection/default.png")
        hover = Golem.loadSurface("button/selection/hover.png")
        pressed = Golem.loadSurface("button/selection/pressed.png")
        theme = Golem.property.create_button_theme(default, hover, pressed)
        
        f1 = Golem.property.Font()
        f2 = Golem.property.Font()
        f3 = Golem.property.Font()
        f1.size = 10
        f2.size = 16
        f2.bold = True
        
        def draw_text(mine_size_str, mine_count_str, post_text_str):
            surf = SDL_CreateRGBSurface(0, self.scale_size[0], self.scale_size[1], 32, 0xff, 0xff00, 0xff0000, 0xff000000);
            size = surf.contents.w, surf.contents.h
            Golem.property.Surface.bind(surf)
            
            # "Mines" text.
            text_mines = Golem.property.TextLine(font = f1, text = post_text_str)
            text_mines.color = SDL_Color(60, 60, 60)
            text_mines._draw()
            
            # Draw 8x8 at the center of the image.
            text = Golem.property.TextLine(font = f2)
            text.color = SDL_Color(60, 60, 60)
            text.text = mine_size_str
            text._draw()
            text.rect.center = size[0]/2, size[1]/2 - text.rect.height/2
            text.draw(surf)
            print ("size test", text.rect.center, surf)
            
            # Mine count.
            text.text = mine_count_str
            x = size[0]/2 - (text_mines.rect.width)/2
            y = size[1]/2 + text.rect.height/2
            text.rect.center = x, y
            text.draw(surf)
            
            # "Mines" is drawn.
            x = size[0]/2 + text.rect.width/2 
            text_mines.rect.center = x, y
            
            text_mines.draw(surf)
            
            return surf
            
        text_8x8_surf = draw_text("8 x 8", "10", " mines")
        text_16x16_surf = draw_text("16 x 16", "40", " mines")
        text_30x16_surf = draw_text("30 x 16", "99", " mines")
        text_custom_surf = draw_text("?", "", "Custom")
        
        surf_8x8 = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 5, 5))
        surf_16x16 = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 5, 5))
        surf_30x16 = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 5, 5))
        surf_custom = Golem.create_new_surface(size = self.scale_size, name = "sprite", color = (50, 5, 5))
        
#        default = text_16x16_surf
        
        
        text.font = font
        text.text = b"text"
#        text.draw(default)
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
        
        self.mode = "RENDER"
        
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
