import threading
from sdl2 import *
from sdl2.sdlttf import *

import Golem


font_list = []

class Font():
    def __init__(self):
        self.m_size = 20
        self.m_bold = False
        self.m_italic = False
        self.m_underline = False
        self.m_strikethrough = False
        self.m_SDLfont = None
        self.m_font = None
    
    def __del__(self):
        TTF_CloseFont(self.m_font)
    
    @property
    def bold(self):
        return m_bold
    
    @property
    def italic(self):
        return m_italic
    
    @property
    def underline(self):
        return m_underline
    
    @property
    def strikethrough(self):
        return m_strikethrough
    
    @bold.setter
    def bold(self, boolean):
        self.m_bold = boolean
    
    @italic.setter
    def italic(self, boolean):
        self.m_italic = boolean
    
    @underline.setter
    def underline(self, boolean):
        self.m_underline = boolean
        
    @strikethrough.setter
    def strikethrough(self, boolean):
        self.m_strikethrough = boolean
    
    def updateFont(self):
        style = TTF_STYLE_NORMAL
         
        
        if self.m_bold:
            style |= TTF_STYLE_BOLD
        
        if self.m_italic:
            style |= TTF_STYLE_ITALIC
        
        if self.m_underline:
            style |= TTF_STYLE_UNDERLINE
        
        if self.m_strikethrough:
            style |= TTF_STYLE_STRIKETHROUGH
        
        if self.m_SDLfont:
            TTF_SetFontStyle(self.m_SDLfont, style)
            
        else:
            self.m_SDLfont = TTF_OpenFont(b"/home/anantha/Desktop/pyGolem/engineSDL2/fonts/OpenSans-Regular.ttf", 20)
            print(self.m_SDLfont)
#            if self.m_font:
#                TTF_SetFontStyle(self.m_font, style)
#            else:
#                print("ERROR: Couldn't create Font.")
#                print(SDL_GetError())
#        
