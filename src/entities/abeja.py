"""La abeja obrera que controla quien juega."""

import math

import pygame

from src.constants import config


class Abeja:
    """Abeja pecoreadora: vuela, junta néctar y lo lleva a la colmena."""

    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.radio = config.ABEJA_RADIO
        self.velocidad = config.ABEJA_VELOCIDAD
        self.capacidad = config.ABEJA_CAPACIDAD
        self.nectar = 0.0
        self._fase_alas = 0.0

    @property
    def rect(self):
        r = self.radio
        return pygame.Rect(self.pos.x - r, self.pos.y - r, r * 2, r * 2)

    @property
    def llena(self):
        return self.nectar >= self.capacidad

    def mover(self, direccion, dt):
        """direccion: Vector2 ya normalizado (o cero)."""
        self.pos += direccion * self.velocidad * dt * config.FPS
        self.pos.x = max(self.radio, min(config.ANCHO - self.radio, self.pos.x))
        self.pos.y = max(self.radio, min(config.ALTO - self.radio, self.pos.y))
        if direccion.length_squared() > 0:
            self._fase_alas += dt * 40

    def sorber(self, cantidad):
        """Suma néctar sin pasar de la capacidad. Devuelve lo aceptado."""
        espacio = self.capacidad - self.nectar
        tomado = min(espacio, cantidad)
        self.nectar += tomado
        return tomado

    def descargar(self):
        """Vacía la carga y devuelve cuánto néctar traía."""
        traido = self.nectar
        self.nectar = 0.0
        return traido

    def dibujar(self, sup):
        x, y = int(self.pos.x), int(self.pos.y)

        # Alas (aletean con una onda seno)
        bat = math.sin(self._fase_alas) * 4
        for signo in (-1, 1):
            ala = pygame.Rect(0, 0, 14, 9)
            ala.center = (x + signo * 8, y - 8 - bat)
            pygame.draw.ellipse(sup, config.ALA, ala)

        # Cuerpo
        pygame.draw.circle(sup, config.AMARILLO_ABEJA, (x, y), self.radio)
        pygame.draw.circle(sup, config.NEGRO, (x, y), self.radio, 2)
        # Rayas
        for dx in (-4, 3):
            pygame.draw.line(sup, config.NEGRO, (x + dx, y - 9), (x + dx, y + 9), 3)
