import pygame, sys
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
        gif_path = 'D:/SpiritKnight/Sprites/lil dude bigger.gif'
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
        attack_sprite_sheet = pygame.image.load('D:/SpiritKnight/Sprites/lil dude big.png').convert_alpha()
        self.attack_frames = []
        sprite_width, sprite_height = attack_sprite_sheet.get_width() // 6, attack_sprite_sheet.get_height()

        for i in range(6):
            frame = attack_sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
            self.attack_frames.append(frame)

        self.flipped_attack_frames = [pygame.transform.flip(frame, True, False) for frame in self.attack_frames]

    def load_charge_attack_frames(self):
        charge_attack_sprite_sheet = pygame.image.load('D:/SpiritKnight/Sprites/Battery.png').convert_alpha()
        self.charge_attack_frames = []
        charge_sprite_width, charge_sprite_height = charge_attack_sprite_sheet.get_width() // 9, charge_attack_sprite_sheet.get_height()

        for i in range(9):
            charge_frame = charge_attack_sprite_sheet.subsurface((i * charge_sprite_width, 0, charge_sprite_width, charge_sprite_height))
            self.charge_attack_frames.append(charge_frame)

        self.flipped_charge_attack_frames = [pygame.transform.flip(charge_frame, True, False) for charge_frame in self.charge_attack_frames]

    def load_run_frames(self):
        run_sprite_sheet = pygame.image.load('D:/SpiritKnight/Sprites/running.png').convert_alpha()
        self.run_frames = []
        run_width, run_height = run_sprite_sheet.get_width() // 8, run_sprite_sheet.get_height()

        for i in range(8):
            run_frame = run_sprite_sheet.subsurface((i * run_width, 0, run_width, run_height))
            self.run_frames.append(run_frame)

        self.flipped_run_frames = [pygame.transform.flip(run_frame, True, False) for run_frame in self.run_frames]

    def load_dash_frames(self):
        dash_sprite_sheet = pygame.image.load('D:/SpiritKnight/Sprites/Dash.png').convert_alpha()
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

        # Define movement boundaries (e.g., within the screen dimensions)
        min_x, max_x = 0, self.width - self.character_rect.width
        min_y, max_y = 0, self.height - self.character_rect.height

        if keys[pygame.K_a]:
            self.character_rect.x = max(min_x, self.character_rect.x - 5)
            self.running = True
            self.flipped = False
        if keys[pygame.K_d]:
            self.character_rect.x = min(max_x, self.character_rect.x + 5)
            self.running = True
            self.flipped = True
        if keys[pygame.K_w]:
            self.character_rect.y = max(min_y, self.character_rect.y - 5)
            self.running = True
        if keys[pygame.K_s]:
            self.character_rect.y = min(max_y, self.character_rect.y + 5)
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
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        self.character = Character(self.width, self.height)
        self.load_goblin_frames()
        self.goblin = Goblin(self.frames_gob, self.width, self.height)

        # UI elements
        self.scale_factor = 0.5
        self.charge_ui = pygame.image.load('D:/SpiritKnight/Sprites/Skill icon.png')
        self.charge_ui = pygame.transform.scale(self.charge_ui, (int(self.charge_ui.get_width()*self.scale_factor), int(self.charge_ui.get_height()*self.scale_factor)))
        self.charge_ui_rect = self.charge_ui.get_rect(center=(60, 750))
        self.dash_ui = pygame.image.load('D:/SpiritKnight/Sprites/Dash icon2.png')
        self.dash_ui = pygame.transform.scale(self.dash_ui, (int(self.dash_ui.get_width()*self.scale_factor), int(self.dash_ui.get_height()*self.scale_factor)))
        self.dash_ui_rect = self.dash_ui.get_rect(center=(160, 750))
        self.cooldown_effect = pygame.image.load('D:/SpiritKnight/Sprites/Skill cooldown.png')
        self.cooldown_effect = pygame.transform.scale(self.cooldown_effect, (int(self.cooldown_effect.get_width()*self.scale_factor), int(self.cooldown_effect.get_height()*self.scale_factor)))
        self.cooldown_effect_rect = self.cooldown_effect.get_rect(center=(60,750))
        self.cooldown_effect_2 = pygame.image.load('D:/SpiritKnight/Sprites/Dash cooldown.png')
        self.cooldown_effect_2 = pygame.transform.scale(self.cooldown_effect_2, (int(self.cooldown_effect_2.get_width()*self.scale_factor), int(self.cooldown_effect_2.get_height()*self.scale_factor)))
        self.cooldown_effect_2_rect = self.cooldown_effect_2.get_rect(center=(160,750))
        self.Hp_bar = pygame.image.load('D:/SpiritKnight/Sprites/HP.png')
        self.Hp_bar = pygame.transform.scale(self.Hp_bar, (int(self.Hp_bar.get_width()*self.scale_factor), int(self.Hp_bar.get_height()*self.scale_factor)))
        self.Hp_bar_rect = self.Hp_bar.get_rect(topleft=(0, 0))
        self.Inv = pygame.image.load('D:/SpiritKnight/Sprites/inv.png')
        self.Inv = pygame.transform.scale(self.Inv, (int(self.Inv.get_width()*self.scale_factor), int(self.Inv.get_height()*self.scale_factor)))
        self.Inv_rect = self.Inv.get_rect(topleft=(0, 0))
        self.frame_ui = pygame.image.load('D:/SpiritKnight/Sprites/Frame2.png')
        self.frame_ui = pygame.transform.scale(self.frame_ui, (int(self.frame_ui.get_width()*self.scale_factor), int(self.frame_ui.get_height()*self.scale_factor)))
        self.frame_ui_rect = self.frame_ui.get_rect(center=(60, 750))
        self.frame_ui2 = pygame.image.load('D:/SpiritKnight/Sprites/Frame1.png')
        self.frame_ui2 = pygame.transform.scale(self.frame_ui2, (int(self.frame_ui2.get_width()*self.scale_factor), int(self.frame_ui2.get_height()*self.scale_factor)))
        self.frame_ui2_rect = self.frame_ui2.get_rect(center=(160, 750))
        self.bg = pygame.image.load('D:/SpiritKnight/Sprites/placeholder.jpg')
        self.bg = pygame.transform.scale(self.bg, (int(self.bg.get_width()*self.scale_factor), int(self.bg.get_height()*self.scale_factor)))

    def load_goblin_frames(self):
        gif_path = 'D:/SpiritKnight/Sprites/Goblin.gif'
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
            self.screen.blit(self.bg, (0,0))

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