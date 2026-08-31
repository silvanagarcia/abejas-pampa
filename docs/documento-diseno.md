# Documento de diseño — Abejas de la Pampa

## Concepto

Juego arcade de recolección donde encarnás una **abeja obrera pecoreadora**
del **Caldenal pampeano**. El lazo central es: *explorar → juntar néctar →
volver a la colmena → producir miel*, contra un reloj.

## Pilares

1. **Raíz local.** Las especies, el ambiente y la dinámica (trashumancia,
   danza, abejas nativas) salen de información real de La Pampa
   (ver `INFO-ABEJAS-LA-PAMPA.md`).
2. **Fácil de entender, difícil de optimizar.** Los controles son solo
   moverse; la profundidad está en decidir *qué flores* y *cuándo volver*.
3. **Crecer por capas.** Cada versión agrega un sistema, sin romper el lazo
   central (ver `ROADMAP.md`).

## Lazo de juego (v0.1)

```
        ┌─────────────┐
        │  buscar flor │◄──────────────┐
        └──────┬───────┘               │
               │ posarse               │ buche con lugar
               ▼                       │
        ┌─────────────┐                │
        │ sorber néctar│────────────────┘
        └──────┬───────┘
               │ buche lleno
               ▼
        ┌─────────────┐      ┌──────────────┐
        │ ir a colmena │─────►│ néctar → miel │──► sube el puntaje
        └─────────────┘      └──────────────┘
```

## Economía (valores en `config.py`)

| Elemento | Valor v0.1 | Nota |
|---|---|---|
| Capacidad del buche | 100 | obliga a volver ~cada 2 flores |
| Néctar por segundo (sorbo) | 55 | posarse ~1–2 s por flor |
| Néctar caldén / chañar / piquillín / jarilla | 60 / 45 / 35 / 30 | por flor llena |
| Recarga | 4 / 3 / 5 / 6 por s | las chicas se reponen más rápido |
| Néctar → miel | ×0,7 | pérdida por deshidratación del néctar |
| Duración de la ronda | 90 s | |

Tensión de diseño: las flores grandes (caldén) rinden más pero se recargan
lento; las chicas (jarilla) son un goteo constante. El jugador arma su ruta.

## Estética

- Paleta pampeana: cielo celeste, pastizal verde seco, tierra clara.
- Formas simples dibujadas con primitivas de pygame (sin assets externos en
  v0.1). Abeja amarilla con rayas y alas que aletean.
- Tipografía monoespaciada para el HUD.

## Sonido (desde v0.2)

- Zumbido de fondo que sube con la velocidad.
- "Sorbo" corto al juntar néctar; "plop" al descargar en la colmena.
- Ambiente: viento, chicharras.

## Métrica de éxito de una partida

Gramos de miel al terminar la jornada. Más adelante: bonus por
**biodiversidad** (visitar las 4 especies) y por **polinización** (flores
distintas tocadas).

## Fuera de alcance por ahora

Multijugador, mapa scrolleable, editor de niveles, físicas realistas de vuelo.
