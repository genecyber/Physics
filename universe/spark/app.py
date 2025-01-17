import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import networkx as nx
import random

class Particle:
    def __init__(self, x, y, theory):
        self.x = x
        self.y = y
        self.theory = theory
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-1, 1)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

class UnifiedTheoryVisualizer:
    def __init__(self):
        self.theories = {}
        self.G = nx.Graph()
        self.particles = []
        self.time = 0
        self.paused = False
        self.pos = None

    def add_theory(self, theory, interactions=None):
        self.theories[theory] = interactions
        self.G.add_node(theory)
        if interactions:
            for interaction in interactions:
                self.G.add_edge(theory, interaction)

    def add_particle(self, theory, x, y):
        self.particles.append(Particle(x, y, theory))

    def simulate(self):
        self.time += 1
        for particle in self.particles:
            particle.update()
            # Apply forces between particles
            for other_particle in self.particles:
                if particle!= other_particle:
                    dx = particle.x - other_particle.x
                    dy = particle.y - other_particle.y
                    distance = np.sqrt(dx**2 + dy**2)
                    force = 1 / distance**2  # simple attraction force
                    particle.velocity_x += force * dx
                    particle.velocity_y += force * dy

    def animate(self, frame):
        self.simulate()
        self.ax.clear()
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_size=500, node_color='lightblue')
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=10)
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, width=2, edge_color='gray')
        particle_x = [particle.x for particle in self.particles]
        particle_y = [particle.y for particle in self.particles]
        self.ax.scatter(particle_x, particle_y, c='red', alpha=0.5)
        self.ax.set_title(f"Time: {self.time}")

    def visualize(self):
        self.pos = nx.spring_layout(self.G)
        self.fig, self.ax = plt.subplots()
        ani = animation.FuncAnimation(self.fig, self.animate, frames=200, interval=50)
        plt.show()

# Create an instance of the visualizer
visualizer = UnifiedTheoryVisualizer()

# Add theories with their interactions
visualizer.add_theory("Gravity")
visualizer.add_theory("Electromagnetism", ["Gravity"])
visualizer.add_theory("Strong Nuclear Force", ["Electromagnetism"])
visualizer.add_theory("Weak Nuclear Force", ["Strong Nuclear Force", "Electromagnetism"])

# Add particles
visualizer.add_particle("Gravity", 0, 0)
visualizer.add_particle("Electromagnetism", 5, 0)
visualizer.add_particle("Strong Nuclear Force", 10, 0)

# Visualize the interactions and particles
visualizer.visualize()