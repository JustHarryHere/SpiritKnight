import pygame
import sys
import time
import subprocess
import os

# Initialize Pygame
pygame.init()

script_dir = os.path.dirname(os.path.abspath(__file__))

Sprites_folder = os.path.join(script_dir, '..', 'Sprites')
Music_folder = os.path.join(script_dir, '..', 'Music')
Font_folder = os.path.join(script_dir, '..', 'Font')

# Window parameters
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))

# Colors
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# Font paths and sizes
font_path = os.path.join(Font_folder, 'Pixelmax-Regular.otf')
font = pygame.font.Font(font_path, 55)
title_font = pygame.font.Font(font_path, 120)
credit_font = pygame.font.Font(font_path, 30)

# Menu text
text_title = title_font.render('SPIRIT KNIGHT', True, black)

# Text position
title_rect = text_title.get_rect(center=(width // 2, height // 2 - 160))

# Load click sound
click_sound_path = os.path.join(Music_folder, 'minecraft_click (mp3cut.net).mp3')
try:
    click_sound = pygame.mixer.Sound(click_sound_path)
except pygame.error as e:
    print(f"Cannot load click sound: {e}")
    sys.exit()

# Load images
image_path = os.path.join(Sprites_folder, 'Background_menu.jpeg')
logo_path = os.path.join(Sprites_folder, 'chill slime.png')
credit_bg_path = os.path.join(Sprites_folder, 'blur.jpeg')
options_image_path = os.path.join(Sprites_folder, 'blur.jpeg')
try:
    background_image = pygame.image.load(image_path)
    background_image = pygame.transform.scale(background_image, (width, height))
    logo_image = pygame.image.load(logo_path)
    logo_image = pygame.transform.scale(logo_image, (400, 200))
    credit_background_image = pygame.image.load(credit_bg_path)
    credit_background_image = pygame.transform.scale(credit_background_image, (width, height))
    options_background_image = pygame.image.load(options_image_path)
    options_background_image = pygame.transform.scale(options_background_image, (width, height))
except pygame.error as e:
    print(f"Cannot load images: {e}")
    sys.exit()

# Function to cut images from sprite sheet
def load_sprite_sheet(sheet, frame_width, frame_height, num_frames):
    frames = []
    sheet_rect = sheet.get_rect()
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

# Load sprite sheets and cut images
try:
    start_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'Start.png'))
    options_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'Option.png'))
    quit_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'Quit.png'))

    start_frames = load_sprite_sheet(start_sprite_sheet, 480, 75, 2)
    options_frames = load_sprite_sheet(options_sprite_sheet, 480, 75, 2)
    quit_frames = load_sprite_sheet(quit_sprite_sheet, 480, 75, 2)
except pygame.error as e:
    print(f"Cannot load sprite sheet: {e}")
    sys.exit()

# Button class to manage sprites
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
            click_sound.play()
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
            self.pressed = False
            return True
        return False

# Variable to store checkbox state
music_on = True

# Function to toggle music when checkbox is clicked
def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

# Function to draw checkbox and tick with outline
def draw_checkbox(surface, pos, checked):
    rect = pygame.Rect(pos, (30, 30))
    
    # Draw white outline
    for dx in [-1, 1, 0, 0]:
        for dy in [0, 0, -1, 1]:
            pygame.draw.rect(surface, white, rect.move(dx, dy), 4)
    # Draw black checkbox
    pygame.draw.rect(surface, black, rect, 4)
    
    if checked:
        # Draw white outline for tick
        for dx in [-1, 1, 0, 0]:
            for dy in [0, 0, -1, 1]:
                pygame.draw.lines(surface, white, False, [(pos[0] + 5 + dx, pos[1] + 15 + dy), (pos[0] + 15 + dx, pos[1] + 25 + dy), (pos[0] + 25 + dx, pos[1] + 5 + dy)], 6)
        # Draw black tick
        pygame.draw.lines(surface, black, False, [(pos[0] + 5, pos[1] + 15), (pos[0] + 15, pos[1] + 25), (pos[0] + 25, pos[1] + 5)], 6)

# Update function to display checkbox and call toggle_music when clicked
def options_menu():
    while True:
        screen.blit(options_background_image, (0, 0))  # Display background for options menu

        # Display checkbox and text
        draw_checkbox(screen, (width // 2 - 50, height // 2), music_on)
        
        # Create text with white outline
        checkbox_outline_text = credit_font.render('Music', True, white)
        checkbox_text = credit_font.render('Music', True, black)

        # Position
        text_rect = checkbox_text.get_rect(topleft=(width // 2, height // 2))

        # Draw outline by blitting multiple times at offset positions
        for dx in [-1, 1, 0, 0]:
            for dy in [0, 0, -1, 1]:
                screen.blit(checkbox_outline_text, text_rect.move(dx, dy))
        screen.blit(checkbox_text, text_rect)  # Blit main text

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(width // 2 - 50, height // 2, 30, 30).collidepoint(event.pos):
                    toggle_music()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Return to main menu

        pygame.display.flip()

# Create text for Credit button
credit_font = pygame.font.Font(font_path, 40)
credit_text = credit_font.render('Credit', True, black)
credit_outline = credit_font.render('Credit', True, white)
credit_rect = credit_text.get_rect(topleft=(15, height - 80))

# Function to display Credit information with outlined text
def show_credits():
    while True:
        screen.blit(credit_background_image, (0, 0))
        credit_info = [
            "Developed by: Dang Vuong, Hai Dang, Minh Thanh",
            "Art by: Nguyen Pham Thanh Tin",
            "Music by: Kevin Macleod, Pix",
            "Special Thanks to: Chat GPT, Copilot"
        ]
        y_offset = 100
        for line in credit_info:
            try:
                # Create text with white outline
                credit_outline = credit_font.render(line, True, white)
                credit_text = credit_font.render(line, True, black)
                
                # Position
                text_rect = credit_text.get_rect(topleft=(50, y_offset))

                # Draw outline by blitting multiple times at offset positions
                for dx in [-1, 1, 0, 0]:
                    for dy in [0, 0, -1, 1]:
                        screen.blit(credit_outline, text_rect.move(dx, dy))
                screen.blit(credit_text, text_rect)  # Blit main text

                y_offset += 60
            except pygame.error as e:
                print(f"Error rendering text: {e}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # Return to main menu when key is pressed or mouse is clicked
        pygame.display.flip()

# Create buttons
start_button = Button(start_frames, (width // 2, height // 2 - 50))
options_button = Button(options_frames, (width // 2, height // 2 + 50))
quit_button = Button(quit_frames, (width // 2, height // 2 + 150))

# Load and play background music
music_path = os.path.join(Music_folder, 'Melancholic Walk.mp3')
try:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # Play music in a loop
except pygame.error as e:
    print(f"Cannot load music: {e}")
    sys.exit()

# Function to show logo before main menu
def show_logo():
    start_time = time.time()
    while time.time() - start_time < 3:  # Show logo for 3 seconds
        screen.fill(black)
        screen.blit(logo_image, (width // 2 - logo_image.get_width() // 2, height // 2 - logo_image.get_height() // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Main menu function
def main_menu():
    while True:
        screen.blit(background_image, (0, 0))  # Display background

        # Display title with white outline and black text
        outline_title = title_font.render('SPIRIT KNIGHT', True, white)
        main_title = title_font.render('SPIRIT KNIGHT', True, black)

        # Title position
        outline_rect = outline_title.get_rect(center=(width // 2, height // 2 - 160))
        main_rect = main_title.get_rect(center=(width // 2, height // 2 - 160))

        # Draw outline by blitting multiple times at offset positions
        for dx in [-3, -2, -1, 1, 2, 3]:
            for dy in [-3, -2, -1, 1, 2, 3]:
                screen.blit(outline_title, outline_rect.move(dx, dy))
        screen.blit(main_title, main_rect)

        # Draw buttons
        start_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)
        screen.blit(credit_outline, credit_rect.move(2, 2))  # Credit text outline
        screen.blit(credit_text, credit_rect)  # Credit text

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.check_click(event):
                # Run the SpiritK9_Mechanics_source_update script
                pygame.quit()  # Quit Pygame to properly transition to the main game
                subprocess.run(['python', os.path.join(script_dir, 'SpiritK9_Mechanics_source_update.py')])
                return  # Exit the main menu loop
            if options_button.check_click(event):
                options_menu()  # Call options menu function
            if quit_button.check_click(event):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and credit_rect.collidepoint(event.pos):
                show_credits()

        pygame.display.flip()

# Call the show_logo function
show_logo()

# Call the main_menu function
main_menu()
