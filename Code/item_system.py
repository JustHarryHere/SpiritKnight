import pygame, sys
from PIL import Image

pygame.init()
pygame.mixer.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Dùng cho stack item
item_count = 0

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

flipped_frames = [pygame.transform.flip(char_frame, True, False) for char_frame in char_frames]

#Item 1 
cross_gif_path = 'D:/SpiritKnight/Sprites/Mary on a.gif'
cross_gif = Image.open(cross_gif_path)
cross_frames = []
try:
    while True:
        cross_frame = cross_gif.copy()
        cross_frame = cross_frame.convert("RGBA")
        cross_frame = cross_frame.resize((60, 60), Image.Resampling.LANCZOS)
        cross_frames.append(pygame.image.fromstring(cross_frame.tobytes(), cross_frame.size, cross_frame.mode))
        cross_gif.seek(len(cross_frames))  # Move to the next frame
except EOFError:
    pass


char_rect = char_frames[0].get_rect(center=(width//2, height//2))
cross_rect = cross_frames[0].get_rect(center = (width//2 + 100, height// 2))
frame_index = 0
cross_frame_index = 0
frame_counter = 0
frame_update_rate = 5
flipped = False
picked_up = False

pick_up_sound = pygame.mixer.Sound('D:/SpiritKnight/Music/Item-Pick-up-_Counter-Strike-Source_-Sound-Effect-for-editing.wav')

scale_factor = 0.5
Hp_bar = pygame.image.load('D:/SpiritKnight/Sprites/HP.png').convert_alpha()
Hp_bar = pygame.transform.scale(Hp_bar, (int(Hp_bar.get_width()*scale_factor), int(Hp_bar.get_height()*scale_factor)))
Hp_rect = Hp_bar.get_rect(topleft = (0,0))
Inv = pygame.image.load('D:/SpiritKnight/Sprites/inv.png').convert_alpha()
Inv = pygame.transform.scale(Inv, (int(Inv.get_width()*scale_factor), int(Inv.get_height()*scale_factor)))
Inv_rect = Inv.get_rect(topleft = (0,0))
item_1 = pygame.image.load('D:/SpiritKnight/Sprites/mary1.png').convert_alpha()
item_1_rect = item_1.get_rect(center = (75,78))
bg = pygame.image.load('D:/SpiritKnight/Sprites/Map_placeholder (1).png')
#bg = pygame.transform.scale(bg, (int(bg.get_width()*scale_factor), int(bg.get_height()*scale_factor)))
bg_rect = bg.get_rect(topleft = (0,0))

while True:
    screen.fill((0, 0, 0))

    screen.blit(bg, bg_rect)
    screen.blit(Hp_bar, Hp_rect)
    screen.blit(Inv, Inv_rect)
    if picked_up:
        screen.blit(item_1, item_1_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    moving = False
    
    # Điều khiển di chuyển nhân vật
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
    
    # Nhặt vật phẩm
    if keys[pygame.K_f] and item_count < 2 and not picked_up:
        item_count += 1
        if char_rect.colliderect(cross_rect):
            picked_up = True
            pick_up_sound.play()
            # Đặt vị trí vật phẩm trong túi đồ
            item_1_rect.center = (75, 78)

    # Quăng vật phẩm
    if keys[pygame.K_g] and picked_up:
        item_count -= 1
        # item_count = 0 thì tiếp tục đoạn dưới và quăng vật phẩm, item_count còn 1 thì vẫn ở trong túi
        if item_count == 0:
          picked_up = False
        # Đặt vật phẩm gần nhân vật khi thả ra
          cross_rect.center = (char_rect.centerx + 50, char_rect.centery)

    # Hiển thị vật phẩm
    if not picked_up:
        screen.blit(cross_frames[cross_frame_index], cross_rect)

    # Cập nhật khung hình
    frame_counter += 1
    if frame_counter >= frame_update_rate:
        frame_counter = 0
        frame_index = (frame_index + 1) % len(char_frames)
        cross_frame_index = (cross_frame_index + 1) % len(cross_frames)
    
    # Hiển thị nhân vật
    if flipped:
        screen.blit(flipped_frames[frame_index], char_rect)
    else:
        screen.blit(char_frames[frame_index], char_rect)

    pygame.display.flip()
    clock.tick(60)
