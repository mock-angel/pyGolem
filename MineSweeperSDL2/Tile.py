#Tile.py
import Golem
from nonGraphics import *
from TileEssentials import  MineImages

RED_FLAG = 1
BLUE_FLAG= 2
NO_FLAG = 3

class GameScene(Golem.property.Scene):
    def __init__(self, t_window):
        Golem.property.Scene.__init__(self, t_window)
        
        self.paused = False
        self.field = MinesField()

        self.button_group = Golem.property.ButtonGroup()
        self.tile_res = MineImages()

        # game settings default.
        self.set_size((8, 8))
        self.flag_count = 0
        self.set_mines(10)
        
        self.uncovered_list = Golem.property.ButtonGroup()

        p = self.pause_screen = Golem.Surface((1, 1)).convert()
        p.blit(1)
        
        print (self.pause_screen.contents, "hello there.......")
        self.pause_screen_rect = self.pause_screen.get_rect()

    def load(self):
        self.tile_res.load_surfaces()

#        self.flag_count_text = TextLine()
#        self.flag_count_text.lable = "flag_count"
#        self.flag_count_text.font_size = 22
#        self.flag_count_text.text_color = (75, 75, 75)
#        self.flag_count_text.text = "10"

    def set_mines(self, mine_count):
        self.mine_count = mine_count

    def generate_tiles(self, size, mine_count):
        self.set_size(size)
        self.set_mines(mine_count)
        self.reset()
        s_r, s_c = size

        print ("Generating graphic tiles ", s_r, '*', s_c, '-', mine_count)

        # LOCK SPRITE
        for r in range(s_r):
          for c in range(s_c):
            tile = Tile(self.panel, (r, c), self.tile_res, self)
            self.button_group.add(tile)

        self.adjust_option_button_placement()
        self.add(self.buffer_group)
        self.buffer_group.empty()
        # UNLOCK

        #ghost_tile = self.ghost_tile
        #ghost_tile.set_pos((0, 0))
        #x, y = ghost_tile.rect.x, ghost_tile.rect.y

        #ghost_tile.set_pos((self.size[0] - 1, self.size[1] - 1))
        #mwidth = ghost_tile.rect.x + ghost_tile.rect.width - x
        #mheight = ghost_tile.rect.y + ghost_tile.rect.height - y
        #self.pause.ready = True
        #self.pause_screen = pygame.Surface((mwidth, mheight))
        #self.pause_screen_rect = pygame.Rect((x, y, mwidth, mheight))
        #self.pause_screen_rect.x = x
        #self.pause_screen_rect.y = y
        #self.pause_screen_rect.width = mwidth
        #self.pause_screen_rect.height = mheight
        print ("DONE")

    def set_size(self, size):
        self.m_size = size

    def is_paused(self):
        return self.paused

    def tile_touched(self, tile):
        pass

    def tile_blown(self, tile):
        pass


class Tile(Golem.property.BasicButton):
    def __init__(self, pos, tile_res, mine_board):
        Golem.property.BasicButton.__init__(self)
        
        self.clicked(touched)
        self.color_number = 0

        self.con = "normal" #won/lost
        self.vis = "covered" # uncovered #stage

        self.mine_board = mine_board

    def adjust_rect(self):
        r, c = self.pos
        offset_x, offset_y = OFFSET_XY = 20, 130
        self.rect.x = (c * self.rect.width) + offset_x
        self.rect.y = (r * self.rect.height) + offset_y



    def touched(self):
        # Called when player touched.
        if self.mine_board.is_paused(): return

        # Red flags do nothing.

        if self.flag == RED_FLAG:
            return

        if self.vis == "uncovered" or self.con == "lost":
            return

        if not(self.color_number == MINES):
            self.mine_board.tile_touched(self)

            self.uncover_tile()
        else:

            print ("Stepped on a mine at : ", self.pos)
            self.mine_board.tile_blown(self)

    def explode(self):
        pass

    def uncover_tile(self):
        if self.flag == RED_FLAG:
            return

        # TODO: Merge these two - self.color_number in ("13", "12")
        if self.color_number == "13":
#            self.con = "lost"
            return

        elif self.color_number == "12":
            return

        self.vis = "uncovered"
        self.flag = NO_FLAG

        self.refresh_theme()

    def pop_tile(self):
        # Called when game is lost.
        self.con = "lost"

        if self.flag == RED_FLAG and (self.color_number == "13"):
            self.theme = self.flag_template["flag"][self.con]
            return

        elif self.flag == RED_FLAG and not (self.color_number == "13"):
            self.theme = self.flag_template["incorrect"][self.con]
            return

        elif self.flag == BLUE_FLAG and not (self.color_number == "13"):
            self.theme = self.flag_template["maybe"][self.con]
            return

        elif self.flag == BLUE_FLAG and (self.color_number == "13"):
            self.flag = NO_FLAG

        if self.color_number in ("13", "12"):

            self.vis = "uncovered"

    def flag(self):
        # called everytime flag is announced.
        theme = None

        if self.vis == "uncovered" or self.condition == "lost":
            return

        if self.flag == NO_FLAG:
            self.flag = RED_FLAG
            self.mine_board.flag_added()
            theme = self.flag_template["flag"][self.con]

        elif self.flag == RED_FLAG:
            self.flag = BLUE_FLAG
            self.mine_board.flag_removed()
            theme = self.flag_template["maybe"][self.con]

        elif self.flag == BLUE_FLAG:
            self.flag = NO_FLAG
            theme = self.tile_template[self.con][self.vis]

        self.theme = theme

        self.adjust_rect()
