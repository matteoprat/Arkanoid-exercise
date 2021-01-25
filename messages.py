import pygame
from arka_settings import *

FONT_YELLOW = (219, 236, 34)
FONT_WHITE = (255, 255, 255)
FONT_RED = (255,0,0)

class Messages():
    
    def __init__(self, parent):
        self.font = pygame.font.SysFont("arial", 20)
        self.surface = parent
        self.screen_width = SCR_WIDTH
        self.screen_height = SCR_HEIGHT
        
    def display_info(self, level, lives, score):
        
        label_level = self.font.render("level: ", True, FONT_WHITE)
        self.surface.blit(label_level, (52,21))
        label_nlevel = self.font.render(f"{level}", True, FONT_RED)
        self.surface.blit(label_nlevel, (52+label_level.get_width(),21))
        
        label_lives = self.font.render("lives: ", True, FONT_WHITE)
        self.surface.blit(label_lives, (222,21))
        label_nlives = self.font.render(f"{lives}", True, FONT_RED)
        self.surface.blit(label_nlives, (222 + label_lives.get_width() ,21))
        
        label_score = self.font.render("score: ", True, FONT_WHITE)
        self.surface.blit(label_score, (450,21))
        label_nscore = self.font.render(f"{score}", True, FONT_YELLOW)
        self.surface.blit(label_nscore, (450 + label_score.get_width(),21))
    
    def display_pause(self):
        line1 = self.font.render(f"Game paused.", True, FONT_YELLOW)
        self._label_centered(line1, (500))
        line2 = self.font.render("Press <p> to resume. <Esc> to exit the game!", True, FONT_YELLOW)
        self._label_centered(line2, (590))
    
    def display_level(self, stage):
        line1 = self.font.render(f"STAGE {stage}", True, FONT_WHITE)
        self._label_centered(line1, (MARGIN_BOTTOM-(BLK_HEIGHT*9)))

    def level_completed(self, score):   
        line1 = self.font.render(f"Congratulations! Level completed with score: {score}", True, FONT_WHITE)
        self._label_centered(line1, (500))
        line2 = self.font.render("Press [ENTER] to play next level. [ESC] to exit the game!", True, FONT_WHITE)
        self._label_centered(line2, (590))
    
    def _label_centered(self, text, y):
        w = text.get_width()
        self.surface.blit(text, ((self.screen_width//2) - (w//2), y))
    
    def _label_left(self, text, x, y):
        w = text.get_width()
        self.surface.blit(text, (x+w, y))
        
    def _label_right(self, text, x, y):
        w = text.get_width()
        self.surface.blit(text, (x-w, y))
            
    def intro_text(self, text, ypos):
        bigfont = pygame.font.SysFont("arial", 30)
        line = bigfont.render(text, True, FONT_WHITE)
        self._label_centered(line, ypos)
        
    def intro_text_small(self, text, ypos):
        bigfont = pygame.font.SysFont("arial", 18)
        line = bigfont.render(text, True, FONT_WHITE)
        self._label_centered(line, ypos)
    
    def highscore_input(self, text, x, y):
        line = self.font.render(text,True, FONT_WHITE)
        self.surface.blit(line, (x, y))
        
    def highscore(self,ranking):
        bigfont = pygame.font.Font("fonts/unispace_rg.ttf", 22)
        distance = 37
        for i, rank in enumerate(ranking):
            
            bgrank = pygame.image.load(f"assets/highscores/{i}.png").convert_alpha()
            self.surface.blit(bgrank, (22, 312+(distance*i)+28))
            col1 = bigfont.render(f"{i+1}.", True, FONT_WHITE)
            col2 = bigfont.render(f"{rank[0]}", True, FONT_WHITE)
            col3 = bigfont.render(f"{int(rank[1]):,}", True, FONT_WHITE)
            col4 = bigfont.render(f"{rank[2]}", True, FONT_WHITE)
            self._label_right(col1, 85, 342+(distance*i))
            self._label_left(col2, 195, 342+(distance*i))
            self._label_right(col3, 500, 342+(distance*i))
            self._label_right(col4, 636, 342+(distance*i))