src_default = "data/themes/bgcolors/Tile/"

tile_size = (64, 64)
tile_number_size = (21*2, 21*2)

def scale(surf, size):
    golem.create_new_surface(size)
class MineImages():
    def __init__(self):
        
        self.generated = False
        self.tile_info = dict()
        self.default_colors = dict()
        
    
    def load_surfaces(self, t_tile_size = (32, 32), t_number_size = (32, 32)):
        self.tile_size = t_tile_size
        self.number_size = t_number_size
        
        frame = golem.create_new_surface(src_default + "frame.png")
        
        self.tile_info = {
            
            "TILEFRAME" : scale(golem.loadSurface(src_default + "frame.png"), tile_size),
            "held_tile_alpha" : scale(golem.loadSurface(src_default + "held_alpha.png"), tile_size),
            "covered_lost" : (136, 138, 133),
            "uncovered_lost" : ( 222, 222, 220),
            "default_covered" : ( 186, 189, 182),
            "default_uncovered" : ( 222, 222, 220),
            "default_hover" : ( 211, 215, 207),
        }
        
        self.held_alpha = scale(self.tile_info["held_tile_alpha"], tile_size)
        
        #load Flags.
        #########################################################
        self.flag_raw = dict()
        
        self.flag_raw["incorrect"] = golem.loadSurface(src_default + "incorrect.png")
        
        self.flag_raw["flag"] = golem.loadSurface(src_default + "flag.png")
        
        self.flag_raw["maybe"] = golem.loadSurface(src_default + "maybe.png")
        
        #Load Mines raw .
        #########################################################
        self.mine_raw = dict()
        self.mine_raw["mine"] = golem.loadSurface(src_default + "mine.png")
        
        self.mine_raw["exploded"] = golem.loadSurface(src_default + "exploded.png")
        
        
        #load colored numbers raw.
        #########################################################
        self.colored_numbers_raw = dict()
        self.colored_numbers_raw["1"] = golem.loadSurface(src_default + "1mines.png")
        
        self.colored_numbers_raw["2"] = golem.loadSurface(src_default + "2mines.png")
        
        self.colored_numbers_raw["3"] = golem.loadSurface(src_default + "3mines.png")
        
        self.colored_numbers_raw["4"] = golem.loadSurface(src_default + "4mines.png")
        
        self.colored_numbers_raw["5"] = golem.loadSurface(src_default + "5mines.png")
        
        self.colored_numbers_raw["6"] = golem.loadSurface(src_default + "6mines.png")
        
        self.colored_numbers_raw["7"] = golem.loadSurface(src_default + "7mines.png")
        
        self.colored_numbers_raw["8"] = golem.loadSurface(src_default + "8mines.png")
        
        self.colored_numbers_raw["13"] = golem.loadSurface(src_default + "mine.png")
        
        self.colored_numbers_raw["12"] = golem.loadSurface(src_default + "exploded.png")
        
        # generate flag template(set of themes.)
        #########################################################
        self.flag_template_collection_unscaled = dict()
        
        for key in self.flag_raw:
            self.flag_template_collection_unscaled[key] = self.gen_template(scale(self.flag_raw[key], tile_number_size).convert_alpha())
        
        self.mine_template_unscaled = dict()
    
    def gen_template(self, t_surf):
        
        r = t_surf.get_rect()
        r.center = tile_size[0]/2, tile_size[1]/2
        
        pos =  r.x, r.y
        
        surf = pygame.Surface(tile_size)
        frame_surf = self.tile_info["TILEFRAME"]
        
        u_default, u_hover, u_held = surf.copy(), surf.copy(), surf.copy()
        u_default.fill(self.tile_info["default_covered"])
        u_default.blit(t_surf, pos)
        u_default.blit(frame_surf, (0, 0))
        u_hover.fill(self.tile_info["default_hover"])
        u_hover.blit(t_surf, pos)
        u_hover.blit(frame_surf, (0, 0)) 
        u_held.fill(self.tile_info["default_hover"])
        u_held.blit(t_surf, pos)
        u_held.blit(frame_surf, (0, 0))
        u_held.blit(self.held_alpha, (0, 0))
        
        norm = create_button_theme(u_default, u_hover, u_held)
        
        v_default, v_hover, v_held = surf.copy(), surf.copy(), surf.copy()
        v_default.fill(self.tile_info["covered_lost"])
        v_default.blit(t_surf, pos)
        v_default.blit(frame_surf, (0, 0))
        v_hover.fill(self.tile_info["covered_lost"])
        v_hover.blit(t_surf, pos)
        v_hover.blit(frame_surf, (0, 0)) 
        v_held.fill(self.tile_info["covered_lost"])
        v_held.blit(t_surf, pos)
        v_held.blit(frame_surf, (0, 0))
        v_held.blit(self.held_alpha, (0, 0))
        
        norm = create_button_theme(u_default, u_hover, u_held)
        lost = create_button_theme(v_default, v_hover, v_held)
        
        return {
            "norm" : norm,
            "lost" : lost,
        }
