import pygame
import sys
import os
import random
import math
import time
from PIL import Image

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# File paths
character_gif_path = 'D:/SpiritKnight/Sprites/lil dude bigger.gif'
enemy_gif_path = 'D:/SpiritKnight/Sprites/Skele.gif'
arrow_image_path = 'D:/SpiritKnight/Sprites/arrow.png'

# Check if files exist
if not all(os.path.exists(path) for path in [character_gif_path, enemy_gif_path, arrow_image_path]):
    print("One or more files do not exist!")
    sys.exit()

# Function to load GIF frames using Pillow
def load_gif_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = gif.copy().convert('RGB')
            frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

# Load character GIF frames
char_frames = load_gif_frames(character_gif_path)

# Load enemy GIF frames
enemy_frames = load_gif_frames(enemy_gif_path)

# Load arrow image
arrow_image = pygame.image.load(arrow_image_path)
arrow_rect = arrow_image.get_rect()

# Character and enemy positions
char_rect = char_frames[0].get_rect(center=(WIDTH // 2, HEIGHT // 2))
enemy_rect = enemy_frames[0].get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

# Scale down character hitbox
hitbox_scale = 0.7  # Hitbox 70% of original size
char_hitbox = char_rect.inflate(-char_rect.width * (1 - hitbox_scale), -char_rect.height * (1 - hitbox_scale))

# Other variables
arrow_speed = 15
arrow_active = False
last_arrow_time = 0
arrow_cooldown = 2  # Cooldown 2 seconds
arrow_dx, arrow_dy = 0, 0
flipped = False
frame_index = 0
frame_counter = 0
frame_update_rate = 5
is_attacking = False
attack_frame_index = 0
attack_timer = 0
attack_duration = 1.0
attack_frame_rate = 0.1

# Main loop
while True:
    screen.fill((0, 0, 0))  # Clear screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move character
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

    # Update hitbox to match character position
    char_hitbox.center = char_rect.center

    # Initialize arrow if not active and cooldown has passed
    current_time = time.time()
    if not arrow_active and current_time - last_arrow_time > arrow_cooldown:
        arrow_rect.center = enemy_rect.center
        arrow_active = True
        last_arrow_time = current_time

        # Set arrow direction
        arrow_dx = char_rect.centerx - enemy_rect.centerx
        arrow_dy = char_rect.centery - enemy_rect.centery
        distance = math.hypot(arrow_dx, arrow_dy)
        if distance != 0:
            arrow_dx /= distance
            arrow_dy /= distance

    # Move arrow
    if arrow_active:
        arrow_rect.x += arrow_dx * arrow_speed
        arrow_rect.y += arrow_dy * arrow_speed

        # Check collision with character hitbox
        if char_hitbox.colliderect(arrow_rect):
            print("Character hit by arrow!")
            arrow_active = False

        # Check if arrow is off screen
        if (arrow_rect.right < 0 or arrow_rect.left > WIDTH or
            arrow_rect.bottom < 0 or arrow_rect.top > HEIGHT):
            arrow_active = False

    # Draw red line indicating arrow direction if not fired
    if not arrow_active:
        pygame.draw.line(screen, (255, 0, 0), enemy_rect.center, char_rect.center, 2)

    # Update frame index for animations
    frame_counter += 1
    if frame_counter >= frame_update_rate:
        frame_index = (frame_index + 1) % len(char_frames)
        frame_counter = 0

    # Display character and enemy
    if flipped:
        flipped_frame = pygame.transform.flip(char_frames[frame_index], True, False)
        screen.blit(flipped_frame, char_rect)
    else:
        screen.blit(char_frames[frame_index], char_rect)

    screen.blit(enemy_frames[frame_index % len(enemy_frames)], enemy_rect)

    # Display arrow if active
    if arrow_active:
        screen.blit(arrow_image, arrow_rect)

    # Update screen
    pygame.display.flip()
    clock.tick(60)
