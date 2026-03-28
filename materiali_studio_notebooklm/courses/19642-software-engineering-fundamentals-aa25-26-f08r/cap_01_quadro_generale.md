# Capitolo 1 - Quadro generale del corso

Il presente documento costituisce la base metodologica e concettuale del corso "SOFTWARE ENGINEERING FUNDAMENTALS". È imperativo che lo studente approcci questa disciplina non come un’estensione delle tecniche di programmazione, ma come una rigorosa formalizzazione dei processi di creazione di sistemi complessi.

## 1. Introduzione e Obiettivi del Corso
La missione del corso è fornire i fondamenti teorici e pratici necessari per governare la transizione critica tra il semplice atto di "scrivere codice" e l’attività ingegneristica di "costruire un sistema". 

Un sistema software si distingue da un programma isolato per due parametri fondamentali:
*   **Natura Multi-persona:** Lo sviluppo richiede la cooperazione coordinata di diversi attori, rendendo la comunicazione e la gestione dei conflitti aspetti tecnici centrali.
*   **Natura Multi-versione:** Il software è un'entità destinata a evolvere nel tempo attraverso manutenzioni e aggiornamenti.

L’Ingegneria del Software è la disciplina che studia la costruzione di sistemi destinati a durare ed evolvere. Gli obiettivi formativi comprendono la padronanza del ciclo di vita (Software Life Cycle), la gestione della complessità attraverso modelli formali e l'applicazione di un rigore metodologico che separi l'intuizione soggettiva dalla verifica oggettiva.

## 2. Evoluzione Storica e la "Software Crisis"
Per comprendere l'Ingegneria del Software, occorre analizzare il fallimento dei metodi artigianali negli anni '60.

### Il Contesto Storico
*   **Anni '50 - Inizio '60:** L'enfasi era sulla risoluzione di problemi algoritmici (Assembler, Fortran). In questa fase, il **Programmatore coincideva con l'Utente**.
*   **Fine anni '60:** Con la diffusione dei sistemi commerciali, nasce la separazione tra chi esprime il bisogno (utente) e chi implementa la soluzione (programmatore).
*   **1968 (Conferenza Garmisch):** Viene coniato il termine **"Software Crisis"**.

### Fattori critici e la distinzione fondamentale
Il materiale didattico identifica chiaramente le cause della crisi:
*   **Costi e Tempi:** Progetti sistematicamente fuori budget e in ritardo.
*   **Invisibilità e Complessità:** La difficoltà di tracciare l'avanzamento del lavoro porta a spendere più tempo in coordinamento che in implementazione.
*   **Cambiamento dei Requisiti:** L'instabilità delle specifiche durante lo sviluppo destabilizza l'intero sistema.
*   **Personnel Turnover:** La perdita di una risorsa umana equivale spesso alla perdita di conoscenza vitale.

Il "punchline" filosofico di questo corso è il seguente: **Good programming $\neq$ Good systems.** Saper scrivere un ottimo algoritmo non garantisce minimamente la qualità di un sistema complesso che deve operare in un ambiente multi-utente e multi-versione.

## 3. Modelli di Ciclo di Vita del Software (Software Life Cycle)
L'ingegnere deve scegliere il modello più adatto alla natura del progetto per organizzare le attività dalla concezione alla dismissione.

### Modello a Cascata (Waterfall)
Il pilastro storico, basato su 5 fasi sequenziali:
1.  **Analisi e Specifica dei Requisiti:** Definizione rigorosa del *cosa*.
2.  **Design:** Architettura del *come*.
3.  **Implementazione:** Codifica.
4.  **Validazione, Verifica e Integrazione (V&V):** Valutazione della correttezza.
5.  **Manutenzione:** Gestione post-consegna.
*   **Limiti:** Il modello ignora che nella realtà le fasi si sovrappongono e richiedono feedback continui.

### Modello Evolutivo
Approccio incrementale basato sul ciclo **"build-deliver-feedback"**. Sebbene riduca il rischio di divergenza dai bisogni dell'utente, il pericolo principale è la **mancanza di disciplina**. Senza l'uso di strumenti CASE (Computer-Aided Software Engineering) e standardizzazione, il modello degenera in "code-and-fix".

### Modello Transformation-based
Un processo semi-automatico in cui il codice viene derivato formalmente dai requisiti tramite raffinamenti successivi. Storicamente è stato considerato un esercizio accademico, ma rimane il punto di riferimento per il rigore formale.

### Meta-modello a Spirale
Cornice integrativa che pone l'analisi del rischio al centro di ogni iterazione di sviluppo.

## 4. Qualità del Software: Interne ed Esterne
La qualità non è un concetto monolitico. Bisogna distinguere tra ciò che l'utente percepisce e ciò che lo sviluppatore deve garantire.

### Qualità Esterne (User-facing)
*   **Correttezza:** Coerenza funzionale assoluta rispetto alle specifiche. È una qualità binaria: il sistema è o non è corretto.
*   **Affidabilità:** Misura statistica del comportamento del sistema nel tempo (es. MTBF - Mean Time Between Failures). È una qualità relativa.
*   **Robustezza:** Capacità di gestire input non validi o condizioni ambientali impreviste senza crash catastrofici.
*   **Efficienza:** Ottimizzazione delle risorse (CPU, memoria). Se non inserita nei requisiti iniziali, l'ottimizzazione *ex-post* è quasi sempre fallimentare.

### Qualità Interne (Developer-facing)
*   **Verificabilità:** Facilità con cui si possono testare correttezza e affidabilità.
*   **Manutenibilità:** Facilità di modifica. Si divide in **Correttiva** (bug fix), **Adattativa** (cambio OS/Hardware) e **Perfettiva** (nuove feature).
*   **Riutilizzabilità e Portabilità:** Capacità di operare in contesti diversi e con componenti pre-esistenti.

### Tabella di Confronto: Correttezza vs. Affidabilità

| Caratteristica | Correttezza | Affidabilità |
| :--- | :--- | :--- |
| **Natura** | Assoluta (Sì/No) | Relativa (Statistica/Contestuale) |
| **Riferimento** | Rispetto alle specifiche formali | Rispetto alle aspettative/uso reale |
| **Relazione** | Se le specifiche sono complete, implica l'affidabilità | Non sempre implica la correttezza |
| **In assenza di specifiche** | Non definibile | Definibile tramite osservazione |

## 5. Lessico Tecnico e Concetti Fondamentali
Lo studente deve assimilare il seguente glossario per la trattazione dei modelli formali:

*   **Reti di Petri:** Strumento matematico per modellare sistemi concorrenti e distribuiti.
*   **Marcatura ($m$):** Stato corrente del sistema rappresentato da gettoni (tokens) nei posti della rete.
*   **Equazione Fondamentale:** $m_{Fin} = m_{Init} + C \cdot s$, dove $C$ è la matrice d'incidenza e $s$ il vettore degli scatti (firing sequence).
*   **SimpleSEM:** Modello formale di memoria. Un accesso a una variabile locale `x` si esprime come `D[current + offset_x]`, mentre l'accesso a una variabile `y` in uno scope superiore richiede l'uso dei puntatori statici: `D[D[current + 2] + offset_y]`.
*   **Activation Record (AR):** Struttura in memoria che contiene: Return Address (ind. 0), Dynamic Pointer (ind. 1), Static Pointer (ind. 2), Parametri e Variabili Locali.
*   **Esecuzione Simbolica:** Analisi del codice tramite valori astratti ($\alpha, \beta$) per identificare proprietà logiche del sistema.
*   **Path Condition (PC):** Insieme di vincoli logici che definiscono gli input necessari per percorrere un determinato cammino nel grafo di controllo.

## 6. Prerequisiti, Mappa dei Contenuti e Collegamenti
**Prerequisiti:** Padronanza di algoritmi, strutture dati e linguaggi C-like.
**Mappa e Collegamenti:** Esiste un legame indissolubile tra la **Verificabilità** (qualità interna) e la **Correttezza** (qualità esterna). L'uso di modelli formali (Reti di Petri) non è un'opzione accademica, ma una necessità per garantire la qualità in sistemi *safety-critical*. La teoria dei modelli serve a prevenire l'esplosione combinatoria degli stati che rende impossibile il test esaustivo.

## 7. Esempi Concreti e Analisi Rigorosa

### Caso 1: Analisi della Manutenibilità
Il software è "morbido" (soft) perché può essere modificato con un editor di testo. Tuttavia, questa facilità fisica è un'illusione. In ingegneria, ogni modifica deve essere progettata e valutata. L'approccio "proviamo e vediamo" è la causa primaria del degrado dei sistemi software.

### Caso 2: Esecuzione Simbolica e Cicli Infiniti
Si consideri un ciclo `while (x > y)` dove all'interno del corpo le trasformazioni simboliche portano a una situazione in cui la condizione di uscita è intrinsecamente falsa. Attraverso l'esecuzione simbolica, possiamo dimostrare che se $a > b \land a \leq 2b$ (assunzioni iniziali), il sistema entrerà in un **loop infinito**. Questo dimostra che l'analisi simbolica non serve solo a trovare input di test, ma a provare l'assenza (o la presenza) di errori fatali di terminazione.

## 8. Esercizi con Soluzione Commentata

### Esercizio 1 (Reti di Petri: Raggiungibilità Formale)
Data la marcatura iniziale $m_{Init} = [1, 1, 0, 0, 0]^T$ e la marcatura finale desiderata $m_{Fin} = [2, 2, 0, 0, 0]^T$, determinare la raggiungibilità usando la matrice d'incidenza $C$ del materiale sorgente.

**Svolgimento:**
Utilizziamo l'equazione $m_{Fin} - m_{Init} = C \cdot s$. Sostituendo i valori:
$[2-1, 2-1, 0-0, 0-0, 0-0]^T = C \cdot s$
Si ottiene il sistema:
1. $1 = -s_1 - s_2 + s_6$
2. $1 = -s_1 + s_5 \implies s_5 = s_1 + 1$
3. $0 = s_1 - s_3 - s_4$
4. $0 = s_2 + s_4 - s_6$
5. $0 = s_3 - s_5 \implies s_3 = s_5 = s_1 + 1$

Sostituendo (5) in (3):
$0 = s_1 - (s_1 + 1) - s_4 \implies 0 = -1 - s_4 \implies \mathbf{s_4 = -1}$
**Conclusione:** Poiché il numero di scatti $s_4$ è negativo, la marcatura **non è raggiungibile**.

### Esercizio 2 (Semantica di Passaggio Parametri)
Si consideri il frammento con `x = 1, y = 3` e due chiamate in sequenza: `x = p(y, x); y = p(x, y);` con la funzione `p(a, b)` definita come: `a = 2*a - b; b = 2*b - a; return(a+b);`.

**Svolgimento Passo-Passo:**
*   **By Reference:**
    1. `p(y, x)`: $a \to y, b \to x$. Calcolo: $y = 2(3)-1 = 5$; $x = 2(1)-5 = -3$. Ritorna 2. `x` diventa 2. Stato: $x=2, y=5$.
    2. `p(x, y)`: $a \to x, b \to y$. Calcolo: $x = 2(2)-5 = -1$; $y = 2(5)-(-1) = 11$. Ritorna 10. `y` diventa 10.
    **Risultato Finale:** $x = -1, y = 10$.
*   **By Copy-in:**
    1. `p(3, 1)`: $a=3, b=1$. Calcolo locale: $a=5, b=-3$. Ritorna 2. `x=2`. Stato: $x=2, y=3$.
    2. `p(2, 3)`: $a=2, b=3$. Calcolo locale: $a=1, b=5$. Ritorna 6. `y=6`.
    **Risultato Finale:** $x = 2, y = 6$.

### Esercizio 3 (Path Condition e Disgiunzione)
Determinare la Path Condition (PC) totale per eseguire `printf("**")` basandosi sui tre cammini $P_1, P_2, P_3$ del materiale d'esame (Jan 10th).

**Svolgimento:**
1.  $PC_1$ (Cammino 1-2-6-7): $(a > 0 \land b < 0) \land (a - b = 2a) \implies a > 0 \land b = -a$.
2.  $PC_2$ (Cammino 1-3-4-6-7): $\neg(a > 0 \land b < 0) \land (a \leq 0 \land b < 0) \land (-(a+b) = -2a) \implies a < 0 \land b = a$.
3.  $PC_3$ (Cammino 1-3-5-6-7): $\neg(a > 0 \land b < 0) \land \neg(a \leq 0 \land b < 0) \land (b - a = a - b) \implies a \geq 0 \land b = a$.
**Sintesi finale:** $PC = (a > 0 \land b = -a) \lor (a < 0 \land b = a) \lor (a \geq 0 \land b = a)$, che si semplifica in: $\mathbf{PC = (a > 0 \land b = -a) \lor (b = a)}$.

## 9. Errori Frequenti e Pitfall Metodologici
*   **Confusione tra Bug e Robustezza:** Correggere un bug ripristina la correttezza, ma non aumenta necessariamente la robustezza (gestione di ciò che non è specificato).
*   **L’illusione del Test Esaustivo:** Ignorare l'infinità dei possibili input. Bisogna usare criteri di copertura logica, non quantitativa.
*   **Scope Dinamico vs Statico:** Tradurre variabili in SimpleSEM senza considerare il record di attivazione corretto porta a violazioni della memoria non rilevate.

## 10. Domande di Autovalutazione
1.  **Perché il costo di produzione del software è atipico?** Perché la produzione coincide con il design. La replica fisica della "copia" ha costo marginale nullo, rendendo il rigore nel design l'unico modo per controllare i costi totali.
2.  **In quali casi una Path Condition risulta non soddisfacibile?** Quando il percorso è logicamente "unfeasible" (es. $x > 0 \land x < 0$) o quando il sistema entra in uno stato di non-terminazione provabile simbolicamente.
3.  **Qual è il vantaggio strutturale del modello evolutivo?** Permette di ricevere feedback dall'utente molto prima della fase finale di V&V del Waterfall, riducendo il rischio di costruire il sistema "sbagliato" (anche se correttamente implementato).

## 11. Mini-Riepilogo Finale
L'Ingegneria del Software è la risposta rigorosa alla "Software Crisis" degli anni '60. Fondata sulla gestione del ciclo di vita e sulla misurazione delle qualità interne ed esterne, essa trasforma lo sviluppo da pratica artigianale a disciplina scientifica, dove la correttezza è garantita da modelli formali e analisi dinamiche sistematiche.