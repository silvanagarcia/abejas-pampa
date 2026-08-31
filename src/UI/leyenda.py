"""Leyenda / pantalla de ayuda: explica qué es cada elemento en pantalla.

Se muestra al empezar la ronda y se abre/cierra con la tecla H.
Mientras está abierta, el juego queda en pausa.
"""

import math

import pygame

from src.constants import config


def _abeja(sup, cx, cy):
    pygame.draw.circle(sup, (250, 225, 150), (cx, cy), 11)
    pygame.draw.circle(sup, config.AMARILLO_ABEJA, (cx, cy), 9)
    pygame.draw.circle(sup, config.NEGRO, (cx, cy), 9, 2)
    for dx in (-3, 2):
        pygame.draw.line(sup, config.NEGRO, (cx + dx, cy - 7), (cx + dx, cy + 7), 2)


def _colmena(sup, cx, cy):
    r = pygame.Rect(cx - 9, cy - 8, 18, 16)
    pygame.draw.rect(sup, config.COLMENA_COLOR, r, border_radius=2)
    pygame.draw.rect(sup, config.NEGRO, r, 2, border_radius=2)
    pygame.draw.line(sup, config.NEGRO, (r.left, cy), (r.right, cy), 1)
    pygame.draw.rect(sup, config.COLMENA_ENTRADA, (cx - 4, cy + 3, 8, 4))


def _flor(sup, cx, cy, color, borde=None):
    for i in range(6):
        ang = math.pi / 3 * i
        pygame.draw.circle(sup, color, (int(cx + math.cos(ang) * 8), int(cy + math.sin(ang) * 8)), 5)
    pygame.draw.circle(sup, (110, 80, 40), (cx, cy), 4)
    if borde:
        pygame.draw.circle(sup, borde, (cx, cy), 12, 2)


def _jarilla(sup, cx, cy):
    _flor(sup, cx, cy, (250, 245, 120))


def _flor_toxica(sup, cx, cy):
    _flor(sup, cx, cy, (150, 170, 90), borde=config.PESTICIDA_COLOR)


def _nube(sup, cx, cy):
    capa = pygame.Surface((26, 26), pygame.SRCALPHA)
    pygame.draw.circle(capa, (*config.PESTICIDA_COLOR, 130), (13, 13), 12)
    pygame.draw.circle(capa, (*config.PESTICIDA_COLOR, 200), (13, 13), 12, 2)
    sup.blit(capa, (cx - 13, cy - 13))


def _avispa(sup, cx, cy):
    pygame.draw.ellipse(sup, config.ALA, (cx - 11, cy - 8, 9, 6))
    pygame.draw.ellipse(sup, config.ALA, (cx + 2, cy - 8, 9, 6))
    pygame.draw.circle(sup, config.AVISPA_COLOR, (cx, cy - 4), 4)
    ab = pygame.Rect(cx - 5, cy - 1, 10, 14)
    pygame.draw.ellipse(sup, config.AVISPA_COLOR, ab)
    pygame.draw.ellipse(sup, config.NEGRO, ab, 2)
    for dy in (2, 7):
        pygame.draw.line(sup, config.NEGRO, (cx - 5, cy + dy), (cx + 5, cy + dy), 2)


def _sombra_ave(sup, cx, cy):
    capa = pygame.Surface((26, 12), pygame.SRCALPHA)
    pygame.draw.ellipse(capa, (*config.SOMBRA_COLOR, 150), capa.get_rect())
    sup.blit(capa, (cx - 13, cy - 6))


def _brujula(sup, cx, cy):
    pygame.draw.circle(sup, (30, 30, 30), (cx, cy), 11)
    pygame.draw.circle(sup, config.BLANCO, (cx, cy), 11, 2)
    pygame.draw.line(sup, config.COLMENA_COLOR, (cx, cy), (cx, cy - 8), 3)
    pygame.draw.circle(sup, config.COLMENA_COLOR, (cx, cy - 8), 3)


def _cultivo(sup, cx, cy):
    pygame.draw.rect(sup, config.CULTIVO_COLOR, (cx - 6, cy - 11, 16, 22))
    pygame.draw.line(sup, (120, 110, 70), (cx - 6, cy - 11), (cx - 6, cy + 11), 2)


class Leyenda:
    ENTRADAS = [
        (_abeja,       "Vos: la abeja obrera. Peluda y redondeada."),
        (_colmena,     "Colmena: descargá acá el néctar. Además recuperás energía y bajás la varroa."),
        (lambda s, x, y: _flor(s, x, y, (255, 240, 170)),
                       "Flores del Monte (caldén, chañar, piquillín): néctar para llevar a la colmena."),
        (_jarilla,     "Jarilla (flor amarillo pálido): da néctar y además te limpia varroa."),
        (_cultivo,     "Franja de cultivo (borde derecho): zona agrícola. Conviene no entrar."),
        (_flor_toxica, "Flor del cultivo (borde violeta): néctar TÓXICO. Suma miel pero la resta al final."),
        (_nube,        "Nube de pesticida (círculo violeta con el cartel PESTICIDA): deriva del cultivo. Te desorienta unos segundos y te apaga la brújula."),
        (_avispa,      "Chaqueta amarilla: avispa de cuerpo alargado. Te persigue cargada y te roba néctar."),
        (_sombra_ave,  "Sombra ovalada en el pasto: el benteveo está por hacer una pasada. Salí de esa línea o te tira la carga."),
        (_brujula,     "Brújula (abajo a la derecha): la flecha marrón apunta a la colmena. Si ves '?', estás desorientada."),
    ]

    NOTA_HUD = ("Barras del HUD (arriba a la izquierda): néctar cargado · energía "
                "(baja al volar) · varroa. Flecha blanca abajo: hacia dónde te empuja el viento. "
                "\"SEQUÍA\": esta ronda hay menos néctar y más viento.")

    def __init__(self):
        self.titulo_f = pygame.font.SysFont("consolas,menlo,monospace", 26, bold=True)
        self.f = pygame.font.SysFont("consolas,menlo,monospace", 15)

    def dibujar(self, sup):
        capa = pygame.Surface((config.ANCHO, config.ALTO), pygame.SRCALPHA)
        capa.fill((0, 0, 0, 210))
        sup.blit(capa, (0, 0))

        panel = pygame.Rect(0, 0, 780, 580)
        panel.center = (config.ANCHO // 2, config.ALTO // 2)
        pygame.draw.rect(sup, (28, 32, 24), panel, border_radius=10)
        pygame.draw.rect(sup, (120, 150, 90), panel, 2, border_radius=10)

        t = self.titulo_f.render("¿Qué es cada cosa?", True, config.BLANCO)
        sup.blit(t, t.get_rect(midtop=(panel.centerx, panel.top + 12)))

        y = panel.top + 52
        for icono, texto in self.ENTRADAS:
            icono(sup, panel.left + 34, y + 8)
            self._wrap(sup, texto, panel.left + 62, y, panel.width - 90)
            y += 35

        y += 6
        for linea in self._lineas(self.NOTA_HUD, panel.width - 60):
            sup.blit(self.f.render(linea, True, (200, 210, 180)), (panel.left + 30, y))
            y += 19

        pie = self.f.render("H para cerrar  ·  R reinicia  ·  ESC sale", True, (255, 230, 120))
        sup.blit(pie, pie.get_rect(midbottom=(panel.centerx, panel.bottom - 12)))

    # -- utilidades de texto ---------------------------------------
    def _lineas(self, texto, ancho_px):
        palabras = texto.split()
        lineas, actual = [], ""
        for p in palabras:
            prueba = f"{actual} {p}".strip()
            if self.f.size(prueba)[0] <= ancho_px:
                actual = prueba
            else:
                lineas.append(actual)
                actual = p
        if actual:
            lineas.append(actual)
        return lineas

    def _wrap(self, sup, texto, x, y, ancho_px):
        for i, linea in enumerate(self._lineas(texto, ancho_px)):
            sup.blit(self.f.render(linea, True, config.BLANCO), (x, y + i * 17))
