from Rect import Rect

class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def isCollided(self, t_rect):
        x, y = self.x, self.y
        return False if((x<t_rect.x) or (y<t_rect.y) or (x>(t_rect.w + t_rect.x)) or (y>(t_rect.h + t_rect.y)) ) else True
