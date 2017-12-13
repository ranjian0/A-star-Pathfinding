from collections import deque
import pygame as pg

AGENT_SIZE = 35, 35
TRANSPARENT = 0, 0, 0, 0


class Agent:
    def __init__(self, pos):
        self.image = self.make_img()
        self.rect = self.image.get_rect(center=pos)

        self.true_pos = list(self.rect.center)
        self.path = None
        self.speed = 100

    def make_img(self):
        img = pg.Surface(AGENT_SIZE).convert_alpha()
        img.fill(TRANSPARENT)
        rect = img.get_rect()

        pg.draw.ellipse(img, pg.Color('black'), rect.inflate(-1, -1))
        pg.draw.ellipse(img, pg.Color('tomato'), rect.inflate(-10, -10))

        return img

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        # Draw path:
        if self.path:
            for p in self.path:
                pg.draw.circle(surface, pg.Color('red'), p, 5)

    def update(self, dt):

        if self.path:
            current = self.path[0]
            self.move_to(current, dt)

            # Update current if we reached it
            dx = current[0] - self.true_pos[0]
            dy = current[1] - self.true_pos[1]

            if pg.math.Vector2(dx, dy).length() < 1:
                self.path.popleft()

    def set_path(self, path):
        self.path = deque(path)

    def move_to(self, pos, dt):
        # Calculate distance between current pos and target, and direction
        vec = pg.math.Vector2(pos[0] - self.true_pos[0], pos[1] - self.true_pos[1])
        direction = vec.normalize()

        # Progress towards the target
        self.true_pos[0] += direction[0] * self.speed * dt
        self.true_pos[1] += direction[1] * self.speed * dt

        self.rect.center = self.true_pos
