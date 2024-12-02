import pygame, sys
from PIL import Image

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Character
character_gif_path = 'D:/SpiritKnight/Sprites/lil dude bigger.gif'
character_gif = Image.open(character_gif_path)
char_frames = []
try:
    while True:
        char_frame = character_gif.copy()
        char_frame = char_frame.convert("RGBA")
        char_frames.append(pygame.image.fromstring(char_frame.tobytes(), char_frame.size, char_frame.mode))
        character_gif.seek(len(char_frames))
except EOFError:
    pass

flipped_frames = [pygame.transform.flip(char_frame, True, False) for char_frame in char_frames]
char_rect = char_frames[0].get_rect(center=(width//2, height//2))

# Enemy
enemy_gif_path = 'D:/SpiritKnight/Sprites/black Wizard.gif'
enemy_gif = Image.open(enemy_gif_path)
enemy_frames = []
try:
    while True:
        enemy_frame = enemy_gif.copy()
        enemy_frame = enemy_frame.convert("RGBA")
        enemy_frames.append(pygame.image.fromstring(enemy_frame.tobytes(), enemy_frame.size, enemy_frame.mode))
        enemy_gif.seek(len(enemy_frames))
except EOFError:
    pass

enemy_rect = enemy_frames[0].get_rect(center=(width//2 + 200, height//2))

# Poison Bottle
poison_image_path = 'D:/SpiritKnight/Sprites/Poisoncloud.gif'
poison_image = pygame.image.load(poison_image_path)

# Poison Pool
poison_pool_image_path = 'D:/SpiritKnight/Sprites/Poisonpool.png'
poison_pool_image = pygame.image.load(poison_pool_image_path)
poison_pools = []

poison_rect = poison_image.get_rect(center=(enemy_rect.centerx, enemy_rect.centery))

poison_thrown = False
poison_timer = pygame.time.get_ticks()

frame_index = 0
frame_counter = 0
frame_update_rate = 5
enemy_frame_index = 0
enemy_frame_counter = 0
flipped = False

while True:
    screen.fill((0,0,0))
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

    # Update character frame index
    frame_counter += 1
    if frame_counter >= frame_update_rate:
        frame_counter = 0
        frame_index = (frame_index + 1) % len(char_frames)

    # Update enemy frame index
    enemy_frame_counter += 1
    if enemy_frame_counter >= frame_update_rate:
        enemy_frame_counter = 0
        enemy_frame_index = (enemy_frame_index + 1) % len(enemy_frames)

    # Throw poison every 4 seconds
    current_time = pygame.time.get_ticks()
    if current_time - poison_timer >= 4000:  # 4 seconds in milliseconds
        poison_thrown = True
        poison_rect = poison_image.get_rect(center=(enemy_rect.centerx, enemy_rect.centery))
        poison_timer = current_time

    if poison_thrown:
        poison_rect.x -= 5  # Move the poison bottle to the left

        # Check collision with character
        if poison_rect.colliderect(char_rect):
            print("Character hit by poison!")
            poison_pools.append(poison_pool_image.get_rect(center=char_rect.center))
            poison_thrown = False

    # Display character
    if flipped:
        screen.blit(flipped_frames[frame_index], char_rect)
    else:
        screen.blit(char_frames[frame_index], char_rect)

    # Display enemy
    screen.blit(enemy_frames[enemy_frame_index], enemy_rect)

    # Display poison bottle
    if poison_thrown:
        screen.blit(poison_image, poison_rect)

    # Display poison pools
    for poison_pool_rect in poison_pools:
        screen.blit(poison_pool_image, poison_pool_rect)

    pygame.display.flip()
    clock.tick(60)
