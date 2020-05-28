import math

class Map():
    def __init__(self):
        pass
    
    
class Builder():
    def __init__(self):
        pass
    
    def add_point_list(self, _li):
        m = Map()
        for rtheta in _li
            r, theta = rtheta
            x = r * math.cos(math.radians(theta))
            y = r * math.sin(math.radians(theta))
            
            m.add(x, y, r, theta)
    def process(self):
        pass
    
    
