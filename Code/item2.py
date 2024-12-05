import pygame, sys
from PIL import Image

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Character
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
frame_index = 0
frame_counter = 0
frame_update_rate = 5
flipped = False

# Load shielded character image
shielded_char_image = pygame.image.load('D:/SpiritKnight/Sprites/Frame1.png').convert_alpha()
shielded_char_image = pygame.transform.scale(shielded_char_image, (char_rect.width, char_rect.height))

immunity_effect_image = pygame.image.load('D:/SpiritKnight/Sprites/defalt circle.png').convert_alpha()
immunity_effect_image = pygame.transform.scale(immunity_effect_image, (100, 100))  # Điều chỉnh kích thước nếu cần

# Health
max_hp = 100
remaining_hp = 50
invincible = False  # Biến để kiểm tra trạng thái miễn sát thương
invincible_start_time = 0  # Thời điểm bắt đầu miễn sát thương

scale_factor = 0.5
Hp_bar = pygame.image.load('D:/SpiritKnight/Sprites/HP1.png')
Hp_bar = pygame.transform.scale(Hp_bar, (int(Hp_bar.get_width() * scale_factor), int(Hp_bar.get_height() * scale_factor)))
Hp_bar_rect = Hp_bar.get_rect(topleft=(0, 0))
Hp_2 = pygame.image.load('D:/SpiritKnight/Sprites/HP2.png')
Hp_2 = pygame.transform.scale(Hp_2, (int(Hp_2.get_width() * scale_factor), int(Hp_2.get_height() * scale_factor)))
Hp_2_rect = Hp_2.get_rect(topleft=(0, 0))

# Shield icon
shield_icon = pygame.image.load('D:/SpiritKnight/Sprites/Celestial_Opposition_item_HD.png').convert_alpha()
shield_icon = pygame.transform.scale(shield_icon, (40, 40))  # Adjust the size as needed
shield_icon_rect = shield_icon.get_rect(topleft=(Hp_bar_rect.left + 70, Hp_bar_rect.top + 70))

# Item on the ground
cross_image_path = 'D:/SpiritKnight/Sprites/Celestial_Opposition_item_HD.png'
cross_image = pygame.image.load(cross_image_path).convert_alpha()
cross_image = pygame.transform.scale(cross_image, (60, 60))
cross_rect = cross_image.get_rect(center=(width // 2, height // 2 + 100))

# Additional items on the ground
item2_image_path = 'D:/SpiritKnight/Sprites/Celestial_Opposition_item_HD.png'
item3_image_path = 'D:/SpiritKnight/Sprites/Celestial_Opposition_item_HD.png'

item2_image = pygame.image.load(item2_image_path).convert_alpha()
item2_image = pygame.transform.scale(item2_image, (60, 60))
item2_rect = item2_image.get_rect(center=(width // 2 - 100, height // 2 + 100))

item3_image = pygame.image.load(item3_image_path).convert_alpha()
item3_image = pygame.transform.scale(item3_image, (60, 60))
item3_rect = item3_image.get_rect(center=(width // 2 + 100, height // 2 + 100))

# Holy cross GIFs
holy_cross_gif_path = 'D:/SpiritKnight/Sprites/Mary on a.gif'
holy_cross_gif = Image.open(holy_cross_gif_path)
holy_cross_frames = []
holy_cross_width, holy_cross_height = 40, 40  # Kích thước mới của thánh giá
try:
    while True:
        holy_cross_frame = holy_cross_gif.copy()
        holy_cross_frame = holy_cross_frame.convert("RGBA")
        holy_cross_frame = holy_cross_frame.resize((holy_cross_width, holy_cross_height), Image.LANCZOS)  # Thay đổi kích thước
        holy_cross_frames.append(pygame.image.fromstring(holy_cross_frame.tobytes(), holy_cross_frame.size, holy_cross_frame.mode))
        holy_cross_gif.seek(len(holy_cross_frames))  # Move to the next frame
except EOFError:
    pass

holy_cross_rect1 = holy_cross_frames[0].get_rect(center=(width // 2 - 200, height // 2 - 200))
holy_cross_rect2 = holy_cross_frames[0].get_rect(center=(width // 2, height // 2 - 200))
holy_cross_rect3 = holy_cross_frames[0].get_rect(center=(width // 2 + 200, height // 2 - 200))
holy_cross_frame_index = 0
holy_cross_frame_counter = 0
holy_cross_frame_rate = 5  # Tốc độ cập nhật khung hình của thánh giá

# Vị trí icon thánh giá dưới thanh máu
holy_cross_icon_pos = (Hp_bar_rect.left + 110, Hp_bar_rect.top + 70)

# Health items
health_item_path = 'D:/SpiritKnight/Sprites/Trans.png'
health_item = pygame.image.load(health_item_path).convert_alpha()
health_item = pygame.transform.scale(health_item, (60, 60))
health_item_rect1 = health_item.get_rect(center=(width // 2 - 200, height // 2 + 200))
health_item_rect2 = health_item.get_rect(center=(width // 2, height // 2 + 200))
health_item_rect3 = health_item.get_rect(center=(width // 2 + 200, height // 2 + 200))

# Hazard area (for losing health)
hazard_rect = pygame.Rect(300, 200, 100, 100)  # Example position and size

# Timer for hazard damage
damage_timer = pygame.time.get_ticks()

# Biến để kiểm tra xem nhân vật đã nhặt thánh giá, khiên hay bình máu hay chưa
has_holy_cross = False
has_shield = False
has_health = [False, False, False]

#hồi sinh
def respawn_character():
    global remaining_hp, has_holy_cross
    
    if has_holy_cross:
        # Hồi sinh nhân vật
        remaining_hp = max_hp  # Hồi sinh với 100% máu
        has_holy_cross = False  # Xóa trạng thái sở hữu thánh giá
        print("Character respawned with full health at current position!")
    else:
        print("Game Over")
        pygame.quit()
        sys.exit()

# Trạng thái của từng cây thánh giá
holy_cross_picked = [False, False, False]  # True nếu cây đó đã bị nhặt

def pick_up_item():
    global has_shield, remaining_hp, has_holy_cross, has_health, holy_cross_picked
    
    if not has_shield:  # Chỉ lượm khi nhân vật chưa có khiên
        if char_rect.colliderect(cross_rect):
            has_shield = True
            cross_rect.center = (-100, -100)
        elif char_rect.colliderect(item2_rect):
            has_shield = True
            item2_rect.center = (-100, -100)
        elif char_rect.colliderect(item3_rect):
            has_shield = True
            item3_rect.center = (-100, -100)

    # Pick up health items
    if char_rect.colliderect(health_item_rect1) and not has_health[0]:
        remaining_hp = min(max_hp, remaining_hp + 20)
        has_health[0] = True
        health_item_rect1.center = (-100, -100)
    elif char_rect.colliderect(health_item_rect2) and not has_health[1]:
        remaining_hp = min(max_hp, remaining_hp + 20)
        has_health[1] = True
        health_item_rect2.center = (-100, -100)
    elif char_rect.colliderect(health_item_rect3) and not has_health[2]:
        remaining_hp = min(max_hp, remaining_hp + 20)
        has_health[2] = True
        health_item_rect3.center = (-100, -100)

    # Pick up holy cross items (chỉ nhặt từng cây một)
    if not has_holy_cross:  # Nếu chưa nhặt bất kỳ thánh giá nào
        if char_rect.colliderect(holy_cross_rect1) and not holy_cross_picked[0]:
            has_holy_cross = True
            holy_cross_picked[0] = True
            holy_cross_rect1.center = (-100, -100)  # Di chuyển cây ra khỏi màn hình
        elif char_rect.colliderect(holy_cross_rect2) and not holy_cross_picked[1]:
            has_holy_cross = True
            holy_cross_picked[1] = True
            holy_cross_rect2.center = (-100, -100)
        elif char_rect.colliderect(holy_cross_rect3) and not holy_cross_picked[2]:
            has_holy_cross = True
            holy_cross_picked[2] = True
            holy_cross_rect3.center = (-100, -100)


while True:
    screen.fill((0, 0, 0))

    screen.blit(Hp_bar, Hp_bar_rect)

    # Display the shield icon if the character has a shield or is invincible
    if has_shield or invincible:
        # Calculate the height of the remaining shield icon
        if invincible:
            elapsed_time = pygame.time.get_ticks() - invincible_start_time
            remaining_height = max(0, shield_icon.get_height() * (2000 - elapsed_time) / 2000)
            partial_icon = pygame.Surface((shield_icon.get_width(), remaining_height), pygame.SRCALPHA)
            partial_icon.blit(shield_icon, (0, 0), (0, 0, shield_icon.get_width(), remaining_height))
            screen.blit(partial_icon, shield_icon_rect.topleft)
        else:
            screen.blit(shield_icon, shield_icon_rect)

    # Kiểm tra nếu nhân vật chết
    if remaining_hp <= 0:
        respawn_character()


    # Hiển thị icon thánh giá nếu nhân vật đã nhặt thánh giá
    if has_holy_cross:
        screen.blit(holy_cross_frames[holy_cross_frame_index], holy_cross_icon_pos)

    # Drawing the hazard area
    pygame.draw.rect(screen, (255, 0, 0), hazard_rect)

    screen.blit(cross_image, cross_rect)
    screen.blit(item2_image, item2_rect)
    screen.blit(item3_image, item3_rect)

    # Drawing the health items
    if not has_health[0]:
        screen.blit(health_item, health_item_rect1)
    if not has_health[1]:
        screen.blit(health_item, health_item_rect2)
    if not has_health[2]:
        screen.blit(health_item, health_item_rect3)

    # Drawing the holy cross items
    if not holy_cross_picked[0]:  # Chỉ vẽ nếu cây 1 chưa bị nhặt
        screen.blit(holy_cross_frames[holy_cross_frame_index], holy_cross_rect1)
    if not holy_cross_picked[1]:  # Chỉ vẽ nếu cây 2 chưa bị nhặt
        screen.blit(holy_cross_frames[holy_cross_frame_index], holy_cross_rect2)
    if not holy_cross_picked[2]:  # Chỉ vẽ nếu cây 3 chưa bị nhặt
        screen.blit(holy_cross_frames[holy_cross_frame_index], holy_cross_rect3)

    # Update holy cross frames
    holy_cross_frame_counter += 1
    if holy_cross_frame_counter >= holy_cross_frame_rate:
        holy_cross_frame_counter = 0
        holy_cross_frame_index = (holy_cross_frame_index + 1) % len(holy_cross_frames)

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

    if keys[pygame.K_f]:
        pick_up_item()

    current_time = pygame.time.get_ticks()

    # Check if character steps into the hazard area and apply damage every 0.5 seconds
    if char_rect.colliderect(hazard_rect) and not invincible:
        if current_time - damage_timer >= 500:
            if has_shield:
                invincible = True  # Kích hoạt trạng thái miễn sát thương
                invincible_start_time = current_time
                has_shield = False  # Vỡ khiên sau 2 giây miễn sát thương
            else:
                remaining_hp -= 5
                damage_timer = current_time  # Reset the timer
                if remaining_hp < 0:
                    remaining_hp = 0

    # Kiểm tra nếu thời gian miễn sát thương đã hết
    if invincible and current_time - invincible_start_time >= 2000:
        invincible = False

    # Cập nhật khung hình
    frame_counter += 1
    if frame_counter >= frame_update_rate:
        frame_counter = 0
        frame_index = (frame_index + 1) % len(char_frames)

    # Hiển thị nhân vật và lớp khiên phía sau
    if flipped:
        frame_image = flipped_frames[frame_index]
    else:
        frame_image = char_frames[frame_index]

    if has_shield or invincible:
        screen.blit(shielded_char_image, char_rect.topleft)  # Lớp khiên phía sau nhân vật
    screen.blit(frame_image, char_rect)  # Hiển thị nhân vật phía trước

    # Hiển thị thanh máu
    font = pygame.font.Font('D:/SpiritKnight/Font/properhitboxglobal.ttf', 18)
    hp_text_black = font.render(f"{remaining_hp}/{max_hp}", True, (0, 0, 0))
    hp_text_rect = hp_text_black.get_rect(center=(240, 40))
    hp_text_white = font.render(f"{remaining_hp}/{max_hp}", True, (255, 255, 255))
    screen.blit(hp_text_black, hp_text_rect.move(2, 2))
    screen.blit(hp_text_white, hp_text_rect)

    pygame.display.flip()
    clock.tick(60)
