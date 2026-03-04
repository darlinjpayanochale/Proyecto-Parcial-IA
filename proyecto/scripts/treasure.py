# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
import random
from scripts.settings import TILE_SIZE


class Treasure:
    def __init__(self, game_map, player):
        self.game_map = game_map
        self.player = player
        self.position = self.generate_position()

    def generate_position(self):
        rows = len(self.game_map.grid)
        cols = len(self.game_map.grid[0])

        # Evitamos la última fila si es muro
        min_row = rows - 4
        max_row = rows - 2

        while True:
            row = random.randint(min_row, max_row)
            col = random.randint(1, cols - 2)  # evitamos bordes laterales

            if (
                self.game_map.grid[row][col] == 0 and
                (row, col) != (self.player.row, self.player.col)
            ):
                return (row, col)

    def draw(self, screen):

        rect = pygame.Rect(
            self.position[1] * TILE_SIZE,  
            self.position[0] * TILE_SIZE,  
            TILE_SIZE,
            TILE_SIZE
        )

        if not self.player.has_treasure:
            pygame.draw.rect(screen, (255, 215, 0), rect)

    def check_collision(self):
        return (
            self.player.row == self.position[0] and
            self.player.col == self.position[1]
        )