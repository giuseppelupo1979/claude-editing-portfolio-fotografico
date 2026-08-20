# editing-portfolio

**Skill per Claude, ottimizzata per Claude Cowork e Claude Code.**
Fa su un insieme di fotografie il lavoro che un fotografo non riesce a fare sul
proprio archivio: misura ogni file, sceglie, trova il filo che tiene insieme le
immagini, costruisce la sequenza di un libro, scrive i testi e dice all'autore cosa
ripete senza accorgersene.

Non è un generatore di complimenti. È un photo editor: giudica ogni fotografia per
quello che fa dentro un insieme, e quando la foto più bella è quella da togliere lo
dice, con il motivo.

---

## Indice

1. [A chi serve e perché](#1-a-chi-serve-e-perché)
2. [Installazione](#2-installazione)
3. [Come si usa, in pratica](#3-come-si-usa-in-pratica)
4. [Le sette modalità](#4-le-sette-modalità)
5. [La pipeline in sei fasi](#5-la-pipeline-in-sei-fasi)
6. [Punteggi, assi e verdetti](#6-punteggi-assi-e-verdetti)
7. [Cosa produce](#7-cosa-produce)
8. [Il provino interattivo](#8-il-provino-interattivo)
9. [I cinque script](#9-i-cinque-script)
10. [Le misure oggettive](#10-le-misure-oggettive)
11. [Il contratto dati: analisi.json](#11-il-contratto-dati-analisijson)
12. [I sette file di riferimento](#12-i-sette-file-di-riferimento)
13. [I due testi che non vanno confusi](#13-i-due-testi-che-non-vanno-confusi)
14. [Sequenza, ritmo, copertina](#14-sequenza-ritmo-copertina)
15. [I tre vincoli di fondo](#15-i-tre-vincoli-di-fondo)
16. [Requisiti e dipendenze](#16-requisiti-e-dipendenze)
17. [Problemi frequenti](#17-problemi-frequenti)
18. [Rapporto con critica-fotografica](#18-rapporto-con-critica-fotografica)
19. [Licenza e crediti](#19-licenza-e-crediti)

---

## 1. A chi serve e perché

A un fotografo che ha una cartella di fotografie e tre problemi che non può risolvere
da solo.

**Il primo: non vede più le proprie immagini.** Ricorda la sveglia alle quattro, il
freddo, i chilometri, e quel ricordo si sovrappone alla fotografia. Un'immagine che è
costata fatica sembra migliore di quello che è, e un'immagine venuta per caso sembra
meno importante di quello che è.

**Il secondo: non sa cosa ripete.** Su una singola fotografia si può dire cosa è
andato storto. Su sessanta si può dire cosa va storto **sempre**, e solo quello si può
correggere. Se un bordo è sporco in una immagine è un incidente; se lo è in un terzo
dell'insieme è un'abitudine motoria, e le abitudini si correggono con un esercizio.

**Il terzo: non conosce la propria tesi.** Quello che un autore crede di aver
fotografato e quello che ha fotografato coincidono raramente. La cosa che ritorna in
tutte le immagini senza che nessuno l'abbia decisa è il progetto vero, e di norma
l'autore è l'ultima persona a vederla.

La skill affronta i tre problemi con tre strumenti: **misure** invece di impressioni,
**conteggi di frequenza** invece di aggettivi, e un **passaggio cieco** registrato
prima di guardare qualunque dato tecnico.

---

## 2. Installazione

### Claude Cowork, app desktop

Apri il file `editing-portfolio.skill` presente in questo repository e salvalo quando
l'app lo propone. È un archivio già impacchettato e non richiede altro.

### Claude Code

```bash
git clone https://github.com/giuseppelupo1979/claude-editing-portfolio-fotografico.git
cp -r claude-editing-portfolio-fotografico/editing-portfolio ~/.claude/skills/
```

La skill si attiva da sola quando indichi una cartella di fotografie o quando parli di
portfolio, selezione, editing, sequenza, libro fotografico, didascalie, gallerie o
concorsi. Non serve richiamarla per nome.

### Gli script da soli, senza Claude

Ogni script funziona anche fuori dalla skill, come utility a riga di comando. Vedi la
[sezione 9](#9-i-cinque-script).

### Aggiornare la skill: il passo che si dimentica

**Aggiornare il repository non aggiorna la skill installata.** Sono due copie
distinte: il repository avanza a ogni commit, l'account di Claude resta fermo
all'ultimo pacchetto `.skill` caricato a mano. Da dentro una conversazione questa
differenza non si vede, e il risultato è una sessione che lavora con regole vecchie
convinta di avere quelle nuove.

È già successo, il 17 agosto 2026: il repository era arrivato al commit `d06feca`
con le descrizioni per immagine, il registro descrittivo e il provino che si spiega
da solo, mentre l'account aveva ancora il pacchetto di undici ore prima. Una sessione
ha prodotto un editing senza didascalie e senza letture di lavoro, e il difetto è
emerso solo dal confronto con un provino precedente.

Perciò, dopo ogni modifica, tre passi in quest'ordine:

```bash
./build-skill.sh                                   # 1. rigenera pacchetto e inventario
git add -A && git commit -m "..." && git push      # 2. pubblica i sorgenti
```

3. Apri le impostazioni delle skill nell'app di Claude e **ricarica
   `editing-portfolio.skill`**.

Lo script `build-skill.sh` assegna una versione (data più progressivo, scritta in
`VERSIONE`), rigenera il pacchetto e riscrive l'inventario dei file dentro
`SKILL.md`. Quell'inventario è la rete di sicurezza: all'inizio di ogni lavoro la
skill si autoverifica confrontando i file presenti con l'elenco dichiarato, e se ne
manca uno si ferma invece di improvvisare.

---

## 3. Come si usa, in pratica

La convenzione consigliata, da impostare una volta e riusare sempre:

```
Portfolio-Analisi/
└── nome-progetto/
    ├── (le immagini da analizzare, copiate qui da te)
    └── _analisi/              (creata dalla skill)
        ├── thumbs/            miniature con orientamento corretto
        ├── griglie/           provini a contatto etichettati
        ├── metriche.csv/.json le misure, una riga per immagine
        ├── firma.json         le aggregazioni (focali, ore, orientamenti...)
        ├── coppie_simili.csv  le ridondanze candidate
        ├── passaggio_cieco.md la prima impressione, registrata
        ├── analisi.json       il contratto dati, da conservare
        ├── report.md          il documento critico
        ├── testi.md           titoli, introduzione, statement, didascalie
        ├── provino.html       il provino interattivo autonomo
        ├── tabella.xlsx       i punteggi per le quattro destinazioni
        └── dummy.pdf          il menabò del libro
```

Il vantaggio è che **scegli cosa analizzare copiando i file in una cartella**, senza
dover selezionare niente a mano. Poi dici a Claude di analizzare quella cartella.

Se in `_analisi` esiste già un `analisi.json` di una sessione precedente, la skill lo
legge e chiude con il **confronto longitudinale**: quali difetti ricorrenti sono
calati, come è cambiata la firma d'autore, quali immagini della selezione precedente
sopravvivono, se la commissione di scatti è stata eseguita.

---

## 4. Le sette modalità

La modalità viene dichiarata in apertura. Se non la specifichi, viene dedotta dal
numero di immagini e dalla richiesta, e dichiarata comunque.

| Modalità | Quando si usa | Cosa produce |
|---|---|---|
| `triage` | archivio grezzo, oltre 100 file, o serve solo scremare | tre pile (dentro, dubbi, fuori), una riga per immagine, più le coppie ridondanti. Massimo 900 parole |
| `insieme` | **predefinita.** Da 3 a 100 immagini, si vuole capire cosa c'è | report completo a 14 punti: singole, corpus, fil rouge, cluster, firma, difetti, crescita |
| `photo-editor` | si parla di libro, dummy, menabò, sequenza | selezione con numero fissato prima, titolo, architettura, sequenza a spread, ritmo, copertina, didascalie, dummy PDF |
| `galleria` | portfolio online, sito, gallerie tematiche | cluster con nome definitivo, ordine di scorrimento, immagine esca, cosa non mettere online |
| `mostra` | stampa e parete | edit corto, immagine manifesto, dimensioni relative, coppie da affiancare, distanze di lettura |
| `concorso` | premi, bandi, candidature | 5 o 10 immagini, statement da 100 parole, lettura da giuria, valutazione onesta delle probabilità |
| `crescita` | si vuole capire come migliorare, o confrontare con un lavoro precedente | firma d'autore, difetti ricorrenti con frequenza, piano, commissione, confronto longitudinale |

Le modalità si sommano: un `photo-editor` include sempre la lettura d'insieme e chiude
sempre con la crescita.

---

## 5. La pipeline in sei fasi

Non è una raccomandazione: è l'ordine che impedisce i tre errori tipici, cioè giudicare
prima di aver guardato tutto, costruire la tesi sulle fotografie preferite, e
confondere impressione e misura.

**F1. Ingestione e misura.** Le immagini entrano nello spazio di lavoro e
`prepara_provino.py` produce miniature, griglie di provino etichettate, le metriche
numeriche e le coppie visivamente simili. Nessun giudizio in questa fase.

**F2. Passaggio cieco.** Si guardano **solo le griglie**, senza aprire metriche né
EXIF, e si registra per iscritto: le tre immagini che fermano l'occhio, le tre che
scivolano, la sensazione dominante in una frase. Il file `passaggio_cieco.md` viene
scritto adesso e non si riscrive dopo.

**F3. Lettura singola.** Si aprono le miniature e si valuta ogni immagine sui sei
assi. Qui si scrive anche la **descrizione** di ogni immagine sottoposta, scarti
compresi.

**F4. Lettura d'insieme.** Fil rouge a tre livelli, cluster, ridondanze misurate,
lacune, firma d'autore involontaria, difetti ricorrenti con frequenza.

**F5. Costruzione.** Selezione, ordine, gallerie secondo la destinazione, poi i testi:
tre titoli candidati, introduzione, statement, didascalie.

**F6. Consegna.** In chat **e** sul disco, dentro `_analisi`, accanto alle fotografie.

### La divergenza cieco / ragionato

È la diagnosi più utile che la skill produce, e nasce dal confronto fra la prima
impressione della fase F2 e la classifica ragionata della fase F3.

| Categoria | Cosa significa | Cosa farne |
|---|---|---|
| **esca che non tiene** | colpisce a freddo, scende dopo l'analisi | funziona come copertina o apertura, non come nucleo |
| **a lenta combustione** | ignorata a freddo, sale dopo l'analisi | è il cuore possibile del progetto, ma va aiutata dalla posizione in sequenza, non dalla post produzione |
| **stabile in alto** | regge su entrambi i piani | sono le immagini pubbliche |
| **stabile in basso** | non regge su nessuno dei due | non salvarla per affetto |

---

## 6. Punteggi, assi e verdetti

### I sei assi

Voto da 1 a 10. Sono assi diversi da quelli della critica di una singola immagine,
perché in un edit contano cose diverse.

| Asse | La domanda |
|---|---|
| `autonomia` | regge da sola, senza didascalia e senza le altre? |
| `forza` | ferma l'occhio? per quanto? |
| `coerenza` | appartiene alla tesi del corpus, o è un'altra fotografia? |
| `originalita` | quanta distanza dal già visto mille volte? |
| `tecnica` | tenuta esecutiva **rispetto all'intenzione**, non in assoluto |
| `funzione` | cosa fa dentro la sequenza (apertura, nucleo, ponte, pausa, climax, chiusura)? |

### I pesi cambiano con la destinazione

Ed è per questo che la stessa fotografia entra in un libro e non in un concorso.

| Destinazione | autonomia | forza | coerenza | originalita | tecnica | funzione |
|---|---|---|---|---|---|---|
| **libro** | 10 | 20 | **25** | 15 | 10 | **20** |
| **mostra** | 25 | 25 | 15 | 15 | **20** | 0 |
| **portfolio web** | **30** | 25 | 15 | 20 | 10 | 0 |
| **concorso** | 25 | **30** | 10 | **25** | 10 | 0 |

Il conto lo fa `esporta_tabella.py`, che produce i quattro punteggi per ogni immagine.
Le immagini che **cambiano molto di rango** fra libro e concorso sono le più
informative: dicono se l'autore fa fotografie singole o progetti.

### I verdetti

Per immagine, cinque livelli crescenti: **da scartare**, **da archivio**, **da
portfolio**, **da stampa**, **da mostra**. Sono gli stessi di `critica-fotografica`,
così le due skill si parlano.

Per il corpus, sei assi (coerenza della visione, profondità, ampiezza, originalità
della visione, tenuta della sequenza, ambizione realizzata) e cinque livelli:
**archivio personale**, **nucleo da sviluppare**, **progetto pubblicabile**, **progetto
da libro**, **corpus d'autore**.

L'asse *ambizione realizzata* misura la distanza fra ciò che il lavoro tenta e ciò che
ottiene: un progetto modesto perfettamente eseguito prende un voto alto, un progetto
ambizioso a metà strada prende un voto basso e vale di più.

### Le regole del taglio

1. **Il numero prima della scelta.** Senza un numero fissato in anticipo non si sta
   editando, si sta commentando.
2. **Nessuna immagine entra per due motivi deboli.** "Completa il gruppo" più "è
   carina" fa zero.
3. **La ridondanza si taglia sempre**, e le coppie candidate arrivano da un numero.
4. **Kill your darling.** Va individuata l'immagine tecnicamente migliore che va
   tagliata perché non serve la tesi, e va nominata.
5. **L'edit alternativo.** Sempre una seconda selezione, più corta e con un'altra
   tesi. Un photo editor con una sola idea non è un photo editor.
6. **Lo scarto difeso.** L'immagine migliore fra le escluse, con l'edit in cui sarebbe
   centrale.

### I bias passati in rassegna a nome

Costo affondato, bias affettivo, bias tecnico, bias del feedback, bias della novità,
bias del già pubblicato. Vanno nominati uno per uno, dicendo se se ne è trovata
traccia e su quali immagini.

---

## 7. Cosa produce

| File | Cosa contiene |
|---|---|
| `report.md` | il documento critico completo, 14 punti in modalità `insieme` |
| `provino.html` | il provino interattivo autonomo, immagini incorporate, funziona offline |
| `testi.md` | titoli candidati, introduzione, statement, didascalie numerate come tavole, letture di lavoro, segnaposto aperti, referto dei controlli |
| `tabella.xlsx` e `.csv` | i punteggi per le quattro destinazioni, i ranghi, i fogli pesi, sequenza e cluster |
| `dummy.pdf` | il menabò del libro: copertina, spread affiancati, didascalie, indice delle tavole |
| `analisi.json` | il contratto dati, ed è il file che rende possibile il confronto della sessione successiva |
| `metriche.csv/.json` | le misure oggettive, 36 campi per immagine |
| `firma.json` | le aggregazioni: focali, aperture, ISO, ore, orientamenti, chiavi tonali, corpi, ottiche, arco temporale |
| `coppie_simili.csv` | le coppie sotto soglia di somiglianza, con distanza di hash e correlazione di istogramma |
| `griglie/` | i provini a contatto etichettati con gli id |
| `thumbs/` | le miniature con orientamento EXIF applicato |

---

## 8. Il provino interattivo

`provino.html` è un solo file, con le immagini incorporate in base64: funziona offline,
non richiede una connessione, non usa storage del browser e si può archiviare accanto
alle fotografie.

**Vincolo di progetto: la pagina si spiega da sola.** Ogni sezione si apre con la
spiegazione di cosa è e come si legge, e nessun elemento richiede una fonte esterna.
Chi la riapre dopo sei mesi non ha bisogno di ricordare niente.

Sei sezioni:

- **Provino** a contatto con tutte le immagini, filtri per cluster, verdetto e
  categoria del passaggio cieco, ordinamento su ciascuna delle quattro destinazioni,
  ricerca testuale. Sotto ogni fotografia: punteggio, verdetto, ruolo, esito del
  passaggio cieco, didascalia da pubblicare, lettura di lavoro. **Passando il mouse sul
  punteggio** compare la tabella con voti, pesi, contributo di ogni asse e totale.
- **Sequenza** a doppia pagina, come la vedrà il lettore, con le pagine bianche, le
  pagine che contengono più immagini, la proposta di copertina con motivazione e
  alternative, la legenda completa della notazione del ritmo, il perché della forma
  scelta e le alternative scartate.
- **Cluster**, ciascuno con nome, registro, tesi e forza da 1 a 10.
- **Testi**, con il conteggio delle parole e i segnaposto evidenziati.
- **Scarti**, ciascuno con il motivo, perché una selezione senza esclusioni motivate
  non è discutibile.
- **Dati**, la tabella completa, con **anteprima della fotografia passando il mouse sul
  nome del file**.

---

## 9. I cinque script

Tutti accettano `--help`, girano senza rete e non modificano le immagini originali.

### `prepara_provino.py`, sempre il primo passo

```bash
python3 scripts/prepara_provino.py CARTELLA [-o CARTELLA_USCITA]
        [--lato-thumb 1024] [--per-griglia 12] [--lato-griglia 2000]
        [--prefisso P] [--soglia-simili 20]
```

Assegna a ogni immagine un id stabile (`P001`, `P002`, ...) e produce miniature,
griglie, metriche, firma, coppie simili e l'elenco dei file saltati con il motivo.
Gestisce JPEG, PNG, TIFF, WebP, BMP, e con le librerie opzionali anche HEIC e RAW
(NEF, RAF, DNG, ARW, CR2, CR3, ORF, RW2, PEF, SRW). Riconosce le coppie RAW più JPEG
dello stesso scatto e ne analizza una sola, dichiarandolo.

### `esporta_tabella.py`

```bash
python3 scripts/esporta_tabella.py analisi.json [-o CARTELLA_USCITA]
```

Calcola i punteggi ponderati per tutte e quattro le destinazioni, i ranghi, e stampa i
cambi di rango più forti. Valida il contratto: si ferma se un id citato in sequenza,
cluster, gallerie o scarti non esiste fra le immagini.

### `genera_provino_html.py`

```bash
python3 scripts/genera_provino_html.py analisi.json [-o provino.html]
        [--radice CARTELLA] [--lato-griglia 420] [--lato-dettaglio 1000]
```

### `genera_testi.py`

```bash
python3 scripts/genera_testi.py analisi.json [-o testi.md] [--solo-controllo]
        [--parole-min 5] [--parole-max 25]
```

Impagina i testi e passa i controlli automatici, cioè il lavoro che a occhio non si
riesce a fare: lunghezze fuori intervallo, aggettivi valutativi, formule descrittive,
lessico da photo editor finito per errore in una didascalia da pubblicare, ripetizioni
fra didascalie contigue, lunghezze tutte uguali (voce meccanica), parole della lista
nera nei titoli e nei nomi di galleria, segnaposto rimasti aperti, presenza e
lunghezza delle descrizioni, copertina con motivazione e almeno due alternative,
numero di codici di ritmo pari al numero di spread, chiusura non su tensione media,
tre picchi consecutivi, presenza del perché del ritmo e delle alternative.

### `genera_dummy_pdf.py`

```bash
python3 scripts/genera_dummy_pdf.py analisi.json [-o dummy.pdf] [--radice CARTELLA]
        [--pagina 21x26] [--dpi 150] [--senza-didascalie] [--con-descrizioni]
        [--copertina P003]
```

Impagina una pagina PDF per ogni doppia pagina del libro. Avverte quando il numero di
pagine interne non è multiplo di 4 (in stampa a segnature non esiste) e quando non ci
sono pagine bianche.

---

## 10. Le misure oggettive

Per ogni immagine, 36 campi. I più usati:

| Campo | Cosa dice | La trappola |
|---|---|---|
| `larghezza`, `altezza`, `mp` | risoluzione reale dell'originale | è l'unico dato legittimo per parlare di dimensione di stampa |
| `clip_neri_pc`, `clip_bianchi_pc` | percentuale di pixel a 0 e a 255 | un po' di nero pieno è struttura. Sopra il 2 per cento sui bianchi, di norma, è informazione perduta |
| `luminanza_media`, `p5`, `p50`, `p95` | dove sta la massa tonale | serve per la chiave tonale e per la coerenza di una sequenza |
| `contrasto` | deviazione standard della luminanza | basso non è brutto: è piatto, e la piattezza può essere voluta |
| `saturazione_media`, `colorfulness` | quanta materia cromatica | sotto soglia l'immagine viene marcata come probabile bianco e nero |
| `hue_dominante`, `nome_colore` | dominante cromatica | utile per cluster e sequenze, non per giudicare il bilanciamento del bianco |
| `nitidezza`, `nitidezza_rango_pc` | varianza del laplaciano e percentile nel gruppo | calcolata sulla miniatura: confronta immagini fra loro, non misura l'ottica |
| `rumore_proxy` | scarto sulle zone più piatte | stima, non misura. Cresce con la grana voluta esattamente come col rumore indesiderato |
| `entropia` | densità di informazione | alta significa affollata, non ricca |
| `chiave_tonale` | bassa, media, alta | è la chiave della scena o dello sviluppo? va distinto |
| `dhash` | impronta visiva percettiva | serve solo per le distanze fra coppie |
| EXIF | corpo, ottica, focale, focale equivalente, apertura, tempo, ISO, data, ora | se il campo non c'è nel file, il campo non esiste. Mai inventarlo |

### Le ridondanze, interpretate

| Distanza dhash | Significato | Cosa fare |
|---|---|---|
| 0 a 5 | quasi identiche, spesso raffiche | tenerne una, sempre |
| 6 a 12 | stessa idea a mezzo passo | tenerne una, salvo funzione diversa dichiarata |
| 13 a 20 | stessa struttura, contenuto diverso | può essere variazione utile: verificare guardando |
| oltre 20 | non correlate visivamente | ignorare il dato |

L'hash misura la forma, non il senso: il numero apre la domanda, non la chiude. Quando
la distanza è bassa ma la correlazione di istogramma è bassa, la coppia viene marcata
come "forma simile, tono diverso".

### La firma d'autore involontaria

`firma.json` aggrega focali, aperture, ISO, ore del giorno, orientamenti, chiavi
tonali, colori dominanti, corpi, ottiche, arco temporale e giorni attivi. Da qui
escono le osservazioni che l'autore non può fare da solo: quali focali usa sempre,
in quali ore esce con la macchina, cosa **non** fa mai. Le assenze sistematiche sono
il dato più prezioso, e quasi sempre involontarie.

---

## 11. Il contratto dati: analisi.json

Claude fa il lavoro di vedere e giudicare, gli script fanno i conti e l'impaginazione.
Il file è leggibile e modificabile a mano: se cambi un voto o riordini la sequenza,
basta rilanciare gli script.

```json
{
  "progetto": {
    "titolo": "Nessuno al terzo piano",
    "sottotitolo": "opzionale",
    "autore": "Nome Cognome",
    "modalita": "photo-editor",
    "destinazione": "libro",
    "fil_rouge": "una frase, non un tema generico",
    "titoli_candidati": [
      {"titolo": "...", "registro": "obliquo", "motivazione": "una riga"}
    ],
    "introduzione": "da 250 a 500 parole, quattro movimenti",
    "registro_introduzione": "scena madre",
    "statement": "da 60 a 120 parole, altra cosa dall'introduzione",
    "nota_autore": "opzionale, da 80 a 150 parole",
    "registro_didascalie": "descrittivo",
    "copertina": "P017",
    "copertina_motivazione": "perché questa e non l'apertura",
    "copertina_alternative": [{"id": "P011", "motivazione": "perché perde"}],
    "cartella_thumbs": "thumbs"
  },
  "immagini": [
    {
      "id": "P007",
      "file": "DSCF1234.jpg",
      "thumb": "thumbs/P007_DSCF1234.jpg",
      "genere": "street",
      "voti": {"autonomia": 8, "forza": 9, "coerenza": 7,
               "originalita": 6, "tecnica": 7, "funzione": 8},
      "verdetto": "da portfolio",
      "ruolo": "climax",
      "descrizione": "obbligatoria per OGNI immagine, 30 a 100 parole",
      "didascalia": "solo per l'edit, nel registro dichiarato",
      "forza_principale": "una frase",
      "limite_principale": "una frase",
      "cluster": ["attese"],
      "registro_tonale": "scuro",
      "densita": "alta",
      "cieco": "esca"
    }
  ],
  "cluster": [
    {"id": "attese", "nome": "Nessuno al terzo piano", "registro_nome": "obliquo",
     "tesi": "una frase", "immagini": ["P007", "P011"], "forza": 8}
  ],
  "sequenza": {
    "spread": [["P003", null], ["P007", "P011"], [null, ["P020", "P021"]]],
    "ritmo": "A= M+ B-",
    "ritmo_perche": "quale caratteristica del materiale impone questa forma",
    "alternative": [
      {"nome": "Alternata a picchi", "ritmo": "A= M- A+ B-", "perche": "perché scartata"}
    ]
  },
  "scarti": [{"id": "P010", "motivo": "ridondante con P007, più debole sui bordi"}],
  "gallerie": [
    {"nome": "Nessuno al terzo piano", "ordine": ["P007", "P011"], "esca": "P007"}
  ]
}
```

Regole: gli id sono quelli assegnati da `prepara_provino.py` e non si cambiano; in
`spread` un `null` è una pagina bianca (il respiro, e serve); una pagina può contenere
più immagini scrivendola come lista; ogni id citato deve esistere in `immagini`, e gli
script si fermano se non è così.

---

## 12. I sette file di riferimento

Sono la conoscenza di dominio, letta solo quando serve.

| File | Contenuto |
|---|---|
| `ingestione.md` | convenzione di cartella, lotti, RAW e HEIC, formati difficili, lettura critica delle metriche, doppia consegna in chat e su disco |
| `connettori.md` | il fil rouge a tre livelli, le **diciotto specie di connettore**, come si costruisce un cluster, le tre prove di robustezza (decapitazione, intruso, titolo cieco), ridondanza contro variazione, le lacune come commissione, quando ammettere che sono due progetti |
| `sequenza.md` | l'unità è lo spread, la notazione del ritmo, le tre architetture (lineare, a movimenti, a spirale), otto regole di adiacenza, apertura e chiusura, il respiro, aritmetica delle segnature, sequenza a parete, scorrimento su schermo, quattro prove di verifica, pagine con più immagini, la copertina, dichiarare ragioni e alternative |
| `didascalie.md` | la distinzione fra descrizione e didascalia, i **sei registri** di didascalia, i cinque registri di titolo, la **lista nera** dei titoli fotografici italiani consumati, lo statement, l'introduzione alla raccolta con i cinque registri e i quattro movimenti, la procedura per scrivere tutte le didascalie in un blocco, il controllo automatico, le regole della descrizione |
| `destinazioni.md` | numeri e criteri per libro, mostra, portfolio online e concorsi: cosa premia e cosa punisce ciascuna, criterio decisivo, cosa consegnare, e cosa fare quando la destinazione richiesta è quella sbagliata |
| `canone-editing.md` | il canone dell'**editing**, non della singola immagine: ogni autore codificato come problema di corpus risolto, con pertinenza, quando non citarlo ed errore dell'imitatore. Più gli strumenti concettuali (specchio o finestra, fotografia singola o insieme, il metodo della rima, la rotazione dei tipi, il lavoro per coppie) |
| `autodiagnosi.md` | la firma d'autore involontaria, come leggere `firma.json`, la tassonomia dei **diciotto difetti ricorrenti** con le soglie di frequenza, come si passa dalla frequenza all'esercizio, la commissione, il confronto longitudinale, come dirlo senza scoraggiare |

---

## 13. I due testi che non vanno confusi

È l'equivoco più frequente di tutto il lavoro, quindi la skill tiene i due testi
separati e li etichetta ovunque compaiano.

| | `descrizione` | `didascalia` |
|---|---|---|
| **per chi** | per l'autore, mentre lavora | per il lettore, nel libro o in mostra |
| **cosa dice** | cosa si vede e cosa fa fotograficamente | quel poco che la fotografia non può contenere |
| **quante** | una per **ogni** immagine analizzata, scarti compresi | solo per le immagini dell'edit |
| **lunghezza** | da 30 a 100 parole | da 15 a 50 nel registro descrittivo, da 5 a 25 negli altri |
| **contiene giudizi** | sì, è il suo mestiere | **mai**, per nessun motivo |
| **si pubblica** | no | sì |

I sei registri di didascalia: **muto** (solo luogo e data), **descrittivo** (racconta al
lettore cosa sta guardando, l'unico in cui descrivere è consentito), **fattuale**,
**contestuale**, **obliquo**, **citazionale**. Uno solo per progetto, dichiarato.

Regola di onestà che vale in entrambi: nessun luogo, nome o fatto viene affermato senza
certezza. Quello che non si sa diventa un segnaposto `[luogo]`, `[nome]`, che viene
contato ed elencato perché lo compili l'autore. E quando una manipolazione cambia ciò
che il lettore crede di vedere, la didascalia descrittiva lo dichiara in una riga: una
descrizione che tace una manipolazione è una descrizione falsa.

---

## 14. Sequenza, ritmo, copertina

### La notazione del ritmo

Due caratteri per ogni doppia pagina. Primo carattere, la **tensione**: `A` alta, `M`
media, `B` bassa. Secondo carattere, la **densità visiva**: `+` affollata, `=` media,
`-` vuota.

Esempio: `A= A+ M+ M= M- B-`

I difetti da cercare leggendo solo la stringa: nessuna `A` nelle prime due posizioni
(il lettore non entra), tre `A` di fila (dal terzo picco non si sentono più i picchi),
quattro `B` di fila (il libro si è spento), tutte `+` (affaticamento), tutte `=` (il
ritmo non esiste), ultima posizione `M` (finale senza intenzione: si chiude in alto col
colpo o in basso con la dissolvenza).

Il ritmo non si dichiara e basta: si consegna con la legenda, con il perché ricavato dal
materiale e con da due a tre alternative scartate, ciascuna con la propria stringa e il
motivo del rifiuto.

### La copertina

Va sempre proposta con motivazione e almeno due alternative, ed è **una scelta distinta
dall'apertura**: l'apertura lavora dentro la sequenza, la copertina lavora prima che il
libro sia aperto. I cinque criteri, in ordine di peso: tiene in piccolo, ha una zona
pulita per il titolo, regge fuori contesto, incuriosisce senza raccontare, appartiene al
tono. Conseguenza quasi sempre vera: **la copertina non è la fotografia migliore**,
perché la migliore va protetta dentro il libro.

---

## 15. I tre vincoli di fondo

Attraversano ogni parte della skill e sono la ragione per cui è scritta così.

### Protocollo epistemico

Ogni affermazione è classificata su sei livelli. `[MISURATO]` viene dai dati e si cita
con il valore; **osservato** è il livello predefinito e non si marca; `[RICAVATO]` si
marca quando la deduzione regge un giudizio importante; `[STIMATO]` e `[NON
DETERMINABILE]` si marcano sempre; `[INTERPRETATO]` basta dichiararlo a inizio sezione.

Un modello linguistico che parla di fotografia sbaglia quasi sempre nello stesso punto,
cioè presenta come misura ciò che è impressione. I numeri veri servono a rendere la
distinzione possibile. Vale anche il rovescio: **un numero non è un giudizio**. Un
contrasto basso non è un difetto se l'immagine cerca la piattezza, e una nitidezza
bassa su un mosso voluto è una conferma, non un rilievo.

### Anti normalizzazione

Non si spingono le immagini verso ordine, pulizia, simmetria e leggibilità. Grana,
mosso, buio, disequilibrio e caos possono essere la lingua del lavoro: la domanda non è
"è pulito" ma "serve". Corollario sul corpus: la coerenza non è il valore più alto, e un
fil rouge trovato a forza che costringe a buttare le due immagini più originali è un fil
rouge sbagliato. Meglio ammettere che nella stessa cartella ci sono due progetti.

### Anti invenzione

Mai EXIF inventati, mai istogrammi simulati, mai luoghi o persone riconosciuti senza
certezza, mai citazioni attribuite a fotografi senza certezza della fonte, mai una
dimensione di stampa dedotta da una miniatura, mai un fatto messo in un testo per farlo
suonare meglio. E mai dire di aver guardato immagini che non si sono aperte: se si sono
viste solo le griglie, il giudizio è a bassa risoluzione e va dichiarato.

---

## 16. Requisiti e dipendenze

Python 3.8 o superiore.

```bash
pip install pillow numpy openpyxl      # necessari
pip install rawpy pillow-heif          # opzionali: file RAW e HEIC
```

`openpyxl` serve solo per il file `.xlsx`: senza di esso viene prodotto il CSV e lo
script lo dichiara. `rawpy` e `pillow-heif` servono solo per RAW e HEIC: senza di esse
quei file vengono elencati fra i saltati con il motivo, e l'analisi prosegue.

Nessuno script richiede rete. Nessuno script modifica le immagini originali: la cartella
di partenza viene solo letta.

---

## 17. Problemi frequenti

**Le miniature sono ruotate male.** Lo script applica l'orientamento EXIF; se una
immagine resta girata, il file ha metadati incoerenti. Va corretto a mano e segnalato:
non si giudica la composizione di una fotografia ruotata.

**Tutti i file hanno la stessa data e ora.** Sono passati da un software che ha
riscritto i metadati. La ricostruzione temporale del progetto non è determinabile, e va
detto invece di inventare una cronologia.

**Nessun EXIF.** Capita con export che rimuovono i metadati, screenshot e immagini
scaricate. La parte di firma d'autore basata su focali, aperture e ore non si può fare;
quella basata sui numeri visivi (chiave tonale, orientamento, densità, colore) sì.

**Ci sono RAW e non vengono letti.** Installa `rawpy`. Nota che il RAW viene sviluppato
in modo neutro a mezza risoluzione, quindi le misure di luminosità, contrasto e
saturazione sono quelle del file non sviluppato: utili per capire i margini di recupero,
non per giudicare il colore. Se esistono i JPEG o i TIFF sviluppati, meglio quelli:
per l'editing servono le immagini nella forma in cui verranno viste.

**Molti file saltati.** Controlla `saltati.csv`: contiene il motivo per ciascuno.
Un'analisi su 47 file quando la cartella ne conteneva 52 senza dirlo è un'analisi
sbagliata, e per questo l'elenco viene sempre riferito.

**Il provino HTML è grosso.** È voluto: le immagini sono dentro il file perché funzioni
offline e sia archiviabile. Si può ridurre con `--lato-dettaglio 700`.

**Il numero di pagine del dummy non è multiplo di 4.** Nella stampa a segnature non
esiste: lo script lo segnala e propone i due numeri validi più vicini.

---

## 18. Rapporto con critica-fotografica

Sono due skill complementari e progettate per incastrarsi.

| Situazione | Skill |
|---|---|
| una immagine sola, parere o critica approfondita | `critica-fotografica` |
| da tre immagini in su, una cartella, un progetto, un archivio | **questa** |
| scheda profonda su una o due immagini chiave emerse dall'edit | `critica-fotografica`, invocata da questa |

Condividono la scala dei cinque verdetti e il protocollo epistemico, quindi i risultati
si sommano invece di contraddirsi. `critica-fotografica` possiede la scheda a tredici
sezioni sul fotogramma e il canone dei problemi di singola immagine; questa possiede il
corpus, la sequenza, i testi e la diagnosi longitudinale.

---

## 19. Licenza e crediti

MIT, vedi `LICENSE`.

Skill scritta per Claude (Cowork e Claude Code) da Giuseppe Lupo con Claude.

I contributi sono benvenuti, in particolare su tre fronti: nuove voci del canone
dell'editing (con il campo *quando non citarlo* compilato, che è la parte che conta),
ampliamenti della lista nera dei titoli, e nuovi controlli automatici in
`genera_testi.py` per errori di testo che si vedono solo a impaginazione fatta.
