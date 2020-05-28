import os
import threading

from sdl2 import *
import time


import Golem
import OpenGL.GL as GL
import OpenGL.GLU as GLU
from OpenGL.arrays import vbo
from OpenGL.GL import *

class ColorRGBA(object):
    def __init__(self, r = 0, g = 0, b = 0, a = 0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

class WindowBackground(object):
    def __init__(self):

        self.m_bgColor = ColorRGBA()
        self.m_renderer = None
        self.m_surface = None

    def getRenderer(self):
        return self.m_renderer

    def setBackgroundColor(self, t_r = 0, t_g = 0, t_b = 0, t_a = 0):
        self.m_bgColor = t_bgColor = ColorRGBA(t_r, t_g, t_b, t_a)
#        SDL_SetRenderDrawColor( self.m_renderer, t_bgColor.r, t_bgColor.g, t_bgColor.b, t_bgColor.a )
        
        return self

class Window( WindowBackground, object ):
    """
    A class that manages the window operations.

    ...

    Attributes
    ----------
    DEFAULTPOS : SDL_ constants
        default flags for window position during creation.
    DEFAULTWINDOWFLAGS : SDL_ constants
    DEFAULTRENDERFLAGS : SDL_ constants

    Methods
    -------
    __init__(title=bytes(b"Hello"), width=592, height= 460)
        defines necessary parameters and initilies certain variables.
    __del__()
        here is where we destroy all stuff
    init()
    render()
    handle_event()
        used by eventThread() run on main thread to process events.
    load()
        FIXME: this is probably broken and model is not usable

    getWindowId()
        returns the window id.
    isClosed()
        returns true if closed.
    isMinimized()
        returns True if minimised.
    sprites()
        returns the current active sprites the Window processes
    title()
        sets the title of the window
        TODO: Make it editable after window creation.

    maximize()
        Maximizes the window.
    minimise()
        Minimises the window.
    restore()
        restores the window to its original shown state.
    focus()
        switch focus to the window.

    newWidget()
        widget management section in development.
    """


    DEFAULTPOS = SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED
    DEFAULTWINDOWFLAGS = SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE | SDL_WINDOW_OPENGL
    DEFAULTRENDERFLAGS = SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC
#    DEFAULTRENDERFLAGS = SDL_WINDOW_OPENGL
    """Used by user to handle and do stuff"""
    def __init__(self, title = bytes(b"Hello"), width = 800, height = 600):
        WindowBackground.__init__(self)
        self.m_title = title
        self.m_windowId = 0

        self.mode = "OPENGL" # "DRAW" use only Surfaces // "RENDER" use textures at the end result for heavy games

        self.m_mouseFocus = True
        self.m_keyboardFocus = True
        self.m_minimized = False
        self.m_closed = False

        self.screen_color = (45, 45, 45)

        """NOTE: Render Lock and Surface Locks are never supposed to be called together."""

        self.m_width = width
        self.m_height = height
        self.m_size = (width, height)

        self.m_mouse = Golem.Mouse()

        self.windowPos = Golem.Window.DEFAULTPOS
        self.m_windowFlags = Golem.Window.DEFAULTWINDOWFLAGS
        self.m_rendererFLags = Golem.Window.DEFAULTRENDERFLAGS
        #self.m_scene = None
        #self.scene = Golem.property.SceneHandler()

        self.screen = None      # FIXME:Depreciated!

        self.m_window = None
        self.scene = Golem.property.SceneHandler(self)


        #Make this work!!!
        #self.sp = Golem.property.Sprite(self)

        # NOTE: Used only when window is opened in drawing mode.
        self.screenSurface = None

    def __del__(self):
        #SDL_GL_DeleteContext(self.context)
        SDL_DestroyRenderer(self.m_renderer)
        SDL_DestroyWindow(self.m_window)
        print("~Deleted Window")

    def init(self):
        #os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        if SDL_Init(SDL_INIT_VIDEO) != 0:
            print(SDL_GetError())
            return -1
        
        self.m_window = m_window = window = SDL_CreateWindow(self.m_title,
                              self.windowPos[0], self.windowPos[1],
                              self.m_width, self.m_height, self.m_windowFlags)

        if SDL_Init(SDL_INIT_VIDEO) != 0:
            print(SDL_GetError())
            return -1

        SDL_HideWindow(m_window)
        #self.context = SDL_GL_CreateContext(window)
        
        #SDL_GetVideoInfo( )
        
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK,
                                            SDL_GL_CONTEXT_PROFILE_CORE)
        
        
        
        self.context = None
        
        # -- SEt hit test rects here.
        if( m_window != 0 ):
            self.m_mouseFocus = True;
            self.m_keyboardFocus = True;

            # Create renderer for window.
            # windowsurface = SDL_GetWindowSurface(window)
        
            if self.mode == "OPENGL":
                self.context = SDL_GL_CreateContext(m_window)
                # SETUP
                print("Context Created")
                
            self.m_windowId = SDL_GetWindowID( m_window )
            self.m_shown = True;
            SDL_ShowWindow(m_window);

        SDL_SetWindowTitle(m_window, self.m_title)

        self.m_windowSurface = SDL_GetWindowSurface(m_window)

        self.load()

    def load(self):
        pass
    
    def start(self):
        self.game_loop()
    
    def glsetup(self):
        self.context = SDL_GL_CreateContext(self.m_window)
        
        # Viewport
        glViewport(0, 0, self.m_width, self.m_height);

#        GL.glOrtho(-400, 400, 300, -300, 0, 1)
    
    def process_event(self):
        e = event = SDL_Event()
        
        while (SDL_PollEvent(ctypes.byref(event)) != 0):
            # Set all event dependant variables.
            if e.type == SDL_MOUSEMOTION:
                self.m_mouse.x = e.motion.x
                self.m_mouse.y = e.motion.y
            
            # Process them in chunks.
            self.handle_event(e);
            self.handle_high_level_event(e)
                
    def handle_event(self, e):
        if( e.type == SDL_WINDOWEVENT ):
            if e.window.event == SDL_WINDOWEVENT_SHOWN:
                self.m_shown = True

            if e.window.event == SDL_WINDOWEVENT_HIDDEN:
                self.m_shown = False

            if e.window.event == SDL_WINDOWEVENT_SIZE_CHANGED:
                #Get new dimensions and repaint.
                
                self.m_width = e.window.data1;
                self.m_height = e.window.data2;

                GL.glViewport(0, 0, self.m_width, self.m_height);
                
            if e.window.event == SDL_WINDOWEVENT_EXPOSED:
                #Repaint on expose.
                pass
            if e.window.event == SDL_WINDOWEVENT_ENTER:
                self.m_mouseFocus = True

            if e.window.event == SDL_WINDOWEVENT_LEAVE:
                self.m_mouseFocus = False

            if e.window.event == SDL_WINDOWEVENT_FOCUS_GAINED:
                self.m_keyboardFocus = True

            if e.window.event == SDL_WINDOWEVENT_FOCUS_LOST:
                self.m_keyboardFocus = False

            if e.window.event == SDL_WINDOWEVENT_MINIMIZED:
                self.m_minimized = True

            if e.window.event == SDL_WINDOWEVENT_MAXIMIZED:
                self.m_minimized = False

            if e.window.event == SDL_WINDOWEVENT_RESTORED:
                self.m_minimized = False

            if e.window.event == SDL_WINDOWEVENT_CLOSE:

                #SDL_HideWindow( self.m_window )
                self.hide()

                self.m_window = None;
                self.m_renderer = None;
                self.m_closed = True;
    
    def handle_high_level_event(self, e):
        if e.type == SDL_MOUSEMOTION:
            sprites = self.sprites();
            for spr in sprites:
                if (spr.m_mouseOver): # If entered before.
                    # event is onHover() if mouse still inside rectangle.
                    if ( self.m_mouse.isCollided(spr.m_rect) ):
                        if spr.m_pressed: spr.onPressed()# call onDrag from here.
                        else: spr.onHover()
                    else:
                        # NOTE: spr.m_pressed should not be changed if you
                        # intend to let the user perform the 
                        spr.m_pressed = False 
                        
                        spr.m_mouseOver = False
                        spr.onLeave()
                    
                elif ( self.m_mouse.isCollided(spr.m_rect) ):
                    # "onEnter" if first collided.
                    spr.m_mouseOver = True
                    spr.onEnter()
            #print("Mouvement to {}, {}".format(w.m_mouse.x, w.m_mouse.y))
            return
            
        if e.type == SDL_MOUSEBUTTONDOWN:
            sprites = self.sprites();
            if (e.button.button == SDL_BUTTON_LEFT):
                #LMB clicked.
                for spr in sprites:
                    if spr.m_mouseOver:
                        #if w.m_mouse.isCollided(spr.m_rect): spr.onHover()
                        #else:
                            spr.m_pressed = True
                            spr.onDrop()
                            spr.onPressed()
            return
            
        if e.type == SDL_MOUSEBUTTONUP:
            sprites = self.sprites();
            if (e.button.button == SDL_BUTTON_LEFT):
                for spr in sprites:
                    if ( spr.m_pressed ):
                        if ( self.m_mouse.isCollided(spr.m_rect) ):
                            spr.m_pressed = False
                            spr.onReleased()
                            spr.onClicked()
                            spr.onLift()# Simulates onClicked here.
                            # TODO: Create option to set onClicked before onLift
                            # or before onDrop() calls.
            return
            
        if e.type == SDL_KEYDOWN:
            print("Physical {} key acting as {} key\n".format(
                SDL_GetScancodeName(e.key.keysym.scancode),
                SDL_GetKeyName(e.key.keysym.sym)));
            return
            
        if e.type == SDL_KEYUP:
            return
        
    def update(self):
        """The application calls this in a thread in a loop."""
        time.sleep(0.1)

    def render(self):
        if (not self.isMinimized()):
            self.clearGl()
            
            self.scene.render();
            
            SDL_GL_SwapWindow(self.m_window)

    def game_loop(self):
        print("renderThread:: Started")
        #clock = pygame.time.Clock()
        clock = Golem.time.Clock()
        
        self.glsetup()
        
        while not self.isClosed():
            self.process_event()
            
            self.update()
            
            self.render()

        print("renderThread:: Stopped")
    
    def clearGl(self):
        glClearColor(0.2, 0.3, 0.3, 1.0);

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        
        SDL_GL_SwapWindow(self.m_window);
        
    # Getters.
    def getWindowId(self):
        return self.m_windowId

    def isClosed(self):
        return self.m_closed

    def isMinimized(self):
        return self.m_minimized

    @property
    def title(self):
        return self.m_title

    @property
    def size(self):
        return self.m_size

    def sprites(self):
        return self.scene.sprites()

    # User setters.
    def set_title(self, title_str):
        # TODO: check if its string and then change.
        self.m_title = title_str
        return self

    def set_size(self, size_tuple):
        self.m_size = size_tuple
        return self

    @title.setter
    def title(self, t_title):
        self.m_title = t_title
        return self
        
    @size.setter
    def size(self, t_size):
        self.m_size = t_size
        self.m_width = t_size[0]
        self.m_height = t_size[1]
        
    # Mutators  IMPORTANT
    def hide(self):
        """Hides the window and makes it disappear."""
        self.m_shown = False
        SDL_HideWindow( self.m_window )

    def show(self):
        """Unhides the window if hidden."""
        self.m_shown = True
        SDL_ShowWindow( self.m_window )

    def maximize(self):
        """Maximizes the window."""
        self.m_minimized = False
        SDL_MaximizeWindow( self.m_window )

    def minimise(self):
        """Minimises the window."""
        self.m_minimized = True
        SDL_MinimizeWindow( self.m_window )

    def restore(self):
        """Restores the window."""
        self.m_minimized = False
        SDL_RestoreWindow( self.m_window )

    def focus(self): # TODO: Test this.
        """Switches the focus to this window."""
        self.m_mouseFocus = self.m_keyboardFocus = True
        SDL_RaiseWindow(self.m_window)

    # Widget management. Application based methods.
    def new_widget(self, classname, *params):
        return classname(self, *params)

    #def showAll(self):
        #os.environ['SDL_VIDEO_CENTERED'] = '1'

        #self.screen = pygame.display.set_mode(self.m_size, pygame.NOFRAME)
