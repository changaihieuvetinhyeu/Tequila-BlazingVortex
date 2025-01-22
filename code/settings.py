from os.path import join
import pygame
from os import walk
from pytmx.util_pygame import load_pygame

pygame.init()
info = pygame.display.Info()
WINDOW_WIDTH, WINDOW_HEIGHT = info.current_w,info.current_h 
TILE_SIZE = 64
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 0, 255)
HOVER_COLOR = (150, 150, 255)
