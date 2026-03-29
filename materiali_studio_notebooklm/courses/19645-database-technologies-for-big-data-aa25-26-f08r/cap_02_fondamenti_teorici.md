# Capitolo 2 - Fondamenti Teorici delle Architetture NoSQL

## 1. Il Concetto di Aggregato nei Database NoSQL

### 1.1. Definizione e Proprietà Formali
Nel panorama delle architetture dati distribuite, l'**aggregato** rappresenta il pilastro fondamentale della modellazione NoSQL. Formalmente, definiamo l'aggregato come una collezione di dati correlati che l'applicazione tratta come un'unità atomica di interazione. Si assiste qui a una necessaria dicotomia tra **unità logica** (la visione dell'applicazione) e **unità fisica** (la memorizzazione sul disco), superando la frammentazione atomica tipica della normalizzazione relazionale.

### 1.2. Assunzioni e Vincoli Operativi: Il Confine ACID
L'aggregato definisce il limite di demarcazione (boundary) per le operazioni **ACID**. Nei sistemi orientati agli aggregati, le garanzie di atomicità, consistenza, isolamento e durabilità sono assicurate esclusivamente all'interno del singolo aggregato. Qualsiasi operazione che coinvolga una mutazione coordinata su più aggregati non è supportata nativamente dal motore del database; ne consegue che l'onere della gestione della consistenza transazionale ricade interamente sulla logica applicativa sviluppata dal programmatore.

### 1.3. Vantaggi Architetturali e Distribuzione
La scelta di modellare per aggregati risponde a precise esigenze di scalabilità e performance:
*   **Semplificazione dello Sharding**: L'aggregato, essendo un'unità autocontenuta, facilita la distribuzione dei dati su cluster (sharding). Poiché il confine dell'aggregato impedisce join tra nodi diversi, il sistema evita i costi computazionali e le latenze della rete associati alla ricomposizione di dati frammentati su più partizioni.
*   **Ottimizzazione del Retrieval**: Tali database eccellono quando la maggior parte delle interazioni avviene operando sulla medesima unità informativa, riducendo drasticamente il numero di operazioni di I/O necessarie.

**Analisi Comparativa della Gestione Transazionale**

| Caratteristica | RDBMS Tradizionale | Database Orientato agli Aggregati |
| :--- | :--- | :--- |
| **Ambito ACID** | Esteso a più righe e tabelle tramite transazioni. | Limitato rigorosamente al singolo aggregato. |
| **Responsabilità** | Garantita dal DBMS. | Delegata al programmatore per operazioni multi-aggregato. |
| **Unità di Accesso** | Singola riga (row). | L'intero aggregato. |

---

## 2. Gestione delle Relazioni tra Aggregati

### 2.1. Modellazione dei Legami e Referencing
Le relazioni tra aggregati distinti vengono implementate mediante l'inserimento dell'identificativo (ID) di un aggregato all'interno della struttura dati di un altro. Questa tecnica, denominata **referencing**, stabilisce un collegamento logico che non comporta la persistenza fisica dell'oggetto correlato nello stesso spazio di memoria.

### 2.2. L'Ignoranza del Database (Database Ignorance)
A differenza dei sistemi RDBMS, il motore NoSQL è caratterizzato da una profonda "ignoranza" riguardo alle relazioni logiche persistite. Il sistema non possiede consapevolezza semantica del valore contenuto in un campo ID di riferimento; pertanto, non è in grado di imporre **vincoli di integrità referenziale** (Foreign Keys). La sicurezza del dato e la consistenza dei legami non sono garantite dal database, ma devono essere preservate dalla logica software.

### 2.3. Join Applicative
In assenza di un motore di join interno, la responsabilità di collegare i dati tra aggregati spetta alla **join applicativa**. Il programmatore deve implementare una sequenza di operazioni: recuperare l'ID dall'aggregato primario e, successivamente, eseguire una query distinta per estrarre le informazioni correlate dall'aggregato di destinazione.

### 2.4. Metadati e Visibilità dei Legami
Sistemi specifici come **Riak** permettono di inserire informazioni di collegamento (link) direttamente nei metadati, offrendo al database una parziale visibilità sulle interconnessioni. Tuttavia, permane la problematica della gestione degli aggiornamenti coordinati.

**Esempio di Modellazione Logica (JSON)**
Si osservi come l'aggregato `orders` contenga il riferimento `customerId`. Per il motore NoSQL, questo è un semplice intero, privo di legami di integrità verso l'aggregato `customers`.

```json
// Aggregato Customer (Unità logica 1)
{
  "id": 1,
  "name": "Martin",
  "billingAddress": [{"city": "Chicago"}]
}

// Aggregato Order (Il database ignora la validità di customerId)
{
  "id": 99,
  "customerId": 1, 
  "orderItems": [
    {
      "productId": 27,
      "price": 32.45,
      "productName": "NoSQL Distilled"
    }
  ],
  "shippingAddress": [{"city": "Chicago"}]
}
```

---

## 3. Database a Grafo: Teoria e Missione

### 3.1. Limiti del Modello Relazionale e Rigidezza dello Schema
Il modello a grafo emerge dalla necessità di superare la frustrazione computazionale degli RDBMS in contesti densamente interconnessi. In un sistema relazionale, la rappresentazione di strutture gerarchiche (es. la query "Chi è il mio manager") o di reti sociali richiede join ricorsive o molteplici che degradano rapidamente le prestazioni. Inoltre, l'aggiunta di una nuova tipologia di relazione in un RDBMS impone spesso radicali e costose modifiche allo schema e ai dati preesistenti.

### 3.2. Modello Formale: Nodi, Archi e Proprietà
*   **Nodi**: Rappresentano le istanze degli oggetti (entità) e contengono proprietà (es. `name`).
*   **Archi (Edges)**: Esprimono le relazioni, possiedono una **significatività direzionale** e sono **tipizzati** (es. "likes", "friend", "employee").
*   **Proprietà**: Coppie chiave-valore applicabili sia ai nodi che agli archi per arricchirne il contenuto informativo.

### 3.3. Persistenza vs Calcolo
Mentre in un RDBMS la relazione è calcolata al momento della query (query-time), nei database a grafo la relazione è **persistita fisicamente**. Questo sposta l'onere computazionale dalla fase di interrogazione alla fase di inserimento (insert-time).

### 3.4. Efficienza del Traversal
L'operazione di attraversamento (**traversal**) è estremamente economica poiché consiste nel seguire puntatori fisici tra nodi. La performance è influenzata solo dalla porzione di grafo esplorata e non dalla dimensione totale del dataset.

**Confronto: Relazionale vs Grafo**

| Caratteristica | Database Relazionali | Database a Grafo |
| :--- | :--- | :--- |
| **Implementazione Relazioni** | Tramite Foreign Keys (chiavi esterne). | Tramite Archi persistiti fisicamente. |
| **Costo delle Interconnessioni** | Elevato (Join costose a query-time). | Molto basso (Traversal economico). |
| **Momento del Carico** | Query-time (calcolo al volo). | Insert-time (carico in fase di scrittura). |
| **Modellazione** | Basata sul traversal atteso (rigida). | Basata su entità e relazioni (flessibile). |

---

## 4. Varianti del Modello a Grafo e Implementazioni

### 4.1. Analisi delle Implementazioni
*   **Neo4J**: Adotta un approccio schemaless, memorizzando oggetti Java come nodi e archi.
*   **InfiniteGraph**: Richiede l'ereditarietà da sottoclassi di tipi predefiniti per la definizione della struttura.

### 4.2. Meccanismi di Query e Anchor Nodes
L'interrogazione inizia sempre da un **Anchor Node** (punto di partenza), individuato solitamente tramite indici su attributi specifici (es. ID). Da qui, il motore naviga la rete di archi.

### 4.3. Esempio Pratico di Traversal
Si consideri la query: *"Trovare i dipendenti di BigCo a cui piace 'NoSQL Distilled'"*.
1.  **Start**: Identificazione dell'anchor node "BigCo".
2.  **Step 1**: Attraversamento degli archi di tipo `employee` verso i nodi intermedi: **Anna**, **Barbara** e **Carol**.
3.  **Step 2**: Navigazione dai nodi intermedi verso l'arco `likes`.
4.  **Result**: Se l'arco `likes` punta al nodo "NoSQL Distilled", il nome del dipendente viene incluso nel set dei risultati.

### 4.4. Rappresentanti del Mercato
Le tecnologie principali includono **Neo4J**, **OrientDB** e **NebulaGraph**. Si noti che **Apache Giraph**, un tempo leader per l'analisi di grafi su scala massiva, è oggi considerato **ritirato (retired)**.

---

## 5. Sistemi Key-Value: Il Caso Redis

### 5.1. Architettura e Filosofia
Redis (**REmote DIctionary Server**) è un database in-memory basato su un modello **single-threaded event loop**, progettato per garantire la massima efficienza prestazionale.

### 5.2. Modello Dati Logico
*   **Keys**: Vincolate all'uso di caratteri **ASCII stampabili**.
*   **Values**:
    *   **Primitive**: Stringhe (limite 512MB).
    *   **Container**: Hashes (O(1) per accesso ai campi), Lists, Sets e Sorted Sets (Z-Sets).

### 5.3. Persistenza dei Dati
Redis implementa due meccanismi di persistenza per prevenire la perdita di dati in-memory:
1.  **RDB (Periodic Dump)**: Istantanea del DB eseguita tramite `fork()` del sistema operativo con meccanismo **Copy-on-Write (CoW)**.
2.  **AOF (Append Only File)**: Log delle operazioni di scrittura con frequenza di `fsync()` configurabile (*always*, *every second*, *never*).

### 5.4. Complessità Computazionale e Modellazione
Le operazioni presentano complessità formali rigorose: `HSET` è **O(1)**, mentre `SDIFF` (differenza tra set) è **O(N)**, dove **N** rappresenta il numero totale di elementi in tutti i set coinvolti nel confronto.

**Modello Redis per Acquisto Prodotti**
Per supportare la query "prodotti acquistati da un utente", separiamo l'indice (Set) dai dati (Hash):

```bash
# Layer Indice: Collegamento Utenti -> Ordini
SADD ords_james_ordID 1 3
SADD ords_chris_ordID 2

# Layer Dati: Dettaglio Ordine tramite Hashes
HSET order_1 user "james" product_28 1 product_372 2
HSET order_2 user "chris" product_15 1 product_160 5 product_201 7
```

---

## 6. L'Ecosistema Facebook: NoSQL in Action

L'evoluzione di Facebook ha portato al superamento del classico stack LAMP. La "M" di MySQL è stata affiancata da una suite di tecnologie specializzate:
*   **Apache Hadoop/HDFS**: Storage distribuito di massa (oltre 100 PB per cluster).
*   **Apache Hive**: Fornisce accesso SQL-like ai dati Hadoop integrando MapReduce.
*   **Apache HBase**: Database column-family che funge da sostituto per **MySQL e Cassandra** nella gestione di messaggistica e SMS.
*   **Memcached**: Storico layer di caching tra web server e database.
*   **RocksDB**: Key-value store ad altissime prestazioni sviluppato internamente.
*   **Apache Giraph**: Sebbene oggi **ritirato**, è stato fondamentale dal 2013 per l'analisi di grafi con trilioni di archi.

---

## 7. Strumenti Didattici e Valutazione

### 7.1. Esercizi con Soluzione Spiegata
1.  **Query su Set**: L'utente James ha acquistato i prodotti {1, 2, 3}, l'utente Chris {2, 4}. Quale comando identifica i prodotti esclusivi di James?
    *   *Soluzione*: `SDIFF set_James set_Chris`. Risultato: {1, 3}. La complessità è O(N), proporzionale al totale degli elementi.
2.  **Modellazione**: Perché un social network predilige i grafi rispetto agli aggregati?
    *   *Soluzione*: Perché l'entità principale è la relazione (arco). Gli aggregati sono ideali quando i dati sono letti insieme, ma non quando le connessioni sono arbitrarie e fitte.

### 7.2. Errori Frequenti (Misconceptions)
*   **Atomicità**: Pensare che NoSQL garantisca atomicità su più aggregati; è limitata a uno solo.
*   **Dinamicità dei Grafi**: Credere che le relazioni nei grafi siano calcolate al volo come in SQL; esse sono invece persistite all'inserimento.

### 7.3. Domande di Autovalutazione
1.  Definisci la differenza tra unità logica e fisica in un aggregato.
2.  Perché la "Database Ignorance" è un rischio per l'integrità dei dati?
3.  Qual è il vantaggio del meccanismo Copy-on-Write nel dump RDB di Redis?
4.  In un database a grafo, cosa accade se cambia la tipologia di traversal richiesta?
5.  Quali sistemi ha sostituito Apache HBase nell'infrastruttura di Facebook?

### 7.4. Sintesi Finale
La scelta del modello NoSQL non è estetica ma funzionale: gli **aggregati** ottimizzano la distribuzione e l'accesso atomico; i **grafi** gestiscono la complessità delle interconnessioni persistendo i legami; i sistemi **key-value** massimizzano le performance in-memory per strutture dati elementari.

---

## Laboratorio Docker

Per avviare un ambiente Redis di test, utilizzare i seguenti comandi. Il flag `-d` indica la modalità **detached**, che esegue il container in background lasciando libera la shell.

```bash
# Avvio dell'ambiente in modalità detached
docker compose up -d

# Accesso alla CLI interattiva di Redis
docker exec -it redis-redis-1 redis-cli

# Gestione del container
docker compose stop
docker compose start
```