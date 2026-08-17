# Sequenza: la grammatica dell'ordine

Una sequenza non è una classifica. Se metti le foto in ordine di bellezza
decrescente hai fatto un catalogo di vendita: comincia forte e poi delude a ogni
pagina. Una sequenza costruisce un'esperienza nel tempo, e il tempo del libro è la
girata di pagina.

## Indice

1. L'unità non è la foto, è lo spread
2. Notazione del ritmo
3. Le tre architetture
4. Regole di adiacenza
5. Apertura e chiusura
6. Il respiro
7. Aritmetica delle pagine
8. Sequenza a parete, che è un'altra cosa
9. Sequenza per scorrimento su schermo
10. Come verificare una sequenza

## 1. L'unità non è la foto, è lo spread

Nel libro il lettore vede due pagine insieme, e non può vederne una sola. Da questo
derivano quasi tutte le regole:

- **Pagina destra (recto)**: è dove cade lo sguardo per prima. Ci va l'immagine
  forte. È anche la pagina che il lettore vede mentre gira, quindi regge la tensione.
- **Pagina sinistra (verso)**: sostiene, contestualizza, contrasta, o resta bianca.
- **Immagine a doppia pagina**: solo per immagini che sopportano la piega al centro.
  Mai su un volto, mai su un soggetto centrale, mai su un dettaglio decisivo. Usala
  al massimo due o tre volte in un libro, per i cambi di movimento.
- **Coppia affiancata**: le due immagini si guardano. Va usata quando la relazione
  fra le due aggiunge un terzo significato, mai per riempire. Attenzione alle
  direzioni: due figure che guardano verso l'esterno spingono il lettore fuori dal
  libro, due che guardano verso il centro lo tengono dentro.

In `analisi.json` la sequenza si scrive come lista di coppie, e `null` è pagina
bianca: `[["P003", null], ["P007", "P011"], [null, "P020"]]`. Il primo elemento è
la sinistra, il secondo la destra. Una pagina bianca a sinistra con immagine a
destra è la configurazione più elegante e la più usata nei libri fotografici seri:
non abusarne, ma è il default sicuro.

## 2. Notazione del ritmo

Serve a vedere la sequenza come struttura invece che come elenco, e va messa nel
report. Per ogni spread annota due lettere:

Tensione: `A` alta, `M` media, `B` bassa.
Densità visiva: `+` affollata, `=` media, `-` vuota.

Esempio di sequenza sana: `M= A+ M- B- A= A+ M= B- A+ M= B-`

Cosa cercare nella stringa:

- **Nessuna A nelle prime due posizioni**: apertura troppo prudente, il lettore non
  entra.
- **Tre A di fila**: saturazione. Dopo il terzo picco il lettore smette di sentire i
  picchi, e la quarta immagine forte lavora come una media.
- **Quattro B di fila**: la sequenza si è spenta, il lettore chiude il libro.
- **Tutte `+`**: affaticamento visivo, servono vuoti.
- **Tutte `=`**: il ritmo non esiste, il libro è piatto anche se le foto sono buone.
- **Ultima posizione non A e non B**: finale senza intenzione. Le chiusure funzionano
  o in alto (colpo finale) o in basso (dissolvenza), mai in mezzo.

Se la stringa sta bene ma il libro non funziona, il problema è di contenuto, non di
ordine, e va detto.

## 3. Le tre architetture

Scegline una e dichiarala. Mischiarle è la ragione più comune per cui una sequenza
sembra casuale.

**Lineare.** Segue un vettore: tempo, percorso geografico, avvicinamento progressivo
(dal generale al dettaglio), luce che cala. Facile da seguire, rischia la
prevedibilità. Serve almeno una rottura a metà, altrimenti il lettore anticipa ogni
pagina.
Adatta a: reportage, viaggio, progetti con una durata.

**A movimenti.** Da tre a cinque blocchi, ciascuno con una sua tesi interna, separati
da uno stacco visibile (pagina bianca, immagine a doppia pagina, cambio netto di
chiave tonale). È l'architettura più robusta per un portfolio eterogeneo, perché
converte l'eterogeneità in struttura.
Adatta a: progetti tematici, lavori pluriennali, edit da archivio.

**A spirale.** Torna sugli stessi elementi da distanze decrescenti: lo stesso
soggetto o luogo ricompare tre volte, ogni volta più vicino o più esplicito.
Difficile, altissima resa quando funziona, richiede almeno tre immagini
riconoscibilmente "della stessa cosa" distribuite lontano fra loro.
Adatta a: progetti su un'ossessione, ritratti di una persona, luoghi.

Dichiara l'architettura in una riga e motiva la scelta con la natura del materiale,
non con il gusto.

## 4. Regole di adiacenza

Da verificare su ogni coppia di spread contigui. Ognuna ha un'eccezione, e
l'eccezione va dichiarata quando la usi.

1. **Mai due composizioni identiche affiancate o consecutive.** Due centrali di fila
   sembrano un errore di stampa. Eccezione: la ripetizione voluta come motivo, e
   allora ne serve una terza per far capire che è voluta.
2. **Non due volti frontali sullo stesso spread.** Si guardano e si annullano.
   Eccezione: dittici di ritratti dichiarati come tali.
3. **Salto tonale controllato.** Da una pagina scura a una molto chiara il lettore
   sbatte gli occhi: usalo come stacco fra movimenti, non dentro un movimento.
   Verificalo con `luminanza_media` `[MISURATO]`, non a occhio.
4. **Continuità di sguardo.** Se una figura guarda fuori dal fotogramma a destra, la
   pagina destra successiva raccoglie quello sguardo. Contraddirlo è possibile, ma
   deve essere un effetto, non una distrazione.
5. **Scala alternata.** Non tre campi larghi di fila, non tre dettagli di fila. Il
   respiro di una sequenza è in larga parte alternanza di scala.
6. **Colore coerente per blocchi.** Se il progetto ha immagini a colori e in bianco e
   nero, non alternarle una a una: raggruppa. Alternare dice al lettore che le due
   forme sono equivalenti, cioè che nessuna delle due è necessaria.
7. **Verticali e orizzontali.** Una verticale a piena pagina accanto a una
   orizzontale piccola crea gerarchia; due orizzontali affiancate creano una striscia
   e leggono come panorama unico, spesso involontariamente.
8. **Nessuna immagine ridondante nello stesso movimento.** Se due immagini simili
   servono davvero, mettile lontanissime: a quella distanza la ripetizione diventa
   rima invece che copia.

## 5. Apertura e chiusura

Sono le due decisioni che contano più di tutte le altre insieme.

**L'apertura** non è la foto migliore. La foto migliore in prima pagina lascia tutto
il resto in discesa. L'apertura deve: annunciare il tono, porre una domanda, e non
rispondere. Un'ottima apertura è spesso un'immagine media in autonomia e altissima
in funzione (`funzione` 9, `autonomia` 6). Se la tua apertura ha `autonomia` 10 e
`funzione` 5, stai aprendo col finale.

Prima dell'apertura può stare una **immagine soglia**: piccola, laterale, quasi
irrilevante, che funziona come schiarita di gola. Facoltativa, efficace.

**La chiusura** deve fare una di tre cose, e devi dire quale: chiudere il cerchio
(riprende un elemento dell'apertura), aprire una fuga (lascia il lettore fuori, in
uno spazio vuoto), oppure dare il colpo (l'immagine più dura, tenuta in serbo).
Vietato chiudere con la seconda foto più bella: è la scelta che fa sembrare finito
lo spazio invece che il libro.

Motiva entrambe le scelte in due righe ciascuna. Se non riesci a motivarle, non le
hai scelte.

## 6. Il respiro

Le pagine bianche e le immagini di pausa non sono spreco: sono ciò che rende
percepibili i picchi. Un libro fotografico senza vuoti è una fisarmonica di rumore.

- Da 3 a 5 pagine bianche in un libro da 60 pagine.
- Una immagine di pausa (bassa tensione, bassa densità, spesso un vuoto, un cielo, un
  muro, un dettaglio muto) ogni 4 o 5 spread.
- Le pause vanno **dopo** i picchi, non prima: prima raffreddano l'ingresso.

Attenzione al problema opposto, più raro ma peggiore: se le pause sono più di un
quarto dell'insieme, il libro non ha materia, e la soluzione non è togliere pause, è
scattare.

## 7. Aritmetica delle pagine

Il numero di immagini si fissa **prima** di scegliere, e dipende dal formato:

| Formato | Pagine | Immagini realistiche |
|---|---|---|
| fanzine, cucito a sella | 24 a 32 | 16 a 24 |
| libro breve d'autore | 48 a 64 | 30 a 45 |
| monografia | 96 a 128 | 60 a 90 |

Vincoli pratici da rispettare e da comunicare all'utente:

- **Le pagine sono multipli di 4** nella stampa in segnature. Un libro da 50 pagine
  non esiste: diventa 48 o 52.
- Contano anche le pagine non fotografiche: guardia, frontespizio, statement,
  colophon, crediti. Tolgono da 6 a 10 pagine al conto delle immagini.
- La copertina è a parte, ed è una scelta editoriale diversa dall'apertura:
  l'immagine di copertina deve funzionare **fuori contesto**, ridotta, con del testo
  sopra. Spesso è la seconda o terza immagine per forza, non la prima.
- Lo statement va dopo le immagini, non prima, salvo che il progetto non sia
  incomprensibile senza (in quel caso c'è un problema di immagini).

## 8. Sequenza a parete, che è un'altra cosa

In mostra lo spettatore non gira pagine: vede tutto insieme e poi si avvicina.
Cambia tutto:

- **Non c'è un ordine obbligato**, c'è un percorso probabile: si entra e si guarda a
  destra, salvo che qualcosa di forte non catturi a sinistra.
- **La gerarchia si fa con le dimensioni**, non con la posizione. Dichiara le
  dimensioni in modo relativo (una grande, tre medie, sei piccole) e non in
  centimetri assoluti se non conosci la parete.
- **Una sola immagine manifesto**, quella grande. Se ne metti due grandi competono.
- **Gli allineamenti** contano più delle singole immagini: linea mediana comune per
  formati diversi, oppure allineamento in alto per gruppi densi.
- **Distanza di lettura**: un'immagine molto dettagliata chiede di avvicinarsi,
  quindi ha bisogno di spazio libero davanti e ai lati. Una silhouette funziona da
  lontano e sopporta il gruppo serrato.
- **Le coppie affiancate** in mostra sono più forti che nel libro, perché si vedono
  insieme più a lungo.
- Numero: da 8 a 15 immagini per una parete singola, da 20 a 30 per una sala.
  Sopra i 30 lo spettatore smette di guardare e comincia a scorrere.

## 9. Sequenza per scorrimento su schermo

Sito, portfolio online, social. Lo scorrimento è verticale e veloce, quindi:

- **La prima immagine è un'esca**, non un'apertura: deve fermare il pollice, quindi
  qui la forza conta più della funzione. È l'unico caso in cui è legittimo mettere in
  testa l'immagine migliore.
- **Le verticali vincono** su telefono, le orizzontali perdono metà del loro effetto.
  Dichiaralo quando l'edit è a maggioranza orizzontale.
- **Da 12 a 20 immagini per galleria.** Oltre, nessuno arriva in fondo, e le ultime
  sono sprecate.
- **Ogni terza o quarta immagine deve reggere da sola**, perché è là che il lettore
  entra dalla condivisione di qualcun altro, senza contesto.
- Il ritmo tonale conta meno, la varietà di scala conta più: su schermo la monotonia
  di inquadratura è la prima causa di abbandono.

## 10. Come verificare una sequenza

Fai queste quattro verifiche e riportane l'esito in poche righe.

1. **Prova della stringa.** Scrivi la notazione del ritmo (sezione 2) e leggi solo
   quella, senza pensare alle immagini. Se la stringa ha un difetto della lista, la
   sequenza ha quel difetto.
2. **Prova dell'inversione.** Prendi due spread contigui e scambiali. Se non cambia
   niente, quei due spread non sono in sequenza: sono affiancati per caso, e almeno
   uno dei due è di troppo.
3. **Prova della rimozione.** Togli uno spread qualsiasi dal centro. Se il libro
   migliora, quello spread andava tolto. Ripeti mentalmente su tutti: è il modo più
   rapido per scendere dal numero sbagliato al numero giusto.
4. **Prova del riassunto.** Racconta la sequenza in tre frasi come se fosse una
   storia. Se ti serve nominare più di cinque immagini per farlo, l'architettura non
   è leggibile.
