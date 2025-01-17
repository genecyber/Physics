import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Dance of Fields and Forces")

# Set up clock for controlling frame rate
clock = pygame.time.Clock()

class Star:
    def __init__(self, x, y, size=5):
        self.x = x
        self.y = y
        self.base_size = size
        self.twinkle_speed = random.uniform(0.05, 0.2)  # Speed of twinkling
        self.brightness = random.uniform(0.5, 1.0)  # Initial brightness

    def draw(self, surface):
        current_size = int(self.base_size * self.brightness)
        pygame.draw.circle(surface, (255, 255, 0), (self.x, self.y), current_size)

    def update(self):
        # Randomly adjust brightness to create a twinkling effect
        self.brightness += self.twinkle_speed * (random.random() - 0.5)
        self.brightness = max(0.1, min(1.0, self.brightness))  # Clamp brightness

def create_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        stars.append(Star(x, y))
    return stars

num_stars = 100
stars = create_stars(num_stars)

def draw_grid():
    grid_color = (100, 100, 255)
    grid_spacing = 20
    
    for x in range(0, WIDTH, grid_spacing):
        pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, grid_spacing):
        pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y))

class Wave:
    def __init__(self, y_offset, frequency, base_amplitude):
        self.y_offset = y_offset
        self.frequency = frequency
        self.base_amplitude = base_amplitude
        self.amplitude = base_amplitude
        self.time = 0

    def update(self):
        self.time += 0.1
        # Modulate amplitude to create a wave-like effect
        self.amplitude = self.base_amplitude * (0.5 + 0.5 * math.sin(self.time * 0.1))

    def draw(self, surface):
        for x in range(WIDTH):
            y = int(self.y_offset + self.amplitude * math.sin(self.frequency * (x + self.time)))
            pygame.draw.circle(surface, (0, 255, 0), (x, y), 1)

wave = Wave(300, 0.05, 50)

def update():
    wave.update()  # Update the wave
    for star in stars:
        star.update()  # Update each star for twinkling effect

def main():
    # Load and play background music
    # pygame.mixer.music.load('background_music.ogg')  # Replace with your music file path
    # pygame.mixer.music.play(-1)  # Loop indefinitely

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        update()  # Update the wave and star twinkling

        # Fill the screen with black
        screen.fill((0, 0, 0))
        
        # Draw everything
        draw_grid()
        wave.draw(screen)
        
        for star in stars:
            star.draw(screen)

        pygame.display.flip()  # Render the changes
        clock.tick(60)  # Control the frame rate

if __name__ == "__main__":
    main()