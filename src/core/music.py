import pygame

class Sound:
    def __init__(self, filename: str):
        self.sound = pygame.mixer.Sound(filename)

    def play(self, loop=False):
        self.sound.play(loops= -1 if loop else 0)
