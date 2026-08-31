# Amenazas reales de las abejas → mecánicas del juego

Cada obstáculo del juego sale de una amenaza documentada. Estado:
✅ implementado (v0.2) · 🔜 planificado.

## Depredadores

| Amenaza real | Evidencia | Mecánica | Estado |
|---|---|---|---|
| **Chaqueta amarilla** (*Vespula germanica*) | Invasora sin enemigos naturales en Argentina; ataca colmenas **en otoño**, roba miel/polen y llega a vaciar la colmena | Avispa que persigue a la abeja **cargada** y le roba néctar por contacto, luego huye. Aparecen sobre todo en el último tramo de la ronda ("otoño") | ✅ |
| **Aves insectívoras** (abejaruco ~300/día; acá benteveo, tijereta) | Depredan abejas en vuelo | **Benteveo**: pasada horizontal rápida; su **sombra** en el pasto avisa ~1 s antes. Si engancha a la abeja, le tira la carga | ✅ |
| **Sapos en la piquera** | Se comen hasta 300 abejas/noche apostados en la entrada | Obstáculo fijo junto a la colmena: entrar por un costado o esperar | 🔜 |
| **Arañas / mantis en flores** | Emboscada en la flor | Algunas flores con depredador oculto: posarse sin mirar = daño | 🔜 |

## Plagas y enfermedades

| Amenaza real | Evidencia | Mecánica | Estado |
|---|---|---|---|
| ***Varroa destructor*** | Ácaro; **principal amenaza sanitaria**; debilita y transmite virus | Infestación que sube con el tiempo de vuelo: **−velocidad y −capacidad**. Se reduce al descargar en la colmena o posándose en **jarilla** (resina/higiene) | ✅ |
| **Nosemosis / virus** | Muy dañinos, potenciados por mala nutrición | Salud de la colonia que empeora con varroa alta y néctar contaminado; penaliza la cosecha | 🔜 (parcial: penalización por tóxico) |

## Agroquímicos

| Amenaza real | Evidencia | Mecánica | Estado |
|---|---|---|---|
| **Deriva de pesticida** | Agroquímicos usados en Argentina y prohibidos en la UE matan abejas en vuelo | Franja de **cultivo** al costado del mapa con **nubes de deriva** que derivan lento | ✅ |
| **Neonicotinoides (dosis subletal)** | Desorientan, **borran memoria y olfato**: la abeja sale y **no vuelve** a la colmena | Efecto **no letal**: controles "torcidos" unos segundos y se **apaga la brújula** a la colmena | ✅ |
| **Néctar contaminado** | Se acumula en miel/cera/pan de abeja; expone a toda la colonia y larvas | Flores del cultivo dan néctar tóxico: **suma miel pero resta** en el balance final | ✅ |

## Ambiente pampeano

| Amenaza real | Evidencia | Mecánica | Estado |
|---|---|---|---|
| **Sequía / clima adverso** | Argentina **pierde ~30 % de las colmenas por año** por causas combinadas | Modificador de ronda: **−néctar y −recarga** en todas las flores + **más viento** | ✅ |
| **Viento** | Impide o dificulta el vuelo | Ráfaga que **empuja** a la abeja y cambia de dirección cada 5–11 s | ✅ |
| **Desmonte del Caldenal** | Quedaba 3,5 M ha (24 % de La Pampa), **hoy ~11 %**; se pierden ~2.400 ha/año | Evento: un sector se "tala" y esas flores de caldén desaparecen esa partida | 🔜 (fase 0.7) |
| **Incendios** | "Enemigo declarado" del bosque de caldén | Frente de fuego que avanza quemando flores | 🔜 (fase 0.7) |
| **Monocultivo de soja** | Dieta pobre; empobrece la microbiota; deja la colonia vulnerable a Varroa/Nosema | Temporada "pradera": mucho néctar fácil pero se acumula "mala nutrición" → abeja lenta y frágil | 🔜 (fase 0.7) |

## Biología de la pecoreadora

| Hecho | Mecánica | Estado |
|---|---|---|
| La obrera en su última etapa se "gasta" (desgaste de alas, vida corta) | **Energía** que solo baja volando; se recupera algo al descargar en la colmena. A 0: 6 s para llegar a la colmena o termina la jornada | ✅ |
| Comunicación por **danza del meneo** (dirección respecto al sol + distancia) | Tras una carga grande, la abeja "baila" y aparecen abejas ayudantes | 🔜 (fase 0.5) |
| **Abejas nativas sin aguijón** (meliponas): poca miel, gran valor, polinizan flora nativa | Personaje alternativo con puntaje de biodiversidad | 🔜 (fase 0.6) |

## Fuentes

- [Infobae — Argentina pierde el 30 % de las colmenas por año](https://www.infobae.com/tendencias/2019/01/02/por-que-en-la-argentina-se-pierde-el-30-de-las-colmenas-por-ano/)
- [SoLatInA — Las chaquetas amarillas en la Patagonia y su impacto sobre la apicultura](https://solatina.org/yellowjackets-patagonia-2024/)
- [CONICET — *Vespula germanica*, la avispa chaqueta amarilla](https://bicyt.conicet.gov.ar/fichas/produccion/111256)
- [IMBIV-CONICET — Contaminantes en la abeja de la miel y productos de la colmena en Argentina](https://imbiv.conicet.unc.edu.ar/contaminantes-encontrados-en-la-abeja-de-la-miel-y-en-diferentes-productos-de-sus-colmenas-para-distintas-regiones-de-argentina/)
- [NRDC — Neonicotinoides 101: efectos en humanos y abejas](https://www.nrdc.org/es/stories/neonicotinoides-101-efectos-humanos-abejas)
- [Redalyc — Daño colateral en abejas por exposición a pesticidas de uso agrícola](https://www.redalyc.org/journal/2654/265457559016/html/)
- [IPS — Insecticidas desorientan a las abejas](https://ipsnoticias.net/2013/04/insecticidas-desorientan-a-las-abejas-europeas/)
- [INIBIOMA-CONICET — La expansión del monocultivo de soja amenaza la producción de miel](https://inibioma.conicet.arg/la-expansion-del-monocultivo-de-soja-amenaza-la-produccion-de-miel-en-argentina/)
- [Ambientum — Desaparece más de la mitad del bosque de caldén en Argentina](https://www.ambientum.com/ambientum/medio-natural/desaparece-mas-de-la-mitad-del-bosque-de-calden-en-argentina.asp)
- [Sobre La Tierra (UBA) — Un bosque pampeano tocado e invadido](https://sobrelatierra.agro.uba.ar/un-bosque-pampeano-tocado-e-invadido/)
- [Bioenciclopedia — Depredadores de las abejas y avispas](https://www.bioenciclopedia.com/depredadores-de-las-abejas-y-avispas-1119.html)
