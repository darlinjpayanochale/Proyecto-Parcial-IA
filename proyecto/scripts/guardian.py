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

        self.move_delay = 200
        self.last_move_time = 0

        self.current_path = []

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
        distance = abs(self.player.row - self.row) + abs(self.player.col - self.col)

        if distance <= 8:
            self.last_seen_position = (self.player.row, self.player.col)
            return True

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
        target = self.patrol_points[self.current_patrol_index]

        if (self.row, self.col) == target:
            self.current_patrol_index = (
                self.current_patrol_index + 1
            ) % len(self.patrol_points)

            target = self.patrol_points[self.current_patrol_index]

        self.move_to(target)

    # MOVIMIENTO CON A*

    def move_to(self, target):

        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < self.move_delay:
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

    # DIBUJO
    def draw(self, screen):
        rect = pygame.Rect(
            self.col * TILE_SIZE,
            self.row * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )
        pygame.draw.rect(screen, (255, 0, 0), rect)