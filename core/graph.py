import pygame as pg
from itertools import permutations as perm

from .agent import Agent
from .astar import a_star_search, reconstruct_path


class Node:
    SIZE = 50
    BORDER = 5

    def __init__(self, pos, walkable):
        self.position = pos
        self.size = self.SIZE
        self.walkable = walkable

        self.rect = pg.Rect(pos[0], pos[1], self.size, self.size)

    def set_size(self, val):
        self.size = val
        px, py = self.position
        self.rect = pg.Rect(px, py, self.size, self.size)

    def draw(self, surface):
        col = pg.Color('white') if self.walkable else pg.Color('black')
        px, py = self.position
        sx, sy = (self.size,) * 2
        pg.draw.rect(surface, col, self.rect.inflate(-self.BORDER, -self.BORDER))

    def get_neighbours(self):
        refx, refy = self.rect.center
        four_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        eight_dirs = list(perm([0, 1, -1], 2)) + [(1, 1), (-1, -1)]

        neighs = []
        for d in four_dirs:
            dx, dy = d
            px, py = refx + (dx * Node.SIZE), refy + (dy * Node.SIZE)
            neighs.append((px, py))
        return neighs


class Graph:
    def __init__(self, size, pos):
        self.size = size
        self.position = pos
        self.nodes = self.make()

        self.agents = []
        self.target = None

    def make(self):
        cx, cy = [gs // ns for ns, gs in zip((Node.SIZE, Node.SIZE), self.size)]
        offx, offy = self.position

        res = []
        for x in range(cx + 2):
            for y in range(cy - 2):
                pos = offx + (x * Node.SIZE), offy + (y * Node.SIZE)
                n = Node(pos, True)
                res.append(n)
        return res

    def draw(self, surface):

        # Draw nodes
        for node in self.nodes:
            node.draw(surface)

        # Draw agents
        if self.agents:
            for ag in self.agents:
                ag.draw(surface)

        # Draw Target
        if self.target:
            pg.draw.circle(surface, pg.Color('black'), self.target, 20)
            pg.draw.circle(surface, pg.Color('blue'), self.target, 15)

    def event(self, ev):

        if ev.type == pg.MOUSEBUTTONDOWN:
            if ev.button == 1:
                self.add_agent(ev.pos)
            if ev.button == 2:
                self.set_node_walkable(ev.pos)
            if ev.button == 3:
                self.set_agent_target(ev.pos)

        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_SPACE:
                self.navigate()
            if ev.key == pg.K_r:
                self.reset()

    def update(self, dt):
        for ag in self.agents:
            ag.update(dt)

    def set_node_walkable(self, pos):
        for node in self.nodes:
            if node.rect.collidepoint(pos):
                node.walkable = not node.walkable

    def set_agent_target(self, pos):
        for node in self.nodes:
            if node.rect.collidepoint(pos):
                if node.walkable:
                    self.target = node.rect.center

    def add_agent(self, pos):
        walkable = [n.position for n in self.nodes if n.walkable]
        try:
            node = [n for n in self.nodes if n.rect.collidepoint(pos)][-1]
        except IndexError:
            return

        if node.position in walkable:
            self.agents.append(Agent(node.rect.center))

    def navigate(self):
        # return if there is no target
        if not self.target:
            return

        # calculate paths for all agents
        for ag in self.agents:
            start = ag.rect.center
            goal = self.target

            cf, cost = a_star_search(self, start, goal)
            try:
                path = reconstruct_path(cf, start, goal)
            except KeyError:
                return

            # Remove start position
            ag.set_path(path[2:])

    def reset(self):
        self.agents.clear()
        self.target = None

        for n in self.nodes:
            if not n.walkable:
                n.walkable = True

    # These two last methods must be implemented for a_star to work
    def neighbors(self, pos):
        # determine the node at pos
        node = [n for n in self.nodes if n.rect.collidepoint(pos)][-1]

        # Get neighbouring nodes
        positions = node.get_neighbours()

        # Filter un-walkable positions
        res = []
        for p in positions:
            for n in self.nodes:
                if n.rect.collidepoint(p):
                    if n.walkable:
                        res.append(p)
        return res

    def cost(self, p1, p2):
        return 10
