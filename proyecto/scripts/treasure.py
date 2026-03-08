# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
import random
import math
from scripts.settings import TILE_SIZE


class Treasure:
    def __init__(self, game_map, player):
        self.game_map = game_map
        self.player = player
        self.position = self.generate_position()

        # Cargar sprite del tesoro
        self.image = pygame.image.load("assets/sprites/treasure.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

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

        x = col * TILE_SIZE + offset_x
        y = row * TILE_SIZE + offset_y

        # Solo dibujar si el jugador aún no lo tiene
        if not self.player.has_treasure:

            # brillo pulsante
            t = pygame.time.get_ticks() * 0.005
            radius = int(TILE_SIZE * 0.6 + math.sin(t) * 6)

            glow_surface = pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 2), pygame.SRCALPHA)

            pygame.draw.circle(
                glow_surface,
                (255, 215, 0, 80),  # dorado transparente
                (TILE_SIZE, TILE_SIZE),
                radius
            )

            screen.blit(glow_surface, (x - TILE_SIZE//2, y - TILE_SIZE//2))

            # sprite del tesoro
            screen.blit(self.image, (x, y))

    def check_collision(self):

        row, col = self.position

        return (
            self.player.row == row and
            self.player.col == col
        )