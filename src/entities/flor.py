"""Flores del mapa: nativas del Caldenal y flores del cultivo (tóxicas)."""

import math
import random

import pygame

from src.constants import config


class Flor:
    """Una mata florecida. Se vacía cuando la visitan y se recarga sola.

    Si `toxica`, su néctar viene contaminado con agroquímico: suma miel
    pero penaliza a la colonia al final de la ronda.
    """

    def __init__(self, x, y, especie, toxica=False):
        self.pos = pygame.Vector2(x, y)
        self.especie = especie
        self.toxica = toxica
        if toxica:
            self.color = (150, 170, 90)
            self.nectar_max = config.FLOR_TOXICA_NECTAR
            self.regen = config.FLOR_TOXICA_REGEN
        else:
            datos = config.FLORES[especie]
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
        dado = min(self.nectar, cantidad)
        self.nectar -= dado
        return dado

    def dibujar(self, sup):
        x, y = int(self.pos.x), int(self.pos.y)
        pygame.draw.line(sup, (90, 140, 70), (x, y), (x, y + self.radio + 10), 3)
        p = 0.35 + 0.65 * self.proporcion
        color = tuple(int(c * p) for c in self.color)
        for i in range(6):
            ang = math.pi / 3 * i
            px = x + math.cos(ang) * self.radio
            py = y + math.sin(ang) * self.radio
            pygame.draw.circle(sup, color, (int(px), int(py)), 7)
        centro = (120, 60, 120) if self.toxica else (110, 80, 40)
        pygame.draw.circle(sup, centro, (x, y), 6)
        if self.toxica:
            pygame.draw.circle(sup, config.PESTICIDA_COLOR, (x, y), self.radio + 3, 1)


def generar_campo(evitar_rect, cultivo_rect):
    """Devuelve la lista de flores: nativas en el Monte + tóxicas en el cultivo."""
    especies = list(config.FLORES.keys())
    flores = []
    margen = 75

    def libre(x, y):
        c = pygame.Rect(x - 40, y - 40, 80, 80)
        if evitar_rect.colliderect(c):
            return False
        return not any(f.rect.inflate(46, 46).collidepoint(x, y) for f in flores)

    # Flores nativas en el Monte (fuera de la franja de cultivo)
    intentos = 0
    while len(flores) < config.CANTIDAD_FLORES and intentos < config.CANTIDAD_FLORES * 50:
        intentos += 1
        x = random.randint(margen, cultivo_rect.left - margen)
        y = random.randint(margen + 40, config.ALTO - margen)
        if libre(x, y):
            flores.append(Flor(x, y, random.choice(especies)))

    # Flores tóxicas dentro del cultivo
    for _ in range(3):
        x = random.randint(cultivo_rect.left + 30, cultivo_rect.right - 30)
        y = random.randint(margen + 40, config.ALTO - margen)
        flores.append(Flor(x, y, "cultivo", toxica=True))

    return flores
