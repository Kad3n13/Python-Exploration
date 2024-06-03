import pygame
import random
import time
import colorsys

# Initialize Pygame
pygame.init()

# Set screen dimensions
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Enhanced Starfield Simulation")

# Define the Star class
class Star:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.uniform(-width / 2, width / 2)
        self.y = random.uniform(-height / 2, height / 2)
        self.z = random.uniform(1, width)
        self.pz = self.z
        self.color = self.random_color()

    def random_color(self):
        # Generate a random color using HSV
        h = random.random()
        s = random.uniform(0.5, 1)
        v = random.uniform(0.5, 1)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))

    def update(self, speed):
        self.pz = self.z
        self.z -= speed
        if self.z < 1:
            self.reset()

    def show(self):
        sx = int(self.x / self.z * width / 2 + width / 2)
        sy = int(self.y / self.z * height / 2 + height / 2)
        px = int(self.x / self.pz * width / 2 + width / 2)
        py = int(self.y / self.pz * height / 2 + height / 2)
        r = int((1 - self.z / width) * 5)
        
        # Draw star
        pygame.draw.circle(screen, self.color, (sx, sy), r)
        
        # Draw trail
        if px != sx or py != sy:
            pygame.draw.line(screen, self.color, (px, py), (sx, sy))

# Create stars
stars = [Star() for _ in range(800)]
last_color_change = time.time()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Map speed to mouse position
    mouse_x, _ = pygame.mouse.get_pos()
    speed = pygame.mouse.get_pos()[0] / width * 50

    # Periodic color change every .5 seconds
    current_time = time.time()
    if current_time - last_color_change > .5:
        for star in stars:
            star.color = star.random_color()
        last_color_change = current_time

    # Update and draw stars
    screen.fill((0, 0, 0))
    for star in stars:
        star.update(speed)
        star.show()

    pygame.display.flip()
    pygame.time.delay(16)

pygame.quit()
