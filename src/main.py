"""Punto de entrada de Abejas de la Pampa.

Ejecutar desde la raíz del repo:

    python -m src.main
"""

import sys

import pygame

from src.constants import config
from src.scenes.game_scene import GameScene


def main():
    pygame.init()
    pygame.display.set_caption(config.TITULO)
    pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
    reloj = pygame.time.Clock()

    escena = GameScene()

    corriendo = True
    while corriendo:
        dt = reloj.tick(config.FPS) / 1000.0  # segundos desde el frame anterior

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

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
