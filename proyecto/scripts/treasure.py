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
        while True:
            x = random.randint(0, len(self.game_map.grid[0]) - 1)
            y = random.randint(0, len(self.game_map.grid) - 1)

            # Celda libre
            if self.game_map.grid[y][x] == 0:
                # No encima del jugador
                if x != self.player.col or y != self.player.row:
                    return (x, y)

    def draw(self, screen):
        rect = pygame.Rect(
            self.position[0] * TILE_SIZE,
            self.position[1] * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )
        pygame.draw.rect(screen, (255, 215, 0), rect)

    def check_collision(self):
        treasure_col = self.position[0]
        treasure_row = self.position[1]

        if self.player.col == treasure_col and self.player.row == treasure_row:
            return True
        return False