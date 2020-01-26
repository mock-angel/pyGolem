import threading
from sdl2 import *

import Golem
from sdl2.sdlttf import *

class Text():
    def __init__(self):
        self.m_font = None
        
        self.m_rect = Golem.Rect((0, 0), (1, 1))
        self.m_text = ""
        
        self._aa = False
        
#        self.color_fg = Color("white")
#        self.color_bg = None#Color("gray20")
        
        self.color_fg = SDL_Color(100, 100, 100)
        self.color_bg = SDL_Color(200, 100, 100)
        self.m_spriteSurface = None
        self.m_spriteTexture = None
        
        self.dirty = True
        
        self.m_renderTarget = None
        
        self.m_surfaceLock = threading.Lock()
        self.m_textureLock = threading.Lock()
        
        self.m_visible = True
    def __del__(self):
        pass
    
    # Getters
    @property
    def aa(self): 
        return self._aa
        
    @property
    def font(self):
        return self.m_font
    
    @property
    def text(self):
        return self.m_font
    
    @property
    def color(self): 
        return self.color_fg
        
    # Setters
    @aa.setter
    def aa(self, aa):
        
        self._aa = aa
        self.dirty = True
        self._render()
    
    @font.setter
    def font(self, font):
        self.m_font = font
    
    @text.setter
    def text(self, t_text):
        self.m_text = t_text
        self.dirty = True
    
    @color.setter
    def color(self, t_color): 
        self.color_fg = t_color
        self.dirty = True
    
    def setText(self, t_text):
        self.text = t_text
        return self
    
    def setColor(self, t_color):
        self.color = t_color
        return self
        
    # Render thread only funtions.
    def _draw(self):
        if not self._aa:
            createdSurface = TTF_RenderText_Solid(self.m_font.m_SDLfont, b"put your text here", self.color_fg)
        else:
            createdSurface = TTF_RenderText_Blended(self.m_font.m_SDLfont, b"put your text here", self.color_fg)
        
        self.m_spriteSurface = createdSurface
        
        if self.m_spriteSurface:
            self.m_rect.w = createdSurface.contents.w
            self.m_rect.h = createdSurface.contents.h
        
    def _render(self):
        self._draw()
        
        newTexture = None
        
        if createdSurface:
            newTexture = SDL_CreateTextureFromSurface( t_renderer, createdSurface )
        
        self.m_textureLock = newTexture
        
        
    def draw(self, t_surface):
        if (not self.m_visible): return
        
        if self.dirty == True:
            self.dirty = False
            self._draw()
            
        if (SDL_BlitSurface(self.m_spriteSurface, None, t_surface, self.m_rect) < 0):
            print(SDL_GetError())
        
    def render(self):
        if (not self.m_visible): return
        
        if self.dirty == True:
            self.dirty = False
            self._render()
        
        if (SDL_RenderCopy(self.m_renderTarget, self.m_spriteTexture, None, self.m_rect)<0):
            print(SDL_GetError())
    
