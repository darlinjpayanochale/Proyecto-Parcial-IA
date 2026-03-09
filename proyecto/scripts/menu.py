# Nombre: Darlin Javier Payano Chale
# Matrícula: 21-MISN-2-034

import pygame

def show_menu(screen, screen_width, screen_height):
    background = pygame.image.load("assets/images/menu_background.jpg").convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))
    
    # Iniciar música del menú
    pygame.mixer.music.load("assets/music/menu_music.mp3")
    pygame.mixer.music.play(-1)  # -1 hace que se repita infinitamente
    pygame.mixer.music.set_volume(0.5)

    font = pygame.font.SysFont(None, 50)
    big_font = pygame.font.SysFont(None, 100)

    waiting = True

    while waiting:

        screen.fill((0, 0, 0))

        screen.blit(background, (0,0))
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))

        title = big_font.render("EL GUARDIÁN DEL TESORO", True, (255,215,0))
        start = font.render("Presiona ENTER para jugar", True, (255,255,255))

        title_rect = title.get_rect(center=(screen_width//2, screen_height//2 - 80))
        start_rect = start.get_rect(center=(screen_width//2, screen_height//2 + 40))

        screen.blit(title, title_rect)
        screen.blit(start, start_rect)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()