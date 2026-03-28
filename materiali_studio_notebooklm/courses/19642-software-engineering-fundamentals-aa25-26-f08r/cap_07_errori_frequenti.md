# Capitolo 7 - Errori frequenti e ripasso

Il presente capitolo analizza le criticità metodologiche riscontrate nell'applicazione dei principi di Ingegneria del Software, con l'obiettivo di trasformare l'errore in uno strumento di apprendimento. La trattazione segue un rigore accademico focalizzato sulla prevenzione di fallimenti logici nella modellazione e verifica dei sistemi.

---

## 1. Analisi delle Reti di Petri: Errori di Raggiungibilità e Conservatività

L'analisi formale delle Reti di Petri si fonda sull'equazione fondamentale dello stato. Un errore sistematico degli studenti consiste nel trattare tale equazione come un mero sistema algebrico, ignorando i vincoli semantici del modello.

### 1.1. Identificazione degli Errori Metodologici

L'equazione fondamentale è definita come:
$$m_{Fin} = m_{Init} + C \cdot s$$
dove $C$ è la matrice di incidenza e $s$ è il vettore di sparo (firing vector). 

**L'Anti-pattern del Vettore di Sparo Negativo**
Il vettore $s$ rappresenta il numero di occorrenze di ogni transizione nella sequenza che porta da $m_{Init}$ a $m_{Fin}$. Ne consegue che ogni componente $s_i$ deve soddisfare il vincolo di non-negatività ($s_i \in \mathbb{N}$). Ignorare questo vincolo porta a conclusioni errate sulla raggiungibilità.

| Assunzione Errata | Verifica Rigorosa |
| :--- | :--- |
| L'esistenza di una soluzione algebrica al sistema $C \cdot s = \Delta m$ garantisce la raggiungibilità. | La raggiungibilità è garantita solo se esiste una sequenza di sparo ammissibile tale che ogni $s_i \ge 0$. |
| La conservatività è una proprietà dei token nel marking corrente. | La conservatività è una proprietà strutturale. Una rete è conservativa se esiste un vettore di pesi $y > 0$ tale che $y^T \cdot C = 0$. |

### 1.2. Esercizio Pratico: Analisi dello Stato (Source 2024-01-10)
Si consideri la rete caratterizzata dalla seguente matrice di incidenza $C$:

$$C = \begin{pmatrix} -1 & -1 & 0 & 0 & 0 & 1 \\ -1 & 0 & 0 & 0 & 1 & 0 \\ 1 & 0 & -1 & -1 & 0 & 0 \\ 0 & 1 & 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 0 & -1 & 0 \end{pmatrix}$$

Dato il marking iniziale $m_{Init} = [1, 1, 0, 0, 0]^T$, si verifichi la raggiungibilità di $m_{Fin} = [2, 2, 0, 0, 0]^T$.

**Passaggi Algebrici:**
Risolvendo $m_{Fin} - m_{Init} = C \cdot s$, otteniamo il sistema:
1.  $s_6 - s_1 - s_2 = 1$
2.  $s_5 - s_1 = 1 \implies s_5 = s_1 + 1$
3.  $s_1 - s_3 - s_4 = 0 \implies s_4 = s_1 - s_3$
4.  $s_2 + s_4 - s_6 = 0$
5.  $s_3 - s_5 = 0 \implies s_3 = s_5 = s_1 + 1$

Sostituendo $s_3$ nella (3):
$$s_4 = s_1 - (s_1 + 1) = -1$$

**Conclusione Tecnica:** Poiché $s_4 = -1$, il marking $m_{Fin}$ è **irraggiungibile**. Non è possibile sparare la transizione $T_4$ un numero negativo di volte.

---

## 2. Semantica del Passaggio dei Parametri: Confronti e Trappole

Il comportamento di un sistema è strettamente dipendente dalla semantica di legame tra parametri attuali e formali. Il rischio principale è il **Double-Aliasing**, dove più nomi si riferiscono alla stessa area di memoria.

### 2.1. Analisi Comparativa delle Semantiche
Si analizzi il seguente frammento di codice (Source 2024-01-10, Ex 3):
```c
void main() {
    int x, y;
    int p(int a, int b) {
        a = 2*a - b;
        b = 2*b - a;
        return(a+b);
    }
    x = 1; y = 3;
    x = p(y, x); // Chiamata 1
    y = p(x, y); // Chiamata 2
}
```

*   **By Reference:** I parametri `a` e `b` diventano alias delle variabili passate. Le modifiche sono istantanee.
*   **By Copy-in Copy-out:** I valori vengono copiati all'ingresso e sovrascritti all'uscita. Se si passa la stessa variabile a più parametri, l'ordine di copia finale determina il valore definitivo (potenziale punto di fallimento).

### 2.2. Tabella di Tracciamento Completa (Trace Table)

| Semantica | Stato post Chiamata 1 | Stato post Chiamata 2 | Valori Finali |
| :--- | :--- | :--- | :--- |
| **Reference** | $x=2, y=5$ | $x=-1, y=10$ | $x=-1, y=10$ |
| **Copy-in** | $x=2, y=3$ | $x=2, y=6$ | $x=2, y=6$ |
| **Copy-in/out** | $x=2, y=5$ | $x=2, y=5$ | $x=2, y=5$ |

**Alert Tecnico:** Nella semantica *By Reference* della Chiamata 1, `a` è alias di `y` e `b` è alias di `x`. Quando `a` viene aggiornato ($a = 2 \cdot 3 - 1 = 5$), `y` cambia immediatamente. Quando `b` viene aggiornato ($b = 2 \cdot 1 - 5 = -3$), `x` cambia immediatamente. Il valore di ritorno $a+b = 2$ viene infine assegnato a $x$, portando a $x=2, y=5$.

---

## 3. Struttura della Memoria e Record di Attivazione

La corretta gestione della memoria richiede la distinzione tra gerarchia di chiamata e gerarchia di visibilità.

### 3.1. Puntatori Statici vs Dinamici
L'errore tipico è confondere il **Puntatore Dinamico** (catena di chiamate, punta al record del chiamante) con il **Puntatore Statico** (scoping, punta al record dell'ambiente di definizione).

**Regola di Visibilità:** In uno scoping statico, una procedura può accedere solo alle variabili definite nel suo scope o negli scope che la contengono.
*   *Sequenza illegale (Ex 4):* `M -> B(C) -> C -> A`. Risulta illegale perché `C` non è visibile a `M`, impedendo a `M` di passarla come parametro a `B`.

### 3.2. Traduzione in SimpleSEM (Source 2024-01-10, Ex 4)
Si consideri l'istruzione `x = y + z + a` all'interno della procedura `C`. Basandoci sulla struttura degli AR fornita:
- `current`: AR di `C`.
- `D[current + 2]`: Puntatore Statico di `C` (punta ad AR di `B`).
- `D[D[current + 2] + 2]`: Puntatore Statico di `B` (punta ad AR di `A`).
- `D[D[D[current + 2] + 2] + 2]`: Puntatore Statico di `A` (punta ad AR di `M`).

**Traduzione Rigorosa:**
- `x` (in `A`, offset 7): `D[D[D[current + 2] + 2] + 7]`
- `y` (in `M`, offset 4): `D[D[D[D[current + 2] + 2] + 2] + 4]`
- `z` (locale in `C`, offset 5): `D[current + 5]`
- `a` (parametro in `C`, offset 4): `D[current + 4]`

Formula: `D[D[D[current + 2] + 2] + 7] = D[D[D[D[current + 2] + 2] + 2] + 4] + D[current + 5] + D[current + 4]`

---

## 4. Verifica e Validazione: Symbolic Execution e Test Case

### 4.1. Path Conditions e Cicli Infiniti
L'esecuzione simbolica trasforma il programma in un insieme di formule logiche. Un cammino è **infattibile** se la sua Path Condition ($PC$) è una contraddizione ($false$).

Si consideri l'analisi di un ciclo `while`: se $PC_{new} = PC_{old} \land Condition$ e l'uscita richiede $PC_{old} \land \neg Condition$, ma entrambe portano a una contraddizione logica, il ciclo è infinito.
*Esempio:* Se $PC$ implica $a > b$ e la condizione di uscita è $a \le b$, allora $a > b \land a \le b \equiv false$. L'uscita è logicamente impossibile.

### 4.2. Esercizio di Copertura: Decision Coverage (Source 2021-09-15)
Data la funzione `void p(int a, int b)` con rami `if (a > b)` e `while (x != 0 && y > x)`:

**Test Case Set (Minimo):**
1.  **TC1:** $a=10, b=5$. Percorre il ramo `then` dell'if. Calcola $x=5, y=0$. La condizione `while` ($5 \ne 0 \land 0 > 5$) è `false`. Copre i rami (If-True, While-False).
2.  **TC2:** $a=5, b=10$. Percorre il ramo `else` dell'if. Calcola $x=5, y=0$. La condizione `while` è `false`. Copre il ramo (If-False).

**Domanda di Autovalutazione:** Il set soddisfa la *Condition Coverage*?
**Risposta:** No. La Condition Coverage richiede che ogni componente atomica della decisione (`x != 0` e `y > x`) sia valutata sia come `true` che come `false`. Nei TC sopra, `y > x` non è mai `true`.

---

## 5. Qualità del Software: Definizioni e Distinzioni Cruciali

### 5.1. Correttezza vs Affidabilità
La distinzione tra queste due qualità è fondamentale per la gestione del rischio:
*   **Correttezza (Logica):** Proprietà assoluta (Sì/No). Un software è corretto se e solo se rispetta integralmente le specifiche.
*   **Affidabilità (Statistica):** Proprietà relativa. Misura la probabilità che il sistema funzioni senza guasti in un tempo dato (correlata al Mean Time Between Failures - MTBF). Un software non corretto può essere comunque affidabile se i suoi bug si presentano raramente.

### 5.2. L'Ingegneria e la "Crisi del Software"
La **Software Crisis** (1968) nacque dalla consapevolezza che il "Good Programming" non scala verso i "Good Systems". Il software è caratterizzato dalla **Morbidezza (Softness)**: è facile da modificare fisicamente (basta un editor), ma estremamente difficile da modificare correttamente senza un approccio ingegneristico che ne valuti le dipendenze.

---

## 6. Strategia di Ripasso Finale e Check-list

### 6.1. Mini-Riepilogo Concettuale

| Area | Errore Critico | Azione Correttiva |
| :--- | :--- | :--- |
| **Petri** | Accettare $s_i < 0$ | Verificare la non-negatività di ogni componente di $s$. |
| **Parametri** | Ignorare l'aliasing | Tracciare ogni alias come puntatore alla stessa cella. |
| **SimpleSEM** | Sbagliare i livelli di $D[...]$ | Contare i salti nel puntatore statico (catena statica). |
| **V&V** | Testare solo cammini "felici" | Calcolare la PC per identificare cammini infattibili. |

### 6.2. Autovalutazione (Self-Diagnostic)
1.  Cosa indica una componente negativa nel vettore di sparo $s$?
2.  In quale semantica di passaggio dei parametri le modifiche sono differite al termine della procedura?
3.  Il puntatore statico punta sempre all'AR del chiamante?
4.  La robustezza può essere definita formalmente in assenza di requisiti specifici?
5.  Qual è la differenza principale tra produzione software e produzione industriale (es. automobili)?

### 6.3. Chiave delle risposte
1. *Indica l'irraggiungibilità del marking finale.*
2. *By Copy-in Copy-out (o Copy-back).*
3. *No, quello è il puntatore dinamico. Il statico punta all'ambiente di definizione.*
4. *No, è una qualità soggettiva se non formalizzata come requisito di correttezza.*
5. *Nel software, il costo di produzione della singola copia fisica è nullo; tutto il costo risiede nel design.*