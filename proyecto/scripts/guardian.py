# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
from scripts.settings import TILE_SIZE
from scripts.astar import astar
from scripts.behavior_tree import Selector, Sequence, Condition, Action


class Guardian:

    def __init__(self, game_map, player, patrol_points):

        self.animations = {
            "down": [],
            "up": [],
            "left": [],
            "right": []
        }

        for i in range(1,7):
            img = pygame.image.load(f"assets/sprites/guardian/down{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(int(TILE_SIZE*1.2), int(TILE_SIZE*1.2)))
            self.animations["down"].append(img)

        for i in range(1,7):
            img = pygame.image.load(f"assets/sprites/guardian/up{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(int(TILE_SIZE*1.2), int(TILE_SIZE*1.2)))
            self.animations["up"].append(img)

        for i in range(1,7):
            img = pygame.image.load(f"assets/sprites/guardian/left{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(int(TILE_SIZE*1.2), int(TILE_SIZE*1.2)))
            self.animations["left"].append(img)

        for i in range(1,7):
            img = pygame.image.load(f"assets/sprites/guardian/right{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(int(TILE_SIZE*1.2), int(TILE_SIZE*1.2)))
            self.animations["right"].append(img)

        self.direction = "down"
        self.frame_index = 0
        self.animation_speed = 0.2

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

        max_distance = 6

        dr = self.player.row - self.row
        dc = self.player.col - self.col

        distance = (dr**2 + dc**2) ** 0.5

        if distance > max_distance:
            return False

        steps = int(max(abs(dr), abs(dc)))

        for i in range(1, steps):
            r = int(self.row + dr * i / steps)
            c = int(self.col + dc * i / steps)

            if self.game_map.grid[r][c] == 1:
                return False

        # SOLO guardar posición si realmente lo vemos ahora
        self.last_seen_position = (self.player.row, self.player.col)

        return True

    def has_last_seen_position(self):
        return self.last_seen_position is not None

    # ACCIONES
    
    def chase_player(self):
        self.current_target = (self.player.row, self.player.col)

    def go_to_last_seen(self):
        if (self.row, self.col) == self.last_seen_position:
            self.last_seen_position = None
            self.current_target = None
        else:
            self.current_target = self.last_seen_position

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
        
        if self.player.has_treasure:
            move_delay = 150
        else:
            move_delay = 200

        if current_time - self.last_move_time < move_delay:
            return

        path = astar(
            self.game_map.grid,
            (self.row, self.col),
            target
        )

        if path and len(path) > 0:
            next_row, next_col = path[0]

            # calcular dirección
            dr = next_row - self.row
            dc = next_col - self.col

            if dr > 0:
                self.direction = "down"
            elif dr < 0:
                self.direction = "up"
            elif dc > 0:
                self.direction = "right"
            elif dc < 0:
                self.direction = "left"

            self.row, self.col = next_row, next_col
        else:
            # si no hay camino, volver a patrullar
            self.current_target = None

        self.last_move_time = current_time

    # UPDATE

    def update(self):

        # ejecutar árbol de comportamiento
        self.tree.run()

        # moverse si hay objetivo
        if hasattr(self, "current_target") and self.current_target:
            self.move_to(self.current_target)

        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.animations[self.direction]):
            self.frame_index = 0


    # DIBUJO

    def draw(self, screen, offset_x, offset_y):

        sprite = self.animations[self.direction][int(self.frame_index)]

        x = self.col * TILE_SIZE + offset_x
        y = self.row * TILE_SIZE + offset_y

        screen.blit(sprite,(x - TILE_SIZE*0.1, y - TILE_SIZE*0.1))


        # Blanco cuando está agresivo
        if self.player.has_treasure:
            color = (255, 255, 255)  # blanco
        else:
            color = (255, 0, 0)      # rojo normal

        