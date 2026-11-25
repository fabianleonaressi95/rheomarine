# HFR download plan — RheoMarine-SLO

Data: 2026-11-25. Stato: **nessun download massivo avviato**. Le stime sono in `hfr_archive_size_estimate.csv`, le query in `hfr_optimized_queries.md`.

## Sintesi delle stime (CSV0, 3 variabili, step nativo)

| Finestra | IZOL size / tempo | PIRA size / tempo | QCflag==1 IZOL | QCflag==1 PIRA |
|----------|-------------------|-------------------|---------------|---------------|
| 30 giorni | 37.8 MB / ~37 s | 35.8 MB / ~36 s | 50.9% | 24.9% |
| 90 giorni | ~113 MB / ~2 min | ~105 MB / ~2 min | 52.8% | ~25% (stima) |
| 12 mesi | ~445 MB / ~7 min | ~340 MB / ~6 min | 23.2% | ~25% (stima) |
| massimo | ~1.7 GB / ~40 min+ | ~2.2 GB / ~40 min+ | 34.7% | ~25% (stima) |

Step orario (ogni 2 timestamp): dimezza tutto. Formato `.nc`: ~10× più piccolo del CSV0 per le finestre grandi.

## Copertura temporale effettiva

- **IZOL**: archivio dal 2022-11-24 (il catalogo dichiara 2022-10-16, ma il .nc verificato parte da fine novembre 2022 — ~5 settimane di gap iniziale da confermare). Buco massimo ~65 giorni.
- **PIRA**: archivio dal 2021-01-01 (~5.9 anni), ma con ~2000 gap >1h e un outage massimo di ~51 giorni. La copertura è più lunga ma più frammentata di IZOL.
- Entrambi arrivano a 2026-11-25T13:00Z (verificato live).

## Qualità e validazione

- `QCflag==1` (pass): IZOL ~51–53% nelle finestre recenti, ma crolla a ~23% sull'anno — la qualità dell'ultimo anno è sensibilmente peggiore o la copertura radar è diminuita. PIRA stabile ~25% (stimato su 30g).
- **Non dichiarare i dati validati**: sono scaricabili e freschi, ma la validazione richiede un confronto indipendente (boa, ADCP, modelli). La scarsa frazione di celle flag=1, specialmente PIRA e IZOL-12mo, va investigata prima di usare le serie in validazione.
- I gap temporali (decine di giorni per PIRA, ~2 mesi per IZOL) devo essere documentati nel dataset di validazione, non interpolati silenziosamente.

## Criterio di scelta della finestra per RheoMarine-SLO

La finestra deve coprire un periodo con:

1. **co-variabilità ambiente-rheo**: eventi di piena/stratificazione nel Golfo di Trieste — servono stagioni complete, quindi **minimo 12 mesi**;
2. **qualità QC sufficiente**: IZOL-30/90g ha ~51–53% flag=1, ma 12mo scende a 23% — verificare se la degradazione è reale o dovuta a stagionalità;
3. **confronto IZOL vs PIRA**: finestre comuni per validazione incrociata (es. ultimi 90 giorni dove entrambi hanno dati);
4. **indipendenza**: le finestre non devono sovrapporsi al periodo usato per calibrare il modello M0–M2.

## Piano proposto (da approvare)

- **Fase 1 (approvata di fatto, già verificata)**: pull da 30 giorni × 2 nodi in CSV0 — ~73 MB totali, ~75 s totali. Utile per validare il pipeline end-to-end.
- **Fase 2 (da approvare)**: pull 90 giorni × 2 nodi in `.nc` — stimato ~20–30 MB binario, ~2–4 min. Finestra minima stagionale.
- **Fase 3 (decisione scientifica)**: finestra 12–24 mesi solo dopo aver verificato la copertura QC mese per mese (query QCflag-only, leggera) e scelto un periodo con flag=1 stabile. Evitare il pull "max archive" in una sola richiesta: PIRA richiederebbe ~2.2 GB CSV / ~40+ min con rischio timeout — se serve l'archivio completo, farlo per anno in `.nc`.

## Note operative

- Clampar sempre `end_time` all'ultimo timestamp noto (feed NRT in ritardo ~2h → 404 altrimenti).
- Salvare i file in `data/hfr/<SITE>_<window>_<format>.<ext>` e registrare data di pull, URL e hash.
- Non lanciare download >90g finché non è approvato il piano.
