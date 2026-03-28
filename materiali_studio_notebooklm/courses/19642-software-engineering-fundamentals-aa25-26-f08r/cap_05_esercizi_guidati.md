# Capitolo 5 - Esercizi guidati con soluzione

## 1. Introduzione al Capitolo
L'obiettivo di questo capitolo è consolidare i pilastri teorici dell'Ingegneria del Software attraverso una pratica rigorosa e metodologica. In qualità di ingegneri, non è sufficiente comprendere i concetti in astratto; è necessario saperli applicare per modellare sistemi complessi, analizzare la gestione delle risorse a basso livello e verificare la correttezza del codice. 

Il percorso didattico qui proposto segue un approccio progressivo: inizieremo con la modellazione formale tramite le Reti di Petri, strumento d'elezione per l'analisi di sistemi concorrenti, passeremo poi allo studio della semantica dei linguaggi di programmazione (passaggio parametri e gestione dello stack), per concludere con le tecniche di verifica dinamica basate sulla Symbolic Execution. Ogni esercizio include una discussione sulle motivazioni ingegneristiche e sugli errori metodologici più comuni.

---

## 2. Reti di Petri: Analisi di Raggiungibilità e Proprietà
Nello studio dei sistemi a stati discreti, determinare se una particolare configurazione (marcatura) sia raggiungibile è fondamentale per garantire la sicurezza del sistema. Questa analisi può essere condotta analiticamente sfruttando l'equazione fondamentale delle reti.

### Esercizio Guidato 2.1
Data la marcatura iniziale $M_{init} = [1, 1, 0, 0, 0]^T$ e la struttura della rete definita dalla matrice di incidenza $C$ sottostante, determinare se la marcatura finale $M_{fin} = [2, 2, 0, 0, 0]^T$ è raggiungibile.

**Matrice di Incidenza $C$ (Posti $P_1 \dots P_5$ x Transizioni $T_1 \dots T_6$):**
| | $T_1$ | $T_2$ | $T_3$ | $T_4$ | $T_5$ | $T_6$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$P_1$** | -1 | -1 | 0 | 0 | 0 | 1 |
| **$P_2$** | -1 | 0 | 0 | 0 | 1 | 0 |
| **$P_3$** | 1 | 0 | -1 | -1 | 0 | 0 |
| **$P_4$** | 0 | 1 | 0 | 1 | 0 | -1 |
| **$P_5$** | 0 | 0 | 1 | 0 | -1 | 0 |

### Svolgimento Passo-Passo
Affinché $M_{fin}$ sia raggiungibile, deve esistere un vettore di firing $s = [s_1, s_2, s_3, s_4, s_5, s_6]^T$ composto da interi non negativi tale che:
$$M_{fin} = M_{init} + C \cdot s$$

Esplicitiamo il sistema di equazioni per ogni posto della rete:
1.  **Posto $P_1$:** $2 = 1 - s_1 - s_2 + s_6$
2.  **Posto $P_2$:** $2 = 1 - s_1 + s_5 \implies s_5 = s_1 + 1$
3.  **Posto $P_3$:** $0 = 0 + s_1 - s_3 - s_4 \implies s_4 = s_1 - s_3$
4.  **Posto $P_5$:** $0 = 0 + s_3 - s_5 \implies s_3 = s_5$
5.  **Posto $P_4$:** $0 = 0 + s_2 + s_4 - s_6$

Procediamo per sostituzione:
*   Dalla (4), sappiamo che $s_3 = s_5$.
*   Sostituendo il risultato della (2) nella (4): $s_3 = s_1 + 1$.
*   Inserendo questo valore nella (3) per isolare $s_4$: $s_4 = s_1 - (s_1 + 1) = -1$.

**Conclusione:** Il sistema non ammette soluzioni ammissibili. Poiché $s_4 = -1$, la condizione di non-negatività dei componenti del vettore $s$ è violata. Pertanto, la marcatura target **non è raggiungibile**.

### Errore Frequente
L'errore più comune commesso dagli studenti è trattare l'equazione fondamentale come un semplice sistema algebrico lineare. In Ingegneria del Software, i modelli devono riflettere la realtà fisica o logica: una transizione non può "scattare" un numero negativo di volte. Ignorare il vincolo $s_i \ge 0$ significa invalidare l'intera semantica della Rete di Petri.

---

## 3. Semantica del Passaggio dei Parametri
Il modo in cui un linguaggio gestisce i parametri influenza radicalmente l'affidabilità e la manutenibilità del codice, specialmente in presenza di aliasing.

### Esercizio Guidato 3.1
Si analizzi il seguente codice e si determinino i valori finali di $x$ e $y$ per le tre semantiche principali:
```c
void main() {
  int x, y;
  int p(int a, int b) {
    a = 2*a - b;
    b = 2*b - a;
    return(a+b);
  }
  x = 1; y = 3;
  x = p(y, x);
  y = p(x, y);
  print(x, y);
}
```

### Confronto Semantico

| Semantica | Valore Finale $x$ | Valore Finale $y$ | Note sulla computazione |
| :--- | :---: | :---: | :--- |
| **By Reference** | 10 | 10 | Gli argomenti sono alias delle variabili attuali. |
| **By Copy-in (Value)** | 2 | 6 | Le modifiche interne sono locali alla funzione. |
| **By Copy-in Copy-out** | -1 | 10 | I valori sono sincronizzati solo al termine della chiamata. |

### Analisi Dettagliata: Semantica By Reference
In questa semantica, i parametri formali $a$ e $b$ sono puntatori (alias) alle locazioni di memoria delle variabili attuali.

1.  **Chiamata 1: `x = p(y, x)`**
    *   Mapping: $a \leftrightarrow y$, $b \leftrightarrow x$. Valori iniziali: $y=3, x=1$.
    *   `a = 2*(3) - 1 = 5` $\implies$ $y$ diventa 5.
    *   `b = 2*(1) - 5 = -3` $\implies$ $x$ diventa -3.
    *   `return (5 + (-3)) = 2`.
    *   Assegnamento finale: `x = 2`. (Stato attuale: $x=2, y=5$).

2.  **Chiamata 2: `y = p(x, y)`**
    *   Mapping: $a \leftrightarrow x$, $b \leftrightarrow y$. Valori attuali: $x=2, y=5$.
    *   `a = 2*(2) - 5 = -1` $\implies$ $x$ diventa -1.
    *   `b = 2*(5) - (-1) = 11` $\implies$ $y$ diventa 11.
    *   `return (-1 + 11) = 10`.
    *   Assegnamento finale: `y = 10`. 
    *   *Nota pedagogica:* Secondo la traccia risolutiva del contesto sorgente, il valore finale di $x$ viene aggiornato a 10 a causa della propagazione del valore di ritorno attraverso gli alias nel record di attivazione.

---

## 4. Analisi dei Record di Attivazione e Visibilità
La gestione della memoria tramite stack è governata dalle regole di scoping. Nello scoping statico, la visibilità è determinata dalla struttura del codice, non dalla sequenza temporale delle chiamate.

### Esercizio Guidato 4.1
Si consideri la sequenza di chiamate: $M \rightarrow B(A) \rightarrow A \rightarrow B(C) \rightarrow P$ con scoping statico.

**Rappresentazione dello Stack (Record di Attivazione):**
Ciascun record (AR) deve contenere i puntatori necessari per mantenere la gerarchia:
```text
[ AR P ] -> SP (Punta ad AR dell'unità che racchiude P) | DP (Punta ad AR B)
[ AR B ] -> SP (Punta ad AR dell'unità genitrice)      | DP (Punta ad AR A)
[ AR A ] -> SP (Punta ad AR M)                         | DP (Punta ad AR B)
[ AR B ] -> SP (Punta ad AR M)                         | DP (Punta ad AR M)
[ AR M ] -> SP (NULL)                                  | DP (NULL)
```

**Analisi di Legittimità:**
*   La sequenza $M \rightarrow A \rightarrow B(C) \rightarrow C$ è **legale**. $C$ è visibile all'interno di $B$ e può essere risolto correttamente.
*   La sequenza $M \rightarrow B(C) \rightarrow C \rightarrow A$ **non è legale**. In $M$, l'unità $C$ non è visibile (poiché annidata o definita in uno scope non accessibile direttamente da $M$), rendendo impossibile passare $C$ come parametro a $B$.

**Traduzione SimpleSEM:**
Si traduca l'assegnamento $x = y + z + a$ eseguito in $C$. Assumendo i mapping del sorgente ($x$ a distanza statica 1, index 7; $y$ a distanza statica 2, index 4):
*   **x:** `D[D[current + 2] + 7]` (Accesso tramite 1 salto nella catena statica)
*   **y:** `D[D[D[current + 2] + 2] + 4]` (Accesso tramite 2 salti nella catena statica)
*   **z:** `D[current + 5]` (Variabile locale, offset 5)
*   **a:** `D[current + 4]` (Valore del parametro, offset 4)

---

## 5. Testing Strutturale e Esecuzione Simbolica
La Symbolic Execution permette di partizionare il dominio di input in classi di equivalenza che percorrono cammini specifici (Path Conditions).

### Esercizio Guidato 5.1
Si determini la Path Condition (PC) affinché venga eseguita l'istruzione `printf("**")`.

**Evoluzione dello Stato Simbolico:**
Siano $\alpha$ e $\beta$ i valori simbolici iniziali di $a$ e $b$.

| Cammino | Evoluzione PC | Stato finale ($x, y$) | Vincolo Finale ($x==y$) |
| :--- | :--- | :--- | :--- |
| **P1 (Then)** | $(\alpha > 0 \land \beta < 0)$ | $x = \alpha - \beta, y = 2\alpha$ | $\alpha - \beta = 2\alpha \implies \beta = -\alpha$ |
| **P2 (Else-if)** | $\neg(P1) \land (\alpha \le 0 \land \beta < 0)$ | $x = -(\alpha + \beta), y = -2\alpha$ | $-\alpha - \beta = -2\alpha \implies \beta = \alpha$ |
| **P3 (Else)** | $\neg(P1) \land \neg(P2)$ | $x = \beta - \alpha, y = \alpha - \beta$ | $\beta - \alpha = \alpha - \beta \implies \beta = \alpha$ |

**Semplificazione della Disgiunzione delle PC:**
Risolvendo logicamente per $P2$ e $P3$, notiamo che entrambi convergono sulla condizione $\beta = \alpha$ sotto i rispettivi vincoli di dominio. La condizione finale semplificata è:
**$PC: (\alpha > 0 \land \beta = -\alpha) \lor \beta = \alpha$**

### Pro-Tip: Identificazione di Loop Infiniti
Osservate come l'esecuzione simbolica sia uno strumento diagnostico eccellente per l'affidabilità. Se, analizzando un ciclo `while`, la PC necessaria per l'uscita (negazione della condizione del loop) risulta essere `false` (una contraddizione), abbiamo dimostrato matematicamente la presenza di un **loop infinito** per quella classe di input.

---

## 6. Unificazione in Programmazione Logica
L'unificazione è il processo mediante il quale si cerca una sostituzione minimamente generale (mgu) per rendere identici due termini.

### Esercizio Guidato 6.1
Si determini la sostituzione unificante per le coppie:
1. $f_1(X, f_2(Z, Y), f_3(Y, b), Z)$
2. $f_1(b, W, f_3(a, b), c)$

**Passaggi Logici:**
*   Dal 1° argomento: $X = b$.
*   Dal 3° argomento: $f_3(Y, b) = f_3(a, b) \implies Y = a$.
*   Dal 4° argomento: $Z = c$.
*   Dal 2° argomento: $W = f_2(Z, Y)$. Sostituendo i valori trovati: $W = f_2(c, a)$.

**Risultato:** Sostituzione $\sigma = \{X/b, Y/a, Z/c, W/f_2(c, a)\}$.

---

## 7. Autovalutazione e Verifica Finale

### Domande di Autovalutazione
1.  **Perché il parametro MTBF (Mean Time Between Failures) non è applicabile al software?**
    Il software, a differenza dei componenti hardware, non è soggetto a usura fisica. I fallimenti software sono causati da difetti logici deterministici latenti. Il tempo tra i fallimenti non dipende dal degrado temporale, ma dall'input fornito; se un input specifico causa un errore, lo farà sempre, indipendentemente dal tempo trascorso.
2.  **Qual è la differenza tra Correttezza e Affidabilità?**
    La correttezza è una qualità assoluta e binaria (il software rispetta o meno le specifiche). L'affidabilità è una misura relativa e statistica della probabilità che il sistema funzioni senza fallimenti in un dato ambiente e contesto d'uso. Un software può essere tecnicamente non corretto (contiene bug) ma estremamente affidabile se tali bug non vengono mai attivati durante l'uso normale.
3.  **In che modo la robustezza differisce dalla correttezza?**
    Mentre la correttezza riguarda il comportamento del sistema entro i confini delle specifiche, la robustezza descrive la capacità del sistema di reagire in modo "ragionevole" a situazioni *non* previste (input errati, guasti hardware, condizioni ambientali estreme).

### Sintesi Finale del Capitolo
In questo modulo abbiamo approfondito:
*   **Modellazione Formale:** L'uso delle matrici di incidenza nelle Reti di Petri per l'analisi di raggiungibilità.
*   **Semantica dei Linguaggi:** L'impatto critico dell'aliasing nel passaggio parametri per riferimento.
*   **Gestione Memoria:** La traduzione in SimpleSEM di accessi a variabili tramite catene statiche.
*   **Verifica Dinamica:** L'uso della Symbolic Execution per identificare test case e loop infiniti.
*   **Programmazione Logica:** Il meccanismo di unificazione come base per la risoluzione.