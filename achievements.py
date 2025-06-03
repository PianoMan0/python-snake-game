from enum import Enum
import json
import os
import time
import pygame

class Achievement(Enum):
    SPEED_DEMON = "Speed Demon"
    SNAKE_MASTER = "Snake Master"
    FOOD_LOVER = "Food Lover"
    SURVIVOR = "Survivor"
    WALL_HUGGER = "Wall Hugger (That's a sus name)"

class AchievementPopup:
    def __init__(self):
        self.active = False
        self.start_time = 0
        self.achievement = None
        self.duration = 3  # seconds to show popup

    def show(self, achievement):
        self.active = True
        self.start_time = time.time()
        self.achievement = achievement

    def update(self, game_window):
        if not self.active:
            return
        
        if time.time() - self.start_time > self.duration:
            self.active = False
            return

        # Draw achievement popup
        font = pygame.font.SysFont('arial', 20)
        text = f"Achievement Unlocked: {self.achievement.value}!"
        surface = font.render(text, True, pygame.Color('yellow'))
        rect = surface.get_rect(centerx=game_window.get_width()//2, top=10)
        
        # Draw background
        bg_rect = rect.inflate(20, 20)
        pygame.draw.rect(game_window, pygame.Color('darkgray'), bg_rect)
        pygame.draw.rect(game_window, pygame.Color('black'), bg_rect, 2)
        
        game_window.blit(surface, rect)

class AchievementManager:
    def __init__(self):
        self.achievements = {
            Achievement.SPEED_DEMON: {
                'description': 'Reach length 20 in under 1 minute',
                'unlocked': False,
                'progress': 0,
                'max_progress': 20
            },
            Achievement.SNAKE_MASTER: {
                'description': 'Reach score of 50',
                'unlocked': False,
                'progress': 0,
                'max_progress': 50
            },
            Achievement.FOOD_LOVER: {
                'description': 'Eat 100 food items total',
                'unlocked': False,
                'progress': 0,
                'max_progress': 100
            },
            Achievement.SURVIVOR: {
                'description': 'Play for 5 minutes without dying',
                'unlocked': False,
                'progress': 0,
                'max_progress': 300
            },
            Achievement.WALL_HUGGER: {
                'description': 'Stay near walls for 30 seconds',
                'unlocked': False,
                'progress': 0,
                'max_progress': 30
            }
        }
        self.popup = AchievementPopup()
        self.load_achievements()

    def save_achievements(self):
        data = {k.value: v for k, v in self.achievements.items()}
        save_path = os.path.join(os.path.dirname(__file__), 'achievements.json')
        with open(save_path, 'w') as f:
            json.dump(data, f)

    def load_achievements(self):
        save_path = os.path.join(os.path.dirname(__file__), 'achievements.json')
        try:
            with open(save_path, 'r') as f:
                data = json.load(f)
                for k, v in data.items():
                    self.achievements[Achievement(k)] = v
        except FileNotFoundError:
            self.save_achievements()

    def unlock_achievement(self, achievement, game_window):
        if not self.achievements[achievement]['unlocked']:
            self.achievements[achievement]['unlocked'] = True
            self.achievements[achievement]['progress'] = self.achievements[achievement]['max_progress']
            self.popup.show(achievement)
            self.save_achievements()
            return True
        return False

    def update_progress(self, achievement, value, game_window):
        if not self.achievements[achievement]['unlocked']:
            self.achievements[achievement]['progress'] = min(
                value,
                self.achievements[achievement]['max_progress']
            )
            if self.achievements[achievement]['progress'] >= self.achievements[achievement]['max_progress']:
                return self.unlock_achievement(achievement, game_window)
        return False

    def draw_achievements_screen(self, game_window):
        y_offset = 50
        font = pygame.font.SysFont('arial', 16)
        
        for achievement in Achievement:
            data = self.achievements[achievement]
            color = pygame.Color('green') if data['unlocked'] else pygame.Color('white')
            progress = f"{int(data['progress'])}/{data['max_progress']}"
            text = f"{achievement.value}: {data['description']} ({progress})"
            surface = font.render(text, True, color)
            game_window.blit(surface, (10, y_offset))
            y_offset += 20