import sys
import ctypes
from sdl2 import *

import Golem
import property

class ButtonThemeFactory():
    """Obsolete, will be removed soon."""
    def __init__(self):
        pass
    
    @staticmethod
    def genTheme(default = None, hover = None, held = None, disabled = None):
        hover = default if not hover else hover
        held = hover if not held else held
        
        dict_ = {   # refilter this.
            "sprite" : default,
            "clicked" : hover,
            "rclicked" : hover,
            
            "enter" : hover,
            "sprite_over" : hover,
            "leave" : default,
            
            "sprite_pressed" : held,
            "released" : hover,
            
            "sprite_disabled" : default,
        }
        
        return dict_
        
def create_button_theme(default = None, hover = None, held = None, disabled = None):
        hover = default if not hover else hover
        held = hover if not held else held
        
        dict_ = {   # refilter this.
            "sprite" : default,
            "clicked" : hover,
            "rclicked" : hover,
            
            "enter" : hover,
            "sprite_over" : hover,
            "leave" : default,
            
            "sprite_pressed" : held,
            "released" : hover,
            
            "sprite_disabled" : default,
        }
        
        return dict_
class ButtonBehaviour(property.SpriteBehaviour):
    SPRITE_DEFAULT = 0
    SPRITE_DISABLED = 1
    SPRITE_OVER = 2
    SPRITE_PRESSED = 3
    
    def __init__(self):
        property.SpriteBehaviour.__init__(self)
        
        self.AddSurface("sprite", None)
        self.AddSurface("sprite_over", None)
        self.AddSurface("sprite_pressed", None)
        self.AddSurface("sprite_disabled", None)
        
#        self.AddTexture("sprite", None)
#        self.AddTexture("sprite_over", None)
#        self.AddTexture("sprite_pressed", None)
#        self.AddTexture("sprite_disabled", None)
        
        self.renderState = ButtonBehaviour.SPRITE_DEFAULT;
        
        self.m_dirty = True
    
    def __del__(self):
        pass
        
    def updateSurfBuffer(self):# or updateBufferSurf?
        # Recheck usage of selectSurface here in this method.
        Golem.property.SpriteBehaviour.updateSurfBuffer(self)
        
        renderState = self.renderState
        
        if renderState == ButtonBehaviour.SPRITE_OVER:
            self.GetSurface("sprite_over")
            if (self.reqSurface != None): self.m_spriteSurface = self.reqSurface
                #if reqSurface switches get new width and height. self.m_rect
            self.reqSurface == None
            return
            
        if renderState == ButtonBehaviour.SPRITE_PRESSED:
            self.GetSurface("sprite_pressed")
            if (self.reqSurface != None): self.m_spriteSurface = self.reqSurface
            self.reqSurface == None
            return
        if self.m_spriteSurface:
            self.m_rect.w, self.m_rect.h = self.m_spriteSurface.contents.w, self.m_spriteSurface.contents.h
    def updateBuffer(self):
        # TODO: BROKEN IMPLETENTATION RIGHT NOW!!
        # Please get back to this and change name of method when adding textures.
        
        Golem.property.SpriteBehaviour.updateBuffer(self)
        
        self.GetSurface("sprite_over")
        if (self.reqSurface != None):
            createdTexture = SDL_CreateTextureFromSurface( self.m_renderTarget, self.reqSurface)
            if (createdTexture != None): self.SetTexture("sprite_over", createdTexture )
        
        self.GetSurface("sprite_pressed")
        if (self.reqSurface != None):
            createdTexture = SDL_CreateTextureFromSurface( self.m_renderTarget, self.reqSurface)
            if (createdTexture != None): self.SetTexture("sprite_pressed", createdTexture )
        
        self.reqSurface = None
        
        renderState = self.renderState
        
        if renderState == ButtonBehaviour.SPRITE_OVER:
            self.GetTexture("sprite_over")
            if (self.reqTexture != None): self.m_spriteTexture = self.reqTexture;
            w = ctypes.pointer(ctypes.c_int())
            h = ctypes.pointer(ctypes.c_int())
            SDL_QueryTexture(self.m_spriteTexture, None, None, w, h);
            self.m_rect.w, self.m_rect.h = w.contents, h.contents
            return
            
        if renderState == ButtonBehaviour.SPRITE_PRESSED:
            self.GetTexture("sprite_pressed")
            if (self.reqTexture != None): self.m_spriteTexture = self.reqTexture;
            SDL_QueryTexture(self.m_spriteTexture, None, None, ctypes.byref(self.m_rect.w), ctypes.byref(self.m_rect.h));
            return
            
    #################################################
    # Calls the callback when events are encountered.
    def onClicked(self):
#        print("onClicked")
        if (self.m_disabled): return
        self.m_callbacks["onClicked"](*self.m_params["onClicked"])
        
    def onLift(self):
        if (self.m_disabled): return
        self.m_callbacks["onLift"](*self.m_params["onLift"])
        
    def onReleased(self):
#        print("onReleased")
        if (self.m_disabled): return
        
        self.m_surfaceLock.acquire();
        self.renderState = ButtonBehaviour.SPRITE_OVER;
        self.buffer_flag = True;
        self.m_surfaceLock.release();
        
        self.m_callbacks["onReleased"](*self.m_params["onReleased"])
        
    def onPressed(self):
#        print("onPressed")
        if (self.m_disabled): return
        
        self.m_callbacks["onPressed"](*self.m_params["onPressed"])
        
    def onDrop(self):
#        print("onDrop")
        if (self.m_disabled): return
        
        self.m_surfaceLock.acquire();
        self.renderState = ButtonBehaviour.SPRITE_PRESSED;
        self.buffer_flag = True;
        self.m_surfaceLock.release();
        
        self.m_callbacks["onDrop"](*self.m_params["onDrop"])
        
    def onRightClicked(self):
#        print("onRightClicked")
        if (self.m_disabled): return
        self.m_callbacks["onRightClicked"](*self.m_params["onRightClicked"])
        
    def onHover(self):
#        print("onHover")
        if (self.m_disabled): return
        self.m_callbacks["onHover"](*self.m_params["onHover"])
        
    def onEnter(self):
#        print("onEnter")
        if (self.m_disabled): return
        
        self.m_surfaceLock.acquire();
        self.renderState = ButtonBehaviour.SPRITE_OVER;
        self.buffer_flag = True;
        self.m_surfaceLock.release();
        
        self.m_callbacks["onEnter"](self.m_params["onEnter"])
        
    def onLeave(self):
#        print("onLeave")
        if (self.m_disabled): return
        
        self.m_surfaceLock.acquire();
        self.renderState = ButtonBehaviour.SPRITE_DEFAULT;
        self.buffer_flag = True;
        self.m_surfaceLock.release();
        
        self.m_callbacks["onLeave"](*self.m_params["onLeave"])
        
class BasicButton(ButtonBehaviour, property.Sprite):
    def __init__(self, t_window):
        
        property.Sprite.__init__(self, t_window)
        ButtonBehaviour.__init__(self)
        self.m_renderTarget = t_window.getRenderer() if t_window else None
    
    def set_pos(self, x, y):
        self.rect
        return self
    
    def setTheme(self, t_theme): # TODO: Make this function invisible?
        self.theme = t_theme
        #self.enscribeTheme(t_theme)
        return self
    
class Button(BasicButton):
    """A Button that acts like BasicButton, but adds in text functionality.
    
    Although this class can accept image themes using setThemes, 
    it gives more priority to text. Call ButtonOBJ.disableText() once to
    disable rendering text and BUttonOBJ.enableText() to enable rendering back.
    """
    def __init__(self, t_window):
        BasicButton.__init__(self, t_window)
        
    def set_text(self, t_text):
        self.m_text = t_text
        return self

class ButtonGroup(property.SpriteGroup):
    def __init__(self):
        property.SpriteGroup.__init__(self)
        pass
