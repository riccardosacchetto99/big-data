# Modellazione dei Dati Key-Value: Guida Completa alla Progettazione NoSQL

### 1. Fondamenti del Data Modeling NoSQL e Orientamento agli Aggregati

Nella progettazione di sistemi distribuiti, è essenziale distinguere tra il **modello di dati** (l'interfaccia logica attraverso cui percepiamo e manipoliamo l'informazione) e il **modello di archiviazione** (il modo in cui i bit sono fisicamente disposti sui supporti). Mentre gli RDBMS tradizionali decompongono l'informazione in tuple normalizzate, il paradigma NoSQL abbraccia l'**Aggregate Orientation**.

#### Comparazione tra Modelli: Dal "Martin" Relazionale all'Aggregato
Si consideri un cliente di nome "Martin" (ID: 1). In un RDBMS, i suoi dati sono frammentati in almeno cinque tabelle: `Customer`, `Orders`, `BillingAddress`, `OrderItem` e `Product`. Per ricostruire il profilo di Martin, il sistema deve eseguire costosi JOIN tra tuple distribuite. Nel modello NoSQL, cerchiamo le caratteristiche condivise e raggruppiamo queste informazioni in un'unica unità logica.

| Caratteristica | RDBMS (Tuple-based) | NoSQL (Aggregate-oriented) |
| :--- | :--- | :--- |
| **Unità di dati** | Tuple distribuite in tabelle correlate. | Aggregati: unità atomiche complesse. |
| **Operazioni** | Operano su tuple e restituiscono tuple. | Operano su intere unità di dati correlate. |
| **Struttura** | Piatta e normalizzata. | Complessa (record annidati, array, liste). |
| **Esempio Martin** | ID 1 distribuito su 5+ tabelle. | Singolo "Customer" con ordini e indirizzi inclusi. |

#### Definizione di Aggregato
Citando **Sadalage & Fowler (2012)**, un aggregato è una collezione di oggetti correlati trattati come un'unità atomica per manipolazione, analisi e gestione della coerenza. 

**Vantaggi degli Aggregati:**
*   **Per i programmatori:** Eliminano il "mismatch" tra oggetti dell'applicazione e tabelle, permettendo di lavorare con strutture dati naturali.
*   **Per il funzionamento in cluster:** Poiché i dati correlati vengono manipolati insieme, essi possono risiedere sullo stesso nodo fisico, ottimizzando la distribuzione e riducendo la latenza di rete.

---

### 2. Lo Store Key-Value: Anatomia e Operazioni Base

Il database key-value è concettualmente una "big hash table" distribuita. In questo modello, l'aggregato viene trattato come un **"opaque blob"**: una sequenza di bit di cui il database non conosce il significato.
**Nota dell'architetto:** Poiché il blob è opaco, l'onere dell'interpretazione (parsing di JSON, XML o formati binari) ricade interamente sull'**applicazione client**.

Le operazioni fondamentali sono:
*   `put(key, value)`: Inserisce o aggiorna un valore.
*   `get(key)`: Recupera il valore.
*   `delete(key)`: Rimuove la coppia.

#### Focus: Redis (REmote DIctionary Server)
Redis è un database in-memory, single-threaded, noto per le altissime prestazioni. I valori (Strings) hanno un limite fisico di **512MB**. La persistenza è gestita tramite:
1.  **Periodic Dump (Background Save):** Il comando `BGSAVE` innesca un `fork()` del sistema operativo. Sfruttando il meccanismo Copy-on-Write, scrive l'intero DB su disco. Viene attivato automaticamente dopo **X secondi e Y cambiamenti**.
2.  **Append Only File (AOF):** Un log di ogni operazione di scrittura, sincronizzato con politiche di `fsync` (sempre, ogni secondo o mai).

---

### 3. Key Design e Naming Convention

Una progettazione superficiale delle chiavi compromette l'efficienza. Come architetto, vi avverto: **chiavi casuali sono inutili** senza una mappatura esterna e chiavi eccessivamente lunghe sprecano memoria preziosa in sistemi in-memory.

**Vincoli Tecnici:** Le chiavi devono essere composte esclusivamente da caratteri **Printable ASCII**.

**Naming Convention Standard:**
Per garantire leggibilità ed estensibilità, utilizziamo il pattern: `prefisso:identificatore:attributo`

1.  **Prefisso:** 3-4 lettere per l'entità (es. `cust` per customer, `inv` per inventory).
2.  **Delimitatore:** Tipicamente `:` (o qualsiasi carattere non presente nei dati).
3.  **Identificatore Unico:** L'ID univoco dell'istanza (es. `14526984`).
4.  **Attributo:** Specifica la proprietà (es. `email`, `name`).

*Esempio di chiave ben strutturata:* `cust:198277:fname`

---

### 4. Strategie Avanzate: Partitioning vs. Atomic Aggregates

La scelta tra memorizzare un intero oggetto o dividerlo è un trade-off di design critico:

1.  **Accesso all'intero aggregato (Atomic Aggregate):** Memorizziamo tutto (Customer + Indirizzi + ID Ordini) sotto un'unica chiave.
    *   *Pro:* Garantisce l'atomicità della lettura/scrittura dell'intero profilo.
    *   *Contro:* Richiede il recupero di 512KB di dati anche se serve solo un flag booleano.
2.  **Partizionamento in proprietà:** Dividiamo l'oggetto in più coppie (es. `cust:1:nome`, `cust:1:bio`).
    *   *Pro:* Accesso granulare ed efficiente ai singoli attributi.
    *   *Contro:* Perdita di atomicità sull'intero oggetto (richiede più operazioni).

**Denormalizzazione:** Nelle relazioni tra aggregati, è pratica comune includere riferimenti diretti (es. una lista di `OrderID` dentro l'aggregato `Customer`) per evitare l'assenza di JOIN.

---

### 5. Casi Studio Pratici

#### Caso 1: Zoo (Gerarchia Fisica)
Utilizzo di chiavi gerarchiche per riflettere l'organizzazione spaziale.
*   **Chiave:** `zoo:area:A1:animal:101`
*   **Valore:** Blob JSON con parametri vitali.

#### Caso 2: E-commerce (L'Aggregato Order)
Basandosi sul modello "Martin", l'aggregato `Order` deve contenere non solo i dati dell'ordine, ma anche `OrderItem`, `ShippingAddress` e riferimenti al `Product`.
*   **Chiave:** `order:99`

#### Caso 3: Università (Relazioni Many-to-Many)
Per gestire l'iscrizione ai corsi, utilizziamo un **Set** Redis. 
*   **Chiave:** `stud:123:courses`
*   **Perché il Set?** Garantisce l'**unicità** degli ID corso (evitando doppie iscrizioni accidentali) e permette operazioni rapide di intersezione tra studenti.

#### Caso 4: Ticketing (Consistenza e Prenotazioni)
Per evitare overbooking, utilizziamo l'operazione atomica `SETNX` (Set if Not Exists).
*   **Operazione:** `SETNX seat:42 user_id_77`
*   **Risultato:** Solo il primo client che esegue il comando otterrà il posto; i successivi riceveranno un errore.

---

### 6. Trade-off e Scelte di Design

Non esiste una "silver bullet". La struttura dell'aggregato deve piegarsi ai pattern di accesso dell'applicazione.

> "La struttura di un aggregato può facilitare grandemente alcune interazioni con i dati, ma agire come un ostacolo insormontabile per altre."

*   **Read-Heavy:** Se l'applicazione richiede spesso la visualizzazione del profilo completo, l'aggregazione totale è vincente.
*   **Write-Heavy:** Se l'applicazione aggiorna costantemente singoli contatori o attributi indipendenti, il partizionamento riduce il carico di rete e i lock.

---

### 7. Esercitazioni Guidate

**Esercizio 1: Modellazione Blog**
Modellare post, commenti e tag per un sistema ad alto traffico.
*   **Soluzione:** 
    *   Post (Hash): `post:ID` con campi titolo e corpo.
    *   Commenti (Lista): `post:ID:comments` (per mantenere l'ordine cronologico).
    *   Tag (Set): `post:ID:tags` (per garantire tag unici e permettere ricerche per intersezione).

**Esercizio 2: Conversione RDBMS**
Ottimizzare la query: `SELECT email FROM users WHERE id = 500`.
*   **Soluzione:** Creare una chiave dedicata `user:500:email` per un accesso O(1) diretto, evitando di caricare l'intero oggetto utente.

#### Schema di Valutazione (Assessment)
| Criterio | Punteggio | Note |
| :--- | :--- | :--- |
| **Naming Convention** | 1 pt | Correttezza prefisso e delimitatore. |
| **Gestione Relazioni** | 2 pt | Uso di liste/set di ID per collegare aggregati. |
| **Scelta Tipo Redis** | 1 pt | Appropriatezza (es. Set per dati unici). |
| **Ottimizzazione** | 1 pt | Evitare blob giganti per letture puntuali. |

---

### 8. Appendice: Tipi di Dati Redis (Containers)

Redis offre contenitori specializzati per organizzare le stringhe. È cruciale comprendere la loro complessità computazionale:

*   **Strings:** Il tipo base (max 512MB). Operazioni `GET`, `SET`, `SETNX`, `GETSET` sono **O(1)**.
*   **Hashes:** Mappe campo-valore.
    *   `HGET`, `HSET`: **O(1)**.
    *   `HMGET`: **O(N)** dove N è il numero di campi richiesti.
    *   `HKEYS`, `HVALS`: **O(N)** dove N è il numero totale di campi nell'hash.
*   **Lists:** Collezioni ordinate con accesso `HEAD` o `TAIL`.
*   **Sets:** Collezioni non ordinate di stringhe uniche.
*   **Sorted Sets:** Ogni elemento ha uno **score** numerico. Ideali per classifiche o code di priorità.

*Nota: Nelle operazioni Hashes, N si riferisce sempre alla quantità di campi manipolati, non alla dimensione totale del database.*