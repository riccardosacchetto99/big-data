# Capitolo 2 - Fondamenti teorici

## 1. Introduzione all'Ingegneria del Software

### 1.1. Definizione e Ambito
L'**Ingegneria del Software** non si esaurisce nella mera scrittura di codice, ma si configura come la disciplina scientifica e tecnologica preposta alla costruzione di sistemi software complessi. Sotto il profilo accademico, essa studia la realizzazione di **sistemi multi-versione**, caratterizzati da un ciclo di vita esteso e dalla necessità di una cooperazione strutturata tra più individui. La distinzione tra "programmazione" e "ingegneria" è netta: mentre la prima si focalizza sulla corretta sequenza di istruzioni per risolvere un problema computazionale, la seconda affronta la gestione di prodotti destinati all'evoluzione, alla manutenzione e all'utilizzo in contesti multi-utente.

### 1.2. Evoluzione Storica e Crisi del Software
Le radici della disciplina risalgono alla fine degli anni '60. Se nei decenni precedenti ('50 e '60) l'enfasi era posta sulla semplificazione della programmazione (tramite l'avvento di Assembler e linguaggi di alto livello come Fortran e Cobol), la diffusione dei primi sistemi commerciali evidenziò limiti strutturali drastici. 

Nel 1968, durante una storica conferenza, fu coniato il termine **Software Crisis** per descrivere una situazione in cui i progetti software risultavano sistematicamente più costosi delle previsioni, affetti da cronici ritardi e incapaci di soddisfare i requisiti degli utenti. Tra le cause determinanti si annoverano la volatilità dei requisiti durante l'implementazione, l'inefficacia della comunicazione interna ai team e l'elevato **turnover del personale**, dove l'abbandono di un singolo sviluppatore poteva compromettere l'integrità dell'intero progetto a causa della scarsa formalizzazione dei processi.

### 1.3. Software vs Ingegneria Tradizionale
Il software possiede proprietà intrinseche che lo differenziano radicalmente dai manufatti dell'ingegneria civile o aeronautica:

| Caratteristica | Ingegneria Tradizionale (Civile/Aeronautica) | Ingegneria del Software |
| :--- | :--- | :--- |
| **Natura del Prodotto** | Rigida: le modifiche post-costruzione sono spesso proibitive o impossibili. | **"Soft"**: il prodotto è intrinsecamente malleabile e modificabile tramite un editor. |
| **Peculiarità della Modifica** | Ogni variazione è preceduta da analisi di impatto rigorose e certificazioni legali. | È estremamente facile modificare il codice, ma è difficilissimo garantire la **modifica corretta** senza effetti collaterali. |
| **Struttura dei Costi** | Legata ai materiali e alla scala di produzione (costi marginali significativi). | Attività **Capital Intensive** legata alle risorse umane. Il costo di riproduzione (copia) è nullo. |

---

## 2. Modelli del Ciclo di Vita del Software (Software Life Cycle)

### 2.1. Il Modello a Cascata (Waterfall)
Il modello a cascata rappresenta l'approccio sequenziale classico, articolato in 5 fasi dove l'output di ciascuna costituisce l'input vincolante per la successiva:
1.  **Analisi e Specifica dei Requisiti**: Definizione formale delle funzionalità del sistema.
2.  **Design (Progettazione)**: Definizione dell'architettura e della struttura dei dati.
3.  **Implementazione**: Codifica effettiva del sistema.
4.  **Validazione, Verifica e Integrazione**: Valutazione della conformità e integrità del sistema.
5.  **Consegna e Manutenzione**: Gestione del software operativo e correzione dei difetti.

**Critica**: Tale modello è una semplificazione teorica. Nella prassi ingegneristica, le fasi si sovrappongono e i **feedback** verso l'alto sono costanti e necessari.

### 2.2. Modelli Evolutivi e Incrementali
Questo approccio prevede cicli ripetuti di costruzione, consegna e feedback. Sebbene garantisca maggiore adattabilità, il rischio principale è la **mancanza di disciplina**. Per mitigare tale rischio, è d'uopo adottare standard di processo rigorosi e strumenti **CASE** (Computer-Aided Software Engineering).

### 2.3. Modelli Basati su Trasformazione
Propongono una derivazione semi-automatica del codice sorgente a partire da specifiche formali attraverso livelli successivi di raffinamento. Nonostante la rigorosità, l'approccio richiede un elevato sforzo computazionale e umano.

### 2.4. Modello a Spirale
Classificato come **meta-modello**, la spirale integra diverse strategie di sviluppo in base all'analisi del rischio e agli obiettivi di progetto.

---

## 3. Qualità del Software

### 3.1. Qualità Esterne (Percepite dall'Utente)
*   **Correttezza**: Qualità assoluta (binaria) che indica la coerenza del software rispetto alle specifiche dei requisiti.
*   **Affidabilità (Reliability)**: Misura statistica e relativa della capacità del sistema di operare senza fallimenti. Peculiarità del software includono una minore aspettativa dell'utente, la presenza di **bug noti** e, sovente, una limitata responsabilità legale del produttore (**no liability**).
*   **Robustezza**: Capacità di comportarsi in modo ragionevole di fronte a eventi imprevisti. Sotto il profilo formale, se il "comportamento ragionevole" viene specificato nei requisiti, la robustezza converge nella **Correttezza**.
*   **Efficienza**: Ottimizzazione dell'uso delle risorse (CPU, memoria). Deve essere affrontata *ex ante*, poiché il miglioramento *ex post* è oneroso.
*   **Usabilità**: Qualità soggettiva dipendente dall'esperienza dell'utente e dal contesto d'uso.

### 3.2. Qualità Interne (Percepite dallo Sviluppatore)
*   **Verificabilità**: Facilità con cui si accertano correttezza e affidabilità. È incrementata da design modulari e linguaggi tipizzati.
*   **Manutenibilità**: Attitudine alla modifica, distinta in **Correttiva** (bug), **Adattativa** (ambiente) e **Perfettiva** (nuove feature).
*   **Riutilizzabilità**: Capacità di impiegare componenti esistenti per ridurre i costi e incrementare l'affidabilità.
*   **Portabilità**: Facilità di migrazione tra diversi ambienti hardware o sistemi operativi.

---

## 4. Validazione e Verifica: Analisi Statica e Dinamica

### 4.1. Fondamenti
L'**Analisi Statica** esamina il codice (o la documentazione) senza eseguirlo. L'**Analisi Dinamica** si basa sull'esecuzione del programma per identificare fallimenti osservabili.

### 4.2. Analisi Dinamica e Problema dell'Infinitezza
A causa dell'**endlessness problem**, un'analisi esaustiva è impossibile. Risulta dunque necessario selezionare un insieme finito di **test case** basandosi su criteri di copertura logica.

### 4.3. Esecuzione Simbolica (Symbolic Execution)
Tecnica di analisi che utilizza valori simbolici ($\alpha, \beta, \dots$) al posto di dati reali. Lo **Stato Simbolico** è definito dalla terna (IP, Variabili, PC). 
La **Path Condition (PC)** è la formula logica che accumula i vincoli sui valori iniziali necessari per percorrere un determinato cammino. Se la PC risulta insoddisfacibile, il cammino è dichiarato **infattibile**.

Per il **Rilevamento di Loop Infiniti**, la strategia consiste nell'entrare nel ciclo con valori generici e dimostrare che la PC necessaria per l'uscita è logicamente equivalente a **Falso** (contraddizione), rendendo l'uscita dal ciclo impossibile.

---

## 5. Semantica e Gestione della Memoria

### 5.1. Passaggio dei Parametri
*   **Per Riferimento**: Il parametro formale è un alias dell'argomento attuale.
*   **Per Copia in Ingresso (Value)**: Il valore viene clonato localmente; nessuna modifica influisce sul chiamante.
*   **Per Copia In-Out**: Il valore è copiato all'ingresso e, alla terminazione, il valore finale del parametro formale viene ricopiato nell'argomento attuale.

### 5.2. Record di Attivazione (AR)
La struttura rigorosa di un AR, essenziale per gestire lo scope statico, include:
1.  **Indirizzo di Ritorno**.
2.  **Puntatore Dinamico** (catena di chiamata).
3.  **Puntatore Statico** (ambiente lessicale).
4.  **Puntatore Statico della procedura P** (per parametri procedurali).
5.  **Dimensione dell'AR di P**.
6.  **Variabili Locali e Parametri** (valore e/o indirizzo).

---

## 6. Modelli Formali: Reti di Petri

Le reti di Petri modellano sistemi concorrenti tramite Posti, Transizioni e una **Marcatura** (stato). Una rete è **conservativa** se il numero di token è costante.
L'**Equazione Fondamentale** per la raggiungibilità è:
$m_{Fin} = m_{Init} + C \cdot s$
Dove $C$ è la matrice di incidenza e $s$ è il vettore degli scatti. È d'uopo sottolineare che $m_{Fin}$ è irraggiungibile se $s$ contiene valori **negativi** o **frazionari**.

---

## 7. Sezione Esercitativa

### 7.1. Esercizio su Reti di Petri
**Dati**: $m_{Init} = <1, 1, 0, 0, 0>^T$, $m_{Fin} = <2, 2, 0, 0, 0>^T$, Matrice $C$ fornita.
**Risoluzione**:
1. $2 = 1 + (-s_1 - s_2 + s_6)$
2. $2 = 1 + (-s_1 + s_5) \implies s_5 = s_1 + 1$
3. $0 = 0 + (s_1 - s_3 - s_4) \implies s_4 = s_1 - s_3$
4. $0 = 0 + (s_3 - s_5) \implies s_3 = s_5 = s_1 + 1$
5. Sostituendo in (3): $s_4 = s_1 - (s_1 + 1) = -1$.
**Conclusione**: $s_4 < 0$ implica l'irraggiungibilità.

### 7.2. Esercizio su Esecuzione Simbolica
Codice `p(int a, int b)` con `printf("**")` finale.
Sviluppando i tre cammini possibili:
*   **PC1**: $(a>0 \land b<0) \land (a-b=2a) \implies a>0 \land b=-a$
*   **PC2**: $(a \le 0 \land b<0) \land (-a-b=-2a) \implies a<0 \land b=a$
*   **PC3**: $(a \le 0 \lor b \ge 0) \land (a>0 \lor b \ge 0) \land (b-a=a-b) \implies a \ge 0 \land b=a$
**PC Finale** ($PC_1 \lor PC_2 \lor PC_3$): $(a>0 \land b=-a) \lor (b=a)$.

### 7.3. Esercizio su Semantica Parametri
`x=1; y=3; x=p(y,x); y=p(x,y);` con `p(a,b) { a=2a-b; b=2b-a; return a+b; }`
*   **Riferimento**: x=10, y=11.
*   **Valore (Copia In)**: x=2, y=6.
*   **Copia In-Out**: 
    1. Chiamata `p(3,1)`: $a \to 5, b \to -3$. Return 2. Copy-out: $y=5, x=-3$. Assegnamento: $x=2$.
    2. Chiamata `p(2,5)`: $a \to -1, b \to 11$. Return 10. Copy-out: $x=-1, y=11$. Assegnamento: $y=10$.
    **Risultato**: x=-1, y=10.

### 7.4. Esercizio su Testing e Copertura
Codice: `y=0; if(a>b) x=a-b; else x=b-a; while(x!=0 && y>x) { ... }`
*   **Decision Coverage**: Richiede test case per `if` (T/F) e `while` (T/F). 
    *   (a=5, b=2) copre `if=T` e `while=F`. 
    *   (a=2, b=5) copre `if=F` e `while=F`. 
*   **Criticità**: Il corpo del `while` è inattaccabile poiché $y=0$ e $x=|a-b| \ge 0$, dunque $y>x$ è sempre Falso all'ingresso se $x \neq 0$.

### 7.5. Esercizio su Unificazione
1. $f1(X, f2(Z,Y), f3(Y,b), Z)$ e $f1(b, W, f3(a,b), c)$
   **Sostituzione**: $\{X/b, Z/c, Y/a, W/f2(c,a)\}$. **Unificabile**.
2. $f1(Y, f2(a,Y), f3(Y,b), a)$ e $f1(c, f2(X,a), f3(a,b), Z)$
   $Y=c, X=a, Z=a$. Ma $f3(Y,b) \to f3(c,b)$ non unifica con $f3(a,b)$ poiché $c \neq a$. **Non unificabile**.

---

## 8. Errori Frequenti e Autovalutazione

### 8.1. Errori Comuni
*   **Confusione Correctness/Reliability**: Considerare la mancanza di bug come unico indice di affidabilità.
*   **Record di Attivazione**: Omettere il puntatore statico, fondamentale per la risoluzione dei nomi in scope statico.
*   **Esecuzione Simbolica**: Non considerare tutte le disgiunzioni dei cammini nella PC finale.
*   **Petri**: Ignorare che un vettore degli scatti non intero implica l'irraggiungibilità fisica dei token.

### 8.2. Domande di Autovalutazione
1. Qual è la differenza economica principale tra software e ingegneria civile?
2. Perché il modello a cascata è considerato un'iper-semplificazione?
3. In quali casi la Robustezza coincide con la Correttezza?
4. Come si dimostra un loop infinito tramite l'analisi simbolica?
5. Qual è la funzione del puntatore statico in un Record di Attivazione?

---

## 9. Mini-Riepilogo Finale

| Concetto | Definizione / Proprietà | Obiettivo |
| :--- | :--- | :--- |
| **Software Engineering** | Sistemi multi-versione e multi-persona. | Gestione complessità e manutenzione. |
| **Reliability** | Statistica, tollera bug noti, no liability. | Misurare la fiducia nel sistema. |
| **Analisi Dinamica** | Basata su esecuzione (Endlessness problem). | Identificazione fallimenti. |
| **Copia In-Out** | Copia all'ingresso e sovrascrittura al ritorno. | Gestione effetti collaterali controllata. |
| **PC Satisfiability** | Se PC è Falso, il cammino è infattibile. | Verifica percorribilità logica. |
| **Raggiungibilità Petri**| $m_{Fin} = m_{Init} + C \cdot s, s \in \mathbb{N}^n$. | Verifica stati possibili del sistema. |