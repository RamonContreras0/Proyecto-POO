import pygame
import sys
import math
import time

# Inicialización de Pygame
pygame.init()

# Obtener la resolución de la pantalla completa
pantalla_resolucion = pygame.display.Info()
ANCHO = pantalla_resolucion.current_w
ALTO = pantalla_resolucion.current_h

# Crear la pantalla en modo pantalla completa
screen = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("Autumn Crown - Tower Defense")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)

# Fuentes
fuente_menu = pygame.font.SysFont("Arial", 50, bold=True)  # Fuente para las opciones
fuente_titulo = pygame.font.SysFont("Arial", 60, bold=True)  # Fuente para el título

# Opciones del menú principal
opciones = ["Jugar", "Salir"]
opcion_seleccionada = 0

# Dificultad seleccionada
dificultad = "Medio"

# Torretas disponibles para colocar
torretas_disponibles = ["Torre 1", "Torre 2", "Torre 3"]
torretas_posicionadas = []
torreta_seleccionada = 0  # Índice de la torreta seleccionada

# Puntos específicos donde se pueden colocar las torretas (agregados 3 nuevos puntos)
puntos_colocacion = [
    (200, 300),
    (400, 300),
    (600, 300),
    (200, 400),
    (400, 400),
    (600, 400),
    (200, 500),  # Nuevo punto
    (400, 500),  # Nuevo punto
    (600, 500)   # Nuevo punto
]

# Enemigos (representados por círculos) que avanzan hacia las torretas
enemigos = []

# Proyectiles disparados por las torretas
proyectiles = []

# Control de generación de enemigos
tiempo_inicio = None
enemigos_generados = 0
max_enemigos = 20
intervalo_generacion = 1  # Un enemigo por segundo durante 30 segundos

# Función para crear un nuevo enemigo
def crear_enemigo():
    enemigo = {
        'posicion': [ANCHO - 50, ALTO // 2],  # Empezamos a la derecha y en el medio de la pantalla
        'radio': 15,  # Tamaño del enemigo
        'color': ROJO,
        'velocidad': 3,  # Velocidad de movimiento del enemigo
        'destino': (200, 300),  # El enemigo se dirige a la primera torre colocada
        'vida': 3  # El enemigo tiene 3 puntos de vida
    }
    enemigos.append(enemigo)
    global enemigos_generados
    enemigos_generados += 1

# Función para mover los enemigos
def mover_enemigos():
    for enemigo in enemigos:
        # Mover enemigo hacia su destino
        dx = enemigo['destino'][0] - enemigo['posicion'][0]
        dy = enemigo['destino'][1] - enemigo['posicion'][1]
        distancia = math.sqrt(dx ** 2 + dy ** 2)  # Calcula la distancia

        # Si la distancia es mayor que 1, normalizamos la dirección
        if distancia > 1:
            dx /= distancia
            dy /= distancia

            # Mueve el enemigo hacia la torre
            enemigo['posicion'][0] += dx * enemigo['velocidad']
            enemigo['posicion'][1] += dy * enemigo['velocidad']

# Función para crear un proyectil desde una torre hacia un enemigo
def disparar_proyectil(torreta_pos):
    if len(enemigos) > 0:
        proyectil = {
            'posicion': [torreta_pos[0] + 25, torreta_pos[1] + 25],  # Proyectil aparece en el centro de la torreta
            'color': AZUL,
            'velocidad': 5,
            'destino': enemigos[0]  # El proyectil va hacia el primer enemigo
        }
        proyectiles.append(proyectil)

# Función para mover los proyectiles
def mover_proyectiles():
    global enemigos
    for proyectil in proyectiles:
        # Movimiento del proyectil hacia el enemigo
        dx = proyectil['destino']['posicion'][0] - proyectil['posicion'][0]
        dy = proyectil['destino']['posicion'][1] - proyectil['posicion'][1]
        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia > 1:
            dx /= distancia
            dy /= distancia

            proyectil['posicion'][0] += dx * proyectil['velocidad']
            proyectil['posicion'][1] += dy * proyectil['velocidad']

            # Verificar si el proyectil tocó a un enemigo
            for enemigo in enemigos:
                if math.sqrt((proyectil['posicion'][0] - enemigo['posicion'][0])**2 + (proyectil['posicion'][1] - enemigo['posicion'][1])**2) < enemigo['radio']:
                    enemigo['vida'] -= 1  # Disminuir la vida del enemigo
                    proyectiles.remove(proyectil)  # El proyectil desaparece al impactar
                    if enemigo['vida'] <= 0:
                        enemigos.remove(enemigo)  # El enemigo muere si su vida llega a 0
                    break

# Función para dibujar el menú principal
def dibujar_menu():
    screen.fill(NEGRO)

    # Título del juego
    titulo = fuente_titulo.render("Autumn Crown", True, BLANCO)
    screen.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 4))

    # Opciones del menú
    for i, opcion in enumerate(opciones):
        color = VERDE if i == opcion_seleccionada else AMARILLO
        texto = fuente_menu.render(opcion, True, color)
        screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 + i * 60))

    pygame.display.update()

# Función para dibujar el juego
def dibujar_juego():
    screen.fill(NEGRO)

    # Dibujar las torretas disponibles en la parte superior en una línea horizontal
    espacio = 70  # Espacio entre las torretas
    for i, torreta in enumerate(torretas_disponibles):
        color = VERDE if i == torreta_seleccionada else AMARILLO
        x_pos = 20 + i * espacio  # Coloca cada torreta a la derecha
        pygame.draw.rect(screen, color, pygame.Rect(x_pos, 50, 50, 50))  # Cuadro de torre

    # Dibujar las torretas colocadas
    for torreta in torretas_posicionadas:
        pygame.draw.rect(screen, ROJO, pygame.Rect(torreta[0], torreta[1], 50, 50))

    # Dibujar los enemigos
    for enemigo in enemigos:
        pygame.draw.circle(screen, enemigo['color'], (int(enemigo['posicion'][0]), int(enemigo['posicion'][1])), enemigo['radio'])

    # Dibujar los proyectiles
    for proyectil in proyectiles:
        pygame.draw.circle(screen, proyectil['color'], (int(proyectil['posicion'][0]), int(proyectil['posicion'][1])), 5)

    # Dibujar los puntos donde se pueden colocar torretas
    for punto in puntos_colocacion:
        pygame.draw.circle(screen, BLANCO, punto, 10)  # Dibujar círculos en los puntos de colocación

    pygame.display.update()

# Función para manejar los clics del ratón en el juego
def manejar_click_juego():
    global torreta_seleccionada, torretas_posicionadas
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Si el clic está en una de las torretas seleccionables, cambiar la torre seleccionada
    espacio = 70  # Espacio entre las torretas
    if mouse_y > 50 and mouse_y < 100:  # Verifica si el clic es en la línea de torretas
        for i in range(len(torretas_disponibles)):
            if 20 + i * espacio <= mouse_x <= 20 + (i + 1) * espacio:
                torreta_seleccionada = i
                break
    else:
        # Colocar la torre seleccionada solo en puntos específicos
        for punto in puntos_colocacion:
            if abs(mouse_x - punto[0]) < 25 and abs(mouse_y - punto[1]) < 25:  # Si está cerca del punto de colocación
                torretas_posicionadas.append((punto[0] - 25, punto[1] - 25))  # Ajustamos para centrar la torre
                disparar_proyectil((punto[0] - 25, punto[1] - 25))  # Disparar un proyectil desde esta torre
                break

# Bucle principal
estado = "menu"  # Estados posibles: "menu", "juego"
while True:
    if estado == "menu":
        dibujar_menu()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Click izquierdo del ratón
                    if opcion_seleccionada == 0:  # Si estamos en el menú principal
                        estado = "juego"  # Cambiar al estado de juego
                        tiempo_inicio = time.time()  # Comenzamos a contar el tiempo de generación de enemigos
                    elif opcion_seleccionada == 1:  # Si se selecciona "Salir"
                        pygame.quit()
                        sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                elif evento.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)

    elif estado == "juego":
        # Control del tiempo para generar enemigos durante 30 segundos
        if tiempo_inicio and time.time() - tiempo_inicio <= 30 and enemigos_generados < max_enemigos:
            if time.time() - tiempo_inicio >= intervalo_generacion * enemigos_generados:
                crear_enemigo()

        dibujar_juego()
        mover_enemigos()  # Mover los enemigos
        mover_proyectiles()  # Mover los proyectiles

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Click izquierdo del ratón
                    manejar_click_juego()

    pygame.time.Clock().tick(30)  # Limitar la velocidad de actualización
