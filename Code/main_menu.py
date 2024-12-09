import pygame
import sys
import time
import subprocess
import os

# Initialize Pygame
pygame.init()

script_dir = os.path.dirname(os.path.abspath(__file__))

Sprites_folder = os.path.join(script_dir ,'..', 'Sprites')

Music_folder = os.path.join(script_dir, '..', 'Music')

Font_folder = os.path.join(script_dir, '..', 'Font')

# Window parameters
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))

# Colors
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)  # White color for text outline

# Path to Pixel font
font_path = os.path.join(Font_folder, 'Pixelmax-Regular.otf')  # Replace with the correct path to your Pixel font file

# Pixel font
font = pygame.font.Font(font_path, 55)
title_font = pygame.font.Font(font_path, 120)  # Larger font for title
credit_font = pygame.font.Font(font_path, 30)

# Menu text
text_title = title_font.render('SPIRIT KNIGHT', True, black)  # Game title

# Text position
title_rect = text_title.get_rect(center=(width // 2, height // 2 - 160))

# Load click sound
click_sound_path = os.path.join(Music_folder, 'minecraft_click (mp3cut.net).mp3')  # Ensure to replace with the correct path
try:
    click_sound = pygame.mixer.Sound(click_sound_path)
except pygame.error as e:
    print(f"Cannot load click sound: {e}")
    sys.exit()

# Load images
image_path = os.path.join(Sprites_folder, 'Background_menu.jpg')  # Ensure to replace with the correct path
logo_path = os.path.join(Sprites_folder, 'Goblin.gif')  # Ensure to replace with the correct path
credit_bg_path = os.path.join(Sprites_folder, 'background_credit.jpg')  # Replace with the correct path
options_image_path = os.path.join(Sprites_folder, 'Options_Background.jpg')  # Replace with the correct path
try:
    background_image = pygame.image.load(image_path)
    background_image = pygame.transform.scale(background_image, (width, height))  # Resize background image if necessary
    logo_image = pygame.image.load(logo_path)
    logo_image = pygame.transform.scale(logo_image, (400, 200))  # Resize logo if necessary
    credit_background_image = pygame.image.load(credit_bg_path)
    credit_background_image = pygame.transform.scale(credit_background_image, (width, height))
    options_background_image = pygame.image.load(options_image_path)
    options_background_image = pygame.transform.scale(options_background_image, (width, height))  # Resize background image if necessary
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

# Load sprite sheet and cut images
try:
    start_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'Start.png'))
    options_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'Option.png'))
    quit_sprite_sheet = pygame.image.load(os.path.join(Sprites_folder, 'Quit.png'))

    start_frames = load_sprite_sheet(start_sprite_sheet, 480, 75, 2)  # Adjust with correct dimensions and frame count
    options_frames = load_sprite_sheet(options_sprite_sheet, 480, 75, 2)  # Adjust with correct dimensions and frame count
    quit_frames = load_sprite_sheet(quit_sprite_sheet, 480, 75, 2)  # Adjust with correct dimensions and frame count
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
            click_sound.play()  # Play sound when button is clicked
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
            self.pressed = False
            return True
        return False

# Variable to store checkbox state
music_on = True

# Function to draw checkbox and tick
def draw_checkbox(surface, pos, checked):
    rect = pygame.Rect(pos, (30, 30))
    pygame.draw.rect(surface, black, rect, 4)
    if checked:
        pygame.draw.lines(surface, black, False, [(pos[0] + 5, pos[1] + 15), (pos[0] + 15, pos[1] + 25), (pos[0] + 25, pos[1] + 5)], 6)

# Function to toggle music when checkbox is clicked
def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

# Update function to display checkbox and call toggle_music when clicked
def options_menu():
    while True:
        screen.blit(options_background_image, (0, 0))  # Display background for options menu

        # Display checkbox and text
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
                    return  # Return to main menu

        pygame.display.flip()

# Create text for Credit button
credit_font = pygame.font.Font(font_path, 40)
credit_text = credit_font.render('Credit', True, black)
credit_outline = credit_font.render('Credit', True, white)
credit_rect = credit_text.get_rect(topleft=(15, height - 80))  # Position at bottom left

# Function to display Credit information
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
music_path = os.path.join(Music_folder, 'Melancholic Walk.mp3')  # Replace with correct path
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
        screen.fill(red)
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
