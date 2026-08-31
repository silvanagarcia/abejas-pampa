"""Escena principal de juego: pecoreo en el Caldenal."""

import pygame

from src.constants import config
from src.entities.abeja import Abeja
from src.entities.colmena import Colmena
from src.entities.flor import generar_flores
from src.UI.hud import HUD


class GameScene:
    """Una ronda completa: juntar néctar y llevarlo a la colmena."""

    def __init__(self):
        self.hud = HUD()
        self.reiniciar()

    def reiniciar(self):
        self.colmena = Colmena(config.ANCHO // 2, 70)
        self.abeja = Abeja(config.ANCHO // 2, config.ALTO // 2)
        self.flores = generar_flores(config.CANTIDAD_FLORES, self.colmena.rect.inflate(80, 80))
        self.tiempo_restante = config.DURACION_RONDA
        self.terminado = False

    # -- ciclo de vida --------------------------------------------------
    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
            self.reiniciar()

    def actualizar(self, dt):
        if self.terminado:
            return

        self.tiempo_restante -= dt
        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0
            self.terminado = True
            return

        self._mover_abeja(dt)
        for flor in self.flores:
            flor.actualizar(dt)
        self._pecorear(dt)
        self._descargar()

    def dibujar(self, sup):
        self._fondo(sup)
        self.colmena.dibujar(sup)
        for flor in self.flores:
            flor.dibujar(sup)
        self.abeja.dibujar(sup)
        self.hud.dibujar(sup, self.abeja, self.colmena, self.tiempo_restante)
        if self.terminado:
            self.hud.cartel_final(sup, self.colmena)

    # -- lógica interna -----------------------------------------------
    def _mover_abeja(self, dt):
        teclas = pygame.key.get_pressed()
        d = pygame.Vector2(
            (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - (teclas[pygame.K_LEFT] or teclas[pygame.K_a]),
            (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) - (teclas[pygame.K_UP] or teclas[pygame.K_w]),
        )
        if d.length_squared() > 0:
            d = d.normalize()
        self.abeja.mover(d, dt)

    def _pecorear(self, dt):
        if self.abeja.llena:
            return
        cupo = config.NECTAR_POR_SEGUNDO * dt
        for flor in self.flores:
            if cupo <= 0:
                break
            if self.abeja.rect.colliderect(flor.rect):
                disponible = flor.extraer(cupo)
                aceptado = self.abeja.sorber(disponible)
                # devolver lo que la abeja no pudo cargar
                if aceptado < disponible:
                    flor.nectar += disponible - aceptado
                cupo -= aceptado

    def _descargar(self):
        if self.abeja.nectar > 0 and self.abeja.rect.colliderect(self.colmena.rect):
            self.colmena.recibir(self.abeja.descargar())

    def _fondo(self, sup):
        sup.fill(config.CIELO)
        pygame.draw.rect(sup, config.PASTIZAL, (0, 120, config.ANCHO, config.ALTO - 120))
