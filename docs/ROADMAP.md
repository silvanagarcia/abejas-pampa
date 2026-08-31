# Roadmap

Cada fase agrega **un** sistema nuevo sobre un juego que ya funciona.

## 0.1 — MVP ✅

Mover la abeja, pecorear flores nativas, descargar en la colmena, HUD,
ronda de 90 s, reinicio.

## 0.2 — Presentación

- Escena de **menú / inicio** y gestor de escenas.
- **Sonido**: zumbido, sorbo, plop, ambiente.
- Sprites/dibujo más cuidado; animación de la abeja según dirección.
- Cartel de instrucciones.

## 0.3 — La abeja como ser vivo

- **Energía** que baja al volar y se recupera al comer néctar; si llega a 0
  la abeja "descansa" unos segundos.
- **Viento** pampeano: empuja la abeja, cambia de dirección cada tanto.
- Ciclo **día/noche**: de noche la abeja no pecorea (vuelve a la colmena).

## 0.4 — Peligros

- **Predadores**: pájaro (*p. ej.* abejaruco/benteveo) y **avispa** que
  persiguen a la abeja cargada.
- Zonas de **agroquímico** cerca de cultivos: bajan energía.
- Vidas o "abejas de la colonia" como intentos.

## 0.5 — Danza de la abeja

- Al descargar una carga grande, la abeja hace la **danza del meneo** y
  aparecen 1–3 **abejas ayudantes** (IA simple) que van a esa flor por un rato.
- El HUD muestra la "info" comunicada (dirección + distancia).

## 0.6 — Abejas nativas sin aguijón

- Selección de personaje: **melífera** (mucho néctar, pica, se defiende) vs
  **nativa/yateí** (poca miel, no pica, poliniza flora autóctona).
- Puntaje de **biodiversidad** separado del de miel.

## 0.7 — Temporadas y trashumancia

- La ronda pasa a ser una **temporada** con etapas: Monte en primavera →
  traslado → pradera/cultivo.
- El jugador decide **cuándo mover el apiario**; cada ambiente tiene su flora.

## 0.8 — Persistencia

- **Ranking en SQLite** (`service/db_manager.py`), como en `galaxy_runner`.
- Tabla de mejores cosechas por modo.

## Ideas sueltas (sin fase)

- Clima: sequía que reduce néctar y recarga.
- Propóleos: juntar resina de jarilla para "reparar" la colmena.
- Modo educativo con fichas de cada especie.
- Empaquetado con PyInstaller (`build/`).
