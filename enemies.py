import pygame
from arka_settings import *
import random

class EvilBubbles():
    def __init__(self, parent, position):
        self.surface = parent
        enemytype = random.choice(["a","b"])
        self.images = [
            pygame.image.load(f"assets/enemy_{enemytype}_01.png").convert_alpha(),
            pygame.image.load(f"assets/enemy_{enemytype}_02.png").convert_alpha(),
            pygame.image.load(f"assets/enemy_{enemytype}_03.png").convert_alpha(),
            pygame.image.load(f"assets/enemy_{enemytype}_04.png").convert_alpha(),
            pygame.image.load(f"assets/enemy_{enemytype}_05.png").convert_alpha(),
            pygame.image.load(f"assets/enemy_{enemytype}_06.png").convert_alpha(),
            pygame.image.load(f"assets/enemy_{enemytype}_07.png").convert_alpha(),
            pygame.image.load(f"assets/enemy_{enemytype}_08.png").convert_alpha(),
            ]
        self.x, self.y = position
        self.timer = 0
        self.wait = 0
        self.vdirection = 3
        self.hdirection = random.choice(range(-3,3))
        self.image=self.images[0]
        self.draw_enemy()
    
    def draw_enemy(self):
        self.wait += 1
        if self.wait == 5:
            self.wait = 0
            self.timer += 1
            if self.timer > 8:
                self.timer = 0
            self.image = self.images[self.timer%8]
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.surface.blit(self.image, self.rect)
        
    
    def move_enemy(self):
        if self.rect.left < MARGIN_LEFT:
            self.rect.left = MARGIN_LEFT+1
            self.hdirection *= -1
        if self.rect.right > MARGIN_RIGHT:
            self.rect.right = MARGIN_RIGHT-1
            self.hdirection *= -1
        if self.rect.top <= MARGIN_TOP:
            self.vdirection *= -1
            self.rect.top = MARGIN_TOP+1
        self.y = self.rect.y + self.vdirection 
        self.x = self.rect.x + self.hdirection + random.choice(range(-2,0) if self.hdirection < 1 else range(0,2))
        self.draw_enemy()
    
    def check_collisions(self, block_list, ball_list, platform, lasers):
        self.move_enemy()
        if self.rect.bottom >= MARGIN_BOTTOM:
            return "out_screen"
        for ball in ball_list:
            if self.rect.colliderect(ball.rect):
                ball.direction *= -1
                self.draw_enemy()
                return "hit_ball"
        for block in block_list:
            if self.rect.colliderect(block.rect):
                if self.rect.bottom >= block.rect.top:
                    self.rect.bottom = block.rect.top-1
                elif self.rect.top <= block.rect.bottom:
                    self.rect.top = block.rect.bottom+1
                self.vdirection *= -1
                self.hdirection *= -1
                return "hit_block"
        for laser in lasers:
            if self.rect.colliderect(laser.rect):
                return "hit_laser"
        if self.rect.colliderect(platform.rect):
            return "hit_platform"
        return "nothing"