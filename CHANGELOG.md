# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).
El proyecto sigue [SemVer](https://semver.org/lang/es/).

## [0.3.0] - 2026-08-31 — "El objetivo del día"

### Agregado

- **Gestor de escenas** en `src/main.py`: Inicio → Juego → Venta → Juego.
  Cada escena expone `manejar_evento` / `actualizar` / `dibujar` / `proxima`.
- **Pantalla de inicio** (`src/scenes/intro_scene.py`): título, explicación del
  objetivo y de los peligros, controles. `ENTER`/`ESPACIO` para empezar.
- **Objetivo de la jornada**: `config.META_MIEL_G` gramos de miel neta (120).
  Al alcanzarlo, la jornada termina en éxito aunque quede tiempo.
- **Pantalla de venta** (`src/scenes/venta_scene.py`): reparte la miel neta en
  **tarritos de `GRAMOS_POR_TARRO` g** (30) dibujados, con resumen de miel
  bruta, descuento por néctar contaminado, miel neta, cantidad de tarritos y
  **venta estimada** (`PRECIO_TARRO`). Distingue jornada cumplida / se hizo de
  noche. `ENTER` inicia una jornada nueva.
- HUD: barra de avance **`miel del día: X / meta g`** en lugar del contador
  suelto de miel.

### Cambiado

- Duración de la jornada 90 s → **120 s**.
- `GameScene` ya no abre la leyenda automáticamente (la pantalla de inicio
  explica el objetivo); `H` la sigue abriendo.
- El cartel de fin de ronda del HUD se reemplazó por la pantalla de venta.

## [0.2.1] - 2026-08-31

### Agregado

- **Pantalla de ayuda / leyenda** (`src/UI/leyenda.py`): explica con íconos qué
  es cada elemento en pantalla. Se abre al empezar la ronda y con la tecla `H`;
  mientras está abierta el juego queda en pausa.
- Pista permanente `H = ¿qué es cada cosa?` abajo a la izquierda.
- `docs/GUIA-VISUAL.md`: guía con capturas anotadas de todos los elementos.

### Cambiado

- Las **nubes de pesticida** ahora se ven claramente: círculo violeta con
  borde oscuro, motas y el cartel `PESTICIDA`. Antes se leían como "círculos
  grises". Radio reducido (70 → 56).
- La franja de cultivo lleva un rótulo vertical `CULTIVO`.

## [0.2.0] - 2026-08-31 — "Peligros del Caldenal"

### Agregado

- **Energía / vida útil** de la abeja: se agota volando (más rápido en
  movimiento), se recupera parcialmente al descargar en la colmena. A 0 hay
  6 s de gracia para llegar a la colmena antes de terminar la jornada.
- **Varroa destructor**: infestación que crece con el tiempo de vuelo y
  penaliza velocidad (−40 % máx) y capacidad (−30 % máx). Se reduce al
  descargar en la colmena y posándose en **jarilla**.
- **Chaqueta amarilla** (`entities/enemigos.py::Avispa`): persigue a la abeja
  cargada, le roba néctar por contacto y huye; aparece a partir del 45 % de la
  ronda con frecuencia creciente.
- **Benteveo** (`entities/enemigos.py::Ave`): pasadas horizontales con sombra
  de aviso ~1 s antes; si engancha a la abeja le tira toda la carga.
- **Cultivo y deriva de pesticida** (`entities/ambiente.py`): franja lateral
  con nubes que derivan; el contacto causa efecto **subletal** (dirección
  rotada + brújula a la colmena desactivada durante 4 s).
- **Flores tóxicas** en el cultivo: suman miel pero restan en el balance
  final (`PENAL_MIEL_TOXICA`).
- **Viento** (`entities/ambiente.py::Viento`): empuje que cambia cada 5–11 s.
- **Sequía**: modificador aleatorio de ronda (35 %) que baja la recarga de
  todas las flores a la mitad y sube el viento.
- **HUD** ampliado: barras de energía y varroa, brújula a la colmena,
  indicador de viento, avisos efímeros, cartel final con cosecha neta.

### Cambiado

- `Abeja.mover()` ahora recibe el vector de viento; `Abeja.descargar()`
  devuelve `(nectar_total, nectar_toxico)` y repone energía/higiene.
- `flor.generar_flores()` → `flor.generar_campo()` (nativas + tóxicas).
- Colmena reubicada más abajo para no solaparse con el HUD.

## [0.1.0] - 2026-08-31

### Agregado

- Estructura del repositorio siguiendo el modelo de `galaxy_runner`
  (`src/` con `constants`, `entities`, `scenes`, `UI`, `service`; `docs/`; `build/`).
- Bucle principal en `src/main.py` (`python -m src.main`).
- Entidad **Abeja**: movimiento en 8 direcciones, buche con capacidad,
  aleteo animado.
- Entidad **Flor**: 4 especies nativas del Caldenal (caldén, chañar,
  piquillín, jarilla) con néctar y recarga configurables; se despintan al
  vaciarse; generación aleatoria del campo sin pisar la colmena.
- Entidad **Colmena**: convierte el néctar descargado en miel.
- **HUD**: barra de néctar, miel acumulada, tiempo restante, cartel final.
- Ronda de 90 s con fin por tiempo y reinicio con `R`.
- Documentación: `README`, `docs/INFO-ABEJAS-LA-PAMPA.md` (investigación de
  respaldo con fuentes), `docs/documento-diseno.md`, `docs/ARQUITECTURA.md`,
  `docs/ROADMAP.md`, `docs/CREDITOS.md`.
- `LICENSE` (MIT), `.gitignore`, `requirements.txt`.
