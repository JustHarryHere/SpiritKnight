import pygame, sys
from PIL import Image
import random
import math

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Load teleportation circle image
teleport_circle_path = 'D:/SpiritKnight/Sprites/defalt circle.png'
teleport_circle_image = pygame.image.load(teleport_circle_path).convert_alpha()
teleport_circle_rect = teleport_circle_image.get_rect()

# Rotation variables
teleport_circle_angle = 0 # Starting angle
rotation_speed = 1 # Degrees to rotate each frame

# Hàm tính khoảng cách
def distance(rect1, rect2):
    return ((rect1.centerx - rect2.centerx) ** 2 + (rect1.centery - rect2.centery) ** 2) ** 0.5

# Enemy teleport variables
teleporting = False
teleport_start_time = 0
teleport_duration = 700  # 1 second

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
char_rect = char_frames[0].get_rect(center=(width // 2, height // 2))
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
enemy_frame_update_rate = 60  # Tăng giá trị này để làm chậm tốc độ GIF
teleport_distance = 200  # Khoảng cách tối thiểu để dịch chuyển

# Load the teleportation charging GIF
teleport_gif_path = 'D:/SpiritKnight/Sprites/black Wizard teleport v.gif'
teleport_gif = Image.open(teleport_gif_path)
teleport_frames = []
try:
    while True:
        teleport_frame = teleport_gif.copy()
        teleport_frame = teleport_frame.convert("RGBA")
        teleport_frames.append(pygame.image.fromstring(teleport_frame.tobytes(), teleport_frame.size, teleport_frame.mode))
        teleport_gif.seek(len(teleport_frames))  # Move to the next frame
except EOFError:
    pass

teleport_frame_index = 0
teleport_frame_timer = 0
teleport_frame_duration = 100  # Adjust as needed for frame duration

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
poison_frame_duration = 200  # Duration for each frame
show_poison_gif = False
poison_gif_display_timer = 0
poison_gif_delay = 2000  # 1.5 seconds delay before showing the poison GIF

# Poison area variables
poison_aoe_path = 'D:/SpiritKnight/Sprites/PoisonAoe.png'
poison_aoe_image = pygame.image.load(poison_aoe_path).convert_alpha()
poison_aoe_rect = poison_aoe_image.get_rect()
warning_circle_radius = poison_aoe_rect.width // 2  # Use the width of the poison area as the radius
show_poison_aoe = False
poison_aoe_timer = 0
poison_aoe_duration = 8000  # Duration the poison area remains on screen

# Teleport cooldown variables
teleport_cooldown = 4000  # 2 seconds in milliseconds
last_teleport_time = 0
first_teleport = True  # Track if the first teleportation has occurred

# Hàm tính toán góc quay để kẻ địch hướng về phía nhân vật
def calculate_angle(character_rect, enemy_rect):
    dx = character_rect.centerx - enemy_rect.centerx
    dy = character_rect.centery - enemy_rect.centery
    angle = math.atan2(dy, dx) * (180 / math.pi)
    return angle

# Hàm tính toán góc quay để kẻ địch hướng về phía nhân vật
def calculate_direction(character_rect, enemy_rect):
    dx = character_rect.centerx - enemy_rect.centerx
    return dx < 0 # True nếu nhân vật ở bên phải kẻ địch, False nếu ở bên trái

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

    # Update character frame
    frame_counter += 1
    if frame_counter >= frame_update_rate:
        frame_counter = 0
        frame_index = (frame_index + 1) % len(char_frames)

    # Update enemy frame
    enemy_frame_counter += clock.get_time()
    if enemy_frame_counter >= enemy_frame_update_rate:
        enemy_frame_counter = 0
        enemy_frame_index = (enemy_frame_index + 1) % len(enemy_frames)

    # Kiểm tra và lật ảnh kẻ địch nếu cần
    direction = calculate_direction(char_rect, enemy_rect)
    if direction:
        flipped_enemy_frame = enemy_frames[enemy_frame_index]
        flipped_teleport_frame = teleport_frames[teleport_frame_index]
    else:
        flipped_enemy_frame = pygame.transform.flip(enemy_frames[enemy_frame_index], True, False)
        flipped_teleport_frame = pygame.transform.flip(teleport_frames[teleport_frame_index], True, False)

    # Teleportation check
    current_time = pygame.time.get_ticks()
    if teleporting:
        if current_time - teleport_start_time >= teleport_duration:
            while True:
                new_x = random.randint(0, width - enemy_rect.width)
                new_y = random.randint(0, height - enemy_rect.height)
                if distance(char_rect, pygame.Rect(new_x, new_y, enemy_rect.width, enemy_rect.height)) > 650:
                    enemy_rect.x = new_x
                    enemy_rect.y = new_y
                    break
            teleporting = False
            last_teleport_time = current_time
            first_teleport = False
        else:
            teleport_frame_timer += clock.get_time()
            if teleport_frame_timer >= teleport_frame_duration:
                teleport_frame_timer = 0
                teleport_frame_index = (teleport_frame_index + 1) % len(teleport_frames)

            teleport_circle_angle = (teleport_circle_angle + rotation_speed) % 360
            rotated_teleport_circle = pygame.transform.rotate(teleport_circle_image, teleport_circle_angle)
            rotated_rect = rotated_teleport_circle.get_rect(center=enemy_rect.center)
            screen.blit(rotated_teleport_circle, rotated_rect)

            screen.blit(flipped_teleport_frame, enemy_rect)
    else:
        if (first_teleport or current_time - last_teleport_time >= teleport_cooldown) and distance(char_rect, enemy_rect) < teleport_distance:
            teleporting = True
            teleport_start_time = current_time
            teleport_frame_index = 0

    # Warning circle management
    warning_circle_timer += clock.get_time()
    if warning_circle_timer >= warning_circle_interval:
        warning_circle_timer = 0
        show_warning_circle = True
        warning_circle_visible_timer = 0
        warning_circle_position = char_rect.center
        poison_gif_display_timer = 0
        throw_poison_bottle = True
        poison_bottle_start_time = pygame.time.get_ticks()
        poison_bottle_target = warning_circle_position
        poison_bottle_rect.center = enemy_rect.center

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

    if throw_poison_bottle:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - poison_bottle_start_time
        if elapsed_time <= 1500:
            progress = elapsed_time / 1500
            new_x = enemy_rect.x + (poison_bottle_target[0] - enemy_rect.x) * progress
            new_y = enemy_rect.y + (poison_bottle_target[1] - enemy_rect.y) * progress
            poison_bottle_rect.center = (new_x, new_y)
            screen.blit(poison_bottle_image, poison_bottle_rect)
        else:
            throw_poison_bottle = False

    if show_poison_gif:
        poison_frame_timer += clock.get_time()
        if poison_frame_timer >= poison_frame_duration:
            poison_frame_timer = 0
            poison_frame_index = (poison_frame_index + 1) % len(poison_frames)
        poison_rect = poison_frames[poison_frame_index].get_rect(center=(warning_circle_position[0], warning_circle_position[1]))
        screen.blit(poison_frames[poison_frame_index], poison_rect)
        if poison_frame_index == len(poison_frames) - 1:
            show_poison_gif = False
            poison_frame_index = 0

    if show_poison_aoe:
        poison_aoe_timer += clock.get_time()
        screen.blit(poison_aoe_image, poison_aoe_rect)
        if poison_aoe_timer >= poison_aoe_duration:
            show_poison_aoe = False

    if not teleporting:
        screen.blit(flipped_enemy_frame, enemy_rect)
    else:
        screen.blit(flipped_teleport_frame, enemy_rect)

    if flipped:
        screen.blit(flipped_frames[frame_index], char_rect)
    else:
        screen.blit(char_frames[frame_index], char_rect)

    if show_poison_aoe and char_rect.colliderect(poison_aoe_rect):
        print("poisoned!")

    pygame.display.flip()
    clock.tick(60)
