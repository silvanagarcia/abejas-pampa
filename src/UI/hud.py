"""Dibujo del HUD: carga de néctar, miel y tiempo."""

import pygame

from src.constants import config


class HUD:
    def __init__(self):
        self.fuente = pygame.font.SysFont("consolas,menlo,monospace", 20)
        self.fuente_grande = pygame.font.SysFont("consolas,menlo,monospace", 48, bold=True)

    def dibujar(self, sup, abeja, colmena, tiempo_restante):
        barra = pygame.Surface((config.ANCHO, 40), pygame.SRCALPHA)
        barra.fill((0, 0, 0, 140))
        sup.blit(barra, (0, 0))

        # Barra de néctar
        pygame.draw.rect(sup, (255, 255, 255), (12, 10, 204, 20), 2)
        prop = abeja.nectar / abeja.capacidad
        color = config.BARRA_LLENA if abeja.llena else config.BARRA_NECTAR
        pygame.draw.rect(sup, color, (14, 12, int(200 * prop), 16))
        etiqueta = "¡LLENA! volvé a la colmena" if abeja.llena else "néctar"
        sup.blit(self.fuente.render(etiqueta, True, config.BLANCO), (224, 8))

        # Miel
        miel_txt = self.fuente.render(f"miel: {colmena.miel:6.1f} g", True, config.BLANCO)
        sup.blit(miel_txt, (config.ANCHO // 2 - 60, 8))

        # Tiempo
        seg = max(0, int(tiempo_restante))
        t_txt = self.fuente.render(f"{seg // 60}:{seg % 60:02d}", True, config.BLANCO)
        sup.blit(t_txt, (config.ANCHO - 70, 8))

    def cartel_final(self, sup, colmena):
        capa = pygame.Surface((config.ANCHO, config.ALTO), pygame.SRCALPHA)
        capa.fill((0, 0, 0, 170))
        sup.blit(capa, (0, 0))

        titulo = self.fuente_grande.render("Fin de la jornada", True, config.BLANCO)
        sup.blit(titulo, titulo.get_rect(center=(config.ANCHO // 2, config.ALTO // 2 - 60)))

        resumen = self.fuente.render(
            f"Cosechaste {colmena.miel:.1f} g de miel del Caldenal", True, config.BARRA_NECTAR
        )
        sup.blit(resumen, resumen.get_rect(center=(config.ANCHO // 2, config.ALTO // 2)))

        ayuda = self.fuente.render("R para jugar de nuevo   ·   ESC para salir", True, config.BLANCO)
        sup.blit(ayuda, ayuda.get_rect(center=(config.ANCHO // 2, config.ALTO // 2 + 50)))
