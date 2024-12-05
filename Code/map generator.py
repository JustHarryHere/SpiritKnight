import pygame, sys
from PIL import Image 
import random

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Char
character_gif_path = 'C:/Users/Administrator/Documents/GitHub/SpiritKnight/SpiritKnight/Sprites/lil dude bigger.gif'
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

char_rect = char_frames[0].get_rect(center=(width // 2 , height // 2))
movement_speed = 5
frame_update_rate = 5
frame_counter = 0
frame_index = 0
flipped = False 

# PNG 
scale_factor = 0.2
obstacle_image = pygame.image.load('C:/Users/Administrator/Documents/GitHub/SpiritKnight/SpiritKnight/Sprites/tree.png')
obstacle_image = pygame.transform.scale(obstacle_image, (int(obstacle_image.get_width() * scale_factor), int(obstacle_image.get_height() * scale_factor)))
bg = pygame.image.load('C:/Users/Administrator/Documents/GitHub/SpiritKnight/SpiritKnight/Sprites/Map_placeholder (1).png')
bg_rect = bg.get_rect(topleft = (0,0))

# Define the spawning area for obstacles
spawn_area_x_min, spawn_area_x_max = width // 4, 3 * width // 4
spawn_area_y_min, spawn_area_y_max = height // 4, 3 * height // 4

# Tạo nhiều obstacle ngẫu nhiên
num_obstacles = 5
obstacles = []
for _ in range(num_obstacles):
    while True:
        x = random.randint(spawn_area_x_min, spawn_area_x_max)
        y = random.randint(spawn_area_y_min, spawn_area_y_max)
        obstacle_rect = obstacle_image.get_rect(center=(x, y))
        
        # Kiểm tra xem obstacle mới có giao với các obstacle đã tạo không
        if all(not obstacle_rect.colliderect(existing["rect"]) for existing in obstacles):
            obstacles.append({"sprite": obstacle_image, "rect": obstacle_rect})
            break

# Danh sách game_objects
game_objects = obstacles + [
    {"sprite": char_frames[0], "rect": char_rect}  # Nhân vật
]

shrink_factor = 100

while True: 
    screen.fill((0, 0, 0))
    screen.blit(bg, bg_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    
    move_x, move_y = 0, 0
    if keys[pygame.K_a]:
        move_x = -movement_speed
        flipped = False
    if keys[pygame.K_d]:
        move_x = movement_speed
        flipped = True
    if keys[pygame.K_w]:
        move_y = -movement_speed
    if keys[pygame.K_s]:
        move_y = movement_speed

    # Move character and check for collision with shrunken hitboxes
    char_rect.x += move_x
    for obstacle in obstacles:
        shrinked_rect = obstacle["rect"].inflate(-shrink_factor, -shrink_factor)
        if char_rect.colliderect(shrinked_rect):
            if move_x > 0:  # Moving right; Hit the left side of obstacle
                char_rect.right = shrinked_rect.left
            if move_x < 0:  # Moving left; Hit the right side of obstacle
                char_rect.left = shrinked_rect.right

    char_rect.y += move_y
    for obstacle in obstacles:
        shrinked_rect = obstacle["rect"].inflate(-shrink_factor, -shrink_factor)
        if char_rect.colliderect(shrinked_rect):
            if move_y > 0:  # Moving down; Hit the top side of obstacle
                char_rect.bottom = shrinked_rect.top
            if move_y < 0:  # Moving up; Hit the bottom side of obstacle
                char_rect.top = shrinked_rect.bottom

    # Frame update logic
    frame_counter += 1
    if frame_counter >= frame_update_rate:
        frame_counter = 0
        frame_index = (frame_index + 1) % len(char_frames)
    
    # Sort game objects by y-coordinate (z-index)
    game_objects.sort(key=lambda obj: obj["rect"].centery)

    # Update character sprite (check for flipping)
    for obj in game_objects:
        if obj["rect"] == char_rect:  # Character object
            obj["sprite"] = flipped_frames[frame_index] if flipped else char_frames[frame_index]

    # Draw objects in sorted order
    for obj in game_objects:
        screen.blit(obj["sprite"], obj["rect"])

        # Draw debug rects for shrunken hitboxes
        if obj in obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obj["rect"].inflate(-shrink_factor, -shrink_factor), 1)

    pygame.display.flip()
    clock.tick(60)