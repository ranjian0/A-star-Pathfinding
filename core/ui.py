from .settings import *
import pygame as pg


def draw_header(surface):
    h_size = 100
    font_name = pg.font.match_font('arial')

    # title font
    tfont = pg.font.Font(font_name, 40)
    tsurface = tfont.render(CAPTION, True, pg.Color('white'))
    text_rect = tsurface.get_rect()
    text_rect.midtop = (SIZE[0] / 2, 10)
    surface.blit(tsurface, text_rect)

    pg.draw.line(surface, pg.Color("white"), (0, h_size), (SIZE[0], h_size), 3)


def draw_instructions(surface):
    surf = pg.Surface((250, 250)).convert_alpha()
    surf.fill(BACKGROUND)
    rect = surf.get_rect(center=(400, 300))

    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, 18)
    font.set_bold(True)

    for idx, line in enumerate(INSTRUCTIONS.split('\n')[1:]):
        tsurface = font.render(line, True, pg.Color('yellow'))
        text_rect = tsurface.get_rect()

        fs = font.size(line)[1]
        text_rect.topleft = (10, 10 + (idx * fs))
        surf.blit(tsurface, text_rect)

    surface.blit(surf, rect)
    pg.draw.rect(surface, pg.Color('black'), rect, 5)


def draw_settings(surface):
    surf = pg.Surface((250, 250)).convert_alpha()
    surf.fill((255, 100, 255))
    rect = surf.get_rect(center=(400, 300))

    surface.blit(surf, rect)
    pg.draw.rect(surface, pg.Color('red'), rect, 5)


class Button:
    def __init__(self, text, size, pos, bg_color=pg.Color('red'), font_color=pg.Color('white'), font_size=16,
                 anchor='topleft'):
        self.text = text
        self.size = size
        self.position = pos

        self.background_color = bg_color
        self.font_color = font_color
        self.font_size = font_size
        self.anchor = anchor

        self.surface = self.make()
        if anchor == 'topleft':
            self.rect = self.surface.get_rect(topleft=self.position)
        elif anchor == 'topright':
            self.rect = self.surface.get_rect(topright=self.position)
        self.callback = None

    def make(self):
        surf = pg.Surface(self.size).convert_alpha()
        surf.fill(self.background_color)

        # Create text
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, self.font_size)
        font.set_bold(True)

        tsurface = font.render(self.text, True, self.font_color)
        text_rect = tsurface.get_rect()
        text_rect.center = surf.get_rect().center
        surf.blit(tsurface, text_rect)

        return surf

    def set_text(self, val):
        self.text = val
        self.surface = self.make()
        if self.anchor == 'topleft':
            self.rect = self.surface.get_rect(topleft=self.position)
        elif self.anchor == 'topright':
            self.rect = self.surface.get_rect(topright=self.position)

    def on_click(self, func):
        self.callback = func

    def draw(self, surf):
        surf.blit(self.surface, self.rect)

    def event(self, ev):
        if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos):
                if self.callback:
                    self.callback()
