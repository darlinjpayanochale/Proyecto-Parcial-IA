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
                if (
                    row == 0 or
                    col == 0 or
                    row == MAP_ROWS - 1 or
                    col == MAP_COLS - 1
                ):
                    current_row.append(1)

                else:
                    # Obstáculos aleatorios
                    if random.random() < 0.1:
                        current_row.append(1)
                    else:
                        current_row.append(0)

            grid.append(current_row)

        # ZONA SEGURA DEL JUGADOR
        safe_zone = [(1,1), (1,2), (2,1), (2,2)]

        for r, c in safe_zone:
            grid[r][c] = 0

        # salida hacia el mapa
        for r in range(1, 5):
            grid[r][1] = 0

        for c in range(1, 5):
            grid[1][c] = 0

        # PUNTOS DE PATRULLA
        patrol_points = [
            (4,8), (4,10), (6,9),
            (8,8), (8,12), (12,10)
        ]

        for r, c in patrol_points:

            if r < MAP_ROWS and c < MAP_COLS:

                # asegurar que el punto esté libre
                grid[r][c] = 0

                # limpiar alrededor para evitar bloqueos
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:

                        rr = r + dr
                        cc = c + dc

                        if (
                            0 <= rr < MAP_ROWS and
                            0 <= cc < MAP_COLS
                        ):
                            grid[rr][cc] = 0

        return grid


    def draw(self, screen, offset_x, offset_y):
        """
        Dibuja el mapa en pantalla.
        """

        for row in range(MAP_ROWS):
            for col in range(MAP_COLS):

                rect = pygame.Rect(
                    offset_x + col * TILE_SIZE,
                    offset_y + row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

                if self.grid[row][col] == 1:
                    pygame.draw.rect(screen, COLOR_WALL, rect)
                else:
                    pygame.draw.rect(screen, COLOR_FLOOR, rect)