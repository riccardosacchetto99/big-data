# Capitolo 4 - Casi studio ed esempi concreti

In qualità di ingegneri del software, dobbiamo riconoscere che la mera scrittura del codice è l'ultima e meno critica delle attività di sistema. Questo capitolo analizza casi studio reali per dimostrare come il rigore formale e l'analisi semantica siano gli unici strumenti atti a garantire la correttezza e l'affidabilità di architetture complesse.

---

## 1. Analisi Formale dei Sistemi con le Reti di Petri

L'analisi della raggiungibilità permette di verificare se un sistema può evolvere verso stati critici o illegali. Utilizziamo l'approccio algebrico per validare la sicurezza del modello.

### 1.1 Il Problema della Raggiungibilità e l'Equazione Fondamentale

Dato un marking iniziale $m_{Init}$, determiniamo se un marking target $m_{Fin}$ è raggiungibile risolvendo l'**Equazione Fondamentale**:

$$m_{Fin} = m_{Init} + C \cdot s$$

Dove $C$ è la matrice di incidenza e $s$ è il vettore di sparo. Consideriamo la rete descritta nell'Esercizio 1 (2024-01-10.pdf), caratterizzata dalla seguente matrice $C$:

$$C = \begin{bmatrix} 
-1 & -1 & 0 & 0 & 0 & 1 \\
-1 & 0 & 0 & 0 & 1 & 0 \\
1 & 0 & -1 & -1 & 0 & 0 \\
0 & 1 & 0 & 1 & 0 & -1 \\
0 & 0 & 1 & 0 & -1 & 0 
\end{bmatrix}$$

Per verificare la raggiungibilità del marking target $m_{Fin} = <2, 2, 0, 0, 0>$ partendo da $m_{Init} = <1, 1, 0, 0, 0>$, impostiamo il sistema di equazioni lineari:

*   $2 = 1 - s_1 - s_2 + s_6$ (Posto $P_1$)
*   $2 = 1 - s_1 + s_5 \implies s_5 = s_1 + 1$ (Posto $P_2$)
*   $0 = 0 + s_1 - s_3 - s_4$ (Posto $P_3$)
*   $0 = 0 + s_2 + s_4 - s_6$ (Posto $P_4$)
*   $0 = 0 + s_3 - s_5 \implies s_3 = s_5$ (Posto $P_5$)

**Derivazione Algebrica:**
Dalle equazioni sopra, otteniamo $s_3 = s_1 + 1$. Sostituendo nell'equazione del posto $P_3$:
$$s_4 = s_1 - s_3 = s_1 - (s_1 + 1) = -1$$

**Analisi dei Risultati:**
Come architetti, dobbiamo interpretare questo risultato non solo come un fallimento matematico, ma come una violazione dei vincoli fisici del sistema. Poiché $s_4 = -1$, il marking target **non è raggiungibile**. Nelle Reti di Petri, uno sparo negativo è un'impossibilità semantica: una transizione non può consumare token che non sono presenti nei posti di input. Il modello dimostra quindi l'invulnerabilità del sistema rispetto a quello specifico stato target.

### 1.2 Conservatività e Sequenze di Sparo

Analizzando il "Problem 1" (2021-09-15.pdf), valutiamo la raggiungibilità di $<2, 1, 0, 1>$.
*   **Conservatività:** Una rete è conservativa se la somma pesata dei token rimane costante. In questo caso, verifichiamo se il numero totale di token nel marking iniziale coincide con quello target. Se $m_{Init}$ possiede 3 token e $m_{Fin}$ ne richiede 4, la rete non è conservativa rispetto al numero puro di token.
*   **Trade-off:** L'analisi statica tramite l'equazione fondamentale è necessaria ma non sufficiente. Essa può fornire "falsi positivi" (vettori $s$ interi positivi che però non corrispondono a sequenze di sparo ammissibili per mancanza di token intermedi). La simulazione dinamica è l'unico modo per confermare l'ordinamento temporale degli spari.

---

## 2. Semantica del Passaggio dei Parametri e Gestione della Memoria

### 2.1 Confronto tra Semantiche: Reference, Copy-in, Copy-in/Copy-out

La scelta della semantica di passaggio dei parametri definisce il grado di isolamento tra i moduli. Analizziamo l'impatto sulle variabili globali $x, y$ utilizzando il codice dell'Esercizio 3 (2024-01-10.pdf):

| Semantica | Valore Finale $x$ | Valore Finale $y$ | Implicazioni Architetturali |
| :--- | :--- | :--- | :--- |
| **Reference** | 10 | 11 | **Side Effect Massimo**: Le modifiche ai parametri agiscono direttamente sui record di attivazione dei chiamanti. Pericoloso in sistemi multi-thread. |
| **Copy-in (Value)** | 2 | 6 | **Isolamento**: Protegge l'integrità dei dati del chiamante, ma sacrifica l'efficienza a causa della duplicazione della memoria. |
| **Copy-in/Copy-out** | 10 | 11 | **Sincronizzazione Differita**: I risultati sono visibili solo al termine della procedura. Sebbene i valori finali siano identici al Reference in questo caso, il comportamento intermedio è diverso. |

### 2.2 Strutture di Memoria e Record di Attivazione (AR)

La gestione della memoria a runtime si basa sui Record di Attivazione (AR). Secondo l'Esercizio 4 (2024-01-10.pdf), un AR standard è strutturato con i seguenti offset:

*   **Offset 0: Return Address:** Punto di rientro nel codice del chiamante.
*   **Offset 1: Dynamic Pointer (DP):** Indirizzo dell'AR del chiamante (catena dinamica).
*   **Offset 2: Static Pointer (SP):** Indirizzo dell'AR dell'ambiente di definizione (catena statica), fondamentale per risolvere la visibilità non locale.
*   **Variabili Locali e Parametri:** Allocati in posizioni successive (es. offset 3, 4...).

**Analisi della Visibilità:**
In una sequenza $M \rightarrow A \rightarrow B(C) \rightarrow C$:
1.  **Stato Statale:** Se $C$ è definito internamente ad $A$, $B$ può ricevere $C$ come parametro procedurale se $B$ è nello scope di $A$.
2.  **Legalità:** La sequenza è legale se la catena statica permette la risoluzione dei nomi. Se $M$ tenta di chiamare $B(C)$ ma $C$ non è visibile a $M$, il sistema fallisce per violazione delle regole di scope statico.

---

## 3. Verifica del Software e Analisi Dinamica

### 3.1 Esecuzione Simbolica e Path Condition (PC)

L'esecuzione simbolica permette di partizionare lo spazio degli input in classi di equivalenza. Riprendendo l'Esercizio 2 (2024-01-10.pdf), deriviamo la Path Condition per il ramo $P_2$:

**Semplificazione logica di PC2:**
La condizione iniziale è $\neg(a > 0 \land b < 0) \land (a \le 0 \land b < 0)$.
Applicando De Morgan:
$$ (a \le 0 \lor b \ge 0) \land (a \le 0 \land b < 0) $$
Distribuendo l'and sulla disgiunzione:
$$ [a \le 0 \land (a \le 0 \land b < 0)] \lor [b \ge 0 \land (a \le 0 \land b < 0)] $$
Il secondo termine è una contraddizione ($b \ge 0 \land b < 0 \implies False$). Rimane:
$$ PC_2: a \le 0 \land b < 0 $$

**PC Finale (Disgiunzione dei cammini):**
$$ PC_{Totale}: (a > 0 \land b = -a) \lor b = a $$

### 3.2 Testing Strutturale: Decision vs. Condition Coverage

Analizziamo il "Problem 4" (2021-09-15.pdf). Per soddisfare il **Decision Coverage**, ogni decisione deve valutare almeno una volta True e una volta False.

**Test Case Proposti:**
1.  `if (a > b)`: Test case $(a=5, b=3)$ [True], $(a=3, b=5)$ [False].
2.  `while (x != 0 && y > x)`: Test case $(a=5, b=4 \implies x=1, y=0)$ per saltare il loop; $(a=5, b=2 \implies x=3, y=10)$ per entrare.

**Nota Critica:** Il Decision Coverage non garantisce il Condition Coverage. Se abbiamo `if (A || B)`, testare la decisione come True usando solo `A=True` non ci dice nulla sul comportamento del sistema quando `A=False` e `B=True`.

---

## 4. Problematiche Avanzate: Cicli Infiniti e Unificazione

### 4.1 Identificazione di Cicli Infiniti tramite Analisi Simbolica

L'analisi simbolica può dimostrare formalmente l'assenza di terminazione (Failure). Consideriamo un loop con condizione di ingresso $a > 2b$ e condizione di uscita $a \le 2b$.
Se all'interno del loop le trasformazioni simboliche mantengono la relazione $a > 2b$, il tentativo di soddisfare la condizione di uscita $PC \land (a \le 2b)$ risulterà in:
$$ (a > 2b) \land (a \le 2b) \implies False $$
Il verdetto è **"Impossible!"**. Questo prova matematicamente che il sistema entrerà in un ciclo infinito, compromettendo la qualità di Affidabilità.

### 4.2 Unificazione di Termini Logici

L'unificazione è il processo di rendere identici due termini tramite sostituzione $\sigma$.
**Esempio (2021-09-15, Prob 5):**
Coppia: $f1(X, f2(Z,Y), f3(Y,b), Z)$ e $f1(b, W, f3(a,b), c)$
1.  Confronto $X$ e $b$: $\sigma_1 = \{X/b\}$.
2.  Confronto $Z$ e $c$: $\sigma_2 = \{X/b, Z/c\}$.
3.  Confronto $f3(Y,b)$ e $f3(a,b)$: $\sigma_3 = \{X/b, Z/c, Y/a\}$.
4.  Confronto $f2(Z,Y)$ e $W$: $W$ riceve $f2(c,a)$.
**Risultato:** Unificazione riuscita.

Coppia con fallimento: $f1(Y, f2(a,Y), f3(Y,b), a)$ e $f1(c, f2(X,a), f3(a,b), Z)$.
Il "disagreement set" evidenzia che $Y$ dovrebbe essere contemporaneamente $c$ (dal primo termine) e $a$ (dal terzo termine). Poiché $a \neq c$, l'unificazione fallisce.

---

## 5. Errori Frequenti e Domande di Autovalutazione

### 5.1 Errori Comuni nella Progettazione
*   **Static vs Dynamic Link:** Confondere l'ambiente di chiamata con quello di definizione.
*   **Aliasing:** Ignorare che nel passaggio per riferimento due nomi diversi possono puntare alla stessa locazione, causando side effects imprevisti.
*   **Petri Net Oversights:** Ignorare i vincoli di abilitazione delle transizioni (marking non raggiungibile nonostante l'equazione fondamentale abbia soluzioni intere).

### 5.2 Esercizi con Soluzione Rapida
1.  **SimpleSEM:** Tradurre $x = y + z + a$ (Esercizio 4.2, 2024-01-10.pdf).
    *   *Soluzione:* `D[D[current + 2] + 7] = D[D[D[current + 2] + 2] + 4] + D[current + 5] + D[current + 4]`
2.  **Path Condition:** Calcolare PC per `a > b` seguito da `if (a == b)`.
    *   *Soluzione:* $(a > b) \land (a == b) \implies False$. Il ramo è inaccessibile.

### 5.3 Domande di Autovalutazione
1.  Perché il modello Evolutionary è preferibile al Waterfall in presenza di requisiti volatili?
2.  In che modo l'esecuzione simbolica riduce il numero di test case rispetto al testing casuale?
3.  Qual è la differenza semantica tra Catena Statica e Catena Dinamica?
4.  Perché un vettore di sparo $s$ con componenti negative indica l'irraggiungibilità?
5.  Il Decision Coverage è sufficiente per garantire la correttezza logica di un predicato complesso?

---

## 6. Mini-Riepilogo Finale

La costruzione di un sistema ingegneristico si fonda sulla trinità di **Modellazione (Reti di Petri)**, **Semantica (Gestione della Memoria)** e **Verifica (Esecuzione Simbolica)**. Questi pilastri trasformano il software da una collezione fragile di istruzioni a un asset robusto, corretto e affidabile. Ricordate: un vero ingegnere non "prova" il codice finché non funziona; progetta il sistema affinché non possa fallire.