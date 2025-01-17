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

# Initialize font
pygame.font.init()
font = pygame.font.Font(None, 36)  # Default font, size 36

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

    def update(self, wave_y):
        self.brightness += self.twinkle_speed * (random.random() - 0.5)
        self.brightness = max(0.1, min(1.0, self.brightness))  # Clamp brightness

        # Simulate "gravitational" pull toward wave
        wave_effect = 0.01 * (wave_y - self.y)  # Pull towards wave
        self.y += wave_effect  

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
        self.amplitude = self.base_amplitude * (0.5 + 0.5 * math.sin(self.time * 0.1))
        self.frequency += 0.001 * math.sin(self.time * 0.2)  # Slight oscillation on frequency

    def draw(self, surface):
        for x in range(WIDTH):
            y = int(self.y_offset + self.amplitude * math.sin(self.frequency * (x + self.time)))
            pygame.draw.circle(surface, (0, 255, 0), (x, y), 1)

    def increase_frequency(self, amount=0.01):
        self.frequency += amount

    def decrease_frequency(self, amount=0.01):
        self.frequency = max(0, self.frequency - amount)  # Keep frequency non-negative

    def increase_amplitude(self, amount=1):
        self.base_amplitude += amount

    def decrease_amplitude(self, amount=1):
        self.base_amplitude = max(0, self.base_amplitude - amount)  # Keep amplitude non-negative

wave = Wave(300, 0.05, 50)

def draw_nebula(surface, num_clouds):
    for _ in range(num_clouds):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        radius = random.randint(30, 100)
        opacity = random.randint(50, 150)  # Transparency for layers
        color = (255, 255, 255, opacity)  # White color with varying opacity

        nebula_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(nebula_surface, color, (radius, radius), radius)
        surface.blit(nebula_surface, (x - radius, y - radius))

def draw_labels():
    frequency_text = font.render(f"Frequency: {wave.frequency:.2f}", True, (255, 255, 255))
    amplitude_text = font.render(f"Amplitude: {wave.amplitude:.2f}", True, (255, 255, 255))
    screen.blit(frequency_text, (10, 10))
    screen.blit(amplitude_text, (10, 40))

def update():
    wave.update()  # Update the wave
    for star in stars:
        wave_y = int(wave.y_offset + wave.amplitude * math.sin(wave.frequency * (star.x + wave.time)))
        star.update(wave_y)  # Update each star (consider wave influence)

def main():
    # pygame.mixer.music.load('background_music.ogg')  # Replace with your music file path
    # pygame.mixer.music.play(-1)  # Loop indefinitely

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    wave.increase_frequency(0.01)  # Change frequency up
                elif event.key == pygame.K_DOWN:
                    wave.decrease_frequency(0.01)  # Change frequency down
                elif event.key == pygame.K_LEFT:
                    wave.decrease_amplitude(1)  # Change amplitude down
                elif event.key == pygame.K_RIGHT:
                    wave.increase_amplitude(1)  # Change amplitude up

        update()  # Update the wave and star twinkling

        # Draw everything
        screen.fill((0, 0, 0))  # Fill the screen with black
        draw_nebula(screen, 10)  # Draw nebula clouds
        draw_grid()  # Draw grid
        wave.draw(screen)  # Draw wave
        draw_labels()  # Draw frequency and amplitude labels
        
        # Draw all the stars
        for star in stars:
            star.draw(screen)

        pygame.display.flip()  # Render the changes
        clock.tick(60)  # Control the frame rate

if __name__ == "__main__":
    main()