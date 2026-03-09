# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import random
import pygame
from scripts.settings import *

class GameMap:
    def __init__(self):
        self.grid = self.generate_map()

        # Cargar sprites
        self.floor_img = pygame.image.load("assets/sprites/floor.png").convert()
        self.wall_img = pygame.image.load("assets/sprites/wall.png").convert()

        # Escalar al tamaño de las celdas
        self.floor_sprite = pygame.transform.scale(self.floor_img, (TILE_SIZE, TILE_SIZE))
        self.wall_sprite = pygame.transform.scale(self.wall_img, (TILE_SIZE, TILE_SIZE))

        # Crear superficie del mapa completo
        self.map_surface = pygame.Surface((MAP_COLS * TILE_SIZE, MAP_ROWS * TILE_SIZE))

        # Dibujar el mapa una sola vez en esa superficie
        for row in range(MAP_ROWS):
            for col in range(MAP_COLS):

                x = col * TILE_SIZE
                y = row * TILE_SIZE

                if self.grid[row][col] == 1:
                    self.map_surface.blit(self.wall_sprite, (x, y))
                else:
                    self.map_surface.blit(self.floor_sprite, (x, y))

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
                    if random.random() < 0.10:
                        current_row.append(1)
                    else:
                        current_row.append(0)

            grid.append(current_row)

        #Zona segura del jugador
        safe_zone = [(1,1), (1,2), (2,1), (2,2)]
        for r, c in safe_zone:
            grid[r][c] = 0

        # Salida garantizada hacia el mapa
        for r in range(1, 5):
            grid[r][1] = 0
        for c in range(1, 5):
            grid[1][c] = 0

        #Puntos de patrulla
        patrol_points = [
            (4,8), (4,10), (6,9),
            (8,8), (8,12), (12,10)
        ]
        for r, c in patrol_points:
            if r < MAP_ROWS and c < MAP_COLS:
                grid[r][c] = 0
                # Limpiar alrededor para evitar bloqueos
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        
                        rr = r + dr
                        cc = c + dc
                        if 0 <= rr < MAP_ROWS and 0 <= cc < MAP_COLS:
                            grid[rr][cc] = 0

        return grid
    
    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.map_surface, (offset_x, offset_y))