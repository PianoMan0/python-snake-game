import pygame
import time
import random
from achievements import AchievementManager, Achievement

pygame.init()

# Define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Window size
window_x = 720
window_y = 480

# Initialize game window
game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('Snake Game with Achievements')
fps = pygame.time.Clock()

def init_game():
    # Starting position of snake
    snake_pos = [100, 50]
    
    # First 4 blocks of snake body
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    
    # First food position
    food_pos = [random.randrange(1, (window_x//10)) * 10,
                random.randrange(1, (window_y//10)) * 10]
    food_spawn = True
    
    # Starting direction
    direction = 'RIGHT'
    change_to = direction
    
    # Initial score
    score = 0
    
    # Initialize achievement system
    achievement_manager = AchievementManager()
    start_time = time.time()
    total_food_eaten = 0
    near_wall_time = 0
    
    return (window_x, window_y, game_window, snake_pos, snake_body, food_pos, 
            food_spawn, direction, change_to, score, achievement_manager, 
            start_time, total_food_eaten, near_wall_time)

def check_achievements(game_state):
    window_x, window_y, game_window, snake_pos, snake_body, _, _, _, _, score, \
    achievement_manager, start_time, total_food_eaten, near_wall_time = game_state
    
    # Speed Demon
    if len(snake_body) >= 20:
        if time.time() - start_time <= 60:
            achievement_manager.update_progress(Achievement.SPEED_DEMON, 20, game_window)
    
    # Snake Master
    achievement_manager.update_progress(Achievement.SNAKE_MASTER, score, game_window)
    
    # Food Lover
    achievement_manager.update_progress(Achievement.FOOD_LOVER, total_food_eaten, game_window)
    
    # Survivor
    elapsed_time = time.time() - start_time
    achievement_manager.update_progress(Achievement.SURVIVOR, elapsed_time, game_window)
    
    # Wall Hugger
    if (snake_pos[0] < 20 or snake_pos[0] > window_x - 20 or 
        snake_pos[1] < 20 or snake_pos[1] > window_y - 20):
        near_wall_time += 1/15  # Assuming 15 FPS
        achievement_manager.update_progress(Achievement.WALL_HUGGER, near_wall_time, game_window)
    
    # Update achievement popup
    achievement_manager.popup.update(game_window)
    
    return near_wall_time

def show_score(game_window, score):
    # Create font object
    score_font = pygame.font.SysFont('arial', 20)
    
    # Create the display surface object
    score_surface = score_font.render(f'Score: {score}', True, white)
    score_rect = score_surface.get_rect()
    
    # Display the score
    game_window.blit(score_surface, score_rect)

def game_over(game_window, score):
    # Game over font
    font = pygame.font.SysFont('arial', 50)
    small_font = pygame.font.SysFont('arial', 24)
    
    # Game over surface
    game_over_surface = font.render('Game Over!', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/4)
    
    # Score surface
    score_surface = font.render(f'Score: {score}', True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (window_x/2, window_y/2)
    
    # Start countdown
    start_time = time.time()
    restart_delay = 5  # seconds before auto-restart
    
    while True:
        # Calculate remaining time
        elapsed = time.time() - start_time
        remaining = max(0, restart_delay - elapsed)
        
        # Draw surfaces
        game_window.fill(black)
        game_window.blit(game_over_surface, game_over_rect)
        game_window.blit(score_surface, score_rect)
        
        # Draw restart message with countdown
        restart_text = f"Restarting in {int(remaining)} seconds... (Press SPACE to restart now)"
        restart_surface = small_font.render(restart_text, True, white)
        restart_rect = restart_surface.get_rect()
        restart_rect.midtop = (window_x/2, window_y*3/4)
        game_window.blit(restart_surface, restart_rect)
        
        pygame.display.flip()
        
        # Check for manual restart or quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Return to main loop for restart
        
        # Auto restart after delay
        if remaining <= 0:
            return  # Return to main loop for restart
        
        time.sleep(0.1)  # Small delay to prevent high CPU usage

def game_loop():
    while True:  # Outer loop for game restart
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
                    elif event.key == pygame.K_TAB:
                        game_state[10].draw_achievements_screen(game_state[2])
                        pygame.display.update()
                        pygame.time.wait(2000)
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
                game_state[12] += 1  # total_food_eaten
                game_state[6] = False  # food_spawn
            else:
                game_state[4].pop()

            # Spawning food
            if not game_state[6]:
                game_state[5] = [random.randrange(1, (window_x//10)) * 10,
                                random.randrange(1, (window_y//10)) * 10]
                game_state[6] = True

            # Update achievements
            game_state[13] = check_achievements(game_state)

            # Game Over conditions
            if (game_state[3][0] < 0 or game_state[3][0] > window_x-10 or
                game_state[3][1] < 0 or game_state[3][1] > window_y-10):
                game_over(game_state[2], game_state[9])
                break  # Break inner loop to restart

            for block in game_state[4][1:]:
                if game_state[3] == block:
                    game_over(game_state[2], game_state[9])
                    running = False
                    break

            if not running:
                break

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