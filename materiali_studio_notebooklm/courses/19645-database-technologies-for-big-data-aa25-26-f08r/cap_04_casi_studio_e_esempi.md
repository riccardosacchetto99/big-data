# Capitolo 4 - Casi studio ed esempi concreti

## 1. Il Concetto di Aggregato nei Database NoSQL

Nel dominio dei sistemi distribuiti, la progettazione prescinde dalla singola riga per focalizzarsi sull'**Aggregato**, inteso come una collezione di dati correlati che vengono trattati dall'applicazione come un'unica unità atomica. Dal punto di vista architettonico, l'aggregato non è solo un raggruppamento logico, ma definisce i **confini per le operazioni ACID** (Atomicità, Consistenza, Isolamento, Durabilità). Mentre in un RDBMS la consistenza transazionale può estendersi su intere tabelle, in un database orientato agli aggregati le garanzie ACID sono solitamente limitate all'interno del singolo aggregato.

**Vantaggi degli aggregati nella gestione dello storage su cluster:**
*   **Località del dato:** Poiché l'aggregato è l'unità di retrieval, il database può memorizzare fisicamente tutti i dati correlati sullo stesso nodo del cluster, minimizzando i trasferimenti di rete.
*   **Scalabilità orizzontale:** Gli aggregati facilitano il partizionamento (sharding) dei dati, poiché il sistema può distribuire unità indipendenti su nodi diversi senza frammentare la logica di accesso.
*   **Performance ottimali:** Questa architettura eccelle negli scenari in cui la maggior parte delle interazioni avviene con lo stesso aggregato (*most data interaction with the same aggregate*).

**Trade-off e gestione delle relazioni:**
Il trade-off fondamentale risiede nella gestione delle relazioni inter-aggregato. In NoSQL, il database è intrinsecamente **"ignorante"** riguardo ai collegamenti tra aggregati diversi: la relazione è espressa inserendo l'ID di un aggregato nel corpo di un altro.
Tuttavia, esistono sfumature ingegneristiche: alcuni sistemi come **Riak** permettono di rendere tali relazioni "visibili" al database tramite l'inserimento di metadati. È fondamentale però distinguere tra *visibilità* e *vincolo*: a differenza di una Foreign Key in un RDBMS, che è **imposta** dal motore, in ambito NoSQL la gestione dell'integrità e l'esecuzione delle join sono delegate interamente al layer applicativo.

---

## 2. Graph Databases: Oltre i Limiti del Modello Relazionale

I database a grafo rappresentano un cambio di paradigma: il passaggio dalla **complessità computazionale** (le costose JOIN a runtime degli RDBMS) alla **complessità strutturale** (archi persistiti direttamente sul disco). La motivazione risiede nella frustrazione derivante dalla gestione di dati altamente interconnessi in schemi tabulari, dove ogni nuova relazione implica modifiche strutturali rigide.

### Confronto Rigoroso: RDBMS vs. Graph Databases

| Parametro | RDBMS | Graph Databases |
| :--- | :--- | :--- |
| **Implementazione Relazioni** | Tramite Foreign Keys (chiavi esterne). | Relazioni persistite direttamente (Edge). |
| **Costo di Join/Traversal** | Elevato; cresce esponenzialmente con la profondità. | Molto basso; il traversal è un'operazione economica. |
| **Shift del Carico di Lavoro** | Concentrato al momento della Query (Query time). | Spostato al momento dell'Inserimento (Insert time). |
| **Atomicità dei dati** | Basata su righe e transazioni multi-tabella. | Basata su Nodi e Archi come entità atomiche. |
| **Flessibilità** | Rigido; modellazione basata sul traversal atteso. | Flessibile; permette di scoprire pattern imprevisti. |

**Caso Studio: Pattern di ricerca e implementazioni**
Si consideri la query: *"Trovare i dipendenti di BigCo a cui piace NoSQL Distilled"*. Nello schema fornito, partiremmo dal nodo ancora "BigCo", navigheremmo gli archi `employee` verso i nodi Anna, Barbara e Carol, e da questi verificheremmo l'esistenza dell'arco `likes` verso il nodo "NoSQL Distilled". 

Le varianti tecnologiche offrono approcci distinti:
*   **Neo4j:** Gestisce in modo *schemaless* oggetti Java mappati direttamente su nodi e archi.
*   **InfiniteGraph:** Adotta un approccio più tipizzato, utilizzando **sottoclassi di tipi predefiniti** (built-in types) per modellare la struttura del grafo.

---

## 3. Caso Studio: L'Evoluzione dell'Ecosistema Dati di Facebook

L'architettura di Facebook dimostra come scalare oltre il modello LAMP tradizionale. In questa evoluzione, la "M" (MySQL) non è stata eliminata, ma affiancata e in molti casi sostituita da sistemi di data management specializzati per risolvere colli di bottiglia specifici.

### Mappatura delle Componenti Architetturali

#### A. Storage & Massiccia Scalabilità
*   **Apache Hadoop (HDFS):** Gestisce oltre **100 PB** in un singolo cluster. HDFS funge da repository primario per i dati non strutturati.

#### B. Query, Analisi & Elaborazione
*   **MapReduce:** Abilita computazioni parallele massive su Hadoop.
*   **Apache Hive:** Fornisce un'interfaccia **SQL-like** per interrogare i dati su HDFS, traducendo le query in job MapReduce.
*   **Apache Giraph:** Utilizzato per l'analisi dei grafi (connessioni tra utenti) su scala di trilioni di archi. Sebbene oggi sia indicato come "ritirato", è stato fondamentale per i task analitici dal 2013.

#### C. Service & Operational Layer
*   **Apache HBase:** Database di tipo column-family integrato in Hadoop. È stato adottato come **sostituto di MySQL e Cassandra** per la gestione di messaggistica istantanea, e-mail e SMS.
*   **Memcached:** Store Key-Value distribuito usato come cache tra web server e database per ridurre drasticamente la latenza di lettura.
*   **RocksDB:** Store Key-Value *embeddable* ad alte prestazioni, sviluppato internamente per casi d'uso a bassa latenza e successivamente reso open-source.

---

## 4. Modellazione Pratica con Redis: Persistence e Strutture Dati

Redis si definisce come un "Main memory database" caratterizzato da un event loop a thread singolo. Questa natura richiede una comprensione profonda dei meccanismi di persistenza per bilanciare sicurezza e performance.

### Confronto Tecnico sui Meccanismi di Persistenza

1.  **Periodic Dump (BGSAVE):**
    Utilizza la chiamata di sistema `fork()` con meccanismo **Copy-on-Write**. Il processo figlio scrive l'intero database su disco in modo asincrono. Viene attivato automaticamente dopo $X$ secondi e $Y$ cambiamenti, o manualmente tramite comando `BGSAVE`.
2.  **Append Only File (AOF):**
    Registra ogni operazione di scrittura in un log file. Il trade-off è gestito tramite lo schedule di `fsync()`:
    *   **Always:** Massima sicurezza; ogni scrittura è sincronizzata (minor throughput).
    *   **Every second:** Compromesso ottimale (default).
    *   **Never:** Le prestazioni sono massime, ma la persistenza è delegata alle politiche di buffer del **sistema operativo**, aumentando il rischio di perdita dati.

### Guida alla Modellazione: Query sui prodotti acquistati

Obiettivo: Ottenere i nomi dei prodotti acquistati dall'utente "James".

**Fase 1: Preparazione dei dati (Writing)**
Utilizziamo un **SET** per indicizzare gli ordini di un utente e degli **HASH** per contenere i dettagli dell'ordine.
```redis
# Associazioni Utente -> Ordini
SADD ords_james_ordID 1 3
SADD ords_chris_ordID 2

# Dettagli Ordine 1 (James)
HSET order_1 user "james" product_28 1 product_372 2
# Dettagli Ordine 2 (Chris)
HSET order_2 user "chris" product_15 1 product_160 5 product_201 7
```

**Fase 2: Esecuzione della Query (Reading)**
Per ottenere i prodotti di James, l'applicazione deve seguire questo workflow:
1.  **Recupero ID ordini:** `SMEMBERS ords_james_ordID` -> Ritorna [1, 3]
2.  **Iterazione e recupero dettagli:** Per ogni ID (es. 1), eseguire `HGETALL order_1`.
3.  **Filtraggio:** L'applicazione estrae i campi `product_x` dal risultato dell'hash.

---

## 5. Analisi degli Errori Frequenti e Best Practices

Dal punto di vista della progettazione di soluzioni, l'errore più comune è l'applicazione di vecchi schemi mentali relazionali a nuovi paradigmi:

1.  **Assumere ACID multi-aggregato:** È un errore critico delegare la consistenza tra aggregati al database. In NoSQL, se un'operazione deve aggiornare due aggregati, è **responsabilità esclusiva del programmatore** gestire l'eventuale fallimento parziale (es. tramite pattern Saga o consistenza eventuale).
2.  **Sottovalutazione del debito tecnico negli RDBMS:** Quando si modellano strutture "graph-like" (es. gerarchie ricorsive "Chi è il mio manager?"), in un RDBMS si è costretti a modellare lo schema preventivamente in base al traversal. Se il tipo di ricerca cambia, il costo in termini di modifiche allo schema e performance delle JOIN ricorsive diventa insostenibile. Nei Graph DB, la relazione è un'entità di prima classe, rendendo il sistema resiliente al cambiamento.
3.  **Configurazione errata di Redis:** Utilizzare Redis senza configurare correttamente l'AOF o il BGSAVE può portare a una percezione di instabilità. La scelta tra `fsync Always` e `Every second` deve essere dettata dal valore economico del singolo dato rispetto alla latenza richiesta.

---

## 6. Strumenti di Autovalutazione

### Domande di Revisione
1.  Qual è la differenza fondamentale tra come un RDBMS e un database come Riak trattano i collegamenti (links) tra i dati?
2.  Perché i Graph Database spostano il carico di lavoro dal "Query time" all' "Insert time"?
3.  In Redis, quale meccanismo di persistenza garantisce minori perdite di dati in caso di crash improvviso e perché?
4.  Nel caso studio Facebook, quale tecnologia ha sostituito MySQL per la gestione specifica dei messaggi e degli SMS?
5.  Cosa si intende per "confini ACID" nell'architettura orientata agli aggregati?

### Mini-Riepilogo Finale
Il passaggio dai modelli RDBMS generalisti alle soluzioni NoSQL non è una semplice evoluzione tecnologica, ma una specializzazione funzionale. La scelta non deve basarsi sulla popolarità del tool, ma sulla **natura intrinseca dei dati** (aggregati indipendenti vs. grafi densi) e sui **pattern di accesso**. L'architetto moderno deve accettare di spostare la logica di join e consistenza dal motore database al codice applicativo per guadagnare scalabilità e flessibilità.