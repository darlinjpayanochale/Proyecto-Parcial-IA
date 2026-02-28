# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
import sys
from scripts.map import GameMap
from scripts.settings import *
from scripts.player import Player
from scripts.treasure import Treasure


def main():
    # Inicializar pygame
    pygame.init()

    font = pygame.font.SysFont(None, 36)

    # Configurar pantalla completa
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("El Guardián del Tesoro")
    game_map = GameMap()
    player = Player(game_map)
    treasure = Treasure(game_map, player)
    message = ""

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if treasure.check_collision() and not player.has_treasure:
                    player.has_treasure = True
                    message = "Tesoro recogido ¡Regresa a la puerta!" 


            if player.has_treasure:
                 if player.row == player.start_row and player.col == player.start_col:
                      message = "¡Ganaste!"              

            # Permitir salir con ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        player.handle_input()

        
        game_map.draw(screen)
        treasure.draw(screen)
        player.draw(screen)

        if message != "":
            text_surface = font.render(message, True, (255, 255, 255))
            screen.blit(text_surface, (20, 20))

        pygame.display.flip()


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()