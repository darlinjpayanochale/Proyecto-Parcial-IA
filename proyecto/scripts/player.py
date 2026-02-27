# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
from scripts.settings import *


class Player:
    def __init__(self, game_map):
        self.game_map = game_map
        self.move_delay = 150  # milisegundos entre movimientos
        self.last_move_time = 0

        # Posición inicial (celda)
        self.row = 1
        self.col = 1

        self.color = COLOR_PLAYER

        self.rect = pygame.Rect(
            self.col * TILE_SIZE,
            self.row * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

    def handle_input(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Evitar movimiento continuo demasiado rápido
        if current_time - self.last_move_time < self.move_delay:
            return

        new_row = self.row
        new_col = self.col

        if keys[pygame.K_w]:
            new_row -= 1
        elif keys[pygame.K_s]:
            new_row += 1
        elif keys[pygame.K_a]:
            new_col -= 1
        elif keys[pygame.K_d]:
            new_col += 1
        else:
            return  # No se presionó nada

        #Verificar colisión
        if self.game_map.grid[new_row][new_col] == 0:
            self.row = new_row
            self.col = new_col

            #Actualizar rect
            self.rect.x = self.col * TILE_SIZE
            self.rect.y = self.row * TILE_SIZE

            self.last_move_time = current_time

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        