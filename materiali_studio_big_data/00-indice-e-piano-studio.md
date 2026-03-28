# Preparazione Parziale - Big Data / NoSQL (Marzo 2026)

## Fonti usate
- class-2026-02-27.pdf
- class-2026-03-03.pdf
- class-2026-03-06-a.pdf
- class-2026-03-06-b.pdf
- class-2026-03-10.pdf
- class-2026-03-13a.pdf
- class-2026-03-13b.pdf
- class-2026-03-20.pdf
- class-2026-03-24.pdf
- class-2026-03-27.pdf
- Example of first partial test.pdf

## Come usare questi materiali
1. Parti da `01-fondamenti-big-data-e-nosql.md` per fissare lessico e concetti cardine.
2. Studia `02-modellazione-aggregate-key-value.md` per la parte progettuale (quella che spesso entra nelle domande teoriche).
3. Passa a `03-redis-operazioni-transazioni-indici.md` per comando, complessità e casi pratici Redis.
4. Chiudi con `04-esercizi-guidati-e-simulazioni-parziale.md` per allenarti in stile prova d’esame.

## Strategia studio consigliata (rapida ma solida)
- Sessione 1 (90 min): Cap. 1 + mappe concettuali.
- Sessione 2 (120 min): Cap. 2 + riscrittura a mano di 2 modelli dati.
- Sessione 3 (120 min): Cap. 3 + mini-lab Redis (comandi su dataset piccolo).
- Sessione 4 (120 min): Simulazione completa da Cap. 4 con correzione.

## Obiettivi minimi per il parziale
- Saper spiegare con parole tue: aggregate, atomic aggregate, trade-off read/write, shard key.
- Saper progettare una naming convention coerente per le key.
- Saper motivare quando usare string/hash/list/set/zset in Redis.
- Saper descrivere il flusso `MULTI ... EXEC` e i casi limite.
- Saper costruire un indice secondario semplice con `ZADD` + query con `ZRANGE`.

## Errori che abbassano il voto
- Definizioni generiche senza esempio concreto.
- Ignorare i trade-off (es. meno read ma write più pesanti).
- Modelli key-value senza convenzioni di naming.
- Risposte Redis senza complessità o impatti pratici.
- Esercizi senza giustificazione della scelta del modello.
