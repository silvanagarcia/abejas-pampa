# Arquitectura

## Idea general

El juego está armado en capas, de lo más estable a lo más cambiante:

```
main.py            bucle: eventos → actualizar(dt) → dibujar → flip
   │
   └── scenes/     una escena por "pantalla" (hoy solo GameScene)
          │
          ├── entities/    objetos con estado propio (Abeja, Flor, Colmena)
          ├── UI/           dibujo de HUD y carteles
          └── constants/    config.py: todo el balance, sin lógica
```

Regla: **la lógica no toca números mágicos**. Cualquier valor de balance
(velocidades, néctar, duración) vive en `src/constants/config.py`.

## Flujo de un frame

1. `main.py` calcula `dt` (segundos desde el frame anterior) con el `Clock`.
2. Procesa eventos de `pygame`: `QUIT` y `ESC` cortan; el resto se delega a
   `escena.manejar_evento(evento)`.
3. `escena.actualizar(dt)`:
   - descuenta el tiempo de la ronda;
   - mueve la abeja según las teclas mantenidas (`pygame.key.get_pressed`);
   - recarga las flores;
   - resuelve el **pecoreo** (flor → buche) y la **descarga** (buche → colmena).
4. `escena.dibujar(pantalla)`: fondo, colmena, flores, abeja, HUD.

Se usa **movimiento por tiempo** (`dt`), no por frame, así el juego corre
igual a distintos FPS.

## Contrato de escena

Toda escena implementa:

| Método | Para qué |
|---|---|
| `manejar_evento(evento)` | eventos discretos (teclas presionadas una vez) |
| `actualizar(dt)` | avanzar la simulación |
| `dibujar(superficie)` | pintar el frame |

Cuando haya más de una pantalla (menú, game over, ranking) se agrega un
gestor de escenas mínimo en `main.py` o en `scenes/`.

## Entidades

- **Abeja** (`entities/abeja.py`): `pos`, `nectar`/`nectar_toxico`, más dos
  relojes biológicos: `energia` (baja volando) y `varroa` (sube con el tiempo).
  `velocidad` y `capacidad` son propiedades que aplican la penalización por
  varroa. `mover(dir, viento, dt)` incluye el empuje del viento y, si está
  `desorientada`, rota la dirección (efecto subletal).
- **Flor** (`entities/flor.py`): `nectar` vs `nectar_max`, `regen` y flag
  `toxica`. `generar_campo(evitar, cultivo)` reparte nativas en el Monte y
  tóxicas dentro del cultivo.
- **Colmena** (`entities/colmena.py`): `recibir(nectar)` aplica `NECTAR_A_MIEL`.
- **Ambiente** (`entities/ambiente.py`): `Viento` (ráfaga que cambia sola),
  `Cultivo` (franja lateral) y `NubePesticida` (deriva; `contiene(punto)`).
- **Enemigos** (`entities/enemigos.py`): `Avispa` (persigue si la abeja lleva
  carga; `actualizar` devuelve el néctar robado) y `Ave` con máquina de estados
  `ESPERA → AVISO → PASADA`.

Colisiones: rectángulos (`pygame.Rect.colliderect`) y distancia para las
nubes. La escena (`game_scene.py`) orquesta spawns, colisiones y el balance
final (`miel_final()` descuenta el néctar tóxico).

## Reservado para más adelante

- `service/audio_manager.py` — música y efectos.
- `service/db_manager.py` — ranking en SQLite (como en `galaxy_runner`).
- Gestor de escenas cuando entren el menú y el ciclo día/noche (fase 0.3).
