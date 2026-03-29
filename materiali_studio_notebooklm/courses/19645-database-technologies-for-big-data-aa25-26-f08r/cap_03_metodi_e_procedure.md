# Capitolo 3 - Metodi e procedure operative

Il presente capitolo delinea le metodologie tecniche e le procedure operative fondamentali per la gestione dei dati in ambienti NoSQL. In qualità di architetti, dobbiamo operare un cambio di paradigma: la logica di consistenza e la gestione delle relazioni non sono più delegate esclusivamente al motore del database, ma diventano parte integrante del workflow di progettazione applicativa. Esamineremo la modellazione orientata agli aggregati, le strutture a grafo e le tecnologie a supporto dei Big Data, analizzando le implementazioni reali in contesti di scala planetaria.

---

### 1. Workflow di Progettazione Orientata agli Aggregati

**1.1. Definizione e Delimitazione degli Aggregati**
Un aggregato è l'unità logica di interazione con il database, una collezione di dati correlati che il sistema manipola come un singolo blocco. Operativamente, gli aggregati definiscono i confini invalicabili per le operazioni ACID (**Atomicità**, Consistenza, Isolamento, Durabilità). 

**Avvertenza Architetturale:** La delimitazione accurata di questi confini è la precondizione per la scalabilità orizzontale. Limitando l'atomicità al singolo aggregato, evitiamo la necessità di lock distribuiti su più nodi del cluster, che degraderebbero irrimediabilmente le prestazioni del sistema.

**1.2. Efficienza delle Interazioni**
Il workflow di progettazione deve garantire che la maggior parte delle operazioni di lettura e scrittura avvenga all'interno dello stesso set di dati (lo stesso aggregato). Questo approccio ottimizza la gestione dello storage su cluster, poiché il database può memorizzare fisicamente insieme i dati che vengono acceduti simultaneamente, riducendo la latenza di rete tra i nodi.

**1.3. Errori Comuni nella Modellazione**
*   **Aggregati sovradimensionati:** Includere troppe informazioni eterogenee appesantisce le operazioni di I/O e riduce la concorrenza.
*   **Confini instabili:** Definire confini che obbligano il sistema a eseguire aggiornamenti costanti tra più unità, vanificando i vantaggi della distribuzione e aumentando il rischio di inconsistenze.

---

### 2. Procedure Operative per la Gestione delle Relazioni

**2.1. Relazioni tra Aggregati (Manual Joins)**
Nei database orientati agli aggregati, le relazioni tra entità distinte non sono gestite dal server tramite vincoli di integrità referenziale. La procedura tecnica prevede l'uso di **Joins manuali**: si memorizza l'ID di un aggregato all'interno di un altro, agendo come una Foreign Key "logica". Il database rimane totalmente "ignorante" rispetto a tale legame.

**2.2. Implementazione Lato Applicazione**
La responsabilità dell'integrità è interamente in mano al programmatore. La procedura operativa per un join richiede due fasi distinte: il recupero del primo aggregato, l'estrazione dell'ID di riferimento e la successiva query per ottenere i dati correlati.

**2.3. Metadati e Visibility**
Per rendere le relazioni "visibili" al database, alcuni sistemi offrono funzionalità specifiche. In Riak, ad esempio, è possibile inserire informazioni di collegamento (**links**) direttamente nei metadati degli oggetti o negli header HTTP, permettendo al server di supportare parzialmente la navigazione tra documenti.

**2.4. Esercizio Pratico 1: Collegamento Customers e Orders**
*   **Scenario:** Collegare il cliente "Martin" (ID: 1) all'ordine "Order 99".
*   **Soluzione Logica:** Il documento dell'ordine deve includere esplicitamente il riferimento al cliente.
    **Esempio Documento Order 99:**
    {
      "id": 99,
      "customerId": 1,
      "orderItems": [ { "productId": 27, "productName": "NoSQL Distilled" } ]
    }
    Il software dovrà estrarre `customerId: 1` per recuperare l'anagrafica di "Martin" dal relativo aggregato.

**Avvertenza Architetturale:** Un errore frequente è dimenticare che la modifica di un ID di riferimento richiede un aggiornamento manuale in ogni documento correlato, poiché non esiste il "cascading update" tipico dei sistemi relazionali.

---

### 3. Gestione degli Aggiornamenti e Atomicità

**3.1. Procedure di Aggiornamento su Singolo Aggregato**
L'atomicità è garantita rigorosamente solo all'interno dell'aggregato. Ogni modifica ai dati contenuti in un unico documento o riga di una colonna-famiglia è considerata un'operazione "tutto o niente".

**3.2. Protocollo per Aggiornamenti Multi-Aggregato**
Qualora un'operazione di business coinvolga più aggregati, il programmatore deve seguire questa checklist procedurale:
1.  Verificare lo stato iniziale di tutti gli aggregati coinvolti.
2.  Eseguire gli aggiornamenti in sequenza logica.
3.  Prevedere una logica di compensazione in caso di fallimento parziale.
A differenza degli RDBMS, che gestiscono la consistenza su molteplici righe tramite transazioni native, nei sistemi NoSQL la consistenza transazionale è un onere del codice applicativo.

**3.3. Esempi Concreti di Fallimento**
Se un aggiornamento fallisce dopo aver modificato il primo aggregato ma prima del secondo, il sistema entra in uno stato di inconsistenza. Ad esempio, un prodotto potrebbe essere rimosso dall'inventario senza che l'ordine corrispondente sia stato confermato nel database ordini.

**Avvertenza Architetturale:** L'errore più grave è assumere che l'atomicità si estenda oltre il singolo aggregato; tale presunzione porta inevitabilmente a corruzione dei dati in sistemi distribuiti ad alto carico.

---

### 4. Metodi Operativi con Graph Databases

**4.1. Workflow di Navigazione (Traversal)**
La query in un database a grafo consiste nella navigazione attraverso la rete di archi (edges). La procedura richiede l'identificazione di un **anchor node** (nodo di partenza). Per ottimizzare questa fase, i nodi devono essere indicizzati tramite attributi univoci come l'ID.

**4.2. Persistenza delle Relazioni**
A differenza dei modelli relazionali, dove il join è calcolato dinamicamente al momento della query, nei database a grafo la relazione è **persistita fisicamente**. Questo elimina il costo computazionale del calcolo dei legami durante l'esecuzione.

**4.3. Confronto Operativo (Graph vs Relational)**

| Caratteristica | Database Relazionale | Database a Grafo |
| :--- | :--- | :--- |
| **Meccanismo Relazione** | Foreign Keys (Join calcolati) | Archi persistiti (Navigazione) |
| **Schema** | Rigido (Richiede Schema Migrations/DDL) | Flessibile (Schemaless, es. Neo4j) |
| **Performance** | Decade con la complessità dei Join | Eccellente per dati iper-connessi |
| **Carico Operativo** | Concentrato al momento della Query | Concentrato al momento dell'Inserimento |

**4.4. Esempio Concreto di Query Social**
*   **Obiettivo:** Trovare i dipendenti di "BigCo" a cui piace "NoSQL Distilled".
*   **Passi Operativi:**
    1.  Posizionarsi sul nodo anchor **BigCo**.
    2.  Attraversare gli archi di tipo **employee** verso i nodi Anna, Barbara e Carol.
    3.  Per ciascuno di questi nodi, seguire gli archi di tipo **likes**.
    4.  Filtrare i risultati mantenendo solo i percorsi che terminano sul nodo **NoSQL Distilled**.

**Avvertenza Architetturale:** Un errore comune è modellare il grafo basandosi su un'unica tipologia di attraversamento prevista. Se le necessità di navigazione cambiano, un modello troppo rigido può diventare inefficiente.

---

### 5. Procedure di Amministrazione e Persistenza con Redis

**5.1. Configurazione dell'ambiente Docker**
Per la gestione operativa del server Redis, i comandi sequenziali da terminale sono:
*   **docker compose up -d**: Crea il container e avvia l'esecuzione in background.
*   **docker exec -it redis-redis-1 redis-cli**: Avvia il client interattivo per impartire comandi.
*   **docker compose stop**: Arresta il container.
*   **docker compose start**: Riavvia un container precedentemente fermato.

**5.2. Workflow di Persistenza**
Redis è un database in memoria principale, ma garantisce la durabilità tramite due procedure:
*   **Periodic Dump (BGSAVE):** Esegue una **fork()** del processo creando un figlio che, tramite il meccanismo **Copy-on-Write**, scrive l'intero database su disco senza bloccare il processo padre. Viene attivato dopo X secondi e Y cambiamenti, o manualmente.
*   **Append Only File (AOF):** Registra ogni operazione di scrittura in un log. La frequenza di **fsync()** su disco può essere impostata su **Always**, **Every second** (compromesso ideale), o **Never**.

**5.3. Modellazione Dati Operativa (Esercizio)**
*   **Obiettivo:** Supportare la query "prodotti acquistati da un utente" per James e Chris.
*   **Comandi Redis per James (Ordini 1 e 3):**
    **SADD ords_james_ordID 1 3**
    **HSET order_1 user "james" product_28 1 product_372 2**
*   **Comandi Redis per Chris (Ordine 2):**
    **SADD ords_chris_ordID 2**
    **HSET order_2 user "chris" product_15 1 product_160 5 product_201 7**

**5.4. Manuale dei Comandi Principali**
*   **GETSET key value**: Ottiene il vecchio valore e imposta il nuovo (O(1)).
*   **HSET / HGET key field**: Gestione campi in un Hash (O(1)).
*   **SINTER key1 key2**: Intersezione tra Set (O(C*M)).
*   **ZADD key score member**: Aggiunta a un Sorted Set (O(log(N))).
*   **ZRANGE key start stop**: Recupero di un range per indice (O(log(N)+M)).

**Avvertenza Architetturale:** Poiché Redis opera con un **single-threaded event loop**, l'esecuzione di comandi con complessità **O(N)** su set di dati molto vasti può "bloccare" l'intero server per tutti gli altri utenti.

---

### 6. Tecnologie Big Data in Azione: Il Caso Facebook

**6.1. Workflow di Analisi Massiva**
Facebook gestisce oltre 100 PB di dati in un singolo cluster **Apache Hadoop**. Il sistema si basa su **HDFS** per lo storage distribuito e su **MapReduce** per eseguire calcoli paralleli su scala massiva.

**6.2. Interfacciamento SQL-like con Hive**
**Apache Hive** consente l'accesso ai dati HDFS tramite una sintassi SQL-like, integrando la valutazione delle query direttamente con il paradigma MapReduce per l'elaborazione batch.

**6.3. Procedure Specialistiche**
*   **Apache HBase:** Database column-family su Hadoop. È stato introdotto come **sostituto di MySQL e Cassandra** per la gestione di messaggistica, chat e SMS.
*   **Memcached:** Store chiave-valore distribuito, utilizzato storicamente come cache tra i web server e i server **MySQL** agli albori di Facebook.
*   **Apache Giraph:** Database a grafo utilizzato per analizzare trilioni di archi (connessioni tra utenti). Nota: la tecnologia è **attualmente ritirata (retired)**, ma rimane un riferimento storico per l'analisi di grafi massivi.
*   **RocksDB:** Motore di storage chiave-valore ad alte prestazioni, sviluppato internamente da Facebook e oggi open-source.

**Avvertenza Architetturale:** L'errore operativo classico è utilizzare Hive per query real-time; Hive è progettato per analisi batch e presenta latenze non compatibili con l'interattività immediata.

---

### 7. Chiusura del Capitolo

**7.1. Checklist Applicativa Finale**
Prima del deploy, l'architetto dati deve convalidare i seguenti punti:
- [ ] I confini degli aggregati sono coerenti con le necessità di isolamento ACID e scalabilità?
- [ ] La strategia di persistenza Redis (AOF/BGSAVE) bilancia correttamente performance e tolleranza ai guasti?
- [ ] La logica di join manuale gestisce correttamente i fallimenti parziali della transazione?
- [ ] Lo stato dell'aggregato è verificato durante tutto il ciclo di vita (es. finalizzazione dell'acquisto)?
- [ ] Sono stati analizzati i rischi di blocco del server Redis causati da query O(N) su chiavi massive?

**7.2. Domande di Autovalutazione**
1. In che modo la delimitazione degli aggregati permette di evitare i lock distribuiti?
2. Descrivere l'interazione tra il processo padre e il processo figlio durante una **BGSAVE** e l'impatto della memoria virtuale tramite Copy-on-Write.
3. Perché nei database a grafo il costo computazionale della relazione è spostato dal momento della query al momento dell'inserimento?
4. Quale evoluzione tecnologica ha portato Facebook a preferire Apache HBase rispetto a MySQL e Cassandra per la messaggistica?
5. Quali sono i rischi legati all'uso di un ID di un aggregato come riferimento manuale in un altro documento NoSQL?

**7.3. Mini-Riepilogo**
La gestione operativa NoSQL richiede che l'architetto si faccia carico della consistenza e delle relazioni, spostando la complessità dal database al codice applicativo. Gli aggregati fungono da unità di distribuzione e atomicità per garantire la scalabilità orizzontale. Mentre i grafi ottimizzano la navigazione di relazioni persistite, strumenti come Redis forniscono velocità estrema in memoria, a patto di gestire con cautela la persistenza e la complessità computazionale dei comandi. Infine, l'ecosistema Big Data (Hadoop, Hive, HBase) permette di scalare l'analisi su volumi di petabyte, superando i limiti dei sistemi relazionali tradizionali.