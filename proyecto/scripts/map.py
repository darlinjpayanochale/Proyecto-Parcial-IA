# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import random
import pygame
from scripts.settings import *


class GameMap:
    def __init__(self):
        self.grid = self.generate_map()

    def generate_map(self):
        """
        Genera un mapa con bordes cerrados y obstáculos aleatorios.
        0 = espacio libre
        1 = pared
        """
        grid = []

        for row in range(MAP_ROWS):
            current_row = []
            for col in range(MAP_COLS):

                # Bordes siempre paredes
                if row == 0 or col == 0 or row == MAP_ROWS - 1 or col == MAP_COLS - 1:
                    current_row.append(1)
                else:
                    # Obstáculos aleatorios
                    if random.random() < 0.2:
                        current_row.append(1)
                    else:
                        current_row.append(0)

            grid.append(current_row)

        return grid

    def draw(self, screen):
        """
        Dibuja el mapa en pantalla.
        """
        for row in range(MAP_ROWS):
            for col in range(MAP_COLS):
                rect = pygame.Rect(
                    col * TILE_SIZE,
                    row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

                if self.grid[row][col] == 1:
                    pygame.draw.rect(screen, COLOR_WALL, rect)
                else:
                    pygame.draw.rect(screen, COLOR_FLOOR, rect)