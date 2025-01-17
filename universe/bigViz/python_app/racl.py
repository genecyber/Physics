import pygame
import math
import requests
from universe.bigViz.python_app.spacetime_curvature import SpacetimeCurvature
from accretion_disk import AccretionDisk
from particle_creation import ParticleCreation
from black_hole_evaporation import BlackHoleEvaporation

class RACLApp:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.spacetime_curvature = SpacetimeCurvature(self)
        self.accretion_disk = AccretionDisk(self)
        self.particle_creation = ParticleCreation(self)
        self.black_hole_evaporation = BlackHoleEvaporation(self)
        self.menu_font = pygame.font.SysFont("Arial", 24)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.spacetime_curvature.BLACK_HOLE_MASS += 100
                requests.post('http://localhost:3010/update-mass', json={'mass': self.spacetime_curvature.BLACK_HOLE_MASS})
            elif event.key == pygame.K_DOWN:
                self.spacetime_curvature.BLACK_HOLE_MASS -= 100
                requests.post('http://localhost:3010/update-mass', json={'mass': self.spacetime_curvature.BLACK_HOLE_MASS})
            elif event.key == pygame.K_LEFT:
                self.spacetime_curvature.BLACK_HOLE_SPIN -= 0.1
                requests.post('http://localhost:3010/update-spin', json={'spin': self.spacetime_curvature.BLACK_HOLE_SPIN})
            elif event.key == pygame.K_RIGHT:
                self.spacetime_curvature.BLACK_HOLE_SPIN += 0.1
                requests.post('http://localhost:3010/update-spin', json={'spin': self.spacetime_curvature.BLACK_HOLE_SPIN})

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_events(event)
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def update(self):
        self.accretion_disk.update()
        self.particle_creation.update()
        self.black_hole_evaporation.update()

    def render(self):
        self.spacetime_curvature.render()
        self.accretion_disk.render()
        self.particle_creation.render()  
        self.black_hole_evaporation.render()  # Render black hole evaporation
        self.render_menu()
        pygame.display.flip()

    def render_menu(self):
        text_surface = self.menu_font.render(f"Black Hole Mass: {self.spacetime_curvature.BLACK_HOLE_MASS}", True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))
        text_surface = self.menu_font.render(f"Black Hole Spin: {self.spacetime_curvature.BLACK_HOLE_SPIN}", True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 40))

if __name__ == "__main__":
    app = RACLApp()
    app.run()