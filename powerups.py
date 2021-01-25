import pygame
import ball_class
import screens
from arka_settings import *


class PowerUp():
    
    def __init__(self, parent, name, x, y):
        
        self.surface = parent
        self.unit_duration = 30
        self.duration = 5 # duration = 30 * number of seconds the power-up will last
        self.active = False
        self.type = name
        self.image = pygame.image.load(f"assets/powerup_{self.type}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft =(x,y))
        # position when the power-up fall down
        self.y_speed = 8
        self.y = y
        self.x = x
        self.maxtime = self.duration * self.unit_duration
        self.time_left = self.maxtime
    
    def draw_powerup(self):
        self.surface.blit(self.image, self.rect)
    
    def powerup_falling(self):
        self.rect.y += self.y_speed
        if self.rect.bottom >= MARGIN_BOTTOM:
            del self
        else:
            self.draw_powerup()
    
class Laser():
    def __init__(self, parent, midbottom_):
        self.surface = parent
        self.image = pygame.image.load("assets/lasers.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = midbottom_)
        self.y_speed = 15
    
    def laser_move(self):
        self.rect.y -= self.y_speed
        
    def draw_laser(self):
        self.surface.blit(self.image, self.rect)
        
    def check_block_collision(self, block_list):
        action = ""
        for block in block_list:
            if self.rect.colliderect(block.rect):
                action = block.block_transition()
                return action,block
        return False, False
        
def handle_powerup(powerup, game):
        
        if powerup.type == "1up":
            game.check_bonus_lives(powerup=True)
            game.powerup_active.remove(powerup)
            del powerup
        
        elif powerup.type == "skip":
            game.powerup_active.remove(powerup)
            game.block_left = 0
            del powerup
            
        elif powerup.type == "speeddown":
            game.powerup_active.remove(powerup)
            for ball in game.balls:
                ball.speed = 10
            del powerup
        
        elif powerup.type == "balls":
            if (len(game.balls)<1):
                game.powerup_active.remove(powerup)
                del powerup
            else:
                extra1 = ball_class.Ball(game.surface)
                extra1.direction = game.balls[0].direction * -1
                extra1.angle_x = game.balls[0].angle_x
                extra1.rect.x = game.balls[0].rect.x
                extra1.rect.y = game.balls[0].rect.y
                game.balls.append(extra1)
                
                extra2 = ball_class.Ball(game.surface)
                extra2.direction = game.balls[0].direction
                extra2.angle_x = game.balls[0].angle_x * -1
                extra2.rect.x = game.balls[0].rect.x
                extra2.rect.y = game.balls[0].rect.y
                game.balls.append(extra2)
                
                game.powerup_active.remove(powerup)
                del powerup
        
        elif powerup.type == "magnet":
            if powerup.time_left == powerup.maxtime:
                game.platform.magnet_activate_platform()
            powerup.time_left -= 1
            if powerup.time_left <= 0:
                game.platform.magnet = 0
                game.platform.powerup_deactivate_platform()
                game.powerup_active.remove(powerup)
                del powerup
            else:
                game.platform.magnet = 1
                
        elif powerup.type == "laser":
            if powerup.time_left == powerup.maxtime:
                game.platform.laser_activate_platform()
            if powerup.time_left % 9 == 0:
                game.lasers.append(Laser(game.surface, game.platform.rect.midtop))
                game.play_sound("laser_hit")
            powerup.time_left -= 1
            if powerup.time_left <= 0:
                game.platform.magnet = 0
                game.platform.powerup_deactivate_platform()
                game.powerup_active.remove(powerup)
                del powerup
        
        elif powerup.type == "enlarge":
            if powerup.time_left == powerup.maxtime:
                game.platform.enlarge_activate_platform()
            powerup.time_left -= 1
            if powerup.time_left <= 0:
                game.platform.magnet = 0
                game.platform.powerup_deactivate_platform()
                game.powerup_active.remove(powerup)
                del powerup
                
def check_powerup_falling(falling_list, platform, powerup_active):
    for powerup in falling_list:
        powerup.powerup_falling()
        # it fall under the screen bottom edge
        if powerup.rect.bottom >= MARGIN_BOTTOM:
            falling_list.remove(powerup)
            del powerup
        # hit the platform
        elif powerup.rect.colliderect(platform.rect):
            powerup.active = True
            falling_list.remove(powerup)
            powerup_active.append(powerup)
        # still falling
        else:    
            powerup.draw_powerup()