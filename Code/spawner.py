import random
from pygame.math import Vector2

class Spawner:
    def __init__(self, width, height, min_distance):
        self.width = width
        self.height = height
        self.min_distance = min_distance

    def spawn_enemy(self, character_pos):
        while True:
            enemy_x = random.randint(0, self.width)
            enemy_y = random.randint(0, self.height)
            enemy_pos = Vector2(enemy_x, enemy_y)
            if enemy_pos.distance_to(character_pos) >= self.min_distance:
                return enemy_pos
