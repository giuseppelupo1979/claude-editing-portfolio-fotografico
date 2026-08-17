# editing-portfolio

**Skill per Claude, ottimizzata per Claude Cowork e Claude Code.** Fa su un insieme
di fotografie il lavoro che un fotografo non riesce a fare sul proprio archivio:
misura ogni file, sceglie, trova il filo che tiene insieme le immagini, costruisce la
sequenza di un libro, scrive i testi e dice all'autore cosa ripete senza accorgersene.

Non è un generatore di complimenti. È un photo editor: giudica ogni fotografia per
quello che fa dentro un insieme, e quando la foto più bella è quella da togliere lo
dice.

Per la critica approfondita di una **singola** immagine esiste una skill separata,
`critica-fotografica`, con cui questa si incastra (stessa scala di verdetti, stesso
protocollo epistemico).

## Cosa fa

- **Misura invece di stimare.** Per ogni file: risoluzione reale, clipping di bianchi
  e neri, luminanza, contrasto, saturazione, colore dominante, nitidezza relativa,
  proxy del rumore, entropia, EXIF completi, impronta percettiva.
- **Passaggio cieco obbligatorio.** Guarda i provini prima dei dati e registra la
  prima impressione, poi confronta le due classifiche. Dove divergono c'è la
  diagnosi: esche che non tengono, immagini a lenta combustione, stabili in alto,
  stabili in basso.
- **Fil rouge a tre livelli**: soggetto, sguardo, ossessione. Solo il terzo è una
  tesi, e c'è la prova della decapitazione per verificare che esista davvero.
- **Ridondanze misurate** con hash percettivo: le coppie che dicono la stessa cosa
  vengono fuori con un numero, comprese quelle che l'occhio non vede più.
- **Cluster e gallerie tematiche**, ciascuna con tre nomi candidati e il registro
  dichiarato, più una lista nera dei titoli fotografici italiani ormai consumati.
- **Modalità photo editor**: numero di pagine, titolo, architettura, sequenza a
  spread con notazione del ritmo, apertura e chiusura argomentate, dummy PDF.
- **Testi**: introduzione alla raccolta (250 a 500 parole, cinque registri, quattro
  movimenti), statement, e la didascalia di ogni immagine in un solo registro, con
  controllo automatico su lunghezze, ripetizioni, aggettivi valutativi e segnaposto.
- **Firma d'autore involontaria**: cosa fai sempre e cosa non fai mai, ricavato dai
  numeri (focali, ore del giorno, orientamenti, chiavi tonali).
- **Difetti ricorrenti con frequenza numerica** e tre esercizi da fare in una sola
  uscita, più una commissione di scatti precisi da andare a prendere.

## Le sette modalità

`triage`, `insieme` (predefinita), `photo-editor`, `galleria`, `mostra`, `concorso`,
`crescita`. Si sommano: un photo-editor include sempre la lettura d'insieme.

## Come si usa

Indichi una cartella di fotografie e chiedi di analizzarla. Convenzione consigliata:

```
Portfolio-Analisi/
└── nome-progetto/
    ├── (le immagini)
    └── _analisi/     (creata dalla skill: provino, report, testi, tabella, dummy)
```

Deliverable prodotti: `report.md`, `provino.html` (provino interattivo autonomo, con
filtri, cluster, sequenza a doppia pagina e testi, funziona offline), `testi.md`,
`tabella.xlsx`, `dummy.pdf`, e `analisi.json`, il file che permette il confronto
longitudinale fra una sessione e la successiva.

## Installazione

**Claude Cowork (app desktop).** Apri `editing-portfolio.skill` e salvalo quando
l'app lo propone.

**Claude Code.** Copia la cartella della skill fra le tue skill:

```bash
git clone https://github.com/giuseppelupo1979/claude-editing-portfolio-fotografico.git
cp -r claude-editing-portfolio-fotografico/editing-portfolio ~/.claude/skills/
```

## Dipendenze degli script

```bash
pip install pillow numpy openpyxl
pip install rawpy pillow-heif      # opzionali: file RAW e HEIC
```

| Script | Cosa produce |
|---|---|
| `prepara_provino.py` | miniature, griglie di provino etichettate, `metriche.csv` e `.json`, `coppie_simili.csv`, `firma.json` |
| `esporta_tabella.py` | punteggi ponderati per libro, mostra, web e concorso, `tabella.xlsx` |
| `genera_provino_html.py` | provino interattivo in un solo file HTML, immagini incorporate |
| `genera_testi.py` | `testi.md` e il controllo automatico su titoli, introduzione, statement, didascalie |
| `genera_dummy_pdf.py` | dummy del libro: copertina, spread affiancati, didascalie, indice delle tavole |

Ogni script accetta `--help` e funziona anche da solo, fuori da Claude.

## Struttura

```
editing-portfolio/
├── SKILL.md                    workflow, modalità, pesi, format lock
├── references/
│   ├── ingestione.md           cartelle, lotti, RAW, metriche, consegna
│   ├── connettori.md           fil rouge, 18 specie di connettore, cluster, prove
│   ├── sequenza.md             grammatica dello spread, ritmo, architetture, parete
│   ├── didascalie.md           registri, titoli, lista nera, introduzione, statement
│   ├── destinazioni.md         numeri e criteri per libro, mostra, web, concorso
│   ├── canone-editing.md       chi ha risolto quale problema di corpus
│   └── autodiagnosi.md         firma d'autore, difetti ricorrenti, crescita
└── scripts/                    i cinque script
```

## Perché è scritta così

Tre vincoli attraversano tutta la skill.

**Protocollo epistemico.** Ogni affermazione è classificata: `[MISURATO]` viene dai
dati, l'osservato è il livello predefinito, `[STIMATO]` e `[NON DETERMINABILE]` si
marcano sempre. Un modello linguistico che parla di fotografia sbaglia quasi sempre
nello stesso punto, presentare come misura ciò che è impressione, e qui i numeri
veri servono a rendere la distinzione possibile.

**Anti normalizzazione.** Non spinge le immagini verso ordine, pulizia e simmetria.
Grana, mosso, buio e disequilibrio possono essere la lingua del lavoro: la domanda
non è "è pulito" ma "serve".

**Anti invenzione.** Nessun EXIF inventato, nessun luogo riconosciuto senza certezza,
nessun fatto messo in una didascalia per farla suonare meglio. Quello che non si sa
diventa un segnaposto da compilare, contato e elencato.

## Licenza

MIT. Vedi `LICENSE`.
