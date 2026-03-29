# Capitolo 7 - Errori frequenti e ripasso

In qualità di esperti in *English for Computer Science* e Technical Writing Accademico, è essenziale riconoscere che la comunicazione scientifica non è semplicemente una questione di traduzione, ma di aderenza a rigorose convenzioni retoriche e grammaticali. Questo capitolo sintetizza le competenze necessarie per redigere abstract efficaci, gestire i gradi di certezza e padroneggiare le strutture sintattiche complesse richieste nel panorama informatico internazionale.

---

## 1. Analisi Critica dell'Abstract: Errori di Struttura e "Moves"

L'abstract non è un'introduzione, ma una sintesi autoportante dell'intero articolo. Per essere efficace, deve riflettere l'anatomia del paper scientifico (IMReD):
*   **Abstract:** Sintesi dell'intero lavoro in un unico paragrafo.
*   **Introduction:** Definizione dello scopo, dal contesto generale alla tesi specifica.
*   **Materials & Methods:** Descrizione dell'esecuzione dell'esperimento o della ricerca.
*   **Results:** Presentazione oggettiva dei dati e dei risultati chiave.
*   **Discussion:** Interpretazione dei risultati e confronto con la letteratura esistente.
*   **Conclusion:** Rafforzamento dei claim principali e rilevanza oltre lo studio specifico.

### Il Modello Swales & Feak (4 "Moves")
Un abstract accademico segue una sequenza logica di "mosse" comunicative. È fondamentale notare che, statisticamente, l'abstract di **Computer Studies** è più denso rispetto ad altre discipline (media di **9.6 frasi** e **232 parole**, contro le 7.9 frasi e 196 parole della Biologia).

1.  **Introduction (Motivation/Problem):** Identifica l'importanza del problema e il "gap" scientifico.
2.  **Methods (Procedure):** Descrive l'approccio e il design sperimentale.
3.  **Results (Findings):** La sezione solitamente **più lunga dell'abstract**. Riporta cosa è stato imparato o creato.
4.  **Conclusion (Implications):** Spiega il valore dei risultati e le inferenze per il contesto più ampio.

### Tipi di frasi di apertura
L'errore più comune è omettere lo scopo (*Purpose*) o il problema. Esistono quattro approcci standard per iniziare:
*   **(A) Fenomeno del mondo reale:** "Corporate taxation rates vary around the world."
*   **(B) Scopo o Obiettivo:** "The aim of this study is to examine the effects of..."
*   **(C) Azione del ricercatore:** "The paper analyses corporate taxation returns before and after..."
*   **(D) Problema o Incertezza:** "The relationship between corporate taxation and corporate strategy remains unclear."

### Pratica Corretta vs. Errore Frequente

| Caratteristica | Pratica Corretta | Errore Frequente |
| :--- | :--- | :--- |
| **Lunghezza** | 150-250/300 parole (Media CS: 232). | Sotto le 150 o sopra le 300 parole. |
| **Formattazione** | Paragrafo unico, Times New Roman 12, interlinea singola. | Più paragrafi, font non standard, interlinea doppia. |
| **Sequenza** | Sequenza logica IMReD (Moves 1-4). | Informazioni fuori ordine (es. conclusioni prima dei metodi). |
| **Elementi Extra** | Citazioni omesse; Acronimi definiti al primo uso. | Uso di citazioni estese o acronimi non definiti (es. NSA, NHS). |

---

## 2. Anti-pattern Linguistici: Tempi Verbali e Registro Accademico

In Informatica, la scelta del tempo verbale segue regole di genere testuale precise.

### Convenzioni sui Tempi Verbali
*   **Present Tense:** Si utilizza per il **Genre-name**, ovvero quando ci si riferisce al paper stesso come entità (es. *"This paper presents a new algorithm..."* o *"This study examines..."*).
*   **Past Tense:** Si utilizza per il **Type of Investigation**, ovvero l'esperimento o l'analisi specifica condotta (es. *"The purpose of this experiment was to measure..."*). Nelle scienze della vita e della salute, vi è una preferenza generale per il passato, ma in CS il presente è molto comune per descrivere funzionalità software.

### Registro e Voce Passiva
L'uso della prima persona (*I/We*) è accettabile in alcuni contesti per indicare l'azione del ricercatore, ma la mossa dei **Methods** ha una probabilità estremamente alta di utilizzare il **passivo** e il **passato** (*"Data were generated from..."*) per mantenere l'oggettività.

**Trasformazione da stile informale a formale:**
*   *Informale:* "What about expanding the role of the department?"
*   *Accademico:* "I propose expanding the role of the department" oppure "It is recommended that the department's role be expanded."

---

## 3. Guida alla Speculazione: Modali e Gradi di Certezza

Esprimere la probabilità corretta evita claim eccessivi (*overstatement*).

### Scala di Intensità e Funzioni (Modality)

| Modale | Funzione Accademica |
| :--- | :--- |
| **Might** | Possibilità debole / cautela estrema. |
| **Could / May** | Possibilità generale. |
| **Would** | Situazione ipotetica. |
| **Should** | **Confident Assumption** (assunzione basata su piani/aspettative). |
| **Will** | **Firm Prediction** (previsione ferma basata su dati certi). |
| **Must** | **Confident Conclusion** (unica spiegazione logica possibile). |

### Speculazione sul Passato
Per deduzioni su eventi conclusi, la struttura è **Modal + Have + Past Participle**:
*   *Deduzione logica:* "The database **must have been** compromised" (Sono certo che sia successo).
*   *Possibilità:* "The network failure **could have resulted** from congestion" (È una spiegazione probabile).
*   *Rimpianto/Obbligo mancato:* "The developers **should have tested** the modules" (Non lo hanno fatto).

---

## 4. Masterizzazione dei Condizionali nel Contesto IT

### Le tre strutture fondamentali
1.  **First Conditional (Reale):** *If + Present, will + base form*.
    *   "If the server temperature exceeds 70°C, the system **will crash**."
2.  **Second Conditional (Ipotetico):** *If + Past Simple, would + base form*.
    *   "If we **used** a Python-based solution, the integration **would** be easier."
3.  **Third Conditional (Hypothetical Past):** *If + Past Perfect, would have + Past Participle*.
    *   "If we **had preprocessed** the data, the model **would have been** more accurate." (Opportunità mancata).

### Alternative a "If" e Trasformazioni Nominali
Oltre a connettivi come *unless* (if not) o *as long as* (a patto che), il registro accademico avanzato preferisce l'uso di **sintagmi nominali** per esprimere condizioni:
*   *Frase con If:* "If the government lowers the limit, lives will be saved."
*   *Trasformazione Nominale:* "**A move to lower the limit** would save lives."
In questo caso, il sostantivo "move" (o "failure", "decision") incapsula la condizione, rendendo il tono più formale e conciso.

---

## 5. Esercizi di Consolidamento (Sentence Transformation)

1.  Experts believe that quantum computing will transform encryption. (IS)
    *   **Quantum computing is believed to transform** encryption. *(Passivo impersonale)*.
2.  The developers should have tested all modules before release. (BEEN)
    *   **All the modules should have been tested** before release. *(Modale del passato al passivo)*.
3.  The algorithm cannot process the dataset without sufficient RAM. (IF)
    *   **The algorithm can process the dataset if there is sufficient** RAM. *(Condizionale)*.
4.  I am certain the programmers implemented protocols. (HAVE)
    *   **The programmers must have implemented** protocols. *(Confident conclusion sul passato)*.
5.  It is possible that network latency resulted from congestion. (LIKELY)
    *   **The network latency is likely to have resulted** from congestion. *(L'uso di "Likely" con evento passato richiede l'infinito passato "to have + participio")*.
6.  The engineer regrets not implementing unit tests. (WISHES)
    *   **The engineer wishes he had implemented** unit tests. *(Wishes + Past Perfect per rimpianti passati)*.
7.  Massive investments were made, but data breaches still occur. (DESPITE)
    *   **Despite massive investments** in cybersecurity, breaches still occur. *(Connettivo concessivo)*.
8.  Cloud services are used by corporations; start-ups use them too. (NOT ONLY)
    *   **Not only are cloud services used by corporations, but** start-ups also rely on them. *(Inversione enfatica)*.
9.  The team optimized queries; consequently, response time decreased. (DECREASE)
    *   After optimization, **there was a dramatic decrease in** response time. *(Nominalizzazione)*.
10. The researchers will complete the module by early July. (HAVE)
    *   **The researchers will have completed** the module by early July. *(Future Perfect per scadenze)*.

---

## 6. Case Study: Analisi del Cyber-Attack (WannaCry)

L'attacco del 2017 ha evidenziato falle critiche nella gestione della sicurezza globale.

### Vocabolario Tecnico e Verbi Accademici
*   **Wake-up call:** Avvertimento per un'azione correttiva.
*   **Flaw / Fault:** Debolezza o errore nel software (es. *exploit a flaw identified by US intelligence*).
*   **Vulnerable:** Esposto a rischi.
*   **Ransomware:** Malware che cripta i dati richiedendo un riscatto (*ransom*).
*   **Treat (Verb):** Gestire o considerare una situazione (es. *treat the attack as a wake-up call*).
*   **Blame (Verb):** Attribuire la responsabilità (es. *Microsoft blamed governments for storing data*).
*   **Restore (Verb):** Ripristinare (es. *restore the computer to its original settings*).

### Analisi dei Fatti (Vero/Falso)
1.  **Vero:** Una falla in un programma Microsoft è stata sfruttata dagli hacker (falla identificata dalla NSA).
2.  **Falso:** Microsoft si è assunta la responsabilità (Ha criticato i governi per la conservazione delle falle e gli utenti per non aver aggiornato i sistemi).
3.  **Falso:** La Cina ha riportato pochi casi (Oltre 29.000 istituzioni sono state infettate).

---

## 7. Strategia di Ripasso Finale e Checklist

### Checklist dell'Abstract (Revisione Pre-consegna)
*   [ ] Ho incluso tutti i 4 move (Introduction, Methods, Results, Conclusion)?
*   [ ] Il move dei **Results** è la sezione più dettagliata e lunga?
*   [ ] Ho definito tutti gli acronimi (es. NSA, NHS) alla prima menzione?
*   [ ] Ho rispettato il limite di parole (obiettivo ~230 per Computer Science)?
*   [ ] Ho utilizzato il font Times New Roman 12 con interlinea singola?

### Strategia Grammaticale
*   **Identificazione del Tempo:** Se descrivo il paper, uso il *Present Tense*. Se descrivo l'esperimento, uso il *Past Tense*.
*   **Gestione dell'Incertezza:** Usa *Might* per suggerimenti cauti; evita *Will* a meno che non ci sia certezza assoluta.
*   **Condizionali:** Usa il **Third Conditional** (*If + Past Perfect*) esclusivamente per scenari passati ipotetici che non si sono verificati.

La precisione nella struttura dei "Moves" e l'accuratezza nell'uso dei modali definiscono la qualità della produzione scientifica. La padronanza di questi strumenti è il requisito minimo per la pubblicazione in ambito Computer Science.