# Capitolo 7 - Errori frequenti e ripasso

## 1. Analisi Critica: Il Concetto di Aggregato e i suoi Confini

In ambito NoSQL, il concetto di **aggregato** non è meramente una modalità di raggruppamento dati, ma rappresenta il pilastro fondamentale su cui poggiano la scalabilità e la consistenza dei sistemi distribuiti. Definiamo l'aggregato come una collezione di dati correlati che trattiamo come un'unità atomica di interazione.

### Caratteristiche e Vantaggi Architetturali
L'efficienza di un database orientato agli aggregati è massima quando l'interazione avviene entro i confini dello stesso aggregato. I vantaggi principali includono:
*   **Confine di Atomicità (ACID):** L'aggregato definisce l'ambito entro il quale il database garantisce le proprietà ACID. Operazioni che coinvolgono un singolo aggregato sono intrinsecamente sicure.
*   **Ottimizzazione della Distribuzione su Cluster:** La gestione dello storage su cluster risulta semplificata poiché l'aggregato funge da unità di partizionamento; il sistema può distribuire gli aggregati su nodi diversi mantenendo i dati correlati fisicamente vicini.
*   **Riduzione dell'Impedance Mismatch:** Modellando i dati secondo le necessità dell'applicazione (es. un documento JSON), si riduce la frizione tra il modello a oggetti del codice e la persistenza.

### Errore Progettuale: Il Rischio dei "Large Aggregates"
Un errore frequente consiste nell'ignorare i confini dell'aggregato o, paradossalmente, nel creare aggregati eccessivamente vasti. Sebbene l'aggregato faciliti la coerenza, un aggregato troppo grande introduce **colli di bottiglia prestazionali** (contention) e degrada la velocità di accesso, poiché il database deve caricare e bloccare l'intera unità anche per modifiche minime. È essenziale trovare il giusto equilibrio per evitare che la granularità dei dati diventi un ostacolo alla concorrenza.

---

## 2. Gestione delle Relazioni: NoSQL vs RDBMS

La transizione dal modello relazionale a quello NoSQL impone un cambio di paradigma radicale nella gestione dei vincoli di integrità e delle interconnessioni tra entità.

| Caratteristica | RDBMS (Foreign Keys) | NoSQL Aggregate-Oriented |
| :--- | :--- | :--- |
| **Meccanismo di Relazione** | Chiavi esterne (Foreign Keys) vincolanti. | ID di un aggregato referenziato in un altro. |
| **Responsabilità del Join** | Eseguito dal motore DB (Query time). | Implementato dal programmatore (Application-level). |
| **Consapevolezza del DB** | Il database valida e conosce la relazione. | **Database Ignorance**: il DB è ignaro del legame. |
| **Garanzie di Integrità** | Transazioni ACID multi-riga native. | Onere del programmatore (Integrità applicativa). |

### Il Concetto di "Database Ignorance"
Nel modello NoSQL, il database non ha consapevolezza semantica della relazione. Se un documento "Ordine" contiene un `customerId`, per il database si tratta di un semplice valore scalare. Questa ignoranza sposta la responsabilità della **coerenza referenziale** interamente sulla logica applicativa: spetta al programmatore assicurarsi, ad esempio, che la cancellazione di un cliente non lasci "ordini orfani" nel sistema.

> **Domanda Trabocchetto:** "Chi è responsabile dell'atomicità durante l'aggiornamento di più aggregati contemporaneamente?"
> **Risposta:** Mentre negli RDBMS il motore transazionale gestisce l'atomicità su più righe, nei sistemi NoSQL la responsabilità ricade sul **programmatore**. L'atomicità è garantita solo a livello di singolo aggregato; le modifiche cross-aggregato richiedono pattern applicativi complessi (come le *Saga* o il *Two-Phase Commit* applicativo).

---

## 3. Graph Databases: Oltre il Modello Relazionale

I database a grafo emergono come risposta paradigmatica ai limiti strutturali del modello relazionale nella gestione di relazioni ad alta densità. Quando i "Join" diventano eccessivamente onerosi, il modello a grafo offre una soluzione nativa.

### Missione e Modellazione
L'obiettivo è rappresentare entità e relazioni con pari dignità computazionale:
*   **Nodi:** Istanze di oggetti dotate di proprietà (es. Nome, Età).
*   **Archi (Edges):** Relazioni con **significatività direzionale** e tipizzazione specifica (es. "likes", "friend", "works_at").

### Efficienza Computazionale: Insert time vs Query time
Negli RDBMS, il costo della navigazione tra relazioni è pagato al "Query time" (Join costosi). I database a grafo spostano questo lavoro all'**"Insert time"**: la relazione non viene calcolata dinamicamente tramite indici, ma viene **persistita** fisicamente. Questo rende il "traversal" (l'esplorazione del grafo) estremamente economico, rendendo i sistemi a grafo ideali per dati altamente interconnessi.

**Esempio Didattico:** Si consideri la query *"Trova i dipendenti di 'BigCo' a cui piace il libro 'NoSQL Distilled'"*. In un database a grafo come **Neo4J** (schemaless, basato su oggetti Java), **OrientDB** o **NebulaGraph**, questo traversal richiede pochi millisecondi partendo da un **anchor node** (punto di ingresso indicizzato, come l'ID di 'BigCo') e seguendo gli archi "employee" e poi "likes".

---

## 4. Redis: Deep Dive Tecnico e Complessità

Redis (*REmote DIctionary Server*) non è un semplice key-value store, ma un server di strutture dati avanzate basato su un'architettura a **single-threaded event loop**.

### Architettura e Persistenza
L'essere single-threaded implica che ogni comando è atomico, ma anche che operazioni con complessità $O(N)$ possono bloccare l'intero server per la durata dell'esecuzione.
1.  **Periodic Dump (RDB):** Innescato dal comando `BGSAVE` o automaticamente dopo $X$ secondi e $Y$ modifiche. Utilizza il `fork()` del sistema operativo con meccanismo *Copy-on-Write* per scrivere il dump su disco senza bloccare il processo principale.
2.  **Append Only File (AOF):** Logga ogni operazione di scrittura. Offre durabilità configurabile tramite la frequenza di `fsync()` (sempre, ogni secondo, o mai).

### Analisi della Complessità e Modelli Dati
Le chiavi sono stringhe ASCII; i valori possono essere stringhe semplici (fino a **512MB**) o contenitori (Hashes, Lists, Sets, Sorted Sets).

| Struttura | Comando | Complessità | Nota Didattica |
| :--- | :--- | :--- | :--- |
| **String** | `GETSET` | **O(1)** | Restituisce il vecchio valore e imposta il nuovo. |
| **Hash** | `HSET`, `HGET` | **O(1)** | Accesso diretto al campo. |
| **Hash** | `HMGET`, `HKEYS` | **O(N)** | $N$ è il numero di campi richiesti o presenti. |
| **Set** | `SMEMBERS` | **O(N)** | $N$ è la cardinalità del set. |
| **Set** | `SINTER` | **O(C*M)** | $C$ = numero di set; $M$ = numero di membri. |
| **Sorted Set** | `ZCARD` | **O(1)** | Restituisce la cardinalità del set ordinato. |
| **Sorted Set** | `ZADD`, `ZRANK` | **O(log(N))** | Basato su skip-list per mantenere l'ordinamento. |
| **Sorted Set** | `ZRANGE` | **O(log(N)+M)** | $M$ è il numero di elementi nel range. |

---

## 5. Case Study: L'Ecosistema di "Persistenza Poliglotta" di Facebook

Facebook rappresenta il paradigma della *Polyglot Persistence*, dove ogni tecnologia è scelta per risolvere un problema specifico.

*   **Apache Hadoop/HDFS:** Gestione di storage distribuito massivo (cluster > 100 PB) per analisi offline tramite MapReduce.
*   **Apache Hive:** Layer per l'accesso SQL-like ai dati su Hadoop, trasformando query in job MapReduce.
*   **Apache HBase:** Database column-family costruito su Hadoop. È il cuore del sistema di messaggistica (email, SMS, chat), avendo sostituito MySQL e Cassandra per questo caso d'uso.
*   **Memcached:** Fondamentale per la scalabilità, funge da cache distribuita tra il layer web e i DB MySQL.
*   **Apache Giraph (Retired):** Utilizzato storicamente per l'analisi del social graph (trilioni di archi). Nonostante sia oggi in disuso a favore di soluzioni interne, ha segnato un'epoca nell'analisi dei grafi massivi.
*   **RocksDB:** Key-value store *embedded* ad altissime prestazioni, ottimizzato per storage SSD, sviluppato internamente e ora standard open-source.

---

## 6. Esercitazione Pratica: Modellazione in Redis

**Scenario:** Modellare un sistema che consenta di recuperare rapidamente i prodotti acquistati da un utente specifico (es. James).

### Logica di Modellazione
Per ottimizzare la query, utilizziamo un **SET** come indice invertito per raggruppare gli ID degli ordini di un utente, e una serie di **HASH** per memorizzare i dettagli dell'ordine.

**1. Definizione dell'indice per utente (Set):**
```redis
# James ha effettuato gli ordini 1 e 3
SADD ords_james_ordID 1 3
# Chris ha effettuato l'ordine 2
SADD ords_chris_ordID 2
```

**2. Definizione dei dettagli dell'ordine (Hash):**
```redis
# Ordine 1: dettagli e prodotti
HSET order_1 user "james" product_28 1 product_372 2
# Ordine 2: dettagli e prodotti
HSET order_2 user "chris" product_15 1 product_160 5 product_201 7
```

---

## 7. Anti-pattern e Autovalutazione

### Anti-pattern: "Relational-only mindset"
Un errore comune è forzare traversal complessi (es. gerarchie organizzative multi-livello) in un RDBMS. In un contesto relazionale, ogni nuova relazione o variazione nel modo di navigare i dati richiede pesanti cambi di schema. Nei database a grafo, la struttura è fluida: la relazione è il dato stesso, permettendo evoluzioni dello schema senza attriti.

### Checklist di Autovalutazione
1.  **Qual è la differenza tra RDB e AOF in Redis?** *RDB è uno snapshot del dataset in un momento preciso; AOF è un log append-only di ogni operazione di scrittura.*
2.  **In un database a grafo, cosa si intende per "anchor node"?** *È il nodo di partenza, solitamente indicizzato, da cui inizia la navigazione del grafo.*
3.  **Perché gli aggiornamenti multi-aggregato sono critici?** *Perché il DB NoSQL non offre transazioni ACID oltre il confine dell'aggregato; la coerenza deve essere garantita a livello applicativo.*

**Sintesi Finale:** La scelta del modello (Aggregate, Graph o Key-Value) deve essere guidata dalla natura del dato e dalle query: gli aggregati ottimizzano la località e la scalabilità su cluster, i grafi ottimizzano le interconnessioni spostando il lavoro al momento dell'inserimento.

---

## 8. Appendice: Amministrazione Redis tramite Docker

Per scopi didattici e di sviluppo, Docker rappresenta lo standard per il deployment di Redis.

```bash
# Avvia i servizi definiti nel docker-compose.yml in modalità distaccata (-d)
docker compose up -d

# Esegue il client interattivo redis-cli all'interno del container. 
# Il flag '-it' (interactive terminal) è fondamentale per interagire con il prompt.
docker exec -it redis-redis-1 redis-cli

# Arresta i container senza rimuovere le immagini
docker compose stop

# Riavvia i container precedentemente fermati
docker compose start
```