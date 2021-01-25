import pygame
from arka_settings import *
import random

class Ball():
    
    def __init__(self, parent):
        
        self.surface = parent
        self.image = pygame.image.load("assets/ball.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (SCR_WIDTH//2, MARGIN_BOTTOM - (3*BLK_HEIGHT)))
        
        self.speed = 12
        self.direction = None # None the ball is not moving, -1 the ball goes UP, 1 the ball goes DOWN, -2 out of borders
        self.angle_x = -3
        
    def reset_ball(self):
        self.speed = 10
        self.direction = None
        self.angle_x = 1
        self.rect = self.image.get_rect(midbottom = (SCR_WIDTH//2, MARGIN_BOTTOM - (3*BLK_HEIGHT)))
       
    def draw_ball(self):
        self.surface.blit(self.image, self.rect)
        
    def launch_ball(self):
        self.direction = -1
        
    def calculate_position(self):
        self.rect.y += (self.speed * self.direction)
        self.rect.x += self.angle_x
        self.check_boundaries()
        self.speed = 15 if self.speed > 15 else self.speed 
    
    def check_boundaries(self):       
        # check Left and Right
        if self.rect.left < MARGIN_LEFT:
            self.rect.left = MARGIN_LEFT
            self.angle_x = self.angle_x * -1
            self.speed += 1
        
        if self.rect.right > MARGIN_RIGHT:
            self.rect.right = MARGIN_RIGHT
            self.angle_x = self.angle_x * -1
            self.speed += 1
             
        # check Top and Bottom
        if self.rect.top < MARGIN_TOP:
            self.rect.y = MARGIN_TOP
            self.direction = 1
            self.speed += 1
            
        elif self.rect.bottom > MARGIN_BOTTOM:
            self.direction = -2
            
    def check_ball_collisions(self, block_list):
        # Something is still not good, sometimes ball does strange things
        for block in block_list:
            
            if self.rect.colliderect(block.rect):
                self.angle_x += random.choice([-1,0,-2]) if self.angle_x < 0 else random.choice([1,0,2])
                self.angle_x = 15 if self.angle_x > 15 else -15 if self.angle_x < -15 else self.angle_x
        
                if (
                    self.rect.collidepoint(block.rect.topright) or 
                    self.rect.collidepoint(block.rect.bottomright) or
                    self.rect.collidepoint(block.rect.topleft) or
                    self.rect.collidepoint(block.rect.bottomleft)
                    ):
                    self.direction *= -1
                    self.speed += 1
                    return [block.block_transition(), block]
            
                # HIT FROM TOP OR BOTTOM
                elif self.rect.collidepoint(block.rect.midbottom) or self.rect.collidepoint(block.rect.midtop):  
                    self.direction *= -1
                    self.speed += 1
                    return [block.block_transition(), block]
            
                # HIT FROM SIDE
                elif self.rect.collidepoint(block.rect.midleft) or self.rect.collidepoint(block.rect.midright):
                    self.angle_x *= -1
                    self.speed += 1
                    return [block.block_transition(), block]
                
                else:
                    self.direction *= -1
                    self.speed += 1
                    return [block.block_transition(), block]
        return "miss", False