import pygame
import random

class BlackHoleEvaporation:
    def __init__(self, app):
        self.app = app
        self.particles = []
        self.num_particles = 10

def update(self):
    # Simulate evaporation by generating particles
    for _ in range(self.num_particles):
        angle = random.uniform(0, 2 * 3.14159)
        radius = random.uniform(50, 100)  # Near event horizon
        x = self.app.screen_width // 2 + radius * pygame.math.cos(angle)
        y = self.app.screen_height // 2 + radius * pygame.math.sin(angle)

        # Simulate escape particle moving outward
        escape_direction = (random.uniform(2, 5), random.uniform(2, 5))
        self.particles.append({"pos": [x, y], "vel": escape_direction})

    # Update positions of emitted particles
    for particle in self.particles:
        particle["pos"][0] += particle["vel"][0]
        particle["pos"][1] += particle["vel"][1]

        # Simple bounds checking to remove particles that move off the screen
        if (particle["pos"][0] < 0 or particle["pos"][0] > self.app.screen_width or
            particle["pos"][1] < 0 or particle["pos"][1] > self.app.screen_height):
            self.particles.remove(particle)

def render(self):
    for particle in self.particles:
        pygame.draw.circle(self.app.screen, (255, 0, 255), (int(particle["pos"][0]), int(particle["pos"][1])), 3)
