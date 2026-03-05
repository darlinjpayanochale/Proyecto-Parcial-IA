# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
from scripts.settings import TILE_SIZE
from scripts.astar import astar
from scripts.behavior_tree import Selector, Sequence, Condition, Action


class Guardian:

    def __init__(self, game_map, player, patrol_points):
        self.game_map = game_map
        self.player = player
        self.patrol_points = patrol_points
        self.current_patrol_index = 0

        self.row, self.col = patrol_points[0]

        self.last_seen_position = None
        self.last_move_time = 0

        # ÁRBOL DE COMPORTAMIENTO
        self.tree = Selector([
            Sequence([
                Condition(self.can_see_player),
                Action(self.chase_player)
            ]),
            Sequence([
                Condition(self.has_last_seen_position),
                Action(self.go_to_last_seen)
            ]),
            Action(self.patrol)
        ])

    # CONDICIONES

    def can_see_player(self):
        max_distance = 7

        dr = self.player.row - self.row
        dc = self.player.col - self.col

        distance = max(abs(dr), abs(dc))

        if distance > max_distance:
            return False

        steps = distance

        if steps == 0:
            return True

        step_row = dr / steps
        step_col = dc / steps

        current_row = self.row
        current_col = self.col

        for _ in range(steps):
            current_row += step_row
            current_col += step_col

            grid_row = round(current_row)
            grid_col = round(current_col)

            if (grid_row, grid_col) == (self.player.row, self.player.col):
                self.last_seen_position = (self.player.row, self.player.col)
                return True

            if self.game_map.grid[grid_row][grid_col] == 1:
                return False

        return False

    def has_last_seen_position(self):
        return self.last_seen_position is not None
    
    # ACCIONES


    def chase_player(self):
        target = (self.player.row, self.player.col)
        self.move_to(target)

    def go_to_last_seen(self):
        if (self.row, self.col) == self.last_seen_position:
            self.last_seen_position = None
            return

        self.move_to(self.last_seen_position)

    def patrol(self):

        if not self.patrol_points:
            return

        target = self.patrol_points[self.current_patrol_index]

        if (self.row, self.col) == target:
            self.current_patrol_index = (
                self.current_patrol_index + 1
            ) % len(self.patrol_points)

            target = self.patrol_points[self.current_patrol_index]

        self.current_target = target

    # MOVIMIENTO CON A*

    def move_to(self, target):

        current_time = pygame.time.get_ticks()

        # Velocidad dinámica
        if self.player.has_treasure:
            move_delay = 150   # agresivo (más rápido)
        else:
            move_delay = 200   # normal

        if current_time - self.last_move_time < move_delay:
            return

        path = astar(
            self.game_map.grid,
            (self.row, self.col),
            target
        )

        if path:
            next_step = path[0]
            self.row, self.col = next_step

        self.last_move_time = current_time

    # UPDATE

    def update(self):
        self.tree.run()

        if self.current_target is not None:
             self.move_to(self.current_target)


    # DIBUJO

    def draw(self, screen):
        rect = pygame.Rect(
            self.col * TILE_SIZE,
            self.row * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

        # Blanco cuando está agresivo
        if self.player.has_treasure:
            color = (255, 255, 255)  # blanco
        else:
            color = (255, 0, 0)      # rojo normal

        pygame.draw.rect(screen, color, rect)