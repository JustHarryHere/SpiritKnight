import pygame, sys, random
from PIL import Image

pygame.init()

# Screen settings
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Character GIF loading
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

flipped_frames = [pygame.transform.flip(char_frame, True, False) for char_frame in char_frames]
char_rect = char_frames[0].get_rect(center=(width // 2, height // 2))
goblin_rect = goblin_idle_frames[0].get_rect(center=(width // 2 + 200, height // 2))
frame_index = 0
frame_counter = 0
frame_update_rate = 5
goblin_frame_index = 0
goblin_frame_counter = 0
flipped = False

# State management
is_paused = False  # True = Gameplay is paused
stairway_visible = False  # True if stairway is visible

# Function to draw the settings popup
def draw_settings_popup():
    # Create a semi-transparent overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    screen.blit(overlay, (0, 0))
    
    # Draw the settings box
    popup_width, popup_height = 400, 300
    popup_rect = pygame.Rect(
        (width - popup_width) // 2, 
        (height - popup_height) // 2, 
        popup_width, popup_height
    )
    pygame.draw.rect(screen, (50, 50, 50), popup_rect)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect, 4)  # Border
    
    # Add text to the popup
    font = pygame.font.Font(None, 48)
    title = font.render("Settings", True, (255, 255, 255))
    screen.blit(
        title, 
        (popup_rect.centerx - title.get_width() // 2, popup_rect.top + 20)
    )

# PNG loading and scaling
scale_factor = 0.5
stairway = pygame.image.load('C:/Users/Administrator/Documents/GitHub/SpiritKnight/Sprites/Stairway.png') 
stairway = pygame.transform.scale(stairway, (int(stairway.get_width() * scale_factor), int(stairway.get_height() * scale_factor)))
stairway_rect = stairway.get_rect(center=(width // 2, height // 2))   
bg = pygame.image.load('C:/Users/Administrator/Documents/GitHub/SpiritKnight/Sprites/Map_placeholder (1).png')
bg_rect = bg.get_rect(topleft=(0,0))
obstacle_image_path = 'C:/Users/Administrator/Documents/GitHub/SpiritKnight/Sprites/tree.png'
obstacle_image = pygame.image.load(obstacle_image_path)
obstacle_image = pygame.transform.scale(obstacle_image, (int(obstacle_image.get_width() * 0.3), int(obstacle_image.get_height() * 0.3)))

# List to store obstacle rects
obstacles_rects = []

# Function to handle level transition
def next_level():
    global stairway_rect, char_rect, bg_rect, obstacles_rects
    # Move the stairway to a new position
    stairway_rect.topleft = (-1000,-1000)
    # Reset character position
    char_rect.center = (width // 2, height // 2)
    # Ensure background is drawn in the next level
    bg_rect = bg.get_rect(topleft=(0, 0))
    
    # Clear previous obstacles and spawn new ones randomly in the new level
    obstacles_rects.clear()
    for _ in range(random.randint(5, 10)): # Spawn between 5 and 10 obstacles
        obstacle_rect = obstacle_image.get_rect()
        obstacle_rect.centerx = random.randint(100, width - 100)
        obstacle_rect.centery = random.randint(100, height - 100)
        obstacles_rects.append(obstacle_rect)

# Main game loop
while True:
    screen.fill((0, 0, 0))  # Background
    screen.blit(bg, bg_rect)  # Draw background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_paused = not is_paused  # Toggle pause state
            elif event.key == pygame.K_r and char_rect.colliderect(stairway_rect):
                next_level()  # Move to the next level

    keys = pygame.key.get_pressed()

    # Update logic (only when not paused)
    if not is_paused:
        # Movement controls
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

        # Update character animation frame
        frame_counter += 1
        if frame_counter >= frame_update_rate:
            frame_counter = 0
            frame_index = (frame_index + 1) % len(char_frames)

        goblin_frame_counter += 1
        if goblin_frame_counter >= frame_update_rate:
            goblin_frame_counter = 0
            goblin_frame_index = (goblin_frame_index + 1) % len(goblin_idle_frames)  


    # Draw everything (always)

    screen.blit(goblin_idle_frames[goblin_frame_index], goblin_rect)

    if stairway_visible:
        screen.blit(stairway, stairway_rect) 

    if flipped:
        screen.blit(flipped_frames[frame_index], char_rect)
    else:
        screen.blit(char_frames[frame_index], char_rect)

    # Draw settings popup if paused
    if is_paused:
        draw_settings_popup()    

    if char_rect.colliderect(goblin_rect): 
        goblin_rect.topleft = (-1000,-1000)
        stairway_visible = True

    # Draw obstacles
    for obstacle_rect in obstacles_rects:
        screen.blit(obstacle_image, obstacle_rect)

    pygame.display.flip()
    clock.tick(60)