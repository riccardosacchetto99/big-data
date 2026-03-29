# Corso: Database Technologies for Big Data - Simulazione della Prova d'Esame

### 1. Introduzione alla Prova e Modalità d'Esame

La presente simulazione è stata concepita per valutare la maturità tecnica e la capacità di analisi critica dello studente in relazione ai paradigmi di gestione dei dati su larga scala. L'obiettivo non è la mera scomposizione mnemonica di definizioni, ma la dimostrazione di una comprensione profonda dei trade-off architetturali che intercorrono tra modelli orientati agli aggregati, sistemi a grafo e implementazioni in-memory.

> **Istruzioni per i candidati:**
> La prova è strutturata in quattro sezioni tematiche e riflette il rigore metodologico richiesto in sede di esame parziale. Il candidato deve dimostrare di saper distinguere tra le diverse unità di retrieval e le relative implicazioni sulla coerenza (ACID) e sulla distribuzione dei dati in ambienti cluster. È richiesto l'utilizzo di una terminologia tecnica precisa e una sintesi rigorosa.

---

### 2. Sezione 1: Teoria degli Aggregati e Gestione delle Relazioni

**Domanda 1:** Fornire una definizione formale di "Aggregato" e discutere il suo ruolo critico nella distribuzione dei dati su cluster e nella definizione dei confini delle operazioni ACID.

**Domanda 2:** Analizzare le strategie di gestione delle relazioni tra aggregati distinti nei sistemi NoSQL, confrontando l'uso dei link (ID) con i join programmatici.

**Soluzioni e Punti Chiave di Analisi:**
*   **Definizione di Aggregato:** Un aggregato è una collezione di dati correlati che il sistema tratta come un'unica unità di interazione (retrieval unit). Tale struttura è fondamentale per garantire la data locality: il database può ottimizzare la distribuzione memorizzando l'intero aggregato su un singolo nodo del cluster.
*   **Confini ACID:** Nei database Aggregate-oriented, l'atomicità è garantita esclusivamente entro i confini del singolo aggregato. Qualsiasi aggiornamento che coinvolga più aggregati ricade sotto la responsabilità del programmatore, poiché il database non fornisce garanzie transazionali cross-aggregate.
*   **Ignoranza del Database:** Il sistema NoSQL è tipicamente "ignorante" delle relazioni semantiche esistenti tra aggregati diversi.
*   **Join Programmatici:** Poiché i join non sono supportati nativamente a livello di engine, la relazione viene mantenuta inserendo l'ID di un aggregato nel corpo di un altro. La correlazione dei dati deve essere implementata a livello applicativo tramite codice che esegua join programmatici, recuperando sequenzialmente le unità correlate.

---

### 3. Sezione 2: Focus sui Database a Grafo

I Graph Database rispondono alla frustrazione derivante dall'inefficienza dei sistemi relazionali nel gestire join complessi e ricorsivi. Mentre in un RDBMS le relazioni sono calcolate a runtime tramite chiavi esterne, nei Graph DB le relazioni sono persistite nativamente.

| Caratteristica | Database Relazionali (RDBMS) | Database a Grafo |
| :--- | :--- | :--- |
| **Motivazione** | Ottimizzazione per schemi tabellari rigidi. | Necessità di navigare interconnessioni complesse senza l'onere dei join. |
| **Modellazione** | Relazioni basate su Foreign Keys. | Nodi (entità) e Archi (relazioni) persistiti. |
| **Performance** | Decadimento esponenziale al crescere dei join (Query time). | Traversal costante ed economico; ideale per dati altamente connessi. |
| **Shift di Carico** | Carico concentrato al momento dell'interrogazione (Query time). | Carico spostato dal Query time al momento dell'inserimento (Insert time). |
| **Casi d'uso** | Sistemi ERP, transazioni finanziarie. | Social network, logistica (mappe), analisi di rete. |

#### Approfondimento: Missione e Varianti del Modello
La missione dei database a grafo è archiviare entità e relazioni affinché la navigazione del network sia un'operazione di primo livello. Gli archi possiedono significatività direzionale e tipologica (es. *likes*, *friend*, *employee*), permettendo di identificare pattern complessi nel grafo.

Le implementazioni variano sensibilmente nell'approccio alla persistenza:
*   **Neo4J:** Archivia oggetti Java mappandoli su nodi e archi in modalità *schemaless*.
*   **InfiniteGraph:** Archivia oggetti Java definendoli come sottoclassi di tipi predefiniti (*built-in types*).

---

### 4. Sezione 3: Analisi di Architetture Reali - Il Caso Facebook

Lo stack tecnologico di Facebook rappresenta un paradigma di ingegneria dei dati eterogenea, progettato per gestire volumi massivi (oltre 100 PB).

*   **Apache Hadoop (HDFS e MapReduce):** HDFS funge da backbone per l'archiviazione distribuita, gestendo cluster singoli oltre i 100 PB. MapReduce abilita il calcolo distribuito su scala massiva.
*   **Apache Hive:** Consente un'interfaccia SQL-like per l'interrogazione dei dati su Hadoop, integrando la valutazione delle query con l'engine MapReduce.
*   **Apache HBase:** Database column-family basato su Hadoop. È stato adottato specificamente per i servizi di messaggistica (e-mail, IM, SMS), sostituendo MySQL e Cassandra in questo ambito critico.
*   **RocksDB:** Storage engine Key-Value embedded ad altissime prestazioni, ottimizzato per l'uso intensivo di risorse e sviluppato internamente da Facebook.
*   **Apache Giraph:** Database a grafo utilizzato per analizzare il social graph (trilioni di archi). Si noti che la tecnologia è attualmente considerata *retired*.

---

### 5. Sezione 4: Esercitazione Pratica su Redis

#### 5.1 Architettura e Persistenza
Redis opera come database in-memory single-threaded. La persistenza è garantita da due meccanismi complementari:
1.  **Periodic Dump (BGSAVE):** Utilizza la chiamata di sistema `fork()` per creare un processo figlio che, tramite meccanismo *Copy-on-Write*, scrive l'intero dataset su disco in background senza bloccare le operazioni correnti.
2.  **Append Only File (AOF):** Registra ogni operazione di scrittura in un log. La frequenza di sincronizzazione è configurabile tramite `fsync()` (opzioni: *always*, *every second*, *never*).

#### 5.2 Modellazione Dati: Il pattern "Order-Items"
Per soddisfare la query "ottenere i prodotti acquistati da un utente", è necessaria una strategia di indicizzazione manuale che rifletta il mindset di un data engineer:
*   **Discovery Index:** Si utilizza un **Set** (es. `ords_james_ordID`) per mappare la relazione uno-a-molti tra utente e ordini. Questo funge da indice per localizzare rapidamente gli ID degli ordini.
*   **Aggregate Storage:** Si utilizza un **Hash** per ogni ordine (es. `order_1`), che funge da unità di retrieval contenente coppie `prodotto:quantità`. Questa scelta garantisce un accesso O(1) ai dettagli dell'ordine una volta ottenuto l'ID.

#### 5.3 Comandi e Complessità Computazionale

| Comando | Funzione | Complessità |
| :--- | :--- | :--- |
| `HSET` | Imposta un campo in un hash. | O(1) |
| `SINTER` | Intersezione tra più set. | O(C*M) (dove C è il numero di set) |
| `SDIFF` | Differenza tra set. | O(N) (numero totale elementi) |
| `ZADD` | Aggiunta a un set ordinato. | O(log(N)) |
| `ZRANK` | Ranking di un membro (Sorted Set). | O(log(N)) |
| `ZRANGEBYSCORE`| Range di membri per punteggio. | O(log(N)+M) |

---

### 6. Errori Frequenti e "Caveats" Tecnici

1.  **Transazionalità Cross-Aggregate:** Errore fatale è assumere che i sistemi NoSQL garantiscano l'atomicità su più aggregati; l'aggiornamento di un ordine e del profilo utente simultaneamente non è nativamente atomico.
2.  **Rigidità dello Schema RDBMS per Grafi:** Implementare grafi in SQL richiede di modellare il traversal *ex-ante*. Qualsiasi nuova tipologia di relazione richiede modifiche costose allo schema (*schema changes*).
3.  **Gestione dell'Anchor Node:** Nelle query sui grafi è indispensabile definire un punto di partenza (anchor node). Tali nodi sono tipicamente individuati tramite indici su attributi specifici, come l'ID, per avviare la navigazione della rete.

---

### 7. Rubrica di Valutazione e Criteri di Punteggio

| Livello | Criteri di Valutazione |
| :--- | :--- |
| **Insufficiente** | Mancata comprensione delle unità di retrieval e dei limiti di atomicità. |
| **Sufficiente** | Capacità di distinguere tra modelli KV, Document e Graph; conoscenza operativa di Redis. |
| **Eccellente** | Padronanza della complessità dei comandi; capacità di giustificare lo spostamento del carico computazionale (insert-time vs query-time) e di progettare architetture integrate complesse. |

---

### 8. Domande di Autovalutazione e Mini-Riepilogo Finale

**Flashcards di revisione:**
1. Qual è la distinzione tecnica tra Neo4J e InfiniteGraph nella gestione degli oggetti Java?
2. Qual è il limite dell'atomicità (ACID) nei database orientati agli aggregati secondo il principio dei "confini"?
3. Perché le performance dei Graph DB sono considerate superiori per dati altamente connessi rispetto agli RDBMS?
4. Descrivere la semantica del "Copy-on-Write" durante l'esecuzione di un `BGSAVE`.
5. In Facebook, quale tecnologia ha sostituito Cassandra per la gestione dei servizi di messaggistica?

**Riepilogo finale:**
La progettazione di architetture Big Data richiede una scelta ponderata tra modelli *Aggregate-oriented* e *Graph-oriented*. Gli aggregati semplificano la distribuzione su cluster fungendo da unità atomiche di retrieval, ideali per accessi puntuali. Di contro, i Graph DB abbattono la complessità computazionale dei traversal, spostando l'onere del calcolo delle relazioni dal momento della query a quello dell'inserimento. La padronanza di questi trade-off è l'elemento discriminante per un esperto di tecnologie database moderne.