import pygame, sys
from PIL import Image

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Character animation frames
character_gif_path = 'C:/Users/Administrator/Documents/GitHub/SpiritKnight/Sprites/lil dude bigger.gif'
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

#Skeleton
skeleton_gif_path = 'C:/Users/Administrator/Documents/GitHub/SpiritKnight/Sprites/Skele.gif'
skeleton_gif = Image.open(skeleton_gif_path)
ske_frames = []
try:
    while True:
        ske_frame = skeleton_gif.copy()
        ske_frame = ske_frame.convert("RGBA")
        ske_frames.append(pygame.image.fromstring(ske_frame.tobytes(), ske_frame.size, ske_frame.mode))
        skeleton_gif.seek(len(ske_frames))  # Move to the next frame
except EOFError:
    pass

# Attack sprite sheet
attack_sprite_sheet = pygame.image.load('C:/Users/Administrator/Documents/GitHub/SpiritKnight/Sprites/Battery.png').convert_alpha()
attack_frames = []
sprite_width, sprite_height = attack_sprite_sheet.get_width() // 9, attack_sprite_sheet.get_height()

# Extract attack frames from sprite sheet
for i in range(9):
    frame = attack_sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
    attack_frames.append(frame)

# Flip attack frames for direction handling
flipped_attack_frames = [pygame.transform.flip(frame, True, False) for frame in attack_frames]

# Slash PNGs
slash_right = pygame.image.load('C:/Users/Administrator/Documents/GitHub/SpiritKnight/Sprites/wind burst.png')
slash_left = pygame.image.load('C:/Users/Administrator/Documents/GitHub/SpiritKnight/Sprites/wind burst2.png')

# Flip character frames for direction handling
flipped_frames = [pygame.transform.flip(char_frame, True, False) for char_frame in char_frames]

# Character initialization
char_rect = char_frames[0].get_rect(center=(width // 2, height // 2))
ske_rect = ske_frames[0].get_rect(center =(width//2 + 200, height//2))
frame_index = 0
attack_frame_index = 0
frame_counter = 0
frame_update_rate = 5
ske_frame_counter = 0
ske_frame_index = 0
flipped = False
attacking = False
attack_frame_counter = 0

# Slash-related variables
slash_rect = pygame.Rect(0, 0, slash_right.get_width(), slash_right.get_height())
slash_speed = 10
slash_active = False
slash_direction = 1  # 1 for right, -1 for left
slash_animation = False
slash_start_x = 0
max_slash_distance = 300  # Maximum distance the slash can travel

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            attacking = True
            attack_frame_index = 0
            attack_frame_counter = 0

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

    # Update boss frame
    ske_frame_counter += 1
    if ske_frame_counter >= frame_update_rate:
        ske_frame_counter = 0
        ske_frame_index = (ske_frame_index + 1) % len(ske_frames)

    # Display boss
    screen.blit(ske_frames[ske_frame_index], ske_rect)    

    if attacking:
        attack_frame_counter += 1
        if attack_frame_counter >= frame_update_rate:
            attack_frame_counter = 0
            attack_frame_index += 1
            if attack_frame_index >= len(attack_frames):
                attacking = False  # End attack animation
                attack_frame_index = 0
                slash_animation = True  # Start slash animation
                slash_active = True
                slash_rect.center = char_rect.center  # Start slash at character position
                slash_start_x = slash_rect.x  # Record the starting x position of the slash
                slash_direction = 1 if flipped else -1  # Move slash in the direction character is facing

        if flipped:
            attack_frame = pygame.transform.flip(attack_frames[attack_frame_index], True, False)
        else:
            attack_frame = attack_frames[attack_frame_index]
        
        screen.blit(attack_frame, char_rect)

    elif slash_animation:
        # Draw the character during the slash animation
        if flipped:
            screen.blit(flipped_frames[frame_index], char_rect)
        else:
            screen.blit(char_frames[frame_index], char_rect)

        # Move slash during attack
        if slash_active:
            slash_image = slash_right if slash_direction == 1 else slash_left
            slash_rect.x += slash_speed * slash_direction
            screen.blit(slash_image, slash_rect)

            # Deactivate slash after it moves a certain distance or goes off-screen
            if abs(slash_rect.x - slash_start_x) > max_slash_distance or slash_rect.x < 0 or slash_rect.x > width:
                slash_active = False
                slash_animation = False  # End slash animation
                slash_rect.topleft = (-1000,-1000)

    else:
        frame_counter += 1
        if frame_counter >= frame_update_rate:
            frame_counter = 0
            frame_index = (frame_index + 1) % len(char_frames)

        if flipped:
            screen.blit(flipped_frames[frame_index], char_rect)
        else:
            screen.blit(char_frames[frame_index], char_rect)

    if slash_rect.colliderect(ske_rect):
	    print('attacked')

    pygame.display.flip()
    clock.tick(60)