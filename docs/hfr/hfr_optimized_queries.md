# HFR ERDDAP — query ottimizzate per RheoMarine-SLO

Data: 2026-11-25. Endpoint verificato live: `erddap.hfrnode.eu` (HTTP 200, dati fino al 2026-11-25T13:00Z).

## Dataset

| Nodo | Dataset ERDDAP | Copertura verificata | Griglia |
|------|----------------|----------------------|---------|
| IZOLA | `EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3` | 2022-11-24 → 2026-11-25 (nc locale); catalogo dichiara da 2022-10-16 | 20 × 22 = 440 celle |
| PIRAN | `EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3` | 2021-01-01 → 2026-11-25 | 440 celle (stesso bbox) |

Bbox comune usato in tutte le query (coordinate della griglia, non del mare):

- `latitude`: 45.52685 → 45.78333
- `longitude`: 13.375 → 13.78056
- `depth`: 0.0 (unico livello)

## Sintassi ERDDAP corretta

I constraint vanno **sulle variabili dati**, un bracket per dimensione, nell'ordine delle dimensioni della variabile (`time, depth, latitude, longitude`). Le coordinate non si elencano come variabili separate. Parentesi e quadre devono essere URL-encoded (`--data-urlencode` con curl `--get`).

Formato `.csv0` (niente header, parsing posizionale: time,depth,lat,lon,EWCT,NSCT,QCflag per riga) oppure `.csv` (con header) per test. Per download grandi preferire `.nc` (binario, ~10× più piccolo del CSV).

## Variabili richieste

Solo `EWCT`, `NSCT`, `QCflag`. Escluse `RDVA`/`DRVA` e le altre non indispensabili.

## Risoluzione temporale

Passo nominale PT30M, ma **irregolare** — non assumere esattamente 30 min:

| Nodo | dt mediano | p5 | p95 | gap >1h | gap massimo |
|------|-----------|----|----|---------|-------------|
| IZOL | 1800 s | 1800 s | 1800 s | 69 | ~65 giorni |
| PIRA | 1800 s | 1800 s | 3600 s | 2008 | ~51 giorni |

- "Ogni 2 timestamp" e "orario" coincidono praticamente (1 timestamp ogni 2 step nominali = ~1 h). Entrambi dimezzano righe e tempo di risposta.
- PIRA ha molti più gap: ~2000 buchi >1h su 5.9 anni, inclusi outage lunghi. Da trattare con buchi espliciti, non interpolazione cieca.
- IZOL ha un buco di ~65 giorni (dt max 5.662.800 s) e 39 gap >6h — la finestra 12mo/corso degli anni ha copertura non uniforme.

## Query base (30 giorni, step nativo)

```
https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3.csv0
  ?EWCT[(2026-10-26T13:00:00Z):1:(2026-11-25T13:00:00Z)][(0.0)][(45.52685):1:(45.78333)][(13.375):1:(13.78056)]
  &NSCT[...stessi constraint...]
  &QCflag[...stessi constraint...]
```

Equivalente PIRA: `EUHFR_NRTcurrent_HFR-NAdr-PIRA_v3.csv0`.

### Esempio curl funzionante (verificato)

```bash
curl -L --fail --show-error --max-time 300 --get \
  --data-urlencode 'EWCT[(2026-10-26T13:00:00Z):1:(2026-11-25T13:00:00Z)][(0.0)][(45.52685):1:(45.78333)][(13.375):1:(13.78056)]' \
  --data-urlencode 'NSCT[(2026-10-26T13:00:00Z):1:(2026-11-25T13:00:00Z)][(0.0)][(45.52685):1:(45.78333)][(13.375):1:(13.78056)]' \
  --data-urlencode 'QCflag[(2026-10-26T13:00:00Z):1:(2026-11-25T13:00:00Z)][(0.0)][(45.52685):1:(45.78333)][(13.375):1:(13.78056)]' \
  'https://erddap.hfrnode.eu/erddap/griddap/EUHFR_NRTcurrent_HFR-NAdr-IZOL_v3.csv0' \
  -o IZOL_30d.csv0
```

### Variante oraria (step 2)

Sostituire `:1:` con `:2:` nel primo bracket di ogni variabile → ~metà righe, ~metà tempo.

### Variante NetCDF (consigliata per >90 giorni)

`.nc` invece di `.csv0`: stesso constraint, output binario compresso lato server. Per le finestre 12mo/max il CSV0 supererebbe i 300–2000 MB; in .nc stimare ~10–15% di quel volume.

## Note operative

- Il feed NRT è in ritardo ~2 h rispetto al tempo reale: l'`end_time` va **clampato** all'ultimo timestamp disponibile, altrimenti ERDDAP risponde 404.
- `QCflag`: 1 = pass, 4 = flagged, NaN = cella senza dato. Filtrare a valle; la quota di celle con `QCflag==1` è in `hfr_archive_size_estimate.csv`.
- Non filtrare NaN lato server (ERDDAP non lo consente sulle variabili dati): le righe contano sempre 440 celle/timestamp.
