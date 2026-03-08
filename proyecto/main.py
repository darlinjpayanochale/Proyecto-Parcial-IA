# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame
import sys
from scripts.map import GameMap
from scripts.settings import *
from scripts.player import Player
from scripts.treasure import Treasure
from scripts.guardian import Guardian
from scripts.menu import show_menu

def start_new_game():

    game_map = GameMap()
    player = Player(game_map)
    treasure = Treasure(game_map, player)

    patrol1 = [(4,8), (4,10), (6,9)]
    patrol2 = [(8,8), (8,12), (12,10)]

    guardian1 = Guardian(game_map, player, patrol1)
    guardian2 = Guardian(game_map, player, patrol2)

    guardians = [guardian1, guardian2]

    return game_map, player, treasure, guardians

def main():

    pygame.init()

    pygame.mixer.init()

    sound_treasure = pygame.mixer.Sound("assets/sounds/treasure.wav")
    sound_caught = pygame.mixer.Sound("assets/sounds/caught.wav")
    sound_win = pygame.mixer.Sound("assets/sounds/win.wav")

    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 90)

    # Pantalla completa
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("El Guardián del Tesoro")

    screen_width, screen_height = screen.get_size()
    # Mostrar menú primero
    show_menu(screen, screen_width, screen_height)

    # Cambiar a música de juego
    pygame.mixer.music.load("assets/music/game_music.mp3")
    pygame.mixer.music.play(-1, fade_ms=1500)  # Repite la música del juego
    pygame.mixer.music.set_volume(0.5)  

    # Centrar mapa
    offset_x = (screen_width - MAP_WIDTH) // 2
    offset_y = (screen_height - MAP_HEIGHT) // 2

    game_map, player, treasure, guardians = start_new_game()
    
    message = ""
    game_over = False

    clock = pygame.time.Clock()
    running = True

    while running:

        clock.tick(60)
        screen.fill((0,0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # CONTROLES CUANDO EL JUEGO TERMINA
                if game_over:

                        if event.key == pygame.K_r:

                            game_map, player, treasure, guardians = start_new_game()

                            message = ""
                            game_over = False

                             # Reiniciar música del juego
                            pygame.mixer.music.load("assets/music/game_music.mp3")
                            pygame.mixer.music.play(-1, fade_ms=1500)
                            pygame.mixer.music.set_volume(0.5)

                        if event.key == pygame.K_ESCAPE:
                            running = False

                # CONTROLES NORMALES DEL JUEGO
                else:
                    if event.key == pygame.K_ESCAPE:
                        running = False

        if not game_over:
            player.handle_input()

        # TESORO
        if not game_over and treasure.check_collision() and not player.has_treasure:
            player.has_treasure = True
            message = "Tesoro recogido ¡Regresa!"
            sound_treasure.play()

        # GANAR
        if not game_over and player.has_treasure:
            if player.row == player.start_row and player.col == player.start_col:
                message = "¡GANASTE!"
                game_over = True
                pygame.mixer.music.fadeout(1500)
                sound_win.play()

        # DIBUJAR MAPA
        game_map.draw(screen, offset_x, offset_y)
        treasure.draw(screen, offset_x, offset_y)
        player.draw(screen, offset_x, offset_y)

        # GUARDIANES
        for guardian in guardians:

            if not game_over:
                if guardian.row == player.row and guardian.col == player.col:
                    message = "GAME OVER"
                    game_over = True
                    pygame.mixer.music.fadeout(1500)
                    sound_caught.play()

                guardian.update()

            guardian.draw(screen, offset_x, offset_y)

        # MENSAJE SUPERIOR 
        if not game_over:

            if not player.has_treasure:
                info = font.render("Encuentra el tesoro y regresa al inicio.", True, (200,200,200))
            else:
                info = font.render("Tesoro recogido ¡Regresa!", True, (255,215,0))

            info_rect = info.get_rect(center=(screen_width // 2, 70))
            screen.blit(info, info_rect)

        # MENSAJE GRANDE SOLO PARA GANAR O PERDER
        if message == "GAME OVER" or message == "¡GANASTE!":

            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(150)
            overlay.fill((0,0,0))
            screen.blit(overlay,(0,0))

            if message == "GAME OVER":
                color = (255,0,0)
            else:
                color = (0,255,0)

            text_surface = big_font.render(message, True, color)

            text_rect = text_surface.get_rect(
                center=(screen_width // 2, screen_height // 2)
            )

            screen.blit(text_surface, text_rect)

            restart_text = font.render("Presiona R para jugar otra vez o ESC para salir.", True, (255,255,255))
            restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 80))
            screen.blit(restart_text, restart_rect)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()