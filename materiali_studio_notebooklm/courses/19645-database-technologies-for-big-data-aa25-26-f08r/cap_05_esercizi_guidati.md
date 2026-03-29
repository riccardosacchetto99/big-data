# Capitolo 5 - Esercizi guidati con soluzione

In qualità di architetti di sistemi dati, il vostro compito non si esaurisce nella conoscenza mnemonica delle tecnologie, ma risiede nella capacità di condurre un'analisi dei trade-off rigorosa. In questa sessione, esploreremo come i modelli NoSQL e le architetture distribuite affrontino i limiti di scalabilità dei sistemi tradizionali. Analizzate attentamente ogni scenario: la scelta di un modello rispetto a un altro determina non solo le performance, ma la stessa manutenibilità del sistema su larga scala.

---

## 1. Fondamenti degli Aggregati e Modelli NoSQL

### 1.1 Analisi Teorica Rigorosa: L'Aggregato come Unità di Distribuzione
Il concetto di **Aggregato** rappresenta l'unità fondamentale di interazione nei database NoSQL (Documentali, Key-Value, Column-family). Formalmente, è una collezione di dati correlati che trattiamo come una singola unità atomica.

Dal punto di vista architettonico, l'aggregato assolve due funzioni critiche:
1.  **Confine per le operazioni ACID**: A differenza dei RDBMS, che garantiscono ACID su più tabelle tramite transazioni complesse, i database orientati agli aggregati limitano solitamente il supporto transazionale al perimetro del singolo aggregato.
2.  **Semplificazione della gestione dei Cluster (Sharding)**: Si noti lo shift fondamentale nella gestione della distribuzione. Poiché l'aggregato è un'unità autosufficiente, il database può distribuire (sharding) i dati spostando l'intero blocco su un nodo diverso del cluster senza preoccuparsi di spezzare relazioni critiche o richiedere transazioni cross-node, migliorando drasticamente la scalabilità orizzontale.

### 1.2 Esercizio Guidato 1 - Modellazione ad Aggregati
**Problema**: Progettare una struttura JSON che rappresenti un ordine completo basandosi sul Source Context, distinguendo tra dati interni e riferimenti esterni.

**Soluzione Analitica**:
```json
// Aggregato "Order"
{
  "id": 99,
  "customerId": 1,        // Relationship among aggregates (Riferimento esterno)
  "orderItems": [         // Dati interni all'aggregato (Nested Objects)
    {
      "productId": 27,
      "price": 32.45,
      "productName": "NoSQL Distilled"
    }
  ],
  "shippingAddress": [{"city": "Chicago"}],
  "orderPayment": [
    {
      "ccinfo": "1000-1000-1000-1000",
      "txnId": "abelif879rft",
      "billingAddress": {"city": "Chicago"}
    }
  ]
}
```
**Ragionamento Architetturale**: 
Il campo `customerId` è un semplice ID. In questo contesto, il database è **ignorante della relazione** (*ignorant of the relationship*). La responsabilità di collegare l'ordine al cliente non ricade sul motore database (niente Join nativi), ma viene delegata interamente al codice applicativo (**Join applicativo**). Al contrario, gli `orderItems` risiedono all'interno del confine dell'aggregato perché la loro esistenza è strettamente legata a quella dell'ordine.

### 1.3 Decisione Passo-Passo: Nested Object vs. ID
Per discriminare cosa includere in un aggregato, seguite questo protocollo decisionale:
*   **Frequenza di Accesso**: Se i dati (es. indirizzo di spedizione) vengono letti sistematicamente insieme all'ID principale, l'inclusione come *Nested Object* è preferibile.
*   **Integrità e Atomicità**: Se è necessario che l'aggiornamento di due informazioni avvenga in modo "tutto o niente" (ACID), esse devono risiedere nello stesso aggregato.
*   **Ciclo di Vita**: Se un'entità (es. Cliente) continua a esistere indipendentemente dall'altra (es. Ordine), si utilizza il riferimento tramite ID.

### 1.4 Errori Frequenti e Sfumature Tecniche
*   **Responsabilità del Programmatore**: Un errore comune è presumere che il DB gestisca la consistenza tra più aggregati. Ricordate: gli aggiornamenti su più aggregati contemporaneamente sono responsabilità esclusiva dello sviluppatore.
*   **Eccezioni Notevoli (Riak)**: Sebbene la maggior parte dei DB ad aggregati non veda le relazioni, alcuni sistemi come **Riak** permettono di inserire informazioni sui legami (links) nei **metadati**, rendendo la struttura parzialmente visibile al database.

---

## 2. Gestione delle Relazioni e Database a Grafo

### 2.1 Esercizio Guidato 2 - Dal Relazionale al Grafo
**Scenario**: Trasformare la query relazionale "Trova i dipendenti di BigCo a cui piace il libro NoSQL Distilled" in un pattern di ricerca su grafo.

### 2.2 Soluzione: Modellazione e Pattern Matching
Per interrogare un grafo, è necessario definire un **Anchor Node** (nodo ancora), ovvero un punto di partenza indicizzato tramite un attributo come l'ID.

**Struttura del Grafo**:
*   **Nodi (Istanze)**: `[BigCo]`, `[Anna]`, `[Barbara]`, `[Carol]`, `[NoSQL Distilled]`.
*   **Archi (Relazioni persistite)**:
    *   `(Anna)-[:employee]->(BigCo)`
    *   `(Barbara)-[:employee]->(BigCo)`
    *   `(Carol)-[:employee]->(BigCo)`
    *   `(Anna)-[:likes]->(NoSQL Distilled)`
    *   `(Barbara)-[:likes]->(NoSQL Distilled)`

**Visualizzazione del Traversal**:
Il pattern di ricerca si esprime come navigazione della rete:
` (Company {name: "BigCo"}) <-[:employee]- (Employee) -[:likes]-> (Book {title: "NoSQL Distilled"}) `

### 2.3 Confronto Tecnico: RDBMS vs. Graph DB

| Caratteristica | RDBMS | Graph DB |
| :--- | :--- | :--- |
| **Implementazione Relazioni** | Foreign Keys (FK) | Archi persistiti fisicamente |
| **Costo dei Join** | Elevato (navigazione a query time) | Molto basso (traversal nativo) |
| **Performance** | Decadono su dati altamente connessi | Eccellenti per dati connessi |
| **Shift del carico** | **Query time** (calcolo relazioni) | **Insert time** (persistenza relazioni) |

### 2.4 Domanda di Autovalutazione
*Perché l'aggiunta di una relazione in un RDBMS è onerosa rispetto a un Graph DB?*
**Risposta**: In un RDBMS modelliamo il grafo preventivamente in base ai traversal desiderati; un cambio di traversal richiede modifiche allo schema (nuove tabelle/FK). Nei Graph DB, la relazione non è calcolata ma **persistita** all'inserimento, permettendo l'aggiunta di nuovi tipi di archi senza alterare la struttura esistente.

---

## 3. Architetture Big Data in Pratica: Il Caso Facebook

### 3.1 Esercizio Guidato 3 - Selezione della Tecnologia
Associa la tecnologia corretta allo scenario d'uso basandoti sullo stack tecnologico di Facebook:
1.  **Scenario A**: Gestione di e-mail, messaggistica istantanea e SMS.
2.  **Scenario B**: Analisi di miliardi di connessioni tra utenti (trilioni di archi).
3.  **Scenario C**: Caching tra Web Server e database MySQL.

### 3.2 Soluzione con Motivazione Tecnica
*   **Scenario A -> HBase**: Un database column-family basato su Hadoop. Scelto da Facebook come rimpiazzo per MySQL e Cassandra per la gestione dei messaggi.
*   **Scenario B -> Apache Giraph**: Database a grafo ottimizzato per analisi massicce su grafi di grandi dimensioni (utilizzato dal 2013 per trilioni di archi).
*   **Scenario C -> Memcached**: Key-value store distribuito, essenziale per ridurre la latenza tra il layer web e i database MySQL.

**Nota su RocksDB**: Si consideri anche **RocksDB**, un key-value store ad alte prestazioni sviluppato internamente da Facebook e successivamente reso open-source.

### 3.3 Ecosistema Hadoop e Hive
*   **HDFS**: File system distribuito capace di gestire oltre 100 PB in un singolo cluster.
*   **MapReduce**: Framework per l'esecuzione di calcoli paralleli su moli massive di dati.
*   **Apache Hive**: Fondamentale per fornire un accesso **SQL-like** ai dati su HDFS, integrando la valutazione delle query con il motore MapReduce.

---

## 4. Redis: Strutture Dati e Persistenza

### 4.1 Esercizio Guidato 4 - Operazioni Atomiche
Analizzate i seguenti comandi e le loro funzioni specifiche secondo la documentazione Redis:
*   `GETSET key value`: Operazione atomica che restituisce il vecchio valore e imposta il nuovo (*Get old value, set new*).
*   `HSET key field value`: Imposta il valore di un campo specifico all'interno di una Hash (O(1)).
*   `SINTER key1 key2`: Calcola l'intersezione tra Set.

### 4.2 Ragionamento sulla Persistenza: RDB vs AOF
La scelta della strategia di persistenza è un delicato equilibrio tra performance e sicurezza del dato:
1.  **RDB (Background Save)**: Effettua un dump periodico dell'intero DB su disco. Utilizza `fork()` con **Copy-on-Write** per minimizzare l'impatto sul processo principale. Scatta dopo X secondi e Y cambiamenti (o tramite comando `BGSAVE`).
2.  **AOF (Append Only File)**: Logga ogni operazione di scrittura. Offre flessibilità tramite la pianificazione di `fsync()`:
    *   *Always*: Massima sicurezza, costo elevato.
    *   *Every second*: Bilanciamento ottimale (default).
    *   *Never*: Delega la gestione al sistema operativo.

### 4.3 Esercizio di Modellazione Redis (James e Chris)
**Obiettivo**: Modellare i dati per rispondere alla query: "Ottenere i prodotti acquistati da un utente".

**Logica di Modellazione**:
Utilizziamo un **Set** per mappare gli ordini appartenenti a un utente (garantendo unicità e velocità di accesso) e una **Hash** per i dettagli dell'ordine, poiché quest'ultima permette di memorizzare coppie campo-valore (ID Prodotto e Quantità).

**Comandi Redis CLI**:
```bash
# Mapping Utente -> Lista Ordini (Set)
SADD ords_james_ordID 1 3
SADD ords_chris_ordID 2

# Dettagli Ordine (Hash: campo "product_ID" -> valore "qty")
HSET order_1 user "james" product_28 1 product_372 2
HSET order_2 user "chris" product_15 1 product_160 5 product_201 7
```

---

## 5. Verifica Finale e Sintesi

### 5.1 Domande di Autovalutazione
1.  **Qual è il limite dell'atomicità nei DB NoSQL orientati agli aggregati?**
    *   È limitata al contesto di un singolo aggregato.
2.  **Qual è la differenza di modellazione tra Neo4j e InfiniteGraph?**
    *   Neo4j è *schemaless*; InfiniteGraph richiede che gli oggetti siano sottoclassi di tipi predefiniti.
3.  **In Redis AOF, quale opzione di fsync() garantisce il miglior compromesso tra durabilità e performance?**
    *   Every second.
4.  **A cosa serve RocksDB nello stack di Facebook?**
    *   È un key-value store interno ad alte prestazioni.
5.  **Perché i database a grafo sono preferibili per query su dati altamente connessi?**
    *   Perché spostano il carico computazionale all'**insert time**, rendendo i traversal estremamente economici rispetto ai Join relazionali.

### 5.2 Tabella di Verifica dei Comandi e Complessità
Si definisca $N$ come il numero di elementi nella struttura, $C$ come il numero di set confrontati e $M$ come il numero di elementi nel set più piccolo.

| Comando | Struttura Dati | Complessità | Descrizione |
| :--- | :--- | :--- | :--- |
| `HGET` / `HSET` | Hash | O(1) | Accesso/scrittura campo singolo |
| `HMGET` | Hash | O(N) | Recupero di più campi specificati |
| `SINTER` | Set | O(C * M) | Intersezione tra $C$ set |
| `ZADD` | Sorted Set | O(log N) | Inserimento elemento con score |
| `ZRANGE` | Sorted Set | O(log(N) + M) | Range di $M$ elementi per indice |

### 5.3 Mini-Riepilogo Finale
*   **Aggregati**: Unità atomiche che semplificano lo sharding distribuendo blocchi di dati integri.
*   **Grafi**: Ottimizzati per relazioni complesse tramite la persistenza degli archi (navigazione nativa).
*   **Stack Facebook**: Architettura eterogenea (HBase per messaging, Giraph per grafi, Memcached per latenza).
*   **Persistenza Redis**: Scelta tra snapshot (RDB) e logging incrementale (AOF).
*   **Modellazione Key-Value**: Richiede l'uso strategico di Hash (per record strutturati) e Set (per relazioni e membership).