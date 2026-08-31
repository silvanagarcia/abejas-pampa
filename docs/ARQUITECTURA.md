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

- **Abeja** (`entities/abeja.py`): `pos`, `nectar`, `capacidad`.
  `mover(dir, dt)` limita a los bordes; `sorber()` respeta la capacidad;
  `descargar()` vacía el buche y devuelve la carga.
- **Flor** (`entities/flor.py`): `nectar` vs `nectar_max`, `regen`.
  `extraer()` nunca da más de lo que tiene. `generar_flores()` arma el campo.
- **Colmena** (`entities/colmena.py`): `recibir(nectar)` aplica el factor
  `NECTAR_A_MIEL` y acumula `miel`.

Colisiones: rectángulos (`pygame.Rect.colliderect`). Alcanza para el MVP;
si hace falta más precisión se pasa a círculos.

## Reservado para más adelante

- `service/audio_manager.py` — música y efectos.
- `service/db_manager.py` — ranking en SQLite (como en `galaxy_runner`).
- `service/` para lógica de temporadas/trashumancia y spawn de predadores.
