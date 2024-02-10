import pygame
import random
import os
import sys

# Get the directory of the script
if getattr(sys, 'frozen', False):
    # If the script is run as an executable (e.g., PyInstaller)
    script_dir = os.path.dirname(sys.executable)
else:
    # If the script is run as a Python script
    script_dir = os.path.dirname(__file__)

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Load sound files with their full paths
beep = pygame.mixer.Sound(os.path.join(script_dir, "beep.mp3"))
over = pygame.mixer.Sound(os.path.join(script_dir, "gameover.mp3"))
intro = pygame.mixer.Sound(os.path.join(script_dir, "intro.mp3"))

# GAME WINDOW
length = 900
height = 600
game_window = pygame.display.set_mode((length, height))
pygame.display.set_caption("Snake Game!")

def display_score(score, color, x, y, content):
    font = pygame.font.SysFont(None, 55)
    text = font.render(content + str(score), True, color)
    game_window.blit(text, (x, y))

def plot_snake(game_window, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(game_window, color, [x, y, snake_size, snake_size])

def generate_food(game_window, color, x, y, food_size):
    pygame.draw.rect(game_window, color, [x, y, food_size, food_size])

def display_text(text, color, x, y):
    font = pygame.font.SysFont(None, 55)
    text = font.render(text, True, color)
    game_window.blit(text, (x, y))

# FPS for the game
clock = pygame.time.Clock()
fps = 30

# Load background image with its full path
background_image = pygame.image.load(os.path.join(script_dir, "background_image.jpg"))
background_image = pygame.transform.scale(background_image, (length, height)).convert_alpha()

def welcome():
    intro.play(loops=-1)
    intro.set_volume(0.5)
    game_window.fill((188, 245, 224))
    display_text("WELCOME TO SNAKES", (0, 0, 0), 225, 275)
    display_text("PRESS SPACEBAR TO PLAY", (0, 0, 0), 200, 325)
    quit_game = False
    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)

def gameloop():
    # GAME VARIABLES
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    snake_x = 50
    snake_y = 50
    snake_size = 20
    quit_game = False
    game_over = False
    velocity_x = 0
    velocity_y = 0
    score = 0
    snake_length = 1

    # Empty SNK_LIST, but "head" list will be appended into it every time (check line 85)
    snk_list = []
    
    # Food
    food_x = random.randint(20, 200)
    food_y = random.randint(20, 350)

    while not quit_game:
        with open(os.path.join(script_dir, "highscore.txt"), "r") as f:
            highscore = f.read()

        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
            game_window.fill(white)
            text = pygame.font.SysFont(None, 56)
            font = text.render("Game Over! Press Enter to continue", True, red)
            game_window.blit(font, (100, height / 2))
                       
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                if event.type == pygame.KEYDOWN:
                    velocity_x = 0
                    velocity_y = 0                  
                    if event.key == pygame.K_LEFT:
                        velocity_x -= 8
                        velocity_y = 0
                    elif event.key == pygame.K_RIGHT:
                        velocity_x += 8
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y -= 8
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN: 
                        velocity_y += 8
                        velocity_x = 0

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snake_length:
                del snk_list[0]

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 8:
                beep.play()
                score += 10
                food_x = random.randint(10, 300)
                food_y = random.randint(10, 450)
                snake_length += 5

                if score > int(highscore):
                    display_score(highscore, black, 10, 20, "Highscore:")
                    highscore = score
                    with open(os.path.join(script_dir, "highscore.txt"), "w") as f:
                        f.write(str(highscore)) 

            snake_x += velocity_x
            snake_y += velocity_y
            game_window.fill(white)
            game_window.blit(background_image, (0, 0))
            display_score(score, black, 10, 10, "Score: ")
            display_score(highscore, black, 10, 50 , "Highscore: ")
            generate_food(game_window, red, food_x, food_y, 20)
            plot_snake(game_window, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

        if (snake_x < 0 or snake_x > length or
            snake_y < 0 or snake_y > height) and not game_over:
            over.play()
            over.set_volume(1.5)
            game_over = True

        if head in snk_list[:-1] and not game_over:
            over.play()
            over.set_volume(1.5)
            game_over = True

welcome()
