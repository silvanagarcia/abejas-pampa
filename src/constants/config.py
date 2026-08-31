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
BARRA_ENERGIA = (120, 220, 130)
BARRA_ENERGIA_BAJA = (230, 90, 80)
VARROA_COLOR = (150, 40, 40)
CULTIVO_COLOR = (210, 200, 120)
PESTICIDA_COLOR = (170, 120, 200)
AVISPA_COLOR = (240, 220, 90)
AVE_COLOR = (90, 110, 130)
SOMBRA_COLOR = (60, 70, 60)

# --- Abeja (jugadora) ---
ABEJA_VELOCIDAD = 4.2          # píxeles por frame
ABEJA_CAPACIDAD = 100          # néctar máximo que carga antes de volver
ABEJA_RADIO = 12

# Energía / vida útil de la pecoreadora: solo baja mientras vuela.
# Se recupera un poco al descargar en la colmena (comer néctar).
ABEJA_ENERGIA_MAX = 100
ENERGIA_GASTO_VUELO = 2.6       # por segundo volando
ENERGIA_GASTO_QUIETA = 0.5     # por segundo quieta (metabolismo)
ENERGIA_RECUPERA_COLMENA = 45   # al descargar néctar en la colmena

# Varroa: ácaro que se acumula con el tiempo de vuelo y penaliza a la abeja.
VARROA_MAX = 100
VARROA_POR_SEGUNDO = 1.1
VARROA_LIMPIA_COLMENA = 20      # se saca algo al descargar
VARROA_LIMPIA_JARILLA = 8       # por segundo posada en jarilla (resina/higiene)
# Con varroa al máximo: hasta -40% velocidad y -30% capacidad efectiva.
VARROA_PENAL_VELOCIDAD = 0.40
VARROA_PENAL_CAPACIDAD = 0.30

# --- Viento pampeano ---
VIENTO_FUERZA_MAX = 1.8        # px/frame de empuje
VIENTO_CAMBIA_CADA = (5, 11)   # segundos: rango entre cambios de ráfaga

# --- Flores ---
# Especies nativas del Caldenal / Monte pampeano.
FLORES = {
    "caldén":    {"nectar": 60, "regen": 4.0, "color": (255, 240, 170)},
    "chañar":    {"nectar": 45, "regen": 3.0, "color": (255, 200, 90)},
    "piquillín": {"nectar": 35, "regen": 5.0, "color": (230, 120, 150)},
    "jarilla":   {"nectar": 30, "regen": 6.0, "color": (250, 245, 120)},
}
CANTIDAD_FLORES = 11
FLOR_RADIO = 16
NECTAR_POR_SEGUNDO = 55        # velocidad a la que la abeja sorbe néctar

# --- Colmena ---
COLMENA_ANCHO = 70
COLMENA_ALTO = 80
NECTAR_A_MIEL = 0.7

# --- Zona de cultivo con deriva de pesticida ---
# Franja al costado del mapa. El néctar de sus flores suma miel pero
# "envenena" la colonia (penalización final). La nube de deriva causa un
# efecto SUBLETAL: no mata, pero desorienta.
CULTIVO_ANCHO = 150
PESTICIDA_RADIO = 70
PESTICIDA_VELOCIDAD = 0.7      # px/frame, deriva lenta
SUBLETAL_DURACION = 4.0        # segundos de desorientación
# La flor tóxica del cultivo:
FLOR_TOXICA_NECTAR = 55
FLOR_TOXICA_REGEN = 7.0
PENAL_MIEL_TOXICA = 0.5        # cada unidad de néctar tóxico resta esto en miel al final

# --- Chaqueta amarilla (Vespula germanica) ---
# Invasora; ataca sobre todo en "otoño" (último tercio de la ronda) y
# persigue a la abeja CARGADA para robarle néctar.
AVISPA_RADIO = 11
AVISPA_VELOCIDAD = 3.4
AVISPA_ROBO = 35              # néctar que arранca por contacto
AVISPA_APARECE_DESDE = 0.45   # fracción de la ronda a partir de la cual salen
AVISPA_MAX = 4

# --- Benteveo (ave insectívora) ---
# Hace pasadas rectas; su SOMBRA en el pasto avisa 1 s antes.
AVE_VELOCIDAD = 7.5
AVE_AVISO = 1.1              # segundos de sombra antes de la pasada
AVE_CADA = (8, 15)          # segundos entre pasadas

# --- Ronda ---
DURACION_RONDA = 90           # segundos
