import pygame, sys
from PIL import Image

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Char
character_gif_path = 'C:/Users/Administrator/Documents/GitHub/SpiritKnight/Sprites/lil dude bigger.gif'
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

# Goblin idle
goblin_gif_path = 'C:/Users/Administrator/Documents/GitHub/SpiritKnight/Sprites/Goblin.gif'
goblin_gif = Image.open(goblin_gif_path)
goblin_idle_frames = []
try:
    while True:
        goblin_frame = goblin_gif.copy()
        goblin_frame = goblin_frame.convert("RGBA")
        goblin_idle_frames.append(pygame.image.fromstring(goblin_frame.tobytes(), goblin_frame.size, goblin_frame.mode))
        goblin_gif.seek(len(goblin_idle_frames))
except EOFError:
    pass

# Goblin attack
goblin_attack_gif_path = 'C:/Users/Administrator/Documents/GitHub/SpiritKnight/Sprites/GoblinAtk.gif'
goblin_attack_gif = Image.open(goblin_attack_gif_path)
goblin_attack_frames = []
try:
    while True:
        attack_frame = goblin_attack_gif.copy()
        attack_frame = attack_frame.convert("RGBA")
        goblin_attack_frames.append(pygame.image.fromstring(attack_frame.tobytes(), attack_frame.size, attack_frame.mode))
        goblin_attack_gif.seek(len(goblin_attack_frames))
except EOFError:
    pass

# Goblin setup
goblin_rect = goblin_idle_frames[0].get_rect(center=(width // 2 + 200, height // 2))
goblin_frame_index = 0
goblin_frame_counter = 0
goblin_state = "idle"  # States: "idle", "attack"

# Char setup
char_rect = char_frames[0].get_rect(center=(width // 2, height // 2))
frame_index = 0
frame_counter = 0
frame_update_rate = 5
flipped = False

# Frame update rates
idle_update_rate = 5
attack_update_rate = 8  # Faster for smoother attack

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Char movement
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

    # Char hitbox
    char_hitbox = pygame.Rect(
        char_rect.x + 5,  # Offset
        char_rect.y + 40,  # Offset
        char_rect.width - 10,  # Width
        char_rect.height - 38  # Height
    )
    
    # Goblin hitbox
    goblin_hitbox = pygame.Rect(
        goblin_rect.x + 15,
        goblin_rect.y + 10,
        goblin_rect.width - 30,
        goblin_rect.height - 20
    )

    # Check collision and update goblin state
    if goblin_hitbox.colliderect(char_hitbox) and goblin_state != "attack":
        goblin_state = "attack"
        goblin_frame_index = 0

    goblin_frame_counter += 1
    current_update_rate = attack_update_rate if goblin_state == "attack" else idle_update_rate
    if goblin_frame_counter >= current_update_rate:
        goblin_frame_counter = 0
        if goblin_state == "idle":
            goblin_frame_index = (goblin_frame_index + 1) % len(goblin_idle_frames)
        elif goblin_state == "attack":
            goblin_frame_index += 1
            if goblin_frame_index >= len(goblin_attack_frames):
                goblin_frame_index = len(goblin_attack_frames) - 1  # Stay on last frame
                # Add a delay or some other condition here to transition back to idle
                goblin_state = "idle"  # Change state after the attack finishes
                goblin_frame_index = 0  # Reset index for the idle animation


    # Display goblin
    if goblin_state == "idle":
        screen.blit(goblin_idle_frames[goblin_frame_index], goblin_rect)
    elif goblin_state == "attack":
        screen.blit(goblin_attack_frames[goblin_frame_index], goblin_rect)

    # Update char animation
    frame_counter += 1
    if frame_counter >= frame_update_rate:
        frame_counter = 0
        frame_index = (frame_index + 1) % len(char_frames)

    # Display char
    if flipped:
        screen.blit(flipped_frames[frame_index], char_rect)
    else:
        screen.blit(char_frames[frame_index], char_rect)

    # Draw hitboxes for debugging
    pygame.draw.rect(screen, (0, 255, 0), char_hitbox, 2)
    pygame.draw.rect(screen, (255, 0, 0), goblin_hitbox, 2)

    pygame.display.flip()
    clock.tick(60)
