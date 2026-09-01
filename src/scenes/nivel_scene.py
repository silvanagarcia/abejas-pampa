"""Pantalla breve entre niveles: muestra el progreso acumulado hacia la meta global."""

import pygame

from src.constants import config


class NivelScene:
    """Se muestra al superar un nivel (menos el último). ENTER pasa al siguiente."""

    def __init__(self, nivel_completado_idx, progreso, siguiente_nivel_idx):
        self.progreso = progreso
        self.siguiente_nivel_idx = siguiente_nivel_idx
        self.nombre_completado = config.NIVELES[nivel_completado_idx]["nombre"]
        self.siguiente = config.NIVELES[siguiente_nivel_idx]
        self.proxima = None
        self.t = 0.0
        self.titulo_f = pygame.font.SysFont("consolas,menlo,monospace", 38, bold=True)
        self.sub_f = pygame.font.SysFont("consolas,menlo,monospace", 20)
        self.f = pygame.font.SysFont("consolas,menlo,monospace", 17)

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
            from src.scenes.game_scene import GameScene
            self.proxima = GameScene(self.siguiente_nivel_idx, self.progreso)

    def actualizar(self, dt):
        self.t += dt

    def dibujar(self, sup):
        sup.fill(config.CIELO)
        pygame.draw.rect(sup, config.PASTIZAL, (0, 420, config.ANCHO, config.ALTO - 420))
        cx = config.ANCHO // 2

        titulo = self.titulo_f.render(f"¡{self.nombre_completado} superado!", True, (60, 45, 20))
        sup.blit(titulo, titulo.get_rect(center=(cx, 150)))

        neta = self.progreso["neta"]
        msg = f"Miel acumulada:  {neta:.0f} / {config.META_GLOBAL_MIEL:.0f} g"
        sup.blit(self.sub_f.render(msg, True, (70, 60, 35)),
                 self.sub_f.render(msg, True, (70, 60, 35)).get_rect(center=(cx, 210)))

        bw = 420
        bx = cx - bw // 2
        prop = max(0.0, min(1.0, neta / config.META_GLOBAL_MIEL))
        pygame.draw.rect(sup, (90, 70, 40), (bx, 236, bw + 4, 20), 2)
        pygame.draw.rect(sup, config.BARRA_META, (bx + 2, 238, int(bw * prop), 16))

        siguiente = (f"Sigue:  {self.siguiente['nombre']}   "
                     f"({self.siguiente['duracion']} s, meta {self.siguiente['meta']} g)")
        sup.blit(self.f.render(siguiente, True, (45, 40, 25)),
                 self.f.render(siguiente, True, (45, 40, 25)).get_rect(center=(cx, 300)))

        if int(self.t * 2) % 2 == 0:
            call = self.sub_f.render("ENTER para continuar", True, (30, 25, 15))
            sup.blit(call, call.get_rect(center=(cx, 500)))
