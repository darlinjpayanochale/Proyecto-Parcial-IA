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
            col = random.randint(1, cols - 2)

            if (
                self.game_map.grid[row][col] == 0 and
                (row, col) != (self.player.row, self.player.col)
            ):
                return (row, col)

    def draw(self, screen, offset_x, offset_y):

        row, col = self.position

        rect = pygame.Rect(
            col * TILE_SIZE + offset_x,
            row * TILE_SIZE + offset_y,
            TILE_SIZE,
            TILE_SIZE
        )

        if not self.player.has_treasure:
            pygame.draw.rect(screen, (255, 215, 0), rect)

    def check_collision(self):

        row, col = self.position

        return (
            self.player.row == row and
            self.player.col == col
        )