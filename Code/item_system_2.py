import pygame, sys
from PIL import Image

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Item
potion_gif_path = 'D:/SpiritKnight/Sprites/Trans.png'
potion_gif = Image.open(potion_gif_path)
potion_frames = []
try:
    while True:
        potion_frame = potion_gif.copy()
        potion_frame = potion_frame.convert("RGBA")
        potion_frame = potion_frame.resize((60, 60), Image.Resampling.LANCZOS)
        potion_frames.append(pygame.image.fromstring(potion_frame.tobytes(), potion_frame.size, potion_frame.mode))
        potion_gif.seek(len(potion_frames))  # Move to the next frame
except EOFError:
    pass

speed_potion_gif_path = 'D:/SpiritKnight/Sprites/speed_potion (1).png'
speed_potion_gif = Image.open(speed_potion_gif_path)
speed_potion_frames = []
try:
    while True:
        speed_potion_frame = speed_potion_gif.copy()
        speed_potion_frame = speed_potion_frame.convert("RGBA")
        speed_potion_frame = speed_potion_frame.resize((60, 60), Image.Resampling.LANCZOS)
        speed_potion_frames.append(pygame.image.fromstring(speed_potion_frame.tobytes(), speed_potion_frame.size, speed_potion_frame.mode))
        speed_potion_gif.seek(len(potion_frames))  # Move to the next frame
except EOFError:
    pass

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
potion_rect = potion_frames[0].get_rect(center=(width // 2 + 100, height // 2 + 100))
potion_rect2 = potion_frames[0].get_rect(center=(width // 2 - 100, height // 2 - 100))
potion_rect3 = potion_frames[0].get_rect(center = (width//2 - 200, height//2))
speed_potion_rect = speed_potion_frames[0].get_rect(center = (width//2 + 300, height//2))
frame_index = 0
frame_counter = 0
frame_update_rate = 5
flipped = False
picked_up_potion = False
picked_up_speed_potion = False
potion_frame_counter = 0
potion_frame_index = 0
speed_potion_frame_counter = 0
speed_potion_frame_index = 0
item_count = 0
item2_count = 0 

# PNG
scale_factor = 0.5
bg = pygame.image.load('D:/SpiritKnight/Sprites/Map_placeholder (1).png').convert_alpha()
bg_rect = bg.get_rect(topleft=(0, 0))
HP = pygame.image.load('D:/SpiritKnight/Sprites/HP1.png').convert_alpha()
HP = pygame.transform.scale(HP, (int(HP.get_width() * scale_factor), int(HP.get_height() * scale_factor)))
HP_rect = HP.get_rect(topleft=(0, 0))
Inv = pygame.image.load('D:/SpiritKnight/Sprites/inv.png').convert_alpha()
Inv = pygame.transform.scale(Inv, (int(Inv.get_width() * scale_factor), int(Inv.get_height() * scale_factor)))
Inv_rect = Inv.get_rect(topleft=(0, 0))
potion_png = pygame.image.load('D:/SpiritKnight/Sprites/Trans.png').convert_alpha()
potion_png = pygame.transform.scale(potion_png, (int(potion_png.get_width() * 0.15), int(potion_png.get_height() * 0.15)))
potion_png_rect = potion_png.get_rect(center=(75, 78))
speed_potion_png = pygame.image.load('D:/SpiritKnight/Sprites/speed_potion (1).png')
speed_potion_png = pygame.transform.scale(speed_potion_png, (int(speed_potion_png.get_width() * 0.15), int(speed_potion_png.get_height() * 0.15)))
speed_potion_png_rect = speed_potion_png.get_rect(center = (115, 78))

while True:
    screen.fill((0, 0, 0))
    screen.blit(bg, bg_rect)
    screen.blit(HP, HP_rect)
    screen.blit(Inv, Inv_rect)
    
    if picked_up_potion:
        screen.blit(potion_png, potion_png_rect)
    if picked_up_speed_potion:
        screen.blit(speed_potion_png, speed_potion_png_rect)

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

    # Check for item pickup
    if keys[pygame.K_f]:
        if char_rect.colliderect(potion_rect):
            potion_rect.topleft = (-1000, -1000)
            picked_up_potion = True
            item_count += 1
        if char_rect.colliderect(potion_rect2):
            potion_rect2.topleft = (-1000, -1000)
            picked_up_potion = True
            item_count += 1
        if char_rect.colliderect(potion_rect3):
            potion_rect3.topleft = (-1000,-1000)
            picked_up_potion = True
            item_count += 1
        if char_rect.colliderect(speed_potion_rect):
            speed_potion_rect.topleft = (-1000,-1000)
            picked_up_speed_potion = True
            item2_count += 1

    # Drop item
    if keys[pygame.K_g] and item_count > 0:
        if potion_rect.topleft == (-1000, -1000):
            potion_rect.center = (char_rect.centerx + 50, char_rect.centery)
        elif potion_rect2.topleft == (-1000, -1000):
            potion_rect2.center = (char_rect.centerx + 50, char_rect.centery)
        elif potion_rect3.topleft == (-1000,-1000):
            potion_rect3.center = (char_rect.centerx + 50, char_rect.centery)
        item_count -= 1
        if item_count == 0:
            picked_up_potion = False

    # Drop item2
    if keys[pygame.K_c] and item2_count > 0:
        if speed_potion_rect.topleft == (-1000, -1000):
            speed_potion_rect.center = (char_rect.centerx + 50, char_rect.centery)
        item2_count -= 1
        if item2_count == 0:
            picked_up_speed_potion = False

    # Display item in inventory
    if item_count > 0:
        screen.blit(potion_png, potion_png_rect)

    # Update potion frame
    potion_frame_counter += 1
    if potion_frame_counter >= frame_update_rate:
        potion_frame_counter = 0
        potion_frame_index = (potion_frame_index + 1) % len(potion_frames)    

    # Display potions
    screen.blit(potion_frames[potion_frame_index], potion_rect)
    screen.blit(potion_frames[potion_frame_index], potion_rect2)
    screen.blit(potion_frames[potion_frame_index], potion_rect3)
    
    # Update speed potion frame
    speed_potion_frame_counter += 1
    if speed_potion_frame_counter >= frame_update_rate:
        speed_potion_frame_counter = 0
        speed_potion_frame_index = (speed_potion_frame_index + 1) % len(speed_potion_frames)

    # Display  speed potions
    screen.blit(speed_potion_frames[speed_potion_frame_index], speed_potion_rect)

    # Update character frame
    frame_counter += 1
    if frame_counter >= frame_update_rate:
        frame_counter = 0
        frame_index = (frame_index + 1) % len(char_frames)

    # Display character
    if flipped:
        screen.blit(flipped_frames[frame_index], char_rect)
    else:
        screen.blit(char_frames[frame_index], char_rect)

    # Display item count
    font = pygame.font.Font('D:/SpiritKnight/Font/properhitboxglobal.ttf', 12)  
    item_text_black = font.render(f"{item_count}", True, (0, 0, 0))  # Black color
    item_text_rect = item_text_black.get_rect(center=(90, 95))
    item_text_white = font.render(f"{item_count}", True, (255, 255, 255))  # White color
    screen.blit(item_text_black, item_text_rect.move(2, 2))  
    screen.blit(item_text_white, item_text_rect)

    # Display item2 count
    font2 = pygame.font.Font('D:/SpiritKnight/Font/properhitboxglobal.ttf', 12)  
    item2_text_black = font2.render(f"{item2_count}", True, (0, 0, 0))  # Black color
    item2_text_rect = item_text_black.get_rect(center=(130, 95))
    item2_text_white = font2.render(f"{item2_count}", True, (255, 255, 255))  # White color
    screen.blit(item2_text_black, item2_text_rect.move(2, 2))  
    screen.blit(item2_text_white, item2_text_rect)

    pygame.display.flip()
    clock.tick(60) 