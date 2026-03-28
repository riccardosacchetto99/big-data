# Guida Completa a Redis: Architettura, Modellazione e Persistenza

## 1. Introduzione ai Modelli NoSQL e all'Orientamento agli Aggregati

### 1.1 Modello dei Dati vs Modello di Memorizzazione
Nel panorama dei sistemi di gestione delle basi di dati, è fondamentale operare una distinzione netta tra il **modello dei dati** e il **modello di memorizzazione**. Il primo rappresenta il modello attraverso il quale l'utente percepisce e manipola le informazioni (la struttura logica), mentre il secondo riguarda le modalità con cui il sistema organizza fisicamente i dati sul supporto persistente. I sistemi NoSQL nascono per ottimizzare la manipolazione di strutture dati complesse che spesso non trovano una mappatura efficiente nel rigido schema tabellare dei database relazionali (RDBMS).

### 1.2 Il Concetto di Aggregato
Citando esplicitamente il lavoro di **Sadalage & Fowler (2012)** in "NoSQL Distilled", un **Aggregato** è definito come una collezione di oggetti correlati che vengono trattati come un'unità atomica ai fini della manipolazione dei dati, dell'analisi e della gestione della consistenza. Mentre un RDBMS opera su tuple, le applicazioni moderne necessitano di operare su unità strutturalmente complesse (array, record nidificati). 
L'orientamento agli aggregati offre vantaggi determinanti:
*   **Per i programmatori:** Semplifica l'interazione con il database, poiché i dati sono recuperati in unità che riflettono direttamente le classi o gli oggetti dell'applicazione.
*   **Per i sistemi distribuiti:** Facilita l'esecuzione su **cluster**. Poiché i dati appartenenti allo stesso aggregato vengono solitamente manipolati insieme, essi possono essere fisicamente co-locati sullo stesso nodo, minimizzando la latenza di rete e semplificando il partizionamento.

### 1.3 Gerarchia NoSQL: Size vs Complexity
I database NoSQL possono essere mappati in una gerarchia basata sul trade-off tra dimensioni dei dati (**Size**) e complessità delle relazioni (**Complexity**):
*   **Key-Value Stores (es. Redis):** Si posizionano nel punto di massima capacità di scalabilità (Size) e minima complessità. Sono ottimizzati per l'accesso tramite chiave primaria.
*   **Column-Family Stores (es. BigTable, Cassandra):** Gestiscono grandi volumi di dati con una struttura basata su famiglie di colonne accessibili tramite righe.
*   **Document Databases (es. MongoDB):** Offrono una maggiore complessità visibile al database, permettendo query sui campi interni dei documenti.
*   **Graph Databases (es. Neo4j):** Gestiscono la massima complessità nelle relazioni tra i dati, ma con una scalabilità dimensionale tipicamente inferiore rispetto ai Key-Value store puri.

## 2. Fondamenti di Redis (REmote DIctionary Server)

### 2.1 Architettura e Filosofia
Redis è un database in memoria principale (**main-memory database**) progettato per fornire prestazioni eccezionali. La sua architettura è basata su un **single-threaded event loop**, il che garantisce l'atomicità di ogni singola operazione senza l'onere computazionale dei lock multi-thread, processando le richieste in modo sequenziale ed estremamente rapido.

### 2.2 Il Modello Logico
Il sistema organizza i dati in coppie **<chiave, valore>**:
*   **Chiavi:** Devono essere composte da caratteri **Printable ASCII**. La loro corretta progettazione è vitale per l'efficienza e la manutenibilità del sistema.
*   **Valori:** Possono essere **Primitivi** (Strings) o **Contenitori** di stringhe (Hashes, Lists, Sets, Sorted Sets).

## 3. Tipi di Dati, Operatori e Complessità Computazionale

Di seguito sono analizzati i tipi di dati fondamentali supportati da Redis, corredati dai relativi operatori e dalla complessità asintotica per garantire il rigore accademico necessario alla progettazione di sistemi scalabili.

### 3.1 Strings
Rappresentano il tipo base di Redis. Una stringa può contenere qualsiasi dato (anche binario) fino a un limite massimo di **512MB**.

| Comando | Descrizione | Complessità |
| :--- | :--- | :--- |
| GET | Recupera il valore associato alla chiave | O(1) |
| SET | Imposta il valore per una chiave | O(1) |
| EXISTS | Verifica la presenza di una chiave | O(1) |
| DEL | Rimuove una chiave e il suo valore | O(1) |
| SETNX | Imposta il valore solo se la chiave non esiste (Set if Not Exists) | O(1) |
| GETSET | Imposta un nuovo valore e restituisce quello precedente | O(1) |

### 3.2 Hashes
Mappe tra campi e valori, ideali per rappresentare oggetti o aggregati le cui proprietà devono essere accessibili singolarmente.

| Comando | Descrizione | Complessità |
| :--- | :--- | :--- |
| HGET | Ottiene il valore di un singolo campo | O(1) |
| HSET | Imposta il valore di un campo | O(1) |
| HEXISTS | Verifica se un campo esiste nell'hash | O(1) |
| HDEL | Elimina uno o più campi | O(1) |
| HMGET | Ottiene i valori di una lista di campi | O(N) con N=num campi |
| HKEYS | Restituisce tutti i nomi dei campi | O(N) con N=num campi totali |
| HVALS | Restituisce tutti i valori dell'hash | O(N) con N=num campi totali |

### 3.3 Lists
Implementate come **liste doppiamente concatenate**, permettono operazioni efficienti sia in testa (**Head**) che in coda (**Tail**).

| Comando | Descrizione | Complessità |
| :--- | :--- | :--- |
| LPUSH | Inserisce un elemento in testa alla lista | O(1) |
| RPUSH | Inserisce un elemento in coda alla lista | O(1) |
| LPOP | Rimuove e restituisce l'elemento in testa | O(1) |
| RPOP | Rimuove e restituisce l'elemento in coda | O(1) |
| LLEN | Restituisce la lunghezza della lista | O(1) |
| LRANGE | Restituisce un intervallo di elementi | O(S+N) con S=offset, N=num elementi |

### 3.4 Sets
Collezioni non ordinate di stringhe uniche. Ideali per gestire relazioni di appartenenza senza duplicati.

| Comando | Descrizione | Complessità |
| :--- | :--- | :--- |
| SADD | Aggiunge un membro al set | O(1) |
| SREM | Rimuove un membro dal set | O(1) |
| SISMEMBER | Verifica l'appartenenza di un membro | O(1) |
| SMEMBERS | Restituisce tutti i membri del set | O(N) con N=cardinalità |
| SUNION | Calcola l'unione tra più set | O(N) con N=num elementi totali |

### 3.5 Sorted Sets
Simili ai Sets, ma ogni elemento è associato a un valore numerico detto **Score**. Il sistema mantiene gli elementi ordinati in base allo Score.

| Comando | Descrizione | Complessità |
| :--- | :--- | :--- |
| ZADD | Aggiunge un membro con il relativo score | O(log(N)) |
| ZRANGE | Restituisce elementi in un intervallo di ranking | O(log(N)+M) con M=num elementi |
| ZSCORE | Restituisce lo score di un membro | O(1) |
| ZREM | Rimuove un membro dal sorted set | O(log(N)) |

## 4. Strategie di Design delle Chiavi e Modellazione

### 4.1 Convenzione di Denominazione
L'uso di chiavi casuali è un grave anti-pattern. Le chiavi devono seguire una struttura logica che renda il codice leggibile, estensibile e garantisca l'efficienza di memorizzazione.

### 4.2 Anatomia di una Chiave Ideale
Secondo le best practice, una chiave dovrebbe essere composta da quattro elementi concatenati:
1.  **Prefisso Entità:** Un identificatore di **3-4 lettere** (es. 'cust' per customer, 'inv' per inventory). Questa brevità garantisce efficienza di storage.
2.  **Delimitatore:** Un carattere speciale, tipicamente il due punti (**:**), per separare i componenti.
3.  **Identificatore Unico (ID):** Il valore della chiave primaria dell'istanza dell'entità (es. 198277).
4.  **Nome Attributo:** Specifica quale proprietà dell'oggetto la chiave rappresenta (es. 'fname').

Esempio completo: **cust:198277:fname**

### 4.3 Partizionamento degli Oggetti
Invece di salvare un intero aggregato come un unico blob opaco, è vantaggioso partizionare l'oggetto nei suoi attributi costituenti. Ciò permette di modificare o recuperare una singola proprietà senza caricare l'intero oggetto. Un approccio comune consiste nell'implementare una funzione di astrazione come **setCustAttr(p_id, p_attrName, p_value)** che costruisce dinamicamente la chiave corretta per l'aggiornamento.

## 5. Persistenza dei Dati: Snapshotting e AOF

Essendo Redis un database in RAM, la persistenza è fondamentale per prevenire la perdita di dati in caso di crash.

### 5.1 Periodic Dump (Background Save)
Il meccanismo crea un'istantanea dell'intero dataset. Utilizza la chiamata di sistema **fork()** per creare un processo figlio. Grazie alla tecnica **Copy-on-Write** del sistema operativo, il processo figlio condivide la memoria col padre e scrive il dump su disco senza bloccare le operazioni di scrittura correnti.
*   **Comando:** `BGSAVE`.
*   **Trigger:** Avviene automaticamente dopo un certo numero di secondi o un numero minimo di cambiamenti.

### 5.2 Append Only File (AOF)
Registra ogni operazione di scrittura in un file di log sequenziale. Offre una protezione maggiore rispetto al dump periodico. La sincronizzazione su disco avviene tramite la funzione **fsync()**, configurabile con tre opzioni:
*   **Always:** Massima sicurezza, impatto elevato sulle performance.
*   **Every second:** Il **default consigliato**. Bilancia ottima protezione e alte prestazioni.
*   **Never:** Delega al sistema operativo la gestione del buffer, massima velocità ma rischio perdita dati.

### 5.3 Tabella Comparativa Strategie di Persistenza

| Caratteristica | Snapshotting (RDB) | Append Only File (AOF) |
| :--- | :--- | :--- |
| **Metodologia** | Intero dataset salvato periodicamente | Log incrementale di ogni scrittura |
| **Punto di Forza** | Ripristino veloce di grandi dataset | Massima granularità nel recupero dati |
| **Impatto I/O** | Basso (concentrato nel tempo) | Costante (scrive a ogni operazione) |
| **Affidabilità** | Possibile perdita dati dall'ultimo dump | Perdita massima di 1 secondo (default fsync) |

## 6. Transazioni e Controllo della Concorrenza

### 6.1 Transazioni MULTI/EXEC
Redis implementa transazioni semplificate. Con il comando **MULTI** si apre la transazione; i comandi successivi vengono messi in coda e non eseguiti immediatamente. Il comando **EXEC** scatena l'esecuzione atomica e sequenziale di tutta la coda.

### 6.2 Gestione dei Conflitti Distribuiti
Per gestire la concorrenza in scenari distribuiti (come nei modelli Dynamo o Riak citati nel contesto), Redis e i sistemi Key-Value simili utilizzano tecniche di versionamento. Tra queste spiccano gli **Stamps** (marche temporali) e i **Vector Clocks**. I Vector Clocks, in particolare, permettono di rilevare conflitti tra versioni divergenti dello stesso dato in un sistema senza un clock globale sincronizzato.

## 7. Indici Secondari e Scenari Reali

### 7.1 Implementazione di Indici
Per effettuare query su attributi non facenti parte della chiave primaria, si costruiscono indici secondari manuali. Ad esempio, per trovare tutti gli utenti residenti a Chicago, si crea un **Set** con chiave **idx:city:chicago** che contiene gli ID degli utenti corrispondenti. Questi set fungono da puntatori ai dati reali.

### 7.2 Scenario UML: Order Management
Considerando il diagramma UML fornito, possiamo modellare un aggregato complesso in Redis.
*   **Aggregato Customer:** Hash con prefisso 'cust' contenente il nome.
*   **Aggregato Order:** Un'istanza di ordine che incapsula diverse entità correlate:
    *   **OrderPayment:** memorizzato come parte dell'aggregato con attributi specifici come **cardNumber** e **txnId**.
    *   **OrderItem:** lista di elementi, ciascuno con il proprio **price**.
    *   **Shipping Address:** memorizzato con i campi dettagliati **street**, **city**, **state** e **post code**.
In Redis, l'aggregato 'Order' può essere modellato come un Hash complesso o una stringa JSON, dove l'accesso avviene tramite lookup della chiave primaria (es. order:99), restituendo istantaneamente tutte le informazioni sul pagamento e sulla spedizione senza join costose.

## 8. Anti-pattern, Troubleshooting e Best Practices

*   **Anti-pattern: Nomi casuali.** Chiavi come 'x123' rendono impossibile il debugging. Usare sempre prefissi di 3-4 lettere.
*   **Troubleshooting: Perdita di dati.** In caso di arresto anomalo, verificare se è attivo l'AOF. Se si usa solo RDB, i dati inseriti dopo l'ultimo snapshot sono irrecuperabili.
*   **Efficienza RAM:** Poiché Redis risiede interamente in memoria, è cruciale usare nomi di campi brevi negli Hash e preferire strutture dati efficienti per minimizzare l'occupazione di byte per record.

## 9. Esercitazione per Esame Universitario

### 9.1 Esercizi Tecnici

1. Modellare tramite Hash l'utente con ID 10 e nome "Luigi".
2. Calcolare la complessità di una HMGET su un Hash con 500 campi, se ne richiediamo solo 5.
3. Qual è il limite massimo di dimensione per un valore di tipo String?
4. Come si implementa una coda FIFO (First-In, First-Out) usando le liste?
5. Descrivere l'effetto del comando SETNX.
6. Spiegare perché il prefisso delle chiavi dovrebbe essere di 3-4 lettere.
7. Quale comando si usa per verificare l'esistenza di un campo in un Hash?
8. Quale strategia di persistenza è preferibile per minimizzare la perdita di dati?
9. Qual è la complessità dell'operazione HGETALL e perché va usata con cautela?
10. In una transazione MULTI/EXEC, quando vengono eseguiti effettivamente i comandi?
11. Come si può modellare una classifica (leaderboard) in tempo reale?
12. Cos'è la tecnica Copy-on-Write nel contesto del BGSAVE?
13. Creare un indice secondario per la categoria "Libri".
14. Cosa sono i Vector Clocks?
15. Come si rimuovono tutti i dati da una specifica chiave?

### 9.2 Soluzioni Commentate

1. HSET cust:10 name "Luigi". (L'uso del prefisso 'cust' e dell'ID 10 segue la convenzione di design).
2. O(N), dove N è il numero di campi richiesti (in questo caso 5).
3. 512 MB.
4. Si usa LPUSH per inserire in testa e RPOP per prelevare dalla coda (o viceversa).
5. Imposta la chiave solo se non è già presente nel database, garantendo che non avvengano sovrascritture accidentali.
6. Per ottimizzare l'efficienza di memorizzazione (storage efficiency), riducendo l'overhead dei metadati in RAM.
7. HEXISTS nome_chiave nome_campo.
8. Append Only File (AOF) con opzione fsync impostata su "Always" o "Every second".
9. O(N), dove N è il numero totale di campi dell'hash. Su hash molto grandi può bloccare il server essendo Redis single-threaded.
10. Solo dopo l'invio del comando EXEC; fino a quel momento rimangono in coda.
11. Utilizzando un Sorted Set (ZADD) dove lo Score rappresenta il punteggio del giocatore.
12. È una tecnica che permette al processo figlio di condividere le pagine di memoria del padre, duplicandole solo se il padre tenta di modificarle durante il salvataggio.
13. SADD idx:cat:libri id_prodotto_1 id_prodotto_2. (Si usa un Set che contiene i puntatori/ID agli oggetti reali).
14. Meccanismi di versionamento usati in sistemi distribuiti per rilevare conflitti tra aggiornamenti concorrenti.
15. Si utilizza il comando DEL seguito dal nome della chiave. (Complessità O(1)).