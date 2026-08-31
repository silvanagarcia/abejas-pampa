"""Dibujo del HUD: néctar, energía, varroa, avance hacia la meta, tiempo..."""

import pygame

from src.constants import config


class HUD:
    def __init__(self):
        self.fuente = pygame.font.SysFont("consolas,menlo,monospace", 18)

    # -- barra genérica ------------------------------------------------
    def _barra(self, sup, x, y, ancho, prop, color, etiqueta):
        pygame.draw.rect(sup, (255, 255, 255), (x, y, ancho + 4, 16), 2)
        pygame.draw.rect(sup, color, (x + 2, y + 2, int(ancho * max(0, min(1, prop))), 12))
        sup.blit(self.fuente.render(etiqueta, True, config.BLANCO), (x + ancho + 12, y - 1))

    def dibujar(self, sup, abeja, miel_neta, meta, tiempo_restante, colmena_dir,
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

        # Avance hacia la meta del día
        cx = config.ANCHO // 2
        bx, bw = cx - 140, 300
        sup.blit(self.fuente.render(f"miel del día:  {miel_neta:.0f} / {meta:.0f} g",
                                    True, config.BLANCO), (bx, 8))
        pygame.draw.rect(sup, (255, 255, 255), (bx, 32, bw + 4, 16), 2)
        prop = max(0.0, min(1.0, miel_neta / meta)) if meta else 0.0
        pygame.draw.rect(sup, config.BARRA_META, (bx + 2, 34, int(bw * prop), 12))

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
