import pygame

class Sound:
    def __init__(self, filename: str, loop = False, volume=1.0):
        self.sound = pygame.mixer.Sound(filename)
        self.sound.set_volume(volume)
        self.loop = loop
        self.is_playing = False

    def play(self):
        if not self.is_playing:
            self.sound.play(loops= -1 if self.loop else 0)

            if self.loop:
                self.is_playing = True

    def stop(self):
        self.sound.stop()
        self.is_playing = False

