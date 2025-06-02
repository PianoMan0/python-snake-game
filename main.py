import pygame
import time
import random

pygame.init()

def init_game():
    # Window size
    window_x = 600
    window_y = 400

    # Initialize window
    pygame.display.set_caption('Snake Game')
    game_window = pygame.display.set_mode((window_x, window_y))

    # Snake default position and body
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]

    # Food position
    food_pos = [random.randrange(1, (window_x//10)) * 10,
                random.randrange(1, (window_y//10)) * 10]
    food_spawn = True

    # Direction
    direction = 'RIGHT'
    change_to = direction

    # Score
    score = 0

    return window_x, window_y, game_window, snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# FPS controller
fps = pygame.time.Clock()

def show_score(game_window, score):
    font = pygame.font.SysFont('arial', 24)
    score_surface = font.render('Score : ' + str(score), True, white)
    game_window.blit(score_surface, (10, 10))

def game_over(window_x, window_y, game_window, score):
    start_time = time.time()
    font = pygame.font.SysFont('arial', 48)
    restart_font = pygame.font.SysFont('arial', 24)
    countdown_font = pygame.font.SysFont('arial', 20)
    
    go_surface = font.render('Game Over', True, red)
    restart_surface = restart_font.render('Press R to Restart', True, white)
    
    go_rect = go_surface.get_rect()
    restart_rect = restart_surface.get_rect()
    
    go_rect.midtop = (window_x // 2, window_y // 4)
    restart_rect.midtop = (window_x // 2, window_y // 2)
    
    while True:
        remaining_time = 5 - int(time.time() - start_time)
        game_window.fill(black)
        game_window.blit(go_surface, go_rect)
        game_window.blit(restart_surface, restart_rect)
        
        countdown_surface = countdown_font.render(f'Auto-restart in {remaining_time}s', True, white)
        countdown_rect = countdown_surface.get_rect()
        countdown_rect.midtop = (window_x // 2, window_y // 2 + 40)
        game_window.blit(countdown_surface, countdown_rect)
        
        show_score(game_window, score)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        if time.time() - start_time >= 5:
            return True
        
        pygame.time.wait(10)

def game_loop():
    window_x, window_y, game_window, snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score = init_game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
            elif event.type == pygame.QUIT:
                pygame.quit()
                return False

        direction = change_to

        if direction == 'UP':
            snake_pos[1] -= 10
        elif direction == 'DOWN':
            snake_pos[1] += 10
        elif direction == 'LEFT':
            snake_pos[0] -= 10
        elif direction == 'RIGHT':
            snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (window_x//10)) * 10,
                       random.randrange(1, (window_y//10)) * 10]
        food_spawn = True

        game_window.fill(black)
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if (snake_pos[0] < 0 or snake_pos[0] > window_x-10 or
            snake_pos[1] < 0 or snake_pos[1] > window_y-10):
            if not game_over(window_x, window_y, game_window, score):
                return False
            return True

        for block in snake_body[1:]:
            if snake_pos == block:
                if not game_over(window_x, window_y, game_window, score):
                    return False
                return True

        show_score(game_window, score)
        pygame.display.update()
        fps.tick(15)

def main():
    while True:
        if not game_loop():
            break

if __name__ == "__main__":
    main()