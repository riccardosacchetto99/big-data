# Capitolo 1 - Quadro generale del corso

## 1. Introduzione e Obiettivi del Corso
Il presente corso delinea il passaggio paradigmatico dalla rigidità strutturale dei database relazionali (RDBMS) alla flessibilità e scalabilità orizzontale dei sistemi NoSQL. La missione principale è fornire gli strumenti metodologici per superare il "mismatch" di impedenza tra i modelli a oggetti moderni e le tabelle normalizzate, guidando lo studente verso la gestione di dati massivi.

Gli obiettivi formativi si articolano su tre direttrici fondamentali:
*   **Modellazione Avanzata:** Comprendere il concetto di "Aggregato" come unità fondamentale di interazione e apprendere la gestione di relazioni complesse attraverso i modelli a grafo.
*   **Analisi Industriale:** Studiare lo stack tecnologico di realtà su scala planetaria (es. Facebook) per comprendere come diverse tecnologie NoSQL possano coesistere per risolvere problemi specifici.
*   **Competenza Tecnica:** Acquisire abilità operative nell'uso di strumenti quali Docker e Redis-CLI, passando dalla teoria dei modelli alla pratica delle implementazioni.

## 2. Lessico Tecnico Fondamentale
La precisione terminologica è il presupposto della competenza ingegneristica. Si definiscono i seguenti termini cardine:

*   **Aggregate (Aggregato):** Una collezione di dati correlati che trattiamo come una singola unità logica. L'aggregato costituisce il confine fondamentale per la gestione della persistenza e della distribuzione su cluster.
*   **Key-Value Store:** Sistemi basati su coppie chiave-valore (es. Redis, Riak, RocksDB), ideali per accesso rapido basato su identificatori univoci.
*   **Graph Database:** Sistemi che modellano entità (Nodi) e relazioni (Archi o Edges) dotati di proprietà. Sono ottimizzati per dati con interconnessioni dense.
*   **ACID Boundaries:** Il perimetro entro cui sono garantite Atomicità, Consistenza, Isolamento e Durata. Nei sistemi NoSQL orientati all'aggregato, tale garanzia è solitamente limitata al singolo aggregato, a differenza degli RDBMS che estendono le transazioni su più tabelle/righe.
*   **Anchor Node (Nodo Ancora):** Il punto di partenza necessario per ogni interrogazione su un grafo; le query iniziano da un nodo specifico, spesso indicizzato tramite ID, per poi procedere alla navigazione.
*   **Traversal (Traversata):** L'operazione di navigazione attraverso la rete di archi partendo da un Anchor Node per identificare pattern o relazioni.
*   **Persistence (RDB vs AOF):** In Redis, si distingue tra **Periodic Dump (BGSAVE)**, che salva l'intera memoria su disco a intervalli configurati, e **Append Only File (AOF)**, che registra ogni operazione di scrittura in un log incrementale.

## 3. Prerequisiti e Motivazioni: Oltre il Modello Relazionale
L'adozione del NoSQL nasce da una specifica "frustrazione" tecnica: l'incapacità dei modelli relazionali di gestire efficientemente relazioni altamente connesse senza incorrere in `JOIN` computazionalmente proibitive. 

Il passaggio al NoSQL comporta un inversione dell'onere computazionale: si sposta il carico dal **tempo di query (query time)** al **tempo di inserimento (insert time)**. I dati vengono strutturati in fase di scrittura per minimizzare il lavoro necessario in fase di lettura. Questo richiede una solida comprensione delle transazioni ACID e, in alcuni contesti (es. Neo4J o InfiniteGraph), la capacità di operare con linguaggi di programmazione come Java per definire tipi di nodi e archi personalizzati.

## 4. Mappa dei Contenuti e Modelli Dati
Il corso copre la tassonomia dei sistemi NoSQL associando a ogni modello le tecnologie leader del settore:

| Modello Dati | Tecnologie di Riferimento |
| :--- | :--- |
| **Key-Value** | Redis, Riak, RocksDB, Memcached |
| **Column-family** | Apache HBase (ecosistema Hadoop) |
| **Graph** | Neo4J, OrientDB, NebulaGraph, Apache Giraph, InfiniteGraph |
| **Big Data Ecosystem** | Apache Hadoop (HDFS, MapReduce), Apache Hive |

In Redis, i dati sono organizzati gerarchicamente: dalle **Primitive** (Stringhe con limite fisico di 512MB) ai **Container** più complessi (Hashes, Lists, Sets, Sorted Sets).

## 5. Collegamenti tra i Temi: Aggregati, Relazioni e Performance
La gestione delle relazioni è il terreno di scontro tra i diversi approcci:
1.  **Ignoranza delle Relazioni:** Molti NoSQL sono "ignari" delle relazioni esterne all'aggregato. Se un documento ordine punta a un ID cliente, il "join" logico deve essere implementato dal programmatore nel codice applicativo.
2.  **Soluzioni Ibride (Riak):** Alcuni sistemi, come Riak, permettono di inserire informazioni di collegamento (link) direttamente nei metadati, rendendo la relazione parzialmente visibile al database.
3.  **Potenza dei Graph DB:** Negli RDBMS, il grafo deve essere modellato preventivamente in base alle traversate attese; ogni nuova relazione richiede pesanti modifiche allo schema. Nei Graph DB, la relazione è **persistita** come entità primaria, rendendo le traversate estremamente economiche e il modello intrinsecamente flessibile.

## 6. Analisi di Casi Reali: L'Ecosistema Facebook
Lo stack tecnologico di Facebook rappresenta l'apice dell'applicazione industriale NoSQL:

*   **Hadoop/HDFS:** Gestione di cluster singoli oltre i 100 PB per calcoli massivi.
*   **Apache Hive:** Fornisce accesso SQL-like ai dati in HDFS, integrando la valutazione delle query direttamente in job **MapReduce**.
*   **Apache HBase:** Database column-family utilizzato per e-mail e messaggistica istantanea, scelto come sostituto più efficiente per MySQL e Cassandra.
*   **Memcached:** Store key-value distribuito, utilizzato come layer di caching tra i web server e i database MySQL.
*   **RocksDB:** Motore key-value ad altissime prestazioni sviluppato internamente da Facebook per carichi di lavoro specifici.
*   **Apache Giraph:** Specializzato nell'elaborazione di grafi su scala di trilioni di archi, fondamentale per analizzare le connessioni tra gli utenti.

## 7. Approfondimento Tecnico: Redis (REmote DIctionary Server)
Redis opera come un database in-memory con un'architettura **single-threaded event loop**. È imperativo comprendere che, essendo single-threaded, comandi con complessità O(N) su grandi dataset possono bloccare l'intero server, degradando le performance globali.

### 7.1 Meccanismi di Persistenza
*   **BGSAVE:** Attiva un dump periodico. Il sistema esegue una `fork()` del processo creando un figlio che, tramite il meccanismo **Copy-on-Write**, scrive lo stato della memoria su disco. Questo processo può essere attivato manualmente o automaticamente dopo X secondi e Y cambiamenti.
*   **Append Only File (AOF):** Registra ogni scrittura. La durabilità dipende dalla frequenza di `fsync()` (impostabile su *Always*, *Every second* o *Never*).

### 7.2 Comandi e Complessità Computazionale
| Tipo | Comando | Descrizione | Complessità |
| :--- | :--- | :--- | :--- |
| **Stringhe** | `GETSET` | Legge il vecchio valore e imposta il nuovo. | O(1) |
| **Hashes** | `HSET` / `HGET` | Scrittura/Lettura di un campo specifico. | O(1) |
| **Hashes** | `HEXISTS` / `HDEL` | Verifica esistenza o cancellazione campo. | O(1) |
| **Hashes** | `HMGET` | Lettura di molteplici campi. | **O(N)** |
| **Hashes** | `HKEYS` / `HVALS` | Estrazione di tutte le chiavi/valori (Pericolo blocco). | **O(N)** |
| **Sets** | `SINTER` | Intersezione tra più insiemi. | O(N*M) |
| **Sorted Sets**| `ZADD` | Inserimento elemento con score. | O(log(N)) |

## 8. Esercitazione: Modellazione Dati per Ordini e Prodotti
Obiettivo: Modellare in Redis un sistema per recuperare i prodotti acquistati dagli utenti James e Chris.

### 8.1 Strategia di Modellazione
Utilizziamo i `SET` per indicizzare gli ordini per utente e gli `HASH` per i dettagli dell'ordine, permettendo un accesso rapido e strutturato.

### 8.2 Implementazione CLI (Mock-up)
Di seguito i comandi da eseguire tramite `redis-cli` (accessibile via Docker con `docker exec -it redis-redis-1 redis-cli`):

```bash
# 1. Creazione degli indici ordini per utente (SET)
SADD ords_james_ordID 1 3
SADD ords_chris_ordID 2

# 2. Creazione dei dettagli ordini (HASH)
HMSET order_1 user james product_28 1 product_372 2
HMSET order_2 user chris product_15 1 product_160 5 product_201 7
HMSET order_3 user james product_99 1

# 3. Query: Quali ordini ha James?
SMEMBERS ords_james_ordID

# 4. Query: Dettagli dell'ordine 1
HGETALL order_1
```

## 9. Errori Frequenti e Best Practices
*   **Gestione Multi-Aggregato:** L'atomicità è garantita solo all'interno di un singolo aggregato. Operazioni che coinvolgono più chiavi o aggregati richiedono una gestione della consistenza a livello applicativo (onere del programmatore).
*   **Operazioni Bloccanti:** Evitare l'uso di `HKEYS` o `SMEMBERS` su dataset con milioni di elementi in ambienti di produzione; preferire approcci incrementali.
*   **Flessibilità Relazionale:** Mentre in un RDBMS aggiungere una relazione (es. "chi è il manager di chi") richiede modifiche allo schema, nei sistemi a grafo è sufficiente persistere un nuovo arco, preservando l'agilità del sistema.
*   **Limiti Fisici:** Non superare mai il limite di 512MB per le stringhe Redis per evitare eccezioni di sistema.

## 10. Domande di Autovalutazione
1.  Analizzare il funzionamento di `BGSAVE`: in che modo la funzione `fork()` e il `Copy-on-Write` garantiscono la non-interruzione del servizio?
2.  Spiegare perché l'uso di comandi O(N) in Redis è considerato un rischio architetturale maggiore rispetto a un sistema multi-threaded.
3.  In che senso il modello a grafi sposta il carico computazionale dal "query time" all'"insert time"?
4.  Descrivere il ruolo di Apache Hive nell'ecosistema Facebook, specificando la sua relazione con MapReduce.
5.  Perché la definizione dei confini dell'Aggregato è critica per la scalabilità orizzontale su cluster?

## 11. Mini-Riepilogo Finale
*   **Centralità dell'Aggregato:** Definisce l'unità di retrieval e il confine ACID.
*   **Polyglot Persistence:** Architetture come quella di Facebook dimostrano che non esiste un database universale, ma una combinazione di strumenti (KV, Column, Graph).
*   **Graph Advantage:** I database a grafo sono superiori per dati connessi perché persistono le relazioni invece di calcolarle.
*   **Redis Performance:** La velocità deriva dall'esecuzione in-memory e dal single-threading, ma richiede estrema attenzione alla complessità algoritmica dei comandi utilizzati.