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
from src.UI.leyenda import Leyenda

SEGUNDOS_GRACIA = 6.0   # tiempo para volver a la colmena tras quedarse sin energía


class GameScene:
    """Un nivel: juntar néctar y llevarlo a la colmena, sorteando peligros.

    La miel neta de cada nivel se suma a `progreso_previo`, que viaja de
    nivel en nivel hasta la meta global del juego.
    """

    def __init__(self, nivel_idx=0, progreso_previo=None):
        self.hud = HUD()
        self.leyenda = Leyenda()
        self.nivel_idx = nivel_idx
        self.progreso_previo = progreso_previo or {"bruta": 0.0, "penal": 0.0, "neta": 0.0}
        self.reiniciar()

    def reiniciar(self):
        nivel = config.NIVELES[self.nivel_idx]

        self.colmena = Colmena(config.ANCHO // 2, 206)
        self.abeja = Abeja(config.ANCHO // 2, config.ALTO // 2)
        self.cultivo = Cultivo()
        self.flores = generar_campo(self.colmena.rect.inflate(80, 80), self.cultivo.rect)
        self.avispas = []
        self.ave = Ave(factor_frecuencia=max(0.5, 1.0 - 0.15 * self.nivel_idx))

        # Dificultad creciente por nivel
        self.avispa_max = min(config.AVISPA_MAX + self.nivel_idx, 8)
        self.avispa_desde = max(0.0, config.AVISPA_APARECE_DESDE - 0.05 * self.nivel_idx)

        prob_sequia = min(0.85, 0.35 + 0.15 * self.nivel_idx)
        self.sequia = random.random() < prob_sequia
        viento_factor = 1.0 + 0.35 * self.nivel_idx
        cambia_min = max(1.5, 3 - 0.4 * self.nivel_idx)
        cambia_max = max(3.5, 7 - 0.8 * self.nivel_idx)
        if self.sequia:
            viento_factor *= 1.8
            for f in self.flores:
                f.regen *= 0.5
        self.viento = Viento(factor=viento_factor, rango_cambio=(cambia_min, cambia_max))

        self.duracion_nivel = nivel["duracion"]
        self.tiempo_restante = nivel["duracion"]
        self.meta = nivel["meta"]
        self.miel_toxica = 0.0          # néctar tóxico ya descargado
        self.sin_energia_t = 0.0
        self.terminado = False
        self.motivo = ""
        self.aviso = ""                 # texto efímero (robo, susto, etc.)
        self._aviso_t = 0.0
        self.mostrar_leyenda = False    # se abre con H
        self.proxima = None             # escena siguiente (nivel/venta)

    # -- ciclo de vida ------------------------------------------------
    def manejar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key == pygame.K_r:
            self.reiniciar()
        elif evento.key == pygame.K_h:
            self.mostrar_leyenda = not self.mostrar_leyenda

    def actualizar(self, dt):
        if self.terminado or self.mostrar_leyenda:
            return

        self.tiempo_restante -= dt
        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0
            self._terminar("Se hizo de noche", exito_nivel=False)
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
        acumulado_total = self.progreso_previo["neta"] + self.miel_final()
        self.hud.dibujar(sup, self.abeja, self.miel_final(), self.meta,
                         self.tiempo_restante, self.colmena_dir(), self.sequia,
                         self.aviso, self.sin_energia_t,
                         self.nivel_idx, len(config.NIVELES),
                         acumulado_total, config.META_GLOBAL_MIEL)
        self.hud.pista_ayuda(sup)
        if self.mostrar_leyenda:
            self.leyenda.dibujar(sup)

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
            if self.miel_final() >= self.meta:
                self._terminar("¡Meta del nivel alcanzada!", exito_nivel=True)

    def _enemigos(self, dt):
        # Aparición de chaquetas amarillas: sobre todo en el "otoño" del nivel
        progreso = 1 - self.tiempo_restante / self.duracion_nivel
        if progreso >= self.avispa_desde and len(self.avispas) < self.avispa_max:
            ritmo = 0.004 + 0.02 * (progreso - self.avispa_desde)
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
                self._terminar("La abeja se agotó lejos de la colmena", exito_nivel=False)
        else:
            self.sin_energia_t = 0.0

    def _terminar(self, motivo, exito_nivel):
        if self.terminado:
            return
        self.terminado = True
        self.motivo = motivo

        neta_nivel = self.miel_final()
        bruta_total = self.progreso_previo["bruta"] + self.colmena.miel
        penal_total = self.progreso_previo["penal"] + (self.colmena.miel - neta_nivel)
        neta_total = self.progreso_previo["neta"] + neta_nivel

        es_ultimo_nivel = self.nivel_idx >= len(config.NIVELES) - 1
        gano_juego = exito_nivel and (es_ultimo_nivel or neta_total >= config.META_GLOBAL_MIEL)

        if exito_nivel and not gano_juego:
            # Superó el nivel pero quedan más por delante: sigue acumulando.
            from src.scenes.nivel_scene import NivelScene
            progreso = {"bruta": bruta_total, "penal": penal_total, "neta": neta_total}
            self.proxima = NivelScene(self.nivel_idx, progreso, self.nivel_idx + 1)
            return

        resultado = {
            "miel_bruta": bruta_total,
            "penal": penal_total,
            "miel_neta": neta_total,
            "meta": config.META_GLOBAL_MIEL,
            "exito": gano_juego,
            "motivo": "¡Ganaste el juego!" if gano_juego else motivo,
            "nivel_alcanzado": self.nivel_idx + 1,
            "niveles_totales": len(config.NIVELES),
        }
        from src.scenes.venta_scene import VentaScene
        self.proxima = VentaScene(resultado)

    def _flash(self, texto):
        self.aviso = texto
        self._aviso_t = 2.2

    def _fondo(self, sup):
        sup.fill(config.CIELO)
        pygame.draw.rect(sup, config.PASTIZAL, (0, 150, config.ANCHO, config.ALTO - 150))
