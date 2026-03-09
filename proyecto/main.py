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


"""Esta función se encarga de crear todos los elementos necesarios
cada vez que empieza una partida nueva o se reinicia el juego.
Aquí se generan el mapa, el jugador, el tesoro y los guardianes."""
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

    #Cargar los efectos de sonido del juego
    #Cada uno se reproduce en momentos específicos.
    sound_treasure = pygame.mixer.Sound("assets/sounds/treasure.wav")
    sound_caught = pygame.mixer.Sound("assets/sounds/caught.wav")
    sound_win = pygame.mixer.Sound("assets/sounds/win.wav")
    

    #Fuentes que se usarán para mostrar textos en pantalla
    #font se usa para mensajes normales y big_font para mensajes importantes
    font = pygame.font.SysFont(None, 44)
    big_font = pygame.font.SysFont(None, 90)

    # Pantalla completa
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("El Guardián del Tesoro")

    screen_width, screen_height = screen.get_size()
    
    #Fonde del juego que se muestra detrás del mapa.
    #Se escala al tamaño de la pantalla para cubrir rodo el fondo.
    background = pygame.image.load("assets/backgrounds/dungeon.jpg").convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))
    
    #Capa oscura transparente que se coloca encima del fondo
    #para que el mapa del juego resalte más visualmente.
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(200)   
    overlay.fill((0,0,0))
        
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

    #Bucle principal del juego.
    #Aquí se actualiza la lógica, se procesan eventos y se dibuja todo en pantalla. 
    while running:

        clock.tick(60)
        screen.blit(background, (0,0))
        screen.blit(overlay,(0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                #Controles cuando el juego termina
                if game_over:

                        if event.key == pygame.K_r:

                            sound_win.stop()
                            sound_caught.stop()

                            game_map, player, treasure, guardians = start_new_game()

                            message = ""
                            game_over = False

                             # Reiniciar música del juego
                            pygame.mixer.music.load("assets/music/game_music.mp3")
                            pygame.mixer.music.play(-1, fade_ms=1500)
                            pygame.mixer.music.set_volume(0.3)

                        if event.key == pygame.K_ESCAPE:
                            running = False

                #Controles normales del juego
                else:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_m:

                        pygame.mixer.music.stop()

                        show_menu(screen, screen_width, screen_height)

                        pygame.mixer.music.load("assets/music/game_music.mp3")
                        pygame.mixer.music.play(-1, fade_ms=1500)
                        pygame.mixer.music.set_volume(0.3)

                        game_map, player, treasure, guardians = start_new_game()

                        message = ""
                        game_over = False
                    
        if not game_over:
                        player.handle_input()

        #Verifica si el jugador llegó a la posición del tesoro
        #Si lo recoge, se activa el estado de "tesoro obtenido"
        if not game_over and treasure.check_collision() and not player.has_treasure:
            player.has_treasure = True
            message = "Tesoro recogido ¡Regresa!"
            sound_treasure.play()

        #Si el jugador tiene el tesoro y vuelve a la posición inicial,
        #eljuego se considera ganado.
        if not game_over and player.has_treasure:
            if player.row == player.start_row and player.col == player.start_col:
                message = "¡GANASTE!"
                game_over = True
                pygame.mixer.music.stop()
                sound_win.play()

        #Dibujar mapa
        game_map.draw(screen, offset_x, offset_y)
        treasure.draw(screen, offset_x, offset_y)
        player.draw(screen, offset_x, offset_y)

        #Actualizar el comportamiento de los guardianes.
        #También se verifica si alguno atrapa añ jugador.
        for guardian in guardians:

            if not game_over:
                if guardian.row == player.row and guardian.col == player.col:
                    message = "GAME OVER"
                    game_over = True
                    pygame.mixer.music.stop()
                    sound_caught.play()

                guardian.update()

            guardian.draw(screen, offset_x, offset_y)

        #Mensaje superior 
        if not game_over:

            if not player.has_treasure:
                info = font.render("Encuentra el tesoro y regresa al inicio.", True, (200,200,200))
            else:
                info = font.render("Tesoro recogido ¡Regresa!", True, (255,215,0))

            info_rect = info.get_rect(center=(screen_width // 2, 30))
            screen.blit(info, info_rect)

            hint = font.render("Moverse = ASWD", True, (200,200,200))
            screen.blit(hint, (20, 20))

            hint = font.render("ESC = Salir", True, (200,200,200))
            screen.blit(hint, (20, 80))

            hint = font.render("M = Menu", True, (200,200,200))
            screen.blit(hint, (20, 140))

        #Mensaje grande solo para ganar o perder
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