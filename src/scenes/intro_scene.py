"""Pantalla de inicio: explica el objetivo del juego."""

import math

import pygame

from src.constants import config


class IntroScene:
    def __init__(self):
        self.proxima = None
        self.titulo_f = pygame.font.SysFont("consolas,menlo,monospace", 52, bold=True)
        self.sub_f = pygame.font.SysFont("consolas,menlo,monospace", 20)
        self.f = pygame.font.SysFont("consolas,menlo,monospace", 18)
        self.chico_f = pygame.font.SysFont("consolas,menlo,monospace", 15)
        self.t = 0.0

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
            from src.scenes.game_scene import GameScene
            self.proxima = GameScene()

    def actualizar(self, dt):
        self.t += dt

    def dibujar(self, sup):
        sup.fill(config.CIELO)
        pygame.draw.rect(sup, config.PASTIZAL, (0, 360, config.ANCHO, config.ALTO - 360))
        cx = config.ANCHO // 2

        # Abeja que revolotea sobre el título
        bx = cx + math.sin(self.t * 2) * 120
        by = 150 + math.cos(self.t * 3) * 12
        self._abeja(sup, int(bx), int(by))

        titulo = self.titulo_f.render("Abejas de la Pampa", True, (60, 45, 20))
        sup.blit(titulo, titulo.get_rect(center=(cx, 235)))

        sub = self.sub_f.render("Pecoreo en el Caldenal — una jornada de una abeja obrera",
                                True, (70, 60, 35))
        sup.blit(sub, sub.get_rect(center=(cx, 278)))

        lineas = [
            "Sos una abeja obrera. Volá por el Monte pampeano y juntá néctar de las",
            "flores nativas (caldén, chañar, piquillín, jarilla). Llevalo a la colmena:",
            "ahí se transforma en miel, recuperás energía y te sacás la varroa.",
            "",
            f"OBJETIVO DEL DÍA:  cosechar  {config.META_MIEL_G} g de miel  para llevar a la venta.",
            "",
            "Cuidado con las avispas (te roban), el benteveo (te tira la carga) y la",
            "deriva de pesticida del cultivo (te desorienta). El viento también molesta.",
        ]
        y = 330
        for ln in lineas:
            col = (150, 90, 30) if ln.startswith("OBJETIVO") else (45, 40, 25)
            sup.blit(self.f.render(ln, True, col), self.f.render(ln, True, col).get_rect(center=(cx, y)))
            y += 26

        if int(self.t * 2) % 2 == 0:
            call = self.sub_f.render("ENTER para empezar", True, (30, 25, 15))
            sup.blit(call, call.get_rect(center=(cx, 560)))

        pie = self.chico_f.render("Flechas o WASD para volar  ·  H = ayuda en el juego  ·  ESC para salir",
                                  True, (60, 55, 40))
        sup.blit(pie, pie.get_rect(center=(cx, 605)))

    def _abeja(self, sup, x, y):
        pygame.draw.ellipse(sup, config.ALA, (x - 16, y - 14, 14, 10))
        pygame.draw.ellipse(sup, config.ALA, (x + 2, y - 14, 14, 10))
        pygame.draw.circle(sup, (250, 225, 150), (x, y), 15)
        pygame.draw.circle(sup, config.AMARILLO_ABEJA, (x, y), 13)
        pygame.draw.circle(sup, config.NEGRO, (x, y), 13, 3)
        for dx in (-5, 3):
            pygame.draw.line(sup, config.NEGRO, (x + dx, y - 11), (x + dx, y + 11), 4)
