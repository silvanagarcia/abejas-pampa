"""Elementos del ambiente: viento pampeano y deriva de pesticida del cultivo."""

import math
import random

import pygame

from src.constants import config


class Viento:
    """Ráfaga que empuja a la abeja y cambia de dirección cada tanto."""

    def __init__(self):
        self.vector = pygame.Vector2(0, 0)
        self._t = 0.0
        self._proximo = random.uniform(*config.VIENTO_CAMBIA_CADA)
        self.factor = 1.0        # 1.0 normal; la sequía lo sube

    def actualizar(self, dt):
        self._t += dt
        if self._t >= self._proximo:
            self._t = 0.0
            self._proximo = random.uniform(*config.VIENTO_CAMBIA_CADA)
            fuerza = random.uniform(0, config.VIENTO_FUERZA_MAX) * self.factor
            ang = random.uniform(0, 360)
            self.vector = pygame.Vector2(fuerza, 0).rotate(ang)

    def dibujar(self, sup, fuente):
        if self.vector.length_squared() < 0.02:
            return
        cx, cy = config.ANCHO - 130, config.ALTO - 26
        d = self.vector.normalize() * 16
        pygame.draw.line(sup, config.BLANCO, (cx, cy), (cx + d.x, cy + d.y), 3)
        pygame.draw.circle(sup, config.BLANCO, (int(cx + d.x), int(cy + d.y)), 3)
        sup.blit(fuente.render("viento", True, config.BLANCO), (cx - 60, cy - 8))


class Cultivo:
    """Franja agrícola al costado del mapa y sus nubes de deriva."""

    def __init__(self):
        self.rect = pygame.Rect(config.ANCHO - config.CULTIVO_ANCHO, 0,
                                config.CULTIVO_ANCHO, config.ALTO)
        self.fuente = pygame.font.SysFont("consolas,menlo,monospace", 13, bold=True)
        self.nubes = [NubePesticida(self.rect) for _ in range(2)]

    def actualizar(self, dt):
        for n in self.nubes:
            n.actualizar(dt)

    def golpea(self, abeja):
        return any(n.contiene(abeja.pos) for n in self.nubes)

    def dibujar(self, sup):
        capa = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        capa.fill((*config.CULTIVO_COLOR, 90))
        sup.blit(capa, self.rect.topleft)
        pygame.draw.line(sup, (120, 110, 70),
                         (self.rect.left, 0), (self.rect.left, config.ALTO), 2)
        rot = self.fuente.render("CULTIVO", True, (90, 80, 40))
        rot = pygame.transform.rotate(rot, 90)
        sup.blit(rot, (self.rect.left + 4, 140))
        for n in self.nubes:
            n.dibujar(sup, self.fuente)


class NubePesticida:
    """Nube de agroquímico que deriva lento. Causa efecto subletal."""

    def __init__(self, zona):
        self.zona = zona
        self.radio = config.PESTICIDA_RADIO
        self.pos = pygame.Vector2(random.uniform(zona.left, zona.right),
                                  random.uniform(150, zona.bottom - 60))
        self.vel = pygame.Vector2(config.PESTICIDA_VELOCIDAD, 0).rotate(random.uniform(0, 360))

    def actualizar(self, dt):
        self.pos += self.vel * dt * config.FPS
        # Rebota dentro de una banda un poco más ancha que el cultivo
        izq = self.zona.left - 80
        if not (izq <= self.pos.x <= self.zona.right):
            self.vel.x *= -1
        if not (130 <= self.pos.y <= config.ALTO - 20):
            self.vel.y *= -1
        self.pos.x = max(izq, min(self.zona.right, self.pos.x))
        self.pos.y = max(130, min(config.ALTO - 20, self.pos.y))

    def contiene(self, punto):
        return self.pos.distance_to(punto) <= self.radio

    def dibujar(self, sup, fuente):
        d = self.radio * 2
        capa = pygame.Surface((d, d), pygame.SRCALPHA)
        c = (self.radio, self.radio)
        pygame.draw.circle(capa, (*config.PESTICIDA_COLOR, 140), c, self.radio)
        pygame.draw.circle(capa, (60, 25, 80), c, self.radio, 3)
        for i in range(9):
            a = i * 1.9 + self.pos.x * 0.02
            rr = self.radio * (0.3 + 0.55 * ((i * 7) % 5) / 5)
            px = self.radio + math.cos(a) * rr
            py = self.radio + math.sin(a) * rr
            pygame.draw.circle(capa, (245, 220, 250), (int(px), int(py)), 3)
        sup.blit(capa, (self.pos.x - self.radio, self.pos.y - self.radio))

        etiqueta = fuente.render("PESTICIDA", True, (255, 255, 255))
        fondo = etiqueta.get_rect(center=(self.pos.x, self.pos.y)).inflate(8, 4)
        pygame.draw.rect(sup, (70, 30, 90), fondo, border_radius=3)
        sup.blit(etiqueta, etiqueta.get_rect(center=(self.pos.x, self.pos.y)))
