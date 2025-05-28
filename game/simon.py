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

        # Mayor record puesto en la pantalla desde un archivo
        self.max_record = 0
        self.user_text = ""

        with open(PUNTAJE, "r") as archivo:
            self.max_record = archivo.read()
        with open(USUARIOS, "r") as archivo_usuarios:
            self.user_text = archivo_usuarios.read()

        self.colores = ["rojo", "amarillo", "azul", "verde"]
        self.secuencia_colores = []
        self.secuencia_jugador = []
        self.ranking = []
        self.puntajes = []

        self.dibujar_cuadrados()
        self.dibujar_botones()

    def dibujar_cuadrados(self):
        self.cuadrado_rojo = pygame.draw.rect(self.pantalla, ROJO_OSCURO, pygame.Rect(CUADRADO_ROJO))
        self.cuadrado_amarillo = pygame.draw.rect(self.pantalla, AMARILLO_OSCURO, pygame.Rect(CUADRADO_AMARILLO))
        self.cuadrado_azul = pygame.draw.rect(self.pantalla, AZUL_OSCURO, pygame.Rect(CUADRADO_AZUL))
        self.cuadrado_verde = pygame.draw.rect(self.pantalla, VERDE_OSCURO, pygame.Rect(CUADRADO_VERDE))
        pygame.display.update()

    def dibujar_botones(self):
        self.boton_inicio = ("iniciar juego", pygame.draw.rect(
            self.pantalla, NEGRO, pygame.Rect(190, 550, 200, 50)), self.font, 190, 550)
        self.superficie_boton_inicio = pygame.Rect(190, 550, 200, 50)

        self.reinicio_record = ("Reiniciar Record", pygame.draw.rect(
            self.pantalla, ROJO_OSCURO, pygame.Rect(1200, 50, 210, 50)), self.font, 1200, 50)
        self.superficie_reinicio_record = pygame.Rect(1200, 50, 210, 50)

        self.nivel_actual = ("Nivel "+str(self.nivel), pygame.draw.rect(
            self.pantalla, NEGRO, pygame.Rect((190, 550, 200, 50))), self.font, 180, 490)
        self.superficie_nivel_actual = pygame.Rect(190, 550, 200, 50)

        self.boton_ranking = ("Ranking", pygame.draw.rect(
            self.pantalla, VERDE_OSCURO, pygame.Rect(970, 50, 200, 50)), self.font, 970, 50)
        self.superficie_boton_ranking = pygame.Rect(970, 50, 200, 50)

        self.boton_salir = ("salir del juego", pygame.draw.rect(
            self.pantalla, ROJO_OSCURO, pygame.Rect(1240, 820, 250, 35)), self.font, 1240, 820)
        self.superficie_boton_salir = pygame.Rect(1240, 820, 250, 35)

        self.titulo = ("Simon Dice", pygame.draw.rect(
            self.pantalla, VERDE_OSCURO, pygame.Rect(100, 20, 370, 80), 5), self.fuente_titulo, 100, 20) 
        self.superficie_titulo = pygame.Rect(100, 20, 370, 80)

        self.mayor_record = (
            "Record: "+self.user_text[0:18]+" "+str(self.max_record), pygame.draw.rect(
        self.pantalla, VERDE_OSCURO, pygame.Rect(550, 50, 370, 50), 5), self.font, 550, 50)
        self.superficie_mayor_record = pygame.Rect(550, 50, 370, 50)

        self.pintar_boton_inicio = self.font.render("iniciar juego", True, BLANCO)
        text_rect_pintar_boton_inicio = self.pintar_boton_inicio.get_rect()
        text_rect_pintar_boton_inicio.center = self.superficie_boton_inicio.center
        self.pantalla.blit(self.pintar_boton_inicio, text_rect_pintar_boton_inicio)

        self.pintar_reinicio_record = self.font.render("Reiniciar Record", True, BLANCO)
        text_rect_pintar_reinicio_record = self.pintar_reinicio_record.get_rect()
        text_rect_pintar_reinicio_record.center = self.superficie_reinicio_record.center
        self.pantalla.blit(self.pintar_reinicio_record, text_rect_pintar_reinicio_record)

        self.pintar_nivel_actual = self.font.render("Nivel "+str(self.nivel), True, BLANCO)
        self.pantalla.blit(self.pintar_nivel_actual, (
            180+(self.superficie_nivel_actual.width-self.pintar_nivel_actual.get_width())/2,
            490+(self.superficie_nivel_actual.height-self.pintar_nivel_actual.get_height())/2))

        self.pintar_boton_ranking = self.font.render("Ranking", True, BLANCO)
        text_rect_pintar_boton_ranking = self.pintar_boton_ranking.get_rect()
        text_rect_pintar_boton_ranking.center = self.superficie_boton_ranking.center
        self.pantalla.blit(self.pintar_boton_ranking, text_rect_pintar_boton_ranking)

        self.pintar_boton_salir = self.font.render("salir del juego", True, BLANCO)
        text_rect_pintar_boton_salir = self.pintar_boton_salir.get_rect()
        text_rect_pintar_boton_salir.center = self.superficie_boton_salir.center
        self.pantalla.blit(self.pintar_boton_salir, text_rect_pintar_boton_salir)

        self.pintar_titulo = self.fuente_titulo.render("Simon Dice", True, BLANCO)
        text_rect_pintar_titulo = self.pintar_titulo.get_rect()
        text_rect_pintar_titulo.center = self.superficie_titulo.center
        self.pantalla.blit(self.pintar_titulo, text_rect_pintar_titulo)

        self.pintar_mayor_record = self.font.render("Record: "+self.user_text[0:18]+" "+str(self.max_record), True, BLANCO)
        text_rect_pintar_mayor_record = self.pintar_mayor_record.get_rect()
        text_rect_pintar_mayor_record.center = self.superficie_mayor_record.center
        self.pantalla.blit(self.pintar_mayor_record, text_rect_pintar_mayor_record)

        pygame.display.update()

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

    # Funcion para iniciar el juego
    def iniciar_juego(self):
        # Iniciar sonido
        mixer.init()
        secuencia_aleatoria = choice(self.colores)
        self.secuencia_colores.append(secuencia_aleatoria)
        for secuencia_aleatoria in self.secuencia_colores:
            time.sleep(self.velocidad_juego)
            mixer.music.load(BEEP)
            mixer.music.set_volume(0.1)
            mixer.music.play()
        
            if secuencia_aleatoria == "rojo":
                pygame.draw.rect(self.pantalla, ROJO, pygame.Rect(CUADRADO_ROJO))
                pygame.display.flip()
                time.sleep(0.3)
                pygame.draw.rect(self.pantalla, ROJO_OSCURO, pygame.Rect(CUADRADO_ROJO))
                pygame.display.flip()
            
            if secuencia_aleatoria == "amarillo":
                pygame.draw.rect(self.pantalla, AMARILLO, pygame.Rect(CUADRADO_AMARILLO))
                pygame.display.flip()
                time.sleep(0.3)
                pygame.draw.rect(self.pantalla, AMARILLO_OSCURO, pygame.Rect(CUADRADO_AMARILLO))
                pygame.display.flip()

            if secuencia_aleatoria == "azul":
                pygame.draw.rect(self.pantalla, AZUL, pygame.Rect(CUADRADO_AZUL))
                pygame.display.flip()
                time.sleep(0.3)
                pygame.draw.rect(self.pantalla, AZUL_OSCURO, pygame.Rect(CUADRADO_AZUL))
                pygame.display.flip()

            if secuencia_aleatoria == "verde":
                pygame.draw.rect(self.pantalla, VERDE, pygame.Rect(CUADRADO_VERDE))
                pygame.display.flip()
                time.sleep(0.3)
                pygame.draw.rect(self.pantalla, VERDE_OSCURO, pygame.Rect(CUADRADO_VERDE))
                pygame.display.flip()

    # Funcion para poder volver a jugar
    def reiniciar_juego(self):
        self.secuencia_colores.clear()
        self.secuencia_jugador.clear()
        self.nivel = 0
        pygame.draw.rect(self.pantalla, NEGRO, (180, 500, 400, 50))
        text2 = self.font.render("Nivel: "+str(self.nivel), True, BLANCO)
        self.pantalla.blit(text2, (180+(self.superficie_nivel_actual.width-text2.get_width())/2,
                                   490+(self.superficie_nivel_actual.height-text2.get_height())/2))
        self.bucle_juego()

    def comprobar_mejor_puntaje(self):
        aceptar = pygame.draw.rect(self.pantalla, NEGRO, pygame.Rect(700, 500, 200, 50))
        if int(self.nivel) > int(self.ranking[0][1]):
            self.user_text = ""
            self.max_record = self.nivel
            mixer.music.load(WIN)
            mixer.music.set_volume(0.5)
            mixer.music.play()
            pygame.draw.rect(self.pantalla, NEGRO, (550, 50, 370, 50))
            self.mayor_record = pygame.draw.rect(self.pantalla, VERDE_OSCURO, pygame.Rect(550, 50, 370, 50), 5)
            pygame.draw.rect(self.pantalla, VERDE_OSCURO, pygame.Rect(550, 50, 370, 50), 5)
            pygame.display.update()
            text1 = self.font.render("Record: "+str(self.nivel), True, BLANCO)
            self.pantalla.blit(text1, (550+(self.mayor_record.width-text1.get_width())/2,
                                       50+(self.mayor_record.height-text1.get_height())/2))
            pygame.display.update()
            pygame.draw.rect(self.pantalla, NEGRO, (590, 150, 900, 550))
            with open(PUNTAJE, "w") as archivo:
                archivo.write(str(self.nivel))
            text2 = self.font.render("Nuevo record: "+str(self.nivel), True, BLANCO)
            self.pantalla.blit(text2, (
                700+(self.superficie_nivel_actual.width-text2.get_width())/2,
                300+(self.superficie_nivel_actual.height-text2.get_height())/2))
            pygame.display.flip()
            text1 = self.font.render("ingresa tu nombre: ", True, BLANCO)
            self.pantalla.blit(text1, (
                700+(self.superficie_boton_inicio.width-text1.get_width())/2,
                400+(self.superficie_boton_inicio.height-text1.get_height())/2))
            pygame.display.update()
            text1 = self.font.render("Aceptar", True, BLANCO)
            self.pantalla.blit(text1, (
                700+(self.superficie_boton_inicio.width-text1.get_width())/2,
                500+(self.superficie_boton_inicio.height-text1.get_height())/2))
            pygame.display.update()
            escribir = True
            while escribir:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        escribir = False
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        elif event.type == pygame.K_RETURN:
                            self.user_text = ''
                        else:
                            self.user_text += event.unicode
                            pygame.draw.rect(self.pantalla, NEGRO, (680, 460, 400, 50))
                            input_surface = self.font.render(self.user_text, True, BLANCO)
                            self.pantalla.blit(input_surface, (700, 460))
                            pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN and aceptar.collidepoint(pygame.mouse.get_pos()):
                    with open(USUARIOS, "w") as archivo:
                        archivo.write(self.user_text)
                    with open(RANKING, "a") as archivo:
                        archivo.write("\n"+self.user_text)
                    with open(RANKING, "a") as archivo:
                        archivo.write("   "+str(self.nivel))
                    self.imprimir_secuencia_final()
                    pygame.draw.rect(self.pantalla, NEGRO, (200, 540, 170, 50))
                    text1 = self.font.render("Iniciar juego", True, BLANCO)
                    self.pantalla.blit(text1, (
                        190+(self.superficie_boton_inicio.width-text1.get_width())/2,
                        550+(self.superficie_boton_inicio.height-text1.get_height())/2))
                    pygame.display.update()
                    self.reiniciar_juego()
                    break
        
    def comprobar_puntaje(self):
        aceptar = pygame.draw.rect(self.pantalla, NEGRO, pygame.Rect(700, 500, 200, 50))
        if int(self.nivel) > int(self.ranking[9][1]):
            self.user_text = ""
            self.max_record = self.nivel
            mixer.music.load(WIN)
            mixer.music.set_volume(0.5)
            mixer.music.play()
            text1 = self.font.render("Ingresa tu nombre: ", True, BLANCO)
            self.pantalla.blit(text1, (
                        700+(self.superficie_boton_inicio.width-text1.get_width())/2,
                        400+(self.superficie_boton_inicio.height-text1.get_height())/2))
            pygame.display.update()
            text1 = self.font.render("Aceptar", True, BLANCO)
            self.pantalla.blit(text1, (
                        700+(self.superficie_boton_inicio.width-text1.get_width())/2,
                        500+(self.superficie_boton_inicio.height-text1.get_height())/2))
            pygame.display.update()
            escribir = True
            while escribir:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        escribir = False

                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        elif event.type == pygame.K_RETURN:
                            self.user_text = ''
                        else:
                            self.user_text += event.unicode
                        pygame.draw.rect(self.pantalla, NEGRO, (680, 460, 400, 50))
                        input_surface = self.font.render(self.user_text, True, BLANCO)
                        self.pantalla.blit(input_surface, (700, 460))
                        pygame.display.flip()

                    if event.type == pygame.MOUSEBUTTONDOWN and aceptar.collidepoint(pygame.mouse.get_pos()):
                        with open(RANKING, "a") as archivo:
                            archivo.write("\n"+self.user_text)
                        self.imprimir_secuencia_final()
                        with open(RANKING, "a") as archivo:
                            archivo.write("   "+str(self.nivel))
                        pygame.draw.rect(self.pantalla, NEGRO, (200, 540, 170, 50))
                        text1 = self.font.render("Iniciar juego", True, BLANCO)
                        self.pantalla.blit(text1, (
                            190+(self.superficie_boton_inicio.width-text1.get_width())/2,
                            550+(self.superficie_boton_inicio.height-text1.get_height())/2))
                        pygame.display.update()
                        self.reiniciar_juego()
                        break

    def record(self):
        # Actualizar ranking
        archivo = RANKING
        with open(archivo, "r") as archivo:
            self.ranking = []
            for linea in archivo:
                partes = linea.strip().rsplit(" ", 1)
                if len(partes) == 2:
                    nombre = partes[0]
                    puntaje = int(partes[1])
                    self.ranking.append((nombre, puntaje))
                    self.ranking.sort(key=lambda x: x[1], reverse=True)
        self.imprimir_secuencia_final()
        pygame.draw.rect(self.pantalla, NEGRO, (200, 540, 170, 50))
        text1 = self.font.render("Perdiste", True, BLANCO)
        self.pantalla.blit(text1, (190+(self.superficie_boton_inicio.width-text1.get_width())/2,
                                   550+(self.superficie_boton_inicio.height-text1.get_height())/2))
        pygame.display.update()
        mixer.music.load(GAME_OVER)
        mixer.music.set_volume(0.5)
        mixer.music.play()
        time.sleep(0.5)
        pygame.draw.rect(self.pantalla, NEGRO, (130, 500, 320, 50))
        text2 = self.font.render("Tu record es: "+str(self.nivel), True, BLANCO)
        self.pantalla.blit(text2, (180+(self.superficie_nivel_actual.width-text2.get_width())/2,
                                   490+(self.superficie_nivel_actual.height-text2.get_height())/2))
        pygame.display.update()
        time.sleep(1.5)
        pygame.draw.rect(self.pantalla, NEGRO, (200, 540, 170, 50))
        text1 = self.font.render("Iniciar juego", True, BLANCO)
        self.pantalla.blit(text1, (190+(self.superficie_boton_inicio.width-text1.get_width())/2,
                                   550+(self.superficie_boton_inicio.height-text1.get_height())/2))
        pygame.display.update()
        self.comprobar_mejor_puntaje()
        self.comprobar_puntaje()
        self.reiniciar_juego()

    # Funcion para saber si ganas o perdes el juego
    def logica_juego(self):
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

    # Bucle del juego
    def bucle_juego(self):
        Si = pygame.draw.rect(self.pantalla, NEGRO, pygame.Rect(750, 300, 50, 50))
        No = pygame.draw.rect(self.pantalla, NEGRO, pygame.Rect(850, 300, 50, 50))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode
            
                if event.type == pygame.MOUSEBUTTONDOWN and self.cuadrado_rojo.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.pantalla, ROJO, pygame.Rect(CUADRADO_ROJO))
                    pygame.display.flip()
                    self.secuencia_jugador.append("rojo")
                    mixer.music.load(BEEP)
                    mixer.music.set_volume(0.1)
                    mixer.music.play()
                    time.sleep(0.3)
                    pygame.draw.rect(self.pantalla, ROJO_OSCURO, pygame.Rect(CUADRADO_ROJO))
                    pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN and self.cuadrado_amarillo.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.pantalla, AMARILLO, pygame.Rect(CUADRADO_AMARILLO))
                    pygame.display.flip()
                    self.secuencia_jugador.append("amarillo")
                    mixer.music.load(BEEP)
                    mixer.music.set_volume(0.1)
                    mixer.music.play()
                    time.sleep(0.3)
                    pygame.draw.rect(self.pantalla, AMARILLO_OSCURO, pygame.Rect(CUADRADO_AMARILLO))
                    pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN and self.cuadrado_azul.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.pantalla, AZUL, pygame.Rect(CUADRADO_AZUL))
                    pygame.display.flip()
                    self.secuencia_jugador.append("azul")
                    mixer.music.load(BEEP)
                    mixer.music.set_volume(0.1)
                    mixer.music.play()
                    time.sleep(0.3)
                    pygame.draw.rect(self.pantalla, AZUL_OSCURO, pygame.Rect(CUADRADO_AZUL))
                    pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN and self.cuadrado_verde.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.pantalla, VERDE, pygame.Rect(CUADRADO_VERDE))
                    pygame.display.flip()
                    self.secuencia_jugador.append("verde")
                    mixer.music.load(BEEP)
                    mixer.music.set_volume(0.1)
                    mixer.music.play()
                    time.sleep(0.3)
                    pygame.draw.rect(self.pantalla, VERDE_OSCURO, pygame.Rect(CUADRADO_VERDE))
                    pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN and self.superficie_boton_salir.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and self.superficie_reinicio_record.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.pantalla, NEGRO, (580, 150, 800, 650))
                    pygame.draw.rect(self.pantalla, NEGRO, (580, 150, 500, 250))
                    pygame.draw.rect(self.pantalla, AZUL, (580, 150, 500, 250), 5)
                    text1 = self.font.render("¿Deseas reiniciar todos los records?", True, BLANCO)
                    self.pantalla.blit(text1, (600, 250))
                    afirmativo = self.font.render("SI", True, BLANCO)
                    self.pantalla.blit(afirmativo, (750, 300))
                    negativo = self.font.render("NO", True, BLANCO)
                    self.pantalla.blit(negativo, (850, 300))
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN and Si.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.pantalla, NEGRO, (580, 150, 800, 650))
                    pygame.draw.rect(self.pantalla, NEGRO, (550, 50, 370, 50))
                    pygame.draw.rect(self.pantalla, VERDE_OSCURO, (550, 50, 370, 50), 5)
                    self.max_record = 0
                    self.user_text = ""
                    text1 = self.font.render("Record: "+str(self.user_text)+" "+str(self.max_record), True, BLANCO)
                    self.pantalla.blit(text1, (
                        550+(self.superficie_mayor_record.width-text1.get_width())/2,
                        50+(self.superficie_mayor_record.height-text1.get_height())/2))
                    pygame.display.update()
                    with open(USUARIOS, "w") as archivo_usuarios:
                        self.user_text = archivo_usuarios.write("")
                    with open(PUNTAJE, "w") as archivo:
                        archivo.write(str("0"))
                    with open(RANKING, "w") as archivo_ranking:
                        reinicio_ranking = archivo_ranking.write(ARCHIVO_REINICIO*10)

                    # Actualizar el reinicio
                    with open(RANKING, "r") as archivo_ranking:
                        archivo_leer = archivo_ranking.read()
                    altura5 = 250
                    archivo = RANKING

                if event.type == pygame.MOUSEBUTTONDOWN and No.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.pantalla, NEGRO, (580, 150, 800, 650))
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN and self.superficie_boton_ranking.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.pantalla, NEGRO, (580, 150, 800, 650))
                    pygame.draw.rect(self.pantalla, NEGRO, (580, 150, 500, 450))
                    pygame.draw.rect(self.pantalla, AZUL, (580, 150, 500, 450), 5)
                    text1 = self.font.render("Posiciones", True, BLANCO)
                    self.pantalla.blit(text1, (700, 210))
                    with open(RANKING, "r") as archivo_ranking:
                        archivo_leer = archivo_ranking.read()
                    altura5 = 250
                    archivo = RANKING

                    with open(archivo, "r") as archivo:
                        ranking = []
                        for linea in archivo:
                            partes = linea.strip().rsplit(" ", 1)
                            if len(partes) == 2:
                                nombre = partes[0]
                                puntaje = int(partes[1])
                                ranking.append((nombre, puntaje))
                                ranking.sort(key=lambda x: x[1], reverse=True)
                        with open(RANKING_ORDEN, "w") as archivo_salida:
                            for nombre, puntaje in ranking:
                                archivo_salida.write(f"{nombre} - {puntaje}\n")

                        with open(RANKING_ORDEN, "r") as archivo_salida:
                            i = 0
                            posiciones = 1
                            for ranking_final in archivo_salida:
                                text1 = self.font.render(ranking_final, True, BLANCO)
                                self.pantalla.blit(text1, (700, altura5))
                                text1 = self.font.render(str(posiciones)+"  -", True, BLANCO)
                                self.pantalla.blit(text1, (650, altura5))
                                pygame.display.flip()
                                altura5 += 30
                                posiciones += 1
                                i += 1
                                if i == 10:
                                    break

                if event.type == pygame.MOUSEBUTTONDOWN and self.superficie_boton_salir.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and self.superficie_boton_inicio.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.pantalla, NEGRO, pygame.Rect(550, 150, 800, 550))
                    pygame.display.flip()
                    self.iniciar_juego()

            self.logica_juego()
        pygame.display.update()
