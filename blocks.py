import pygame
import random

class Block():
    
    def __init__(self, parent, data, position, color):
        self.surface = parent
        self.color = color
        self.image, self.hit, self.score = data
        self.rect = self.image.get_rect(topleft=position)
        self.powerup = random.choice([False, False, False, False, False, False, False, False, False,  True]) # 20% to have a powerup
    
    def draw_block(self):
        self.surface.blit(self.image, self.rect)
        
    def block_transition(self):
        if self.color != "G":
            self.hit -= 1
        if self.hit == 0:
            return "destroy"
        return "redraw"