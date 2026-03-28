# 2) Modellazione Aggregate e Key-Value

## 2.1 Dalla teoria alla modellazione
Nelle lezioni di marzo il focus forte è: non basta conoscere i database key-value, bisogna **modellare bene le key e i valori** in funzione del workload.

Punto chiave:
- Una key-value store è semplice in interfaccia, ma la qualità della modellazione decide performance, costi e manutenibilità.

## 2.2 Atomic Aggregate
Concetto esplicito nelle slide.

**Atomic Aggregate** = pattern di modellazione che consente accesso read/write a più attributi con una singola operazione logica.

Esempio astratto:
- Buono: `ticket:9888 -> {data, location, seat}`
- Peggio (se sempre co-usati):
  - `ticket:9888:data -> ...`
  - `ticket:9888:location -> ...`
  - `ticket:9888:seat -> ...`

### Vantaggi
- Meno read separate.
- Update coerenti su più campi in un solo passaggio.
- Migliore locality del dato.

### Svantaggi
- Oggetti grandi (soprattutto se con campi variabili/annidati).
- Maggior costo quando aggiorni un solo campo spesso.
- Maggiore rischio di contention su entità molto calde.

## 2.3 Come decidere la granularità dell’aggregate
Domande pratiche:
- Questi campi sono letti insieme frequentemente?
- Questi campi cambiano insieme o indipendentemente?
- Il payload resta ragionevole per latenza e memoria?
- L’eventuale duplicazione è sostenibile?

Regola pragmatica:
- Se leggi insieme molto più spesso di quanto aggiorni separatamente, aggrega.
- Se aggiorni spesso campi indipendenti ad alta frequenza, valuta split.

## 2.4 Naming conventions per key
Dalle lezioni: key random “senza senso” sono un anti-pattern (salvo mapping esterno).

### Obiettivi naming
- Leggibilità codice.
- Estendibilità futura.
- Facilità di debugging e data governance.
- Supporto a pattern query (prefix/range dove applicabile).

### Pattern consigliato
`<dominio>:<entita>:<id>[:<sottochiave>]`

Esempi:
- `zoo:animal:4821`
- `zoo:species:tiger`
- `shop:order:2026-000345`
- `app:user:77:preferences`

### Anti-pattern comuni
- `a9x771` (nessun contesto)
- key con separatori incoerenti misti
- embedding di troppi concetti in una stringa non parsabile

## 2.5 Key design e partizionamento
La key spesso guida anche distribuzione/partitioning.

### Rischio: hotspot
Se la parte iniziale della key concentra traffico su pochi shard, il sistema degrada.

Esempio rischio:
- `event:2026-03-28:<id>` con picchi forti su data corrente.

Mitigazioni:
- prefisso hash/salt controllato
- composizione key che distribuisca meglio
- bucket temporali bilanciati

## 2.6 Structured values: approccio workload-first
Dalle slide: se nome e indirizzo cliente sono richiesti insieme spesso, conviene tenerli insieme.

Esempio 1 (approccio sparso):
- `cust:100:fname`
- `cust:100:lname`
- `cust:100:addr`
- `cust:100:city`

Esempio 2 (approccio aggregato):
- `cust:100 -> {fname,lname,addr,city,state,zip}`

Confronto:
- Approccio 1: più chiamate read, flessibilità su singolo campo.
- Approccio 2: meno chiamate read, payload più grande.

## 2.7 Relazioni tra aggregate
In aggregate-oriented DB, la relazione spesso è rappresentata da ID referenziati, non join nativi complessi.

Esempio:
- `order:5001` contiene `customerId=100`
- l’applicazione risolve l’utente con lookup separato.

Implicazioni:
- Più controllo applicativo.
- Possibile denormalizzazione selettiva per query frequenti.

## 2.8 Denormalizzazione consapevole
Non è “duplicare a caso”, ma duplicare ciò che serve per ridurre query costose.

### Quando conviene
- read-critical path ad alta frequenza
- dato sorgente relativamente stabile
- aggiornamenti gestibili con workflow chiaro

### Come farla bene
- definire source of truth
- definire trigger/eventi di aggiornamento
- introdurre versioning o timestamp di sincronizzazione

## 2.9 Caso studio guidato: Zoo (in stile tracce parziale)
Scenario (coerente con il test esempio):
- Uno zoo ospita animali, specie, classi biologiche, aree e staff.
- Serve consultazione rapida scheda animale e report periodici.

### Requisiti tipici
- Aprire scheda animale in O(1) per ID.
- Filtrare animali per specie.
- Filtrare animali per anno nascita.
- Visualizzare alimentazione e stato sanitario recente.

### Proposta modello
- `zoo:animal:<id> -> {name,species,birthYear,sex,enclosureId,feedingPlan,healthStatus}`
- `zoo:species:<speciesId> -> {name,class,diet,avgWeightRange}`
- `zoo:idx:species:<speciesId> -> set(animalId...)`
- `zoo:idx:birthyear -> zset(score=year, member=animalId)`

### Motivazione
- Scheda animale = aggregate unico.
- Query per specie = set dedicato.
- Query per anno/range = zset per ordinamento numerico.

## 2.10 Errori tipici nella modellazione (e come evitarli)
1. Modellare per entità teoriche e non per query reali.
2. Assumere join gratuiti come in SQL.
3. Ignorare evoluzione schema applicativo.
4. Usare key naming non versionabile.
5. Nessun piano per migrazione dati.

Contromisure:
- partire da 5 query principali di business
- mappare query -> struttura dati
- validare con test di carico minimo

## 2.11 Esercizi applicativi
### Esercizio 1
Piattaforma concerti:
- ticket con data, location, seat, price, status.
- query frequenti: scheda ticket, ticket per evento, ticket per stato.

Richiesto:
- definisci naming convention
- proponi aggregate
- proponi 2 indici secondari
- elenca trade-off principali

### Esercizio 2
E-commerce:
- carrello utente letto e scritto continuamente.

Richiesto:
- modellazione aggregate carrello
- gestione item count e totale
- strategia aggiornamento atomico

### Esercizio 3
Registro studenti:
- query per matricola, corso, media voto.

Richiesto:
- progettare chiavi principali
- indice per corso
- indice per range media

## 2.12 Soluzioni guida (struttura)
### Soluzione 1 (concerti)
- Key ticket: `concert:ticket:<id>`
- Aggregate: campi ticket in un valore unico
- Indici:
  - `concert:idx:event:<eventId>` (set ticketId)
  - `concert:idx:status:<status>` (set ticketId)
- Trade-off:
  - read rapide su scheda
  - maggiore coordinamento update quando cambia status

### Soluzione 2 (carrello)
- `shop:cart:<userId> -> {items:[...], total, itemCount, updatedAt}`
- Operazioni atomiche via transazione/script (dipende dal datastore)
- Validazione concorrenza su version/timestamp

### Soluzione 3 (studenti)
- `uni:student:<matricola>`
- `uni:idx:course:<courseId>` (set matricole)
- `uni:idx:gpa` (zset score=media, member=matricola)

## 2.13 Checklist pre-esame (capitolo 2)
- So definire atomic aggregate e citarne pro/contro.
- So progettare naming convention coerente e leggibile.
- So motivare split vs merge di campi.
- So progettare almeno 2 indici secondari diversi.
- So discutere hotspot e partizionamento in modo concreto.
