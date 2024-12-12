import pygame, sys
from PIL import Image

pygame.init()
pygame.mixer.init()

width = 1280
height= 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

#Sound
pick_up_sound = pygame.mixer.Sound('D:/SpiritKnight/Music/Pop-_Minecraft-Sound_-Sound-Effect-for-editing.wav')

#Char
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

#Witch 
witch_gif_path = 'D:/SpiritKnight/Sprites/black Wizard.gif'
witch_gif = Image.open(witch_gif_path)
witch_frames = []
try:
    while True:
        witch_frame = witch_gif.copy()
        witch_frame = witch_frame.convert("RGBA")
        witch_frames.append(pygame.image.fromstring(witch_frame.tobytes(), witch_frame.size, witch_frame.mode))
        witch_gif.seek(len(witch_frames))  # Move to the next frame
except EOFError:
    pass

#Skeleton
skeleton_gif_path = 'D:/SpiritKnight/Sprites/Skele.gif'
skeleton_gif = Image.open(skeleton_gif_path)
skeleton_frames = []
try:
    while True:
        skeleton_frame = skeleton_gif.copy()
        skeleton_frame = skeleton_frame.convert("RGBA")
        skeleton_frames.append(pygame.image.fromstring(skeleton_frame.tobytes(), skeleton_frame.size, skeleton_frame.mode))
        skeleton_gif.seek(len(skeleton_frames))  # Move to the next frame
except EOFError:
    pass

#Speed_potion
speed_gif_path = 'D:\SpiritKnight\Sprites\wingedboot.gif'
speed_gif = Image.open(speed_gif_path)
speed_frames = []
try:
    while True:
        speed_frame = speed_gif.copy()
        speed_frame = speed_frame.convert("RGBA")
        speed_frame = speed_frame.resize((100,100), Image.Resampling.LANCZOS)
        speed_frames.append(pygame.image.fromstring(speed_frame.tobytes(), speed_frame.size, speed_frame.mode))
        speed_gif.seek(len(speed_frames))  # Move to the next frame
except EOFError:
    pass

#Damage potion
damage_gif_path = 'D:/SpiritKnight/Sprites/damage.gif'
damage_gif = Image.open(damage_gif_path)
damage_frames = []
try:
    while True:
        damage_frame = damage_gif.copy()
        damage_frame = damage_frame.convert("RGBA")
        damage_frame = damage_frame.resize((100,100), Image.Resampling.LANCZOS)
        damage_frames.append(pygame.image.fromstring(damage_frame.tobytes(), damage_frame.size, damage_frame.mode))
        damage_gif.seek(len(damage_frames))  # Move to the next frame
except EOFError:
    pass

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

flipped_frames = [pygame.transform.flip(char_frame, True, False) for char_frame in char_frames]
char_rect = char_frames[0].get_rect(center=(width//2 - 200, height//2))
witch_rect = witch_frames[0].get_rect(center = (width//2, height//2))
skeleton_rect = skeleton_frames[0].get_rect(center = (width//2, height//2 - 200))
speed_rect = speed_frames[0].get_rect(center = (width//2, height//2))
dmg_rect = damage_frames[0].get_rect(center =  (width//2, height//2 - 200))

#Variables
movement_speed = 5
frame_index = 0
frame_counter = 0
frame_update_rate = 5
attack_frame_counter = 0
attack_frame_index = 0
attack_frame_rate = 2
witch_frame_index = 0
witch_frame_counter = 0
skeleton_frame_counter = 0
skeleton_frame_index = 0
speed_frame_counter = 0
speed_frame_index = 0
dmg_frame_counter = 0
dmg_frame_index = 0
attacking = False
flipped = False

witch_health = 60
skeleton_health = 40
damage = 20
hit_timer = 0
hit_delay = 500
witch_killed = False
skeleton_killed = False

speed_boost_active = False
speed_boost_start_time = 0
speed_boost_duration = 2000

dmg_boost_active = False
dmg_boost_start_time = 0
dmg_boost_duration = 2000

#PNG 
scale_factor = 0.5
bg = pygame.image.load('D:/SpiritKnight/Sprites/Map_placeholder (1).png')
bg_rect = bg.get_rect(topleft = (0,0))
Hp_bar = pygame.image.load('D:/SpiritKnight/Sprites/HP1.png')
Hp_bar = pygame.transform.scale(Hp_bar, (int(Hp_bar.get_width()*scale_factor), int(Hp_bar.get_height()*scale_factor)))
Hp_bar_rect = Hp_bar.get_rect(topleft = (0,0))
Hp_2 = pygame.image.load('D:/SpiritKnight/Sprites/HP2.png')
Hp_2 = pygame.transform.scale(Hp_2, (int(Hp_2.get_width()*scale_factor), int(Hp_2.get_height()*scale_factor)))
Hp_2_rect = Hp_2.get_rect(topleft = (0,0))

while True:
    current_time = pygame.time.get_ticks()
    screen.fill((0,0,0))
    screen.blit(bg, bg_rect)
    screen.blit(Hp_bar, Hp_bar_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Chuột trái
            attacking = True
            attack_frame_index = 0
            attack_frame_counter = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        char_rect.x -= movement_speed
        flipped = False
    if keys[pygame.K_d]:
        char_rect.x += movement_speed
        flipped = True
    if keys[pygame.K_w]:
        char_rect.y -= movement_speed
    if keys[pygame.K_s]:
        char_rect.y += movement_speed
    if keys[pygame.K_f]:
        if char_rect.colliderect(speed_rect) and not speed_boost_active:
            pick_up_sound.play()
            speed_rect.topleft = (-1000, -1000)  # Move the speed potion off screen
            movement_speed = 10
            speed_boost_active = True
            speed_boost_start_time = current_time
        if char_rect.colliderect(dmg_rect) and not dmg_boost_active:
            pick_up_sound.play()
            dmg_rect.topleft = (-1000, -1000)
            damage = 40 
            dmg_boost_active = True
            dmg_boost_start_time = current_time

    # Disable speed boost after duration
    if speed_boost_active and current_time - speed_boost_start_time > speed_boost_duration:
        movement_speed = 5  # Reset to normal speed
        speed_boost_active = False 
    #Disable dmg_boost
    if dmg_boost_active and current_time - dmg_boost_start_time > dmg_boost_duration:
        damage = 20
        dmg_boost_active = False

    # Update witch frame
    witch_frame_counter += 1
    if witch_frame_counter >= frame_update_rate:
        witch_frame_counter = 0
        witch_frame_index = (witch_frame_index + 1) % len(witch_frames)

    # Display witch
    screen.blit(witch_frames[witch_frame_index], witch_rect)

    # Update skeleton frame
    skeleton_frame_counter += 1
    if skeleton_frame_counter >= frame_update_rate:
        skeleton_frame_counter = 0
        skeleton_frame_index = (skeleton_frame_index + 1) % len(skeleton_frames)

    # Display skeleton
    screen.blit(skeleton_frames[skeleton_frame_index], skeleton_rect)
    
    if witch_killed:
        speed_frame_counter += 1
        if speed_frame_counter >= frame_update_rate:
            speed_frame_counter = 0
            speed_frame_index = (speed_frame_index + 1) % len(speed_frames)
        screen.blit(speed_frames[speed_frame_index], speed_rect)

    if skeleton_killed:
        dmg_frame_counter += 1
        if dmg_frame_counter >= frame_update_rate:
            dmg_frame_counter = 0
            dmg_frame_index = (dmg_frame_index + 1) % len(damage_frames)
        screen.blit(damage_frames[dmg_frame_index], dmg_rect)

    #Display character
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
        if char_rect.colliderect(witch_rect) and current_time - hit_timer > hit_delay:
            witch_health -= damage
            hit_timer = current_time
            if witch_health <= 0:
                witch_rect.topleft = (-1000,-1000)
                witch_killed = True
        elif char_rect.colliderect(skeleton_rect) and current_time - hit_timer > hit_delay:
            skeleton_health -= damage
            hit_timer = current_time
            if skeleton_health <= 0:
                skeleton_rect.topleft = (-1000,-1000)
                skeleton_killed = True
    else:
        frame_counter += 1
        if frame_counter >= frame_update_rate:
            frame_counter = 0
            frame_index = (frame_index + 1) % len(char_frames)

        if flipped:
            screen.blit(flipped_frames[frame_index], char_rect)
        else:
            screen.blit(char_frames[frame_index], char_rect)

    pygame.display.flip()
    clock.tick(60)
    