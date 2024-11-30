import pygame
import sys
import time

# Khởi tạo Pygame
pygame.init()

info = pygame.display.Info()

# Thông số của cửa sổ pygame 
width = info.current_w
height = info.current_h
screen = pygame.display.set_mode((width, height - 50))
clock = pygame.time.Clock()

# Màu sắc
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255) # Màu trắng cho viền chữ

# Đường dẫn đến font Pixel
font_path = 'D:\SpiritKnight\Font\Pixelmax-Regular.otf'  # Thay thế bằng đường dẫn chính xác đến tệp font Pixel của bạn

# Font chữ Pixel
font = pygame.font.Font(font_path, 74)
title_font = pygame.font.Font(font_path, 200)  # Font chữ lớn hơn cho tiêu đề
credit_font = pygame.font.Font(font_path, 50)
# Văn bản Menu
text_title = title_font.render('SPIRIT KNIGHT', True, black)  # Tiêu đề game

# Vị trí văn bản
title_rect = text_title.get_rect(center=(width // 2, height // 2 - 300))

# Tải âm thanh click
click_sound_path = 'D:\SpiritKnight\Music\minecraft_click (mp3cut.net).mp3'  # Đảm bảo thay thế bằng đường dẫn chính xác
try:
    click_sound = pygame.mixer.Sound(click_sound_path)
except pygame.error as e:
    print(f"Không thể tải âm thanh click: {e}")
    sys.exit()

# Tải hình ảnh
image_path = 'D:\SpiritKnight\Sprites\Background_menu.jpg'  # Đảm bảo thay thế bằng đường dẫn chính xác
logo_path = 'D:\SpiritKnight\Sprites\Goblin.gif'  # Đảm bảo thay thế bằng đường dẫn chính xác
credit_bg_path = 'D:\SpiritKnight\Sprites/background_credit.jpg' # Thay thế bằng đường dẫn chính xác đến tệp ảnh nền của bạn
options_image_path = 'D:\SpiritKnight\Sprites\Options_Background.jpg' # Thay thế bằng đường dẫn chính xác
try:
    background_image = pygame.image.load(image_path)
    background_image = pygame.transform.scale(background_image, (width, height))  # Điều chỉnh kích thước ảnh nền nếu cần
    logo_image = pygame.image.load(logo_path)
    logo_image = pygame.transform.scale(logo_image, (400, 200))  # Điều chỉnh kích thước logo nếu cần
    credit_background_image = pygame.image.load(credit_bg_path)
    credit_background_image = pygame.transform.scale(credit_background_image, (width, height))
    options_background_image = pygame.image.load(options_image_path)
    options_background_image = pygame.transform.scale(options_background_image, (width, height)) # Điều chỉnh kích thước ảnh nền nếu cần
except pygame.error as e:
    print(f"Không thể tải hình ảnh: {e}")
    sys.exit()

# Hàm cắt các hình ảnh từ sprite sheet
def load_sprite_sheet(sheet, frame_width, frame_height, num_frames):
    frames = []
    sheet_rect = sheet.get_rect()
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

# Tải sprite sheet và cắt các hình ảnh
try:
    start_sprite_sheet = pygame.image.load('D:\SpiritKnight\Sprites\Start.png')
    options_sprite_sheet = pygame.image.load('D:\SpiritKnight\Sprites\Option.png')
    quit_sprite_sheet = pygame.image.load('D:\SpiritKnight\Sprites\Quit.png')

    start_frames = load_sprite_sheet(start_sprite_sheet, 640, 100, 2)  # Chỉnh sửa với kích thước và số lượng khung hình
    options_frames = load_sprite_sheet(options_sprite_sheet, 640, 100, 2)  # Chỉnh sửa với kích thước và số lượng khung hình
    quit_frames = load_sprite_sheet(quit_sprite_sheet, 640, 100, 2)  # Chỉnh sửa với kích thước và số lượng khung hình
except pygame.error as e:
    print(f"Không thể tải sprite sheet: {e}")
    sys.exit()

# Lớp Button để quản lý sprite
class Button:
    def __init__(self, frames, pos):
        self.frames = frames
        self.rect = self.frames[0].get_rect(center=pos)
        self.pressed = False

    def draw(self, surface):
        if self.pressed:
            surface.blit(self.frames[1], self.rect)
        else:
            surface.blit(self.frames[0], self.rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.pressed = True
            click_sound.play() # Phát âm thanh khi nút được click
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
            self.pressed = False
            return True
        return False
    
# Tạo biến để lưu trạng thái của ô vuông
music_on = True

# Hàm để vẽ ô vuông và dấu tick
def draw_checkbox(surface, pos, checked):
    rect = pygame.Rect(pos, (30, 30))
    pygame.draw.rect(surface, black, rect, 4) 
    if checked:
        pygame.draw.lines(surface, black, False, [(pos[0] + 5, pos[1] + 15), (pos[0] + 15, pos[1] + 25), (pos[0] + 25, pos[1] + 5)], 6) 

# Hàm để xử lý bật/tắt nhạc khi tick vào ô vuông
def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.play(-1)
    else:    
        pygame.mixer.music.stop()

# Cập nhật hàm để hiển thị ô vuông và gọi hàm toggle_music khi tick vào ô vuông
def options_menu():
    while True:
        screen.blit(options_background_image, (0, 0)) # Hiển thị ảnh nền cho menu tùy chọn        
        
        # Hiển thị ô vuông và văn bản
        draw_checkbox(screen, (width // 2 - 50, height // 2), music_on)
        checkbox_text = credit_font.render('Music', True, black)
        screen.blit(checkbox_text, (width // 2, height // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(width // 2 - 50, height // 2, 30, 30).collidepoint(event.pos):
                    toggle_music()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return # Quay lại menu chính

        pygame.display.flip()

# Tạo văn bản cho nút Credit
credit_font = pygame.font.Font(font_path, 50)
credit_text = credit_font.render('Credit', True, black)
credit_outline = credit_font.render('Credit', True, white)
credit_rect = credit_text.get_rect(topleft=(15, height - 120)) # Vị trí góc trái màn hình

# Hàm để hiển thị thông tin Credit
def show_credits():
    while True:
        screen.blit(credit_background_image, (0, 0))
        credit_info = [
            "Developed by: Your Name",
            "Art by: Your Artist",
            "Music by: Your Musician",
            "Special Thanks to: Your Supporters"
            ]
        y_offset = 100
        for line in credit_info:
            try:
                credit_line = credit_font.render(line, True, black)
                screen.blit(credit_line, (50, y_offset))
                y_offset += 60
            except pygame.error as e:
                print(f"Lỗi khi render văn bản: {e}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return # Quay lại menu chính khi nhấn phím hoặc click chuột
        pygame.display.flip()

# Tạo các nút
start_button = Button(start_frames, (width // 2, height // 2 - 100))
options_button = Button(options_frames, (width // 2, height // 2 + 50))
quit_button = Button(quit_frames, (width // 2, height // 2 + 200))

# Tải và phát nhạc nền
music_path = 'D:\SpiritKnight\Music\Melancholic Walk.mp3'  # Thay thế bằng đường dẫn chính xác đến tệp nhạc của bạn
try:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # Phát nhạc lặp lại không ngừng
except pygame.error as e:
    print(f"Không thể tải nhạc: {e}")
    sys.exit()

# Hiển thị logo trước khi vào menu chính
def show_logo():
    start_time = time.time()
    while time.time() - start_time < 3:  # Hiển thị logo trong 3 giây
        screen.fill(red)
        screen.blit(logo_image, (width // 2 - logo_image.get_width() // 2, height // 2 - logo_image.get_height() // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Chức năng Main Menu
def main_menu():
    while True:
        screen.blit(background_image, (0, 0))  # Hiển thị ảnh nền

        # Hiển thị tiêu đề với viền trắng và chữ đen
        outline_title = title_font.render('SPIRIT KNIGHT', True, white)
        main_title = title_font.render('SPIRIT KNIGHT', True, black)

        # Vị trí tiêu đề
        outline_rect = outline_title.get_rect(center=(width // 2, height // 2 - 300))
        main_rect = main_title.get_rect(center=(width // 2, height // 2 - 300))

        # Render tiêu đề với viền
        for dx in [-3, -2, -1, 1, 2, 3]:            
            for dy in [-3, -2, -1, 1, 2, 3]:
                screen.blit(outline_title, outline_rect.move(dx, dy))
                screen.blit(main_title, main_rect)

        # Hiển thị nút
        start_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)
        screen.blit(credit_outline, credit_rect.move(2, 2)) # Viền trắng chữ Credit
        screen.blit(credit_text, credit_rect) # Chữ Credit đen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.check_click(event):
                # Bắt đầu trò chơi
                return  # Thay bằng hàm bắt đầu trò chơi thực tế
            if options_button.check_click(event):
                # Tùy chọn trò chơi
                options_menu() # Gọi hàm options_menu
            if quit_button.check_click(event):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and credit_rect.collidepoint(event.pos):
                show_credits()

        pygame.display.flip()

# Gọi hàm Hiển thị Logo 
show_logo()

# Gọi hàm Main Menu
main_menu()

# Vòng lặp game chính (ví dụ)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background_image, (0, 0))  # Hiển thị ảnh nền
    pygame.display.flip()