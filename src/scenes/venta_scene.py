"""Pantalla de cierre del día: la cosecha servida en tarritos para la venta."""

import pygame

from src.constants import config


class VentaScene:
    """Muestra el resultado de la jornada como tarritos de miel."""

    MAX_TARROS_DIBUJO = 12

    def __init__(self, resultado):
        # resultado: dict con miel_bruta, miel_neta, penal, meta, exito, motivo
        self.r = resultado
        self.proxima = None
        self.titulo_f = pygame.font.SysFont("consolas,menlo,monospace", 40, bold=True)
        self.sub_f = pygame.font.SysFont("consolas,menlo,monospace", 20)
        self.f = pygame.font.SysFont("consolas,menlo,monospace", 17)
        self.chico_f = pygame.font.SysFont("consolas,menlo,monospace", 14)

        self.tarros = int(self.r["miel_neta"] // config.GRAMOS_POR_TARRO)
        self.resto = self.r["miel_neta"] - self.tarros * config.GRAMOS_POR_TARRO
        self.venta = self.tarros * config.PRECIO_TARRO
        self.t = 0.0

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_r, pygame.K_SPACE):
            from src.scenes.game_scene import GameScene
            self.proxima = GameScene()

    def actualizar(self, dt):
        self.t += dt

    def dibujar(self, sup):
        sup.fill((247, 238, 214))
        pygame.draw.rect(sup, (224, 205, 165), (0, config.ALTO - 90, config.ANCHO, 90))  # "mesa"
        cx = config.ANCHO // 2

        exito = self.r["exito"]
        titulo = "¡Jornada cumplida!" if exito else "Se hizo de noche"
        color_t = (150, 110, 30) if exito else (140, 70, 60)
        sup.blit(self.titulo_f.render(titulo, True, color_t),
                 self.titulo_f.render(titulo, True, color_t).get_rect(center=(cx, 46)))

        if exito:
            msg = f"Cosechaste la meta de {config.META_MIEL_G} g. A envasar."
        else:
            msg = f"Llegaste a {self.r['miel_neta']:.0f} g de los {config.META_MIEL_G} g. Probá de nuevo."
        sup.blit(self.sub_f.render(msg, True, (80, 65, 40)),
                 self.sub_f.render(msg, True, (80, 65, 40)).get_rect(center=(cx, 84)))

        self._tarros(sup, cx, 118 if self.tarros > 6 else 210)
        self._resumen(sup, cx, 410)

        if int(self.t * 2) % 2 == 0:
            call = self.sub_f.render("ENTER para una nueva jornada   ·   ESC para salir",
                                     True, (40, 30, 15))
            sup.blit(call, call.get_rect(center=(cx, config.ALTO - 45)))

    # -- dibujo -------------------------------------------------------
    def _tarros(self, sup, cx, top):
        n = min(self.tarros, self.MAX_TARROS_DIBUJO)
        if n == 0:
            txt = self.f.render("(no alcanzó para ningún tarrito)", True, (120, 90, 60))
            sup.blit(txt, txt.get_rect(center=(cx, top + 120)))
            return

        por_fila = 6
        aw, ah, sep, sep_fila = 78, 108, 20, 16
        filas = (n + por_fila - 1) // por_fila
        for i in range(n):
            fila, col = divmod(i, por_fila)
            en_fila = min(por_fila, n - fila * por_fila)
            fila_ancho = en_fila * aw + (en_fila - 1) * sep
            x = cx - fila_ancho // 2 + col * (aw + sep)
            y = top + fila * (ah + sep_fila)
            if self.t > 0.15 + i * 0.08:      # aparición escalonada
                self._un_tarro(sup, x, y, aw, ah)

        if self.tarros > self.MAX_TARROS_DIBUJO:
            extra = self.f.render(f"+ {self.tarros - self.MAX_TARROS_DIBUJO} tarritos más",
                                  True, (110, 80, 50))
            sup.blit(extra, extra.get_rect(center=(cx, top + filas * (ah + sep_fila) + 4)))

    def _un_tarro(self, sup, x, y, w, h):
        cuerpo = pygame.Rect(x, y + 14, w, h - 14)
        pygame.draw.rect(sup, config.TARRO_VIDRIO, cuerpo, border_radius=10)
        # miel adentro (deja un cuello de vidrio arriba)
        miel = cuerpo.inflate(-10, -10)
        miel.height = int((cuerpo.height - 22) * 0.86)
        miel.bottom = cuerpo.bottom - 6
        pygame.draw.rect(sup, config.TARRO_MIEL, miel, border_radius=8)
        pygame.draw.rect(sup, (60, 45, 25), cuerpo, 2, border_radius=10)
        # tapa
        tapa = pygame.Rect(x - 3, y, w + 6, 16)
        pygame.draw.rect(sup, config.TARRO_TAPA, tapa, border_radius=4)
        pygame.draw.rect(sup, (60, 45, 25), tapa, 2, border_radius=4)
        # etiqueta
        et = pygame.Rect(0, 0, w - 20, 22)
        et.center = (cuerpo.centerx, cuerpo.centery + 6)
        pygame.draw.rect(sup, (250, 248, 240), et)
        pygame.draw.rect(sup, (120, 90, 50), et, 1)
        g = self.chico_f.render(f"{config.GRAMOS_POR_TARRO} g", True, (110, 80, 40))
        sup.blit(g, g.get_rect(center=et.center))

    def _resumen(self, sup, cx, top):
        caja = pygame.Rect(0, 0, 460, 132)
        caja.center = (cx, top + 40)
        pygame.draw.rect(sup, (255, 250, 236), caja, border_radius=8)
        pygame.draw.rect(sup, (200, 175, 130), caja, 2, border_radius=8)

        filas = [
            ("miel cosechada (bruta)", f"{self.r['miel_bruta']:.0f} g"),
        ]
        if self.r["penal"] > 0.5:
            filas.append(("descuento por néctar contaminado", f"- {self.r['penal']:.0f} g"))
        filas += [
            ("miel neta para envasar", f"{self.r['miel_neta']:.0f} g"),
            (f"tarritos de {config.GRAMOS_POR_TARRO} g", f"{self.tarros}  (sobran {self.resto:.0f} g)"),
            ("venta estimada", f"$ {self.venta:,.0f}".replace(",", ".")),
        ]
        y = caja.top + 12
        for etiqueta, valor in filas:
            sup.blit(self.f.render(etiqueta, True, (90, 75, 50)), (caja.left + 16, y))
            v = self.f.render(valor, True, (60, 45, 25))
            sup.blit(v, v.get_rect(topright=(caja.right - 16, y)))
            y += 23
