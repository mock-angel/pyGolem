import json

class JsonParser():
    def __init__(self):
        self.path = "engine.json"
        
        self.data = None
        self.load()
    
    def load(self):
        with open(self.path) as json_file:
            self.data = json.load(json_file)
        print(self.data)

