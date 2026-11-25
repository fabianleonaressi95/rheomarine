# RHEOMARINE-SLO
## Note del relatore
### Proposta di collaborazione e richieste di dati

**Relatore:** Fabian Leo Naressi  
**Durata:** 60 minuti (25 di esposizione, 35 di discussione)  
**Riferimento:** RheoMarine – Dossier unico di progetto, versione 1.1, 25 novembre 2026  
**Uso:** copione esteso per l'incontro scientifico; distinguere sempre risultati acquisiti, implementazioni esistenti e attività proposte.

---

## 1. Apertura (2 minuti)

Grazie per il vostro tempo. Vi presento RheoMarine soprattutto per capire con voi se ci siano le condizioni scientifiche e osservative per un primo studio pilota sul trasporto delle microplastiche nel Nord Adriatico.

Vorrei chiarire subito il carattere della proposta: non presento un modello già validato né una previsione operativa. Il lavoro svolto finora ha prodotto un'infrastruttura di acquisizione e controllo dei dati HFR e un primo esercizio numerico riproducibile su sottoinsiemi reali. Restano da costruire e verificare le parti che riguardano la trasformazione biologica delle particelle, la sedimentazione, la reologia e il confronto con osservazioni indipendenti.

L'obiettivo di questo incontro è capire se possiamo delimitare insieme un problema scientifico affrontabile, con dati accessibili e un protocollo realistico. Vorrei arrivare alla discussione su tre questioni: quali dati sono effettivamente utilizzabili; quale domanda circoscritta possono sostenere; quale protocollo sperimentale e computazionale serve per ottenere un risultato difendibile.

## 2. Domanda e posizionamento (4 minuti)

La domanda generale è: **in quali condizioni costiere e sperimentali, se ve ne sono, includere la reologia dell'acqua biologicamente modificata migliora la previsione del trasporto e della sedimentazione delle microplastiche nel Nord Adriatico sloveno?**

Non assumo in partenza che la reologia produca un miglioramento. La tratto come un'ipotesi da confrontare con una descrizione convenzionale e con un modello che includa già le trasformazioni delle particelle.

La domanda si articola in tre parti:

- **RQ1:** quanto le correnti HFR-NAdr permettono di ricostruire la dispersione superficiale e individuare zone e periodi di convergenza?
- **RQ2:** quanto aggregazione, biofouling ed EPS cambiano dimensione, densità efficace, forma, traiettorie e comportamento delle particelle?
- **RQ3:** se proprietà reologiche misurate migliorano la previsione di sedimentazione e distribuzione verticale rispetto a un modello con sola aggregazione e fluido convenzionale?

Il posizionamento bibliografico parte da lavori con funzioni diverse, che non vanno confusi.

Cosoli, Mazzoldi e Gačić (2010) forniscono un riferimento per la validazione di correnti HF radar mediante ADCP nel Nord Adriatico. Il confronto riguarda una rete e un contesto costiero diversi dall'attuale HFR-NAdr: è quindi un precedente metodologico regionale, non una validazione trasferibile automaticamente al nostro dominio.

Mihanović e collaboratori (2011) analizzano i pattern di circolazione superficiale del Nord Adriatico con dati HF radar e Self-Organizing Maps. È utile per la classificazione dei regimi di circolazione, ma i dati sono del 2008 e appartengono alla rete NASCUM.

Weiss e collaboratori (2025) costituiscono un riferimento per il tracciamento lagrangiano nel Mediterraneo. La letteratura sul particle tracking evidenzia però che biofouling, frammentazione, aggregazione e risospensione non possono essere considerati automaticamente risolti da un modello di sola deriva.

Capodici e collaboratori (2024) sono pertinenti per il confronto fra campionamenti in situ e correnti HFR. Il risultato statistico va letto nel contesto del dataset e del disegno sperimentale di quello studio, non generalizzato a ogni costa o campagna.

Mrokowska e collaboratori (2024, 2025) sono particolarmente importanti per la parte di laboratorio: studiano il settling di microplastiche in mezzi a reologia modificata, inclusi sistemi con xanthan gum e carragenina e configurazioni stratificate. Nel repository sono già stati acquisiti e analizzati i dataset associati a questi lavori; le analisi numeriche disponibili sono però limitate dalle informazioni di calibrazione spaziale e dalla necessità di verificare alcuni dettagli sperimentali rispetto agli articoli.

Il contributo che cerco non è quindi un nuovo modello complesso per principio. È l'integrazione, su un caso locale, di correnti osservate, trasformazioni delle particelle, reologia misurata e validazione indipendente. La trasferibilità dai polisaccaridi modello agli EPS naturali resta aperta: distinguerei nettamente sistemi controllati, campioni naturali e uso dei parametri nel modello oceanografico.

## 3. Modelli e confronto (6 minuti)

Presento M0, M1 e M2 come una gerarchia di modelli da confrontare. È importante non confondere questa architettura scientifica con ciò che è già implementato nel software.

**M0 – baseline convenzionale.** La specifica scientifica prevede un modello lagrangiano stocastico forzato dalle correnti HFR, con diffusione turbolenta parametrizzata, sorgenti e rimozioni dichiarate e una legge convenzionale per la velocità di sedimentazione, per esempio Stokes quando le ipotesi di regime e geometria sono rispettate. Il trasporto superficiale sarebbe accoppiato a una descrizione verticale parametrizzata. Deriva di Stokes e contributo del vento vanno inclusi soltanto se non sono già rappresentati nel campo di velocità utilizzato, per evitare doppi conteggi.

**Stato effettivo:** il pilot HFR già eseguito è un esercizio di advezione superficiale con K=0, integrazione forward-Euler e controllo QC del percorso. Non implementa ancora diffusione, sedimentazione, trasporto verticale, deposizione o risospensione. Esiste inoltre un motore finite-volume advection–diffusion separato, ma non è il motore usato nel pilot HFR descritto nel dossier. Non presenterei quindi M0 completo come già operativo o validato.

**M1 – trasformazioni biologiche.** Qui dimensione, densità efficace, forma e stato di aggregazione evolvono nel tempo. Vorrei mantenere pochi parametri, ciascuno giustificato da letteratura o misure. Biofouling e aggregazione possono modificare il comportamento di una particella, ma non vanno rappresentati con coefficienti liberi non identificabili. Prima di aggiungere processi, occorre capire quali variabili siano effettivamente osservabili.

**M2 – estensione reologica, condizionale.** Questa parte introdurrebbe una correzione della velocità di sedimentazione basata su misure reologiche. Carreau–Yasuda è una legge candidata per descrivere lo shear-thinning; non è una scelta già dimostrata per gli EPS naturali del Golfo di Trieste. Oldroyd-B o Giesekus entrerebbero solo se le misure mostrassero una componente viscoelastica rilevante e se i dati fossero sufficienti a identificare i parametri.

L'ipotesi nulla è che la descrizione convenzionale sia sufficiente. L'alternativa è che una correzione reologica, giustificata sperimentalmente, migliori la previsione rispetto a M1. Il confronto deve essere fissato prima delle simulazioni e usare dati non impiegati nella calibrazione.

Le metriche che propongo sono RMSE e MAE, errori sulla distribuzione spaziale, sulla velocità di sedimentazione e sui tempi di permanenza, oltre a skill score, sensibilità e intervalli d'incertezza. Dobbiamo anche controllare il numero di parametri: un modello più complesso non è migliore se migliora soltanto perché ha più gradi di libertà.

M2 sarà credibile soltanto se il miglioramento si mantiene su condizioni indipendenti. Un risultato negativo è scientificamente utile: se M0 o M1 bastano, la componente reologica non serve per quel contesto e non va mantenuta artificialmente.

## 4. Area pilota e dati (4 minuti)

Il dossier individua come area di interesse le acque costiere slovene, in particolare il settore di Ankaran, Koper, Izola e Piran. Il perimetro resta provvisorio: deve dipendere dalla copertura HFR effettiva, dalla qualità e continuità dei dati, dalle osservazioni complementari e dalla possibilità concreta di un confronto sperimentale.

Partirei da una stagione o da un intervallo ben documentato, rinviando l'estensione all'intera serie 2021–2026. Una serie lunga non è automaticamente migliore se la configurazione della rete, la disponibilità delle stazioni e le procedure di elaborazione sono cambiate nel tempo.

Per HFR-NAdr, la documentazione del nodo europeo e di OGS conferma una rete WERA nel Golfo di Trieste con quattro siti: AURI, PIRA, IZOL e TRI1. Le frequenze centrali indicate sono rispettivamente 24,635, 24,525, 24,500 e 24,525 MHz. La rete fornisce dati mediati su 30 minuti, con risoluzione spaziale nominale di 1,5 km e copertura radiale massima indicativa di 35–40 km. Le velocità superficiali sono rappresentative dello strato superiore, circa 0,3–2,5 metri.

C'è una precisazione storica importante: i campi totali erano inizialmente combinati da AURI e PIRA; IZOL è stata aggiunta il 1° marzo 2023 e TRI1 il 10 luglio 2023. Non possiamo quindi trattare la rete a quattro stazioni come omogenea per tutto il periodo storico.

Il DOI della scheda HFR-NAdr è 10.57762/8RRE-0Z07. I dati sono accessibili tramite ERDDAP, con prodotti radiali distinti per stazione e un prodotto di velocità totale. Le variabili EWCT e NSCT sono le componenti est-ovest e nord-sud della velocità totale. UACC e VACC sono informazioni di incertezza/deviazione standard secondo la convenzione del prodotto, non ulteriori componenti della corrente. GDOP è un indicatore geometrico; QCflag va interpretato usando gli attributi effettivi del file e della versione scaricata.

Per il pilot non basta citare la risoluzione nominale. Occorre selezionare celle e periodi in base alla copertura comune, ai flag di qualità, alla geometria e alla continuità. Dobbiamo associare meteo e onde, in particolare per gli episodi di Bora, senza presumere che il solo campo HFR rappresenti ogni contributo alla deriva.

## 5. Richieste di dati (4 minuti)

**NIB e ARSO.** Come indicato nel dossier, il 25 novembre 2026 ho scritto a Branko Čermelj (NIB, Izola), con Matjaž Ličer in copia, e ad ARSO per il nodo di Piran. Le richieste riguardano calibrazioni, manutenzioni, modifiche di configurazione e documentazione di qualità. A NIB chiedo anche, in modo esplicito, controlli di antenna e radial pattern, QC flag, interruzioni e rapporti di validazione.

Nei metadati ERDDAP consultati il 25 novembre, il campo `last_calibration_date` riporta 2023-01-01 per Izola e 2015-01-10 per Piran, a fronte di osservazioni recenti. Non traggo da questo una conclusione sulla qualità o sull'effettiva calibrazione corrente: voglio sapere dai gestori che cosa rappresenta il campo, a quale procedura si riferisce e se esistono registri più aggiornati.

**Osservazioni indipendenti.** Mi interessano i drifter NEREIDES di OGS e ARPA FVG nel Golfo di Trieste. CODE e Stokes devono essere trattati separatamente: rispondono a forzanti differenti e non sono misure intercambiabili della corrente. La richiesta dei dati è ancora da formalizzare e la sovrapposizione con il periodo pilota non è verificata. Chiederei tracciati GPS, date e orari di rilascio e recupero, identificativi, configurazione e drogue, profondità effettiva, frequenza di campionamento, flag QC e modalità di trattamento, preferibilmente in CSV o NetCDF.

Per un primo confronto con il campo di corrente, i CODE potrebbero essere prioritari, ma solo dopo avere verificato profondità e configurazione. I drifter Stokes risentono congiuntamente di corrente, vento e onde: sono interessanti per un modello di deriva più ampio, non per una validazione diretta della sola corrente senza ulteriori termini.

**Copernicus Marine.** Sto esaminando due prodotti distinti. Il prodotto globale `INSITU_GLO_PHY_UV_DISCRETE_NRT_013_048`, DOI 10.48670/moi-00041, raccoglie famiglie separate di dati: drifter del Global Drifter Program, HF radar totali e radiali e velocità associate ai float Argo. Il manuale specifica che i drifter con drogue possono rappresentare circa 15 metri di profondità, mentre quelli senza drogue sono trattati come superficiali. Argo non va confuso con un drifter superficiale; le osservazioni radar non sono indipendenti se provengono dalla stessa rete usata come forcing.

Il prodotto mediterraneo `INSITU_MED_PHYBGCWAV_DISCRETE_MYNRT_013_035`, DOI 10.48670/moi-00044, include variabili di corrente, onde, livello del mare, temperatura e salinità, con geometrie trajectory, profile e point. È aggiornato più volte al giorno, ma l'estensione geografica e temporale del catalogo non dimostra che esistano misure nel nostro dominio.

Per entrambi resta da fare una query puntuale: bbox, date, piattaforma, coordinate, profondità, variabili e QC. Finché questa estrazione non è fatta, li considero fonti candidate, non osservazioni indipendenti già disponibili.

Sarebbero inoltre utili profili ADCP, boa Vida, dati meteorologici, onde, livello del mare e campionamenti di microplastiche con metadati spazio-temporali.

## 6. Validazione, piano e collaborazione (4 minuti)

La validazione va organizzata per livelli, perché non tutti i dati possono validare la stessa cosa.

T1 riguarda qualità, copertura e continuità delle correnti HFR. T2 riguarda la dispersione superficiale e richiede confronti con osservazioni indipendenti di corrente o drifter compatibili per tempo, spazio e profondità. T3 riguarda aggregazione e trasformazioni delle particelle. T4 riguarda sedimentazione e distribuzione verticale. T5 riguarda la caratterizzazione reologica. T6 è il confronto predittivo M0–M2 su dati non usati in calibrazione.

Il pilot già realizzato è utile come verifica numerica e studio di sensibilità su sottoinsiemi HFR reali, con controllo QC del percorso. Non costituisce una validazione indipendente del trasporto e non verifica diffusione, settling, deposizione o concentrazioni di microplastiche. La selezione automatica del dominio massimizza la copertura QC: è una regola computazionale, non una dimostrazione di rappresentatività geografica. Anche i bordi riflettenti o assorbenti del crop sono condizioni artificiali, non una rappresentazione fisica della costa.

**Piano su otto mesi:**

| WP | Mesi | Attività | Risultato |
|---|---|---|---|
| WP1 | 1–2 | Dati HFR, metadati, osservazioni complementari e area pilota | Rapporto sulla qualità dei dati e scelta motivata dell'area |
| WP2 | 2–4 | Settling, reologia e, se possibile, EPS naturali | Protocollo e rapporto di caratterizzazione |
| WP3 | 3–7 | Sviluppo dei modelli e validazione indipendente | Prototipo riproducibile e rapporto di confronto |
| WP4 | 7–8 | Sintesi e trasferimento | Rapporto finale, documentazione aperta, incontro con stakeholder e sintesi pubblica |

Al mese 4 propongo un gate decisionale: M2 procede soltanto se esistono misure reologiche adeguate e un legame quantitativo difendibile con il settling. Altrimenti resta esplorativo e il progetto continua con M0/M1.

**Collaborazione.** Vedo tre livelli possibili, nessuno dei quali è già concordato: confronto tecnico-scientifico; supporto osservativo e accesso a dataset; studio pilota congiunto.

Il mio contributo riguarda architettura matematica, implementazione, integrazione dei dati, confronto tra modelli, analisi di sensibilità, incertezza e documentazione riproducibile. Le misure di laboratorio, l'accesso alle serie osservative e la validazione oceanografica richiedono strutture, strumentazione e competenze qualificate. Non intendo sostituire queste attività con simulazioni.

## 7. Chiusura dell'esposizione (1 minuto)

Dalla discussione vorrei uscire con quattro indicazioni operative: una proposta di area e periodo pilota; un riferimento tecnico per i dati HFR; l'identificazione delle osservazioni indipendenti effettivamente accessibili; un protocollo minimo per EPS, sedimentazione e reologia.

Non chiedo di approvare oggi il progetto nella sua interezza. Chiedo di verificare se esista un primo problema abbastanza circoscritto, con dati e metodi adeguati, che abbia senso affrontare insieme.

---

# DISCUSSIONE (35 minuti)

## Per Laura Ursella

1. Qual è la copertura effettiva delle quattro stazioni, e quali differenze esistono tra i nodi in termini di continuità, lacune e qualità? Quali celle sono più stabili per un primo studio?
2. Quali periodi, stagioni e zone — costiere o più centrali — consigliereste per un pilota che debba essere confrontabile con dati indipendenti?
3. Sono disponibili e accessibili le serie storiche radiali oltre ai campi totali? Quali informazioni sono disponibili su GDOP, deviazioni standard, accuratezza e QC? Qual è la procedura consigliata per selezionare le velocità totali?
4. Esistono confronti recenti con ADCP, drifter o altri strumenti indipendenti nel Golfo di Trieste? Quali sono i limiti noti di quei confronti?
5. Quali misure verticali, meteorologiche e ondose possono essere associate alle serie HFR, in particolare durante gli episodi di Bora?
6. Per una prima fase, partire in 2D con verticale parametrizzata vi sembra metodologicamente corretto? Esistono già dati sufficienti per impostare una componente 3D?
7. Quali informazioni di calibrazione, manutenzione, configurazione e validazione sono disponibili oltre ai campi esposti nei metadati ERDDAP?

## Per Cinzia De Vittor

1. Esistono dati, campioni o serie su EPS, sostanza organica, aggregati, marine snow e fioriture nel settore di interesse? Quali indicatori biologici e chimici usereste per caratterizzare i campioni?
2. Quali campionamenti di microplastiche sono disponibili nel Nord Adriatico, e con quali informazioni su dimensione, forma, polimero, posizione, data e profondità? Quali metodi analitici consigliate?
3. Esistono misure reologiche su campioni naturali? Che cosa è realisticamente ottenibile in una prima fase: curve di flusso, prove oscillatorie o un test più semplice per verificare lo shear-thinning?
4. Qual è il protocollo minimo per collegare le misure reologiche alla sedimentazione, confrontando campioni naturali e sistemi controllati con polisaccaridi modello?
5. Che cosa si può affrontare con dati e campioni già esistenti, che cosa richiede un laboratorio qualificato e che cosa richiederebbe una nuova campagna?
6. In M0 partirei da particelle libere: i dati locali o la letteratura disponibile suggeriscono di includere da subito una classe di aggregati, oppure è più prudente introdurla in M1?
7. Per M2, ha senso partire dallo shear-thinning e introdurre la viscoelasticità soltanto se le misure mostrano che è necessaria?
8. Quali misure minime servono per stimare densità efficace, dimensione e forma degli aggregati e per collegarle a una legge di settling?

## Per entrambe

1. Quali campagne NEREIDES sono concluse e dispongono di tracciati condivisibili? Quali sono le caratteristiche dei dispositivi, le profondità effettive, gli intervalli di campionamento e i criteri QC?
2. I drifter CODE e Stokes sono già stati confrontati con HFR-NAdr? Esiste un periodo con sovrapposizione temporale e spaziale documentata?
3. Quali dataset indipendenti — ADCP, boa Vida, drifter, campionamenti di microplastiche — sono realisticamente accessibili e con quali tempi?
4. Quale parte del progetto considerate più interessante e quale andrebbe ridimensionata per rendere il primo studio pilota più solido?
5. Avrebbe senso preparare una prima nota tecnica congiunta, limitata a dati, area, protocollo e ipotesi verificabili? Chi potrebbe essere il referente per ciascuna linea?

---

## Promemoria del relatore: confini da non oltrepassare

- Non descrivere il pilot HFR attuale come modello di trasporto delle microplastiche validato.
- Non dire che il codice del pilot implementa già diffusione, settling, trasporto verticale, deposizione o biofouling.
- Non presentare i campi riflettenti/assorbenti del crop come una costa fisica.
- Non affermare che i prodotti Copernicus contengano già osservazioni nel dominio pilota: serve la query piattaforma-tempo-spazio.
- Non usare HFR dello stesso sistema come validazione indipendente del campo HFR che lo forza.
- Non aggregare CODE e Stokes in un'unica classe di drifter.
- Non trasferire automaticamente i risultati su xanthan/carragenina agli EPS naturali.
- Presentare M2 come estensione condizionale, subordinata a misure sperimentali.

**FLN**
