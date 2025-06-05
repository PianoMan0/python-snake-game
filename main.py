import pygame
import time
import random
import os

# Initialize Pygame
pygame.init()

# Define colors
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)

# Window size
window_x = 720
window_y = 480

# Initialize game window
game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('Snake Game')

# FPS controller
fps = pygame.time.Clock()

def init_game():
    """Initialize game state"""
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, (window_x//10)) * 10,
                random.randrange(1, (window_y//10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    
    return (
        snake_pos,      # [0] Current snake position
        snake_body,     # [1] List of snake body positions
        game_window,    # [2] Game window surface
        snake_pos,      # [3] Snake head position
        snake_body,     # [4] Snake body list
        food_pos,       # [5] Food position
        food_spawn,     # [6] Food spawn flag
        direction,      # [7] Current direction
        change_to,      # [8] Direction to change to
        score          # [9] Current score
    )

def get_high_score():
    """Read the high score from file or return 0 if file doesn't exist"""
    try:
        with open('highscore.txt', 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    """Save the high score to file if it's higher than the current high score"""
    current_high = get_high_score()
    if score > current_high:
        with open('highscore.txt', 'w') as f:
            f.write(str(score))
        return True
    return False

def show_score(game_window, score):
    # Create font object
    score_font = pygame.font.SysFont('arial', 20)
    
    # Create the display surface object for current score
    score_surface = score_font.render(f'Score: {score}', True, white)
    score_rect = score_surface.get_rect()
    
    # Create the display surface for high score
    high_score = get_high_score()
    high_score_surface = score_font.render(f'High Score: {high_score}', True, white)
    high_score_rect = high_score_surface.get_rect()
    high_score_rect.topright = (window_x - 10, 10)
    
    # Display both scores
    game_window.blit(score_surface, score_rect)
    game_window.blit(high_score_surface, high_score_rect)

def game_over(game_window, score):
    # Game over font
    font = pygame.font.SysFont('arial', 50)
    small_font = pygame.font.SysFont('arial', 30)
    
    # Game over surface
    game_over_surface = font.render('Game Over!', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/4)
    
    # Score surface
    score_surface = font.render(f'Score: {score}', True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (window_x/2, window_y/2)
    
    # High score message
    if save_high_score(score):
        new_high_surface = small_font.render('New High Score!', True, green)
        new_high_rect = new_high_surface.get_rect()
        new_high_rect.midtop = (window_x/2, window_y/2 + 50)
    
    # Draw surfaces
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    game_window.blit(score_surface, score_rect)
    if save_high_score(score):
        game_window.blit(new_high_surface, new_high_rect)
    pygame.display.flip()
    
    # Wait 2 seconds before quitting
    time.sleep(2)
    pygame.quit()
    quit()

def game_loop():
    game_state = list(init_game())
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game_state[7] != 'DOWN':
                    game_state[8] = 'UP'
                elif event.key == pygame.K_DOWN and game_state[7] != 'UP':
                    game_state[8] = 'DOWN'
                elif event.key == pygame.K_LEFT and game_state[7] != 'RIGHT':
                    game_state[8] = 'LEFT'
                elif event.key == pygame.K_RIGHT and game_state[7] != 'LEFT':
                    game_state[8] = 'RIGHT'
            elif event.type == pygame.QUIT:
                pygame.quit()
                return False

        # Direction validation
        if game_state[8] == 'UP' and game_state[7] != 'DOWN':
            game_state[7] = 'UP'
        if game_state[8] == 'DOWN' and game_state[7] != 'UP':
            game_state[7] = 'DOWN'
        if game_state[8] == 'LEFT' and game_state[7] != 'RIGHT':
            game_state[7] = 'LEFT'
        if game_state[8] == 'RIGHT' and game_state[7] != 'LEFT':
            game_state[7] = 'RIGHT'

        # Moving the snake
        if game_state[7] == 'UP':
            game_state[3][1] -= 10
        if game_state[7] == 'DOWN':
            game_state[3][1] += 10
        if game_state[7] == 'LEFT':
            game_state[3][0] -= 10
        if game_state[7] == 'RIGHT':
            game_state[3][0] += 10

        # Snake body growing mechanism
        game_state[4].insert(0, list(game_state[3]))
        
        if game_state[3] == game_state[5]:  # snake_pos == food_pos
            game_state[9] += 1  # score
            game_state[6] = False  # food_spawn
        else:
            game_state[4].pop()

        # Spawning food
        if not game_state[6]:
            game_state[5] = [random.randrange(1, (window_x//10)) * 10,
                            random.randrange(1, (window_y//10)) * 10]
            game_state[6] = True

        # Game Over conditions
        if (game_state[3][0] < 0 or game_state[3][0] > window_x-10 or
            game_state[3][1] < 0 or game_state[3][1] > window_y-10):
            game_over(game_state[2], game_state[9])

        for block in game_state[4][1:]:
            if game_state[3] == block:
                game_over(game_state[2], game_state[9])

        # Refresh game screen
        game_state[2].fill(black)
        for pos in game_state[4]:
            pygame.draw.rect(game_state[2], green, 
                           pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_state[2], red, 
                        pygame.Rect(game_state[5][0], game_state[5][1], 10, 10))

        show_score(game_state[2], game_state[9])
        pygame.display.update()
        fps.tick(15)

if __name__ == "__main__":
    game_loop()