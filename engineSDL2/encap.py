import time as t

from sdl2 import *
import sdl2
import sdl2.sdlimage

import Golem

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
    
    Golem.Surface.wrap(newSurface)
    
    return optimizedSurface;
    
    
def loadSurface(path):
    #newTexture = SDL_Texture()
    
    bpath = path.encode()
    
    loadedSurface = sdlimage.IMG_Load( bpath )
    print (loadedSurface, bpath)
    #exit()
    if loadedSurface == None :
        print ("Unable to load surface from path :", bpath)
    
#    else:
#        loadedSurface
        
    Golem.Surface.wrap(loadedSurface)
    
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
    
    #Golem.Texture.wrap(newSurface)
    
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
    if (newSurface == None):
        print(SDL_GetError())
    #SDL_FillRect(newSurface, 0, color);
    print(SDL_MapRGB(newSurface.contents.format , color[0], color[1], color[2]))
    SDL_FillRect(newSurface, None, SDL_MapRGB(newSurface.contents.format , color[0], color[1], color[2]));
    
    # THis is where we bind to a golemsurface.
    Golem.Surface.wrap(newSurface)
    
    return newSurface

#def SDL_ScaleSurface(surface, width, height):
#    #SDL_ScaleSurface(surface, width, height);
#    if(!Surface || !Width || !Height)
#        return 0;
#    
#    _ret = SDL_CreateRGBSurface(surface.contents.flags, width, height, surface.contents.format.BitsPerPixel,
#        contents.format.Rmask, contents.format.Gmask, contents.format.Bmask, contents.format.Amask);
#        
#    _stretch_factor_x = (static_cast<double>(Width)  / static_cast<double>(Surface->w)),
#        _stretch_factor_y = (static_cast<double>(Height) / static_cast<double>(Surface->h));
    
#    for(Sint32 y = 0; y < Surface->h; y++) //Run across all Y pixels.
#        for(Sint32 x = 0; x < Surface->w; x++) //Run across all X pixels.
#            for(Sint32 o_y = 0; o_y < _stretch_factor_y; ++o_y) //Draw _stretch_factor_y pixels for each Y pixel.
#                for(Sint32 o_x = 0; o_x < _stretch_factor_x; ++o_x) //Draw _stretch_factor_x pixels for each X pixel.
#                    DrawPixel(_ret, static_cast<Sint32>(_stretch_factor_x * x) + o_x, 
#                        static_cast<Sint32>(_stretch_factor_y * y) + o_y, ReadPixel(Surface, x, y));
