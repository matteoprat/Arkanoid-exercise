import pygame
from pygame.locals import *
import random
import platform, ball_class, blocks, level_map, messages, screens, powerups, enemies
from arka_settings import *

BONUS_LIVES = [(i * 5000) + (i*5000)//2 for i in range(1,10)]

class Game():
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Arkanoid_Clone")
        pygame.mixer.init()
        self.surface = pygame.display.set_mode(size=(SCR_WIDTH, SCR_HEIGHT))
        
        self.bonus_lives = BONUS_LIVES
        self.level = 1
        self.score = 0
        self.lives = 3
        
        self.powerup_options = ["enlarge", "1up", "magnet", "balls", "skip", "laser", "speeddown"]
        self.powerup_falling = []
        self.powerup_active = []
        '''
        stuff to handle block colors, images and relations between blocks
        '''
        block_white = pygame.image.load("assets/block_white.png").convert()
        block_orange = pygame.image.load("assets/block_orange.png").convert()
        block_light_blue = pygame.image.load("assets/block_light_blue.png").convert()
        block_green = pygame.image.load("assets/block_green.png").convert()
        block_red = pygame.image.load("assets/block_red.png").convert()
        block_blue = pygame.image.load("assets/block_blue.png").convert()
        block_pink = pygame.image.load("assets/block_pink.png").convert()
        block_yellow = pygame.image.load("assets/block_yellow.png").convert()
        block_silver = pygame.image.load("assets/block_silver.png").convert()
        block_gold = pygame.image.load("assets/block_gold.png").convert()
        self.show_level = 90       
        # colorprefix: (image, hit to be destroyed, score)
        self.block_dict = {"w": (block_white, 1, 50),
                           "o": (block_orange, 1, 60),
                           "c": (block_light_blue, 1, 70),
                           "g": (block_green, 1, 80),
                           "r": (block_red, 1, 90),
                           "b": (block_blue, 1, 100),
                           "p": (block_pink, 1, 110),
                           "y": (block_yellow, 1, 120),
                           "s": (block_silver, 3, 50*self.level),
                           "G": (block_gold, 9999, 0)
                           }
        self.on_screen_blocks = []
        
        self.frame = pygame.image.load("assets/background.png").convert_alpha()       
        self.load_bg_img()
        self.messages = messages.Messages(self.surface)
        
        self.platform = platform.Platform(self.surface)
        
        self.balls = [ball_class.Ball(self.surface)] 
        
        self.load_map()
        self.block_left = level_map.get_bricks_to_destroy(self.map_blocks)
        
        self.lasers = []
        
        self.enemy_spawn_cooldown = 0
        self.list_enemies = []
        self.max_enemies = 3
    
    def play_sound(self, sound_name):
        sound = pygame.mixer.Sound("sounds/"+sound_name+".mp3")
        pygame.mixer.Sound.play(sound)
    
    def load_bg_img(self):
        self.level_bg = pygame.image.load(f"assets/bg_level{self.level%4}.png").convert()
    
    def load_map(self):
        self.map_blocks = level_map.get_level_map(self.level)
        for element in self.map_blocks:
            color, xpos, ypos = element
            image = self.block_dict[color]
            obj_ = blocks.Block(self.surface, image, (xpos, ypos), color)
            self.on_screen_blocks.append(obj_)
    
    def reset_game(self):
        self.lives = 3
        self.level = 1
        self.score = 0
        self.enemy_spawn_cooldown = 0
        self.__garbage_remove()
        self.bonus_lives = BONUS_LIVES
        self.load_bg_img()
        self.on_screen_blocks.clear() 
        self.balls = [ball_class.Ball(self.surface)]
        self.platform.reset_platform()
        self.load_map()
        self.block_left = level_map.get_bricks_to_destroy(self.map_blocks)
        self.update_blocks()
    
    def render_background(self):
        self.surface.blit(self.level_bg, (MARGIN_LEFT-3, MARGIN_TOP))
        self.surface.blit(self.frame, (0,0))
      
    def update_blocks(self):
        for block in self.on_screen_blocks:
            block.draw_block()
    
    def check_bonus_lives(self, powerup=False):
        if powerup == True:
            self.lives += 1
            self.play_sound("lifeup")
        if self.bonus_lives:
            if self.score >= self.bonus_lives[0]:
                self.bonus_lives.pop(0)
                self.lives += 1
                self.play_sound("lifeup")

    def check_powerup(self, block):
        if block.powerup == True:
            powertype = random.choice(self.powerup_options)
            powerup = powerups.PowerUp(self.surface, powertype, block.rect.left,
                                       block.rect.bottom)
            self.powerup_falling.append(powerup)    
    
    def get_highscore(self):
        ranking = []
        with open("ranking.csv", "r")as f:
            for line in f:
                ranking.append(line.strip("\n").split(","))
        return ranking
                
    def destroy_laser(self, laser):
        self.lasers.remove(laser)
        del laser
    
    def destroy_block(self, block):
        self.block_left -= 1 if self.block_left > 0 else 0
        self.score += block.score
        self.check_powerup(block)
        self.on_screen_blocks.remove(block)
        del block

    def destroy_enemy(self, enemy):
        self.list_enemies.remove(enemy)
        del enemy 
    
    def enemy_spawn(self):
        self.enemy_spawn_cooldown += 1
        if self.enemy_spawn_cooldown == 210:
            posx = random.choice( range( MARGIN_LEFT+(3*BLK_WIDTH), MARGIN_RIGHT-(3*BLK_WIDTH) ))
            posy = random.choice( range( MARGIN_TOP+1, MARGIN_TOP+(2*BLK_HEIGHT) ))
            if len(self.list_enemies) < self.max_enemies:
                self.list_enemies.append(enemies.EvilBubbles(self.surface,(posx, posy)))
            self.enemy_spawn_cooldown = 0
    
    def no_balls_on_screen(self):
        self.lives -= 1
        self.powerup_falling.clear()
        self.powerup_active.clear()
        for enemy in self.list_enemies:
            self.destroy_enemy(enemy)
        self.list_enemies.clear()
        self.enemy_spawn_cooldown = 0
        for laser in self.lasers:
            self.destroy_laser(laser)
        self.play_sound("balldown")
        self.balls.append(ball_class.Ball(self.surface))
        self.platform.reset_platform()
            
    def play(self):
        self.check_bonus_lives()
        self.render_background()
        self.messages.display_info(self.level, self.lives, self.score)
        self.platform.draw_platform()
        
        # If any laser on the screen evaluate if they hit blocks 
        for laser in self.lasers:
            laser.laser_move()
            laser.draw_laser()   
            action, block = laser.check_block_collision(self.on_screen_blocks)
            if action == "destroy":
                self.destroy_block(block)
                self.destroy_laser(laser)
                self.play_sound("hit_brick")
            if action == "redraw" or laser.rect.y <= MARGIN_TOP:
                self.destroy_laser(laser)
        
        # check for active power-ups and do things if any
        for powerup in self.powerup_active:
            powerups.handle_powerup(powerup, self)
            
        for ball in self.balls:
            # check if the current ball is glued to platform or free
            if ball.direction == None: # the ball is glued to the platform
                ball.rect.centerx = self.platform.rect.centerx
            
            # check if the current ball hit one platform or a block
            else:
                if self.platform.check_plaftorm_collision(ball):
                    self.play_sound("hit_paddle")
                    continue
                
                if ball.direction != None:
                    self.enemy_spawn()
                    ball.calculate_position()
                    
                action, block = ball.check_ball_collisions(self.on_screen_blocks)
                if action == "destroy":
                    self.destroy_block(block)
                if action != "miss":
                    self.play_sound("hit_brick")
        
        # check all falling power-ups
        powerups.check_powerup_falling(self.powerup_falling, self.platform, self.powerup_active)
        
        # control all the balls 
        for ball in self.balls:
            ball.draw_ball()
            # -2 means that the ball is under the bottom edge, so we need to remove it
            if ball.direction == -2:
                self.balls.remove(ball)
                del ball
        self.update_blocks() # redraw all the bricks on the screen
        
        # it control if we have to show the current level at the beginning of round
        if self.show_level > 0:
            self.messages.display_level(self.level)
            self.show_level -= 1
        
        for enemy in self.list_enemies:
            event = enemy.check_collisions(self.on_screen_blocks, self.balls,
                                           self.platform, self.lasers)
            if event == "hit_ball" or event == "hit_laser":
                self.score += 100+self.level
                self.destroy_enemy(enemy)
            elif event == "hit_platform":
                for ball in self.balls:
                    self.balls.remove(ball)
                    del ball
                self.destroy_enemy(enemy)
            elif event == "out_screen":
                self.destroy_enemy(enemy)
        
        # control all the balls in play, if no balls are in play
        # remove a live and reset ball and platform position
        if len(self.balls) == 0:
            self.no_balls_on_screen()
                  
    def next_level(self):
        self.level += 1
        self.load_bg_img()
        self.platform.reset_platform()
        self.__garbage_remove()
        self.balls = [ball_class.Ball(self.surface)]
        self.load_map()
        self.block_left = level_map.get_bricks_to_destroy(self.map_blocks)
        self.show_level = 90
        self.update_blocks()
    
    def __garbage_remove(self):
        for block in self.on_screen_blocks:
            del block
        self.on_screen_blocks.clear()
        for powerup in self.powerup_falling:
            del powerup
        self.powerup_falling.clear()
        for powerup in self.powerup_active:
            del powerup
        self.powerup_active.clear()
        for laser in self.lasers:
            del laser
        self.lasers.clear()
        for ball in self.balls:
            del ball
        self.balls.clear()
        for enemy in self.list_enemies:
            del enemy
        self.list_enemies.clear()
        
    def run(self):
        pygame.mixer.music.load("sounds/arka_stage.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops = -1)
        music_on = 1
        self.running = True
        self.pause = False
        pygame.key.set_repeat(1, 10)
            
        self.render_background()
        self.platform.draw_platform()
        self.balls[0].draw_ball()
            
        while self.running:
            for event in pygame.event.get():
                                  
                if event.type == KEYDOWN:                        
                    if event.key == K_ESCAPE:
                        self.running = False                        
                    if event.key == K_RETURN:
                        #pygame.mixer.music.unpause()
                        if self.block_left == 0:
                            self.next_level()
                            self.pause = False
   
                    if not self.pause:
                        
                        # MOVEMENTS CONTROL                       
                        if event.key == K_LEFT:
                            self.platform.move_left()        
                        if event.key == K_RIGHT: 
                            self.platform.move_right()
                        if event.key == K_SPACE:
                            for ball in self.balls:
                                if ball.direction == None:
                                    ball.launch_ball()
                        
                        # SOUND CONTROL
                        if event.key == K_m:
                            if music_on == 1:
                                pygame.mixer.music.pause()
                                music_on = 0
                        if event.key == K_n:
                            if music_on == 0:
                                pygame.mixer.music.unpause()
                                music_on = 1
                        if event.key == K_p:
                            self.pause = True
                            screens.show_pause_game(game)
                
                elif event.type == QUIT:
                    self.running = False
                    
            try:        
                if not self.pause:
                    self.play()
                
            except Exception as e:
                print(e)
            
            if self.lives == 0:
                screens.show_game_over(self)
                self.pause = True
                
            if self.block_left == 0:
                if self.level == 35:
                    screens.show_game_over(self)
                else:
                    screens.show_level_completed(self)
                self.pause = True
                    
            pygame.display.update()
            FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    game = Game()
    screens.play_intro(game)