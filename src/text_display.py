import pygame
from pygame.math import Vector2 as Vec2
from colors import COLOR

class TextDisplay:
    def __init__(self, text, fontcolor, fontsize) -> None:
        self.texts = text.split('\n')
        self.dontcolor = fontcolor
        self.fontsize = fontsize
        self.font = pygame.font.Font('res/uwufont.ttf', fontsize)
        self.imgs = []
        max_width = -1
        for text in self.texts:
            self.imgs.append(self.font.render(text, True, fontcolor))
            max_width = max(max_width, self.imgs[-1].get_width())
        textsurf = pygame.Surface((max_width, self.fontsize * len(self.imgs)))
        for i, img in enumerate(self.imgs):
            textsurf.blit(img, (0, i*fontsize))
        self.img = textsurf
        # self.img = self.font.render(self.text, True, fontcolor)
        # self.rect = self.img.get_rect()
        # self.drawrect()
    def drawrect(self):
        rect = self.img.get_rect()
        
        # rect = rect.inflate(100,100)

        surface = pygame.Surface((rect.width, rect.height))
        pygame.draw.rect(surface, COLOR.WHITE, rect, 1)
        surface = pygame.transform.scale_by(surface, 2)
        surface.blit(self.img, Vec2(surface.get_width() - self.img.get_width(), surface.get_height() - self.img.get_height())/2)
        self.img = surface