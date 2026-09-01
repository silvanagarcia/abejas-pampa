"""Depredadores del Caldenal: chaqueta amarilla y benteveo."""

import random

import pygame

from src.constants import config


class Avispa:
    """Chaqueta amarilla (Vespula germanica).

    Invasora. Persigue a la abeja cuando lleva carga y le roba néctar por
    contacto; después huye un rato. Si la abeja va vacía, merodea.
    """

    def __init__(self):
        borde = random.choice(("arriba", "abajo", "izq", "der"))
        if borde == "arriba":
            self.pos = pygame.Vector2(random.uniform(0, config.ANCHO), -20)
        elif borde == "abajo":
            self.pos = pygame.Vector2(random.uniform(0, config.ANCHO), config.ALTO + 20)
        elif borde == "izq":
            self.pos = pygame.Vector2(-20, random.uniform(0, config.ALTO))
        else:
            self.pos = pygame.Vector2(config.ANCHO + 20, random.uniform(0, config.ALTO))
        self.radio = config.AVISPA_RADIO
        self.huida = 0.0
        self._deriva = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
        self._t_deriva = 0.0

    @property
    def rect(self):
        r = self.radio
        return pygame.Rect(self.pos.x - r, self.pos.y - r, r * 2, r * 2)

    def actualizar(self, dt, abeja):
        objetivo = None
        if self.huida > 0:
            self.huida -= dt
        elif abeja.nectar > 0:
            objetivo = abeja.pos

        if objetivo is not None:
            direccion = (objetivo - self.pos)
            if direccion.length_squared() > 1:
                direccion = direccion.normalize()
        else:
            self._t_deriva += dt
            if self._t_deriva > 2.0:
                self._t_deriva = 0.0
                self._deriva = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
            direccion = self._deriva

        self.pos += direccion * config.AVISPA_VELOCIDAD * dt * config.FPS
        self.pos.x = max(-40, min(config.ANCHO + 40, self.pos.x))
        self.pos.y = max(-40, min(config.ALTO + 40, self.pos.y))

        if self.huida <= 0 and self.rect.colliderect(abeja.rect) and abeja.nectar > 0:
            robado = abeja.robar_nectar(config.AVISPA_ROBO)
            self.huida = 2.5
            return robado
        return 0.0

    def dibujar(self, sup):
        x, y = int(self.pos.x), int(self.pos.y)
        # Alas hacia atrás
        pygame.draw.ellipse(sup, config.ALA, (x - 14, y - 11, 12, 7))
        pygame.draw.ellipse(sup, config.ALA, (x + 2, y - 11, 12, 7))
        # Antenas
        pygame.draw.line(sup, config.NEGRO, (x - 2, y - 8), (x - 6, y - 14), 1)
        pygame.draw.line(sup, config.NEGRO, (x + 2, y - 8), (x + 6, y - 14), 1)
        # Tórax + abdomen alargado con cintura (avispa, no abeja)
        pygame.draw.circle(sup, config.AVISPA_COLOR, (x, y - 4), 5)
        abdomen = pygame.Rect(0, 0, 12, 18)
        abdomen.center = (x, y + 6)
        pygame.draw.ellipse(sup, config.AVISPA_COLOR, abdomen)
        pygame.draw.ellipse(sup, config.NEGRO, abdomen, 2)
        for dy in (2, 8, 14):
            pygame.draw.line(sup, config.NEGRO, (x - 6, y + dy - 4), (x + 6, y + dy - 4), 2)
        # Aguijón
        pygame.draw.line(sup, config.NEGRO, (x, y + 15), (x, y + 19), 2)


class Ave:
    """Benteveo: hace pasadas horizontales rápidas.

    Su sombra sobre el pasto avisa ~1 s antes de la pasada, así se puede
    esquivar. Si engancha a la abeja durante la pasada, le tira la carga.
    """

    ESPERA, AVISO, PASADA = range(3)

    def __init__(self, factor_frecuencia=1.0):
        self.estado = Ave.ESPERA
        self._factor = factor_frecuencia
        self.t = random.uniform(*config.AVE_CADA) * self._factor
        self.y = 0.0
        self.dir = 1
        self.pos = pygame.Vector2(-100, -100)
        self.golpeo = False

    def _arranca(self, abeja):
        self.y = abeja.pos.y
        if abeja.pos.x < config.ANCHO / 2:
            self.dir = 1
            self.pos = pygame.Vector2(-60, self.y)
        else:
            self.dir = -1
            self.pos = pygame.Vector2(config.ANCHO + 60, self.y)
        self.golpeo = False

    def actualizar(self, dt, abeja):
        self.t -= dt
        if self.estado == Ave.ESPERA:
            if self.t <= 0:
                self.estado = Ave.AVISO
                self.t = config.AVE_AVISO
                self._arranca(abeja)
        elif self.estado == Ave.AVISO:
            if self.t <= 0:
                self.estado = Ave.PASADA
        elif self.estado == Ave.PASADA:
            self.pos.x += self.dir * config.AVE_VELOCIDAD * dt * config.FPS
            if not self.golpeo and self._rect().colliderect(abeja.rect):
                abeja.soltar_carga()
                self.golpeo = True
            if self.pos.x < -80 or self.pos.x > config.ANCHO + 80:
                self.estado = Ave.ESPERA
                self.t = random.uniform(*config.AVE_CADA) * self._factor

    def _rect(self):
        return pygame.Rect(self.pos.x - 16, self.y - 10, 32, 20)

    def dibujar(self, sup):
        if self.estado == Ave.ESPERA:
            return
        if self.estado == Ave.AVISO:
            # Sombra que corre por el pasto anticipando la trayectoria
            sx = 40 if self.dir == 1 else config.ANCHO - 40
            capa = pygame.Surface((60, 22), pygame.SRCALPHA)
            pygame.draw.ellipse(capa, (*config.SOMBRA_COLOR, 120), capa.get_rect())
            sup.blit(capa, (sx - 30, self.y - 11))
            return
        x, y = int(self.pos.x), int(self.y)
        cuerpo = [(x - 16 * self.dir, y), (x + 10 * self.dir, y - 7), (x + 10 * self.dir, y + 7)]
        pygame.draw.polygon(sup, config.AVE_COLOR, cuerpo)
        pygame.draw.circle(sup, config.AVE_COLOR, (x + 10 * self.dir, y), 7)
        pygame.draw.polygon(sup, (240, 210, 80),
                            [(x + 14 * self.dir, y), (x + 20 * self.dir, y - 3), (x + 20 * self.dir, y + 3)])
