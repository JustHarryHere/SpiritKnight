import pygame

class HealthBar:
    def __init__(self, max_hp, current_hp, position, scale_factor=0.5):
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.position = position

        # Load images for the health bar
        self.bar_image = pygame.image.load('D:/SpiritKnight/Sprites/HP2.png').convert_alpha()
        self.bar_image = pygame.transform.scale(
            self.bar_image, 
            (int(self.bar_image.get_width() * scale_factor), int(self.bar_image.get_height() * scale_factor))
        )
        self.bar_rect = self.bar_image.get_rect(topleft=position)

        self.overlay_image = pygame.image.load('D:/SpiritKnight/Sprites/HP1.png').convert_alpha()
        self.overlay_image = pygame.transform.scale(
            self.overlay_image, 
            (int(self.overlay_image.get_width() * scale_factor), int(self.overlay_image.get_height() * scale_factor))
        )

        # Font for displaying HP text
        self.font = pygame.font.Font('D:/SpiritKnight/Font/properhitboxglobal.ttf', 18)

    def update(self, new_hp):
        """Update the current HP value."""
        self.current_hp = max(0, min(self.max_hp, new_hp))  # Clamp value between 0 and max_hp

    def draw(self, screen):
        """Draw the health bar and the text."""
        # Draw the background health bar
        screen.blit(self.bar_image, self.bar_rect)

        # Calculate the width of the overlay based on current HP
        overlay_width = int((self.current_hp / self.max_hp) * self.bar_image.get_width())
        overlay_surface = pygame.Surface((overlay_width, self.overlay_image.get_height()), pygame.SRCALPHA)
        overlay_surface.blit(self.overlay_image, (0, 0), (0, 0, overlay_width, self.overlay_image.get_height()))
        screen.blit(overlay_surface, self.bar_rect.topleft)

        # Draw the HP text
        hp_text_black = self.font.render(f"{self.current_hp}/{self.max_hp}", True, (0, 0, 0))
        hp_text_white = self.font.render(f"{self.current_hp}/{self.max_hp}", True, (255, 255, 255))
        hp_text_rect = hp_text_black.get_rect(center=(240,40))

        # Add shadow effect for the text
        screen.blit(hp_text_black, hp_text_rect.move(2, 2))
        screen.blit(hp_text_white, hp_text_rect)
