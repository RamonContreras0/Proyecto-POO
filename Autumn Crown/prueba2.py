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
fuente_info = pygame.font.SysFont("Arial", 30)  # Fuente para la información de torretas

# Opciones del menú principal
opciones = ["Jugar", "Salir"]
opcion_seleccionada = 0

# Dificultad seleccionada
dificultad = "Medio"

# Torretas disponibles para colocar
torretas_disponibles = ["Asesino", "Hada", "Cazador", "Caballero"]
torretas_posicionadas = []
torreta_seleccionada = None  # Inicializamos como None, para evitar errores al seleccionar

# Puntos específicos donde se pueden colocar las torretas (ubicación de las casillas de la cuadrícula)
puntos_colocacion = [
    (200, 300),
    (400, 300),
    (600, 300),
    (200, 400),
    (400, 400),
    (600, 400),
    (200, 500),
    (400, 500),
    (600, 500),
    (300, 600),
    (500, 600),
    (300, 700),
    (500, 700)
]

# Enemigos (representados por círculos) que avanzan hacia las torretas
enemigos = []

# Proyectiles disparados por las torretas
proyectiles = []

# Control de generación de enemigos
tiempo_inicio = time.time()  # Inicializamos el tiempo de inicio para que se pueda utilizar
enemigos_generados = 0
max_enemigos = 30  # Aumentamos la cantidad de enemigos
intervalo_generacion = 1  # Un enemigo por segundo durante 30 segundos

# Diccionario con las estadísticas de las torretas
torretas_info = {
    "Asesino": {
        "salud": 80,
        "daño": 20,
        "velocidad": 15,
        "alcance": 2,
        "defensa": 5,
        "habilidad": "Golpe Sombra",
        "descripcion": "Realiza un ataque crítico que inflige 50% más de daño y tiene un 30% de probabilidad de eliminar al enemigo de un solo golpe.",
        "enfriamiento": 5,
        "ultima_habilidad": 0  # Última vez que se usó la habilidad
    },
    "Hada": {
        "salud": 60,
        "daño": 10,
        "velocidad": 12,
        "alcance": 5,
        "defensa": 3,
        "habilidad": "Bendición de Luz",
        "descripcion": "Restaura el 30% de la salud a todos los aliados cercanos y aumenta su velocidad de ataque en un 20% durante 15 segundos.",
        "enfriamiento": 20,
        "ultima_habilidad": 0
    },
    "Cazador": {
        "salud": 100,
        "daño": 15,
        "velocidad": 10,
        "alcance": 3,
        "defensa": 7,
        "habilidad": "Ataque Táctico",
        "descripcion": "Permite tirar muchas proyectiles al aire y cada uno hace 20 de daño.",
        "enfriamiento": 25,
        "ultima_habilidad": 0
    },
    "Caballero": {
        "salud": 120,
        "daño": 12,
        "velocidad": 8,
        "alcance": 1,
        "defensa": 10,
        "habilidad": "Barrera de Hierro",
        "descripcion": "Crea una barrera que reduce el daño recibido por él y sus aliados en un 50% durante 8 segundos.",
        "enfriamiento": 30,
        "ultima_habilidad": 0
    }
}

# Función para crear un nuevo enemigo
def crear_enemigo():
    global enemigos_generados
    destino = puntos_colocacion[enemigos_generados % len(puntos_colocacion)]  # Asignar destino de los puntos disponibles
    enemigo = {
        'posicion': [ANCHO - 50, ALTO // 2],  # Comienza en la parte derecha de la pantalla
        'radio': 15,  # Tamaño del enemigo
        'color': ROJO,
        'velocidad': 1,  # Velocidad reducida para que se mueva más lento
        'destino': destino,  # El enemigo se dirige a uno de los puntos de colocación
        'vida': 3  # Vida del enemigo
    }
    enemigos.append(enemigo)
    enemigos_generados += 1  # Incrementamos la cantidad de enemigos generados

# Función para mover los enemigos
def mover_enemigos():
    for enemigo in enemigos:
        # Calcular la dirección hacia el destino
        dx = enemigo['destino'][0] - enemigo['posicion'][0]
        dy = enemigo['destino'][1] - enemigo['posicion'][1]
        distancia = math.sqrt(dx ** 2 + dy ** 2)  # Calcula la distancia

        # Si la distancia es mayor que 1, normalizamos la dirección
        if distancia > 1:
            dx /= distancia
            dy /= distancia
            enemigo['posicion'][0] += dx * enemigo['velocidad']
            enemigo['posicion'][1] += dy * enemigo['velocidad']
        else:
            # Si el enemigo ha llegado a su destino, avanzamos al siguiente destino
            current_index = puntos_colocacion.index(tuple(enemigo['destino']))  # Encuentra el índice del destino actual
            if current_index + 1 < len(puntos_colocacion):  # Si hay un siguiente punto en la ruta
                enemigo['destino'] = puntos_colocacion[current_index +1]  # Asignamos el siguiente destino
            else:
                # Si no hay siguiente punto (llegó al final de la ruta), eliminamos el enemigo
                enemigos.remove(enemigo)

# Función para dibujar el menú principal
def dibujar_menu():
    screen.fill(NEGRO)

    # Título
    texto_titulo = fuente_titulo.render("Autumn Crown - Tower Defense", True, BLANCO)
    screen.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 4))

    # Opciones del menú
    for i, opcion in enumerate(opciones):
        color = AMARILLO if opcion_rect(i).collidepoint(pygame.mouse.get_pos()) else BLANCO
        texto_opcion = fuente_menu.render(opcion, True, color)
        screen.blit(texto_opcion, (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 60))

    pygame.display.update()

# Función para obtener el rectángulo de la opción del menú
def opcion_rect(indice):
    texto_opcion = fuente_menu.render(opciones[indice], True, BLANCO)
    return pygame.Rect(ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + indice * 60, texto_opcion.get_width(), texto_opcion.get_height())

# Función para dibujar la pantalla de selección de torretas
def dibujar_seleccion_torretas():
    screen.fill(NEGRO)

    # Dibujar las casillas para torretas
    for i, torreta in enumerate(torretas_disponibles):
        rect = pygame.Rect(20 + i * 200, 100, 100, 100)  # Casilla más pequeña
        pygame.draw.rect(screen, AZUL, rect)
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, VERDE, rect, 5)

    pygame.display.update()

# Función para dibujar el juego
def dibujar_juego():
    screen.fill(NEGRO)

    # Dibujar enemigos
    for enemigo in enemigos:
        pygame.draw.circle(screen, enemigo['color'], (int(enemigo['posicion'][0]), int(enemigo['posicion'][1])), enemigo['radio'])

    # Dibujar torretas
    for torreta in torretas_posicionadas:
        pygame.draw.rect(screen, AZUL, (torreta[0] - 25, torreta[1] - 25, 50, 50))

    # Dibujar la cuadrícula de colocación de torretas
    for punto in puntos_colocacion:
        pygame.draw.rect(screen, BLANCO, (punto[0] - 25, punto[1] - 25, 50, 50), 2)

    pygame.display.update()

# Bucle principal
estado = "menu"
while True:
    if estado == "menu":
        dibujar_menu()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if opcion_rect(0).collidepoint(evento.pos):
                    estado = "seleccion_torreta"
                elif opcion_rect(1).collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

    elif estado == "seleccion_torreta":
        dibujar_seleccion_torretas()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(torretas_disponibles):
                    if pygame.Rect(20 + i * 200, 100, 100, 100).collidepoint(evento.pos):
                        torreta_seleccionada = torretas_disponibles[i]  # Establecer la torreta seleccionada
                        estado = "juego"

    elif estado == "juego":
        dibujar_juego()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for punto in puntos_colocacion:
                    if pygame.Rect(punto[0] - 25, punto[1] - 25, 50, 50).collidepoint(evento.pos):
                        if torreta_seleccionada is not None:
                            torretas_posicionadas.append((punto[0], punto[1]))  # Coloca la torreta
                            torreta_seleccionada = None  # Resetear la torreta seleccionada

        # Control de enemigos
        if time.time() - tiempo_inicio >= intervalo_generacion and enemigos_generados < max_enemigos:
            crear_enemigo()
            tiempo_inicio = time.time()  # Resetear el tiempo para el siguiente enemigo
            

        mover_enemigos()

    pygame.display.update()
    pygame.time.Clock().tick(60)
