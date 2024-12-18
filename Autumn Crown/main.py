import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((800, 600)) # Tamaño de la ventana
pygame.display.set_caption("Autumn Crown") # Título de la ventana

# Definir fuente de letra
font = pygame.font.SysFont("Times New Roman", 70)
font_2 = pygame.font.SysFont("Georgia", 30)

# Definir colores
TEXT_COL = (255, 255, 255)

def dibujar_título(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def dibujar_texto(text, font, text_col, x, y):
    img = font_2.render(text, True, text_col)
    screen.blit(img, (x, y))

# Icono del juego
icon = pygame.image.load('Autumn Crown/icon.ico')
pygame.display.set_icon(icon)
#pygame.display.iconfy():
#pygame.set_gamma():

# Imagen de fondo
image = pygame.image.load('Autumn Crown/image/background.jpg')

# Color de fondo
background_color = (255, 255, 255)

# Bucle principal del juego
running = True
while running:
    # Evento para cerrar la ventana
    for event in pygame.event.get(): # Lista de Eventos
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    # Pintar el fondo
    screen.fill(background_color)

    # Dibujar la imagen de fondo
    screen.blit(image, (-50,-50))

    
    # Dibujar textos
    dibujar_título("Autumn Crown", font, TEXT_COL, 180, 80)
    dibujar_texto("• Jugar", font, TEXT_COL, 210, 245)
    dibujar_texto("• Puntuaciones", font, TEXT_COL, 210, 300)
    dibujar_texto("• Opciones", font, TEXT_COL, 210, 350)
    dibujar_texto("• Salir del juego", font, TEXT_COL, 210, 400)
    class boton():
        def __init__(self,imagen,pos,texto,font,color_base,color_flo):
            self.imagen = imagen 
            self.x_pos = pos[0]
            self.y_pos = pos[1]
            self.color_base, self.color_flo = color_base , color_flo
            self.texto = texto
            self.texto = self.font.render(self.texto, True, self.color_base)
            if self.imagen is None:
                self.imagen = self.texto
                self.rect = self.imagen.get_rect(centro=(self.x_pos, self.y_pos))
                self.texto_rect = self.texto.get_rect(centro=(self.x_pos, self.y_pos))
        def actualizaar(self,pantalla):
            if self.imagen is not None:
                pantalla.blit(self.imagen, self.rect)
            pantalla.blit(self.texto, self.texto_rect)
        def inputrevisado(self,posicion):
            if posicion[0] in range(self.rect.left, self.rect.right) and posicion[1] in range(self.rect.top, self.rect.boton):
                return True
            return False
        def cambiarcolor(self,position):
            if position[0] in range (self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.boton):
                self.texto = self.font.render(self.texto_input, True, self.color_flo)
            else:
                self.texto = self.font.render(self.texto_input, True, self.color_base)
        
    def jugar():
        pygame.display.set_caption("jugar")
        while True:
            
            menus_con_mouse = pygame.mouse.get_pos
            screen.fill("black")
            jugar_texto = get_font(45).render(True)
    def jugar(self,color):
        pygame.display.set_caption("Menu")
        while True:
            
            menu_con_mouse = pygame.mouse.get_pos()
            texto_menu = get_font(100).render("Menu", True,"#b68f40")
            rect_menu = texto_menu.get_rect(centro =(640, 100))
            
            boton_jugar = boton(imagen=pygame.image.load("assets/play rect.png"),pos=(640, 250),
                                ) 


    # Limita los FPS a 60
    pygame.time.Clock().tick(60)

    # Actualizar la pantalla
    pygame.display.update()

# Cerrar Pygame
pygame.quit()