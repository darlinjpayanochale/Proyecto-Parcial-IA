# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
from scripts.settings import TILE_SIZE

class Guardian:
    """
    Guardian que patrulla, detecta al jugador y lo persigue.
    Estados: patrol, chase, search
    """

    def __init__(self, game_map, player, patrol_points):
        self.game_map = game_map
        self.player = player
        self.patrol_points = patrol_points  # Lista de puntos de patrulla [(row, col), ...]
        self.current_patrol_index = 0

        # Delay de movimiento
        self.move_delay = 300  # milisegundos entre movimientos
        self.last_move_time = 0

        # Posición inicial
        self.row, self.col = patrol_points[0]

        # Estado y visión
        self.state = "patrol"  # patrol, chase, search
        self.vision_range = 3
        self.last_seen_position = None

        # Color visible
        self.color = (255, 0, 0)  # rojo

    def detect_player(self):
        """
        Detecta al jugador si está en la misma fila o columna y dentro del rango de visión
        """
        if self.player.row == self.row and abs(self.player.col - self.col) <= self.vision_range:
            return True
        if self.player.col == self.col and abs(self.player.row - self.row) <= self.vision_range:
            return True
        return False

    def update(self):
        """
        Actualiza el comportamiento según el estado y controla el delay de movimiento
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < self.move_delay:
            return  # aún no se mueve

        # Ejecutar acción según estado
        if self.state == "patrol":
            self.patrol()
            if self.detect_player():
                self.state = "chase"
                self.last_seen_position = (self.player.row, self.player.col)
        elif self.state == "chase":
            self.chase_player()
        elif self.state == "search":
            self.search_last_seen()

        # Actualiza el tiempo después de moverse
        self.last_move_time = current_time

    def patrol(self):
        """
        Movimiento entre los puntos de patrulla
        """
        target_row, target_col = self.patrol_points[self.current_patrol_index]
        if self.row < target_row:
            self.row += 1
        elif self.row > target_row:
            self.row -= 1
        elif self.col < target_col:
            self.col += 1
        elif self.col > target_col:
            self.col -= 1
        else:
            # Llegó al punto de patrulla, siguiente
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)

    def chase_player(self):
        """
        Movimiento simple hacia el jugador
        """
        if self.row < self.player.row:
            self.row += 1
        elif self.row > self.player.row:
            self.row -= 1
        elif self.col < self.player.col:
            self.col += 1
        elif self.col > self.player.col:
            self.col -= 1

        # Cambiar estado si pierde visión
        if not self.detect_player():
            self.state = "search"
        else:
            self.last_seen_position = (self.player.row, self.player.col)

    def search_last_seen(self):
        """
        Ir a la última posición conocida del jugador
        """
        if self.last_seen_position is None:
            self.state = "patrol"
            return

        target_row, target_col = self.last_seen_position
        if self.row < target_row:
            self.row += 1
        elif self.row > target_row:
            self.row -= 1
        elif self.col < target_col:
            self.col += 1
        elif self.col > target_col:
            self.col -= 1
        else:
            # Llegó y no encontró jugador
            self.state = "patrol"
            self.last_seen_position = None

        # Si detecta al jugador nuevamente
        if self.detect_player():
            self.state = "chase"
            self.last_seen_position = (self.player.row, self.player.col)

    def draw(self, screen):
        """
        Dibuja el guardian en pantalla
        """
        rect = pygame.Rect(
            self.col * TILE_SIZE,
            self.row * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )
        pygame.draw.rect(screen, self.color, rect)