import pygame
import random

class ParticleCreation:
    def __init__(self, app):
        self.app = app
        self.particles = []
        self.num_particles = 10

def update(self):
    # Simulate particle-antiparticle pair creation
    for _ in range(self.num_particles):
        angle = random.uniform(0, 2 * 3.14159)
        radius = random.uniform(0, 50)  # Create near the event horizon
        x = self.app.screen_width // 2 + radius * pygame.math.cos(angle)
        y = self.app.screen_height // 2 + radius * pygame.math.sin(angle)

        # Particle can escape to the right, simulating Hawking radiation
        escape_direction = random.choice([(5, 0), (-5, 0)])  # Right or left escape
        self.particles.append({"pos": [x, y], "vel": escape_direction})

    # Update positions of particles
    for particle in self.particles:
        particle["pos"][0] += particle["vel"][0]
        particle["pos"][1] += particle["vel"][1]

        # Simple bounds checking
        if (particle["pos"][0] < 0 or particle["pos"][0] > self.app.screen_width or
            particle["pos"][1] < 0 or particle["pos"][1] > self.app.screen_height):
            self.particles.remove(particle)

def render(self):
    for particle in self.particles:
        pygame.draw.circle(self.app.screen, (255, 215, 0), (int(particle["pos"][0]), int(particle["pos"][1])), 3)