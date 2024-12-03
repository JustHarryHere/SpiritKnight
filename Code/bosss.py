import pygame, sys
from PIL import Image

pygame.init()
pygame.mixer.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Load character GIF
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

flipped_frames = [pygame.transform.flip(frame, True, False) for frame in char_frames]

# Load sprite_sheet tấn công
attack_sprite_sheet = pygame.image.load('D:/SpiritKnight/Sprites/lil dude big.png').convert_alpha()
attack_frames = []
sprite_width, sprite_height = attack_sprite_sheet.get_width() // 6, attack_sprite_sheet.get_height()

# Assuming 6 frames in the sprite sheet
for i in range(6):
    frame = attack_sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
    attack_frames.append(frame)

# Xoay frame tấn công
flipped_attack_frames = [pygame.transform.flip(frame, True, False) for frame in attack_frames]

# Load boss GIF
boss_gif_path = 'D:/SpiritKnight/Sprites/test_boss.gif'
boss_gif = Image.open(boss_gif_path)
boss_frames = []
try:
    while True:
        boss_frame = boss_gif.copy()
        boss_frame = boss_frame.convert("RGBA")
        boss_frame = boss_frame.resize((250,250), Image.Resampling.LANCZOS)
        boss_frames.append(pygame.image.fromstring(boss_frame.tobytes(), boss_frame.size, boss_frame.mode))
        boss_gif.seek(len(boss_frames))
except EOFError:
    pass

# Rectangles
char_rect = char_frames[0].get_rect(center=(width // 2 - 300, height // 2))
boss_rect = boss_frames[0].get_rect(center=(width // 2, height // 2))

# Variables
frame_index = 0
boss_frame_index = 0
frame_counter = 0
boss_frame_counter = 0
frame_update_rate = 5
attack_frame_rate = 2
flipped = False
max_hp = 100
remaining_hp = max_hp
hp_ratio = remaining_hp/max_hp
dmg = 10
attack_frame_counter = 0
attack_frame_index = 0
attacking = False
char_dmg = 50
boss_max_hp = 500
boss_remaining_hp = boss_max_hp
boss_hp_ratio = boss_remaining_hp/boss_max_hp
boss_hit_timer = 0
boss_hit_delay = 500


#PNG
scale_factor = 0.5
bg = pygame.image.load('D:/SpiritKnight/Sprites/Map_placeholder (1).png')
bg_rect = bg.get_rect(topleft = (0,0))
boss_health = pygame.image.load('D:/SpiritKnight/Sprites/pixil-frame-0.png')
boss_health = pygame.transform.scale(boss_health, (int(boss_health.get_width()*8), int(boss_health.get_height()*8)))
boss_health_rect = boss_health.get_rect(center = (width//2,60))
boss_hp_2 = pygame.image.load('D:/SpiritKnight/Sprites/pixil-frame-0 (1).png')
boss_hp_2 = pygame.transform.scale(boss_hp_2, (int(boss_hp_2.get_width()*8), int(boss_hp_2.get_height()*8)))
boss_hp_2_rect = boss_hp_2.get_rect(center = (width//2,60))
knife = pygame.image.load('D:/SpiritKnight/Sprites/knife.png')
knife = pygame.transform.scale(knife, (int(knife.get_width()*0.3), int(knife.get_height()*0.3)))
Hp_bar = pygame.image.load('D:/SpiritKnight/Sprites/HP1.png')
Hp_bar = pygame.transform.scale(Hp_bar, (int(Hp_bar.get_width()*scale_factor), int(Hp_bar.get_height()*scale_factor)))
Hp_bar_rect = Hp_bar.get_rect(topleft = (0,0))
Hp_2 = pygame.image.load('D:/SpiritKnight/Sprites/HP2.png')
Hp_2 = pygame.transform.scale(Hp_2, (int(Hp_2.get_width()*scale_factor), int(Hp_2.get_height()*scale_factor)))
Hp_2_rect = Hp_2.get_rect(topleft = (0,0))

# Knife variables
knife_speed = 10
knife_speed_2 = 9
knife_timer = 0
knife_interval = 5000 # 8 seconds in milliseconds
knives_left = []  # Knives moving to the left
knives_right = []  # Knives moving to the right
knives_up = []
knives_down = []
knives_bottom_left = []
knives_bottom_right = []
knives_top_right = []
knives_top_left = []

#Sound 
attack_sound = pygame.mixer.Sound('D:/SpiritKnight/Music/sword-sound-260274.wav')

while True:
    current_time = pygame.time.get_ticks()
    screen.fill((0, 0, 0))
    screen.blit(bg, bg_rect)
    screen.blit(Hp_bar, Hp_bar_rect)
    screen.blit(boss_health,boss_health_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Chuột phải
            attacking = True
            attack_frame_index = 0
            attack_frame_counter = 0
            attack_sound.play()

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

    if attacking:
        attack_frame_counter += 1
        if attack_frame_counter >= attack_frame_rate:
            attack_frame_counter = 0
            attack_frame_index += 1
            if attack_frame_index >= len(attack_frames):
                attacking = False  # Kết thúc hoạt ảnh tấn công
                attack_frame_index = 0
        if flipped:
            attack_frame = pygame.transform.flip(attack_frames[attack_frame_index], True, False)
        else:
            attack_frame = attack_frames[attack_frame_index]
        screen.blit(attack_frame, char_rect)
        if char_rect.colliderect(boss_rect) and current_time - boss_hit_timer > boss_hit_delay:
            boss_remaining_hp -= char_dmg
            boss_hp_ratio = boss_remaining_hp/boss_max_hp
            boss_hit_timer = current_time
    else:
        frame_counter += 1
        if frame_counter >= frame_update_rate:
            frame_counter = 0
            frame_index = (frame_index + 1) % len(char_frames)

        if flipped:
            screen.blit(flipped_frames[frame_index], char_rect)
        else:
            screen.blit(char_frames[frame_index], char_rect)

    # Update boss frame
    boss_frame_counter += 1
    if boss_frame_counter >= frame_update_rate:
        boss_frame_counter = 0
        boss_frame_index = (boss_frame_index + 1) % len(boss_frames)

    # Display boss
    screen.blit(boss_frames[boss_frame_index], boss_rect)

    # Shoot knives every 2 seconds
    if current_time - knife_timer > knife_interval:
        knife_timer = current_time
        # Knife moving left
        knife_rect_left = knife.get_rect(center=(boss_rect.centerx, boss_rect.centery))
        knives_left.append(knife_rect_left)
        # Knife moving right (rotated 180 degrees)
        knife_rect_right = knife.get_rect(center=(boss_rect.centerx, boss_rect.centery))
        rotated_knife = pygame.transform.rotate(knife, 180)  # Rotate knife by 180 degrees
        knives_right.append((rotated_knife, knife_rect_right))  # Store rotated knife with its rect
        #knife moving up
        knife_rect_up = knife.get_rect(center=(boss_rect.centerx, boss_rect.centery))
        up_knife = pygame.transform.rotate(knife,270)
        knives_up.append((up_knife, knife_rect_up))
        #knife moving down
        knife_rect_down = knife.get_rect(center=(boss_rect.centerx, boss_rect.centery))
        down_knife = pygame.transform.rotate(knife,90)
        knives_down.append((down_knife, knife_rect_down))
        #knife moving botton left
        knife_rect_bottom_left = knife.get_rect(center=(boss_rect.centerx, boss_rect.centery))
        bottom_left_knife = pygame.transform.rotate(knife,45)
        knives_bottom_left.append((bottom_left_knife, knife_rect_bottom_left))
        #knife moving bottom right
        knife_rect_bottom_right = knife.get_rect(center=(boss_rect.centerx, boss_rect.centery))
        bottom_right_knife = pygame.transform.rotate(knife,135)
        knives_bottom_right.append((bottom_right_knife, knife_rect_bottom_right))
        #knife moving top right
        knife_rect_top_right = knife.get_rect(center=(boss_rect.centerx, boss_rect.centery))
        top_right_knife = pygame.transform.rotate(knife,225)
        knives_top_right.append((top_right_knife, knife_rect_top_right))
        #knife moving top left
        knife_rect_top_left = knife.get_rect(center=(boss_rect.centerx, boss_rect.centery))
        top_left_knife = pygame.transform.rotate(knife,315)
        knives_top_left.append((top_left_knife, knife_rect_top_left))

    # Update knife positions (left)
    for knife_rect in knives_left:
        knife_rect.x -= knife_speed
        screen.blit(knife, knife_rect)
        pygame.draw.rect(screen, (0, 255, 0), knife_rect.inflate(-30, -100), 1)
        if char_rect.colliderect(knife_rect.inflate(-30, -100)):
            knife_rect.topleft = (-1000,-100)
            remaining_hp -= dmg
            hp_ratio = remaining_hp / max_hp
        elif knife_rect.x < 0:
            knives_left.remove(knife_rect)


    # Update knife positions (right)
    for rotated_knife, knife_rect in knives_right:
        knife_rect.x += knife_speed
        screen.blit(rotated_knife, knife_rect)
        pygame.draw.rect(screen, (0, 255, 0), knife_rect.inflate(-30, -100), 1)
        if char_rect.colliderect(knife_rect.inflate(-30, -100)):
            knife_rect.topleft = (-1000,-100)
            remaining_hp -= dmg
            hp_ratio = remaining_hp / max_hp
        elif knife_rect.x > width:
            knives_right.remove((rotated_knife, knife_rect))


    # Update knife positions (up)
    for up_knife, knife_rect in knives_up:
        knife_rect.y -= knife_speed
        screen.blit(up_knife, knife_rect)
        pygame.draw.rect(screen, (0, 255, 0), knife_rect.inflate(-30, -100), 1)
        if char_rect.colliderect(knife_rect.inflate(-30, -100)):
            knife_rect.topleft = (-1000,-100)
            remaining_hp -= dmg
            hp_ratio = remaining_hp / max_hp
        elif knife_rect.y < 0:
            knives_up.remove((up_knife, knife_rect))


    # Update knife positions (down)
    for down_knife, knife_rect in knives_down:
        knife_rect.y += knife_speed
        screen.blit(down_knife, knife_rect)
        pygame.draw.rect(screen, (0, 255, 0), knife_rect.inflate(-30, -100), 1)
        if char_rect.colliderect(knife_rect.inflate(-30, -100)):
            knife_rect.topleft = (-1000,-100)
            remaining_hp -= dmg
            hp_ratio = remaining_hp / max_hp
        elif knife_rect.y > height:
            knives_down.remove((down_knife, knife_rect))


    # Update knife positions (bottom left)
    for bottom_left_knife, knife_rect in knives_bottom_left:
        knife_rect.x -= knife_speed_2 
        knife_rect.y += knife_speed_2
        screen.blit(bottom_left_knife, knife_rect)
        pygame.draw.rect(screen, (0, 255, 0), knife_rect.inflate(-100, -100), 1)
        if char_rect.colliderect(knife_rect.inflate(-100, -100)):
            knife_rect.topleft = (-1000,-100)
            remaining_hp -= dmg
            hp_ratio = remaining_hp / max_hp
        elif knife_rect.x < 0 or knife_rect.y > height:
            knives_bottom_left.remove((bottom_left_knife, knife_rect))

    # Update knife positions (bottom right)
    for bottom_right_knife, knife_rect in knives_bottom_right:
        knife_rect.x += knife_speed_2
        knife_rect.y += knife_speed_2
        screen.blit(bottom_right_knife, knife_rect)
        pygame.draw.rect(screen, (0, 255, 0), knife_rect.inflate(-100, -100), 1)
        if char_rect.colliderect(knife_rect.inflate(-100, -100)):
            knife_rect.topleft = (-1000,-100)
            remaining_hp -= dmg 
            hp_ratio = remaining_hp / max_hp
        elif knife_rect.x > width or knife_rect.y > height:
            knives_bottom_right.remove((bottom_right_knife, knife_rect))

    # Update knife positions (top right)
    for top_right_knife, knife_rect in knives_top_right:
        knife_rect.x += knife_speed_2
        knife_rect.y -= knife_speed_2
        screen.blit(top_right_knife, knife_rect)
        pygame.draw.rect(screen, (0, 255, 0), knife_rect.inflate(-100, -100), 1)
        if char_rect.colliderect(knife_rect.inflate(-100, -100)):
            knife_rect.topleft = (-1000,-100)
            remaining_hp -= dmg 
            hp_ratio = remaining_hp / max_hp
        elif knife_rect.x > width or knife_rect.y < 0:
            knives_top_right.remove((top_right_knife, knife_rect))

    # Update knife positions (top left)
    for top_left_knife, knife_rect in knives_top_left:
        knife_rect.x -= knife_speed_2
        knife_rect.y -= knife_speed_2
        screen.blit(top_left_knife, knife_rect)
        pygame.draw.rect(screen, (0, 255, 0), knife_rect.inflate(-100, -100), 1)
        if char_rect.colliderect(knife_rect.inflate(-100, -100)):
            knife_rect.topleft = (-1000,-100)
            remaining_hp -= dmg 
            hp_ratio = remaining_hp / max_hp
        elif knife_rect.x < 0 or knife_rect.y < 0:
            knives_top_left.remove((top_left_knife, knife_rect))

    health_width = int(Hp_2_rect.width * (1 - hp_ratio))    
    if health_width > 0:
        remaining_health_rect = pygame.Rect(Hp_2_rect.right - health_width, Hp_2_rect.top, health_width, Hp_2_rect.height)
        Hp_2_partial = Hp_2.subsurface((Hp_2_rect.width - health_width, 0, health_width, Hp_2_rect.height))
        screen.blit(Hp_2_partial, remaining_health_rect)

    boss_health_width = int(boss_hp_2_rect.width * (1 - boss_hp_ratio))    
    if boss_health_width > 0:
        boss_remaining_health_rect = pygame.Rect(boss_hp_2_rect.right - boss_health_width, boss_hp_2_rect.top, boss_health_width, boss_hp_2_rect.height)
        boss_Hp_2_partial = boss_hp_2.subsurface((boss_hp_2_rect.width - boss_health_width, 0, boss_health_width, boss_hp_2_rect.height))
        screen.blit(boss_Hp_2_partial, boss_remaining_health_rect)

    # Font for displaying remaining HP
    font = pygame.font.Font('D:/SpiritKnight/Font/properhitboxglobal.ttf', 18)  
    hp_text_black = font.render(f"{remaining_hp}/{max_hp}", True, (0, 0, 0))  # Màu đen
    hp_text_rect = hp_text_black.get_rect(center=(240, 40))
    hp_text_white = font.render(f"{remaining_hp}/{max_hp}", True, (255, 255, 255))  # Màu trắng
    screen.blit(hp_text_black, hp_text_rect.move(2, 2))  
    screen.blit(hp_text_white, hp_text_rect)

    # Font for displaying remaining boss_HP
    font2 = pygame.font.Font('D:/SpiritKnight/Font/properhitboxglobal.ttf', 18)  
    boss_hp_text_black = font.render(f"{boss_remaining_hp}/{boss_max_hp}", True, (0, 0, 0))  # Màu đen
    boss_hp_text_rect = boss_hp_text_black.get_rect(center=(width//2, 63))
    boss_hp_text_white = font2.render(f"{boss_remaining_hp}/{boss_max_hp}", True, (255, 255, 255))  # Màu trắng
    screen.blit(boss_hp_text_black, boss_hp_text_rect.move(2, 2))  
    screen.blit(boss_hp_text_white, boss_hp_text_rect)

    if remaining_hp <= 0:
        game_over = True
        font_die = pygame.font.Font('D:/SpiritKnight/Font/Pixelmax-Regular.otf', 100)
        text_die_black = font_die.render(f"GAME OVER!", True, (0, 0, 0))  # Màu đen
        text_die_rect = text_die_black.get_rect(center = (width//2, height//2 - 200))
        text_die_white = font_die.render(f"GAME OVER!", True, (255, 255, 255))  # Màu trắng
        screen.blit(text_die_black, text_die_rect.move(10,10))
        screen.blit(text_die_white, text_die_rect)
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Hiển thị thông báo game over tại đây
            pygame.display.flip()

    pygame.display.flip()
    clock.tick(60)