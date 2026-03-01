# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
from scripts.settings import TILE_SIZE
from scripts.astar import astar


class Guardian:

    def __init__(self, game_map, player, patrol_points):
        self.game_map = game_map
        self.player = player
        self.patrol_points = patrol_points
        self.current_patrol_index = 0
        self.chasing = False
        self.last_seen_time = 0
        self.memory_duration = 1500  # milisegundos

        self.normal_move_delay = 175
        self.aggressive_move_delay = 160

        self.last_move_time = 0

        self.row, self.col = patrol_points[0]

        self.normal_vision_range = 10
        self.aggressive_vision_range = 15

        self.color = (255, 0, 0)

    def detect_player(self):

        # MODO AGRESIVO (cuando tiene el tesoro)
        if self.player.has_treasure:
            distance = abs(self.player.row - self.row) + abs(self.player.col - self.col)
            return distance <= self.aggressive_vision_range

        # MODO NORMAL (visión por distancia con chequeo simple de obstáculos)

        distance = abs(self.player.row - self.row) + abs(self.player.col - self.col)

        if distance <= self.normal_vision_range:

            # Chequeo simple: intentar trazar línea aproximada
            dr = self.player.row - self.row
            dc = self.player.col - self.col

            steps = max(abs(dr), abs(dc))

            for i in range(1, steps):
                r = self.row + (dr * i) // steps
                c = self.col + (dc * i) // steps

                if self.game_map.grid[r][c] != 0:
                    return False

            return True
        return False

    def update(self):

        current_time = pygame.time.get_ticks()

        if self.player.has_treasure:
            move_delay = self.aggressive_move_delay
        else:
            move_delay = self.normal_move_delay

        if current_time - self.last_move_time < move_delay:
            return

        # --- DECISIÓN DE OBJETIVO ---

        if self.detect_player():
            target = (self.player.row, self.player.col)

        else:
            # Si estaba persiguiendo y te pierde, forzar cambio de patrulla
            if (self.row, self.col) == self.patrol_points[self.current_patrol_index]:
                self.current_patrol_index = (
                    self.current_patrol_index + 1
                ) % len(self.patrol_points)

            target = self.patrol_points[self.current_patrol_index]

            # Si llegó al punto, cambiar al siguiente
            if (self.row, self.col) == target:
                self.current_patrol_index = (
                    self.current_patrol_index + 1
                ) % len(self.patrol_points)
                target = self.patrol_points[self.current_patrol_index]

        self.move_to(target)

        self.last_move_time = current_time

    def move_to(self, target):

        path = astar(
            self.game_map.grid,
            (self.row, self.col),
            target
        )

        if not path:
            # Cambiar al siguiente punto de patrulla si no hay camino
            self.current_patrol_index = (
                self.current_patrol_index + 1
            ) % len(self.patrol_points)
            return

        next_step = path[0]

        if self.game_map.grid[next_step[0]][next_step[1]] == 0:
            self.row, self.col = next_step

    def draw(self, screen):

        rect = pygame.Rect(
            self.col * TILE_SIZE,
            self.row * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

        # Cambiar color en modo agresivo
        if self.player.has_treasure:
            pygame.draw.rect(screen, (255, 100, 100), rect)
        else:
            pygame.draw.rect(screen, self.color, rect)