import sys
import ctypes
from sdl2 import *
import sdl2
import sdl2.ext

from threading import Thread

import Golem

class LockGuard():
    def __init__(self, lockObj):
        self.m_lockObj = lockObj
        lockObj.acquire()
    
    def __del__(self):
        self.m_lockObj.release()
    

class Application():
    def __init__(self):
        self.m_windowsMap = {}
        self.experi_window = None
        self.m_threads = []
        
        SDL_Init(SDL_INIT_VIDEO)
    
    def __del__(self):
        SDL_Quit()
    
    def createNewWindow(self, title = "", window = None):
        new_window = Golem.Window() if not window else window()
        new_window.init()
        self.m_windowsMap[new_window.getWindowId()] = new_window
        
        t_update = Thread(target=new_window.updateThread, args=() )
        t_update.start()
        self.m_threads.append(t_update)
        
        if new_window.mode == "RENDER":
            t_render = Thread(target=new_window.renderThread, args=() )
            t_render.start()
            self.m_threads.append(t_render)
        elif new_window.mode == "DRAW":
            t_render = Thread(target=new_window.drawThread, args=() )
            t_render.start()
            self.m_threads.append(t_render)
        
        self.m_threads.append(t_update)
        
        
        return new_window
        
    def wait_till_thread_closed(self):
        for thread in self.m_threads:
            thread.join()
            
    def start(self):
        
        self.eventThread()
        self.wait_till_thread_closed()
    
    def eventThread(self): # Doesnt use sdl2.ext module because this is faster.
        #if experi_window.isClosed():
        #    pass
        e = event = SDL_Event()
        win = None
        
        while len(self.m_windowsMap)!=0 and SDL_WaitEvent(ctypes.byref(event)) != 0:
        
            if(e.window.windowID in self.m_windowsMap):
                win = self.m_windowsMap[e.window.windowID]
                if e.type == SDL_MOUSEMOTION:
                    win.m_mouse.x = e.motion.x
                    win.m_mouse.y = e.motion.y
                    #print("%d , %d\n", e.motion.x, e.motion.y)
                    
                    
                #if event.type == KEYDOWN and event.key == K_ESCAPE:#Normal escape route.
                    #experi_win.m_closed = True
                    #return
                    
                win.handleEvent(e);
                self.handleSpriteEvent(win, e)
                #win.scene.handleEvent(e)
            else:
                print("eventThread: Event does not belong to any existing window");
            
            idKeys = list(self.m_windowsMap.keys())
            for windowID in idKeys:
                if self.m_windowsMap[windowID].isClosed():
                    self.m_windowsMap.pop(windowID)
                    
    def handleSpriteEvent(self, w, e):
        #w = self.m_windowsMap[e.window.windowID];
        #w.scenes.m_containerLock.lock();
        #locked = LockGuard
        
        if e.type == SDL_MOUSEMOTION:
            sprites = w.sprites();
            for spr in sprites:
                if (spr.m_mouseOver): # If entered before.
                    # event is onHover() if mouse still inside rectangle.
                    if ( w.m_mouse.isCollided(spr.m_rect) ):
                        if spr.m_pressed: spr.onPressed()# call onDrag from here.
                        else: spr.onHover()
                    else:
                        # NOTE: spr.m_pressed should not be changed if you
                        # intend to let the user perform the 
                        spr.m_pressed = False 
                        
                        spr.m_mouseOver = False
                        spr.onLeave()
                    
                elif ( w.m_mouse.isCollided(spr.m_rect) ):
                    # "onEnter" if first collided.
                    spr.m_mouseOver = True
                    spr.onEnter()
            #print("Mouvement to {}, {}".format(w.m_mouse.x, w.m_mouse.y))
            return
            
        if e.type == SDL_MOUSEBUTTONDOWN:
            sprites = w.sprites();
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
            sprites = w.sprites();
            if (e.button.button == SDL_BUTTON_LEFT):
                for spr in sprites:
                    if ( spr.m_pressed ):
                        if ( w.m_mouse.isCollided(spr.m_rect) ):
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
            
'''
def messageBox(app, title, message):
    pass
    

def createWindow(window_name, size_r = 400, size_c = 400):
    window = Window("", 400, 400)
    return window
'''
