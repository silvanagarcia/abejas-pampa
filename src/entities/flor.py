"""Flores nativas del Caldenal que ofrecen néctar."""

import math
import random

import pygame

from src.constants import config


class Flor:
    """Una mata florecida. Se vacía cuando la visitan y se recarga sola."""

    def __init__(self, x, y, especie):
        datos = config.FLORES[especie]
        self.pos = pygame.Vector2(x, y)
        self.especie = especie
        self.color = datos["color"]
        self.nectar_max = datos["nectar"]
        self.regen = datos["regen"]
        self.nectar = float(self.nectar_max)
        self.radio = config.FLOR_RADIO

    @property
    def rect(self):
        r = self.radio
        return pygame.Rect(self.pos.x - r, self.pos.y - r, r * 2, r * 2)

    @property
    def proporcion(self):
        return self.nectar / self.nectar_max if self.nectar_max else 0.0

    def actualizar(self, dt):
        if self.nectar < self.nectar_max:
            self.nectar = min(self.nectar_max, self.nectar + self.regen * dt)

    def extraer(self, cantidad):
        """Quita néctar de la flor. Devuelve lo que había disponible."""
        dado = min(self.nectar, cantidad)
        self.nectar -= dado
        return dado

    def dibujar(self, sup):
        x, y = int(self.pos.x), int(self.pos.y)
        # Tallo
        pygame.draw.line(sup, (90, 140, 70), (x, y), (x, y + self.radio + 10), 3)
        # Pétalos: más pálidos cuanto menos néctar queda
        p = 0.35 + 0.65 * self.proporcion
        color = tuple(int(c * p) for c in self.color)
        for i in range(6):
            ang = math.pi / 3 * i
            px = x + math.cos(ang) * self.radio
            py = y + math.sin(ang) * self.radio
            pygame.draw.circle(sup, color, (int(px), int(py)), 7)
        # Centro
        pygame.draw.circle(sup, (110, 80, 40), (x, y), 6)


def generar_flores(cantidad, evitar_rect):
    """Ubica flores al azar sin pisar la colmena ni los bordes."""
    especies = list(config.FLORES.keys())
    flores = []
    margen = 60
    intentos = 0
    while len(flores) < cantidad and intentos < cantidad * 40:
        intentos += 1
        x = random.randint(margen, config.ANCHO - margen)
        y = random.randint(margen + 40, config.ALTO - margen)
        candidata = pygame.Rect(x - 40, y - 40, 80, 80)
        if evitar_rect.colliderect(candidata):
            continue
        if any(f.rect.inflate(50, 50).collidepoint(x, y) for f in flores):
            continue
        flores.append(Flor(x, y, random.choice(especies)))
    return flores
