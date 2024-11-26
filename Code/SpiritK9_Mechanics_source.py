# import pygame, sys
# from PIL import Image
# import time

# pygame.init()

# info = pygame.display.Info()

# # Thông số của cửa sổ pygame
# width = info.current_w
# height = info.current_h
# screen = pygame.display.set_mode((width, height-50))
# clock = pygame.time.Clock()

# #UI
# scale_factor = 0.5
# Hp_bar = pygame.image.load('D:\SpiritKnight-main\Sprites\HP.png').convert_alpha()
# Hp_bar = pygame.transform.scale(Hp_bar, (int(Hp_bar.get_width()*scale_factor), int(Hp_bar.get_height()*scale_factor)))
# Hp_bar_rect = Hp_bar.get_rect(topleft = (0,0))
# Inv = pygame.image.load('D:\SpiritKnight-main\Sprites\inv.png').convert_alpha()
# Inv = pygame.transform.scale(Inv, (int(Inv.get_width()*scale_factor), int(Inv.get_height()*scale_factor)))
# Inv_rect = Inv.get_rect(topleft = (0,0))
# frame_ui = pygame.image.load('D:\SpiritKnight-main\Sprites\Frame2.png').convert_alpha()
# frame_ui = pygame.transform.scale(frame_ui, (int(frame_ui.get_width()*scale_factor), int(frame_ui.get_height()*scale_factor)))
# frame_ui_rect = frame_ui.get_rect(center = (60,750))
# charge_ui = pygame.image.load('D:\SpiritKnight-main\Sprites\Skill icon.png').convert_alpha()
# charge_ui = pygame.transform.scale(charge_ui, (int(charge_ui.get_width()*scale_factor), int(charge_ui.get_height()*scale_factor)))
# charge_ui_rect = charge_ui.get_rect(center = (60,750))
# frame_ui2 = pygame.image.load('D:\SpiritKnight-main\Sprites\Frame1.png').convert_alpha()
# frame_ui2 = pygame.transform.scale(frame_ui2, (int(frame_ui2.get_width()*scale_factor), int(frame_ui2.get_height()*scale_factor)))
# frame_ui2_rect = frame_ui2.get_rect(center = (160, 750))
# dash_ui = pygame.image.load('D:\SpiritKnight-main\Sprites\Dash icon2.png').convert_alpha()
# dash_ui = pygame.transform.scale(dash_ui, (int(dash_ui.get_width()*scale_factor), int(dash_ui.get_height()*scale_factor)))
# dash_ui_rect = dash_ui.get_rect(center = (160,750))
# cooldown_effect = pygame.image.load('D:\SpiritKnight-main\Sprites\Skill cooldown.png')
# cooldown_effect = pygame.transform.scale(cooldown_effect, (int(cooldown_effect.get_width()*scale_factor), int(cooldown_effect.get_height()*scale_factor)))
# cooldown_effect_rect = cooldown_effect.get_rect(center = (60, 750))
# cooldown_effect_2 = pygame.image.load('D:\SpiritKnight-main\Sprites\Dash cooldown.png').convert_alpha()
# cooldown_effect_2 = pygame.transform.scale(cooldown_effect_2, (int(cooldown_effect_2.get_width()*scale_factor), int(cooldown_effect_2.get_height()*scale_factor)))
# cooldown_effect_2_rect = cooldown_effect_2.get_rect(center = (160,750))


# #Load animation stance của goblin 
# gif_path_gob = 'D:\SpiritKnight-main\Sprites\Goblin.gif'
# gif_gob = Image.open(gif_path_gob)
# frames_gob = []

# try: 
#     while True:
#         frame_gob = gif_gob.copy()
#         frame_gob = frame_gob.convert("RGBA")
#         frames_gob.append(pygame.image.fromstring(frame_gob.tobytes(), frame_gob.size, frame_gob.mode))
#         gif_gob.seek(len(frames_gob))
# except EOFError:
#     pass

# gob_rect = frames_gob[0].get_rect(center=((width//2) - 200, (height//2) ))
# frame_gob_index = 0 
# gob_frame_counter = 0

# # Load animation stance của nhân vật
# gif_path = 'D:\SpiritKnight-main\Sprites\lil dude bigger.gif'
# gif = Image.open(gif_path)
# frames = []

# try:
#     while True:
#         frame = gif.copy()
#         frame = frame.convert("RGBA")
#         frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
#         gif.seek(len(frames))  # Di chuyển đến frame tiếp theo
# except EOFError:
#     pass

# # Xoay frame stance nhân vật
# flipped_frames = [pygame.transform.flip(frame, True, False) for frame in frames]

# # Load sprite_sheet tấn công
# attack_sprite_sheet = pygame.image.load('D:\SpiritKnight-main\Sprites\lil dude big.png').convert_alpha()
# attack_frames = []
# sprite_width, sprite_height = attack_sprite_sheet.get_width() // 6, attack_sprite_sheet.get_height()

# # Assuming 6 frames in the sprite sheet
# for i in range(6):
#     frame = attack_sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
#     attack_frames.append(frame)

# # Xoay frame tấn công
# flipped_attack_frames = [pygame.transform.flip(frame, True, False) for frame in attack_frames]

# # Load sprite_sheet skill
# charge_attack_sprite_sheet = pygame.image.load('D:\SpiritKnight-main\Sprites\Battery.png').convert_alpha()
# charge_attack_frames = []
# charge_sprite_width, charge_sprite_height = charge_attack_sprite_sheet.get_width() // 9, charge_attack_sprite_sheet.get_height()

# # Assuming 9 frames in the sprite sheet
# for i in range(9):
#     charge_frame = charge_attack_sprite_sheet.subsurface((i * charge_sprite_width, 0, charge_sprite_width, charge_sprite_height))
#     charge_attack_frames.append(charge_frame)

# # Xoay frame skill
# flipped_charge_attack_frames = [pygame.transform.flip(charge_frame, True, False) for charge_frame in charge_attack_frames]

# # Load sprite_sheet chạy
# run_sprite_sheet = pygame.image.load('D:\SpiritKnight-main\Sprites\\running.png').convert_alpha()
# run_frames = []
# run_width, run_height = run_sprite_sheet.get_width() // 8, run_sprite_sheet.get_height()

# # Assuming 8 frames in the sprite sheet
# for i in range(8):
#     run_frame = run_sprite_sheet.subsurface((i * run_width, 0, run_width, run_height))
#     run_frames.append(run_frame)

# # Xoay frame chạy
# flipped_run_frames = [pygame.transform.flip(run_frame, True, False) for run_frame in run_frames]

# # Load sprite sheet lướt
# dash_sprite_sheet = pygame.image.load('D:\SpiritKnight-main\Sprites\Dash.png').convert_alpha()
# dash_frames = []
# dash_width, dash_height = dash_sprite_sheet.get_width() // 8, dash_sprite_sheet.get_height()

# # Assuming 6 frames in the sprite sheet
# for i in range(8):
#     dash_frame = dash_sprite_sheet.subsurface((i * dash_width, 0, dash_width, dash_height))
#     dash_frames.append(dash_frame)

# # Xoay frame lướt
# flipped_dash_frames = [pygame.transform.flip(dash_frame, True, False) for dash_frame in dash_frames]

# # Thông số nhân vật
# character_rect = frames[0].get_rect(center=(width // 2, height // 2))
# hitbox = character_rect.copy()
# hitbox.inflate_ip(-27,-27)
# frame_index = 0
# run_frame_index = 0
# attack_frame_index = 0
# charge_frame_index = 0
# dash_frame_index = 0
# flipped = False
# attacking = False
# charging = False
# running = False
# dashing = False
# charge_cooldown = False
# dash_cooldown = False

# charge_cooldown_time = 2  # Thời gian cooldown charge (giây)
# dash_cooldown_time = 1.5  # Thời gian cooldown lướt (giây)
# last_charge_time = 0
# last_dash_time = 0

# # Biến đếm frame
# frame_counter = 0
# run_frame_counter = 0
# attack_frame_counter = 0
# charge_frame_counter = 0
# dash_frame_counter = 0

# # Tốc độ frame cập nhật
# frame_update_rate = 5
# attack_frame_update_rate = 2
# charge_frame_update_rate = 4
# dash_frame_update_rate = 2
# dash_duration = len(dash_frames)
# dash_speed = 10

# goblin_hit_count = 0

# collision = False

# while True:
#     screen.fill((0, 0, 0))  # Fill màn hình màu đen

#     #Goblin
#     if goblin_hit_count < 3:
#         gob_frame_counter += 1
#         if gob_frame_counter >= frame_update_rate:
#             gob_frame_counter = 0
#             frame_gob_index = (frame_gob_index +1) % len(frames_gob)
#         screen.blit(frames_gob[frame_gob_index], gob_rect)
#         pygame.draw.rect(screen, (0, 255, 0), gob_rect, 2)  # Hitbox goblin (màu xanh lá)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == pygame.MOUSEBUTTONDOWN:  # Chuột nhấn
#             if event.button == 1:  # Chuột trái
#                 attacking = True
#                 attack_frame_index = 0
#                 attack_frame_counter = 0
#                 if hitbox.colliderect(gob_rect):
#                     goblin_hit_count += 1
#             elif event.button == 3 and not charge_cooldown:  # Chuột phải
#                 charging = True
#                 charge_frame_index = 0
#                 charge_frame_counter = 0
#                 charge_cooldown = True
#                 last_charge_time = time.time()

#     if goblin_hit_count >= 3:
#         gob_rect.topleft = (-1000,-1000)

#     keys = pygame.key.get_pressed()
#     running = False

#     # Xử lý phím di chuyển
#     if keys[pygame.K_a]:
#         character_rect.x -= 5
#         running = True
#         flipped = False
#     if keys[pygame.K_d]:
#         character_rect.x += 5
#         running = True
#         flipped = True
#     if keys[pygame.K_w]:
#         character_rect.y -= 5
#         running = True
#     if keys[pygame.K_s]:
#         character_rect.y += 5
#         running = True

#     # Cập nhật hitbox theo vị trí nhân vật
#     hitbox.center = character_rect.center

#     # Kiểm tra va chạm giữa hitbox của nhân vật và goblin
#     collision = hitbox.colliderect(gob_rect)

#     # Vẽ hitbox (chỉ để kiểm tra, có thể xóa khi phát hành)
#     pygame.draw.rect(screen, (255, 0, 0), hitbox, 2)  # Hitbox nhân vật (màu đỏ)

#     if collision: 
#          pygame.draw.rect(screen, (255, 255, 0), gob_rect, 2)  # Đổi màu hitbox của goblin để báo hiệu

#     # Kích hoạt lướt
#     if keys[pygame.K_LSHIFT] and not dashing and not dash_cooldown:
#         dashing = True
#         dash_frame_index = 0
#         dash_frame_counter = 0
#         last_dash_time = time.time()
#         dash_cooldown = True

#     # Logic animation
#     if dashing:
#         if flipped:
#             screen.blit(flipped_dash_frames[dash_frame_index], character_rect)
#         else:
#             screen.blit(dash_frames[dash_frame_index], character_rect)
#         dash_frame_counter += 1
#         if dash_frame_counter >= dash_frame_update_rate:
#             dash_frame_counter = 0
#             dash_frame_index = (dash_frame_index + 1) % len(dash_frames)

#         # Di chuyển nhanh khi lướt
#         if flipped:
#             character_rect.x += dash_speed
#         else:
#             character_rect.x -= dash_speed

#         # Kết thúc lướt
#         if dash_frame_index == len(dash_frames)-1:
#             dashing = False

#     elif charging:
#         if flipped:
#             screen.blit(flipped_charge_attack_frames[charge_frame_index], character_rect)
#         else:
#             screen.blit(charge_attack_frames[charge_frame_index], character_rect)
#         charge_frame_counter += 1
#         if charge_frame_counter >= charge_frame_update_rate:
#             charge_frame_counter = 0
#             charge_frame_index += 1
#         if charge_frame_index >= len(charge_attack_frames):
#             charging = False

#     elif attacking:
#         if flipped:
#             screen.blit(flipped_attack_frames[attack_frame_index], character_rect)
#         else:
#             screen.blit(attack_frames[attack_frame_index], character_rect)
#         attack_frame_counter += 1
#         if attack_frame_counter >= attack_frame_update_rate:
#             attack_frame_counter = 0
#             attack_frame_index += 1
#         if attack_frame_index >= len(attack_frames):
#             attacking = False

#     elif running:
#         if flipped:
#             screen.blit(flipped_run_frames[run_frame_index], character_rect)
#         else:
#             screen.blit(run_frames[run_frame_index], character_rect)
#         run_frame_counter += 1
#         if run_frame_counter >= frame_update_rate: 
#             run_frame_counter = 0
#             run_frame_index = (run_frame_index + 1) % len(run_frames)

#     else:
#         frame_counter += 1
#         if frame_counter >= frame_update_rate:
#             frame_counter = 0
#             frame_index = (frame_index + 1) % len(frames)
#         if flipped:
#             screen.blit(flipped_frames[frame_index], character_rect)
#         else:
#             screen.blit(frames[frame_index], character_rect)
    
#     screen.blit(charge_ui, charge_ui_rect)
#     screen.blit(dash_ui, dash_ui_rect)


#     # Xử lý cooldown
#     if charge_cooldown:
#         charge_elapsed_time = time.time() - last_charge_time
#         charge_cooldown_ratio = charge_elapsed_time / charge_cooldown_time

#         # Hiển thị thanh cooldown trên kỹ năng charge
#         cooldown_height = int(cooldown_effect_rect.height * (1 - charge_cooldown_ratio))
#         if cooldown_height > 0:
#             charge_cooldown_rect = pygame.Rect(cooldown_effect_rect.left, cooldown_effect_rect.top, cooldown_effect_rect.width, cooldown_height)
#             cooldown_effect_partial = cooldown_effect.subsurface((0, 0, cooldown_effect_rect.width, cooldown_height))
#             screen.blit(cooldown_effect_partial, charge_cooldown_rect)

#         if charge_elapsed_time >= charge_cooldown_time:
#             charge_cooldown = False

#     if dash_cooldown:
#         dash_elapsed_time = time.time() - last_dash_time
#         dash_cooldown_ratio = dash_elapsed_time / dash_cooldown_time

#         # Hiển thị thanh cooldown trên kỹ năng dash
#         cooldown_height_2 = int(cooldown_effect_2_rect.height * (1 - dash_cooldown_ratio))
#         if cooldown_height_2 > 0:
#             dash_cooldown_rect = pygame.Rect(frame_ui2_rect.left, frame_ui2_rect.top, cooldown_effect_2_rect.width, cooldown_height_2)
#             cooldown_effect_partial_2 = cooldown_effect_2.subsurface((0, 0, cooldown_effect_2_rect.width, cooldown_height_2))
#             screen.blit(cooldown_effect_partial_2, dash_cooldown_rect)

#         if dash_elapsed_time >= dash_cooldown_time:
#             dash_cooldown = False

#     screen.blit(Hp_bar, Hp_bar_rect.topleft)
#     screen.blit(Inv, Inv_rect.topleft)
#     screen.blit(frame_ui, frame_ui_rect)
#     screen.blit(frame_ui2, frame_ui2_rect)

#     pygame.display.update()
#     clock.tick(60)




import pygame
import sys
from PIL import Image
import time
import random
from pygame.math import Vector2
import math

# Function to load GIF frames
def gif_image(gif, frames):
    try:
        while True:
            frame = gif.copy()
            frame = frame.convert("RGBA")
            frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
            gif.seek(len(frames))  # Move to the next frame
    except EOFError:
        pass

# Function to load frames from a sprite sheet
def load_frames_from_sprite_sheet(sprite_sheet_path, frame_count):
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    frames = []
    sprite_width, sprite_height = sprite_sheet.get_width() // frame_count, sprite_sheet.get_height()

    for i in range(frame_count):
        frame = sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
        frames.append(frame)
    
    return frames

# Function to spawn enemies at a random position with a minimum distance from the character
def spawn_enemy(character_pos, width, height, min_distance):
    while True:
        enemy_x = random.randint(0, width)
        enemy_y = random.randint(0, height)
        enemy_pos = Vector2(enemy_x, enemy_y)
        if enemy_pos.distance_to(character_pos) >= min_distance:
            return enemy_pos

# Function to handle events
def handle_events(attacking, attack_frame_index, attack_frame_counter, charging, charge_frame_index, charge_frame_counter, charge_cooldown, last_charge_time, skill_active, cooldown_start_time):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                attacking = True
                attack_frame_index = 0
                attack_frame_counter = 0
            elif event.button == 3 and not charge_cooldown:  # Right click
                charging = True
                charge_frame_index = 0
                charge_frame_counter = 0
                charge_cooldown = True
                last_charge_time = time.time()
                skill_active = True
                cooldown_start_time = pygame.time.get_ticks()
    return attacking, attack_frame_index, attack_frame_counter, charging, charge_frame_index, charge_frame_counter, charge_cooldown, last_charge_time, skill_active, cooldown_start_time

# Function to handle key inputs and return the direction the player is facing
def handle_keys(character_rect, width, height, flipped):
    keys = pygame.key.get_pressed()
    running = False

    # Movement controls
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        character_rect.x -= 5
        if character_rect.x < 0:
            character_rect.x = 0
        running = True
        flipped = False  # Facing left
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        character_rect.x += 5
        if character_rect.right > width:
            character_rect.right = width
        running = True
        flipped = True  # Facing right
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        character_rect.y -= 5
        if character_rect.y < 0:
            character_rect.y = 0
        running = True
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        character_rect.y += 5
        if character_rect.bottom > height:
            character_rect.bottom = height
        running = True

    return running, flipped

class Character:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.load_assets()
        self.reset_states()

    def load_assets(self):
        self.load_gif()
        self.load_attack_frames()
        self.load_charge_attack_frames()
        self.load_run_frames()
        self.load_dash_frames()

    def load_gif(self):
        gif_path = 'D:\\SpiritKnight-main\\Sprites\\lil dude bigger.gif'
        gif = Image.open(gif_path)
        self.frames = []
        try:
            while True:
                frame = gif.copy()
                frame = frame.convert("RGBA")
                self.frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
                gif.seek(len(self.frames))  # Move to the next frame
        except EOFError:
            pass

        self.flipped_frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]

    def load_attack_frames(self):
        attack_sprite_sheet = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\lil dude big.png').convert_alpha()
        self.attack_frames = []
        sprite_width, sprite_height = attack_sprite_sheet.get_width() // 6, attack_sprite_sheet.get_height()

        for i in range(6):
            frame = attack_sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
            self.attack_frames.append(frame)

        self.flipped_attack_frames = [pygame.transform.flip(frame, True, False) for frame in self.attack_frames]

    def load_charge_attack_frames(self):
        charge_attack_sprite_sheet = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\Battery.png').convert_alpha()
        self.charge_attack_frames = []
        charge_sprite_width, charge_sprite_height = charge_attack_sprite_sheet.get_width() // 9, charge_attack_sprite_sheet.get_height()

        for i in range(9):
            charge_frame = charge_attack_sprite_sheet.subsurface((i * charge_sprite_width, 0, charge_sprite_width, charge_sprite_height))
            self.charge_attack_frames.append(charge_frame)

        self.flipped_charge_attack_frames = [pygame.transform.flip(charge_frame, True, False) for charge_frame in self.charge_attack_frames]

    def load_run_frames(self):
        run_sprite_sheet = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\running.png').convert_alpha()
        self.run_frames = []
        run_width, run_height = run_sprite_sheet.get_width() // 8, run_sprite_sheet.get_height()

        for i in range(8):
            run_frame = run_sprite_sheet.subsurface((i * run_width, 0, run_width, run_height))
            self.run_frames.append(run_frame)

        self.flipped_run_frames = [pygame.transform.flip(run_frame, True, False) for run_frame in self.run_frames]

    def load_dash_frames(self):
        dash_sprite_sheet = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\Dash.png').convert_alpha()
        self.dash_frames = []
        dash_width, dash_height = dash_sprite_sheet.get_width() // 8, dash_sprite_sheet.get_height()

        for i in range(8):
            dash_frame = dash_sprite_sheet.subsurface((i * dash_width, 0, dash_width, dash_height))
            self.dash_frames.append(dash_frame)

        self.flipped_dash_frames = [pygame.transform.flip(dash_frame, True, False) for dash_frame in self.dash_frames]

    def reset_states(self):
        self.character_rect = self.frames[0].get_rect(center=(self.width // 2, self.height // 2))
        self.hitbox = self.character_rect.copy()
        self.hitbox.inflate_ip(-27, -27)
        self.frame_index = 0
        self.run_frame_index = 0
        self.attack_frame_index = 0
        self.charge_frame_index = 0
        self.dash_frame_index = 0
        self.flipped = False
        self.attacking = False
        self.charging = False
        self.running = False
        self.dashing = False
        self.charge_cooldown = False
        self.dash_cooldown = False
        self.charge_cooldown_time = 2  # Charge cooldown time (seconds)
        self.dash_cooldown_time = 1.5  # Dash cooldown time (seconds)
        self.last_charge_time = 0
        self.last_dash_time = 0
        self.frame_counter = 0
        self.run_frame_counter = 0
        self.attack_frame_counter = 0
        self.charge_frame_counter = 0
        self.dash_frame_counter = 0
        self.frame_update_rate = 5
        self.attack_frame_update_rate = 2
        self.charge_frame_update_rate = 4
        self.dash_frame_update_rate = 2
        self.dash_duration = len(self.dash_frames)
        self.dash_speed = 10
        self.collision = False

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        self.running = False

        if keys[pygame.K_a]:
            self.character_rect.x -= 5
            self.running = True
            self.flipped = False
        if keys[pygame.K_d]:
            self.character_rect.x += 5
            self.running = True
            self.flipped = True
        if keys[pygame.K_w]:
            self.character_rect.y -= 5
            self.running = True
        if keys[pygame.K_s]:
            self.character_rect.y += 5
            self.running = True

        self.hitbox.center = self.character_rect.center

    def draw(self, screen):
        if self.dashing:
            if self.flipped:
                screen.blit(self.flipped_dash_frames[self.dash_frame_index], self.character_rect)
            else:
                screen.blit(self.dash_frames[self.dash_frame_index], self.character_rect)
            self.dash_frame_counter += 1
            if self.dash_frame_counter >= self.dash_frame_update_rate:
                self.dash_frame_counter = 0
                self.dash_frame_index = (self.dash_frame_index + 1) % len(self.dash_frames)
            if self.flipped:
                self.character_rect.x += self.dash_speed
            else:
                self.character_rect.x -= self.dash_speed
            if self.dash_frame_index == len(self.dash_frames) - 1:
                self.dashing = False

        elif self.charging:
            if self.flipped:
                screen.blit(self.flipped_charge_attack_frames[self.charge_frame_index], self.character_rect)
            else:
                screen.blit(self.charge_attack_frames[self.charge_frame_index], self.character_rect)
            self.charge_frame_counter += 1
            if self.charge_frame_counter >= self.charge_frame_update_rate:
                self.charge_frame_counter = 0
                self.charge_frame_index += 1
            if self.charge_frame_index >= len(self.charge_attack_frames):
                self.charging = False

        elif self.attacking:
            if self.flipped:
                screen.blit(self.flipped_attack_frames[self.attack_frame_index], self.character_rect)
            else:
                screen.blit(self.attack_frames[self.attack_frame_index], self.character_rect)
            self.attack_frame_counter += 1
            if self.attack_frame_counter >= self.attack_frame_update_rate:
                self.attack_frame_counter = 0
                self.attack_frame_index += 1
            if self.attack_frame_index >= len(self.attack_frames):
                self.attacking = False

        elif self.running:
            if self.flipped:
                screen.blit(self.flipped_run_frames[self.run_frame_index], self.character_rect)
            else:
                screen.blit(self.run_frames[self.run_frame_index], self.character_rect)
            self.run_frame_counter += 1
            if self.run_frame_counter >= self.frame_update_rate:
                self.run_frame_counter = 0
                self.run_frame_index = (self.run_frame_index + 1) % len(self.run_frames)

        else:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_update_rate:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
            if self.flipped:
                screen.blit(self.flipped_frames[self.frame_index], self.character_rect)
            else:
                screen.blit(self.frames[self.frame_index], self.character_rect)
        
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)  # Hitbox (red)

class Goblin:
    def __init__(self, frames_gob, width, height):
        self.frames_gob = frames_gob
        self.width = width
        self.height = height
        self.gob_rect = self.frames_gob[0].get_rect(center=((width // 2) - 200, (height // 2)))
        self.frame_gob_index = 0
        self.gob_frame_counter = 0
        self.goblin_hit_count = 0
        self.flipped_frames_goblin = [pygame.transform.flip(frame, True, False) for frame in self.frames_gob]
        self.hit_recently = False  # Flag to track if goblin was hit recently
        self.last_hit_time = 0  # Time when the last hit was registered
        self.hit_delay = 0.5  # Delay in seconds before registering the hit
        self.skill_hit_recently = False  # Flag to track if the goblin was hit by a skill
        self.last_skill_hit_time = 0  # Time when the last skill hit was registered
        self.skill_hit_delay = 10  # Delay in seconds for the skill hit

    def update(self, character_pos, attacking, charging):
        player_pos = Vector2(character_pos)
        enemy_pos = Vector2(self.gob_rect.center)
        distance_to_player = player_pos.distance_to(enemy_pos)
        direction = player_pos - enemy_pos

        current_time = time.time()

        if distance_to_player < 100:
            direction = direction.normalize() if direction.length() != 0 else Vector2(0, 0)

            if attacking and not self.hit_recently:
                if current_time - self.last_hit_time >= self.hit_delay:
                    self.goblin_hit_count += 1
                    print(self.goblin_hit_count)
                    self.hit_recently = True  # Set the flag to true when hit
                    self.last_hit_time = current_time  # Update the last hit time
            if charging and not self.skill_hit_recently:
                if current_time - self.last_skill_hit_time >= self.skill_hit_delay:
                    self.goblin_hit_count += 1
                    print(self.goblin_hit_count)
                    self.skill_hit_recently = True  # Set the flag to true when skill hit
                    self.last_skill_hit_time = current_time  # Update the last skill hit time
        else:
            self.hit_recently = False  # Reset the flag when not close to the player
            self.skill_hit_recently = False  # Reset the skill hit flag when not close to the player
            if direction.length() >= 50:
                direction = direction.normalize()
            enemy_pos += direction * 2
            self.gob_rect.center = enemy_pos

        if direction.x < 0:
            self.direction = "right"
        else:
            self.direction = "left"

        return self.direction

    def draw(self, screen):
        if self.goblin_hit_count < 3:
            self.gob_frame_counter += 1
            if self.gob_frame_counter >= 5:
                self.gob_frame_counter = 0
                self.frame_gob_index = (self.frame_gob_index + 1) % len(self.frames_gob)
            if self.direction == "right":
                screen.blit(self.frames_gob[self.frame_gob_index], self.gob_rect)
            else:
                screen.blit(self.flipped_frames_goblin[self.frame_gob_index], self.gob_rect)
            pygame.draw.rect(screen, (0, 255, 0), self.gob_rect, 2)  # Hitbox (green)

class Game:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height - 50))
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        self.character = Character(self.width, self.height)
        self.load_goblin_frames()
        self.goblin = Goblin(self.frames_gob, self.width, self.height)

        # UI elements
        self.charge_ui = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\Skill icon.png')
        self.charge_ui_rect = self.charge_ui.get_rect(topleft=(10, 10))
        self.dash_ui = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\Dash icon2.png')
        self.dash_ui_rect = self.dash_ui.get_rect(topleft=(10, 50))
        self.cooldown_effect = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\Skill cooldown.png')
        self.cooldown_effect_rect = self.cooldown_effect.get_rect()
        self.cooldown_effect_2 = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\Dash cooldown.png')
        self.cooldown_effect_2_rect = self.cooldown_effect_2.get_rect()
        self.Hp_bar = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\Hp.png')
        self.Hp_bar_rect = self.Hp_bar.get_rect(topleft=(10, 90))
        self.Inv = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\Inv.png')
        self.Inv_rect = self.Inv.get_rect(topleft=(10, 130))
        self.frame_ui = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\Frame2.png')
        self.frame_ui_rect = self.frame_ui.get_rect(topleft=(10, 170))
        self.frame_ui2 = pygame.image.load('D:\\SpiritKnight-main\\Sprites\\Frame1.png')
        self.frame_ui2_rect = self.frame_ui2.get_rect(topleft=(10, 210))

    def load_goblin_frames(self):
        gif_path = 'D:\\SpiritKnight-main\\Sprites\\Goblin.gif'
        gif = Image.open(gif_path)
        self.frames_gob = []
        try:
            while True:
                frame = gif.copy()
                frame = frame.convert("RGBA")
                self.frames_gob.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
                gif.seek(len(self.frames_gob))
        except EOFError:
            pass

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))  # Fill the screen with black

            direction = self.goblin.update(self.character.character_rect.center, self.character.attacking, self.character.charging)

            self.goblin.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.character.attacking = True
                        self.character.attack_frame_index = 0
                        self.character.attack_frame_counter = 0
                        if self.character.hitbox.colliderect(self.goblin.gob_rect):
                            self.goblin.hit_recently = False  # Allow goblin to be hit again
                    elif event.button == 3 and not self.character.charge_cooldown:  # Right click
                        self.character.charging = True
                        self.character.charge_frame_index = 0
                        self.character.charge_frame_counter = 0
                        self.character.charge_cooldown = True
                        self.character.last_charge_time = time.time()

            if self.goblin.goblin_hit_count >= 3:
                self.goblin.gob_rect.topleft = (-1000, -1000)

            self.character.handle_keys()

            # Check for collision between character hitbox and goblin
            self.character.collision = self.character.hitbox.colliderect(self.goblin.gob_rect)

            # Change color of goblin hitbox if collision occurs
            if self.character.collision:
                pygame.draw.rect(self.screen, (255, 255, 0), self.goblin.gob_rect, 2)  # Yellow hitbox

            # Handle dashing
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] and not self.character.dashing and not self.character.dash_cooldown:
                self.character.dashing = True
                self.character.dash_frame_index = 0
                self.character.dash_frame_counter = 0
                self.character.last_dash_time = time.time()
                self.character.dash_cooldown = True

            # Draw the character
            self.character.draw(self.screen)

            # Draw UI elements
            self.screen.blit(self.charge_ui, self.charge_ui_rect)
            self.screen.blit(self.dash_ui, self.dash_ui_rect)

            # Handle cooldowns
            if self.character.charge_cooldown:
                charge_elapsed_time = time.time() - self.character.last_charge_time
                charge_cooldown_ratio = charge_elapsed_time / self.character.charge_cooldown_time
                cooldown_height = int(self.cooldown_effect_rect.height * (1 - charge_cooldown_ratio))
                if cooldown_height > 0:
                    charge_cooldown_rect = pygame.Rect(self.cooldown_effect_rect.left, self.cooldown_effect_rect.top, self.cooldown_effect_rect.width, cooldown_height)
                    cooldown_effect_partial = self.cooldown_effect.subsurface((0, 0, self.cooldown_effect_rect.width, cooldown_height))
                    self.screen.blit(cooldown_effect_partial, charge_cooldown_rect)
                if charge_elapsed_time >= self.character.charge_cooldown_time:
                    self.character.charge_cooldown = False

            if self.character.dash_cooldown:
                dash_elapsed_time = time.time() - self.character.last_dash_time
                dash_cooldown_ratio = dash_elapsed_time / self.character.dash_cooldown_time
                cooldown_height_2 = int(self.cooldown_effect_2_rect.height * (1 - dash_cooldown_ratio))
                if cooldown_height_2 > 0:
                    dash_cooldown_rect = pygame.Rect(self.frame_ui2_rect.left, self.frame_ui2_rect.top, self.cooldown_effect_2_rect.width, cooldown_height_2)
                    cooldown_effect_partial_2 = self.cooldown_effect_2.subsurface((0, 0, self.cooldown_effect_2_rect.width, cooldown_height_2))
                    self.screen.blit(cooldown_effect_partial_2, dash_cooldown_rect)
                if dash_elapsed_time >= self.character.dash_cooldown_time:
                    self.character.dash_cooldown = False

            # Draw additional UI elements
            self.screen.blit(self.Hp_bar, self.Hp_bar_rect.topleft)
            self.screen.blit(self.Inv, self.Inv_rect.topleft)
            self.screen.blit(self.frame_ui, self.frame_ui_rect)
            self.screen.blit(self.frame_ui2, self.frame_ui2_rect)

            pygame.display.update()
            self.clock.tick(60)



if __name__ == "__main__":
    game = Game()
    game.run()


