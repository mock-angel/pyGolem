# Containers
class Tab():
    def __init__(self):
        pass

class TabContainer():
    def __init__(self):
        pass
    
    def add_tab(self, tab):
        pass
    
    def create_tab(self, tab_class = Tab, *params):
        if len(params):
            tab_class(*params)
        
        else:
            tab_class()
        
class GameView(Golem.TabContainer):
    def __init__(self):
        Golem.TabContainer.__init__(self)

