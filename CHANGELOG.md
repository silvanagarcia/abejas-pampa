# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).
El proyecto sigue [SemVer](https://semver.org/lang/es/).

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
