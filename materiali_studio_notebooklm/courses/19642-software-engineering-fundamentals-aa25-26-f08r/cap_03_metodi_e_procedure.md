# Capitolo 3 - Metodi e procedure operative

## 1. Introduzione alla Metodologia Ingegneristica

In ambito accademico e professionale, è imperativo distinguere tra l'attività di "programmazione" e la disciplina dell' "ingegneria del software". Mentre la prima si configura spesso come una risoluzione algoritmica estemporanea condotta da un singolo individuo, l'Ingegneria del Software è lo studio della costruzione di sistemi multi-versione, destinati a cicli di vita prolungati e realizzati mediante la cooperazione coordinata di più attori.

La natura "morbida" del software costituisce il paradosso centrale della materia: l'estrema facilità con cui è possibile modificare il codice sorgente tramite un semplice editor induce a un approccio empirico non rigoroso ("code-and-fix"). Al contrario, l'ingegneria insegna che la malleabilità del software richiede un rigore metodologico superiore rispetto ai prodotti fisici, poiché ogni modifica può propagare effetti collaterali non deterministici nell'intero sistema.

La cosiddetta **"Software Crisis"**, termine coniato nel 1968, identifica una serie di criticità sistemiche che tuttora affliggono i progetti non gestiti secondo criteri ingegneristici:
*   **Costi elevati:** Le risorse economiche necessarie superano sistematicamente le stime iniziali.
*   **Ritardi cronici:** La mancata aderenza a modelli di processo porta a scivolamenti imprevedibili delle date di rilascio.
*   **Requisiti cangianti:** L'evoluzione delle necessità dell'utente durante l'implementazione distrugge l'integrità del sistema se non gestita formalmente.
*   **Difficoltà di comunicazione:** Il turnover del personale e l'assenza di specifiche formali causano una perdita di conoscenza critica ad ogni cambio di team.

## 2. Analisi Formale: Workflow per le Reti di Petri

L'analisi della raggiungibilità di una marcatura in una rete di Petri non deve basarsi sull'intuizione, ma sulla risoluzione del sistema lineare derivante dall'**Equazione Fondamentale**:

$$m_{fin} = m_{init} + C \cdot s$$

Dove $m_{fin}$ rappresenta la marcatura finale target, $m_{init}$ la marcatura iniziale, $C$ la matrice di incidenza e $s$ il vettore di sparo (firing vector).

### Procedura Operativa di Analisi (Rif. Esercizio 1)
Consideriamo una rete con $m_{init} = [1, 1, 0, 0, 0]^T$ e l'obiettivo $m_{fin} = [2, 2, 0, 0, 0]^T$.
1.  **Costruzione della matrice $C$:** Si estraggono le relazioni dai flussi degli archi (archi uscenti dalle transizioni - archi entranti).
2.  **Impostazione del sistema:** Si risolve l'equazione per il vettore $s = [s_1, s_2, s_3, s_4, s_5, s_6]^T$.
3.  **Derivazione algebrica:**
    *   Dalla seconda riga della matrice: $2 = 1 + (-s_1 + s_5) \implies s_5 = s_1 + 1$.
    *   Dalla quinta riga: $0 = 0 + (s_3 - s_5) \implies s_3 = s_5 = s_1 + 1$.
    *   Dalla terza riga: $0 = 0 + (s_1 - s_3 - s_4) \implies s_4 = s_1 - s_3$.
    *   Sostituendo $s_3$: $s_4 = s_1 - (s_1 + 1) \implies s_4 = -1$.

### Checklist di Validazione
- [ ] Il sistema lineare ammette una soluzione matematica?
- [ ] Tutti i valori del vettore $s$ sono numeri interi?
- [ ] **Vincolo di non-negatività:** Tutti gli elementi di $s$ sono $\geq 0$? 

**Errore Comune:** Dichiarare raggiungibile una marcatura solo perché il sistema è bilanciato. Nel caso sopra citato, poiché $s_4 = -1$, la marcatura deve essere dichiarata formalmente **non raggiungibile**.

## 3. Semantica del Passaggio dei Parametri: Procedure di Valutazione

La corretta interpretazione dell'output di un programma dipende strettamente dalla semantica di passaggio dei parametri. Analizziamo l'evoluzione delle variabili $x$ e $y$ nell'**Exercise 3** (dove $x=1, y=3$ e $p(a, b)$ esegue $a = 2a-b, b = 2b-a, \text{return}(a+b)$).

### Tabella Comparativa dei Risultati

| Semantica | Valore Finale `x` | Valore Finale `y` | Logica Operativa |
| :--- | :---: | :---: | :--- |
| **By Reference** | 10 | 11 | $a$ e $b$ sono alias delle locazioni di memoria originali. Le modifiche sono immediate. |
| **By Copy-in (Value)** | 2 | 6 | Le modifiche avvengono su copie locali. Solo il valore di ritorno aggiorna $x$ o $y$. |
| **By Copy-in Copy-out** | 10 | 11 | I valori locali vengono copiati nuovamente nelle variabili originali solo alla terminazione della procedura. |

**Nota Didattica:** Nella semantica *Copy-in Copy-out*, l'aggiornamento finale produce lo stesso risultato del *By Reference* in questo specifico caso di studio, poiché il meccanismo di "copy-back" riflette le modifiche subite dalle copie locali $a$ e $b$ sulle variabili originali $x$ e $y$ al termine di ogni chiamata.

## 4. Architettura della Memoria e Record di Attivazione

La gestione della memoria a runtime deve seguire una mappatura rigorosa della struttura statica del programma nei Record di Attivazione (AR).

### Workflow di Strutturazione AR (Rif. Exercise 4)
In un sistema con scope statico, ogni AR deve includere:
1.  **Offset 0:** Indirizzo di Ritorno (Return Address).
2.  **Offset 1:** Puntatore Dinamico (Dynamic Pointer - al chiamante).
3.  **Offset 2:** Puntatore Statico (Static Pointer - al contenitore statico).
4.  **Offset Successivi:** Parametri (per indirizzo o valore) e variabili locali.

### Traduzione SimpleSEM
Data l'istruzione in `C`: $x = y + z + a$, con $x$ in $A$, $y$ in $M$, $z$ e $a$ locali a $C$:
*   **Accesso a x:** $d(1, 7) \implies D[D[current + 2] + 7]$
*   **Accesso a y:** $d(2, 4) \implies D[D[D[current + 2] + 2] + 4]$
*   **Accesso a z:** $d(0, 5) \implies D[current + 5]$
*   **Accesso a a:** $d(0, 4) \implies D[current + 4]$

**Comando Completo:**
`D[D[current + 2] + 7] = D[D[D[current + 2] + 2] + 4] + D[current + 5] + D[current + 4]`

## 5. Verifica Dinamica: Workflow dell'Esecuzione Simbolica

L'esecuzione simbolica modella il comportamento del software utilizzando simboli ($\alpha, \beta$) al posto di valori concreti, permettendo di derivare la **Path Condition (PC)**, ovvero il predicato logico che definisce un cammino.

### Procedura Operativa (Rif. Exercise 2)
Per determinare quando lo statement `(**)` viene eseguito, analizziamo i tre cammini possibili:
1.  **PC1 (Cammino 1-2-6-7):** $(a > 0 \wedge b < 0) \wedge (a - b = 2a) \implies a > 0 \wedge b = -a$.
2.  **PC2 (Cammino 1-3-4-6-7):** $\neg(a > 0 \wedge b < 0) \wedge (a \leq 0 \wedge b < 0) \wedge (-(a+b) = -2a) \implies a < 0 \wedge b = a$.
3.  **PC3 (Cammino 1-3-5-6-7):** $\neg(a > 0 \wedge b < 0) \wedge \neg(a \leq 0 \wedge b < 0) \wedge (b - a = a - b) \implies a \geq 0 \wedge b = a$.

**Soluzione Finale:**
La condizione completa è la disgiunzione dei tre predicati:
$$PC_{total} = (a > 0 \wedge b = -a) \vee (b = a)$$

### Identificazione di Loop Infiniti (Endlessness)
L'esecuzione simbolica è uno strumento diagnostico per l'infinità delle esecuzioni. Se, entrando in un ciclo con valori non vincolati, la $PC$ necessaria per l'uscita risulta essere `false`, abbiamo dimostrato formalmente la presenza di un **infinite loop** (Rif. Problema 16).

## 6. Testing Strutturale e Criteri di Copertura

Il testing strutturale non è un'attività casuale, ma richiede la copertura sistematica del grafo di controllo del flusso.

### Risoluzione Problem 4 (Funzione $p(int\ a,\ int\ b)$)
Analizzando il codice, notiamo che $y$ viene inizializzato a $0$ e $x$ assume il valore assoluto della differenza $|a-b|$. Il ciclo `while (x != 0 && y > x)` richiede $0 > |a-b|$, condizione mai verificata per valori reali.

**Test Case per Decision Coverage:**
*   **TC1:** $a = 10, b = 5 \implies$ Copre il ramo `if (a > b)` come *True* e la condizione `while` come *False* (uscita immediata).
*   **TC2:** $a = 5, b = 10 \implies$ Copre il ramo `if (a > b)` come *False* (ramo `else`) e la condizione `while` come *False*.

Questi due test case soddisfano il Decision Coverage poiché forzano ogni ramo decisionale a assumere sia valore vero che falso.

## 7. Logica e Unificazione: Procedura Operativa

L'unificazione è il processo di ricerca di una sostituzione $\sigma$ che renda identici due termini.

### Soluzione Problem 5
1.  **Coppia 1:** $f_1(X, f_2(Z,Y), f_3(Y,b), Z)$ e $f_1(b, W, f_3(a,b), c)$
    *   $X = b$
    *   $Y = a$
    *   $Z = c$
    *   $W = f_2(c, a)$
    *   **Risultato:** Unificabile con $\sigma = \{X/b, Y/a, Z/c, W/f_2(c,a)\}$.

2.  **Coppia 2:** $f_1(Y, f_2(a,Y), f_3(Y,b), a)$ e $f_1(c, f_2(X,a), f_3(a,b), Z)$
    *   $Y = c$
    *   Dalla seconda sotto-espressione: $Y = a$
    *   **Risultato:** Fallimento. La variabile $Y$ non può essere legata contemporaneamente a due costanti distinte ($a$ e $c$).

## 8. Esercizi di Autovalutazione e Soluzioni

1.  **Domanda:** Quando una rete di Petri è definita conservativa?
    *   **Soluzione:** Una rete è strettamente conservativa se la somma dei token in tutti i posti rimane costante per ogni transizione scattata. In termini formali, esiste un vettore di pesi $w > 0$ tale che $w^T \cdot C = 0$.

2.  **Esercizio:** Determinare la Path Condition semplificata per l'esecuzione di `printf("**")` nell'Exercise 2.
    *   **Soluzione:** $PC = (a > 0 \wedge b = -a) \vee (b = a)$.

3.  **Quesito:** Qual è la differenza tra Correctness e Reliability?
    *   **A.** La Correctness è statistica, la Reliability è binaria.
    *   **B.** La Correctness è una qualità assoluta (rispetto alle specifiche), la Reliability è una qualità relativa (comportamento statistico).
    *   **Risposta corretta:** **B**.

## 9. Mini-Riepilogo Finale

> Il passaggio da una programmazione artigianale a una visione ingegneristica è mediato dall'adozione di metodi formali. La gestione rigorosa della memoria attraverso la corretta strutturazione dei Record di Attivazione, l'analisi di raggiungibilità nelle Reti di Petri e la verifica dei cammini tramite Esecuzione Simbolica sono procedure essenziali per mitigare i rischi della "Software Crisis" e garantire la qualità interna ed esterna del prodotto software.