# Sprite.py 

import threading
import ctypes
from sdl2 import *

import Golem

class SpriteBehaviour(object):
    """
    Methods:
    
    Variables:
    m_sprTextures
        Stores surfaces that the Sprite uses.
    m_surfaceLock, self.m_textureLock
        Locks for both surfaces and textures.
    selectedSurface
        What the owner gets after SelectSurface
    m_renderTarget
        Target for rendering, save here to reduce stack time.
    
    """
    SPRITE_DEFAULT = 0
    SPRITE_DISABLED = 1
    
    def __init__(self):
        
        self.m_sprTextures = {}
        self.m_sprSurfaces = {} # TODO:Change to surfaceMap?
        self.selectedSurface = None
        
        # Locks for multithreading access.
        self.m_surfaceLock = threading.Lock()
        self.m_textureLock = threading.Lock() # FIXME: Not used
        
        self.m_renderTarget = None
        self.renderState = SpriteBehaviour.SPRITE_DEFAULT
        
        # Add basic Surface keys.
        self.AddSurface("sprite", None)
        self.AddSurface("sprite_disabled", None)
        
        # Do the same for textures.
#        self.AddTexture("sprite", None)
#        self.AddTexture("sprite_disabled", None)
        
    def __del__(self):
        # Do nothing.
        # TODO: Get to delete owning textures and sprites.
        pass
    
    
    def AddSurface(self, string, t_surface):
        """
            Initialises Key in Surface pool.
        """
        self.m_surfaceLock.acquire()
        if string in self.m_sprSurfaces:
            self.m_surfaceLock.release()
            print("Key {} allready existant".format(string))
            return None
        
        self.m_sprSurfaces[string] = t_surface
        self.m_surfaceLock.release()
    
    def SetSurface(self, string, t_surface):
        """
            Sets the key value to a passes surface.
        """
        self.m_surfaceLock.acquire()
        print ("SetSurface :", string)
        #self.buffer_flag = True # TODO: compare with previous implementation.
        if string not in self.m_sprSurfaces:
            self.m_surfaceLock.release()
            return None
            
        self.m_sprSurfaces[string] = t_surface 
        self.m_surfaceLock.release()
    
    def GetSurface(self, string):
        self.m_surfaceLock.acquire()
        if string not in self.m_sprSurfaces:
            print ("Button::GetSurface: key non-existant.")
            self.m_surfaceLock.release()
            return None
            
        self.reqSurface = self.m_sprSurfaces[string]
        self.m_surfaceLock.release()
        return self.reqSurface
    
    def SelectSurface(self, string):            # For user use only.
        self.m_surfaceLock.acquire()
        if string not in self.m_sprSurfaces:
            print("SelectSurface(): Key does not exist.")
            self.m_surfaceLock.release()
            return None
        self.selectedSurface = self.m_sprSurfaces[string]
        self.m_surfaceLock.release()
    
    def enscribeTheme(self, t_theme, keyList = None):
        # Call this inside draw function cuz this will hold up code.
        for key in t_theme:
            if (not keyList) or (key in keyList):
                self.SetSurface(key, t_theme[key])
                #print("ddd")
    def updateSurfBuffer(self):
        # TODO: FIXME: THIS has problems.
        
        renderState = self.renderState
        
        if renderState == SpriteBehaviour.SPRITE_DEFAULT:
            self.GetSurface("sprite")
            if (self.reqSurface != None): 
                self.m_spriteSurface = self.reqSurface;
                
            self.reqSurface == None
            return
            
        if renderState == SpriteBehaviour.SPRITE_DISABLED:
            self.GetSurface("sprite_disabled")
            if (self.reqSurface != None): self.m_spriteSurface = self.reqSurface;
            
            self.reqSurface == None
            return
        
        self.reqSurface == None
        
        if self.m_spriteSurface:
            self.m_rect.w, self.m_rect.h = self.m_spriteSurface.contents.w, self.m_spriteSurface.contents.h
        
    def updateRenderBuffer(self):
        self.updateSurfBuffer()
        self.m_spriteTexture = self.m_spriteSurface.getTexture(self.m_renderTarget);
        
    def force_apply(self):
        self.updateSurfBuffer()
        
class Sprite(SpriteBehaviour, object):
    """
    Attributes
    ----------
            Action control attributes.
    m_mouseOver
        True if Mouse is Over the Sprite.
    m_pressed
        True if inside m_rect and pressed.
    m_visible
        True if visible.
    m_disabled
        True if disabled.
    m_depth
        0 default. Used to set teh dept of the Sprite.
        Sprite of depth 1 appears behind sprite of depth 0.
    
    m_spriteSurface
        This surface will be drawn on the screen.
        
    Methods
    -------
    __init__(window)
    
    depth - property
        changes m_depth value of sprite.
    
    
    Methods Feature Exclusive 
    -------------------------...anything that returns self sprite.
    setDepth
        uses depth property
    
    
    
    """
    DEFAULTWINDOW = None
    RECENTWINDOW = None
    
    def __init__(self, t_window):
        SpriteBehaviour.__init__(self)
        
        Sprite.RECENTWINDOW = t_window
        
        self.m_mouseOver = False
        self.m_pressed = False
        self.m_visible = True
        self.m_disabled = False
        
        self.m_depth = 0
        
        self.m_spriteSurface = None
        self.m_spriteTexture = None
        
        self.buffer_flag = True;
        
        self.surface_buffer = True;
        self.texture_buffer = True;
        
        self.m_theme = None
        
        # None if using surfaces only mode.
        self.m_renderTarget = t_window.getRenderer() if t_window else None
        if not self.m_renderTarget:
            print("Sprite.__init__(self): created without any renderTarget.")
            #Golem.log_error("Sprite.__init__(self): created without any renderTarget.")
        
        self.m_rect = Golem.Rect((0, 0), (1, 1))
        self.rect = self.m_rect
        
        self.m_callbacks = {
            "onClicked": self.onDummy,
            "onReleased": self.onDummy,
            "onPressed": self.onDummy,
            "onRightClicked": self.onDummy,
            "onHover": self.onDummy,
            "onEnter": self.onDummy,
            "onLeave": self.onDummy,
            "onDrop": self.onDummy,
            "onLift": self.onDummy,
        }
        
        params = list()
        self.m_params = {
            "onClicked": params,
            "onReleased": params,
            "onPressed": params,
            "onRightClicked": params,
            "onHover": params,
            "onEnter": params,
            "onLeave": params,
            "onDrop": params,
            "onLift": params,
        }
        # TODO: Implement background blitting first.
        # variable to enable background blitting of sprite maybe?.
        # variable for buffer for surfaces?
    def setVisible(self, boolean):
        m_visible = bool(boolean)
        return self
    
    def isDisabled(self):
        return m_disabled
    
    def hide(self):
        self.m_visible = False
    
    def show(self):
        self.m_visible = True
    
    def getRenderer(self):
        return self.m_renderTarget
    
    def setTexture(self, t_texture):
        self.m_spriteTexture = self.t_texture
    
    def setRenderer(self, t_pRenderer):
        self.m_renderTarget = t_pRenderer
    
    def setVisible(self, t_visible):
        self.m_visible = t_visible
    
    def disable(self):
        self.m_disabled = True
    
    def enable(self):
        self.m_disabled = False
    
    def isDisabled(self):
        return self.m_disabled
    
    # Setters
    @property
    def depth(self):
        return m_depth
    
    @depth.setter
    def depth(self, d):
        self.m_depth = d
        
    @property
    def theme(self):
        return self.m_theme
    
    @theme.setter
    def theme(self, t_theme):
        self.m_theme = t_theme
        self.enscribeTheme(t_theme)
        self.buffer_flag = True
        
    def setDepth(self, d):
        self.depth = d
        return self
    
    # Called by handleEvent thread.
    def handleEvent(self, e):
        pass
    
    # Called by update Thread when not Disabled.
    def update(self):
        pass
    
    # Used by user to Draw sprite onto a surface.
    def draw(self, t_surface):
        if (not self.m_visible): return
        
        if self.buffer_flag == True:
            self.buffer_flag = False
            self.updateSurfBuffer()
#            print("Updating Surf Buffer")
            
        if (SDL_BlitSurface(self.m_spriteSurface, None, t_surface, self.m_rect) < 0):
            print(SDL_GetError())
        
    # Called by render Thread when sprite is visible.
    def render(self):
        if (not self.m_visible): return
        
        if self.buffer_flag == True:
            self.buffer_flag = False
            # TODO: Do something here
            
            self.updateRenderBuffer()
            
        if (SDL_RenderCopy(self.m_renderTarget, self.m_spriteTexture, None, self.m_rect)<0):
            print(SDL_GetError())
        
    # Defining Event methods.
    def onDummy(self, *params):
        pass
        
    def onPressed(self):
        self.m_callbacks["onPressed"](*self.m_params["onPressed"])
        print("onPressed")
        
    def onReleased(self):
        self.m_callbacks["onReleased"](*self.m_params["clicked"])
        print("onReleased")
        
    def onClicked(self):
        self.callbacks["onClicked"](*self.m_params["onClicked"])
        print("onClicked")
        
    def onRightClicked(self):
        self.m_callbacks["onRightClicked"](*self.m_params["onRightClicked"])
        print("onRightClicked")
        
    def onHover(self):
        self.m_callbacks["onHover"](*self.m_params["onHover"])
        print("onHover")
        
    def onEnter(self):
        self.m_callbacks["onEnter"](*self.m_params["onEnter"])
        print("onEnter")
        
    def onLeave(self):
        self.m_callbacks["onLeave"](*self.m_params["onLeave"])
        print("onLeave")
        
    def onDrop(self):
        self.m_callbacks["onDrop"](*self.m_params["onDrop"])
        print("onDrop")
        
    def onLift(self):
        self.m_callbacks["onLift"](*self.m_params["onLift"])
        print("onLift")
        
class SpriteGroup():
    def __init__(self):
        self.m_container = list()
        self.containerRenderLock = threading.Lock()
        self.containerDrawLock = threading.Lock()
        self.containerUpdateLock = threading.Lock()
        
    def add(self, spr, depth = 0):
        self.containerRenderLock.acquire()
        
        self.m_container.append(spr)
        #spr.__attatch_internal(self)
        
        self.containerRenderLock.release()
        
    def remove(self, spr):
        self.containerRenderLock.acquire()
        self.containerDrawLock.acquire()
        self.containerUpdateLock.acquire()
        
        self.m_container.pop(spr)
        self.__release_internal(self)
        
        self.containerUpdateLock.release()
        self.containerDrawLock.release()
        self.containerRenderLock.release()
    
    def update(self):
        self.containerUpdateLock.acquire()
        
        sprites = self.sprites()
        for spr in sprites:
            spr.update()
        
        self.containerUpdateLock.release()
    
    def render(self):
        self.containerRenderLock.acquire()
        
        sprites = self.sprites()
        for spr in sprites:
            spr.render()
        
        self.containerRenderLock.release()
        
    def draw(self, t_surface):
        self.containerDrawLock.acquire()
        
        sprites = self.sprites()
        for spr in sprites:
            spr.draw(t_surface)
        
        self.containerDrawLock.release()
        
    def sprites(self):
        return self.m_container
    
class SpriteHandler(SpriteGroup):
    def __init__(self, t_window):
        
        SpriteGroup.__init__(self)
        self.m_containerLock = threading.Lock()
        
    def setWindow(self, t_window):
        self.m_window = t_window
    
    def getWindow(self):
        return self.m_window
    
    def handleEvent(self, e):
        self.m_containerLock.acquire();
        
        sprites = self.sprites()
        
        if e.type == SDL_MOUSEMOTION:
            
            for spr in sprites:
                
                if (spr.m_mouseOver): # If entered before.
                    # event is onHover() if mouse still inside rectangle.
                    if ( self.m_window.m_mouse.isCollided(spr.m_rect) ):
                        if spr.m_pressed: spr.onPressed()# call onDrag from here.
                        else: spr.onHover()
                    else:
                        spr.m_mouseOver = False
                        spr.onLeave()
                    
                elif ( self.m_window.m_mouse.isCollided(spr.m_rect) ):
                    # "onEnter" if first collided.
                    spr.m_mouseOver = True
                    spr.onEnter()
            return
            
        if e.type == SDL_MOUSEBUTTONDOWN:

            if (e.button.button == SDL_BUTTON_LEFT):

                for spr in sprites:
                    if ( self.m_window.m_mouse.isCollided(spr.m_rect) ):
                        spr.m_pressed = True
                        spr.onPressed()
                    #temp->onClicked();
            
#            if (e.button.button == SDL_BUTTON_RIGHT):
#                for spr in sprites:
#                    if ( self.m_window.m_mouse.isCollided(spr.m_rect) ):
#                        spr.m_pressed = True
#                        spr.onRightClicked()
            
        if e.type == SDL_MOUSEBUTTONUP:

            if (e.button.button == SDL_BUTTON_LEFT): #Change to switch-case statements?
                for spr in sprites:
                    if ( spr.m_pressed ):
                        if m_window.m_mouse.isCollided(spr.m_rect) :
                            spr.m_pressed = False
                            spr.onClicked(); # TODO: refer order from python.
                            spr.onReleased();
                         
                    #temp->onClicked();
        if e.type == SDL_KEYDOWN:
            print ("Physical {} key acting as {} key\n",
                SDL_GetScancodeName(e.key.keysym.scancode),
                SDL_GetKeyName(e.key.keysym.sym));
        if e.type == SDL_KEYUP:
            pass
        
        self.m_containerLock.unlock();
