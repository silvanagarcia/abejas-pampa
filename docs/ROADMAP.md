# Roadmap

Cada fase agrega **un** sistema nuevo sobre un juego que ya funciona.

## 0.1 — MVP ✅

Mover la abeja, pecorear flores nativas, descargar en la colmena, HUD,
ronda de 90 s, reinicio.

## 0.2 — Peligros del Caldenal ✅

- **Energía / vida útil** de la abeja; se recupera en la colmena.
- **Varroa**: se acumula volando, penaliza velocidad y capacidad; se limpia
  en la colmena y en la jarilla.
- **Chaqueta amarilla**: persigue a la abeja cargada y le roba néctar.
- **Benteveo**: pasadas con sombra de aviso; hace soltar la carga.
- **Deriva de pesticida** en la franja de cultivo: efecto subletal
  (desorientación + brújula apagada).
- **Néctar tóxico** de las flores del cultivo: penaliza el total.
- **Viento** y rondas con **sequía**.

Detalle en [`AMENAZAS-Y-MECANICAS.md`](AMENAZAS-Y-MECANICAS.md).

## 0.3 — Presentación

- Escena de **menú / inicio** y gestor de escenas.
- **Sonido**: zumbido, sorbo, plop, ambiente.
- Sprites/dibujo más cuidado; animación de la abeja según dirección.
- Cartel de instrucciones.
- Ciclo **día/noche**: de noche la abeja vuelve a la colmena.

## 0.4 — Más peligros

- **Sapo** apostado en la piquera de la colmena.
- **Arañas / mantis** emboscadas en algunas flores.
- Vidas o "abejas de la colonia" como intentos.
- Salud de la colonia (nosemosis/virus) afectada por varroa y tóxico.

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

- Propóleos: juntar resina de jarilla para "reparar" la colmena.
- Modo educativo con fichas de cada especie.
- Empaquetado con PyInstaller (`build/`).
