import pygame
import math
from arka_settings import *
import random

class Platform():
    def __init__(self, parent):
        
        self.surface = parent
        self.image = pygame.image.load("assets/bar.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (SCR_WIDTH//2, MARGIN_BOTTOM - (2*BLK_HEIGHT)))
        self.magnet = 0 
    
    def reset_platform(self):
        self.image = pygame.image.load("assets/bar.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (SCR_WIDTH//2, MARGIN_BOTTOM - (2*BLK_HEIGHT)))
        self.magnet = 0
    
    def magnet_activate_platform(self):
        self.image = pygame.image.load("assets/bar_magnet.png").convert_alpha()
        self.rect = self.image.get_rect(center = (self.rect.center))
    
    def laser_activate_platform(self):
        self.image = pygame.image.load("assets/bar_laser.png").convert_alpha()
        self.rect = self.image.get_rect(center = (self.rect.center))
        
    def enlarge_activate_platform(self):
        self.image = pygame.image.load("assets/bar_enlarge.png").convert_alpha()
        self.rect = self.image.get_rect(center = (self.rect.center))
    
    def powerup_deactivate_platform(self):
        self.image = pygame.image.load("assets/bar.png").convert_alpha()
        self.rect = self.image.get_rect(center = (self.rect.center))
    
    def draw_platform(self):
        self.surface.blit(self.image, self.rect)
    
    def move_left(self):
        self.rect.x = self.rect.x - 4 if self.rect.x - 4 > MARGIN_LEFT else MARGIN_LEFT
        self.draw_platform()
    
    def move_right(self):
        self.rect.x = self.rect.x + 4 if self.rect.right + 4 < MARGIN_RIGHT else MARGIN_RIGHT - self.rect.width
        self.draw_platform()
    
    def calc_angle(self, ball):
        # Not very convinced about this thing, to check in the future
        max_angle = 8
        point_of_collision = ball.rect.centerx - self.rect.centerx
        mid = (self.rect.width // 2) + abs(point_of_collision)
        ball.angle_x = int(max_angle*(mid/self.rect.width))
        #print(point_of_collision, mid, ball.angle_x, self.rect.width)
        #if point_of_collision <= self.rect.width//2:
        if point_of_collision <= 0:
            ball.angle_x = ball.angle_x * -1 + random.choice([-2,-1,0,1,2])
        else:
            ball.angle_x = ball.angle_x + random.choice([-2,-1,0,1,2])
    
    def check_plaftorm_collision(self, ball):
        if self.magnet == 1:
            if self.rect.colliderect(ball.rect) and abs(ball.rect.bottom - self.rect.top) >= ball.rect.height:
                ball.direction = None
                ball.rect.bottom = self.rect.top
                ball.speed = 10
                ball.angle_x = 1
                return True
        if self.rect.colliderect(ball.rect) and abs(ball.rect.bottom - self.rect.top) >= ball.rect.height:   
            ball.direction = -1
            ball.rect.bottom = self.rect.top
            self.calc_angle(ball)
            return True
        return False