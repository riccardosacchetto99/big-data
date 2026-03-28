# 1) Fondamenti Big Data e NoSQL

## 1.1 Big Data: definizione operativa
Dalle lezioni emergono più definizioni, ma in esame conviene usare una formulazione operativa:

**Big Data** = dati con volume, varietà e velocità tali da rendere inadeguati (o troppo costosi) approcci tradizionali di gestione e analisi.

### Le 3V (minimo sindacale)
- **Volume**: la quantità cresce oltre i limiti pratici di un singolo nodo o di DBMS tradizionali.
- **Varietà**: non solo tabelle relazionali, ma log, eventi, documenti, JSON, grafi, stream.
- **Velocità**: arrivo continuo, spesso in near real-time.

### Le estensioni frequenti (se vuoi alzare il livello)
- **Veridicità**: qualità/affidabilità del dato non uniforme.
- **Valore**: il dato è utile solo se produce decisioni o automazioni.

## 1.2 Perché non basta sempre il modello relazionale
Il modello relazionale resta ottimo per molti casi (integrità, SQL, transazioni forti), ma in scenari Big Data emergono limiti pratici:

- Scalabilità orizzontale complessa su join pesanti.
- Schema rigido in ambienti con dato che evolve rapidamente.
- Costi di join elevati per workload ad alta frequenza.
- Necessità di throughput elevato su operazioni semplici e ripetute.

**Nota importante da ricordare in esame**: NoSQL non sostituisce automaticamente SQL; è una scelta architetturale guidata dal workload.

## 1.3 Famiglie NoSQL richiamate nel corso
Dalle slide: modelli aggregate-oriented e graph-based.

### Aggregate-oriented
- Key-Value
- Document
- Column-family

### Graph-based
- Grafo di nodi e archi, utile quando la relazione è il dato principale.

## 1.4 Aggregate Orientation
Concetto centrale del tuo blocco lezioni.

**Aggregate**: insieme di dati trattati come unità applicativa.

### Implicazioni pratiche
- Le operazioni sono pensate per lavorare “dentro” l’aggregate.
- Le relazioni cross-aggregate sono in genere gestite a livello applicativo (non join nativo pesante in stile RDBMS).
- L’aggregate diventa spesso il confine delle operazioni atomiche/consistenti.

### Vantaggi
- Accesso rapido a dati co-usati spesso.
- Migliore compatibilità con sharding/partizionamento.
- Modello più vicino a certe esigenze applicative reali.

### Svantaggi
- Possibile duplicazione dati tra aggregate.
- Aggiornamenti multi-aggregate più complessi.
- Rischio inconsistenza temporanea se non gestita bene.

## 1.5 CAP e compromessi (versione esame)
Nei sistemi distribuiti:
- **Consistency (C)**: tutti vedono la stessa versione del dato.
- **Availability (A)**: il sistema risponde sempre.
- **Partition tolerance (P)**: il sistema regge partizioni di rete.

In pratica, con partizioni realistiche, scegli compromessi tra C e A.

### Collegamento utile con NoSQL
Molti sistemi NoSQL privilegiano disponibilità/scalabilità e accettano modelli di coerenza meno rigidi (eventual consistency) in alcune operazioni.

## 1.6 Consistenza: strong vs eventual
### Strong consistency
- Dopo una write confermata, ogni read vede il valore aggiornato.
- Più semplice mentalmente, ma può costare in latenza/disponibilità.

### Eventual consistency
- Le repliche convergono nel tempo.
- Ottima per scalare e restare disponibili.
- Richiede logica applicativa robusta (idempotenza, merge policy, retry).

## 1.7 Workload-driven design
Tema trasversale in molte slide: **progettare guardando i pattern di accesso**.

Domande guida:
- Cosa leggo più spesso?
- Cosa aggiorno più spesso?
- Quali campi leggo insieme?
- Serve ordinamento per range?
- Quale query deve essere O(1) o vicino?

Se una risposta critica non è supportata dal modello scelto, il design va rivisto prima di implementare.

## 1.8 Esempio concreto: profilo cliente
Scenario:
- 80% delle volte che leggo nome, leggo anche indirizzo.

Scelta progettuale:
- Aggregare nome + indirizzo nella stessa struttura, invece di spezzare troppo.

Effetto:
- Meno round-trip in lettura.
- Write potenzialmente più “larghe”, ma bilanciate dal beneficio di read.

## 1.9 Domande teoriche tipiche (con risposta sintetica)
### D1. “Cos’è un aggregate e perché è utile in NoSQL?”
Risposta forte:
Un aggregate è un’unità applicativa di dati acceduti/aggiornati insieme. È utile perché riduce join runtime, si adatta allo sharding e ottimizza workload centrati su letture aggregate.

### D2. “Perché NoSQL in Big Data?”
Risposta forte:
Perché in molti contesti Big Data servono scalabilità orizzontale, flessibilità di schema e throughput elevato su pattern specifici che possono essere meno efficienti in approcci relazionali classici.

### D3. “NoSQL significa rinunciare alla consistenza?”
Risposta forte:
No. Significa scegliere il livello di consistenza più adatto al requisito: alcuni flussi richiedono forte consistenza, altri funzionano bene con consistenza eventuale per guadagnare disponibilità e scala.

## 1.10 Mini-esercizi (allenamento rapido)
### Esercizio A
Un’app e-commerce legge sempre `nome prodotto + prezzo + disponibilità` nella pagina catalogo.
- Come modelleresti il dato in logica aggregate-oriented?
- Cosa metteresti nello stesso aggregate?
- Quale trade-off introduci sulle write?

### Esercizio B
Sistema di analytics eventi clickstream in tempo reale.
- Perché un modello relazionale puro può essere limitante?
- Quali caratteristiche NoSQL aiutano?

### Esercizio C
Applicazione bancaria.
- Dove preferisci strong consistency?
- Dove puoi tollerare eventual consistency?

## 1.11 Soluzioni sintetiche mini-esercizi
### Soluzione A
Metto insieme i campi co-letti nella stessa struttura. Vantaggio: read più veloci. Svantaggio: update più pesanti quando cambia un singolo attributo.

### Soluzione B
Volume e velocità elevati rendono critici ingest e scalabilità. NoSQL può aiutare con partizionamento naturale e write throughput alto.

### Soluzione C
Saldo e movimenti contabili: strong consistency. Dashboard aggregate e statistiche differite: eventual consistency accettabile.

## 1.12 Checklist pre-esame (capitolo 1)
- So spiegare le 3V con esempio reale.
- So distinguere modello dati da modello di storage.
- So descrivere aggregate orientation senza confonderla con “tabella”.
- So motivare trade-off C/A in presenza di P.
- So proporre una scelta guidata dal workload e non “per moda”.
