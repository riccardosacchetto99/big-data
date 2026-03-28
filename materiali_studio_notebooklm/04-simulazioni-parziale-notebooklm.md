# Raccolta di Simulazioni d'Esame: Sistemi NoSQL e Modellazione Dati

Benvenuti a questo set di simulazioni d'esame. Questo documento è strutturato per testare la vostra padronanza dei paradigmi NoSQL, con un focus rigoroso sulla modellazione orientata agli aggregati, le architetture di persistenza e le strategie di design basate sui pattern di accesso. Ogni simulazione riflette la complessità dei test parziali, bilanciando il rigore teorico con l'applicazione pratica.

---

## Simulazione 1: Fondamenti e Orientamento agli Aggregati

**1.1 Traccia d'Esame**
*   **Domanda Teorica 1:** Spiegare la distinzione tra "Data Model" e "Storage Model" e definire l'aggregato citando i riferimenti bibliografici del corso.
*   **Domanda Teorica 2:** Analizzando il grafico "Size/Complexity", come si posizionano i diversi modelli NoSQL (Key-Value, Column-family, Document, Graph)? Qual è la relazione generale tra la complessità del modello e la dimensione dei dati gestibili?
*   **Esercizio di Modellazione:** Partendo da uno schema relazionale `Customer` (Id, Name) e `Address` (Id, CustomerId, Street, City), trasformare i dati in un modello orientato agli aggregati ottimizzato per un accesso unitario al cliente.

**1.2 Soluzione Dettagliata**
*   **Risposte Teoriche:**
    1.  Il *Data Model* è il modello attraverso il quale l'utente percepisce e manipola i dati, mentre lo *Storage Model* descrive come il database memorizza effettivamente tali dati su disco. Secondo Sadalage & Fowler (2012), l'aggregato è una "collezione di oggetti correlati trattati come un'unità per manipolazione, analisi e gestione della consistenza".
    2.  Nel grafico Size/Complexity, i Key-Value Store occupano il vertice in alto a sinistra (massima dimensione, minima complessità), seguiti da Column-families e Document Databases. I Graph Databases si trovano in basso a destra (massima complessità, minore dimensione gestibile rispetto agli altri). La regola generale indica che all'aumentare della complessità del modello dati, diminuisce solitamente la dimensione totale dei dati che il sistema può gestire efficientemente.
*   **Risoluzione Modellazione:**
    ```json
    {
      "customerId": 1,
      "name": "Martin",
      "addresses": [
        {
          "street": "123 Main St",
          "city": "Chicago"
        }
      ]
    }
    ```
*   **Logica di Design:** La scelta di nidificare l'indirizzo all'interno dell'entità cliente crea un'unità atomica di consistenza. Questo approccio favorisce l'operatività su cluster poiché i dati correlati risiedono sullo stesso nodo, minimizzando i jump di rete.

**1.3 Criteri di Valutazione**
*   **Max 2 punti:** Corretta distinzione tra Data e Storage Model.
*   **Max 2 punti:** Definizione di aggregato con citazione di Sadalage & Fowler.
*   **Max 2 punti:** Corretta interpretazione del grafico Size/Complexity.
*   **Max 4 punti:** Modellazione JSON corretta con nidificazione dell'array `addresses`.

---

## Simulazione 2: Architetture Key-value e Redis

**2.1 Traccia d'Esame**
*   **Domanda Teorica 1:** Spiegare il concetto di "opacità" dell'aggregato per un database Key-value.
*   **Domanda Teorica 2:** Quali sono le tre operazioni fondamentali (API) fornite da un Key-value store?
*   **Esercizio di Modellazione:** Si desidera memorizzare un prodotto (ID: 27, Nome: "NoSQL Distilled", Prezzo: 32.45) in Redis. Progettare uno schema che consenta l'accesso e la modifica dei singoli attributi in modo indipendente, mostrando i comandi Redis necessari.

**2.2 Soluzione Dettagliata**
*   **Risposte Teoriche:**
    1.  L'aggregato è "opaco" perché il database lo percepisce come un semplice "big blob" di bit senza significato intrinseco. Il sistema non può filtrare o indicizzare i campi interni; l'unico metodo di accesso è tramite la chiave primaria.
    2.  Le API fondamentali sono: `put(key, value)`, `value := get(key)` e `delete(key)`.
*   **Risoluzione Modellazione:**
    Si applica il partizionamento dell'oggetto in proprietà costituenti utilizzando la naming convention `prefisso:id:attributo`:
    ```bash
    SET prod:27:name "NoSQL Distilled"
    SET prod:27:price "32.45"
    ```
    Per recuperare solo il prezzo: `GET prod:27:price`.
*   **Logica di Design:** Partizionando l'aggregato in coppie Key-Value distinte, rendiamo trasparenti le singole proprietà all'applicazione, permettendo aggiornamenti granulari senza dover riscrivere l'intero oggetto.

**2.3 Criteri di Valutazione**
*   **Max 4 punti:** Spiegazione del concetto di opacità e limiti di interrogazione.
*   **Max 3 punti:** Utilizzo corretto del delimitatore `:` e del prefisso di entità.
*   **Max 3 punti:** Correttezza sintattica dei comandi Redis (`SET`/`GET`).

---

## Simulazione 3: Document Store e Trasparenza

**3.1 Traccia d'Esame**
*   **Domanda Teorica 1:** In cosa differisce un Document store da un Key-value store per quanto riguarda la visibilità della struttura interna? Quali vantaggi comporta questa caratteristica?
*   **Esercizio di Modellazione:** Modellare un profilo utente (ID: 5, Nome: Pramod, Città visitate: Chicago, London, NYC). Mostrare: 1) Il documento JSON risultante. 2) Il comando per recuperare l'utente con ID 5. 3) Il comando per recuperare solo il nome e l'ultima città visitata (proiezione).

**3.2 Soluzione Dettagliata**
*   **Risposte Teoriche:**
    1.  A differenza dei Key-value store, nei Document store la struttura dell'aggregato è "trasparente" al database. Questo permette al motore del DB di eseguire query sui campi interni, creare indici sul contenuto e restituire solo parti specifiche del documento (proiezioni).
*   **Risoluzione Modellazione:**
    ```json
    {
      "personID": 5,
      "firstname": "Pramod",
      "citiesvisited": ["Chicago", "London", "NYC"],
      "lastcity": "Chicago"
    }
    ```
    - Recupero totale: `db.users.find({ "personID": 5 })`
    - Proiezione selettiva: `db.users.find({ "personID": 5 }, { "firstname": 1, "lastcity": 1 })`
*   **Logica di Design:** Il modello a documenti è ideale quando la flessibilità dello schema deve unirsi alla capacità di interrogazione complessa senza ricorrere a JOIN lato applicazione.

**3.3 Criteri di Valutazione**
*   **Max 4 punti:** Corretta nidificazione JSON e uso di array per `citiesvisited`.
*   **Max 4 punti:** Spiegazione della trasparenza e dell'indicizzabilità dei campi.
*   **Max 2 punti:** Corretta sintassi della proiezione (recupero parziale).

---

## Simulazione 4: Column-family e Wide-column Stores

**4.1 Traccia d'Esame**
*   **Domanda Teorica 1:** Descrivere le tre dimensioni che indicizzano una mappa in una Column-family. Qual è la natura del "valore" memorizzato e chi ne gestisce l'interpretazione?
*   **Esercizio di Modellazione:** Progettare uno schema di tipo BigTable per memorizzare l'URL "a:cnn.com". Il sistema deve mantenere due versioni temporali del contenuto HTML (famiglia "contents", qualificatore "html").

**4.2 Soluzione Dettagliata**
*   **Risposte Teoriche:**
    1.  Le tre dimensioni sono: `row_key` (identificatore riga), `column_key` (composta da family e qualifier) e `timestamp` (per il versionamento). Il valore è un "uninterpreted byte array"; l'interpretazione semantica dei byte è a totale carico della *client application*.
*   **Risoluzione Modellazione:**
    ```text
    Row Key: "a:cnn.com"
    Column Family: "contents"
    Column Qualifier: "html"
    --------------------------------------------------
    Timestamp: t1 | Value: [byte array della versione 1]
    Timestamp: t2 | Value: [byte array della versione 2]
    ```
*   **Logica di Design:** L'uso della `row_key` come URL invertito (es. `com.cnn.www`) è un pattern comune per raggruppare domini simili. Il timestamp garantisce l'atomicità a livello di riga e la gestione storica senza sovrascritture.

**4.3 Criteri di Valutazione**
*   **Max 4 punti:** Definizione delle tre dimensioni e concetto di "uninterpreted byte array".
*   **Max 4 punti:** Corretta rappresentazione del versionamento tramite timestamp.
*   **Max 2 punti:** Specifica che l'interpretazione spetta alla client application.

---

## Simulazione 5: Redis Avanzato e Sorted Sets

**5.1 Traccia d'Esame**
*   **Domanda Teorica 1:** Confrontare `Set` e `Sorted Set` in Redis. Qual è la complessità computazionale dell'inserimento in un Sorted Set e perché?
*   **Esercizio di Modellazione:** Implementare un sistema di leaderboard per un gioco online. Mostrare i comandi per inserire "Player1" con score 100 e "Player2" con score 300 nella chiave `game:leaderboard`.

**5.2 Soluzione Dettagliata**
*   **Risposte Teoriche:**
    1.  Un `Set` è una collezione non ordinata di stringhe uniche. Un `Sorted Set` associa a ogni elemento uno *score* numerico, mantenendo gli elementi ordinati. L'operazione di inserimento (`ZADD`) ha una complessità di **O(log(N))**, poiché il sistema deve mantenere l'ordine della struttura dati interna (tipicamente una skip list).
*   **Risoluzione Modellazione:**
    ```bash
    ZADD game:leaderboard 100 "Player1"
    ZADD game:leaderboard 300 "Player2"
    ```
    Per recuperare la classifica: `ZRANGE game:leaderboard 0 -1 WITHSCORES`.
*   **Logica di Design:** Il Sorted Set è la struttura ottimale per le classifiche poiché l'ordinamento è gestito nativamente dal server, sollevando l'applicazione dall'onere di ordinare i dati dopo il recupero.

**5.3 Criteri di Valutazione**
*   **Max 4 punti:** Spiegazione della differenza tra Set e Sorted Set e citazione della complessità O(log(N)).
*   **Max 6 punti:** Uso corretto della sintassi `ZADD` con la sequenza score-valore.

---

## Simulazione 6: Design Strategy e Pattern di Accesso

**6.1 Traccia d'Esame**
*   **Domanda Teorica 1:** Perché nel design NoSQL si afferma che "non esiste una risposta universale"? In che modo i pattern di accesso influenzano la scelta tra "Single Aggregate" e "Multiple Aggregates"?
*   **Esercizio di Modellazione:** Un sistema di e-commerce deve decidere se modellare i dati come un unico aggregato "Customer + Orders" o come aggregati separati. Discutere i Pros e Cons basandosi sul materiale didattico.

**6.2 Soluzione Dettagliata**
*   **Risposte Teoriche:**
    1.  La modellazione NoSQL è strettamente legata al modo in cui l'applicazione manipola i dati. Se l'accesso avviene quasi sempre per "cliente con tutta la sua storia", l'aggregato singolo è preferibile. Se l'applicazione accede a un "singolo ordine alla volta", aggregati separati sono più efficienti.
*   **Risoluzione Modellazione (Analisi Critica):**
    *   **Single Aggregate (Customer con ordini nidificati):**
        *   *Pros:* Lettura atomica dell'intero profilo; eccellente per la data locality su cluster (tutto su un nodo).
        *   *Cons:* L'aggregato può superare i limiti di dimensione (es. 16MB in MongoDB o 512MB in Redis); diventa un ostacolo se serve analizzare solo i prodotti venduti globalmente.
    *   **Multiple Aggregates (Ordini separati):**
        *   *Pros:* Gestione snella di singoli ordini; facilità di aggiornamento.
        *   *Cons:* Richiede join lato applicazione per ricostruire la storia del cliente.

**6.3 Criteri di Valutazione**
*   **Max 5 punti:** Spiegazione della dipendenza dai pattern di accesso.
*   **Max 5 punti:** Analisi bilanciata di Pros (cluster affinity) e Cons (dimensione e ostacoli all'interazione).

---

## Simulazione 7: Persistenza Redis e Operazioni Atomiche

**7.1 Traccia d'Esame**
*   **Domanda Teorica 1:** Descrivere il meccanismo di Snapshotting (BGSAVE) in Redis, menzionando esplicitamente il ruolo della `fork()` e del "Copy-on-Write". Confrontarlo brevemente con l'Append Only File (AOF).
*   **Esercizio di Modellazione:** Progettare un sistema di lock distribuito elementare per la risorsa `resource_alpha` utilizzando il comando atomico appropriato.

**7.2 Soluzione Dettagliata**
*   **Risposte Teoriche:**
    1.  Il `BGSAVE` esegue un dump periodico della memoria su disco. Redis chiama una `fork()`, creando un processo figlio che scrive il database su file mentre il processo padre continua a servire i client. Grazie al meccanismo di **Copy-on-Write**, la memoria viene duplicata solo quando avvengono modifiche, garantendo efficienza. L'AOF, invece, registra ogni singola operazione di scrittura in un log, offrendo una persistenza più granulare ma con file potenzialmente più grandi.
*   **Risoluzione Modellazione:**
    Utilizzo del comando `SETNX` (Set if Not eXists):
    ```bash
    SETNX lock:resource_alpha "client_id_99"
    ```
    Se il comando restituisce `1`, il lock è acquisito. Se restituisce `0`, la risorsa è già occupata.

**7.3 Criteri di Valutazione**
*   **Max 5 punti:** Spiegazione tecnica di BGSAVE (fork/copy-on-write).
*   **Max 5 punti:** Corretto utilizzo di `SETNX` e interpretazione del valore di ritorno (0/1).

---

## Simulazione 8: Naming Convention e Strategie di Chiave

**8.1 Traccia d'Esame**
*   **Domanda Teorica 1:** Perché le chiavi casuali sono considerate inutili nel contesto NoSQL? Quali sono le caratteristiche di una naming convention ben progettata (prefissi, delimitatori, ecc.)?
*   **Esercizio di Modellazione:** Progettare una chiave per memorizzare la quantità di un articolo in inventario (ID riga: 1452). Seguire rigorosamente le raccomandazioni del corso sulla lunghezza dei prefissi.

**8.2 Soluzione Dettagliata**
*   **Risposte Teoriche:**
    1.  Le chiavi casuali sono inutili a meno che non esista una struttura esterna (mappa) che le colleghi ai dati. Una naming convention rigorosa rende il codice leggibile, minimizza il codice di get/set e permette di derivare le chiavi logicamente. Deve includere un prefisso di 3-4 lettere per l'entità, un identificatore unico, un delimitatore (es. `:`) e il nome dell'attributo.
*   **Risoluzione Modellazione:**
    ```text
    Chiave: inv:1452:qty
    Valore: "500"
    ```
    - `inv`: Prefisso di 3-4 lettere per l'entità *inventory*.
    - `1452`: Identificatore unico dell'istanza.
    - `qty`: Stringa dell'attributo (quantity).
    - `:`: Delimitatore standard.
*   **Logica di Design:** Questo schema permette di implementare funzioni generiche come `setInvAttr(id, attr, val)` che costruiscono la chiave programmaticamente.

**8.3 Criteri di Valutazione**
*   **Max 2 punti:** Spiegazione del limite delle chiavi casuali.
*   **Max 4 punti:** Uso corretto del prefisso di 3-4 lettere e del delimitatore.
*   **Max 4 punti:** Struttura completa `entità:id:attributo`.

---

## Strategia di Studio: Programma di 7 Giorni

| Giorno | Argomento di Studio | Focus Pratico |
| :--- | :--- | :--- |
| **1-2** | NoSQL e Aggregati | Definizione Sadalage & Fowler, Grafico Size/Complexity, Data vs Storage Model. |
| **3** | Key-value e Document | Opacità vs Trasparenza, modellazione JSON, lookup per chiave e proiezioni. |
| **4** | Column-family | BigTable, Cassandra, le 3 dimensioni (Row, Column, Timestamp), byte arrays. |
| **5** | Redis: Strutture Dati | Primitives (Strings) e Containers (Hashes, Lists, Sets, Sorted Sets). Operazioni O(1) e O(log N). |
| **6** | Design Strategy | Access patterns, Key naming convention (`pref:id:attr`), atomicità a livello di riga. |
| **7** | Persistenza e Ripasso | BGSAVE (fork/copy-on-write) vs AOF. Simulazioni complete di modellazione. |

---

## Errori Frequenti da Evitare

1.  **Confusione tra Storage e Data Model:** Pensare che il modo in cui il DB scrive su disco (Storage) debba coincidere con la percezione dell'utente (Data).
2.  **Ignorare i Pattern di Accesso:** Progettare un aggregato complesso (es. nidificare tutto in Customer) quando l'applicazione accede solo a singole proprietà, creando un overhead inutile.
3.  **Uso di Naming Convention Incoerenti:** Non utilizzare delimitatori chiari o prefissi di entità, rendendo impossibile la generazione programmatica delle chiavi.
4.  **Sottovalutazione dell'Opacità:** Tentare di eseguire query su campi interni di un Key-value store (non possibile senza recuperare l'intero blob).
5.  **Negligenza sui Byte Arrays:** Dimenticare che nelle Column-family il DB non interpreta i dati; se il client non sa come leggere i byte, il dato è inutilizzabile.
6.  **Confusione tra Aggregato e Tabella:** Trattare l'aggregato come una tabella relazionale piatta, perdendo i vantaggi della nidificazione e della coerenza atomica.