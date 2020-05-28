
from sdl2 import *

def rect(renderer, color, rect, width=0):
    SDL_RenderDrawRect(renderer, rect)

def polygon(renderer, color, points, width=0):
    for i, end_pos in enumerate(points):
        start_pos = points[i - 1]
        line(renderer, color, start_pos, end_pos, width) # only temporary
        #SDL_RenderDrawLine(renderer, start_pos[0], start_pos[1], end_pos[0], end_pos[1]);

def line(renderer, color, start_pos, end_pos, width = 1):
    SDL_RenderDrawLine(renderer, start_pos[0], start_pos[1], end_pos[0], end_pos[1]);

def circle(renderer, color, center, radius, width=0):
    cx, cy = center
