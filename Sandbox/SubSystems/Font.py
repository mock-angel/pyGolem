class FontSubsystem():
    def __init__(self):
        self.font_res_data = None
        self.fonts_data = None
        
    def load_json_font(self, data):
        self.font_res_data = data["font_res"]
        self.fonts_data = data["font"]
        
        for font_name in self.fonts_data:
            font_data = self.fonts_data[font_key]
            
            font_res = font_data["font_res"]
            size = font_data["size"]
            bold = font_data["bold"]
            italic = font_data["italic"]
            strikethrough = font_data["strikethrough"]
            self.font_dict[font_name] = Font()
            
    def get_font(self, font_name):
        return self.dont_dict[font_name]
