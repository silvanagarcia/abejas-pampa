"""Punto de entrada de Abejas de la Pampa.

Ejecutar desde la raíz del repo:

    python -m src.main

Gestor de escenas mínimo: cada escena expone `manejar_evento`, `actualizar`,
`dibujar` y un atributo `proxima` (None o la siguiente escena) para encadenar
Inicio → Juego → Venta → Juego ...
"""

import sys

import pygame

from src.constants import config
from src.scenes.intro_scene import IntroScene


def main():
    pygame.init()
    pygame.display.set_caption(config.TITULO)
    pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
    reloj = pygame.time.Clock()

    escena = IntroScene()

    corriendo = True
    while corriendo:
        dt = reloj.tick(config.FPS) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                corriendo = False
            else:
                escena.manejar_evento(evento)

        escena.actualizar(dt)
        escena.dibujar(pantalla)
        pygame.display.flip()

        if getattr(escena, "proxima", None) is not None:
            escena = escena.proxima

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
