import pygame, sys
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

flipped_frames = [pygame.transform.flip(char_frame, True, False) for char_frame in char_frames]
char_rect = char_frames[0].get_rect(center=(width // 2, height // 2))
frame_index = 0
frame_counter = 0
frame_update_rate = 5
flipped = False

# State management
is_paused = False  # True = Gameplay is paused

# Function to draw the settings popup
def draw_settings_popup():
    # Create a semi-transparent overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    #overlay.fill((0, 0, 0, 180))  # Black with transparency
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
    
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_paused = not is_paused  # Toggle pause state

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

    # Draw everything (always)
    screen.fill((0, 0, 0))  # Background
    if flipped:
        screen.blit(flipped_frames[frame_index], char_rect)
    else:
        screen.blit(char_frames[frame_index], char_rect)

    # Draw settings popup if paused
    if is_paused:
        draw_settings_popup()

    pygame.display.flip()
    clock.tick(60)
