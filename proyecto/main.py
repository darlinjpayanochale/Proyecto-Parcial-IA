# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
import sys
from scripts.map import GameMap
from scripts.settings import *
from scripts.player import Player
from scripts.treasure import Treasure
from scripts.guardian import Guardian


def main():
    # Inicializar pygame
    pygame.init()

    font = pygame.font.SysFont(None, 36)

    # Configurar pantalla completa
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    offset_x = (screen_width - MAP_WIDTH) // 2
    offset_y = (screen_height - MAP_HEIGHT) // 2
    pygame.display.set_caption("El Guardián del Tesoro")
    game_map = GameMap()
    player = Player(game_map)
    treasure = Treasure(game_map, player)
    message = ""
    # Crear guardianes
    patrol1 = [(4,8), (4,10), (6,9)]
    patrol2 = [(8,8), (8,12), (12,10)]
    guardian1 = Guardian(game_map, player, patrol1)
    guardian2 = Guardian(game_map, player, patrol2)
    guardians = [guardian1, guardian2]


    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)  # 60 FPS
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Permitir salir con ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        if message == "":
            info = font.render("Encuentra el tesoro y regresa al inicio", True, (200,200,200))
            info_rect = info.get_rect(center=(screen_width // 2, 70))
            screen.blit(info, info_rect)

        player.handle_input()
        if treasure.check_collision() and not player.has_treasure:
            player.has_treasure = True
            message = "Tesoro recogido ¡Regresa a la puerta!" 
        
        if player.has_treasure:
            if player.row == player.start_row and player.col == player.start_col:
                message = "¡Ganaste! Escapaste con el tesoro."              

        game_map.draw(screen, offset_x, offset_y)
        treasure.draw(screen, offset_x, offset_y)
        player.draw(screen, offset_x, offset_y)

        for guardian in guardians:
            guardian.update()
            guardian.draw(screen, offset_x, offset_y)

        if message != "":
            text_surface = font.render(message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_width // 2, 40))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()