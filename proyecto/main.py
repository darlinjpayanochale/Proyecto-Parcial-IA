# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
import sys
from scripts.map import GameMap
from scripts.settings import *
from scripts.player import Player


def main():
    # Inicializar pygame
    pygame.init()

    # Configurar pantalla completa
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("El Guardián del Tesoro")
    game_map = GameMap()
    player = Player(game_map)

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Permitir salir con ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        player.handle_input()

        # Fondo negro
        game_map.draw(screen)
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()