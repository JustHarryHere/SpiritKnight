import pygame, sys
from PIL import Image
import time
import random
from pygame.math import Vector2
import math
import os
from spawner import Spawner
from bosss import spawn_boss
from healthbar import HealthBar

#Hehehehe
pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

max_hp = 100
remaining_hp = 100
health_bar = HealthBar(max_hp, remaining_hp, position=(0, 0))

pygame.mixer.init()

script_dir = os.path.dirname(os.path.abspath(__file__))
Sprites_folder = os.path.join(script_dir, '..', 'Sprites')
Music_folder = os.path.join(script_dir, '..', 'Music')

run_sound = pygame.mixer.Sound(os.path.join(Music_folder, 'running-6358.wav'))
pygame.mixer.music.load(os.path.join(Music_folder, 'Kevin MacLeod - 8bit Dungeon Boss  NO COPYRIGHT 8-bit Music.mp3'))
#pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

class Enemy:
    def __init__(self, frames, initial_pos, width, height, character, game):
        self.frames = frames
        self.width = width
        self.height = height
        self.rect = self.frames[0].get_rect(center=initial_pos)
        self.frame_index = 0
        self.frame_counter = 0
        self.hit_count = 0
        self.flipped_frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.hit_recently = False
        self.last_hit_time = 0
        self.hit_delay = 0.5
        self.skill_hit_recently = False
        self.last_skill_hit_time = 0
        self.skill_hit_delay = 10
        self.eliminated = False
        self.direction = "left"
        self.character = character
        self.dropped_item = None

    def update_hit_count(self, current_time):
        if current_time - self.last_hit_time > self.skill_hit_delay:
            self.hit_count += 1
            self.last_hit_time = current_time
            print(f"Hit count updated at {current_time}. Total hits: {self.hit_count}")

    def drop_item(self):
        items = [
            ('speed.gif', 0.3),
            ('health.gif', 0.3),
            ('damage.gif', 0.2),
            ('shield.gif', 0.1),
            ('cross.gif', 0.1),
            (None, 0.1)
        ]
        item = random.choices([i[0] for i in items], weights=[i[1] for i in items], k=1)[0]
        if item is not None:
            self.dropped_item = LoadItem(item, self.rect, self.character)

    def update(self, character_pos, attacking, charging, character):
        current_time = time.time()

        if self.hit_count >= 3 and not self.eliminated:
            self.eliminated = True
            self.drop_item()
            print(f"Enemy eliminated. Dropping item: {self.dropped_item}")  # Debug statement

        if not self.eliminated:
            player_pos = Vector2(character_pos)
            self.enemy_pos = Vector2(self.rect.center)
            distance_to_player = player_pos.distance_to(self.enemy_pos)
            direction = player_pos - self.enemy_pos

            if distance_to_player < 50:
                direction = direction.normalize() if direction.length() != 0 else Vector2(0, 0)

                if attacking and not self.hit_recently:
                    if current_time - self.last_hit_time >= self.hit_delay:
                        self.hit_count += 1
                        print(f"Hit count increased: {self.hit_count}")  # Debug statement
                        self.hit_recently = True
                        self.last_hit_time = current_time

                if (charging or character.slash_hitted) and not self.skill_hit_recently:
                    if current_time - self.last_skill_hit_time >= self.skill_hit_delay:
                        self.hit_count += 1
                        print(f"Skill hit count increased: {self.hit_count}")  # Debug statement
                        self.skill_hit_recently = True
                        self.last_skill_hit_time = current_time
            else:
                self.hit_recently = False
                self.skill_hit_recently = False
                if direction.length() >= 50:
                    direction = direction.normalize()
                self.enemy_pos += direction * 2
                self.rect.center = self.enemy_pos

            if direction.x < 0:
                self.direction = "right"
            else:
                self.direction = "left"

        return self.direction

    def draw(self, screen):
        if not self.eliminated:
            self.frame_counter += 1
            if self.frame_counter >= 5:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
            if self.direction == "right":
                screen.blit(self.frames[self.frame_index], self.rect)
            else:
                screen.blit(self.flipped_frames[self.frame_index], self.rect)

            pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)

        if self.eliminated and self.dropped_item:
            self.dropped_item.draw(screen, self.character.character_rect)

class LoadItem:
    def __init__(self, gif_name, enemy_rect, character):
        self.item_gif_rect = enemy_rect
        self.pick_up_sound = pygame.mixer.Sound(os.path.join(Music_folder, 'Pop-_Minecraft-Sound_-Sound-Effect-for-editing.wav'))
        self.picked_up = False
        self.frame_index = 0
        self.frame_counter = 0
        self.frame_update_rate = 5
        self.game = None  # This will be set when the item is added to the game
        self.character = character

        gif_paths = {
            'speed.gif': os.path.join(Sprites_folder, 'wingedboot.gif'),
            'health.gif': os.path.join(Sprites_folder, 'Trans.gif'),
            'damage.gif': os.path.join(Sprites_folder, 'Heroine.gif'),
            'shield.gif': os.path.join(Sprites_folder, 'shield.gif'),
            'cross.gif': os.path.join(Sprites_folder, 'Mary on a.gif')
        }
        gif_path = gif_paths.get(gif_name)
        if gif_path is None:
            raise ValueError(f"Unknown gif name: {gif_name}")

        self.frames = self.load_gif(gif_path)

    def load_gif(self, gif_path):
        frames = []
        gif = Image.open(gif_path)
        try:
            while True:
                frame = gif.copy().convert("RGBA")
                frame = frame.resize((60, 60), Image.LANCZOS)
                pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                frames.append(pygame_frame)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        return frames

    def check_pick_up(self, char_rect):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and not self.picked_up:
            current_time = pygame.time.get_ticks()
            if char_rect.colliderect(self.item_gif_rect):
                self.picked_up = True
                self.play()
                if self.game:
                    self.game.remove_dropped_item(self)
                self.character.activate_speed_boost(current_time)

                # Hồi máu tùy vào loại vật phẩm
                if self.frames == self.load_gif(os.path.join(Sprites_folder, 'Trans.gif')):  # health.gif
                    self.character.hp = min(self.character.hp + 20, self.character.max_hp)
                    print("Nhặt health.gif: Hồi 20 máu")
                elif self.frames == self.load_gif(os.path.join(Sprites_folder, 'Mary on a.gif')):  # cross.gif
                    self.character.hp = self.character.max_hp
                    print("Nhặt cross.gif: Hồi đầy máu")

    def draw(self, screen, char_rect):
        self.check_pick_up(char_rect)
        if not self.picked_up:
            screen.blit(self.frames[self.frame_index], self.item_gif_rect)
            self.frame_counter += 1
            if self.frame_counter >= self.frame_update_rate:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)

    def play(self):
        self.pick_up_sound.play()

class Goblin(Enemy):
    def __init__(self, frames, attack_frames, initial_pos, width, height, character, game):
        super().__init__(frames, initial_pos, width, height, character, game)
        self.attack_frames = attack_frames  # Add attack frames
        self.flipped_attack_frames = [pygame.transform.flip(frame, True, False) for frame in self.attack_frames]
        self.is_attacking = False
        self.attack_frame_index = 0
        self.attack_frame_counter = 0
        self.attack_range = 50  # Define the attack range
        self.attack_damage = 1  # Damage dealt by the goblin
        self.attack_delay = 1  # Delay between attacks in seconds
        self.last_attack_time = time.time()

    def goblin_special_attack(self, character, current_time):
        if current_time - self.last_attack_time >= self.attack_delay:
            self.last_attack_time = current_time
            self.is_attacking = True  # Set attacking state
            self.attack_frame_index = 0  # Reset attack frame index for animation
            character.take_damage(self.attack_damage)

    def update(self, character_pos, attacking, charging, character):
        current_time = time.time()

        # Call the parent class update method
        super().update(character_pos, attacking, charging, character)

        # Check if the goblin should attack
        if self.rect.colliderect(character.hitbox) and not self.eliminated:
            self.goblin_special_attack(character, current_time)
        else:
            self.is_attacking = False

    # def goblin_special_attack(self, character, current_time): 
    #     if current_time - self.last_attack_time >= self.attack_delay: 
    #         self.last_attack_time = current_time 
    #         self.is_attacking = True 
    #         self.attack_frame_index = 0 # Reset attack frame index for animation 
    #         character.take_damage(20)
    #         # print(f"Goblin attacked! Player HP: {character.hp}")

    def draw(self, screen):
        if not self.eliminated:
            if self.is_attacking:
                self.attack_frame_counter += 1
                if self.attack_frame_counter >= 5:  # Adjust the frame rate as needed
                    self.attack_frame_counter = 0
                    self.attack_frame_index = (self.attack_frame_index + 1) % len(self.attack_frames)
                
                if self.direction == "right":
                    screen.blit(self.attack_frames[self.attack_frame_index], self.rect)  # Draw the attack frames
                else:
                    screen.blit(self.flipped_attack_frames[self.attack_frame_index], self.rect)  # Draw the flipped attack frames

                # Reset attacking state if the attack animation completes
                if self.attack_frame_index == len(self.attack_frames) - 1:
                    self.is_attacking = False
            else:
                self.frame_counter += 1
                if self.frame_counter >= 5:
                    self.frame_counter = 0
                    self.frame_index = (self.frame_index + 1) % len(self.frames)
                if self.direction == "right":
                    screen.blit(self.frames[self.frame_index], self.rect)
                else:
                    screen.blit(self.flipped_frames[self.frame_index], self.rect)

            pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)

        if self.eliminated and self.dropped_item:
            self.dropped_item.draw(screen, self.character.character_rect)

class Skeleton(Enemy):
    def __init__(self, frames, attack_frames, initial_pos, width, height, character, game):
        super().__init__(frames, initial_pos, width, height, character, game)
        self.attack_frames = attack_frames
        self.arrow_image = pygame.image.load(os.path.join(Sprites_folder, 'arrow.png'))
        self.arrow_rect = self.arrow_image.get_rect()
        self.arrow_hitbox = self.arrow_rect.inflate(-self.arrow_rect.width * 0.5, -self.arrow_rect.height * 0.5)
        self.ideal_distance = 500
        self.enemy_speed = 3
        self.arrow_speed = 15
        self.arrow_active = False
        self.last_arrow_time = 0
        self.arrow_cooldown = 2  # Adjusted cooldown duration
        self.arrow_dx, self.arrow_dy = 0, 0
        self.is_attacking = False
        self.attack_frame_index = 0
        self.attack_timer = 0
        self.attack_duration = 1.0
        self.attack_frame_rate = 0.2
        self.attack_damage = 0.000001

    def skeleton_special_attack(self, character, current_time):
        self.last_attack_time = current_time
        self.is_attacking = True  # Set attacking state
        self.attack_frame_index = 0  # Reset attack frame index for animation
        character.take_damage(self.attack_damage)

    def update(self, character_pos, attacking, charging, character):
        self.current_time = time.time()
        if self.hit_count >= 3 and not self.eliminated:
            self.eliminated = True
            self.drop_item()
            print(f"Skeleton eliminated. Dropping item: {self.dropped_item}")  # Debug statement

        if not self.eliminated:
            player_pos = Vector2(character_pos)
            self.enemy_pos = Vector2(self.rect.center)
            distance_to_player = player_pos.distance_to(self.enemy_pos)
            direction = player_pos - self.enemy_pos

            if not self.is_attacking:
                if distance_to_player < self.ideal_distance:
                    direction = direction.normalize() if direction.length() != 0 else Vector2(0, 0)
                    self.enemy_pos -= direction * (self.enemy_speed / 2)  # Move away slowly
                elif distance_to_player > self.ideal_distance:
                    direction = direction.normalize() if direction.length() != 0 else Vector2(0, 0)
                    self.enemy_pos += direction * self.enemy_speed
                self.rect.center = self.enemy_pos

            # Ensure the skeleton stays within screen bounds
            min_x, max_x = 200, self.width - 100  
            min_y, max_y = 100, self.height - 100  
            self.rect.left = max(min_x, self.rect.left)
            self.rect.right = min(max_x, self.rect.right)
            self.rect.top = max(min_y, self.rect.top)
            self.rect.bottom = min(max_y, self.rect.bottom)
            self.enemy_pos = Vector2(self.rect.center)

            if not self.arrow_active and not self.is_attacking and self.current_time - self.attack_timer > self.arrow_cooldown:
                self.is_attacking = True
                self.attack_timer = self.current_time

            if self.is_attacking:
                self.attack_frame_index = int((self.current_time - self.attack_timer) / self.attack_frame_rate) % len(self.attack_frames)
                if self.current_time - self.last_arrow_time >= self.attack_duration:
                    self.is_attacking = False
                    self.arrow_active = True
                    self.last_arrow_time = self.current_time
                    print(f"Last arrow time: {self.last_arrow_time}")
                    self.arrow_rect.center = self.rect.center
                    self.arrow_dx = character_pos[0] - self.rect.centerx
                    self.arrow_dy = character_pos[1] - self.rect.centery
                    distance = math.hypot(self.arrow_dx, self.arrow_dy)
                    if distance != 0:
                        self.arrow_dx /= distance
                        self.arrow_dy /= distance

            if self.arrow_active:
                self.arrow_rect.x += self.arrow_dx * self.arrow_speed
                self.arrow_rect.y += self.arrow_dy * self.arrow_speed
                self.arrow_hitbox.center = self.arrow_rect.center

                if character.character_rect.colliderect(self.arrow_hitbox):                  
                    self.skeleton_special_attack(character, self.current_time)
                    self.arrow_active = False

                if (self.arrow_rect.right < 0 or self.arrow_rect.left > self.width or
                    self.arrow_rect.bottom < 0 or self.arrow_rect.top > self.height):
                    self.arrow_active = False

            # super().update(character_pos, attacking, charging, character)

            if direction.x < 0:
                self.direction = "right"
            else:
                self.direction = "left"

        return self.direction

    def draw(self, screen):
        current_time = time.time()
        if not self.eliminated:
            self.frame_counter += 1
            if self.frame_counter >= 5:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
            if self.direction == "right":
                if self.is_attacking:
                    screen.blit(self.attack_frames[self.attack_frame_index], self.rect)
                else:
                    screen.blit(self.frames[self.frame_index], self.rect)
            else:
                flipped_frame = pygame.transform.flip(self.frames[self.frame_index], True, False)
                flipped_attack_frame = pygame.transform.flip(self.attack_frames[self.attack_frame_index], True, False)
                if self.is_attacking:
                    screen.blit(flipped_attack_frame, self.rect)
                else:
                    screen.blit(flipped_frame, self.rect)

            pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)

            if self.arrow_active:
                arrow_angle = math.degrees(math.atan2(self.arrow_dy, self.arrow_dx))
                rotated_arrow_image = pygame.transform.rotate(self.arrow_image, -arrow_angle)
                rotated_arrow_rect = rotated_arrow_image.get_rect(center=self.arrow_rect.center)
                screen.blit(rotated_arrow_image, rotated_arrow_rect)
        else:
            if self.dropped_item:
                self.dropped_item.draw(screen, self.character.character_rect)

class Witch(Enemy):
    def __init__(self, frames, teleport_frames, poison_bottle_image, poison_frames, initial_pos, width, height, character, clock, game):
        super().__init__(frames, initial_pos, width, height, character, game)
        self.clock = clock
        self.teleport_frames = teleport_frames
        self.teleport_circle_image = pygame.image.load(os.path.join(Sprites_folder, 'defalt circle.png')).convert_alpha()
        self.teleport_circle_rect = self.teleport_circle_image.get_rect()
        self.teleport_circle_angle = 0
        self.rotation_speed = 1
        self.teleporting = False
        self.teleport_start_time = 0
        self.teleport_duration = 700
        self.teleport_cooldown = 4000
        self.last_teleport_time = 0
        self.first_teleport = True
        self.warning_circle_timer = 0
        self.warning_circle_interval = 4000
        self.warning_circle_duration = 3000
        self.warning_circle_visible_timer = 0
        self.show_warning_circle = False
        self.warning_circle_position = None
        self.poison_bottle_image = poison_bottle_image
        self.poison_bottle_rect = self.poison_bottle_image.get_rect()
        self.poison_bottle_speed = 10
        self.throw_poison_bottle = False
        self.poison_bottle_start_time = 0
        self.poison_bottle_target = None
        self.poison_frames = poison_frames
        self.poison_frame_index = 0
        self.poison_frame_timer = 0
        self.poison_frame_duration = 200
        self.show_poison_gif = False
        self.poison_gif_display_timer = 0
        self.poison_gif_delay = 2000
        self.poison_aoe_image = pygame.image.load(os.path.join(Sprites_folder, 'PoisonAoe.png')).convert_alpha()
        self.poison_aoe_rect = self.poison_aoe_image.get_rect()
        self.warning_circle_radius = self.poison_aoe_rect.width // 2
        self.show_poison_aoe = False
        self.poison_aoe_timer = 0
        self.poison_aoe_duration = 8000

    def update(self, character_pos, attacking, charging, character):
        current_time = pygame.time.get_ticks()
        super().update(character_pos, attacking, charging, character)

        # Apply poison damage 
        if self.poison_active and self.rect.colliderect(character.character_rect): 
            character.hp -= 2 # Reduce player's HP by 2 per second 
            print(f"Player poisoned! Player HP: {character.hp}") # Check if poison duration is over 

        if current_time - self.poison_start_time >= 1: 
            self.poison_active = False

        if self.hit_count >= 3 and not self.eliminated:
            self.eliminated = True
            self.drop_item()

        if not self.eliminated:
            player_pos = Vector2(character_pos)
            self.enemy_pos = Vector2(self.rect.center)
            distance_to_player = player_pos.distance_to(self.enemy_pos)
            direction = player_pos - self.enemy_pos

            if self.teleporting:
                if current_time - self.teleport_start_time >= self.teleport_duration:
                    while True:
                        # Định nghĩa giới hạn vùng dịch chuyển
                        min_x, max_x = 100, self.width - 100
                        min_y, max_y = 100, self.height - 100

                        # Chọn vị trí ngẫu nhiên trong vùng giới hạn
                        new_x = random.randint(min_x, max_x - self.rect.width)
                        new_y = random.randint(min_y, max_y - self.rect.height)

                        # Kiểm tra khoảng cách đủ xa với người chơi
                        if Vector2(new_x, new_y).distance_to(player_pos) > 650:
                            self.rect.x = new_x
                            self.rect.y = new_y
                            break
                    self.teleporting = False
                    self.last_teleport_time = current_time
                    self.first_teleport = False
                else:
                    self.teleport_circle_angle = (self.teleport_circle_angle + self.rotation_speed) % 360

            else:
                if (self.first_teleport or current_time - self.last_teleport_time >= self.teleport_cooldown) and distance_to_player < 200:
                    self.teleporting = True
                    self.teleport_start_time = current_time

            self.warning_circle_timer += self.clock.get_time()
            if self.warning_circle_timer >= self.warning_circle_interval:
                self.warning_circle_timer = 0
                self.show_warning_circle = True
                self.warning_circle_visible_timer = 0
                self.warning_circle_position = character_pos
                self.poison_gif_display_timer = 0
                self.throw_poison_bottle = True
                self.poison_bottle_start_time = pygame.time.get_ticks()
                self.poison_bottle_target = self.warning_circle_position
                self.poison_bottle_rect.center = self.rect.center

            if self.show_warning_circle:
                self.warning_circle_visible_timer += self.clock.get_time()
                self.poison_gif_display_timer += self.clock.get_time()
                if self.poison_gif_display_timer >= self.poison_gif_delay:
                    self.show_poison_gif = True
                if self.warning_circle_visible_timer >= self.warning_circle_duration:
                    self.show_warning_circle = False
                    self.show_poison_aoe = True
                    self.poison_aoe_timer = 0
                    self.poison_aoe_rect.center = self.warning_circle_position

            if self.throw_poison_bottle:
                elapsed_time = current_time - self.poison_bottle_start_time
                if elapsed_time <= 1500:
                    progress = elapsed_time / 1500
                    new_x = self.rect.x + (self.poison_bottle_target[0] - self.rect.x) * progress
                    new_y = self.rect.y + (self.poison_bottle_target[1] - self.rect.y) * progress
                    self.poison_bottle_rect.center = (new_x, new_y)
                else:
                    self.throw_poison_bottle = False

            if self.show_poison_gif:
                self.poison_frame_timer += self.clock.get_time()
                if self.poison_frame_timer >= self.poison_frame_duration:
                    self.poison_frame_timer = 0
                    self.poison_frame_index = (self.poison_frame_index + 1) % len(self.poison_frames)
                if self.poison_frame_index == len(self.poison_frames) - 1:
                    self.show_poison_gif = False
                    self.poison_frame_index = 0

            if self.show_poison_aoe:
                self.poison_aoe_timer += self.clock.get_time()
                if self.poison_aoe_timer >= self.poison_aoe_duration:
                    self.show_poison_aoe = False

            if distance_to_player < 100:
                if attacking and not self.hit_recently:
                    if current_time - self.last_hit_time >= self.hit_delay:
                        self.hit_count += 1
                        self.hit_recently = True
                        self.last_hit_time = current_time

                if charging and not self.skill_hit_recently:
                    if current_time - self.last_skill_hit_time >= self.skill_hit_delay:
                        self.hit_count += 1
                        self.skill_hit_recently = True
                        self.last_skill_hit_time = current_time
                        
                if character.slash_hitted and not self.skill_hit_recently:  # Add slash hit detection
                    if current_time - self.last_skill_hit_time >= self.skill_hit_delay:
                        self.hit_count += 1
                        self.skill_hit_recently = True
                        self.last_skill_hit_time = current_time
            else:
                self.hit_recently = False
                self.skill_hit_recently = False

            if direction.x < 0:
                self.direction = "right"
            else:
                self.direction = "left"

        return self.direction

    def draw(self, screen):
        if not self.eliminated:
            self.frame_counter += 1
            if self.frame_counter >= 5:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
            if self.direction == "right":
                screen.blit(self.frames[self.frame_index], self.rect)
            else:
                screen.blit(self.flipped_frames[self.frame_index], self.rect)

            if self.teleporting:
                rotated_teleport_circle = pygame.transform.rotate(self.teleport_circle_image, self.teleport_circle_angle)
                rotated_rect = rotated_teleport_circle.get_rect(center=self.rect.center)
                screen.blit(rotated_teleport_circle, rotated_rect)

            if self.show_warning_circle:
                pygame.draw.circle(screen, (255, 0, 0), self.warning_circle_position, self.warning_circle_radius, 3)

            if self.throw_poison_bottle:
                screen.blit(self.poison_bottle_image, self.poison_bottle_rect)

            if self.show_poison_gif:
                poison_rect = self.poison_frames[self.poison_frame_index].get_rect(center=self.warning_circle_position)
                screen.blit(self.poison_frames[self.poison_frame_index], poison_rect)

            if self.show_poison_aoe:
                screen.blit(self.poison_aoe_image, self.poison_aoe_rect)
        else:
            if self.dropped_item:
                self.dropped_item.draw(screen, self.character.character_rect)

class EnemyManager:
    def __init__(self, enemy_frames, width, height, min_distance, num_enemies, enemy_list, clock):
        self.enemy_frames = enemy_frames
        self.width = width
        self.height = height
        self.min_distance = min_distance
        self.num_enemies = num_enemies
        self.enemy_list = enemy_list
        self.enemies = []
        self.active_enemies = []
        self.spawner = Spawner(width, height, min_distance)
        self.clock = clock
        self.dropped_items = []

    def spawn_multiple_enemies(self, character_pos, character, game):
        sample_size = min(self.num_enemies, len(self.enemy_list))
        sample_enemies = random.sample(self.enemy_list, sample_size)
        for enemy_name in sample_enemies:
            self.enemy_pos = self.spawner.spawn_enemy(character_pos)
            enemy = None
            if enemy_name == "Goblin":
                goblin_frames = self.enemy_frames["goblin"]
                goblin_attack_frames = self.enemy_frames["goblin_attack"]
                enemy = Goblin(goblin_frames, goblin_attack_frames, self.enemy_pos, self.width, self.height, character, game)
            elif enemy_name == "Witch":
                enemy = Witch(
                    self.enemy_frames["witch"],
                    self.enemy_frames["witch_teleport"],
                    pygame.image.load(os.path.join(Sprites_folder, 'poison bottle.png')).convert_alpha(),
                    self.enemy_frames["poison"],
                    self.enemy_pos, self.width, self.height, character, self.clock, game)
            elif enemy_name == "Skeleton":
                enemy = Skeleton(self.enemy_frames["skeleton"], self.enemy_frames["skeleton_attack"], self.enemy_pos, self.width, self.height, character, game)
            if enemy is not None:
                self.enemies.append(enemy)
                print(f"Spawned {enemy_name} at {self.enemy_pos}")
        self.active_enemies = self.enemies

    def update(self, character_pos, attacking, charging, character):
        for enemy in self.active_enemies:
            direction = enemy.update(character_pos, attacking, charging, character)
            if enemy.eliminated and enemy.dropped_item:
                self.dropped_items.append(enemy.dropped_item)
                enemy.dropped_item = None

        self.active_enemies = [enemy for enemy in self.enemies if not enemy.eliminated]
        if not self.active_enemies:
            self.enemies = []  # Clear the enemies list but keep dropped items

    def draw(self, screen, character_rect):
        for enemy in self.enemies:
            enemy.draw(screen)
        for item in self.dropped_items:
            item.draw(screen, character_rect)

    def next_level(self):
        self.enemies = []
        self.dropped_items = []

class Cross:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.load_assets()
        self.frame_index = 0
        self.frame_counter = 0
        self.frame_update_rate = 5
        self.pick_up_sound = pygame.mixer.Sound(os.path.join(Music_folder, 'Pop-_Minecraft-Sound_-Sound-Effect-for-editing.wav'))
        self.picked_up = False
        self.item_1 = pygame.image.load(os.path.join(Sprites_folder, 'mary1.png')).convert_alpha()
        self.item_1_rect = self.item_1.get_rect(center=(75, 78))
        self.cross_frame_index = 0

    def load_assets(self):
        self.load_gif()

    def load_gif(self):
        gif_path = os.path.join(Sprites_folder, 'Mary on a.gif')
        gif = Image.open(gif_path)
        character_gif_path = os.path.join(Sprites_folder, 'lil dude bigger.gif')
        character_gif = Image.open(character_gif_path)
        
        self.char_frames = []
        try:
            while True:
                char_frame = character_gif.copy()
                char_frame = char_frame.convert("RGBA")
                self.char_frames.append(pygame.image.fromstring(char_frame.tobytes(), char_frame.size, char_frame.mode))
                character_gif.seek(len(self.char_frames))  # Move to the next frame
        except EOFError:
            pass

        self.flipped_char_frames = [pygame.transform.flip(char_frame, True, False) for char_frame in self.char_frames]

        self.frames = []
        try:
            while True:
                frame = gif.copy()
                frame = frame.convert("RGBA")
                frame = frame.resize((60, 60), Image.Resampling.LANCZOS)
                self.frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
                gif.seek(len(self.frames))  # Move to the next frame
        except EOFError:
            pass

        self.flipped_frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.cross_rect = self.frames[0].get_rect(center=(self.width//2 + 100, self.height//2))

    def check_pick_up(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and not self.picked_up:
            if self.char_rect.colliderect(self.cross_rect):
                print(self.char_rect)
                self.picked_up = True
                self.pick_up_sound.play()

    def draw(self, screen, slot_inventory):
        self.check_pick_up()
        if self.picked_up and not slot_inventory["slot1"]["status"]:
            slot_inventory["slot1"]["status"] = True
        elif self.picked_up and slot_inventory["slot2"]["status"]:
            slot_inventory["slot2"]["status"] = True

        if not self.picked_up:
            screen.blit(self.frames[self.cross_frame_index], self.cross_rect)
        
        if slot_inventory["slot1"]["status"]:
            screen.blit(self.item_1, slot_inventory["slot1"]["slot_1_pos"])
        elif slot_inventory["slot2"]["status"]:
            screen.blit(self.item_1, slot_inventory["slot2"]["slot_2_pos"])

        self.frame_counter += 1
        if self.frame_counter >= self.frame_update_rate:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.char_frames)
            self.cross_frame_index = (self.cross_frame_index + 1) % len(self.frames)

class Character:
    def __init__(self, width, height, enemy_manager):
        self.width = width
        self.height = height
        self.enemy_manager = enemy_manager
        self.hp = 100
        self.speed_boost_duration = 5000
        self.speed_boost_start_time = 0
        self.speed_boost_active = False
        self.load_assets()
        self.slash()
        self.reset_states()
        self.alive = True  # Trạng thái nhân vật



    def slash(self):
        self.slash_right = pygame.image.load(os.path.join(Sprites_folder, 'wind burst.png'))
        self.slash_left = pygame.image.load(os.path.join(Sprites_folder, 'wind burst2.png'))
        self.slash_rect = pygame.Rect(0, 0, self.slash_right.get_width(), self.slash_right.get_height())
        self.slash_speed = 10
        self.slash_active = False
        self.slash_direction = 1  # 1 for right, -1 for left
        self.slash_animation = False
        self.slash_start_x = 0
        self.max_slash_distance = 300  # Maximum distance the slash can travel
        self.slash_hitted = False

    def take_damage(self, damage):
        """Giảm máu của nhân vật khi bị tấn công."""
        if self.alive:
            self.hp -= damage
            # print(f"Character HP: {self.hp}")
            if self.hp <= 0:
                self.hp = 0
                self.alive = False
                print("Game Over! Character died.")

    def load_assets(self):
        self.load_gif()
        self.load_attack_frames()
        self.load_charge_attack_frames()
        self.load_run_frames()
        self.load_dash_frames()

    def load_gif(self):
        gif_path = os.path.join(Sprites_folder, 'lil dude bigger.gif')
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
        attack_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'lil dude big.png')).convert_alpha()
        self.attack_frames = []
        sprite_width, sprite_height = attack_sprite_sheet.get_width() // 6, attack_sprite_sheet.get_height()

        for i in range(6):
            frame = attack_sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
            self.attack_frames.append(frame)

        self.flipped_attack_frames = [pygame.transform.flip(frame, True, False) for frame in self.attack_frames]

    def load_charge_attack_frames(self):
        charge_attack_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'Battery.png')).convert_alpha()
        self.charge_attack_frames = []
        charge_sprite_width, charge_sprite_height = charge_attack_sprite_sheet.get_width() // 9, charge_attack_sprite_sheet.get_height()

        for i in range(9):
            charge_frame = charge_attack_sprite_sheet.subsurface((i * charge_sprite_width, 0, charge_sprite_width, charge_sprite_height))
            self.charge_attack_frames.append(charge_frame)

        self.flipped_charge_attack_frames = [pygame.transform.flip(charge_frame, True, False) for charge_frame in self.charge_attack_frames]

    def load_run_frames(self):
        run_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'running.png')).convert_alpha()
        self.run_frames = []
        run_width, run_height = run_sprite_sheet.get_width() // 8, run_sprite_sheet.get_height()

        for i in range(8):
            run_frame = run_sprite_sheet.subsurface((i * run_width, 0, run_width, run_height))
            self.run_frames.append(run_frame)

        self.flipped_run_frames = [pygame.transform.flip(run_frame, True, False) for run_frame in self.run_frames]

    def load_dash_frames(self):
        dash_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'Dash.png')).convert_alpha()
        self.dash_frames = []
        dash_width, dash_height = dash_sprite_sheet.get_width() // 8, dash_sprite_sheet.get_height()

        for i in range(8):
            dash_frame = dash_sprite_sheet.subsurface((i * dash_width, 0, dash_width, dash_height))
            self.dash_frames.append(dash_frame)

        self.flipped_dash_frames = [pygame.transform.flip(dash_frame, True, False) for dash_frame in self.dash_frames]

    def reset_states(self):
        self.character_rect = self.frames[0].get_rect(center=(self.width // 2, self.height // 2))
        self.hitbox = self.character_rect.copy()
        self.hitbox.inflate_ip(-40, -40)
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
        self.frame_update_rate = 10
        self.attack_frame_update_rate = 2
        self.charge_frame_update_rate = 4
        self.dash_frame_update_rate = 2
        self.dash_duration = len(self.dash_frames)
        self.dash_speed = 10
        self.character_direction = None
        self.collision = False
        self.movement_speed = 5

    def activate_speed_boost(self, current_time):
        self.speed_boost_active = True
        self.speed_boost_start_time = current_time
        self.movement_speed = 20  # Increase movement speed
        print(f"Speed boost activated at {current_time}.")

    def handle_speed_boost(self, current_time):
        if self.speed_boost_active:
            time_left = current_time - self.speed_boost_start_time
            print(time_left)
            # print(f"current_time = {current_time}, speed_boost_start_time = {self.speed_boost_start_time}")
            if current_time - self.speed_boost_start_time >= self.speed_boost_duration:
                self.movement_speed = 5  # Reset to normal state including movement speed
                self.speed_boost_active = False
                print("Speed boost ended.")

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        self.running = False

        min_x, max_x = 0, self.width - 15 - self.character_rect.width
        top_border, bottom_border = 70, self.height - 32 - self.character_rect.height

        if keys[pygame.K_a]:
            self.character_direction = 'Left'
            self.character_rect.x = max(min_x, self.character_rect.x - self.movement_speed)
            self.running = True
            self.flipped = False
        if keys[pygame.K_d]:
            self.character_direction = 'Right'
            self.character_rect.x = min(max_x, self.character_rect.x + self.movement_speed)
            self.running = True
            self.flipped = True
        if keys[pygame.K_w]:
            self.character_rect.y = max(top_border, self.character_rect.y - self.movement_speed)
            self.running = True
        if keys[pygame.K_s]:
            self.character_rect.y = min(bottom_border, self.character_rect.y + self.movement_speed)
            self.running = True

        if self.dashing:
            if self.flipped:
                self.character_rect.x = min(max_x, self.character_rect.x + self.dash_speed)
            else:
                self.character_rect.x = max(min_x, self.character_rect.x - self.dash_speed)

            if self.character_rect.y < top_border:
                self.character_rect.y = top_border
            elif self.character_rect.y > bottom_border:
                self.character_rect.y = bottom_border

            self.dash_frame_counter += 1
            if self.dash_frame_counter >= self.dash_frame_update_rate:
                self.dash_frame_counter = 0
                self.dash_frame_index = (self.dash_frame_index + 1) % len(self.dash_frames)

            if self.dash_frame_index == len(self.dash_frames) - 1:
                self.dashing = False

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
                self.charge_frame_index = 0
                self.slash_animation = True
                self.slash_active = True
                self.slash_rect.center = self.character_rect.center
                self.slash_start_x = self.slash_rect.x
                self.slash_direction = 1 if self.flipped else -1
        elif self.slash_animation:
            if self.flipped:
                screen.blit(self.flipped_frames[self.frame_index], self.character_rect)
            else:
                screen.blit(self.frames[self.frame_index], self.character_rect)
            if self.slash_active:
                slash_image = self.slash_right if self.slash_direction == 1 else self.slash_left
                self.slash_rect.x += self.slash_speed * self.slash_direction
                screen.blit(slash_image, self.slash_rect)
                if abs(self.slash_rect.x - self.slash_start_x) > self.max_slash_distance or self.slash_rect.x < 0 or self.slash_rect.x > self.width:
                    self.slash_active = False
                    self.slash_animation = False
                    self.slash_rect.topleft = (-1000, -1000)
                for enemy in self.enemy_manager.enemies:
                    if self.slash_rect.colliderect(enemy.rect):
                        self.slash_hitted = True
                        current_time = time.time()
                        enemy.update_hit_count(current_time)

            self.slash_hitted = False

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

class Game:
    def __init__(self):
        pygame.init()
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)
        self.dropped_items = []  # List to hold dropped items

        self.load_enemy_frames()
        self.load_enemies()

        self.enemy_manager = EnemyManager(self.enemy_frames, self.width, self.height, 100, 2, self.enemy_list, self.clock)
        self.character = Character(self.width, self.height, self.enemy_manager)
        # self.loaditem = LoadItem

        self.attack_sound = pygame.mixer.Sound(os.path.join(Music_folder, 'sword-sound-260274.wav'))
        self.charge_sound = pygame.mixer.Sound(os.path.join(Music_folder, 'loud-thunder-192165.wav'))
        self.dash_sound = pygame.mixer.Sound(os.path.join(Music_folder, 'Dash-_Jett_-Sound-Effect-_Valorant-Game-SFX_.wav'))
        self.pick_up_sound = pygame.mixer.Sound(os.path.join(Music_folder, 'Pop-_Minecraft-Sound_-Sound-Effect-for-editing.wav'))

        self.scale_factor = 0.5
        self.stairway = pygame.image.load(os.path.join(Sprites_folder, 'Stairway.png'))
        self.stairway = pygame.transform.scale(self.stairway, (int(self.stairway.get_width() * self.scale_factor), int(self.stairway.get_height() * self.scale_factor)))
        self.stairway_rect = self.stairway.get_rect(center=(self.width // 2, self.height // 2))
        self.obstacle = pygame.image.load(os.path.join(Sprites_folder, 'tree.png'))
        self.obstacle = pygame.transform.scale(self.obstacle, (int(self.obstacle.get_width() * 0.3), int(self.obstacle.get_height() * 0.3)))
        self.rock = pygame.image.load(os.path.join(Sprites_folder, 'rock.png'))
        self.rock = pygame.transform.scale(self.rock, (int(self.rock.get_width() * self.scale_factor), int(self.rock.get_height() * self.scale_factor)))

        self.obstacle_list = []
        self.game_objs = []
        self.stair_drawn = False

        self.cross = Cross(self.width, self.height)

        self.charge_ui = pygame.image.load(os.path.join(Sprites_folder, 'Skill icon.png'))
        self.charge_ui = pygame.transform.scale(self.charge_ui, (int(self.charge_ui.get_width() * self.scale_factor), int(self.charge_ui.get_height() * self.scale_factor)))
        self.charge_ui_rect = self.charge_ui.get_rect(center=(1220, 45))
        self.dash_ui = pygame.image.load(os.path.join(Sprites_folder, 'Dash icon2.png'))
        self.dash_ui = pygame.transform.scale(self.dash_ui, (int(self.dash_ui.get_width() * self.scale_factor), int(self.dash_ui.get_height() * self.scale_factor)))
        self.dash_ui_rect = self.dash_ui.get_rect(center=(1120, 45))
        self.cooldown_effect = pygame.image.load(os.path.join(Sprites_folder, 'Skill cooldown.png'))
        self.cooldown_effect = pygame.transform.scale(self.cooldown_effect, (int(self.cooldown_effect.get_width() * self.scale_factor), int(self.cooldown_effect.get_height() * self.scale_factor)))
        self.cooldown_effect_rect = self.cooldown_effect.get_rect(center=(1220, 45))
        self.cooldown_effect_2 = pygame.image.load(os.path.join(Sprites_folder, 'Dash cooldown.png'))
        self.cooldown_effect_2 = pygame.transform.scale(self.cooldown_effect_2, (int(self.cooldown_effect_2.get_width() * self.scale_factor), int(self.cooldown_effect_2.get_height() * self.scale_factor)))
        self.cooldown_effect_2_rect = self.cooldown_effect_2.get_rect(center=(1120, 45))
        self.Hp_bar = pygame.image.load(os.path.join(Sprites_folder, 'HP.png'))
        self.Hp_bar = pygame.transform.scale(self.Hp_bar, (int(self.Hp_bar.get_width() * self.scale_factor), int(self.Hp_bar.get_height() * self.scale_factor)))
        self.Hp_bar_rect = self.Hp_bar.get_rect(topleft=(0, 0))
        self.Inv = pygame.image.load(os.path.join(Sprites_folder, 'inv.png'))
        self.Inv = pygame.transform.scale(self.Inv, (int(self.Inv.get_width() * self.scale_factor), int(self.Inv.get_height() * self.scale_factor)))
        self.Inv_rect = self.Inv.get_rect(topleft=(0, 0))
        self.frame_ui = pygame.image.load(os.path.join(Sprites_folder, 'Frame2.png'))
        self.frame_ui = pygame.transform.scale(self.frame_ui, (int(self.frame_ui.get_width() * self.scale_factor), int(self.frame_ui.get_height() * self.scale_factor)))
        self.frame_ui_rect = self.frame_ui.get_rect(center=(1220, 45))
        self.frame_ui2 = pygame.image.load(os.path.join(Sprites_folder, 'Frame1.png'))
        self.frame_ui2 = pygame.transform.scale(self.frame_ui2, (int(self.frame_ui2.get_width() * self.scale_factor), int(self.frame_ui2.get_height() * self.scale_factor)))
        self.frame_ui2_rect = self.frame_ui2.get_rect(center=(1120, 45))
        self.bg = pygame.image.load(os.path.join(Sprites_folder, 'Map_placeholder (1).png'))

        self.slot_inventory = {
            "slot1": {
                "slot_1_pos": (60, 65),
                "status": False
            },
            "slot2": {
                "slot_2_pos": (100, 65),
                "status": False
            }
        }
        self.level = 0

    def check_and_increase_level(self):
        if not self.enemy_manager.enemies and self.stair_drawn:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.level += 1
                if self.level == 3:
                    spawn_boss()
                else:
                    self.move_next_level()
                    self.enemy_manager.spawn_multiple_enemies(Vector2(self.width // 4, self.height // 4), self.character, self)

    def get_time(self):
        return self.clock.get_time()

    def load_enemies(self):
        self.enemy_list = []
        self.enemies = {}
        with open(os.path.join(script_dir, 'enemy_list.txt'), mode='r') as file:
            for line in file:
                key, value = line.strip().split(': ')
                self.enemies[key] = int(value)

        for enemy, count in self.enemies.items():
            self.enemy_list.extend([enemy] * count)

    def update_game_objs(self):
        self.game_objs.clear()
        self.game_objs.append({"type": "character", "sprite": self.character.frames[0], "rect": self.character.character_rect})
        for obstacle in self.obstacle_list:
            self.game_objs.append({"type": "obstacle", "sprite": obstacle["sprite"], "rect": obstacle["rect"]})

        for enemy in self.enemy_manager.enemies:
            self.game_objs.append({"type": "enemy", "enemy": enemy, "rect": enemy.rect})

    def check_enemy_list(self):
        if not self.enemy_manager.enemies and not self.stair_drawn:
            self.stair_drawn = True
        if self.stair_drawn:
            self.screen.blit(self.stairway, self.stairway_rect)

        # Draw all dropped items
        for item in self.enemy_manager.dropped_items:
            item.draw(self.screen, self.character.character_rect)

    def move_next_level(self):
        self.enemy_manager.dropped_items.clear()
        self.stair_drawn = False
        self.obstacle_list.clear()
        for _ in range(random.randint(5, 10)):
            obstacle_type = random.choice(["tree", "rock"])
            if obstacle_type == "tree":
                obstacle_sprite = self.obstacle
                obstacle_rect = self.obstacle.get_rect()
            else:
                obstacle_sprite = self.rock
                obstacle_rect = self.rock.get_rect()

            obstacle_rect.centerx = random.randint(100, self.width - 100)
            obstacle_rect.centery = random.randint(100, self.height - 100)
            self.obstacle_list.append({"sprite": obstacle_sprite, "rect": obstacle_rect})
            print(f"Spawned obstacle at position: ({obstacle_rect.centerx}, {obstacle_rect.centery})")

        self.update_game_objs()
        self.enemy_manager.spawn_multiple_enemies(Vector2(self.width // 4, self.height // 4), self.character, self)

    def load_enemy_frames(self):
        self.enemy_frames = {}
        self.enemy_frames["goblin"] = self.load_frames(os.path.join(Sprites_folder, 'Goblin.gif'))
        self.enemy_frames["goblin_attack"] = self.load_frames(os.path.join(Sprites_folder, 'GoblinAtk.gif'))  # Load attack frames
        self.enemy_frames["witch"] = self.load_frames(os.path.join(Sprites_folder, 'black Wizard.gif'))
        self.enemy_frames["witch_teleport"] = self.load_frames(os.path.join(Sprites_folder, 'black Wizard teleport v.gif'))
        self.enemy_frames["skeleton"] = self.load_frames(os.path.join(Sprites_folder, 'skele.gif'))
        self.enemy_frames["skeleton_attack"] = self.load_frames(os.path.join(Sprites_folder, 'Skeleshoot.gif'))
        self.enemy_frames["poison"] = self.load_frames(os.path.join(Sprites_folder, 'Poisoncloud.gif'))


    def load_frames(self, gif_path):
        gif = Image.open(gif_path)
        frames = []
        try:
            while True:
                frame = gif.copy()
                frame = frame.convert("RGBA")
                frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
                gif.seek(len(frames))
        except EOFError:
            pass
        return frames

    def draw(self):
        self.game_objs.sort(key=lambda obj: obj["rect"].centery)
        for obj in self.game_objs:
            if obj["type"] == "character":
                self.character.draw(self.screen)
            elif obj["type"] == "enemy":
                obj["enemy"].draw(self.screen)
            else:
                self.screen.blit(obj["sprite"], obj["rect"])

        # Ensure dropped items are drawn
        self.enemy_manager.draw(self.screen, self.character.character_rect)

    def run(self):
        self.enemy_manager.spawn_multiple_enemies(Vector2(self.width // 4, self.height // 4), self.character, self)

        while True:
            self.screen.blit(self.bg, (0, 0))
            self.update_game_objs()
            self.check_enemy_list()
            self.draw()
            current_time = pygame.time.get_ticks()  # Get the current time
            current_hp = max_hp
            self.health_bar = HealthBar(max_hp, current_hp, position=(0, 0), scale_factor=0.5)

            self.health_bar.update(self.character.hp)
            self.health_bar.draw(self.screen)
            # Kiểm tra nếu nhân vật đã chết
            if not self.character.alive:
                print("Game Over!")
                pygame.quit()
                sys.exit()

            for enemy in self.enemy_manager.enemies:
                if isinstance(enemy, Goblin):
                    if self.character.hitbox.colliderect(enemy.rect):
                        enemy.goblin_special_attack(self.character, time.time())
                elif isinstance(enemy, Skeleton):
                    if enemy.arrow_active and self.character.hitbox.colliderect(enemy.arrow_hitbox):
                        enemy.skeleton_special_attack(self.character, time.time())
                elif isinstance(enemy, Witch):
                    for poison in enemy.poisons:
                        if self.character.hitbox.colliderect(poison.rect):
                            enemy.cast_poison(self.character)
                            break  # Only process one collision per frame

            for item in self.dropped_items:
                item.draw(self.screen, self.character.character_rect, current_time, self.character)

            if self.stair_drawn and self.character.character_rect.colliderect(self.stairway_rect):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.move_next_level()
                    self.enemy_manager.spawn_multiple_enemies(Vector2(self.width // 4, self.height // 4), self.character, self)

            self.cross.char_rect = self.character.character_rect
            self.enemy_manager.update(self.character.character_rect.center, self.character.attacking, self.character.charging, self.character)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.character.attacking = True
                        self.character.attack_frame_index = 0
                        self.character.attack_frame_counter = 0
                        self.attack_sound.play()
                        for enemy in self.enemy_manager.enemies:
                            if self.character.hitbox.colliderect(enemy.rect):
                                enemy.hit_recently = False
                    elif event.button == 3 and not self.character.charge_cooldown:
                        self.character.charging = True
                        self.character.charge_frame_index = 0
                        self.character.charge_frame_counter = 0
                        self.character.charge_cooldown = True
                        self.character.last_charge_time = time.time()
                        self.charge_sound.play()

            self.character.handle_keys()
            self.character.handle_speed_boost(current_time)  # Handle speed boost in the character

            collision_detected = False
            for enemy in self.enemy_manager.enemies:
                if self.character.hitbox.colliderect(enemy.rect):
                    collision_detected = True
                    break

            self.character.collision = collision_detected

            if self.character.collision:
                pygame.draw.rect(self.screen, (255, 255, 0), self.character.hitbox, 2)
                for enemy in self.enemy_manager.enemies:
                    if self.character.hitbox.colliderect(enemy.rect) and not enemy.eliminated:
                        pygame.draw.rect(self.screen, (255, 255, 0), enemy.rect, 2)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] and not self.character.dashing and not self.character.dash_cooldown:
                self.character.dashing = True
                self.character.dash_frame_index = 0
                self.character.dash_frame_counter = 0
                self.character.last_dash_time = time.time()
                self.character.dash_cooldown = True
                self.dash_sound.play()

            self.screen.blit(self.charge_ui, self.charge_ui_rect)
            self.screen.blit(self.dash_ui, self.dash_ui_rect)

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
                    dash_cooldown_rect = pygame.Rect(self.cooldown_effect_2_rect.left, self.cooldown_effect_2_rect.top, self.cooldown_effect_2_rect.width, cooldown_height_2)
                    cooldown_effect_partial_2 = self.cooldown_effect_2.subsurface((0, 0, self.cooldown_effect_2_rect.width, cooldown_height_2))
                    self.screen.blit(cooldown_effect_partial_2, dash_cooldown_rect)
                if dash_elapsed_time >= self.character.dash_cooldown_time:
                    self.character.dash_cooldown = False

            # Draw additional UI elements
            self.screen.blit(self.frame_ui, self.frame_ui_rect)
            self.screen.blit(self.frame_ui2, self.frame_ui2_rect)

            # Check and increase level if all enemies are eliminated
            self.check_and_increase_level()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
     game = Game() 
     game.run()
