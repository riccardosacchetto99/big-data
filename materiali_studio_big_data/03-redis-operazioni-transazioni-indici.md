# 3) Redis: Operazioni, Transazioni, Persistence e Indici

## 3.1 Panorama rapido
Redis è presentato come:
- in-memory data store
- event loop single-threaded
- estremamente veloce su pattern chiave/valore e strutture native

Il punto in esame non è memorizzare comandi a caso, ma spiegare **quando** usare ogni struttura.

## 3.2 Modello logico Redis
- Key: stringa (tipicamente ASCII stampabile)
- Value: tipo concreto (`string`, `hash`, `list`, `set`, `zset`, ecc.)

### Conseguenza pratica
Due key diverse possono rappresentare concetti molto diversi; la naming convention è cruciale.

## 3.3 Tipi dati e use case

### 3.3.1 String
Use case:
- contatori semplici
- flag
- payload piccoli serializzati

Comandi frequenti:
- `GET key`
- `SET key value`
- `EXISTS key`
- `DEL key`
- `SETNX key value`
- `GETSET key value`

Quando evitarlo:
- quando hai molti campi da aggiornare selettivamente (meglio hash).

### 3.3.2 Hash
Use case:
- oggetti con più attributi (utente, prodotto, ticket)

Comandi frequenti:
- `HSET key field value`
- `HGET key field`
- `HEXISTS key field`
- `HDEL key field`
- `HMGET key f1 f2 ...`
- `HKEYS key`, `HVALS key`

Pro:
- aggiornamento puntuale campo per campo.

Contro:
- attenzione a oggetti troppo grandi o accessi full-scan frequenti.

### 3.3.3 Set
Use case:
- membership senza ordine (tag, utenti attivi, id associati)

Comandi tipici:
- `SADD`, `SREM`, `SCARD`, `SMEMBERS`
- operazioni insiemistiche: `SDIFF`, `SUNION`

Pro:
- test di appartenenza e deduplicazione naturali.

### 3.3.4 Sorted Set (ZSet)
Use case:
- ranking
- indici secondari ordinati (es. anno nascita, score)

Comandi base:
- `ZADD key score member`
- `ZRANGE ...`
- query per punteggio/range (molto utile per indici secondari)

## 3.4 Complessità computazionale (valore da esame)
Nelle slide compaiono distinzioni O(1)/O(N). In risposta, cita sempre almeno un impatto pratico:

- O(1): ottimo per hot path ad alta frequenza.
- O(N): accettabile su cardinalità piccole, rischioso su dataset grandi.

Esempio da spendere:
- `HGET` O(1) va bene in loop frequente.
- `SMEMBERS` su set enorme può diventare costoso.

## 3.5 Persistence in Redis
### 3.5.1 Snapshotting (RDB / BGSAVE)
- dump periodico dell’intero DB su disco
- spesso via processo figlio (`fork`, copy-on-write)

Pro:
- recovery rapido da snapshot
- overhead generalmente contenuto tra dump

Contro:
- possibile perdita dati tra due snapshot

### 3.5.2 AOF (Append Only File)
- ogni write appendata su log
- politica `fsync` configurabile: sempre, ogni secondo, mai

Pro:
- maggiore durabilità configurabile

Contro:
- più overhead I/O rispetto a solo snapshot

### 3.5.3 Scelta pratica
- Se vuoi più performance e tolleri minima perdita: snapshot aggressivo.
- Se vuoi durabilità maggiore: AOF (spesso everysec).
- In produzione spesso combinazione delle due strategie.

## 3.6 Transazioni Redis (`MULTI/EXEC`)
Dalle lezioni:
- i comandi in transazione vengono serializzati/eseguiti in sequenza.
- blocco atomico: o esegue tutto o nulla (nel contesto del blocco).

Flusso:
1. `MULTI`
2. enqueue comandi
3. `EXEC`

Caso importante citato:
- se il client perde connessione prima di `EXEC`, le operazioni non vengono applicate.

### Limiti da ricordare
- Non è una transazione relazionale completa con isolamento sofisticato.
- Va progettata con attenzione in presenza di concorrenza e vincoli applicativi.

## 3.7 Indici secondari con Redis
Lezione 27/03: costruire strutture complementari.

### Esempio base (nomi per anno nascita)
- `ZADD birthyear:name 1986 Manuel`
- `ZADD birthyear:name 2003 Anna`
- `ZADD birthyear:name 1959 Jon`
- `ZADD birthyear:name 2001 Helen`

Query: nati dopo 2000 via range score.

### Pattern generale
- Primary access: key principale dell’entità
- Secondary index: set/zset per rispondere a query non coperte dalla key primaria

### Rischio
- disallineamento tra dato primario e indice se update non coordinati

Mitigazione:
- aggiornare sempre entità + indice nello stesso flusso transazionale/logico.

## 3.8 Caso completo: anagrafica persone
Requisiti:
- ricerca per id (puntuale)
- ricerca per città
- ricerca per anno nascita > X

Modello:
- `person:<id>` -> hash con dati base
- `idx:city:<city>` -> set di id
- `idx:birthyear` -> zset con score anno, member id

Write create persona:
1. `HSET person:<id> ...`
2. `SADD idx:city:<city> <id>`
3. `ZADD idx:birthyear <year> <id>`

Update città:
1. recupero old city
2. `SREM idx:city:<oldCity> <id>`
3. `SADD idx:city:<newCity> <id>`
4. update hash persona

## 3.9 Errori tipici su Redis
- Usare solo string per tutto (perdi semantica e operazioni native).
- Ignorare complessità asintotica dei comandi.
- Nessuna policy di expiration/TTL quando necessaria.
- Indici secondari non aggiornati in write path.
- Nessuna strategia persistence coerente col requisito di durabilità.

## 3.10 Esercizi pratici (stile orale/scritto)
### Esercizio 1
Progetta modello Redis per gestione prenotazioni visite mediche:
- lookup paziente
- indice per data visita
- indice per medico
- cancellazione prenotazione

### Esercizio 2
Spiega differenza pratica tra `SETNX` e `SET` con esempio lock semplice.

### Esercizio 3
Disegna flusso transazionale `MULTI/EXEC` per aggiornare saldo e log movimento (livello concettuale).

## 3.11 Soluzioni sintetiche
### Soluzione 1
- `visit:<id>` hash
- `idx:doctor:<doctorId>` set(visitId)
- `idx:visitDate` zset(score=timestamp, member=visitId)
- on delete: rimozione da hash e da entrambi gli indici

### Soluzione 2
- `SETNX lock:resource token` crea lock solo se assente
- `SET` sovrascrive sempre

### Soluzione 3
- `MULTI`
- update saldo
- append log
- `EXEC`
- in caso di failure pre-EXEC: nessuna modifica

## 3.12 Checklist pre-esame (capitolo 3)
- So scegliere tipo Redis corretto per caso d’uso.
- So citare almeno 2 comandi per tipo con complessità.
- So spiegare snapshot vs AOF con trade-off.
- So descrivere `MULTI/EXEC` e caso di disconnect.
- So costruire un indice secondario con zset e motivarlo.
