#def spawn_boss():
import pygame, sys
from PIL import Image
import os

pygame.init()
pygame.mixer.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def update_dash_frame_index():
    global dash_frame_index
    dash_frame_index += 1
    if dash_frame_index >= len(flipped_dash_frames):
        dash_frame_index = 0  # Reset or wrap around the index

script_dir = os.path.dirname(os.path.abspath(__file__))
Sprites_folder = os.path.join(script_dir, '..', 'Sprites')
Music_folder = os.path.join(script_dir, '..', 'Music')
Font_folder = os.path.join(script_dir, '..', 'Font')

# Load character GIF
character_gif_path = os.path.join(Sprites_folder, 'lil dude bigger.gif')
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
attack_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'lil dude big.png')).convert_alpha()
attack_frames = []
sprite_width, sprite_height = attack_sprite_sheet.get_width() // 6, attack_sprite_sheet.get_height()

# Assuming 6 frames in the sprite sheet
for i in range(6):
    frame = attack_sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
    attack_frames.append(frame)

# Xoay frame tấn công
flipped_attack_frames = [pygame.transform.flip(frame, True, False) for frame in attack_frames]

# Load sprite_sheet nhận sát thương
attacked_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'Ouch.png')).convert_alpha()
attacked_frames = []
attacked_sprite_width, attacked_sprite_height = attacked_sprite_sheet.get_width() // 7, attacked_sprite_sheet.get_height()

# Assuming 6 frames in the sprite sheet
for i in range(7):
    attacked_frame = attacked_sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
    attacked_frames.append(attacked_frame)

# Load boss GIF
boss_gif_path = os.path.join(Sprites_folder, 'Slime king smily.gif')
boss_gif = Image.open(boss_gif_path)
boss_frames = []
try:
    while True:
        boss_frame = boss_gif.copy()
        boss_frame = boss_frame.convert("RGBA")
        boss_frame = boss_frame.resize((400,400), Image.Resampling.LANCZOS)
        boss_frames.append(pygame.image.fromstring(boss_frame.tobytes(), boss_frame.size, boss_frame.mode))
        boss_gif.seek(len(boss_frames))
except EOFError:
    pass

# Load new boss GIF for weakened state
weak_boss_gif_path = os.path.join(Sprites_folder, 'phase 2 idle.gif')  # Đường dẫn tới hình ảnh boss yếu
weak_boss_gif = Image.open(weak_boss_gif_path)
weak_boss_frames = []
try:
    while True:
        weak_boss_frame = weak_boss_gif.copy()
        weak_boss_frame = weak_boss_frame.convert("RGBA")
        weak_boss_frame = weak_boss_frame.resize((400, 400), Image.Resampling.LANCZOS)
        weak_boss_frames.append(pygame.image.fromstring(weak_boss_frame.tobytes(), weak_boss_frame.size, weak_boss_frame.mode))
        weak_boss_gif.seek(len(weak_boss_frames))
except EOFError:
    pass

#Load jumping gif
boss_jump_gif_path = os.path.join(Sprites_folder, 'jump.gif')
boss_jump_gif = Image.open(boss_jump_gif_path)
boss_jump_frames = []
try:
    while True:
        boss_jump_frame = boss_jump_gif.copy()
        boss_jump_frame = boss_jump_frame.convert("RGBA")
        boss_jump_frame = boss_jump_frame.resize((400,400), Image.Resampling.LANCZOS)
        boss_jump_frames.append(pygame.image.fromstring(boss_jump_frame.tobytes(), boss_jump_frame.size, boss_jump_frame.mode))
        boss_jump_gif.seek(len(boss_jump_frames))
except EOFError:
    pass



# Load sprite_sheet lướt
dash_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'Dash.png')).convert_alpha()
dash_frames = []
dash_width, dash_height = dash_sprite_sheet.get_width() // 8, dash_sprite_sheet.get_height()

# Assuming 8 frames in the sprite sheet
for i in range(8):
    dash_frame = dash_sprite_sheet.subsurface((i * dash_width, 0, dash_width, dash_height))
    dash_frames.append(dash_frame)

# Xoay frame lướt
flipped_dash_frames = [pygame.transform.flip(dash_frame, True, False) for dash_frame in dash_frames]

#Biến
dash_frame_counter = 0
dash_frame_index = 0
dash_frame_update_rate = 2
dashing = False
dash_cooldown = False
last_dash_time = 0
dash_speed = 10
dash_cooldown_time = 1500


# Load sprite_sheet charge
charge_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'Battery.png')).convert_alpha()
charge_frames = []
charge_width, charge_height = charge_sprite_sheet.get_width() // 9, charge_sprite_sheet.get_height()

# Assuming 9 frames in the sprite sheet
for i in range(9):
    charge_frame = charge_sprite_sheet.subsurface((i * charge_width, 0, charge_width, charge_height))
    charge_frames.append(charge_frame)

# Xoay frame lướt
flipped_charge_frames = [pygame.transform.flip(charge_frame, True, False) for charge_frame in charge_frames]

#Biến
charge_frame_counter = 0 
charge_frame_index = 0 
charge_frame_update_rate = 4
charging = False
charge_cooldown = False
last_charge_time = 0 
charge_cooldown_time = 2000

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
dmg = 5
attack_frame_counter = 0
attack_frame_index = 0
attacking = False
char_dmg = 25
boss_max_hp = 500
boss_remaining_hp = boss_max_hp
boss_hp_ratio = boss_remaining_hp/boss_max_hp
boss_hit_timer = 0
boss_hit_delay = 500
taking_damage = False
damage_frame_counter = 0
damage_frame_index = 0
damage_frame_rate = 3
boss_attacking = False
boss_jump_timer = 0
boss_attack_interval = 10000  # 10 giây
boss_jump_frame_index = 0
boss_jump_frame_counter = 0
boss_jump_frame_rate = 5
boss_damage = 0

#PNG
scale_factor = 0.5
bg = pygame.image.load(os.path.join(Sprites_folder, 'Map_placeholder (1).png'))
bg_rect = bg.get_rect(topleft = (0,0))
boss_health = pygame.image.load(os.path.join(Sprites_folder, 'king slime HP1.png'))
boss_health = pygame.transform.scale(boss_health, (int(boss_health.get_width()*0.7), int(boss_health.get_height()*0.7)))
boss_health_rect = boss_health.get_rect(center = (width//2,50))
boss_hp_2 = pygame.image.load(os.path.join(Sprites_folder, 'king slime HP2.png'))
boss_hp_2 = pygame.transform.scale(boss_hp_2, (int(boss_hp_2.get_width()*0.7), int(boss_hp_2.get_height()*0.7)))
boss_hp_2_rect = boss_hp_2.get_rect(center = (width//2,50))
knife = pygame.image.load(os.path.join(Sprites_folder, 'bullet.png'))
knife = pygame.transform.scale(knife, (int(knife.get_width()*0.3), int(knife.get_height()*0.3)))
Hp_bar = pygame.image.load(os.path.join(Sprites_folder, 'HP1.png'))
Hp_bar = pygame.transform.scale(Hp_bar, (int(Hp_bar.get_width()*scale_factor), int(Hp_bar.get_height()*scale_factor)))
Hp_bar_rect = Hp_bar.get_rect(topleft = (0,0))
Hp_2 = pygame.image.load(os.path.join(Sprites_folder, 'HP2.png'))
Hp_2 = pygame.transform.scale(Hp_2, (int(Hp_2.get_width()*scale_factor), int(Hp_2.get_height()*scale_factor)))
Hp_2_rect = Hp_2.get_rect(topleft = (0,0))
Charge_ui = pygame.image.load(os.path.join(Sprites_folder, 'Skill icon.png'))
Charge_ui = pygame.transform.scale(Charge_ui, (int(Charge_ui.get_width()*scale_factor), int(Charge_ui.get_height()*scale_factor)))
Charge_ui_rect = Charge_ui.get_rect(center = (1220, 45))
Skill_frame = pygame.image.load(os.path.join(Sprites_folder, 'Frame2.png'))
Skill_frame = pygame.transform.scale(Skill_frame, (int(Skill_frame.get_width()*scale_factor), int(Skill_frame.get_height()*scale_factor)))
Skill_frame_rect = Skill_frame.get_rect(center = (1220, 45))
Charge_cd_ui = pygame.image.load(os.path.join(Sprites_folder, 'Skill cooldown.png'))
Charge_cd_ui = pygame.transform.scale(Charge_cd_ui, (int(Charge_cd_ui.get_width()*scale_factor), int(Charge_cd_ui.get_height()*scale_factor)))
Charge_cd_ui_rect = Charge_cd_ui.get_rect(center = (1220, 45))
Dash_ui = pygame.image.load(os.path.join(Sprites_folder, 'Dash icon2.png'))
Dash_ui = pygame.transform.scale(Dash_ui, (int(Dash_ui.get_width()*scale_factor), int(Dash_ui.get_height()*scale_factor)))
Dash_ui_rect = Dash_ui.get_rect(center = (1120, 45))
Dash_frame = pygame.image.load(os.path.join(Sprites_folder, 'Frame1.png'))
Dash_frame = pygame.transform.scale(Dash_frame, (int(Dash_frame.get_width()*scale_factor), int(Dash_frame.get_height()*scale_factor)))
Dash_frame_rect = Dash_frame.get_rect(center = (1120, 45))
Dash_cd_ui = pygame.image.load(os.path.join(Sprites_folder, 'Dash cooldown.png'))
Dash_cd_ui = pygame.transform.scale(Dash_cd_ui, (int(Dash_cd_ui.get_width()*scale_factor), int(Dash_cd_ui.get_height()*scale_factor)))
Dash_cd_ui_rect = Dash_cd_ui.get_rect(center = (1120, 45))

# Knife variables
knife_speed = 10
knife_speed_2 = 9
knife_timer = 0
knife_interval = 5000 # 5 seconds in milliseconds
knives_left = []  # Knives moving to the left
knives_right = []  # Knives moving to the right
knives_up = []
knives_down = []
knives_bottom_left = []
knives_bottom_right = []
knives_top_right = []
knives_top_left = []

#Sound 
attack_sound = pygame.mixer.Sound(os.path.join(Music_folder, 'sword-sound-260274.wav'))
getting_hit_sound = pygame.mixer.Sound(os.path.join(Music_folder, 'Ouch.wav'))

while True:
    current_time = pygame.time.get_ticks()
    screen.fill((0, 0, 0))
    screen.blit(bg, bg_rect)
    screen.blit(Hp_bar, Hp_bar_rect)
    screen.blit(boss_health,boss_health_rect)
    screen.blit(Charge_ui, Charge_ui_rect)
    screen.blit(Skill_frame, Skill_frame_rect)
    screen.blit(Dash_ui, Dash_ui_rect)
    screen.blit(Dash_frame, Dash_frame_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Chuột trái
                attacking = True
                attack_frame_index = 0
                attack_frame_counter = 0
                attack_sound.play()
            if event.button == 3 and not charge_cooldown:
                charge_cooldown = True
                charging = True 
                charge_frame_index = 0
                charge_frame_counter = 0
                last_charge_time = current_time
    min_x, max_x = 0, width - 15 - char_rect.width
    top_border, bottom_border = 70, height - 32 - char_rect.height

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        char_rect.x = max(min_x, char_rect.x - 5)
        flipped = False
    if keys[pygame.K_d]:
        char_rect.x = min(max_x, char_rect.x + 5)
        flipped = True
    if keys[pygame.K_w]:
        char_rect.y = max(top_border, char_rect.y -5)
    if keys[pygame.K_s]:
        char_rect.y = min(bottom_border, char_rect.y + 5)
    if keys[pygame.K_LSHIFT] and not dashing and not dash_cooldown: 
        dash_cooldown = True
        last_dash_time = current_time
        dashing = True
        dash_frame_index = 0
        dash_frame_counter = 0

    # Boss nhảy tấn công
    if boss_attacking:
        # Xử lý hoạt ảnh nhảy
        boss_jump_frame_counter += 1
        if boss_jump_frame_counter >= boss_jump_frame_rate:
            boss_jump_frame_counter = 0
            boss_jump_frame_index = (boss_jump_frame_index + 1) % len(boss_jump_frames)

        # Kiểm tra nếu boss đã nhảy xong
        if boss_jump_frame_index >= len(boss_jump_frames):
            boss_attacking = False  # Quay lại trạng thái bình thường
            boss_jump_frame_index = 0  # Reset hoạt ảnh nhảy
            boss_jump_timer = current_time  # Cập nhật thời gian tấn công tiếp theo
    
        else:
            # Di chuyển boss về phía nhân vật
            boss_rect.x += (char_rect.x - boss_rect.x) // 50  
            boss_rect.y += (char_rect.y - boss_rect.y) // 50

            # Vẽ hoạt ảnh nhảy
            screen.blit(boss_jump_frames[boss_jump_frame_index], boss_rect)


            # Kết thúc hoạt ảnh nhảy
            if boss_jump_frame_index == len(boss_jump_frames) - 1:  
                boss_attacking = False
                boss_jump_timer = current_time

            # Kiểm tra va chạm và gây sát thương
            if char_rect.colliderect(boss_hitbox) and not taking_damage:
                taking_damage = True
                remaining_hp -= boss_damage
                hp_ratio = remaining_hp / max_hp
                getting_hit_sound.play()

    else:
        # Kiểm tra thời gian tấn công
        if current_time - boss_jump_timer > boss_attack_interval:
            boss_attacking = True
            boss_jump_frame_index = 0
            boss_jump_frame_counter = 0
        else: 
            if boss_remaining_hp <= 250:
                # Boss trong trạng thái yếu
                knife_interval = 2000
                boss_attack_interval = 4000
                dmg = 10
                boss_damage = 0 
                knife = pygame.image.load(os.path.join(Sprites_folder, 'knife.png')).convert_alpha()
                knife = pygame.transform.scale(knife, (int(knife.get_width()*0.2), int(knife.get_height()*0.2)))

                # Vẽ boss yếu
                boss_frame_counter += 1
                if boss_frame_counter >= frame_update_rate:
                    boss_frame_counter = 0
                    boss_frame_index = (boss_frame_index + 1) % len(weak_boss_frames)
                screen.blit(weak_boss_frames[boss_frame_index], boss_rect)
            else: 
                # Vẽ boss bình thường nếu không tấn công
                boss_frame_counter += 1
                if boss_frame_counter >= frame_update_rate:
                    boss_frame_counter = 0
                    boss_frame_index = (boss_frame_index + 1) % len(boss_frames)
                screen.blit(boss_frames[boss_frame_index], boss_rect)

    # Vẽ rect của boss để debug
    boss_hitbox = boss_rect.inflate(-200,-200)
    
    if taking_damage:
        damage_frame_counter += 1
        if damage_frame_counter >= damage_frame_rate:
            damage_frame_counter = 0
            damage_frame_index += 1
            if damage_frame_index >= len(attacked_frames):
                taking_damage = False  # Kết thúc hoạt ảnh nhận sát thương
                damage_frame_index = 0

    # Hiển thị khung hình hoạt ảnh nhận sát thương
        if flipped:
            damage_frame = pygame.transform.flip(attacked_frames[damage_frame_index], True, False)
        else:
            damage_frame = attacked_frames[damage_frame_index]
        screen.blit(damage_frame, char_rect)

    elif dashing: 
        if flipped: 
            screen.blit(flipped_dash_frames[dash_frame_index], char_rect)
        else: 
            screen.blit(dash_frames[dash_frame_index], char_rect)
        dash_frame_counter += 1
        if dash_frame_counter >= dash_frame_update_rate: 
            dash_frame_counter = 0
            dash_frame_index = (dash_frame_index + 1) % len(dash_frames)
        if flipped:
            char_rect.x = min(max_x, char_rect.x + dash_speed)
        else: 
            char_rect.x = max(min_x, char_rect.x - dash_speed)
        if char_rect.y < top_border: 
            char_rect.y = top_border
        elif char_rect.y > bottom_border:
            char_rect.y = bottom_border
        if dash_frame_index == len(dash_frames) - 1:
            dashing = False

    elif charging: 
        if flipped: 
            screen.blit(flipped_charge_frames[charge_frame_index], char_rect)
        else: 
            screen.blit(charge_frames[charge_frame_index], char_rect)
        charge_frame_counter += 1
        if charge_frame_counter >= charge_frame_update_rate: 
            charge_frame_counter = 0
            charge_frame_index += 1
        if charge_frame_index >= len(charge_frames):
            charging = False
            charge_frame_index = 0

    elif attacking:
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
        if char_rect.colliderect(boss_hitbox) and current_time - boss_hit_timer > boss_hit_delay:
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

    #Cooldown
    if dash_cooldown: 
        dash_elapsed_time = current_time - last_dash_time
        dash_cooldown_ratio = dash_elapsed_time / dash_cooldown_time
        cd_height_2 = int(Dash_cd_ui_rect.height* (1-dash_cooldown_ratio) )
        if cd_height_2 > 0: 
            Dash_cooldown_rect = pygame.Rect(Dash_cd_ui_rect.left, Dash_cd_ui_rect.top, Dash_cd_ui_rect.width, cd_height_2)
            cd_effect_partial2 = Dash_cd_ui.subsurface((0,0, Dash_cd_ui_rect.width, cd_height_2))
            screen.blit(cd_effect_partial2, Dash_cooldown_rect)
        if dash_elapsed_time > dash_cooldown_time: 
            dash_cooldown = False

    if charge_cooldown: 
        charge_elapsed_time = current_time - last_charge_time
        charge_cooldown_ratio = charge_elapsed_time / charge_cooldown_time
        cd_height_1 = int(Charge_cd_ui_rect.height* (1-charge_cooldown_ratio) )
        if cd_height_1 > 0: 
            Charge_cooldown_rect = pygame.Rect(Charge_cd_ui_rect.left, Charge_cd_ui_rect.top, Charge_cd_ui_rect.width, cd_height_1)
            cd_effect_partial1 = Charge_cd_ui.subsurface((0,0, Charge_cd_ui_rect.width, cd_height_1))
            screen.blit(cd_effect_partial1, Charge_cooldown_rect)
        if charge_elapsed_time > charge_cooldown_time: 
            charge_cooldown = False
            
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
            taking_damage = True
            getting_hit_sound.play()
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
            taking_damage = True
            getting_hit_sound.play()
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
            taking_damage = True
            getting_hit_sound.play()
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
            taking_damage = True
            getting_hit_sound.play()
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
            taking_damage = True
            getting_hit_sound.play()
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
            taking_damage = True
            getting_hit_sound.play()
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
            taking_damage = True
            getting_hit_sound.play()
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
            taking_damage = True
            getting_hit_sound.play()
            remaining_hp -= dmg 
            hp_ratio = remaining_hp / max_hp
        elif knife_rect.x < 0 or knife_rect.y < 0:
            knives_top_left.remove((top_left_knife, knife_rect))

    # Cập nhật và vẽ thanh máu
    health_width = int(Hp_2_rect.width * (1 - hp_ratio))
    health_width = max(0, min(Hp_2_rect.width, health_width))
    if health_width > 0:
        Hp_2_partial = Hp_2.subsurface((Hp_2_rect.width - health_width, 0, health_width, Hp_2_rect.height))
        screen.blit(Hp_2_partial, (Hp_bar_rect.right - health_width, Hp_bar_rect.top))

    boss_health_width = int(boss_hp_2_rect.width * (1 - boss_hp_ratio))
    boss_health_width = max(0, min(boss_hp_2_rect.width, boss_health_width))
    if boss_health_width > 0:
        boss_Hp_2_partial = boss_hp_2.subsurface((boss_hp_2_rect.width - boss_health_width, 0, boss_health_width, boss_hp_2_rect.height))
        screen.blit(boss_Hp_2_partial, (boss_hp_2_rect.right - boss_health_width, boss_hp_2_rect.top))

    # Font for displaying remaining HP
    font = pygame.font.Font(os.path.join(Font_folder, 'properhitboxglobal.ttf'), 18)
    hp_text_black = font.render(f"{remaining_hp}/{max_hp}", True, (0, 0, 0))  # Màu đen
    hp_text_rect = hp_text_black.get_rect(center=(240, 40))
    hp_text_white = font.render(f"{remaining_hp}/{max_hp}", True, (255, 255, 255))  # Màu trắng
    screen.blit(hp_text_black, hp_text_rect.move(2, 2))  
    screen.blit(hp_text_white, hp_text_rect)

    # Font for displaying remaining boss_HP
    font2 = pygame.font.Font(os.path.join(Font_folder, 'properhitboxglobal.ttf'), 18)
    boss_hp_text_black = font.render(f"{boss_remaining_hp}/{boss_max_hp}", True, (0, 0, 0))  # Màu đen
    boss_hp_text_rect = boss_hp_text_black.get_rect(center=(width//2, 73))
    boss_hp_text_white = font2.render(f"{boss_remaining_hp}/{boss_max_hp}", True, (255, 255, 255))  # Màu trắng
    screen.blit(boss_hp_text_black, boss_hp_text_rect.move(2, 2))  
    screen.blit(boss_hp_text_white, boss_hp_text_rect)

    if remaining_hp <= 0:
        game_over = True
        font_die = pygame.font.Font(os.path.join(Font_folder, 'Pixelmax-Regular.otf'), 100)
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

    if boss_remaining_hp <= 0:
        win = True
        font_win = pygame.font.Font(os.path.join(Font_folder, 'Pixelmax-Regular.otf'), 100)
        text_win_black = font_win.render(f"VICTORY!", True, (0, 0, 0))  # Màu đen
        text_win_rect = text_win_black.get_rect(center = (width//2, height//2 - 200))
        text_win_white = font_win.render(f"VICTORY!", True, (255, 255, 255))  # Màu trắng
        screen.blit(text_win_black, text_win_rect.move(10,10))
        screen.blit(text_win_white, text_win_rect)
        while win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Hiển thị thông báo win tại đây
            pygame.display.flip()

    pygame.display.flip()
    clock.tick(60)