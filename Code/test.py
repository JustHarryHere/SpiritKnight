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
        flipped = True # Facing right
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

def main():
    pygame.init()
    info = pygame.display.Info()
    
    width = info.current_w
    height = info.current_h
    screen = pygame.display.set_mode((width, height-50))
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    
    gif_path = 'D:\\Sprites\\lil dude bigger.gif'
    goblin_gif = 'D:\\Sprites\\Goblin.gif'
    frames = []
    goblin_frames = []
    
    # Load character and goblin frames
    gif_image(Image.open(gif_path), frames)
    gif_image(Image.open(goblin_gif), goblin_frames)
    
    # Flip frames for left-facing sprites
    flipped_frames = [pygame.transform.flip(frame, True, False) for frame in frames]
    flipped_frames_goblin = [pygame.transform.flip(goblin_frame, True, False) for goblin_frame in goblin_frames]
    
    # Load frames for attack, charge, and run animations
    attack_frames = load_frames_from_sprite_sheet('D:\\Sprites\\lil dude big.png', 6)
    charge_attack_frames = load_frames_from_sprite_sheet('D:\\Sprites\\Battery.png', 9)
    run_frames = load_frames_from_sprite_sheet('D:\\Sprites\\running.png', 8)

    # Flip frames for left-facing animations
    flipped_attack_frames = [pygame.transform.flip(frame, True, False) for frame in attack_frames]
    flipped_charge_attack_frames = [pygame.transform.flip(frame, True, False) for frame in charge_attack_frames]
    flipped_run_frames = [pygame.transform.flip(frame, True, False) for frame in run_frames]
    
    # Set up character initial position
    character_rect = frames[0].get_rect(center=(width // 2, height // 2))
    character_pos = Vector2(character_rect.center)
    
    min_distance = 50
    enemies = []
    for _ in range(1):
        enemy_pos = spawn_enemy(character_pos, width, height, min_distance)
        enemy_rect = goblin_frames[0].get_rect(center=enemy_pos)
        enemies.append({"pos": enemy_pos, "rect": enemy_rect, "direction": "right", "hit_range": 100})
        
    removed_enemies = []
    speed = 2
    
    frame_index = 0
    run_frame_index = 0
    attack_frame_index = 0
    charge_frame_index = 0
    
    flipped = False
    attacking = False
    charging = False
    charge_cooldown = False
    
    cooldown_time = 2
    last_charge_time = 0
    
    frame_counter = 0
    run_frame_counter = 0
    attack_frame_counter = 0
    charge_frame_counter = 0
    
    frame_update_rate = 10
    attack_frame_update_rate = 2
    charge_frame_update_rate = 4
    
    cooldown_duration = 2
    cooldown_start_time = None
    skill_active = False
    
    esc_pressed = False
    
    while True:
        screen.fill((0, 0, 0))
        
        # Handle events and user inputs
        attacking, attack_frame_index, attack_frame_counter, charging, charge_frame_index, charge_frame_counter, charge_cooldown, last_charge_time, skill_active, cooldown_start_time = handle_events(attacking, attack_frame_index, attack_frame_counter, charging, charge_frame_index, charge_frame_counter, charge_cooldown, last_charge_time, skill_active, cooldown_start_time)
        
        running, flipped = handle_keys(character_rect, width, height, flipped)
        
        # Update character animation state
        if charging:
            if flipped:
                screen.blit(flipped_charge_attack_frames[charge_frame_index], character_rect)
            else:
                screen.blit(charge_attack_frames[charge_frame_index], character_rect)
            charge_frame_counter += 1
            if charge_frame_counter >= charge_frame_update_rate:
                charge_frame_counter = 0
                charge_frame_index += 1
            if charge_frame_index >= len(charge_attack_frames):
                charging = False
        elif attacking:
            if flipped:
                screen.blit(flipped_attack_frames[attack_frame_index], character_rect)
            else:
                screen.blit(attack_frames[attack_frame_index], character_rect)
            attack_frame_counter += 1
            if attack_frame_counter >= attack_frame_update_rate:
                attack_frame_counter = 0
                attack_frame_index += 1
            if attack_frame_index >= len(attack_frames):
                attacking = False
        elif running:
            if flipped:
                screen.blit(flipped_run_frames[run_frame_index], character_rect)
            else:
                screen.blit(run_frames[run_frame_index], character_rect)
            run_frame_counter += 1
            if run_frame_counter >= frame_update_rate:
                run_frame_counter = 0
                run_frame_index = (run_frame_index + 1) % len(run_frames)
        else:
            frame_counter += 1
            if frame_counter >= frame_update_rate:
                frame_counter = 0
                frame_index = (frame_index + 1) % len(frames)
            if flipped:
                screen.blit(flipped_frames[frame_index], character_rect)
            else:
                screen.blit(frames[frame_index], character_rect)
        
        # Reset charge cooldown
        if charge_cooldown and time.time() - last_charge_time >= cooldown_time:
            charge_cooldown = False
        
        frame_index = 0
        frame_duration_goblin = 100
        last_update = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        
        if current_time - last_update > frame_duration_goblin:
            frame_index = (frame_index + 1) % len(frames)
            last_update = current_time
        
        for enemy in enemies[:]:
            enemy_pos = enemy["pos"]
            enemy_rect = enemy["rect"]
            player_pos = Vector2(character_rect.center)
            distance_to_player = player_pos.distance_to(enemy_pos)
            direction = player_pos - enemy_pos
            if distance_to_player < enemy["hit_range"]:
                direction = (player_pos - enemy_pos).normalize() if direction.length() != 0 else Vector2(0, 0)
                
                if attacking:
                    enemies.remove(enemy)
                    removed_enemies.append(enemy)
                elif charging:
                    time.sleep(0.1)
                    enemies.remove(enemy)
                    removed_enemies.append(enemy)
                else:
                    if direction.x < 0:
                        enemy["direction"] = "right"
                    else:
                        enemy["direction"] = "left"
            else:
                if direction.length() >= min_distance:
                    direction = direction.normalize()
                enemy_pos += direction * speed
                enemy_rect.center = enemy_pos

            if direction.x < 0:
                enemy["direction"] = "right"
            else:
                enemy["direction"] = "left"

            if enemy["direction"] == "right":
                screen.blit(goblin_frames[frame_index], enemy_rect)
            else:
                screen.blit(flipped_frames_goblin[frame_index], enemy_rect)

        # Drawing the skill cooldown indicator
        center = (50, 50)
        radius = 30

        if skill_active:
            elapsed_time = (pygame.time.get_ticks() - cooldown_start_time) / 1000
            if elapsed_time >= cooldown_duration:
                skill_active = False
                elapsed_time = cooldown_duration
            angle = (elapsed_time / cooldown_duration) * 360
            end_angle = angle
            start_angle = 0
            pygame.draw.circle(screen, (100, 100, 100), center, radius)
            pygame.draw.arc(screen, (0, 255, 0), (center[0] - radius, center[1] - radius, 2 * radius, 2 * radius), math.radians(start_angle - 90), math.radians(end_angle - 90), radius)
        else:
            pygame.draw.circle(screen, (0, 255, 0), center, radius)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()

