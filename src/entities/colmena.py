"""La colmena: donde la abeja descarga el néctar y se transforma en miel."""

import pygame

from src.constants import config


class Colmena:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, config.COLMENA_ANCHO, config.COLMENA_ALTO)
        self.rect.center = (x, y)
        self.miel = 0.0

    def recibir(self, nectar):
        """Convierte néctar en miel y lo acumula. Devuelve la miel sumada."""
        sumado = nectar * config.NECTAR_A_MIEL
        self.miel += sumado
        return sumado

    def dibujar(self, sup):
        r = self.rect
        # Cuerpo tipo caja Langstroth con franjas
        pygame.draw.rect(sup, config.COLMENA_COLOR, r, border_radius=6)
        pygame.draw.rect(sup, config.NEGRO, r, 2, border_radius=6)
        for i in range(1, 4):
            y = r.top + i * r.height // 4
            pygame.draw.line(sup, config.NEGRO, (r.left, y), (r.right, y), 1)
        # Piquera (entrada)
        entrada = pygame.Rect(0, 0, 26, 10)
        entrada.midbottom = (r.centerx, r.bottom - 6)
        pygame.draw.rect(sup, config.COLMENA_ENTRADA, entrada, border_radius=3)
        # Techo
        techo = [(r.left - 6, r.top), (r.right + 6, r.top), (r.centerx, r.top - 16)]
        pygame.draw.polygon(sup, (120, 90, 50), techo)
        pygame.draw.polygon(sup, config.NEGRO, techo, 2)
