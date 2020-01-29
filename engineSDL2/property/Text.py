import threading
from sdl2 import *

import Golem
from sdl2.sdlttf import *

class Text():
    def __init__(self, text = "", font = None):
        self.m_font = font
        
        self.rect = Golem.Rect((0, 0), (1, 1))
        self.m_text = text.encode()#text#.encode('utf-8')
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
        return self.m_text
    
    @property
    def color(self): 
        return self.color_fg
        
    # Setters
    @aa.setter
    def aa(self, aa):
        
        self._aa = aa
        self.dirty = True
    
    @font.setter
    def font(self, font):
        self.m_font = font
    
    @text.setter
    def text(self, t_text):
        self.m_text = t_text.encode()
        self.dirty = True
    
    @color.setter
    def color(self, t_color): 
        self.color_fg = t_color
        self.dirty = True
    
    def setText(self, t_text):
        self.text = t_text.encode()
        return self
    
    def setColor(self, t_color):
        self.color = t_color
        return self
        
    # Render thread only funtions.
    def _draw(self):
        prev_surf = self.m_spriteSurface
        
        if self.m_font == None:
            print("Error : _draw() :: Font object not set")
            return
        
        self.m_font.updateFont()
        
        if not self._aa:
            createdSurface = TTF_RenderText_Solid(self.m_font.m_SDLfont, self.m_text, self.color_fg)
        else:
            createdSurface = TTF_RenderText_Blended(self.m_font.m_SDLfont, self.m_text, self.color_fg)
        
        self.m_spriteSurface = createdSurface
        
        if self.m_spriteSurface:
            self.rect.w = createdSurface.contents.w
            self.rect.h = createdSurface.contents.h
        
        SDL_FreeSurface(prev_surf)
        
    def _render(self):
        self._draw()
        
        prevTexture = self.m_spriteTexture
        newTexture = None
        
        if createdSurface:
            newTexture = SDL_CreateTextureFromSurface( t_renderer, createdSurface )
        
        self.m_textureLock = newTexture
        SDL_DestroyTexture(prevTexture)
        
    def draw(self, t_surface):
        if (not self.m_visible): return
        
        if self.dirty == True:
            self.dirty = False
            self._draw()
        
        if (SDL_BlitSurface(self.m_spriteSurface, None, t_surface, self.rect) < 0):
            print(SDL_GetError())
        
    def render(self):
        if (not self.m_visible): return
        
        if self.dirty == True:
            self.dirty = False
            self._render()
        
        if (SDL_RenderCopy(self.m_renderTarget, self.m_spriteTexture, None, self.rect)<0):
            print(SDL_GetError())


class TextLine(Text):
    def __init__(self, text = "", font = None):
        Text.__init__(self, text, font)
        pass

# Needs immense revision.
class TextWall(object):
    def __init__(self, font = None):
        self.m_font = None
        self.offset = Golem.Rect((20, 20), (1, 1))
        
        self.text_lines = []
        self._text_paragraph = "Empty\nText"
        self._text_paragraph_split = []
        self.dirty = True
        
    def _render(self):
        # render list 
        self.text_lines = [ TextLine(line, self.m_font) for line in self.text_lines ]        

        # offset whole paragraph
        if len(self.text_lines):
            self.text_lines[0].rect.top = self.offset.top
        
    def parse_text(self, text):
        # parse raw text to something usable
        self._text_paragraph = text.split("\n")
        
    @property
    def font(self):
        return self.m_font
    
    @property
    def text(self):
        return self.m_text
    
    @property
    def color(self): 
        return self.color_fg
        
    # Setters
    @font.setter
    def font(self, font):
        self.m_font = font
    
    @text.setter
    def text(self, t_text):
        self._text_paragraph = t_text
        self.dirty = True
    
    def parse_text(self, text):
        # parse raw text to something usable
        self._text_paragraph_split = _text_paragraph.split("\n")
        self.dirty = True
    
    def draw(self, surface):
        # draw with cached surfaces
        if self.dirty: 
            self.dirty = True
            self._render()
            
        for text in self.text_lines:
             text.draw(surface)
    
    def render(self, surface):
        # draw with cached surfaces
        if self.dirty: 
            self.dirty = True
            self._render()
            
        for text in self.text_lines:
             text.render()
