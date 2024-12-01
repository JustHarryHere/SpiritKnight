import pygame
import sys
import os
import random
import math
import time
from PIL import Image

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Đường dẫn tệp
character_gif_path = 'D:/SpiritKnight/Sprites/lil dude bigger.gif'
enemy_attack_gif_path = 'D:\SpiritKnight\Sprites\Skeleshoot.gif'
arrow_image_path = 'D:/SpiritKnight/Sprites/arrow.png'

# Kiểm tra tệp tồn tại
if not all(os.path.exists(path) for path in [character_gif_path, enemy_attack_gif_path, arrow_image_path]):
    print("Một hoặc nhiều tệp không tồn tại!")
    sys.exit()

# Hàm load các khung từ GIF
def load_gif_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = gif.convert('RGBA')
            frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, 'RGBA'))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

# Load ảnh nhân vật (chỉ 1 khung cho đơn giản)
character_image = pygame.image.load(character_gif_path).convert_alpha()
char_rect = character_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Load hoạt ảnh tấn công của quái vật
enemy_attack_frames = load_gif_frames(enemy_attack_gif_path)
enemy_rect = enemy_attack_frames[0].get_rect(center=(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)))

# Load ảnh mũi tên
arrow_image = pygame.image.load(arrow_image_path).convert_alpha()
arrow_rect = arrow_image.get_rect()

# Các biến của quái vật
is_attacking = False      # Trạng thái tấn công
attack_frame_index = 0    # Khung hiện tại của hoạt ảnh tấn công
attack_timer = 0          # Bộ đếm thời gian cho hoạt ảnh tấn công
attack_duration = 1.0     # Thời gian hoạt ảnh tấn công (giây)
attack_frame_rate = 0.7   # Thời gian giữa các khung (giây)

# Các biến mũi tên
arrow_active = False
arrow_dx, arrow_dy = 0, 0
arrow_speed = 15
arrow_cooldown = 4  # Cooldown 2 giây
last_arrow_time = 0

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
    if keys[pygame.K_d]:
        char_rect.x += 5
    if keys[pygame.K_w]:
        char_rect.y -= 5
    if keys[pygame.K_s]:
        char_rect.y += 5

    # Thời gian hiện tại
    current_time = time.time()

    # Xử lý trạng thái tấn công của quái vật
    if is_attacking:
        # Hiển thị hoạt ảnh tấn công
        if current_time - attack_timer > attack_frame_rate:
            attack_frame_index = (attack_frame_index + 1) % len(enemy_attack_frames)
            attack_timer = current_time

        # Vẽ khung hiện tại
        screen.blit(enemy_attack_frames[attack_frame_index], enemy_rect)

        # Nếu hoạt ảnh tấn công kết thúc, bắn tên
        if current_time - last_arrow_time >= attack_duration:
            is_attacking = False  # Kết thúc tấn công
            arrow_active = True   # Chuẩn bị bắn tên
            last_arrow_time = current_time

            # Tính toán hướng bắn
            arrow_rect.center = enemy_rect.center
            arrow_dx = char_rect.centerx - enemy_rect.centerx
            arrow_dy = char_rect.centery - enemy_rect.centery
            distance = math.hypot(arrow_dx, arrow_dy)
            if distance != 0:
                arrow_dx /= distance
                arrow_dy /= distance
    else:
        # Nếu không tấn công, bắt đầu tấn công sau cooldown
        screen.blit(enemy_attack_frames[0], enemy_rect)  # Quái vật trạng thái đứng yên
        if not arrow_active and current_time - last_arrow_time > arrow_cooldown:
            is_attacking = True
            attack_timer = current_time
            attack_frame_index = 0  # Reset khung hoạt ảnh tấn công

    # Di chuyển và hiển thị mũi tên
    if arrow_active:
        arrow_rect.x += arrow_dx * arrow_speed
        arrow_rect.y += arrow_dy * arrow_speed
        screen.blit(arrow_image, arrow_rect)

        # Kiểm tra nếu mũi tên ra khỏi màn hình
        if (arrow_rect.right < 0 or arrow_rect.left > WIDTH or
            arrow_rect.bottom < 0 or arrow_rect.top > HEIGHT):
            arrow_active = False

        # Kiểm tra va chạm với nhân vật
        if char_rect.colliderect(arrow_rect):
            print("Nhân vật bị trúng mũi tên!")
            arrow_active = False

    # Vẽ nhân vật
    screen.blit(character_image, char_rect)

    # Cập nhật màn hình
    pygame.display.flip()
    clock.tick(60)
