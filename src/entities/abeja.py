"""La abeja obrera que controla quien juega."""

import math

import pygame

from src.constants import config


class Abeja:
    """Abeja pecoreadora: vuela, junta néctar y lo lleva a la colmena.

    Además de la carga, arrastra dos "relojes biológicos":
      - energia: se agota volando; a 0 la abeja no puede seguir.
      - varroa: ácaro que se acumula y la vuelve lenta y con menos capacidad.
    """

    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.radio = config.ABEJA_RADIO
        self.capacidad_base = config.ABEJA_CAPACIDAD
        self.nectar = 0.0
        self.nectar_toxico = 0.0          # parte de la carga que viene del cultivo
        self.energia = float(config.ABEJA_ENERGIA_MAX)
        self.varroa = 0.0
        self.subletal = 0.0              # segundos restantes de desorientación
        self._fase_alas = 0.0
        self._ultimo_mov = pygame.Vector2(0, -1)

    # -- estado derivado ---------------------------------------------
    @property
    def rect(self):
        r = self.radio
        return pygame.Rect(self.pos.x - r, self.pos.y - r, r * 2, r * 2)

    @property
    def varroa_prop(self):
        return self.varroa / config.VARROA_MAX

    @property
    def velocidad(self):
        factor = 1.0 - config.VARROA_PENAL_VELOCIDAD * self.varroa_prop
        if self.energia <= 0:
            factor *= 0.35
        return config.ABEJA_VELOCIDAD * factor

    @property
    def capacidad(self):
        factor = 1.0 - config.VARROA_PENAL_CAPACIDAD * self.varroa_prop
        return self.capacidad_base * factor

    @property
    def llena(self):
        return self.nectar >= self.capacidad

    @property
    def desorientada(self):
        return self.subletal > 0

    @property
    def agotada(self):
        return self.energia <= 0

    # -- acciones ---------------------------------------------------
    def mover(self, direccion, viento, dt):
        """direccion: Vector2 normalizado (o cero). viento: Vector2 de empuje."""
        if self.desorientada and direccion.length_squared() > 0:
            # Efecto subletal de neonicotinoides: controles "torcidos".
            ang = math.sin(self.subletal * 6) * 1.2
            direccion = direccion.rotate_rad(ang)

        moviendo = direccion.length_squared() > 0
        self.pos += direccion * self.velocidad * dt * config.FPS
        self.pos += viento * dt * config.FPS
        self.pos.x = max(self.radio, min(config.ANCHO - self.radio, self.pos.x))
        self.pos.y = max(self.radio, min(config.ALTO - self.radio, self.pos.y))

        if moviendo:
            self._fase_alas += dt * 40
            self._ultimo_mov = direccion

        # Relojes biológicos
        gasto = config.ENERGIA_GASTO_VUELO if moviendo else config.ENERGIA_GASTO_QUIETA
        self.energia = max(0.0, self.energia - gasto * dt)
        self.varroa = min(config.VARROA_MAX, self.varroa + config.VARROA_POR_SEGUNDO * dt)
        if self.subletal > 0:
            self.subletal = max(0.0, self.subletal - dt)

    def sorber(self, cantidad, toxico=False):
        """Suma néctar sin pasar de la capacidad. Devuelve lo aceptado."""
        espacio = self.capacidad - self.nectar
        tomado = max(0.0, min(espacio, cantidad))
        self.nectar += tomado
        if toxico:
            self.nectar_toxico += tomado
        return tomado

    def descargar(self):
        """Vacía la carga en la colmena y recupera algo de energía / higiene.

        Devuelve (nectar_total, nectar_toxico).
        """
        total, toxico = self.nectar, self.nectar_toxico
        self.nectar = 0.0
        self.nectar_toxico = 0.0
        self.energia = min(config.ABEJA_ENERGIA_MAX,
                           self.energia + config.ENERGIA_RECUPERA_COLMENA)
        self.varroa = max(0.0, self.varroa - config.VARROA_LIMPIA_COLMENA)
        return total, toxico

    def robar_nectar(self, cantidad):
        """Una avispa le arranca néctar. Devuelve lo robado."""
        robado = min(self.nectar, cantidad)
        self.nectar -= robado
        self.nectar_toxico = min(self.nectar_toxico, self.nectar)
        return robado

    def soltar_carga(self):
        """Pierde toda la carga (susto de un ave)."""
        self.nectar = 0.0
        self.nectar_toxico = 0.0

    def limpiar_varroa(self, cantidad):
        self.varroa = max(0.0, self.varroa - cantidad)

    def intoxicar(self):
        self.subletal = config.SUBLETAL_DURACION

    # -- dibujo ---------------------------------------------------
    def dibujar(self, sup):
        x, y = int(self.pos.x), int(self.pos.y)

        bat = math.sin(self._fase_alas) * 4
        for signo in (-1, 1):
            ala = pygame.Rect(0, 0, 14, 9)
            ala.center = (x + signo * 8, y - 8 - bat)
            pygame.draw.ellipse(sup, config.ALA, ala)

        # Pelusa (la abeja es "peluda", la avispa no)
        pygame.draw.circle(sup, (250, 225, 150), (x, y), self.radio + 2)
        pygame.draw.circle(sup, config.AMARILLO_ABEJA, (x, y), self.radio)
        pygame.draw.circle(sup, config.NEGRO, (x, y), self.radio, 2)
        for dx in (-4, 3):
            pygame.draw.line(sup, config.NEGRO, (x + dx, y - 9), (x + dx, y + 9), 3)
        # Cabeza
        pygame.draw.circle(sup, config.NEGRO, (x, y - self.radio + 1), 4)

        # Ácaros de varroa: puntitos rojos según infestación
        for i in range(int(self.varroa_prop * 5)):
            ang = i * 2.3
            px = x + math.cos(ang) * (self.radio - 3)
            py = y + math.sin(ang) * (self.radio - 3)
            pygame.draw.circle(sup, config.VARROA_COLOR, (int(px), int(py)), 2)

        # Aura de desorientación
        if self.desorientada:
            pygame.draw.circle(sup, config.PESTICIDA_COLOR, (x, y), self.radio + 6, 2)
