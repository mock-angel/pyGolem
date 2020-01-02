import time as t

#import Golem
from sdl2 import *
import sdl2
import sdl2.sdlimage
class time():
    class Clock():
        def __init__(self):
            self.m_tickSpeed = 0
            
            self.m_prevTime = t.time()
            self.m_currentTime = t.time()
            
            self.m_timeElapsed = 0
            
            self.m_frames = 0
            
        def setTickSpeed(self, FPS):
            self.m_tickSpeed = FPS
            
        def tick(self):
            
            
            self.m_currentTime = currT = t.time()
            self.m_timeSpent = currT - self.m_prevTime
            
            self.m_timeElapsed += self.m_timeSpent
            self.m_frames += 1
            
            if self.m_timeElapsed >= 1:
                self.m_timeElapsed = 0
                
                print ("Frames Per Second", self.m_frames)
                self.m_frames = 0
            
            self.m_prevTime = self.m_currentTime
            
            #if self.m_tickSpeed:
            #    pass

def loadSurfaceOptimised(windowSurface, path):
    #newTexture = SDL_Texture()
    
    bpath = path.encode()
    
    optimizedSurface = None
    
    loadedSurface = sdlimage.IMG_Load( bpath )
    
    if( loadedSurface == None ):
        print( "Unable to load image {}! SDL_image Error: ".format(bpath), IMG_GetError() );
    else:
        #Convert surface to screen format
        optimizedSurface = SDL_ConvertSurface( loadedSurface, t_screenSurface.format, 0 );
        if( optimizedSurface == None ):
            printf( "Unable to optimize image {}! SDL Error: ".format(bpath), SDL_GetError() );
            
        #Get rid of old loaded surface
        SDL_FreeSurface( loadedSurface );

    return optimizedSurface;
    
    
def loadSurface(path):
    #newTexture = SDL_Texture()
    
    bpath = path.encode()
    
    loadedSurface = sdlimage.IMG_Load( bpath )
    print (loadedSurface, bpath)
    #exit()
    if loadedSurface == None :
        print ("Unable to load surface from path :", bpath)
    
    return loadedSurface
    
    
def loadTexture(t_renderer, path):
    #newTexture = SDL_Texture()
    
    bpath = path.encode()
    
    newTexture = None
    
    loadedSurface = sdlimage.IMG_Load( bpath )
    if loadedSurface:
        newTexture = SDL_CreateTextureFromSurface( t_renderer, loadedSurface )
        
        if not newTexture:
            print("Unable to create texture from {}! SDL Error: {}".format(bpath.c_str(), SDL_GetError()) )
            
        SDL_FreeSurface( loadedSurface )
        
    return newTexture

def create_new_surface(size = (1, 1), name = None, color = (189, 189, 189)):# TODO: Change default args.
    #newTexture = SDL_Texture()
    width = size[0]
    height = size[1]
    
    if SDL_BYTEORDER == SDL_BIG_ENDIAN:
        rmask = 0xff000000;
        gmask = 0x00ff0000;
        bmask = 0x0000ff00;
        amask = 0x000000ff;
    else:
        rmask = 0x000000ff;
        gmask = 0x0000ff00;
        bmask = 0x00ff0000;
        amask = 0xff000000;

    
    newSurface = SDL_CreateRGBSurface(0, width, height, 32,
                                   rmask, gmask, bmask, amask)
    #SDL_FillRect(newSurface, 0, color);
    print(SDL_MapRGB(newSurface.contents.format , color[0], color[1], color[2]))
    SDL_FillRect(newSurface, SDL_Rect(0,0,100,100), SDL_MapRGB(newSurface.contents.format , color[0], color[1], color[2]));
    return newSurface


        
