import pygame
import sys
from pygame import mixer
from random import choice
from .config import *
import time


class Game:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption(TITLE)

        self.font = pygame.font.SysFont(TYPE_FONT, SIZE_FONT)
        self.fuente_titulo = pygame.font.SysFont(TYPE_FONT, SIZE_FONT+20)
        self.nivel = 0
        self.velocidad_juego = 0.4
        self.max_record = 0
        self.user_text = ""
        self.limpiar_pantalla = (580, 150, 700, 550)
        self.limpiar_record = (550, 50, 370, 50)
        self.colores = ["rojo", "amarillo", "azul", "verde"]
        self.secuencia_colores = []
        self.secuencia_jugador = []
        self.ranking = []
        self.puntajes = []

        self.superficie_boton_inicio = pygame.Rect(190, 550, 200, 50)
        self.superficie_reinicio_record = pygame.Rect(1200, 50, 210, 50)
        self.superficie_nivel_actual = pygame.Rect(190, 490, 200, 50)
        self.superficie_boton_ranking = pygame.Rect(970, 50, 200, 50)
        self.superficie_boton_salir = pygame.Rect(1240, 820, 250, 35)
        self.superficie_titulo = pygame.Rect(100, 20, 370, 80)
        self.superficie_mayor_record = pygame.Rect(550, 50, 370, 50)

        mixer.init()
        self.cargar_records()
        self.dibujar_cuadrados()
        self.dibujar_botones()
        self.bucle_juego()

    def dibujar_cuadrados(self):
        """ Dibuja los cuadrados en la pantalla """
        self.cuadrado_rojo = pygame.draw.rect(self.pantalla, ROJO_OSCURO, CUADRADO_ROJO)
        self.cuadrado_amarillo = pygame.draw.rect(self.pantalla, AMARILLO_OSCURO, CUADRADO_AMARILLO)
        self.cuadrado_azul = pygame.draw.rect(self.pantalla, AZUL_OSCURO, CUADRADO_AZUL)
        self.cuadrado_verde = pygame.draw.rect(self.pantalla, VERDE_OSCURO, CUADRADO_VERDE)
        pygame.display.update()

    def dibujar_texto(self, text, font, color, rect_surface, outline_color=None, outline_width=0):
        """ Dibuja el texto en la pantalla y lo centra """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect_surface.center)
        self.pantalla.blit(text_surface, text_rect)
        if outline_color:
            pygame.draw.rect(self.pantalla, outline_color, rect_surface, outline_width)

    def dibujar_botones(self):
        """ Dibuja todos los botones """
        pygame.draw.rect(self.pantalla, NEGRO, self.superficie_boton_inicio)
        self.dibujar_texto("Iniciar Juego", self.font, BLANCO, self.superficie_boton_inicio)

        pygame.draw.rect(self.pantalla, ROJO_OSCURO, self.superficie_reinicio_record)
        self.dibujar_texto("Reiniciar Record", self.font, BLANCO, self.superficie_reinicio_record)

        pygame.draw.rect(self.pantalla, NEGRO, self.superficie_nivel_actual)
        self.dibujar_texto("Nivel " + str(self.nivel), self.font, BLANCO, self.superficie_nivel_actual)

        pygame.draw.rect(self.pantalla, VERDE_OSCURO, self.superficie_boton_ranking)
        self.dibujar_texto("Ranking", self.font, BLANCO, self.superficie_boton_ranking)

        pygame.draw.rect(self.pantalla, ROJO_OSCURO, self.superficie_boton_salir)
        self.dibujar_texto("Salir del Juego", self.font, BLANCO, self.superficie_boton_salir)

        pygame.draw.rect(self.pantalla, VERDE_OSCURO, self.superficie_titulo, 5)
        self.dibujar_texto("Simon Dice", self.fuente_titulo, BLANCO, self.superficie_titulo)

        pygame.draw.rect(self.pantalla, NEGRO, self.limpiar_record)
        pygame.draw.rect(self.pantalla, VERDE_OSCURO, self.superficie_mayor_record, 5)
        self.cargar_records()
        self.dibujar_texto("Record: " + self.user_text[0:18].strip() + " " + str(
            self.max_record), self.font, BLANCO, self.superficie_mayor_record)
        pygame.display.update()

    def cargar_records(self):
        """ Carga el record máximo y el usuario desde archivos. """
        try:
            with open(PUNTAJE, "r") as f:
                self.max_record = int(f.read().strip() or 0)
            with open(USUARIOS, "r") as f:
                self.user_text = f.read().strip()
        except FileNotFoundError:
            print("Archivos de record no encontrados, se crearán por defecto.")
            self.max_record = 0
            self.user_text = ""
            self.guardar_records()  # Crea los archivos si no existen
        except ValueError:
            print("Error leyendo el record. Reiniciando a 0.")
            self.max_record = 0
            self.user_text = ""
            self.guardar_records()

    def guardar_records(self):
        """ Guarda el record máximo y el usuario en archivos. """
        with open(PUNTAJE, "w") as f:
            f.write(str(self.max_record))
        with open(USUARIOS, "w") as f:
            f.write(self.user_text)

    def imprimir_secuencia_final(self):
        secuencia_final = pygame.draw.rect(self.pantalla, NEGRO, pygame.Rect(550, 150, 800, 550))
        pygame.display.flip()
        altura1 = 190
        altura2 = 190
        for i, x in zip(self.secuencia_colores, self.secuencia_jugador):
            text1 = self.font.render("Secuencia", True, CELESTE)
            self.pantalla.blit(text1, (300+(secuencia_final.width-text1.get_width())/2, 150))
            text1 = self.font.render(i, True, BLANCO)
            self.pantalla.blit(text1, (300+(secuencia_final.width-text1.get_width())/2, altura1))
            text1 = self.font.render("Secuencia Jugador", True, CELESTE)
            self.pantalla.blit(text1, (650+(secuencia_final.width-text1.get_width())/2, 150))
            if i != x:
                text1 = self.font.render(x, True, ROJO_OSCURO)
                self.pantalla.blit(text1, (650+(secuencia_final.width-text1.get_width())/2, altura2))
            else:
                text1 = self.font.render(x, True, BLANCO)
                self.pantalla.blit(text1, (650+(secuencia_final.width-text1.get_width())/2, altura2))
            pygame.display.update()
            altura1 += 30
            altura2 += 30

    def iluminar_color(self, color_name, light_color, dark_color, rect_coords):
        """ Ilumina cuadrados y reproducir sonido """
        mixer.music.load(BEEP)
        mixer.music.set_volume(0.1)
        mixer.music.play()

        pygame.draw.rect(self.pantalla, light_color, pygame.Rect(rect_coords))
        pygame.display.flip()
        time.sleep(0.3)
        pygame.draw.rect(self.pantalla, dark_color, pygame.Rect(rect_coords))
        pygame.display.flip()

    def iniciar_juego(self):
        """ Inicia el juego iluminando un color """
        secuencia_aleatoria = choice(self.colores)
        self.secuencia_colores.append(secuencia_aleatoria)

        for color_name in self.secuencia_colores:
            time.sleep(self.velocidad_juego)
            if color_name == "rojo":
                self.iluminar_color("rojo", ROJO, ROJO_OSCURO, CUADRADO_ROJO)
            elif color_name == "amarillo":
                self.iluminar_color("amarillo", AMARILLO, AMARILLO_OSCURO, CUADRADO_AMARILLO)
            elif color_name == "azul":
                self.iluminar_color("azul", AZUL, AZUL_OSCURO, CUADRADO_AZUL)
            elif color_name == "verde":
                self.iluminar_color("verde", VERDE, VERDE_OSCURO, CUADRADO_VERDE)

    def reiniciar_juego(self):
        """ Reinicia el juego para poder volver a jugar """
        self.secuencia_colores.clear()
        self.secuencia_jugador.clear()
        self.nivel = 0
        pygame.draw.rect(self.pantalla, NEGRO, (180, 500, 400, 50))
        text2 = self.font.render("Nivel: "+str(self.nivel), True, BLANCO)
        self.pantalla.blit(text2, (180+(self.superficie_nivel_actual.width-text2.get_width())/2,
                                   490+(self.superficie_nivel_actual.height-text2.get_height())/2))
        self.dibujar_botones()
        self.bucle_juego()

    def mayor_record(self, is_overall_record=False):
        """ Gestiona el proceso de ingreso de un nuevo record. """
        mixer.music.load(WIN)
        mixer.music.set_volume(0.5)
        mixer.music.play()

        pygame.draw.rect(self.pantalla, NEGRO, (590, 150, 900, 550))  # Borra el área
        self.dibujar_texto("¡Nuevo Record!", self.font, BLANCO, pygame.Rect(650, 250, 400, 50))
        self.dibujar_texto("Tu puntaje: " + str(self.nivel), self.font, BLANCO, pygame.Rect(650, 300, 400, 50))
        self.dibujar_texto("Ingresa tu nombre:", self.font, BLANCO, pygame.Rect(650, 400, 400, 50))

        input_rect = pygame.Rect(700, 460, 200, 32)
        pygame.draw.rect(self.pantalla, BLANCO, input_rect, 2)  # Cuadro de texto

        accept_button_rect = pygame.Rect(700, 500, 200, 50)
        pygame.draw.rect(self.pantalla, NEGRO, accept_button_rect)
        self.dibujar_texto("Aceptar", self.font, BLANCO, accept_button_rect)

        pygame.display.flip()

        self.user_text = ""
        writing = True
        while writing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        writing = False
                    else:
                        self.user_text += event.unicode

                    # Actualizar el texto del input
                    pygame.draw.rect(self.pantalla, NEGRO, input_rect)
                    pygame.draw.rect(self.pantalla, BLANCO, input_rect, 2)
                    self.dibujar_texto(self.user_text, self.font, BLANCO, input_rect)
                    pygame.display.flip()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if accept_button_rect.collidepoint(event.pos):
                        writing = False

        # Guardar el nuevo record (ranking)
        if is_overall_record:
            self.max_record = self.nivel
            self.guardar_records()

        with open(RANKING, "a") as archivo:
            archivo.write(f"\n{self.user_text}   {self.nivel}")

        self.imprimir_secuencia_final()
        self.reiniciar_juego()

    def record(self):
        """ Comprueba si es un record histórico """
        if self.nivel > self.max_record:
            self.mayor_record(is_overall_record=True)
        elif len(self.ranking) < 10 or self.nivel > self.ranking[9][1]:
            self.mayor_record(is_overall_record=False)
        else:
            self.imprimir_secuencia_final()
            pygame.draw.rect(self.pantalla, NEGRO, (200, 540, 170, 50))
            self.dibujar_texto("Perdiste", self.font, BLANCO, self.superficie_boton_inicio)
            self.dibujar_texto("Tu puntaje: " + str(self.nivel), self.font, BLANCO, self.superficie_nivel_actual)
            pygame.display.update()
            mixer.music.load(GAME_OVER)
            mixer.music.set_volume(0.5)
            mixer.music.play()
            time.sleep(1.5)
            self.reiniciar_juego()

    def logica_juego(self):
        """ Funcion para saber si ganas o perdes el juego y para aumentar dificultad """
        for i, x in zip(self.secuencia_colores, self.secuencia_jugador):
            if i != x:
                self.record()
        if self.secuencia_colores == self.secuencia_jugador and self.secuencia_jugador != [] and len(
                self.secuencia_colores) == len(self.secuencia_jugador):
            time.sleep(0.5)
            self.nivel += 1
            pygame.draw.rect(self.pantalla, NEGRO, (230, 500, 150, 50))
            pygame.draw.rect(self.pantalla, NEGRO, (200, 540, 170, 50))
            text1 = self.font.render("Excelente", True, BLANCO)
            self.pantalla.blit(text1, (
                    190+(self.superficie_boton_inicio.width-text1.get_width())/2,
                    550+(self.superficie_boton_inicio.height-text1.get_height())/2))
            text2 = self.font.render("Nivel: "+str(self.nivel), True, BLANCO)
            self.pantalla.blit(text2, (
                    180+(self.superficie_nivel_actual.width-text2.get_width())/2,
                    490+(self.superficie_nivel_actual.height-text2.get_height())/2))
            pygame.display.update()
            time.sleep(0.4)
            if len(self.secuencia_colores) == 5 or len(self.secuencia_colores) == 10 or len(
                    self.secuencia_colores) == 15:
                self.velocidad_juego -= 0.1
            self.secuencia_jugador.clear()
            time.sleep(0.5)
            self.iniciar_juego()

    def manejo_eventos(self, event):
        """ manejo de eventos durante el bucle del juego. """
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.cuadrado_rojo.collidepoint(mouse_pos):
                self.iluminar_color("rojo", ROJO, ROJO_OSCURO, CUADRADO_ROJO)
                self.secuencia_jugador.append("rojo")
            elif self.cuadrado_amarillo.collidepoint(mouse_pos):
                self.iluminar_color("amarillo", AMARILLO, AMARILLO_OSCURO, CUADRADO_AMARILLO)
                self.secuencia_jugador.append("amarillo")
            elif self.cuadrado_azul.collidepoint(mouse_pos):
                self.iluminar_color("azul", AZUL, AZUL_OSCURO, CUADRADO_AZUL)
                self.secuencia_jugador.append("azul")
            elif self.cuadrado_verde.collidepoint(mouse_pos):
                self.iluminar_color("verde", VERDE, VERDE_OSCURO, CUADRADO_VERDE)
                self.secuencia_jugador.append("verde")

            # Clicks en botones de la pantalla principal
            if self.superficie_boton_salir.collidepoint(mouse_pos):
                sys.exit()
            elif self.superficie_reinicio_record.collidepoint(mouse_pos):
                self.confirmar_reinicio_records()
            elif self.superficie_boton_ranking.collidepoint(mouse_pos):
                self.mostrar_ranking() 
            elif self.superficie_boton_inicio.collidepoint(mouse_pos):
                pygame.draw.rect(self.pantalla, NEGRO, pygame.Rect(550, 150, 800, 550))  # Borra el área
                pygame.display.flip()
                self.iniciar_juego()

    def bucle_juego(self):
        running = True
        while running:
            for event in pygame.event.get():
                self.manejo_eventos(event)

            self.logica_juego()
            pygame.display.update()

    def confirmar_reinicio_records(self):
        """ confirmación para reiniciar records. """
        dialog_rect = pygame.Rect(580, 150, 500, 250)
        pygame.draw.rect(self.pantalla, NEGRO, self.limpiar_pantalla)
        pygame.draw.rect(self.pantalla, NEGRO, dialog_rect)
        pygame.draw.rect(self.pantalla, AZUL, dialog_rect, 5)
        self.dibujar_texto("¿Deseas reiniciar todos los records?", self.font, BLANCO, pygame.Rect(
            dialog_rect.x, dialog_rect.y + 50, dialog_rect.width, 50))

        yes_button_rect = pygame.Rect(750, 300, 50, 50)
        no_button_rect = pygame.Rect(850, 300, 50, 50)
        pygame.draw.rect(self.pantalla, NEGRO, yes_button_rect) # Fondo para los botones de SI/NO
        pygame.draw.rect(self.pantalla, NEGRO, no_button_rect)
        self.dibujar_texto("SI", self.font, BLANCO, yes_button_rect)
        self.dibujar_texto("NO", self.font, BLANCO, no_button_rect)
        pygame.display.update()

        waiting_for_answer = True
        while waiting_for_answer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button_rect.collidepoint(event.pos):
                        self.reiniciar_records()
                        waiting_for_answer = False
                    elif no_button_rect.collidepoint(event.pos):
                        waiting_for_answer = False
                    else:
                        waiting_for_answer = False
                    pygame.draw.rect(self.pantalla, NEGRO, self.limpiar_pantalla) # Borra el diálogo 
                    pygame.display.update()

    def reiniciar_records(self):
        """ Reinicia todos los records guardados y actualiza la pantalla. """
        self.max_record = 0
        self.user_text = ""
        self.guardar_records()  # Guarda los records principales

        with open(RANKING, "w") as f:
            f.write(ARCHIVO_REINICIO * 10)

        # Actualizar la visualización del record principal
        pygame.draw.rect(self.pantalla, NEGRO, self.superficie_mayor_record)
        pygame.draw.rect(self.pantalla, VERDE_OSCURO, self.superficie_mayor_record, 5)
        self.dibujar_texto("Record: " + self.user_text + " " + str(
            self.max_record), self.font, BLANCO, self.superficie_mayor_record)
        pygame.display.update()

    def cargar_ranking(self):
        """ Carga y ordena el ranking del archivo RANKING. """
        try:
            with open(RANKING, "r") as f:
                self.ranking = []
                for line in f:
                    parts = line.strip().rsplit(" ", 1)
                    if len(parts) == 2:
                        name = parts[0].strip()
                        try:
                            score = int(parts[1])
                            self.ranking.append((name, score))
                        except ValueError:
                            print(f"Omitir la línea de clasificación mal formada: {line.strip()}")
                self.ranking.sort(key=lambda x: x[1], reverse=True)
        except FileNotFoundError:
            print("Archivo de clasificación no encontrado, se creará uno predeterminado.")
            with open(RANKING, "w") as f:
                f.write(ARCHIVO_REINICIO * 10)
            self.cargar_ranking() # Recargar después de crear el archivo

    def mostrar_ranking(self):
        """muestra el ranking en la pantalla"""
        self.cargar_ranking() # Asegura que el ranking esté actualizado

        pygame.draw.rect(self.pantalla, NEGRO, self.limpiar_pantalla)
        ranking_display_rect = pygame.Rect(580, 150, 500, 450)
        pygame.draw.rect(self.pantalla, NEGRO, ranking_display_rect)
        pygame.draw.rect(self.pantalla, AZUL, ranking_display_rect, 5)

        self.dibujar_texto("Posiciones", self.font, BLANCO, pygame.Rect(
            ranking_display_rect.x, ranking_display_rect.y + 20, ranking_display_rect.width, 30))

        y_offset = ranking_display_rect.y + 80
        for i, (name, score) in enumerate(self.ranking[:10]):  # Mostrar solo los top 10
            rank_text = f"{i + 1}. {name} - {score}"
            self.dibujar_texto(rank_text, self.font, BLANCO, pygame.Rect(
                ranking_display_rect.x + 50, y_offset, ranking_display_rect.width - 100, 30), outline_color=None)
            y_offset += 30
        pygame.display.flip()

        