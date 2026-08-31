"""Escena principal de juego: pecoreo en el Caldenal, ahora con peligros."""

import random

import pygame

from src.constants import config
from src.entities.abeja import Abeja
from src.entities.ambiente import Cultivo, Viento
from src.entities.colmena import Colmena
from src.entities.enemigos import Ave, Avispa
from src.entities.flor import generar_campo
from src.UI.hud import HUD

SEGUNDOS_GRACIA = 6.0   # tiempo para volver a la colmena tras quedarse sin energía


class GameScene:
    """Una ronda: juntar néctar y llevarlo a la colmena, sorteando peligros."""

    def __init__(self):
        self.hud = HUD()
        self.reiniciar()

    def reiniciar(self):
        self.colmena = Colmena(config.ANCHO // 2, 165)
        self.abeja = Abeja(config.ANCHO // 2, config.ALTO // 2)
        self.cultivo = Cultivo()
        self.flores = generar_campo(self.colmena.rect.inflate(80, 80), self.cultivo.rect)
        self.viento = Viento()
        self.avispas = []
        self.ave = Ave()

        self.sequia = random.random() < 0.35
        if self.sequia:
            self.viento.factor = 1.8
            for f in self.flores:
                f.regen *= 0.5

        self.tiempo_restante = config.DURACION_RONDA
        self.miel_toxica = 0.0          # néctar tóxico ya descargado
        self.sin_energia_t = 0.0
        self.terminado = False
        self.motivo = ""
        self.aviso = ""                 # texto efímero (robo, susto, etc.)
        self._aviso_t = 0.0

    # -- ciclo de vida ------------------------------------------------
    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
            self.reiniciar()

    def actualizar(self, dt):
        if self.terminado:
            return

        self.tiempo_restante -= dt
        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0
            self._terminar("Se hizo de noche")
            return

        self.viento.actualizar(dt)
        self.cultivo.actualizar(dt)
        for flor in self.flores:
            flor.actualizar(dt)

        self._mover_abeja(dt)
        self._ambiente(dt)
        self._pecorear(dt)
        self._descargar()
        self._enemigos(dt)
        self._chequear_energia(dt)

        if self._aviso_t > 0:
            self._aviso_t -= dt
            if self._aviso_t <= 0:
                self.aviso = ""

    def dibujar(self, sup):
        self._fondo(sup)
        self.cultivo.dibujar(sup)
        self.colmena.dibujar(sup)
        for flor in self.flores:
            flor.dibujar(sup)
        self.ave.dibujar(sup)
        for avispa in self.avispas:
            avispa.dibujar(sup)
        self.abeja.dibujar(sup)

        self.viento.dibujar(sup, self.hud.fuente)
        self.hud.dibujar(sup, self.abeja, self.colmena, self.tiempo_restante,
                         self.colmena_dir(), self.sequia, self.aviso,
                         self.sin_energia_t)
        if self.terminado:
            self.hud.cartel_final(sup, self.colmena, self.miel_final(), self.motivo)

    # -- helpers de estado -----------------------------------------
    def colmena_dir(self):
        """Vector hacia la colmena para la brújula del HUD (None si desorientada)."""
        if self.abeja.desorientada:
            return None
        d = pygame.Vector2(self.colmena.rect.center) - self.abeja.pos
        return d.normalize() if d.length_squared() > 1 else pygame.Vector2()

    def miel_final(self):
        return max(0.0, self.colmena.miel - self.miel_toxica * config.PENAL_MIEL_TOXICA)

    # -- lógica interna -------------------------------------------
    def _mover_abeja(self, dt):
        teclas = pygame.key.get_pressed()
        d = pygame.Vector2(
            (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - (teclas[pygame.K_LEFT] or teclas[pygame.K_a]),
            (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) - (teclas[pygame.K_UP] or teclas[pygame.K_w]),
        )
        if d.length_squared() > 0:
            d = d.normalize()
        self.abeja.mover(d, self.viento.vector, dt)

    def _ambiente(self, dt):
        if self.cultivo.golpea(self.abeja) and not self.abeja.desorientada:
            self.abeja.intoxicar()
            self._flash("¡deriva de pesticida! desorientada")

    def _pecorear(self, dt):
        if self.abeja.llena:
            return
        cupo = config.NECTAR_POR_SEGUNDO * dt
        for flor in self.flores:
            if cupo <= 0:
                break
            if not self.abeja.rect.colliderect(flor.rect):
                continue
            if flor.especie == "jarilla" and not flor.toxica:
                self.abeja.limpiar_varroa(config.VARROA_LIMPIA_JARILLA * dt)
            disponible = flor.extraer(cupo)
            aceptado = self.abeja.sorber(disponible, toxico=flor.toxica)
            if aceptado < disponible:
                flor.nectar += disponible - aceptado
            cupo -= aceptado

    def _descargar(self):
        if self.abeja.nectar > 0 and self.abeja.rect.colliderect(self.colmena.rect):
            total, toxico = self.abeja.descargar()
            self.colmena.recibir(total)
            self.miel_toxica += toxico

    def _enemigos(self, dt):
        # Aparición de chaquetas amarillas: sobre todo en el "otoño" de la ronda
        progreso = 1 - self.tiempo_restante / config.DURACION_RONDA
        if progreso >= config.AVISPA_APARECE_DESDE and len(self.avispas) < config.AVISPA_MAX:
            ritmo = 0.004 + 0.02 * (progreso - config.AVISPA_APARECE_DESDE)
            if random.random() < ritmo:
                self.avispas.append(Avispa())

        for avispa in self.avispas:
            robado = avispa.actualizar(dt, self.abeja)
            if robado > 0:
                self._flash(f"¡una avispa te robó {robado:.0f} de néctar!")

        antes = self.abeja.nectar
        self.ave.actualizar(dt, self.abeja)
        if self.abeja.nectar == 0 and antes > 0 and self.ave.golpeo:
            self._flash("¡el benteveo te hizo soltar la carga!")

    def _chequear_energia(self, dt):
        if self.abeja.energia <= 0:
            self.sin_energia_t += dt
            if self.sin_energia_t >= SEGUNDOS_GRACIA:
                self._terminar("La abeja se agotó lejos de la colmena")
        else:
            self.sin_energia_t = 0.0

    def _terminar(self, motivo):
        self.terminado = True
        self.motivo = motivo

    def _flash(self, texto):
        self.aviso = texto
        self._aviso_t = 2.2

    def _fondo(self, sup):
        sup.fill(config.CIELO)
        pygame.draw.rect(sup, config.PASTIZAL, (0, 120, config.ANCHO, config.ALTO - 120))
