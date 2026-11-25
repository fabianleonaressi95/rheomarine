# Protocollo sperimentale minimo — RheoMarine-SLO

Stato: **proposta di protocollo, non eseguita, non concordata con alcun laboratorio.** Disponibilità di strumenti e campioni non confermata. Distinzione mantenuta: **xanthan/κ-carragenina = sistemi sperimentali di riferimento**, non equivalenti automatici degli **EPS naturali** (dossier §3.3). Soglie numeriche non sono inventate: da fissare *prima* delle misure.

## 1. Prove e obiettivi
| ID | Prova | Obiettivo | Variabili | Livello |
|----|-------|-----------|-----------|---------|
| P1 | Caratterizzazione particelle di riferimento | Fornire d, ρp, forma per i modelli | diametro/distribuzione, densità, forma, polimero | Indispensabile |
| P2 | Reologia di flusso di fluidi proxy (xantana, carragenina, miscele) in acqua marina artificiale | Stimare η(γ̇) e parametri candidati (es. Carreau–Yasuda) | viscosità vs. γ̇, temperatura, salinità, concentrazione | Indispensabile |
| P3 | Sedimentazione in acqua di controllo e nei fluidi P2 | Misurare ws e confrontarla con Stokes e con la chiusura f(…;θr) | ws, tempi di attraversamento, d, ρ, forma, T, repliche | Indispensabile |
| P4 | Densità/salinità/temperatura del fluido | Condizioni al contorno delle prove | ρw, S, T | Indispensabile (a basso costo) |
| P5 | Prove oscillatorie | Valutare viscoelasticità (Oldroyd-B/Giesekus solo se richiesto) | G′, G″ | Opzionale |
| P6 | EPS naturali: quantificazione e/o reologia di campioni dell'area | Verificare se le proprietà proxy sono rappresentative | EPS/sostanza organica, clorofilla se disponibile, reologia | Opzionale, subordinata a campioni, servizio e budget |
| P7 | Sedimentazione di aggregati | Alimentare M1 (variazioni di d e ρ) | d e ρ effettivi, ws | Opzionale |

## 2. Dati necessari per modello
- **M0:** d, ρp, ρw, μ (newtoniana), S, T; forma/regime per la validità della relazione di Stokes (Re da verificare); dati HFR (fuori da questo protocollo).
- **M1:** distribuzioni di dimensione, densità effettiva, tassi di aggregazione/biofouling documentabili (misure o letteratura pertinente), bilanci di massa.
- **M2:** η(γ̇) dai P2, ws dai P3 per vincolare f, **un insieme distinto** di misure di sedimentazione per la valutazione finale (dossier §4.4, §6).

## 3. Separazione calibrazione / validazione
Prima di misurare, definire per iscritto quali repliche/condizioni sono per stimare θr e quali per valutare le prestazioni. Le misure non devono servire a entrambi gli scopi.

## 4. Criteri per giustificare M2 (decisione di fine mese 4, dossier §6)
Procedere solo se **tutte** le condizioni seguenti sono documentate:
1. Caratterizzazione reologica utilizzabile (curve di flusso con ripetibilità dichiarata).
2. Dipendenza dal tasso di deformazione non trascurabile rispetto all'incertezza di misura **nell'intervallo di γ̇ rilevante** per le particelle in caduta (stimato da ws/d).
3. Dati di sedimentazione sufficienti per vincolare la chiusura e un insieme indipendente per valutarla.
4. Un percorso credibile di valutazione indipendente delle previsioni del modello.
Altrimenti: M2 documentato come esplorativo o non attivato. Un esito inconclusivo per dati insufficienti ≠ risultato negativo.

## 5. Risultati attesi come dati (non conclusioni)
- Tabelle di η(γ̇) con incertezza per fluido e condizione.
- Tabelle di ws misurata con repliche, accanto alla ws di Stokes calcolata con i parametri misurati.
- Metadati completi (strumenti, temperatura, preparazione dei fluidi).
- Nessuna affermazione su effetti in mare; la rilevanza per le acque slovene resta una domanda di ricerca.

## 6. Riferimenti di metodo
Articolo di dati Mrokowska & Krztoń-Maziopa (Data in Brief 53, 110101) e dataset Mendeley pb7fjnwcw4/ccm9k8pjft (CC BY 4.0, da verifica bibliografica) descrivono apparato e organizzazione dei dati; sono lo stesso programma sperimentale, non repliche indipendenti.
