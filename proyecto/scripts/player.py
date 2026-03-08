# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
from scripts.settings import *


class Player:
    def __init__(self, game_map):

        self.animations = {
            "down": [],
            "up": [],
            "left": [],
            "right": []
        }

        for i in range(1, 7):
            img = pygame.image.load(f"assets/sprites/player/down{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(int(TILE_SIZE*1.2), int(TILE_SIZE*1.2)))
            self.animations["down"].append(img)

        for i in range(1, 7):
            img = pygame.image.load(f"assets/sprites/player/up{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(int(TILE_SIZE*1.2), int(TILE_SIZE*1.2)))
            self.animations["up"].append(img)

        for i in range(1, 7):
            img = pygame.image.load(f"assets/sprites/player/left{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(int(TILE_SIZE*1.2), int(TILE_SIZE*1.2)))
            self.animations["left"].append(img)

        for i in range(1, 7):
            img = pygame.image.load(f"assets/sprites/player/right{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(int(TILE_SIZE*1.2), int(TILE_SIZE*1.2)))
            self.animations["right"].append(img)
        
        self.direction = "down"
        self.frame_index = 0

        self.game_map = game_map
        self.move_delay = 150  # milisegundos entre movimientos
        self.last_move_time = 0
        
        # Posición inicial (celda)
        self.row = 1
        self.col = 1

        self.start_row = self.row
        self.start_col = self.col
        self.has_treasure = False

        self.color = COLOR_PLAYER
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Evitar movimiento demasiado rápido
        if current_time - self.last_move_time < self.move_delay:
            return

        new_row = self.row
        new_col = self.col

        if keys[pygame.K_w]:
            new_row -= 1
            self.direction = "up"

        elif keys[pygame.K_s]:
            new_row += 1
            self.direction = "down"

        elif keys[pygame.K_a]:
            new_col -= 1
            self.direction = "left"

        elif keys[pygame.K_d]:
            new_col += 1
            self.direction = "right"

        else:
            return  # No se presionó nada

        # Verificar colisión
        if self.game_map.grid[new_row][new_col] == 0:
            self.row = new_row
            self.col = new_col

            self.last_move_time = current_time

            self.frame_index += 1

            if self.frame_index >= len(self.animations[self.direction]):
                self.frame_index = 0

    def draw(self, screen, offset_x, offset_y):
        rect = pygame.Rect(
            self.col * TILE_SIZE + offset_x,
            self.row * TILE_SIZE + offset_y,
            TILE_SIZE,
            TILE_SIZE
        )
        
        sprite = self.animations[self.direction][self.frame_index]

        screen.blit(sprite, (rect.x, rect.y))
