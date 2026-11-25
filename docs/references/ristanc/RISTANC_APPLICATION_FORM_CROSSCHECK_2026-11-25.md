# RISTANC — cross-check del formulario con dossier e documenti della call

Data: 25 novembre 2026  
Repository: `fabianleonaressi95/rheomarine`  
Fonti interne confrontate:
- `02_APPLICATION_FORM_FULL_TEXT.md`
- `02_APPLICATION_FORM_FIELD_MAP.md`
- `docs/references/ristanc/RISTANC_DOCUMENTS_AUDIT_2026-11-25.md`
- `docs/references/ristanc/RISTANC_EVALUATION_REVIEW_2026-11-25.md`
- `docs/references/ristanc/RISTANC_ETHICS_REVIEW_2026-11-25.md`
- `docs/references/ristanc/RISTANC_QA_2026-11-05_REVIEW.md`
- `docs/ristanc/application-support/RISTANC_BUDGET_AUDIT.md`
- `docs/ristanc/application-support/RISTANC_GAP_ANALYSIS.md`
- `docs/ristanc/application-support/ADMINISTRATIVE_OPEN_QUESTIONS.md`

## 1. Esito sintetico

Il testo estratto contiene le principali sezioni del formulario: applicant, conflitti/etica/doppio finanziamento, progetto, piano finanziario, entrate, dichiarazione e allegati. È sufficiente per un primo cross-check sostanziale.

Non è però ancora una base affidabile per la compilazione automatica: la field map ha errori strutturali, alcune richieste esplicite del formulario non sono trasformate in attività operative, e il budget corrente è aggregato in modo più generico di quanto consenta la tabella finanziaria.

I file di estrazione risultano nel commit più recente alla radice del repository, non nei percorsi `docs/references/ristanc/` originariamente previsti.

## 2. Correzioni necessarie alla field map

### 2.1 Struttura della tabella

La field map presenta righe con un numero di celle diverso dalle sette colonne dichiarate nell'intestazione. Inoltre raggruppa impropriamente A.1, A.2, A.3 e Section B sotto l'etichetta generica `Section A/B — Applicant`.

Correzione:
- distinguere A.1 — legal entity;
- distinguere A.2 — natural person;
- distinguere A.3 — contact person;
- distinguere B — conflict of interest, ethical aspects, double funding;
- distinguere C — project idea;
- distinguere financial plan, income, statement, annexes, date/signature.

Per il caso di candidatura individuale, A.2 è la sezione anagrafica da compilare; A.1 è esplicitamente da lasciare vuota. A.3 si compila solo se la persona di contatto è diversa dal richiedente.

### 2.2 Campi non mappati o mappati in modo incompleto

La field map deve includere espressamente:
- dichiarazione di accuratezza dei dati e delle condizioni di partecipazione;
- presa d'atto del GDPR e dell'informativa privacy;
- data e firma del richiedente persona fisica;
- caselle Yes/No e testo di dichiarazione della Section B;
- righe per altre entrate/fonti di finanziamento e relativo importo;
- campo descrittivo associato a OTHER negli allegati;
- istruzione condizionale di A.3 e istruzioni per lasciare A.1 vuota nel caso di persona fisica.

La field map non dovrebbe indicare soltanto le righe del piano finanziario: deve anche descrivere le colonne UNIT, UNIT COST e TOTAL COSTS e la riconciliazione tra costi e fonti di finanziamento.

### 2.3 Ambiguità grafica della Section B

Nel testo estratto la domanda sui conflitti contiene:
- una casella per confermare l'assenza di conflitti;
- una casella per dichiarare un conflitto e descriverlo;
- un impegno a comunicare conflitti sopravvenuti;
- un'ulteriore coppia Yes/No.

La disposizione logica di queste ultime caselle non è del tutto chiara nella trascrizione lineare. Prima di spuntare il DOCX originale, controllare visivamente la tabella e non selezionare risposte contraddittorie. La dichiarazione deve coprire applicant e, se presenti, partner, dipendenti e subappaltatori proposti, in coerenza con la FAQ del 5 novembre.

## 3. Corrispondenza tra formulario e progetto RheoMarine

| Campo del formulario | Contenuto da predisporre | Stato / vincolo |
|---|---|---|
| Project title | Titolo breve che identifichi RheoMarine-SLO e il focus sulle acque territoriali slovene | Da finalizzare |
| Project duration | 8 mesi | Coerente con il dossier; la decorrenza effettiva è dalla firma dell'accordo, non va fissata unilateralmente al 1 gennaio |
| Project relevance | Sfida 3: inquinamento marino/plastiche; spiegare il nesso concreto con mare territoriale sloveno e costa | Priorità alta; non basta scrivere genericamente Nord Adriatico |
| Objectives | Obiettivo falsificabile e indicatori di successo per M0/M1 e M2 solo condizionale | Da sintetizzare in 1 obiettivo e 2–4 indicatori |
| Implementation plan | WP1–WP4, attività, tempi relativi, milestone, deliverable, dipendenze e fallback | Integrare copertura HFR, accesso al laboratorio e decision gate M2 al mese 4 |
| Innovation | Novità nell'architettura comparativa e nella validazione locale, non una nuova legge reologica già dimostrata | Evitare di affermare che l'acqua marina è in generale non-Newtoniana |
| Impact | Benefici, target group, bisogni, cambiamenti attesi e numero stimato di persone raggiunte per gruppo | Lacuna importante: il dossier non quantifica ancora la reach per ciascun target group |
| Sustainability | Accesso a codice, metadati, dati utilizzabili, licenze e riuso dopo il progetto | Non promettere manutenzione istituzionale non concordata |
| Competencies and experience | Competenze documentabili del richiedente e ruolo di eventuali partner | Non presentare OGS o singoli ricercatori come partner senza consenso; distinguere fornitore da partner |

### 3.1 Impatto: integrazione obbligatoria nella risposta

Il formulario non chiede soltanto di descrivere l'impatto: chiede anche una stima del numero di persone raggiunte in ciascun gruppo target. La risposta dovrà quindi includere una tabella sintetica con:
- gruppo target;
- bisogno affrontato;
- output/beneficio concreto;
- modalità di raggiungimento;
- numero stimato di persone.

Le stime devono derivare da attività realmente pianificate (ad esempio partecipanti a un briefing, destinatari di una nota tecnica, utenti potenziali del repository), non da numeri di audience inventati né da adesioni istituzionali non ottenute.

### 3.2 Piano di implementazione

Il formulario chiede attività di preparazione, implementazione e promozione. Il WP4 deve quindi esplicitare la disseminazione/promozione dei risultati, con output e pubblico identificati. Usare mesi relativi alla firma dell'accordo; indicare che il progetto dura otto mesi e che il completamento resta entro il termine della call.

### 3.3 Partner e Section C.7

La FAQ del 5 novembre consente di descrivere i partner nella sezione C.7 senza allegati amministrativi o firme separate del partner; il lead applicant resta responsabile. Nel testo estratto non compare la numerazione esplicita C.7, ma la settima voce narrativa è “Competencies and experience” e corrisponde funzionalmente a tale sezione.

Per la candidatura corrente non attribuire a OGS un ruolo di partner già confermato. Un laboratorio può essere trattato come fornitore/subappaltatore B.1, sulla base di preventivo e procedura trasparente, oppure come partner soltanto dopo un accordo effettivo e una descrizione condivisa del ruolo.

## 4. Audit del piano finanziario

Il formulario specifica queste righe:
- A.1 Employees (or equivalent staff);
- A.2 Natural persons under direct contract;
- A.3 SME owners and natural persons recipients;
- B.1 Direct costs of subcontractors;
- C.1 Travel and subsistence;
- C.2 Equipment;
- C.3 Consumables;
- C.4 Costs of organising meetings and seminars;
- C.5 Costs of communication activities;
- C.6 Other;
- E. Indirect costs (25% × (A+C)).

Il budget di lavoro corrente è aritmeticamente coerente:

| Voce | Importo EUR | Valutazione |
|---|---:|---|
| A.3 | 6.600 | Coerente con applicant persona fisica; indicare quantità/unità e costo unitario, costo complessivo lordo per oneri applicabili |
| B.1 | 3.000 | Servizio esterno/laboratorio; ancora da sostenere con preventivo e descrizione di metodi/output/IVA |
| C | 600 | Importo non ancora allocato alle sottovoci C.1–C.6; deve essere dettagliato senza inventare acquisti |
| E | 1.800 | 25% × (6.600 + 600) = 1.800; B.1 esclusa dalla base |
| Totale | 12.000 | Somma coerente e pari al massimale |

### 4.1 Azioni necessarie sul budget

1. Non lasciare la voce C come aggregato generico: assegnare i 600 EUR alle sottovoci C.1–C.6 sulla base di spese reali, documentabili e necessarie. Se non esistono costi in una sottovoce, lasciarla a zero.
2. Per A.3 indicare quantità e costo unitario. La FAQ richiede una quantità (ore o mesi) e il relativo costo unitario. Il totale di 6.600 EUR è lordo complessivo (“bruto bruto/bruto 2”) per imposte e contributi applicabili: non presentarlo come netto e non sottrarre automaticamente IVA o contributi.
3. Per B.1 ottenere un preventivo che identifichi attività, metodi, campioni, deliverable, tempi, costo e trattamento IVA. Il preventivo è evidenza di congruità e pianificazione anche se il grant è lump sum.
4. Verificare che i consumabili eventualmente inclusi nel preventivo B.1 non siano duplicati nella voce C.3.
5. Compilare UNIT, UNIT COST e TOTAL COSTS in modo coerente per ogni riga usata.
6. La tabella INCOME deve riportare le altre entrate/fonti che contribuiscono al progetto, il funding requested e il totale. Il totale delle entrate deve riconciliarsi con il totale dei costi. Dichiarare correttamente l'assenza di altre fonti se non ve ne sono; non confondere dataset pubblici preesistenti con un secondo finanziamento delle stesse attività.
7. Mantenere il budget totale entro EUR 7.500–12.000. Non cambiare il totale senza una decisione motivata e una nuova verifica delle categorie.

## 5. Etica, dichiarazioni e allegati

- Spuntare la presa d'atto etica solo dopo aver letto il documento Ethical Aspects e assumendo l'impegno di rispettarlo.
- Il consenso RISTANC collegato al processo di ricerca è distinto da eventuali consensi GDPR per interviste, registrazioni o fotografie condotte dal progetto.
- Il progetto, come attualmente definito, deve dichiarare con precisione l'uso di dati ambientali e test di laboratorio contenuti; nessun rilascio di microplastiche o polimeri nell'ambiente.
- Se non sono previsti partecipanti umani, interviste o raccolta di dati personali nell'attività scientifica, dichiararlo senza inventare un work package di coinvolgimento.
- La dichiarazione di doppio finanziamento riguarda il progetto e ogni sua parte: verificare l'assenza di sovrapposizione con altri fondi pubblici e dichiarare correttamente eventuali fonti che contribuiscono alle attività.
- La lista allegati del formulario menziona estratto AJPES/registro e statuto per persone giuridiche, procura se la domanda è presentata da un soggetto diverso dal richiedente/rappresentante e OTHER. Per una persona fisica, gli allegati specifici delle persone giuridiche non vanno trattati come applicabili automaticamente.
- Il formulario non elenca esplicitamente un CV tra gli allegati obbligatori. Il criterio di valutazione 6 richiede però evidenza delle competenze: preparare un CV pertinente e verificare se inserirlo come OTHER sia ammesso/utile, senza dichiararlo obbligatorio.
- La firma e la dichiarazione di accuratezza sono sostanziali: verificare il formato di firma accettato e compilare data/firma secondo le istruzioni.

## 6. Questioni aperte da non risolvere per supposizione

1. Chiarire la resa grafica della Section B nel DOCX originale, in particolare la coppia Yes/No finale.
2. Verificare se la modulistica ufficiale ha una numerazione C.7 esplicita nell'originale; la trascrizione presenta sette prompt narrativi ma non le etichette C.1–C.7.
3. Chiedere/confermare se il CV possa essere allegato sotto OTHER e se vi siano eventuali istruzioni integrative di compilazione.
4. Completare la quantificazione dei target group e il piano di disseminazione.
5. Ottenere il preventivo di laboratorio e chiudere la ripartizione C.1–C.6.
6. Confermare copertura HFR, periodo e dati indipendenti per l'area slovena.
7. Prima della firma, leggere il funding agreement effettivo per classificazione fiscale, previdenziale, IVA, ritenute e tutela dell'IP preesistente.

## 7. Priorità operative

**P0 — prima di compilare**
- correggere la field map;
- confermare la lettura grafica della Section B;
- usare A.2 per applicant persona fisica e lasciare A.1 vuota;
- ripartire C=600 sulle sottovoci corrette, sulla base delle spese reali;
- indicare quantità e unit cost per A.3;
- riconciliare costi e income.

**P1 — per la qualità della candidatura**
- rendere esplicito il perimetro del mare territoriale sloveno;
- aggiungere numeri realistici per i target group;
- rendere misurabili obiettivi e milestone;
- aggiungere promozione/disseminazione al piano;
- documentare competenze senza attribuire partnership non confermate.

**P2 — prima dell'invio/firma**
- controllare allegati e firma;
- acquisire preventivo e chiarimenti amministrativi;
- verificare il funding agreement e la posizione fiscale/contributiva;
- fare un controllo finale di doppio finanziamento, conflitti e licenze.

## 8. Limiti di questo cross-check

Questo documento confronta la trascrizione Markdown disponibile con gli audit e le note presenti nel repository. Non sostituisce un'ispezione visiva del DOCX originale: le immagini incorporate e la disposizione grafica della Section B non sono state qui verificate. Il testo della FAQ inglese è una traduzione automatica secondo l'audit esistente; in caso di divergenze prevale il testo sloveno ufficiale. Nessun campo è stato compilato e nessun importo è stato modificato.
