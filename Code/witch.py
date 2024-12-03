import pygame, sys, random
from PIL import Image

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Tải ảnh GIF nhân vật chính
character_gif_path = 'D:/SpiritKnight/Sprites/lil dude bigger.gif'
character_gif = Image.open(character_gif_path)
char_frames = []
try:
    while True:
        char_frame = character_gif.copy()
        char_frame = char_frame.convert("RGBA")
        char_frames.append(pygame.image.fromstring(char_frame.tobytes(), char_frame.size, char_frame.mode))
        character_gif.seek(len(char_frames))  # Chuyển sang khung hình tiếp theo
except EOFError:
    pass

flipped_frames = [pygame.transform.flip(char_frame, True, False) for char_frame in char_frames]
char_rect = char_frames[0].get_rect(center=(width // 2, height // 2))
frame_index = 0
frame_counter = 0
frame_update_rate = 5
flipped = False

# Tải ảnh GIF kẻ địch
enemy_gif_path = 'D:/SpiritKnight/Sprites/black Wizard.gif'
enemy_gif = Image.open(enemy_gif_path)
enemy_frames = []
try:
    while True:
        enemy_frame = enemy_gif.copy()
        enemy_frame = enemy_frame.convert("RGBA")
        enemy_frames.append(pygame.image.fromstring(enemy_frame.tobytes(), enemy_frame.size, enemy_frame.mode))
        enemy_gif.seek(len(enemy_frames))  # Chuyển sang khung hình tiếp theo
except EOFError:
    pass

enemy_rect = enemy_frames[0].get_rect(center=(random.randint(0, width), random.randint(0, height)))
enemy_frame_index = 0
enemy_frame_counter = 0
enemy_frame_update_rate = 5

# Tải ảnh bãi độc
poison_path = 'D:/SpiritKnight/Sprites/PoisonAoe.png'
poison_image = pygame.image.load(poison_path).convert_alpha()

# Tải ảnh bình độc
vial_path = 'D:/SpiritKnight/Sprites/poison bottle.png'
vial_image = pygame.image.load(vial_path).convert_alpha()
vials = []

# Biến bộ đếm thời gian và danh sách bãi độc
poison_spawn_interval = 4000  # 4 giây
poison_lifetime = 5000  # 5 giây
warning_time = 2000  # 2 giây
last_poison_spawn_time = pygame.time.get_ticks()
poison_rects = []
warnings = []

# Vòng lặp trò chơi
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        char_rect.x -= 5
        flipped = False
    if keys[pygame.K_d]:
        char_rect.x += 5
        flipped = True
    if keys[pygame.K_w]:
        char_rect.y -= 5
    if keys[pygame.K_s]:
        char_rect.y += 5

    # Cập nhật khung hình nhân vật chính
    frame_counter += 1
    if frame_counter >= frame_update_rate:
        frame_counter = 0
        frame_index = (frame_index + 1) % len(char_frames)

    # Thêm cảnh báo bãi độc mỗi 4 giây tại vị trí nhân vật chính
    current_time = pygame.time.get_ticks()
    if current_time - last_poison_spawn_time >= poison_spawn_interval:
        last_poison_spawn_time = current_time
        target_center = (char_rect.x + char_rect.width // 2, char_rect.y + char_rect.height // 2)
        warnings.append((target_center, current_time))
        # Tạo bình độc tại vị trí của phù thủy
        vial_rect = vial_image.get_rect(center=enemy_rect.center)
        vial_velocity = ((target_center[0] - vial_rect.x) / 120, (target_center[1] - vial_rect.y) / 120)  # Di chuyển trong 120 frame (khoảng 2 giây)
        vials.append((vial_rect, vial_velocity, target_center, current_time))

    # Hiển thị các cảnh báo và thêm bãi độc sau cảnh báo 2 giây
    warnings = [(center, start_time) for center, start_time in warnings if current_time - start_time < warning_time + 1000]
    for warning_center, start_time in warnings:
        if current_time - start_time < warning_time:
            warning_radius = poison_image.get_rect().width // 2
            pygame.draw.circle(screen, (255, 255, 0), warning_center, warning_radius, 2)

    # Hiển thị các bình độc
    for vial in vials[:]:
        vial_rect, vial_velocity, target_center, spawn_time = vial
        vial_rect.x += vial_velocity[0]
        vial_rect.y += vial_velocity[1]
        screen.blit(vial_image, vial_rect)
        # Kiểm tra va chạm của bình độc với vị trí mục tiêu
        if ((target_center[0] - vial_rect.centerx)**2 + (target_center[1] - vial_rect.centery)**2) < warning_radius**2:  # Kiểm tra va chạm với tâm bãi độc
            vials.remove(vial)
            poison_rects.append((pygame.Rect(target_center[0] - poison_image.get_width() // 2, target_center[1] - poison_image.get_height() // 2, poison_image.get_width(), poison_image.get_height()), current_time))

    # Hiển thị các bãi độc và xóa sau 5 giây
    poison_rects = [(rect, spawn_time) for rect, spawn_time in poison_rects if current_time - spawn_time < poison_lifetime]
    for poison_rect, spawn_time in poison_rects:
        screen.blit(poison_image, poison_rect)
        # Kiểm tra va chạm với nhân vật chính
        if char_rect.colliderect(poison_rect):
            print("poisoned")

    # Hiển thị nhân vật chính
    if flipped:
        screen.blit(flipped_frames[frame_index], char_rect)
    else:
        screen.blit(char_frames[frame_index], char_rect)

    # Cập nhật khung hình kẻ địch
    enemy_frame_counter += 1
    if enemy_frame_counter >= enemy_frame_update_rate:
        enemy_frame_counter = 0
        enemy_frame_index = (enemy_frame_index + 1) % len(enemy_frames)

    # Hiển thị kẻ địch
    screen.blit(enemy_frames[enemy_frame_index], enemy_rect)

    pygame.display.flip()
    clock.tick(60)
