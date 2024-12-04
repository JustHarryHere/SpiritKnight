import pygame, sys
from PIL import Image
import random

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Char
character_gif_path = 'D:/SpiritKnight/Sprites/lil dude bigger.gif'
character_gif = Image.open(character_gif_path)
char_frames = []
try:
    while True:
        char_frame = character_gif.copy()
        char_frame = char_frame.convert("RGBA")
        char_frames.append(pygame.image.fromstring(char_frame.tobytes(), char_frame.size, char_frame.mode))
        character_gif.seek(len(char_frames))  # Move to the next frame
except EOFError:
    pass

flipped_frames = [pygame.transform.flip(char_frame, True, False) for char_frame in char_frames]
char_rect = char_frames[0].get_rect(center=(width//2, height//2))
frame_index = 0
frame_counter = 0
frame_update_rate = 5
flipped = False

# Enemy
enemy_gif_path = 'D:/SpiritKnight/Sprites/black Wizard.gif'
enemy_gif = Image.open(enemy_gif_path)
enemy_frames = []
try:
    while True:
        enemy_frame = enemy_gif.copy()
        enemy_frame = enemy_frame.convert("RGBA")
        enemy_frames.append(pygame.image.fromstring(enemy_frame.tobytes(), enemy_frame.size, enemy_frame.mode))
        enemy_gif.seek(len(enemy_frames))  # Move to the next frame
except EOFError:
    pass

enemy_rect = enemy_frames[0].get_rect(center=(random.randint(0, width), random.randint(0, height)))
enemy_frame_index = 0
enemy_frame_counter = 0
enemy_frame_update_rate = 10

# Teleportation variables
teleportation_distance_threshold = 150  # Distance at which the enemy will teleport
teleportation_cooldown = 2000  # 2 seconds cooldown between teleports
last_teleportation_time = 0

# Warning circle variables
warning_circle_timer = 0
warning_circle_interval = 4000  # 4 seconds
warning_circle_duration = 3000  # Duration for which the circle is visible
warning_circle_visible_timer = 0
show_warning_circle = False
warning_circle_position = None

# Poison bottle variables
poison_bottle_path = 'D:/SpiritKnight/Sprites/poison bottle.png'
poison_bottle_image = pygame.image.load(poison_bottle_path).convert_alpha()
poison_bottle_rect = poison_bottle_image.get_rect()
poison_bottle_speed = 10
throw_poison_bottle = False
poison_bottle_start_time = 0
poison_bottle_target = None

# Poison cloud GIF variables
poison_gif_path = 'D:/SpiritKnight/Sprites/Poisoncloud.gif'
poison_gif = Image.open(poison_gif_path)
poison_frames = []
try:
    while True:
        poison_frame = poison_gif.copy()
        poison_frame = poison_frame.convert("RGBA")
        poison_frames.append(pygame.image.fromstring(poison_frame.tobytes(), poison_frame.size, poison_frame.mode))
        poison_gif.seek(len(poison_frames))  # Move to the next frame
except EOFError:
    pass

poison_frame_index = 0
poison_frame_timer = 0
poison_frame_duration = 300  # Duration for each frame
show_poison_gif = False
poison_gif_display_timer = 0
poison_gif_delay = 1500  # 1.5 seconds delay before showing the poison GIF

# Poison area variables
poison_aoe_path = 'D:/SpiritKnight/Sprites/PoisonAoe.png'
poison_aoe_image = pygame.image.load(poison_aoe_path).convert_alpha()
poison_aoe_rect = poison_aoe_image.get_rect()
warning_circle_radius = poison_aoe_rect.width // 2  # Use the width of the poison area as the radius
show_poison_aoe = False
poison_aoe_timer = 0
poison_aoe_duration = 3000  # Duration the poison area remains on screen

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

    # Cập nhật khung hình nhân vật
    frame_counter += 1
    if frame_counter >= frame_update_rate:
        frame_counter = 0
        frame_index = (frame_index + 1) % len(char_frames)

    # Cập nhật khung hình kẻ địch
    enemy_frame_counter += clock.get_time()
    if enemy_frame_counter >= enemy_frame_update_rate:
        enemy_frame_counter = 0
        enemy_frame_index = (enemy_frame_index + 1) % len(enemy_frames)

    # Teleportation logic
    current_time = pygame.time.get_ticks()
    distance_to_player = ((char_rect.centerx - enemy_rect.centerx) ** 2 + (char_rect.centery - enemy_rect.centery) ** 2) ** 0.5
    if distance_to_player < teleportation_distance_threshold and current_time - last_teleportation_time >= teleportation_cooldown:
        enemy_rect.center = (random.randint(0, width), random.randint(0, height))
        last_teleportation_time = current_time

    # Quản lý cảnh báo hình tròn
    warning_circle_timer += clock.get_time()
    if warning_circle_timer >= warning_circle_interval:
        warning_circle_timer = 0
        show_warning_circle = True
        warning_circle_visible_timer = 0
        warning_circle_position = char_rect.center
        poison_gif_display_timer = 0  # Reset GIF display timer
        throw_poison_bottle = True
        poison_bottle_start_time = pygame.time.get_ticks()
        poison_bottle_target = warning_circle_position
        poison_bottle_rect.center = enemy_rect.center  # Start from the enemy's position

    if show_warning_circle:
        warning_circle_visible_timer += clock.get_time()
        poison_gif_display_timer += clock.get_time()
        pygame.draw.circle(screen, (255, 0, 0), warning_circle_position, warning_circle_radius, 3)
        if poison_gif_display_timer >= poison_gif_delay:
            show_poison_gif = True
        if warning_circle_visible_timer >= warning_circle_duration:
            show_warning_circle = False
            show_poison_aoe = True
            poison_aoe_timer = 0
            poison_aoe_rect.center = warning_circle_position

    # Ném bình độc
    if throw_poison_bottle:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - poison_bottle_start_time
        if elapsed_time <= 1500:  # 1.5 seconds to reach the target
            progress = elapsed_time / 1500
            new_x = enemy_rect.x + (poison_bottle_target[0] - enemy_rect.x) * progress
            new_y = enemy_rect.y + (poison_bottle_target[1] - enemy_rect.y) * progress
            poison_bottle_rect.center = (new_x, new_y)
            screen.blit(poison_bottle_image, poison_bottle_rect)
        else:
            throw_poison_bottle = False

    # Hiển thị GIF bình độc vỡ
    if show_poison_gif:
        poison_frame_timer += clock.get_time()
        if poison_frame_timer >= poison_frame_duration:
            poison_frame_timer = 0
            poison_frame_index = (poison_frame_index + 1) % len(poison_frames)
        poison_rect = poison_frames[poison_frame_index].get_rect(center=(warning_circle_position[0], warning_circle_position[1])) 
        screen.blit(poison_frames[poison_frame_index], poison_rect)
        if poison_frame_index == len(poison_frames) - 1:
            show_poison_gif = False
            poison_frame_index = 0  # Reset the frame index

    # Quản lý vùng độc
    if show_poison_aoe:
        poison_aoe_timer += clock.get_time()
        screen.blit(poison_aoe_image, poison_aoe_rect)
        if poison_aoe_timer >= poison_aoe_duration:
            show_poison_aoe = False

    # Hiển thị kẻ địch
    screen.blit(enemy_frames[enemy_frame_index], enemy_rect)

    # Hiển thị nhân vật
    if flipped:
        screen.blit(flipped_frames[frame_index], char_rect)
    else:
        screen.blit(char_frames[frame_index], char_rect)

    # Kiểm tra nếu nhân vật dính độc
    if show_poison_aoe and char_rect.colliderect(poison_aoe_rect):
        print("Nhân vật đã dính độc!")

    pygame.display.flip()
    clock.tick(60)
