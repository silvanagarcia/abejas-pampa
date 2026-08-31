"""Dibujo del HUD: néctar, energía, varroa, miel, tiempo, brújula y avisos."""

import pygame

from src.constants import config


class HUD:
    def __init__(self):
        self.fuente = pygame.font.SysFont("consolas,menlo,monospace", 18)
        self.fuente_grande = pygame.font.SysFont("consolas,menlo,monospace", 44, bold=True)

    # -- barra genérica ------------------------------------------------
    def _barra(self, sup, x, y, ancho, prop, color, etiqueta):
        pygame.draw.rect(sup, (255, 255, 255), (x, y, ancho + 4, 16), 2)
        pygame.draw.rect(sup, color, (x + 2, y + 2, int(ancho * max(0, min(1, prop))), 12))
        sup.blit(self.fuente.render(etiqueta, True, config.BLANCO), (x + ancho + 12, y - 1))

    def dibujar(self, sup, abeja, colmena, tiempo_restante, colmena_dir,
                sequia, aviso, sin_energia_t):
        franja = pygame.Surface((config.ANCHO, 70), pygame.SRCALPHA)
        franja.fill((0, 0, 0, 140))
        sup.blit(franja, (0, 0))

        # Néctar
        etiqueta = "¡LLENA! volvé a la colmena" if abeja.llena else "néctar"
        self._barra(sup, 12, 8, 150, abeja.nectar / abeja.capacidad,
                    config.BARRA_LLENA if abeja.llena else config.BARRA_NECTAR, etiqueta)

        # Energía
        e_prop = abeja.energia / config.ABEJA_ENERGIA_MAX
        e_color = config.BARRA_ENERGIA if e_prop > 0.3 else config.BARRA_ENERGIA_BAJA
        self._barra(sup, 12, 28, 150, e_prop, e_color, "energía")

        # Varroa
        if abeja.varroa > 1:
            self._barra(sup, 12, 48, 150, abeja.varroa_prop, config.VARROA_COLOR, "varroa")

        # Miel
        sup.blit(self.fuente.render(f"miel: {colmena.miel:6.1f} g", True, config.BLANCO),
                 (config.ANCHO // 2 - 55, 10))

        # Tiempo + sequía
        seg = max(0, int(tiempo_restante))
        sup.blit(self.fuente.render(f"{seg // 60}:{seg % 60:02d}", True, config.BLANCO),
                 (config.ANCHO - 60, 10))
        if sequia:
            sup.blit(self.fuente.render("SEQUÍA", True, (240, 200, 120)),
                     (config.ANCHO - 130, 32))

        # Brújula a la colmena
        self._brujula(sup, abeja, colmena_dir)

        # Aviso efímero
        if aviso:
            txt = self.fuente.render(aviso, True, (60, 30, 10))
            fondo = txt.get_rect(center=(config.ANCHO // 2, 92)).inflate(16, 8)
            pygame.draw.rect(sup, (255, 230, 120), fondo, border_radius=5)
            sup.blit(txt, txt.get_rect(center=(config.ANCHO // 2, 92)))

        # Alerta de energía agotada
        if sin_energia_t > 0:
            queda = max(0, 6.0 - sin_energia_t)
            txt = self.fuente.render(
                f"¡SIN ENERGÍA! llegá a la colmena ({queda:0.1f}s)", True, (255, 120, 110))
            sup.blit(txt, txt.get_rect(center=(config.ANCHO // 2, config.ALTO - 24)))

    def _brujula(self, sup, abeja, colmena_dir):
        cx, cy = config.ANCHO - 40, config.ALTO - 60
        pygame.draw.circle(sup, (0, 0, 0, 120), (cx, cy), 20)
        pygame.draw.circle(sup, config.BLANCO, (cx, cy), 20, 2)
        if colmena_dir is None:
            t = self.fuente.render("?", True, (255, 120, 110))
            sup.blit(t, t.get_rect(center=(cx, cy)))
        elif colmena_dir.length_squared() > 0:
            p = colmena_dir * 14
            pygame.draw.line(sup, config.COLMENA_COLOR, (cx, cy), (cx + p.x, cy + p.y), 4)
            pygame.draw.circle(sup, config.COLMENA_COLOR, (int(cx + p.x), int(cy + p.y)), 4)

    def pista_ayuda(self, sup):
        t = self.fuente.render("H = ¿qué es cada cosa?", True, (255, 255, 255))
        fondo = t.get_rect(bottomleft=(10, config.ALTO - 8)).inflate(10, 6)
        capa = pygame.Surface(fondo.size, pygame.SRCALPHA)
        capa.fill((0, 0, 0, 120))
        sup.blit(capa, fondo.topleft)
        sup.blit(t, t.get_rect(bottomleft=(15, config.ALTO - 11)))

    def cartel_final(self, sup, colmena, miel_final, motivo):
        capa = pygame.Surface((config.ANCHO, config.ALTO), pygame.SRCALPHA)
        capa.fill((0, 0, 0, 175))
        sup.blit(capa, (0, 0))
        cx = config.ANCHO // 2

        titulo = self.fuente_grande.render("Fin de la jornada", True, config.BLANCO)
        sup.blit(titulo, titulo.get_rect(center=(cx, config.ALTO // 2 - 80)))

        sup.blit(self.fuente.render(motivo, True, (230, 200, 160)),
                 self.fuente.render(motivo, True, (230, 200, 160)).get_rect(center=(cx, config.ALTO // 2 - 40)))

        bruto = self.fuente.render(f"miel cosechada: {colmena.miel:.1f} g", True, config.BLANCO)
        sup.blit(bruto, bruto.get_rect(center=(cx, config.ALTO // 2 - 6)))

        penal = colmena.miel - miel_final
        if penal > 0.05:
            p = self.fuente.render(f"− {penal:.1f} g por néctar contaminado", True, (220, 150, 210))
            sup.blit(p, p.get_rect(center=(cx, config.ALTO // 2 + 18)))

        neto = self.fuente_grande.render(f"{miel_final:.1f} g", True, config.BARRA_NECTAR)
        sup.blit(neto, neto.get_rect(center=(cx, config.ALTO // 2 + 58)))

        ayuda = self.fuente.render("R para jugar de nuevo   ·   ESC para salir", True, config.BLANCO)
        sup.blit(ayuda, ayuda.get_rect(center=(cx, config.ALTO // 2 + 100)))
