"""Elementos del ambiente: viento pampeano y deriva de pesticida del cultivo."""

import math
import random

import pygame

from src.constants import config


class RachaVisual:
    """Una racha de viento visible: una estela que cruza la pantalla."""

    def __init__(self, vector):
        diagonal = pygame.Vector2(config.ANCHO, config.ALTO).length()
        direccion = vector.normalize() if vector.length_squared() > 0 else pygame.Vector2(1, 0)
        perp = pygame.Vector2(-direccion.y, direccion.x)
        centro = pygame.Vector2(config.ANCHO / 2, config.ALTO / 2)
        lateral = perp * random.uniform(-diagonal / 2, diagonal / 2)
        atras = -direccion * (diagonal / 2 + 40)
        self.pos = centro + lateral + atras
        self.vida = random.uniform(1.0, 1.8)
        self.edad = 0.0

    def actualizar(self, dt, vector):
        self.pos += vector * dt * config.FPS * 6   # más rápido que el empuje real: se nota
        self.edad += dt

    def viva(self):
        return self.edad < self.vida

    def dibujar(self, sup, vector):
        if vector.length_squared() < 0.02:
            return
        direccion = vector.normalize()
        largo = 16 + vector.length() * 10
        p1 = self.pos - direccion * largo
        prop = max(0.0, 1 - self.edad / self.vida)
        color = tuple(int(config.CIELO[i] + (255 - config.CIELO[i]) * prop * 0.8) for i in range(3))
        pygame.draw.line(sup, color, p1, self.pos, 2)


class Viento:
    """Ráfaga que empuja a la abeja y cambia de dirección cada tanto.

    Arranca con una ráfaga ya activa (no en calma) para que se note desde
    el primer segundo del nivel, no recién sobre el final.
    """

    def __init__(self, factor=1.0, rango_cambio=None):
        self.factor = factor        # 1.0 normal; la sequía y el nivel lo suben
        self.rango_cambio = rango_cambio or config.VIENTO_CAMBIA_CADA
        fuerza = random.uniform(0, config.VIENTO_FUERZA_MAX) * self.factor
        ang = random.uniform(0, 360)
        self.vector = pygame.Vector2(fuerza, 0).rotate(ang)
        self._t = 0.0
        self._proximo = random.uniform(*self.rango_cambio)
        self.rachas = []
        self._spawn_t = 0.0

    def actualizar(self, dt):
        self._t += dt
        if self._t >= self._proximo:
            self._t = 0.0
            self._proximo = random.uniform(*self.rango_cambio)
            fuerza = random.uniform(0, config.VIENTO_FUERZA_MAX) * self.factor
            ang = random.uniform(0, 360)
            self.vector = pygame.Vector2(fuerza, 0).rotate(ang)

        intensidad = self.vector.length() / config.VIENTO_FUERZA_MAX
        if intensidad > 0.08:
            self._spawn_t += dt
            cada = max(0.05, 0.5 - intensidad * 0.4)
            if self._spawn_t >= cada:
                self._spawn_t = 0.0
                self.rachas.append(RachaVisual(self.vector))

        for racha in self.rachas:
            racha.actualizar(dt, self.vector)
        self.rachas = [r for r in self.rachas if r.viva()]

    def dibujar(self, sup, fuente):
        for racha in self.rachas:
            racha.dibujar(sup, self.vector)

        if self.vector.length_squared() < 0.02:
            return
        cx, cy = config.ANCHO - 130, config.ALTO - 26
        intensidad = self.vector.length() / config.VIENTO_FUERZA_MAX
        largo = 14 + self.vector.length() * 8
        d = self.vector.normalize() * largo
        pygame.draw.line(sup, config.BLANCO, (cx, cy), (cx + d.x, cy + d.y), 3)
        pygame.draw.circle(sup, config.BLANCO, (int(cx + d.x), int(cy + d.y)), 3)
        nivel = "suave" if intensidad < 0.4 else ("fuerte" if intensidad < 0.75 else "¡RÁFAGA!")
        sup.blit(fuente.render(f"viento {nivel}", True, config.BLANCO), (cx - 95, cy - 8))


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
