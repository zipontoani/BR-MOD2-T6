
import os
import pygame
import random

from turtle import Screen

from dino_runner.utils.constants import IMG_DIR
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.power_ups.types_power_ups import Shield, Hammer, TimeReset
from dino_runner.components.power_ups.power_up_manager import PowerUpManager



class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.power_ups = []
        self.HIT_SFX = pygame.mixer.Sound(os.path.join(IMG_DIR, 'Sounds/hit.wav'))
        self.POWER_UP_SFX = pygame.mixer.Sound(os.path.join(IMG_DIR, 'Sounds/upgrade.wav'))

    def update(self, game):
        obstacle_type = [
            Cactus(),
            Bird(),
        ]
        if len(self.obstacles) == 0:
             self.obstacles.append(obstacle_type[random.randint(0,1)])

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    self.HIT_SFX.play()
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                elif game.player.has_power_up and game.player.type == "shield":
                    self.POWER_UP_SFX.play()
                    game.player.dino_rect.colliderect(obstacle.rect) == False
                    break
                elif game.player.has_power_up and game.player.type == "hammer":
                    self.POWER_UP_SFX.play()
                    self.obstacles.remove(obstacle)
                    break
                elif game.player.has_power_up and game.player.type == "timereset":
                    self.HIT_SFX.play()
                    game.game_speed - 100
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break

    def draw(self, screen):
       for obstacle in self.obstacles:
        obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []


