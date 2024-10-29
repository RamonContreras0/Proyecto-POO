import pygame

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((800, 600)) # Tamaño de la ventana
pygame.display.set_caption("Autumn Crown") # Título de la ventana

#pygame.display.set_icon():
#pygame.display.iconfy():
#pygame.set_gamma():

# Color de fondo
background_color = (0, 0 ,0)

# Bucle principal del juego
running = True
while running:
    # Evento para cerrar la ventana
    for event in pygame.event.get(): # Lista de Eventos
        if event.type == pygame.QUIT:
            running = False

    # Pintar el fondo
    screen.fill(background_color)

    # Actualizar la pantalla
    pygame.display.update()

# Cerrar Pygame
pygame.quit()