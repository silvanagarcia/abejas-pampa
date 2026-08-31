"""Configuración central del juego.

Todas las constantes de balance, colores y tamaños viven acá para que
ajustar el juego no implique tocar la lógica.
"""

# --- Ventana ---
ANCHO = 960
ALTO = 640
FPS = 60
TITULO = "Abejas de la Pampa"

# --- Colores (R, G, B) ---
CIELO = (135, 190, 235)
PASTIZAL = (170, 200, 120)      # verde seco pampeano
TIERRA = (196, 164, 120)
NEGRO = (20, 20, 20)
BLANCO = (245, 245, 245)
AMARILLO_ABEJA = (245, 200, 60)
ALA = (230, 240, 255)
COLMENA_COLOR = (150, 110, 60)
COLMENA_ENTRADA = (60, 40, 20)
HUD_FONDO = (0, 0, 0)
BARRA_NECTAR = (255, 210, 70)
BARRA_LLENA = (255, 120, 60)

# --- Abeja (jugadora) ---
ABEJA_VELOCIDAD = 4.2          # píxeles por frame
ABEJA_CAPACIDAD = 100          # néctar máximo que carga antes de volver
ABEJA_RADIO = 12

# --- Flores ---
# Especies nativas del Caldenal / Monte pampeano.
# nectar: cuánto ofrece una flor llena
# regen: unidades de néctar que recupera por segundo
# color: color de los pétalos
FLORES = {
    "caldén":    {"nectar": 60, "regen": 4.0, "color": (255, 240, 170)},
    "chañar":    {"nectar": 45, "regen": 3.0, "color": (255, 200, 90)},
    "piquillín": {"nectar": 35, "regen": 5.0, "color": (230, 120, 150)},
    "jarilla":   {"nectar": 30, "regen": 6.0, "color": (250, 245, 120)},
}
CANTIDAD_FLORES = 10
FLOR_RADIO = 16
NECTAR_POR_SEGUNDO = 55        # velocidad a la que la abeja sorbe néctar

# --- Colmena ---
COLMENA_ANCHO = 70
COLMENA_ALTO = 80
# 1 unidad de néctar depositada = este factor en miel
NECTAR_A_MIEL = 0.7

# --- Ronda ---
DURACION_RONDA = 90           # segundos
