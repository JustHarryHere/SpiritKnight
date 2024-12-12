# game_objects.py

import pygame
import time

# Lớp WingedBoot
class WingedBoot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('winged_boot_image.png')  # Thay bằng hình ảnh của winged boot
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Lớp Character
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('character_image.png')  # Thay bằng hình ảnh của nhân vật
        self.rect = self.image.get_rect()
        self.rect.x = 100  # Vị trí ban đầu của nhân vật
        self.rect.y = 100
        self.speed = 5  # Tốc độ ban đầu của nhân vật
        self.original_speed = self.speed
        self.boosted_speed = 10  # Tốc độ khi có wingedboot
        self.boost_time = 0  # Biến thời gian để kiểm tra khi nào hết thời gian tăng tốc
        self.is_boosted = False  # Kiểm tra xem nhân vật có đang tăng tốc không

    def update(self):
        # Nếu có tăng tốc, kiểm tra thời gian còn lại
        if self.is_boosted:
            if time.time() - self.boost_time > 3:  # 3 giây đã trôi qua
                self.speed = self.original_speed  # Trở lại tốc độ ban đầu
                self.is_boosted = False  # Kết thúc trạng thái tăng tốc

    def handle_keys(self):
        # Xử lý các phím di chuyển của nhân vật
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def check_pick_up(self, item):
        # Kiểm tra xem nhân vật có nhặt được wingedboot không
        if self.rect.colliderect(item.rect):
            if isinstance(item, WingedBoot):  # Kiểm tra nếu là winged boot
                self.activate_boost()

    def activate_boost(self):
        self.speed = self.boosted_speed  # Tăng tốc độ lên
        self.is_boosted = True  # Đánh dấu là đang tăng tốc
        self.boost_time = time.time()  # Ghi lại thời gian khi tăng tốc
