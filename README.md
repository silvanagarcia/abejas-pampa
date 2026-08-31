# 🐝 Abejas de la Pampa

> Juego 2D en **Python + Pygame** sobre el pecoreo de una abeja obrera en el
> **Caldenal** de La Pampa: volá de flor en flor, juntá néctar de especies
> nativas y llevalo a la colmena para producir miel.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame--CE-2.5-green)
![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow)
![Estado](https://img.shields.io/badge/versi%C3%B3n-0.2.0-orange)

<p align="center">
  <img src="docs/screenshots/juego-v0.2.png" alt="Abejas de la Pampa — v0.2" width="70%">
</p>

---

## Índice

- [Descripción](#descripción)
- [Estado actual (v0.2.0)](#estado-actual-v020)
- [Peligros del Caldenal](#peligros-del-caldenal)
- [Requisitos](#requisitos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Controles](#controles)
- [Cómo se juega](#cómo-se-juega)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Contexto: por qué La Pampa](#contexto-por-qué-la-pampa)
- [Roadmap](#roadmap)
- [Créditos](#créditos)
- [Licencia](#licencia)

---

## Descripción

Controlás una **abeja pecoreadora**. El mapa es un recorte del **Monte
pampeano** con flores de **caldén, chañar, piquillín y jarilla**. Cada especie
da distinta cantidad de néctar y se recarga a distinto ritmo. Juntás néctar
hasta llenar el buche y volvés a la **colmena**, donde se transforma en miel.
La ronda dura 90 segundos: la meta es cosechar la mayor cantidad de miel.

Toda la información biológica y regional que sustenta el juego está en
[`docs/INFO-ABEJAS-LA-PAMPA.md`](docs/INFO-ABEJAS-LA-PAMPA.md).

## Estado actual (v0.2.0)

**"Peligros del Caldenal".** Sobre el MVP (mover, pecorear, descargar, HUD,
ronda de 90 s) se agregó todo lo que le complica la vida a una abeja real:

- **Energía / vida útil**: se agota volando; se recupera algo al descargar en
  la colmena. Si llega a 0, hay 6 s para volver o termina la jornada.
- **Varroa**: ácaro que se acumula con el vuelo y baja velocidad y capacidad.
  Se limpia en la colmena o posándose en **jarilla**.
- **Chaqueta amarilla** (*Vespula germanica*): avispa invasora que persigue a
  la abeja cargada y le roba néctar; aparece sobre todo en el "otoño" de la ronda.
- **Benteveo**: hace pasadas rápidas; su **sombra** avisa antes. Te hace soltar
  la carga.
- **Deriva de pesticida**: franja de cultivo con nubes de agroquímico. Efecto
  **subletal**: desorienta (controles torcidos) y **apaga la brújula** a la colmena.
- **Néctar contaminado**: las flores del cultivo suman miel pero **penalizan**
  el total al final.
- **Viento** pampeano que empuja, y rondas con **sequía** (menos néctar, más viento).

Cada mecánica sale de una amenaza documentada: ver
[`docs/AMENAZAS-Y-MECANICAS.md`](docs/AMENAZAS-Y-MECANICAS.md).
Lo que sigue (danza de la abeja, abeja nativa, trashumancia, ranking) está en
[`docs/ROADMAP.md`](docs/ROADMAP.md).

## Peligros del Caldenal

Guía visual completa con capturas anotadas: [`docs/GUIA-VISUAL.md`](docs/GUIA-VISUAL.md).
Dentro del juego, `H` abre la misma leyenda.

<p align="center">
  <img src="docs/screenshots/leyenda-v0.2.png" alt="Leyenda del juego (tecla H)" width="70%">
</p>

| Peligro | Qué te hace | Cómo lo manejás |
|---|---|---|
| Energía agotada | La abeja no puede seguir | Volvé seguido a la colmena a "comer" |
| Varroa | Más lenta, menos capacidad | Descargá en la colmena; visitá jarilla |
| Chaqueta amarilla | Te roba néctar | Descargá rápido; evitala cuando vas cargada |
| Benteveo | Te tira la carga | Mirá la sombra en el pasto y salí de esa línea |
| Deriva de pesticida | Te desorienta, sin brújula | No entres a la franja de cultivo |
| Flor tóxica (cultivo) | Resta miel al final | Pecoreá en el Monte, no en el cultivo |
| Viento / sequía | Te empuja, hay menos néctar | Corregí el rumbo; priorizá flores llenas |

## Requisitos

- Python 3.10 o superior
- [pygame-ce](https://pyga.me/) 2.5+

## Instalación y ejecución

```bash
git clone https://github.com/silvanagarcia/abejas-pampa.git
cd abejas-pampa

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python -m src.main
```

## Controles

| Tecla | Acción |
|---|---|
| ← ↑ → ↓  /  W A S D | Mover la abeja |
| `H` | Abrir/cerrar la ayuda (**qué es cada cosa**) |
| `R` | Reiniciar la ronda |
| `ESC` | Salir |

La ronda arranca en la pantalla de ayuda; con `H` la cerrás y empezás a jugar.

## Cómo se juega

1. Salís de la zona de la colmena y buscás flores **en el Monte** (evitá la
   franja de cultivo de la derecha).
2. Te posás sobre una flor: el néctar pasa de la flor a tu buche.
3. Cuando el buche está lleno (`¡LLENA!`), volvés a tocar la **colmena**. Ahí
   también recuperás energía y bajás la varroa.
4. El néctar descargado se convierte en miel (factor 0,7).
5. Las flores se recargan solas: conviene rotar entre varias. La **jarilla**
   además te limpia varroa.
6. Cuidado con la **avispa** (te roba), el **benteveo** (te tira la carga) y
   las **nubes de pesticida** (te desorientan).
7. A los 90 segundos termina la jornada y ves tu cosecha neta.

## Estructura del proyecto

```
abejas-pampa/
├── src/
│   ├── main.py                 # bucle principal y manejo de eventos
│   ├── constants/
│   │   └── config.py           # todo el balance y los colores
│   ├── entities/
│   │   ├── abeja.py            # la jugadora: carga, energía, varroa
│   │   ├── flor.py             # flores nativas + tóxicas + campo
│   │   ├── colmena.py          # descarga de néctar → miel
│   │   ├── ambiente.py         # viento, cultivo, nubes de pesticida
│   │   └── enemigos.py         # chaqueta amarilla y benteveo
│   ├── scenes/
│   │   └── game_scene.py       # una ronda completa
│   ├── UI/
│   │   ├── hud.py              # HUD, brújula y cartel final
│   │   └── leyenda.py          # pantalla de ayuda (tecla H)
│   └── service/                # (reservado: audio, persistencia)
├── docs/
│   ├── INFO-ABEJAS-LA-PAMPA.md   # investigación de respaldo
│   ├── AMENAZAS-Y-MECANICAS.md   # amenazas reales → mecánicas
│   ├── GUIA-VISUAL.md            # qué es cada cosa en pantalla
│   ├── documento-diseno.md       # diseño del juego
│   ├── ARQUITECTURA.md           # cómo está armado el código
│   ├── ROADMAP.md                # fases de complejidad
│   └── CREDITOS.md
├── build/                      # scripts de empaquetado (a futuro)
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

## Contexto: por qué La Pampa

La Pampa produce ~7.000 t de miel al año (~11 % del total nacional), con la
floración del **Caldenal** como sustento principal y una apicultura
**trashumante**. El juego usa ese marco real. Detalle y fuentes en
[`docs/INFO-ABEJAS-LA-PAMPA.md`](docs/INFO-ABEJAS-LA-PAMPA.md).

## Roadmap

| Fase | Contenido |
|---|---|
| **0.1** ✅ | MVP: mover, pecorear, descargar, HUD, ronda por tiempo |
| **0.2** ✅ | Peligros: energía, varroa, viento/sequía, chaqueta amarilla, benteveo, deriva de pesticida, néctar tóxico |
| 0.3 | Menú, pantalla de inicio, sonido, día y noche |
| 0.4 | Sapo en la piquera, arañas en flores, más pulido de predadores |
| 0.5 | Danza de la abeja: abejas ayudantes tras una buena carga |
| 0.6 | Modo abeja nativa sin aguijón + puntaje de biodiversidad |
| 0.7 | Temporadas / trashumancia: mover el apiario entre Monte y pradera |
| 0.8 | Ranking persistente en SQLite |

## Créditos

**Dirección y desarrollo:** Silvana Garcia.
Detalle en [`docs/CREDITOS.md`](docs/CREDITOS.md).

## Licencia

[MIT](LICENSE) — © 2026 Silvana Garcia.
