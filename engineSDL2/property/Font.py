class Font():
    def __init__(self):
        self.m_size = 20
        self.m_bold = False
        self.m_italic = False
        self.m_underline = False
        self.m_strikethrough = False
        self.m_font = None
        
    @property
    def bold(self):
        return m_bold
    
    @property
    def italic(self):
        return m_italic
    
    @property
    def underline(self):
        return m_underline
    
    @property
    def strikethrough(self):
        return m_strikethrough
    
    @bold.setter
    def bold(self, boolean):
        self.m_bold = boolean
    
    @italic.setter
    def italic(self, boolean):
        self.m_italic = boolean
    
    @underline.setter
    def underline(self, boolean):
        self.m_underline = boolean
        
    @strikethrough.setter
    def strikethrough(self, boolean):
        self.m_strikethrough = boolean
    
    def TTF_SetFontStyle
