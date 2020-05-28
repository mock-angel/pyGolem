class Color(object):
    def __init__(self, r = 0, g = 0, b = 0, a = 0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

class World():
    def __init__(self):
        """
            load()
                loading assets the game world required.
            
            draw()
                draw on surface
            render()
                render to render_target
        """
#        self.scenes = None
        
        #self.window = None
        #self.render_target = None
        
    def __del__(self):
        pass
    
    def draw(self, surface):
        pass
    
    def render(self):
        pass
