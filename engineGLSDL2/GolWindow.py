import os
import threading

from sdl2 import *
import time


import Golem

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
        here is where we destroy all SDL stuff
    init()
        probably not use this? But is called by user to activate the window.
    render()
        is called by renderThread() and this is where per frame render takes place.
    draw()
        is called by drawThread() and this is where per frame drawing takes place.
    renderThread()
        is run as a seperate thread if the window was created using "RENDER" mode
    drawThread()
        is run as a seperate thread if the window was created using "DRAW" mode
    handleEvent()
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
    DEFAULTWINDOWFLAGS = SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE
    DEFAULTRENDERFLAGS = SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC | SDL_WINDOW_OPENGL
    """Used by user to handle and do stuff"""
    def __init__(self, title = bytes(b"Hello"), width = 592, height = 460):
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

        self.updateLock = threading.Lock()
        self.renderLock = threading.Lock()
        #self.drawLock = threading.Lock()

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
        SDL_DestroyRenderer(self.m_renderer)
        SDL_DestroyWindow(self.m_window)
        print("~Deleted Window")

    def init(self):
        #os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.m_window = m_window = SDL_CreateWindow(self.m_title,
                              self.windowPos[0], self.windowPos[1],
                              self.m_width, self.m_height, self.m_windowFlags)
        SDL_HideWindow(m_window)
        
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK,
                                            SDL_GL_CONTEXT_PROFILE_CORE)
        
        self.context = SDL_GL_CreateContext(m_window)
        
        # -- SEt hit test rects here.
        if( m_window != 0 ):
            self.m_mouseFocus = True;
            self.m_keyboardFocus = True;

            # Create renderer for window.
            # windowsurface = SDL_GetWindowSurface(window)
            if self.mode == "RENDER":
                self.m_renderer = SDL_CreateRenderer( m_window, -1,
                    self.m_rendererFLags )

            elif self.mode == "DRAW":
                self.screenSurface = SDL_GetWindowSurface( m_window );
        
            elif self.mode == "OPENGL":
                pass
            
                #if self.screenSurface == None:
                 #   print(SDL_GetError())
            self.m_windowId = SDL_GetWindowID( m_window )
            self.m_shown = True;
            SDL_ShowWindow(m_window);

        SDL_SetWindowTitle(m_window, self.m_title)

        self.m_windowSurface = SDL_GetWindowSurface(m_window)

        #self.sp = Golem.property.BasicButton(self)
        #self.scene.add(self.sp)

        #theme = Golem.property.ButtonThemeFactory.genTheme(Golem.loadSurface("golem.png"), Golem.loadSurface("g1.png"))
        #self.sp.setTheme(theme)
        self.load()

    def load(self):
        pass

    def handleEvent(self, e):
        if( e.type == SDL_WINDOWEVENT ):
            if e.window.event == SDL_WINDOWEVENT_SHOWN:
                self.m_shown = True

            if e.window.event == SDL_WINDOWEVENT_HIDDEN:
                self.m_shown = False

            if e.window.event == SDL_WINDOWEVENT_SIZE_CHANGED:
                #Get new dimensions and repaint.
                #lock mutexes
                self.renderLock.acquire()
                self.updateLock.acquire()
                
                self.m_width = e.window.data1;
                self.m_height = e.window.data2;

                # Fixed the instance where the only operation for draw mode 
                # calls clearRenderer(). Added statements for render 
                # mode as well.
                if self.mode == "RENDER":
                    #self.m_windowSurface = SDL_GetWindowSurface(self.m_window)
                    self.clearRenderer()
                    #SDL_UpdateWindowSurface(self.m_window)
                
                if self.mode == "DRAW":
                    #self.m_windowSurface = SDL_GetWindowSurface(self.m_window)
                    self.clearScreen()
                    
                self.updateLock.release()
                self.renderLock.release()
                #unlock mutexes
                
            if e.window.event == SDL_WINDOWEVENT_EXPOSED:
                #Repaint on expose.
                #lock mutexes
                self.renderLock.acquire();
                if (self.mode == "RENDER"):
                    SDL_RenderPresent(self.m_renderer);
                else:
                    SDL_UpdateWindowSurface( self.m_window );
                self.renderLock.release();
                #unlock mutexes

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

                self.renderLock.acquire(); # First lock the render thread.
                self.updateLock.acquire(); # Second lock the update thread.

                self.m_window = None;
                self.m_renderer = None;
                self.m_closed = True;

                self.renderLock.release();
                self.updateLock.release();

    def update(self):
        """The application calls this in a thread in a loop."""
        pass

    def render(self):
        if (not self.isMinimized()):
            self.clearRenderer()

            self.scene.render();
            #self.sp.render()
#            SDL_RenderPresent( self.m_renderer );
            SDL_GL_SwapWindow(self.m_window)
            
        #self.screen.fill(self.screen_color)
        #self.UpdateEngine.draw(self.screen)
        #pygame.display.update()
#    def draw(self,):
#        if (not self.isMinimized()):
#            self.clearScreen()

#            self.scene.draw(self.screenSurface);

#            #Update the surface
#            SDL_UpdateWindowSurface( self.m_window );
#    # Threads.
    def updateThread(self):
        print("updateThread:: Started")

        while not self.isClosed():
            self.updateLock.acquire()

            self.update()

            self.updateLock.release()

        print("updateThread:: Stopped")

    def renderThread(self):
        print("renderThread:: Started")
        #clock = pygame.time.Clock()
        clock = Golem.time.Clock()

        while not self.isClosed():
            self.renderLock.acquire()

            self.render()

            self.renderLock.release()
            time.sleep(0)
        print("renderThread:: Stopped")

    def drawThread(self):
        """Calls the draw function"""
        print("drawThread:: Started")
        #clock = pygame.time.Clock()
        clock = Golem.time.Clock()

        while not self.isClosed():
            self.renderLock.acquire()

            self.draw()#self.screenSurface)

            self.renderLock.release()
            time.sleep(0.01) # 100 frames per second max
        print("drawThread:: Stopped")

    def clearRenderer(self):
        SDL_RenderClear( self.m_renderer )

    def clearScreen(self):
        #SDL_RenderClear( self.m_renderer )

        SDL_FillRect(self.screenSurface, None, SDL_MapRGB(self.screenSurface.contents.format, self.m_bgColor.r, self.m_bgColor.g, self.m_bgColor.b))

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
        print("Hiding window")

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
    def newWidget(self, classname, *params):
        return classname(self, *params)

    #def showAll(self):
        #os.environ['SDL_VIDEO_CENTERED'] = '1'

        #self.screen = pygame.display.set_mode(self.m_size, pygame.NOFRAME)
