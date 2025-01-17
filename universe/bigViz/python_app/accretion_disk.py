import pygame
import random

class AccretionDisk:
    def __init__(self, app):
        self.app = app
        self.num_particles = 100
        self.particles = []

    # Initialize particle positions and velocities
    for _ in range(self.num_particles):
        angle = random.uniform(0, 2 * 3.14159)
        radius = random.uniform(100, 300)
        x = self.app.screen_width // 2 + radius * pygame.math.cos(angle)
        y = self.app.screen_height // 2 + radius * pygame.math.sin(angle)
        self.particles.append({"pos": [x, y], "vel": [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]})

def update(self):
    for particle in self.particles:
        x, y = particle["pos"]
        # Update position based on velocity
        particle["pos"][0] += particle["vel"][0]
        particle["pos"][1] += particle["vel"][1]

        # Simple bounds checking to keep particles inside the screen
        if x < 0 or x > self.app.screen_width or y < 0 or y > self.app.screen_height:
            particle["pos"][0] -= particle["vel"][0]
            particle["pos"][1] -= particle["vel"][1]

def render(self):
    for particle in self.particles:
        pygame.draw.circle(self.app.screen, (0, 0, 255), (int(particle["pos"][0]), int(particle["pos"][1])), 2)