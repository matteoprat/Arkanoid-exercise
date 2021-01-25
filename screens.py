import pygame
from pygame.locals import *
from arka_settings import *
import messages

def check_highscore(score, level, ranking, messages, surface):
    pygame.key.set_repeat()
    for i, rank in enumerate(ranking):
        if score > int(rank[1]) or score == int(rank[1]) and level > int(rank[2]):
            highscore = True
            name = ""
            input_rect = pygame.Rect((SCR_WIDTH-60)//2, 545,60, 30)
            while highscore:
                img = pygame.image.load("assets/gameoverscreen.png").convert_alpha()
                surface.blit(img, (0, 0))
                messages.intro_text_small("CONGRATULATIONS", 375)
                messages.intro_text_small("YOUR SCORE OF", 395)
                messages.intro_text_small(f"{score}", 415)
                messages.intro_text_small("WILL BE RECORDED!", 435)
                messages.intro_text_small("Enter a 3 letter or digit name", 465)
                messages.intro_text_small("press [return] when you are done", 485)
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            write_highscore(score, level, ranking, name, i)
                            highscore = False
                        elif event.key == K_BACKSPACE:
                            name = name[:-1]
                        else:
                            if event.unicode != ",":
                                if len(name) < 3:
                                    name += event.unicode                
                pygame.draw.rect(surface,(255,255,255),input_rect, 2)
                messages.highscore_input(name, input_rect.x+10, input_rect.y+1)                
                pygame.display.flip()
                FPSCLOCK.tick(FPS)
            break

def write_highscore(score, level, ranking, name, pos):
    ranking.insert(pos, [name,str(score),str(level)])
    with open("ranking.csv", "w") as f:
        for i in range (0,10):
            f.write(ranking[i][0]+","+ranking[i][1]+","+ranking[i][2]+"\n")
    return True            
    
def draw_all(game):
    game.render_background()
    game.messages.display_info(game.level, game.lives, game.score)
    game.platform.draw_platform()
    for laser in game.lasers:
        laser.draw_laser()
    for ball in game.balls:
        ball.draw_ball()
    for block in game.on_screen_blocks:
        block.draw_block()
    for enemy in game.list_enemies:
        enemy.draw_enemy()
    for powerup in game.powerup_falling:
        powerup.draw_powerup()

def play_intro(game):
    pygame.mixer.music.load("sounds/arka_intro.mp3")
    pygame.mixer.music.play(loops = -1)
    intro_running = True    
    i = pygame.image.load("assets/concept_intro.png").convert_alpha()
    game.surface.blit(i, (0, 0))
    next_to_load=""
    while intro_running:       
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    intro_running = False
                if event.key == K_RETURN:
                    intro_running = False
                    next_to_load = "play"
                if event.key == K_s:                   
                    intro_running = False
                    next_to_load = "highscores"
                if event.key == K_h:
                    intro_running = False
                    next_to_load = "instructions"
            if event.type == QUIT:
                pygame.quit()
                exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    if next_to_load == "play":
        game.run()
    elif next_to_load == "highscores":
        play_highscores(game)
    elif next_to_load == "instructions":
        play_instructions(game)
        
def play_highscores(game):
    highscores_running = True
    i = pygame.image.load("assets/concept_hiscore.png").convert_alpha()
    game.surface.blit(i, (0, 0))
    ranking = game.get_highscore()
    game.messages.highscore(ranking)
    while highscores_running:       
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                highscores_running = False
            if event.type == QUIT:
                pygame.quit()
                exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    play_intro(game)
        
def play_instructions(game):
    howto_running = True
    i = pygame.image.load("assets/concept_instructions.png").convert_alpha()
    game.surface.blit(i, (0, 0))
    while howto_running:       
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                howto_running = False
            if event.type == QUIT:
                pygame.quit()
                exit()        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    play_intro(game)
        
def show_pause_game(game):
    pause_running = True
    draw_all(game)
    i = pygame.image.load("assets/pausescreen.png").convert_alpha()
    game.surface.blit(i, (0, 0))
    game.messages.intro_text("PRESS [ENTER] TO RESUME", 345)
    while pause_running:       
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key ==  K_RETURN:
                pause_running = False
            if event.type == QUIT:
                pygame.quit()
                exit()       
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    game.run()
    
def show_game_over(game):
    pause_game_over = True
    check_highscore(game.score, game.level, game.get_highscore(), game.messages, game.surface)
    game.render_background()
    draw_all(game)
    i = pygame.image.load("assets/gameoverscreen.png").convert_alpha()
    game.surface.blit(i, (0, 0))
    game.messages.intro_text_small("PRESS [ENTER] TO RETURN TO TITLE SCREEN", 380)
    while pause_game_over:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == K_RETURN:
                    pause_game_over = False
            if event.type == QUIT:
                pygame.quit()
                exit()        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    game.reset_game()
    play_intro(game)
    
def show_level_completed(game):
    game.render_background()
    game.messages.display_info(game.level, game.lives, game.score)
    game.platform.draw_platform()
    game.balls[0].draw_ball()
    game.update_blocks()
    image = pygame.image.load("assets/stageclear.png").convert_alpha()
    game.surface.blit(image, (0,0))
    game.messages.level_completed(game.score)
    game.platform.magnet = 0   
            
    
    
    