import pygame
import sys
import os
import random
import math
import time

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Đường dẫn tệp
character_gif_path = 'D:/SpiritKnight/Sprites/lil dude bigger.gif'
enemy_gif_path = 'D:/SpiritKnight/Sprites/Skele.gif'
arrow_image_path = 'D:/SpiritKnight/Sprites/arrow.png'

# Kiểm tra tệp tồn tại
if not all(os.path.exists(path) for path in [character_gif_path, enemy_gif_path, arrow_image_path]):
    print("Một hoặc nhiều tệp không tồn tại!")
    sys.exit()

# Load ảnh GIF của nhân vật
char_frames = []
character_gif = pygame.image.load(character_gif_path)
char_frames.append(character_gif)

# Load ảnh GIF của kẻ địch
enemy_frames = []
enemy_gif = pygame.image.load(enemy_gif_path)
enemy_frames.append(enemy_gif)

# Load ảnh mũi tên
arrow_image = pygame.image.load(arrow_image_path)
arrow_rect = arrow_image.get_rect()

# Vị trí nhân vật và kẻ địch
char_rect = char_frames[0].get_rect(center=(WIDTH // 2, HEIGHT // 2))
enemy_rect = enemy_frames[0].get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

# Thu nhỏ hitbox nhân vật
hitbox_scale = 0.01  # Hitbox 70% kích thước ban đầu
char_hitbox = char_rect.inflate(-char_rect.width * (1 - hitbox_scale), -char_rect.height * (1 - hitbox_scale))

# Các biến khác
arrow_speed = 15
arrow_active = False
last_arrow_time = 0
arrow_cooldown = 2  # Cooldown 2 giây
arrow_dx, arrow_dy = 0, 0
flipped = False
frame_index = 0
frame_counter = 0
frame_update_rate = 5

# Vòng lặp chính
while True:
    screen.fill((0, 0, 0))  # Xóa màn hình

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Di chuyển nhân vật
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        char_rect.x -= 5
        flipped = True
    if keys[pygame.K_d]:
        char_rect.x += 5
        flipped = False
    if keys[pygame.K_w]:
        char_rect.y -= 5
    if keys[pygame.K_s]:
        char_rect.y += 5

    # Cập nhật hitbox theo vị trí của nhân vật
    char_hitbox.center = char_rect.center

    # Khởi tạo mũi tên nếu chưa được kích hoạt và đã qua thời gian cooldown
    current_time = time.time()
    if not arrow_active and current_time - last_arrow_time > arrow_cooldown:
        arrow_rect.center = enemy_rect.center
        arrow_active = True
        last_arrow_time = current_time

        # Hướng bắn
        arrow_dx = char_rect.centerx - enemy_rect.centerx
        arrow_dy = char_rect.centery - enemy_rect.centery
        distance = math.hypot(arrow_dx, arrow_dy)
        if distance != 0:
            arrow_dx /= distance
            arrow_dy /= distance

    # Di chuyển mũi tên
    if arrow_active:
        arrow_rect.x += arrow_dx * arrow_speed
        arrow_rect.y += arrow_dy * arrow_speed

        # Kiểm tra va chạm với hitbox nhân vật
        if char_hitbox.colliderect(arrow_rect):
            print("Nhân vật bị trúng mũi tên!")
            arrow_active = False

        # Kiểm tra nếu mũi tên ra khỏi màn hình
        if (arrow_rect.right < 0 or arrow_rect.left > WIDTH or
            arrow_rect.bottom < 0 or arrow_rect.top > HEIGHT):
            arrow_active = False

    # Vẽ đường màu đỏ báo hiệu hướng bắn nếu mũi tên chưa được bắn
    if not arrow_active:
        pygame.draw.line(screen, (255, 0, 0), enemy_rect.center, char_rect.center, 2)

    # Hiển thị nhân vật và kẻ địch
    if flipped:
        flipped_frame = pygame.transform.flip(char_frames[frame_index], True, False)
        screen.blit(flipped_frame, char_rect)
    else:
        screen.blit(char_frames[frame_index], char_rect)

    screen.blit(enemy_frames[frame_index % len(enemy_frames)], enemy_rect)

    # Vẽ mũi tên nếu đang hoạt động
    if arrow_active:
        screen.blit(arrow_image, arrow_rect)

    # Cập nhật màn hình
    pygame.display.flip()
    clock.tick(60)
