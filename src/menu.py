import pygame
import sys
import os
from pygame.math import Vector2 as Vec2
from importlib import reload
from components.text_box import TextBox
from core.color import Color

CLICKED = False


class Menu:
    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.windowname = pygame.display.set_caption("Menu")

    def run_menu(self):
        pygame.init()

        clock = pygame.time.Clock()
        running = True
        mouse = (0, 0)

        text = pygame.font.Font("res/uwu-font.ttf", 24)
        text_surface = text.render("Game mode:", True, Color.WHITE)

        easy_surface = text.render("easy", True, Color.GREEN)
        easy_surfaceclicked = text.render("easy", True, Color.WHITE)
        normal_surface = text.render("normal", True, Color.BLUE)
        normal_surfaceclicked = text.render("normal", True, Color.WHITE)
        hard_surface = text.render("hard", True, Color.RED)
        hard_surfaceclicked = text.render("hard", True, Color.WHITE)

        text_rect = text_surface.get_rect()
        easy_rect = easy_surface.get_rect()
        easy_rectclicked = easy_surfaceclicked.get_rect()
        normal_rect = normal_surface.get_rect()
        normal_rectclicked = normal_surfaceclicked.get_rect()
        hard_rect = hard_surface.get_rect()
        hard_rectclicked = hard_surfaceclicked.get_rect()

        x_val = 250
        y_val = 150
        text_rect.center = (x_val, y_val)
        easy_rect.center = (x_val, y_val + 50)
        easy_rectclicked.center = (x_val, y_val + 50)
        normal_rect.center = (x_val, y_val + 100)
        normal_rectclicked.center = (x_val, y_val + 100)
        hard_rect.center = (x_val, y_val + 150)
        hard_rectclicked.center = (x_val, y_val + 150)

        while running:
            self.screen.fill(Color.BLACK)
            list_of_modes = [
                (easy_rect, "easy"),
                (normal_rect, "normal"),
                (hard_rect, "hard"),
            ]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pressed = pygame.mouse.get_pos()
                    for mode, name in list_of_modes:
                        if mode.collidepoint(mouse_pressed):
                            os.environ["NAP_GAME_MODE_SELECT_69"] = name
                            global CLICKED
                            if not CLICKED:
                                import entry_point

                                CLICKED = True
                                return
                            else:
                                reload(sys.modules["entry_point"])
                                return

            self.screen.blit(text_surface, text_rect)
            if easy_rect.collidepoint(mouse[0], mouse[1]):
                # os.environ['NAP_GAME_MODE_SELECT_69'] = 'easy'
                self.screen.blit(easy_surface, easy_rect)
            else:
                self.screen.blit(easy_surfaceclicked, easy_rectclicked)

            if normal_rect.collidepoint(mouse[0], mouse[1]):
                self.screen.blit(normal_surface, normal_rect)
            else:
                self.screen.blit(normal_surfaceclicked, normal_rectclicked)

            if hard_rect.collidepoint(mouse[0], mouse[1]):
                # os.environ['NAP_GAME_MODE_SELECT_69'] = 'hard'
                self.screen.blit(hard_surface, hard_rect)
            else:
                self.screen.blit(hard_surfaceclicked, hard_rectclicked)

            pygame.display.update()


while True:
    pygame.init()
    screensize = pygame.display.set_mode((500, 500))
    menu = Menu()
    menu.run_menu()
