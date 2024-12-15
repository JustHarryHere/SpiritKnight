import pygame, sys
from PIL import Image
import time
import random
from pygame.math import Vector2
import math
import os

# Khởi tạo pygame
pygame.init()

# Cài đặt màn hình
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Thư mục chứa tài nguyên
script_dir = os.path.dirname(os.path.abspath(__file__))
Sprites_folder = os.path.join(script_dir, '..', 'Sprites')
Music_folder = os.path.join(script_dir, '..', 'Music')

# Âm thanh
pygame.mixer.init()
pickup_sound = pygame.mixer.Sound(os.path.join(Music_folder, 'Pop-_Minecraft-Sound_-Sound-Effect-for-editing.wav'))

class LoadItem:
    def __init__(self, gif_name, enemy_rect):
        self.item_gif_rect = enemy_rect
        self.pick_up_sound = pickup_sound
        self.picked_up = False
        self.frames = self.load_gif(os.path.join(Sprites_folder, 'wingedboot.gif'))
        self.frame_index = 0
        self.frame_counter = 0
        self.frame_update_rate = 5

    def load_gif(self, gif_path):
        frames = []
        gif = Image.open(gif_path)
        try:
            while True:
                gif.seek(gif.tell())
                frame = gif.copy().convert("RGBA")
                frame = frame.resize((60, 60), Image.LANCZOS)
                pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                frames.append(pygame_frame)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        return frames

    def check_pick_up(self, char_rect, character):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and not self.picked_up:
            if char_rect.colliderect(self.item_gif_rect):
                self.picked_up = True
                self.pick_up_sound.play()
                character.activate_speed_boost()
                print("Speed boost activated!")

    def draw(self, screen, char_rect, character):
        self.check_pick_up(char_rect, character)
        if not self.picked_up:
            screen.blit(self.frames[self.frame_index], self.item_gif_rect)
            self.frame_counter += 1
            if self.frame_counter >= self.frame_update_rate:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)

class Character:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.character_rect = pygame.Rect(width // 2, height // 2, 50, 50)
        self.default_speed = 5
        self.boosted_speed = 10
        self.speed_boost = False
        self.speed_boost_timer = 0
        self.boost_duration = 3000  # 3 giây

    def activate_speed_boost(self):
        self.speed_boost = True
        self.speed_boost_timer = pygame.time.get_ticks()

    def handle_keys(self):
        current_speed = self.boosted_speed if self.speed_boost else self.default_speed

        if self.speed_boost and pygame.time.get_ticks() - self.speed_boost_timer >= self.boost_duration:
            self.speed_boost = False
            print("Speed boost ended!")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.character_rect.x = max(0, self.character_rect.x - current_speed)
        if keys[pygame.K_d]:
            self.character_rect.x = min(self.width - self.character_rect.width, self.character_rect.x + current_speed)
        if keys[pygame.K_w]:
            self.character_rect.y = max(0, self.character_rect.y - current_speed)
        if keys[pygame.K_s]:
            self.character_rect.y = min(self.height - self.character_rect.height, self.character_rect.y + current_speed)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.character_rect)

def main():
    character = Character(width, height)
    wingedboot = LoadItem('wingedboot.gif', pygame.Rect(400, 300, 60, 60))  # Ví dụ vị trí nhặt wingedboot

    while True:
        screen.fill((0, 0, 0))  # Xóa màn hình

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Xử lý di chuyển nhân vật
        character.handle_keys()

        # Vẽ nhân vật và vật phẩm
        character.draw(screen)
        wingedboot.draw(screen, character.character_rect, character)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
