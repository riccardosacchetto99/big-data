# 4) Esercizi Guidati e Simulazioni Parziale (stile "Example of first partial test")

## 4.1 Struttura tipica del parziale (ripresa dal tuo esempio)
Formato utile da allenare:
- 3 domande teoriche brevi/medie
- 1 esercizio di modellazione più esteso

Nel tuo esempio compaiono:
- Atomic aggregate
- Pro/contro aggregate-oriented
- Building blocks document-oriented
- Esercizio di progettazione dominio (zoo)

Questo file replica quel formato con più varianti.

---

## Simulazione 1

### Question 1 (teoria)
Spiega il pattern di modellazione **atomic aggregate** e descrivi quando è particolarmente efficace in un datastore key-value.

### Solution 1 (schema risposta completa)
Atomic aggregate significa progettare una rappresentazione dati in cui attributi fortemente correlati, letti/scritti insieme, sono mantenuti nella stessa unità logica (es. un hash o un documento unico). È efficace quando il workload è read-heavy su bundle di campi correlati, perché riduce round-trip e semplifica accessi applicativi. I vantaggi principali sono locality, minori letture multiple e write coerenti su gruppo di campi. I limiti includono payload più grandi, possibili update costosi su singolo campo e rischio contention su aggregate molto “caldi”.

### Question 2 (teoria)
Elenca vantaggi e svantaggi dei modelli aggregate-oriented rispetto a un approccio relazionale classico con join.

### Solution 2
Vantaggi:
- accesso rapido a unità applicative complete
- ottima compatibilità con partizionamento/scalabilità orizzontale
- riduzione di join runtime

Svantaggi:
- denormalizzazione più frequente
- aggiornamenti cross-aggregate più difficili
- maggiore responsabilità lato applicazione per mantenere consistenza tra viste diverse

### Question 3 (teoria)
Quali sono i principali building block del modello document-oriented e in cosa differiscono dai record relazionali?

### Solution 3
Building block tipici:
- documento (JSON/BSON-like)
- campi e sotto-documenti annidati
- array
- identificatore univoco
- collezione di documenti

Differenze rispetto a record relazionale:
- schema più flessibile
- struttura gerarchica/annidata naturale
- minore dipendenza da join per comporre oggetti complessi

### Exercise 1 (modellazione)
La piattaforma di mobilità urbana di una grande città gestisce:
- veicoli condivisi (bike/scooter)
- utenti
- corse
- stazioni di parcheggio

Requisiti:
1. Caricare rapidamente scheda veicolo per ID.
2. Elencare i veicoli disponibili in una stazione.
3. Trovare veicoli con batteria sotto il 20%.
4. Tracciare cronologia corse utente.
5. Aggiornare stato veicolo a ogni fine corsa.

Richiesto:
- Proponi modello key-value/Redis con naming convention.
- Definisci aggregate principali.
- Definisci almeno due indici secondari.
- Spiega 3 trade-off progettuali.

### Exercise 1 - Soluzione guida
Naming:
- `mob:vehicle:<id>`
- `mob:user:<id>`
- `mob:ride:<id>`
- `mob:station:<id>`

Aggregate principali:
- `mob:vehicle:<id>` (hash): tipo, stationId, batteryPct, status, lastUpdate
- `mob:user:<id>` (hash): profilo essenziale + crediti
- `mob:ride:<id>` (hash): userId, vehicleId, startTs, endTs, cost

Indici:
- `mob:idx:station:<stationId>` (set vehicleId disponibili)
- `mob:idx:battery` (zset score=batteryPct, member=vehicleId)
- opzionale: `mob:idx:userRides:<userId>` (list rideId o zset con timestamp)

Trade-off:
1. Tenere info stato veicolo aggregate accelera read ma aumenta lavoro update in tempo reale.
2. Indice batteria su zset abilita range query ma richiede manutenzione ad ogni variazione.
3. Cronologia corse denormalizzata per utente migliora UX ma richiede coerenza tra ride primaria e indice utente.

---

## Simulazione 2

### Question 1
Descrivi come il key design influenza partizionamento e performance in un datastore distribuito.

### Solution 1
Il key design influenza direttamente la distribuzione del carico: chiavi poco bilanciate possono creare hotspot. Una convenzione con componenti ben distribuite (o hashing/salting controllato) riduce concentrazione su pochi nodi, migliora throughput e stabilizza latenza. Key semanticamente chiare aiutano manutenzione e debug.

### Question 2
Differenza tra consistenza forte ed eventual consistency in termini pratici applicativi.

### Solution 2
Con consistenza forte, dopo una write confermata ogni read successiva vede il dato aggiornato. Con eventual consistency, repliche diverse possono temporaneamente divergere, ma convergono nel tempo. Applicativamente, strong consistency semplifica logica critica; eventual consistency migliora disponibilità e scala in scenari ad alto throughput.

### Question 3
A cosa servono gli indici secondari in Redis e come si implementano in modo semplice?

### Solution 3
Servono a rispondere in modo efficiente a query non coperte dalla key primaria (es. filtro per anno, ranking, città). Si implementano con strutture dedicate (set/zset) che mappano attributi verso ID entità. Devono essere aggiornati in modo coordinato con il dato primario per evitare disallineamenti.

### Exercise 2
Sistema universitario:
- studenti
- corsi
- iscrizioni
- esami

Query frequenti:
1. Scheda studente per matricola.
2. Studenti iscritti a un corso.
3. Studenti con media > 27.
4. Ultimi esami sostenuti da uno studente.

Progetta:
- key naming
- aggregate
- 2 indici set/zset
- flusso aggiornamento voto con coerenza indici

### Exercise 2 - Soluzione guida
Key:
- `uni:student:<matricola>`
- `uni:course:<courseId>`
- `uni:exam:<examId>`

Aggregate:
- studente in hash con dati anagrafici e indicatori sintetici (media, cfu)

Indici:
- `uni:idx:course:<courseId>` -> set(matricole)
- `uni:idx:gpa` -> zset(score=media, member=matricola)
- storico esami per studente -> `uni:idx:exams:<matricola>` zset(score=timestamp, member=examId)

Update voto (schema):
1. scrivi record esame
2. aggiorna storico esami studente
3. ricalcola media studente
4. aggiorna hash studente
5. aggiorna zset GPA

---

## Simulazione 3 (full, livello alto)

### Question 1
Confronta modello aggregate-oriented e graph-based per un social network professionale.

### Soluzione 1
Aggregate-oriented è efficace per profili utente, feed personali e preferenze dove letture aggregate sono dominanti. Graph-based eccelle quando la query principale riguarda traversals multi-hop (connessioni, suggerimenti, shortest path sociale). In pratica, profilo e sessione possono stare in KV/document, mentre recommendation network può richiedere motore grafo.

### Question 2
Spiega persistenza Redis: snapshot e AOF, con criterio di scelta per piattaforma ticketing eventi.

### Soluzione 2
Snapshot (RDB) offre dump periodici efficienti ma può perdere dati recenti tra snapshot. AOF registra write sequenziali e riduce perdita dati, con overhead I/O maggiore. In ticketing eventi, per prenotazioni critiche conviene AOF (tipicamente everysec) e snapshot come complemento per recovery veloce.

### Question 3
Descrivi flusso `MULTI/EXEC` e un caso in cui non basta da solo.

### Soluzione 3
`MULTI` apre blocco transazionale, i comandi vengono accodati e `EXEC` li applica in sequenza atomica. Non basta da solo quando serve validazione condizionale complessa su stato concorrente senza meccanismi aggiuntivi (watch/versioning/logica applicativa).

### Exercise 3
Marketplace freelance:
- profili professionisti
- skill
- progetti
- candidature

Query:
1. Cerca professionisti per skill.
2. Ordina professionisti per rating.
3. Elenca candidature recenti per progetto.
4. Apri scheda completa professionista in una read.

Progetta modello Redis e spiega:
- aggregate principali
- indici secondari
- gestione aggiornamento rating
- possibili inconsistenze e mitigazioni

### Exercise 3 - Soluzione guida
Aggregate:
- `mk:pro:<id>` hash con campi principali
- `mk:project:<id>` hash
- `mk:application:<id>` hash

Indici:
- `mk:idx:skill:<skill>` set(proId)
- `mk:idx:rating` zset(score=rating, member=proId)
- `mk:idx:projectApps:<projectId>` zset(score=timestamp, member=applicationId)

Update rating:
1. update hash professionista
2. update zset rating
3. eventuale update cache risultati ricerca

Inconsistenze possibili:
- hash aggiornato ma zset no (o viceversa)
Mitigazioni:
- write path unico transazionale/logico
- job periodico di riconciliazione
- idempotenza update eventi

---

## 4.2 Banco prova rapido (30 minuti)
Esegui questa routine prima dell’esame:
1. Rispondi senza appunti a 3 domande teoriche (max 8 righe ciascuna).
2. Modella un dominio nuovo in 15 minuti (key, aggregate, indici).
3. Fai autovalutazione con rubrica:
- Chiarezza concetti (0-10)
- Concretezza esempi (0-10)
- Correttezza trade-off (0-10)
- Completezza soluzione esercizio (0-10)

Soglia consigliata: almeno 30/40.

## 4.3 Prompt di allenamento orale
- “Definisci atomic aggregate e dimmi un caso in cui NON lo useresti.”
- “Fammi un esempio di key naming sbagliato e rifallo bene.”
- “Costruisci un indice secondario in Redis per età cliente.”
- “Confronta snapshot e AOF per un sistema ordini online.”

## 4.4 Checklist finale pre-parziale
- So parlare 2 minuti continui su aggregate-oriented.
- So costruire un modello key-value completo da zero.
- So proporre almeno un indice set e uno zset con motivazione.
- So spiegare almeno un trade-off di consistenza.
- So risolvere esercizio stile prova in tempo limitato.
