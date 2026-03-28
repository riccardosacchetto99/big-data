# Capitolo 6 - Simulazione d'esame

## 1. Introduzione e Obiettivi della Simulazione

Benvenuti alla sessione di simulazione d'esame per il corso di **Software Engineering Fundamentals**. Questo documento è stato redatto per riflettere fedelmente il rigore metodologico e la precisione analitica richiesti durante le prove ufficiali del Prof. Alberto Coen Porisini. 

In ingegneria del software, la capacità di risolvere un problema è secondaria solo alla capacità di dimostrare la correttezza della soluzione tramite modelli formali. **Non sono ammesse soluzioni approssimative**: lo studente deve dimostrare una padronanza assoluta sia della componente teorica (cicli di vita e metriche di qualità) sia di quella pratica (Reti di Petri, semantica dei linguaggi, testing e logica). Questo capitolo funge da guida strutturata per trasformare le nozioni teoriche in strumenti operativi pronti per l'applicazione in sede d'esame.

---

## 2. Sezione I: Modellazione con Reti di Petri

### 2.1 Analisi Teorica e Metodologica
Le Reti di Petri sono strumenti formali per la modellazione di sistemi asincroni e concorrenti. La loro analisi si basa su due proprietà cardine:

1.  **Raggiungibilità**: Determina se una marcatura $m_{Fin}$ è ottenibile da $m_{Init}$. Si utilizza l'equazione fondamentale:
    $$m_{Fin} = m_{Init} + C \cdot s$$
    Dove $C$ è la matrice di incidenza e $s$ è il vettore di sparo (*firing vector*). **Vincolo fondamentale**: Tutte le componenti di $s$ devono essere interi non negativi ($s_i \in \mathbb{N}$). Un valore negativo indica l'impossibilità fisica di scattare le transizioni necessarie.
2.  **Conservatività**: Una rete è conservativa se esiste un vettore di pesi $w$ composto da elementi tutti positivi ($w > 0$) tale che:
    $$w^T \cdot C = 0$$
    Ciò garantisce che la somma pesata dei gettoni nei posti rimanga costante per ogni marcatura raggiungibile.

### 2.2 Esercizio Pratico: Verifica di Raggiungibilità (Appello 2024-01-10)
**Quesito**: Determinare se la marcatura $m_{Fin} = \langle 2, 2, 0, 0, 0 \rangle$ è raggiungibile partendo da $m_{Init} = \langle 1, 1, 0, 0, 0 \rangle$.

**Svolgimento**:
Dall'equazione $m_{Fin} - m_{Init} = C \cdot s$, otteniamo il sistema lineare basato sulla matrice $C$ della rete:
1.  $(2-1) = -s_1 - s_2 + s_6 \implies -s_1 - s_2 + s_6 = 1$
2.  $(2-1) = -s_1 + s_5 \implies s_5 = s_1 + 1$
3.  $(0-0) = s_1 - s_3 - s_4 \implies s_4 = s_1 - s_3$
4.  $(0-0) = s_2 + s_4 - s_6$
5.  $(0-0) = s_3 - s_5 \implies s_3 = s_5$

Sostituendo (2) in (5), otteniamo $s_3 = s_1 + 1$. Sostituendo quest'ultimo valore in (3):
$$s_4 = s_1 - (s_1 + 1) = -1$$
**Conclusione**: Poiché $s_4 < 0$, la marcatura **non è raggiungibile**.

### 2.3 Errori Frequenti e Rubrica di Valutazione
*   **Segni in C**: Errata attribuzione del segno $-1$ agli archi entranti nelle transizioni e $+1$ a quelli uscenti.
*   **Omissione del Vincolo $s$**: Validare una soluzione matematica senza verificare che i valori di $s$ siano interi positivi.

| Criterio di Valutazione | Punteggio Massimo |
| :--- | :---: |
| Corretta costruzione della matrice di incidenza $C$ | 3 pt |
| Impostazione e risoluzione del sistema lineare | 3 pt |
| Analisi del vettore di sparo $s$ e conclusione | 2 pt |
| **Totale** | **8 pt** |

---

## 3. Sezione II: Semantica dei Parametri e Gestione della Memoria

### 3.1 Confronto Semantico
*   **By Reference**: Il parametro formale è un puntatore alla locazione di memoria del parametro reale.
*   **By Copy-in**: Il valore viene copiato all'attivazione; modifiche locali non influenzano il chiamante.
*   **By Copy-in Copy-out**: Il valore viene copiato in ingresso; al termine dell'esecuzione, il valore finale del parametro formale viene ricopiato nel parametro reale.

### 3.2 Esercizio di Tracciamento Codice (2024)
Si analizzi il codice con $x=1, y=3$ iniziali e le chiamate `x = p(y, x)` e `y = p(x, y)`.

**Semantica: By Reference**
| Passo | a | b | x | y |
| :--- | :--- | :--- | :---: | :---: |
| Call 1: p(y,x) | alias y | alias x | 1 | 3 |
| Modifiche | a=5, b=-3 | | -3 | 5 |
| **Fine Call 1** | x = p = 2 | | **2** | **5** |
| Call 2: p(x,y) | alias x | alias y | 2 | 5 |
| Modifiche | a=-1, b=11 | | -1 | 11 |
| **Fine Call 2** | y = p = 10 | | **-1** | **10** |

**Semantica: By Copy-in**
| Passo | a (form.) | b (form.) | x (reale) | y (reale) |
| :--- | :---: | :---: | :---: | :---: |
| Call 1: p(3,1) | 5 | -3 | **2** (ret) | **3** |
| Call 2: p(2,3) | 1 | 5 | **2** | **6** (ret) |

**Semantica: By Copy-in Copy-out**
| Passo | a (form.) | b (form.) | x (reale) | y (reale) |
| :--- | :---: | :---: | :---: | :---: |
| Call 1: p(3,1) | 5 | -3 | **-3** (out) | **5** (out) |
| Fine Call 1 | | | **2** (x=p) | **5** |
| Call 2: p(2,5) | -1 | 11 | **-1** (out) | **11** (out) |
| **Fine Finale** | | | **11** | **10** (y=p) |

### 3.3 SimpleSEM e Record di Attivazione
Dall'Esercizio 4 (2024), la traduzione dell'assegnamento `x = y + z + a` in procedura $C$ richiede la navigazione dei puntatori statici:
*   `z` (locale a $C$): `D[current + 5]`
*   `a` (locale a $C$, valore): `D[current + 4]`
*   `x` (in $A$, un salto statico): `D[D[current + 2] + 7]`
*   `y` (in $B$, due salti statici): `D[D[D[current + 2] + 2] + 4]`

---

## 4. Sezione III: Testing e Analisi Dinamica

### 4.1 Decision vs. Condition Coverage
Il *Decision Coverage* richiede che ogni ramo di un predicato sia testato. Il *Condition Coverage* richiede che ogni singola variabile booleana atomica all'interno del predicato assuma valore vero e falso.

### 4.2 Esecuzione Simbolica: Calcolo della Path Condition (PC)
Per la stampa `printf("**")` nel codice 2024, analizziamo i percorsi:

1.  **P1 (1-2-6-7)**: $a>0 \land b<0$ e $x=y \implies (a-b=2a) \implies a=-b$.
    *   **PC1**: $a>0 \land b = -a$.
2.  **P2 (1-3-4-6-7)**: $\neg(a>0 \land b<0) \land (a \le 0 \land b < 0) \land (x=y)$.
    *   Semplificazione: $(a \le 0 \land b < 0) \land (-(a+b) = -2a) \implies -a-b = -2a \implies b=a$.
    *   **PC2**: $a < 0 \land b = a$.
3.  **P3 (1-3-5-6-7)**: $\neg(a>0 \land b<0) \land \neg(a \le 0 \land b < 0) \land (x=y)$.
    *   Semplificazione: $(a > 0 \lor b \ge 0) \land (a > 0 \lor b \ge 0) \land (b-a = a-b) \implies b=a$.
    *   Considerando i vincoli: $a \ge 0 \land b = a$.

**PC Totale (Disgiunzione)**: $(a>0 \land b = -a) \lor (a<0 \land b=a) \lor (a \ge 0 \land b=a) \implies \mathbf{(a>0 \land b = -a) \lor (b=a)}$.

### 4.3 Cicli Infiniti
L'esecuzione simbolica prova l'esistenza di un ciclo infinito se la PC per l'uscita dal loop risulta `false` (contraddizione). Se entrando in un loop con $a > b$ le operazioni interne rendono la condizione di uscita $a \le b$ logicamente impossibile, il sistema fallisce formalmente.

---

## 5. Sezione IV: Unificazione e Logica

**Esercizio (Problem 5, 2021)**:
1.  `f1(X, f2(Z,Y), f3(Y,b), Z)` e `f1(b, W, f3(a,b), c)`
    *   $X = b$; $Z = c$; $f3(Y,b) = f3(a,b) \implies Y = a$.
    *   $W = f2(Z,Y) \implies W = f2(c,a)$.
    *   **Sostituzione**: $\{X/b, Y/a, Z/c, W/f2(c,a)\}$.
2.  `f1(Y, f2(a,Y), f3(Y,b), a)` e `f1(c, f2(X,a), f3(a,b), Z)`
    *   $Y = c$; $f3(Y,b) = f3(a,b) \implies Y = a$.
    *   **Risultato**: **Impossibile**. Una variabile ($Y$) non può essere unificata simultaneamente a due costanti diverse ($a$ e $c$).

---

## 6. Sezione V: Fondamenti di Ingegneria del Software

### 6.1 Definizioni e Storia
*   **Software Engineering**: Disciplina che studia la costruzione di sistemi software **multi-person** e **multi-version**. Sviluppare un sistema è radicalmente diverso dallo scrivere codice.
*   **Software Crisis**: Emersa a fine anni '60, causata dall'incapacità di gestire la complessità. Un fattore chiave fu che "la maggior parte del tempo era spesa a parlare l'uno con l'altro piuttosto che a scrivere codice".

### 6.2 Modelli di Ciclo di Vita
*   **Waterfall**: Sequenziale, rigido. Utile per identificare le fasi ma distante dalla realtà (manca di incrementalità).
*   **Evolutionary**: Iterativo, basato su feedback. Rischio: mancanza di disciplina e standardizzazione del processo.

### 6.3 Qualità del Software
| Qualità Esterne (Utente) | Qualità Interne (Sviluppatore) |
| :--- | :--- |
| **Correttezza**: Coerenza con i requisiti. | **Manutenibilità**: Facilità di modifica. |
| **Affidabilità**: Operatività senza fallimenti. | **Riusabilità**: Riuso di spec/design/codice. |
| **Robustezza**: Comportamento in casi imprevisti. | **Verificabilità**: Facilità di controllo qualità. |

**Relazione Correttezza/Affidabilità**: La correttezza implica l'affidabilità **solo se** tutti i requisiti sono correttamente elencati nelle specifiche. In caso contrario, un software "corretto" rispetto a una specifica incompleta può risultare inaffidabile per l'utente.

---

## 7. Conclusione e Autovalutazione

### 7.1 Domande di Autovalutazione
1.  Perché il parametro **MTBF** non ha senso per il software? (Risposta: Il software non si "usura" fisicamente; i guasti sono errori di design, non statistici).
2.  Cosa implica un valore negativo in $s$ per una Petri Net?
3.  Perché la *Software Crisis* ha distinto il "buon programmare" dal "creare buoni sistemi"?
4.  In esecuzione simbolica, quando un percorso è definito "unfeasible"?
5.  Qual è il vantaggio principale della riusabilità in termini di costi e affidabilità?

### 7.2 Mini-Riepilogo Finale
Lo studente deve dimostrare assoluta padronanza di:
*   **Semplificazione logica delle Path Condition**: Non limitarsi a scrivere la disgiunzione, ma ridurla ai minimi termini.
*   **Vettore di sparo**: Verifica rigorosa della non-negatività.
*   **Scoping Statico**: Corretta navigazione della catena dei record di attivazione in SimpleSEM tramite offset interi specifici.