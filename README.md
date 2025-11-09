#  Air Quality Dashboard (Flask + Nuxt + Tailwind 4)

Una web app moderna per visualizzare la qualità dell’aria in tempo reale da diverse stazioni di monitoraggio.  
Il backend è basato su **Flask (Python)** e funge da proxy per l’API ufficiale di [ZeroC Green](https://api.zeroc.green), mentre il frontend è costruito con **Nuxt 4 + Tailwind CSS v4** per un’interfaccia elegante e reattiva.

---

##  Funzionalità principali

-  Recupero dinamico delle stazioni via API Flask (`/api/stations`)
-  Dettaglio stazione con metriche e medie ponderate
-  Interfaccia responsive e colorata con Tailwind CSS v4
-  Calcolo e visualizzazione indicatore AQI (qualità dell’aria)
-  Routing client-side con Nuxt

-------------------------------------------------------------------------------------------
## Cos’è la “media ponderata” e perché serve?

Calcolo della media ponderata

Il backend (Flask) calcola per ogni metrica una media ponderata sugli ultimi 7 giorni con dati validi,
escludendo quelli con sample_size = 0.
Questo garantisce un valore più rappresentativo e affidabile della qualità dell’aria.

Formula

weighted_average = (Σ (average × sample_size)) / (Σ sample_size)

Esempio visivo:


| Giorno | Average | Sample Size | Considerato nel calcolo? | Prodotto (average × sample_size) |
| :----- | :------ | :---------- | :----------------------- | :------------------------------- |
| 25/10  | 12.0    | 200         |  Sì                      | 2400                             |
| 26/10  | 8.0     | 180         |  Sì                      | 1440                             |
| 27/10  | 0.0     | 0           |  No (nessun campione)    | —                                |
| 28/10  | 10.0    | 220         |  Sì                      | 2200                             |
| 29/10  | 7.0     | 150         |  Sì                      | 1050                             |
| 30/10  | 0.0     | 0           |  No (nessun campione)    | —                                |
| 31/10  | 9.0     | 190         |  Sì                      | 1710                             |

Calcolo effettivo

weighted_average = (2400 + 1440 + 2200 + 1050 + 1710) / (200 + 180 + 220 + 150 + 190)
weighted_average = 8800 / 940 = 9.36

Risultato finale → weighted_avg = 9.36



Gestione dei casi limite


| Situazione                 | Cosa fa il backend              | Cosa mostra il frontend         |
| :------------------------- | :------------------------------ | :------------------------------ |
| Tutti i `sample_size = 0`  | `weighted_avg = None`           | “n/d” (non disponibile)         |
| Meno di 7 giorni validi    | Calcolo sui giorni disponibili  | Media reale sui giorni validi   |
| Valori parziali o mancanti | Giorni con `0` o `None` esclusi | Nessuna distorsione nel calcolo |


Beneficio
Questa strategia evita che giornate incomplete o senza campioni influenzino la media.
Il risultato rappresenta solo i giorni effettivamente misurati, rendendo il dato finale più realistico e affidabile



##  Struttura del progetto

Tecnologie usate
Componente	Tecnologia
Frontend	Nuxt 4, Vue 3, Tailwind CSS 4
Backend	Flask (Python)
API Source	ZeroC Green – Public API

Build Tools	Vite, PostCSS, Autoprefixer

##  Architettura del progetto: Flask + Nuxt

Questo progetto è costruito su un’architettura **Full Stack moderna** che combina la semplicità di **Flask (Python)** con la potenza di **Nuxt (Vue.js)**.  
Le due parti sono separate ma comunicano tramite API REST, garantendo un sistema modulare, scalabile e facilmente manutenibile.

###  Perché Flask lato backend
- **Semplice e leggero:** Flask è un microframework Python perfetto per creare API RESTful senza eccessiva complessità.
- **Proxy sicuro:** il backend funge da ponte tra il frontend e l’API pubblica di [ZeroC Green](https://api.zeroc.green), proteggendo le chiamate e gestendo eventuali errori o timeout.
- **Facile integrazione:** con Flask è immediato aggiungere logica di elaborazione (es. calcolo di medie ponderate o filtri sui dati).
- **Python ecosystem:** permette di sfruttare librerie scientifiche e di analisi dati (pandas, numpy) se in futuro si vorranno elaborare statistiche più avanzate.

###  Perché Nuxt lato frontend
- **Basato su Vue 3:** offre un’esperienza di sviluppo fluida e reattiva, perfetta per dashboard dinamiche.
- **Routing automatico:** Nuxt gestisce le rotte (`/station/:id`) in modo dichiarativo, senza dover configurare manualmente un router Vue.
- **Rendering ottimizzato:** può usare SSR o SPA, migliorando SEO e prestazioni.
- **Tailwind integrato:** consente di creare rapidamente un’interfaccia moderna e responsive con poche classi utility.
- **Esperienza utente fluida:** la navigazione tra le stazioni è istantanea grazie al router client-side.

###  Comunicazione tra frontend e backend
Il frontend Nuxt comunica con il backend Flask tramite fetch API:


Frontend (Nuxt) → http://localhost:5000/api/stations

Backend (Flask) → https://api.zeroc.green/v1/stations/


In questo modo:
- il browser non chiama direttamente l’API esterna (evitando problemi di CORS*),
- Flask controlla e filtra i dati prima di inviarli al frontend,
- Nuxt si occupa solo della presentazione grafica e dell’esperienza utente.



*Nota sui problemi di CORS

Il browser, per motivi di sicurezza, blocca automaticamente le richieste verso domini esterni diversi da quello dell’applicazione (es. chiamate dirette da localhost:3000 a api.zeroc.green).
Questo meccanismo si chiama CORS (Cross-Origin Resource Sharing).

Per evitare questi errori, il backend Flask funge da proxy intermedio:

Il frontend comunica solo con http://localhost:5000/api/...,

Flask inoltra la richiesta all’API esterna,

e restituisce al frontend una risposta “sicura” e con header corretti.

In questo modo:

 si eliminano gli errori di CORS,

 si mantiene il controllo sui dati in ingresso,

 si può aggiungere logica (es. media ponderata) prima che i dati arrivino al frontend

---

In sintesi:  
**Flask** = cervello e sicurezza  
**Nuxt** = interfaccia e interazione 

## Considerazioni e sviluppi futur ##

Questo progetto dimostra come un’architettura Flask + Nuxt possa integrare calcolo e visualizzazione in modo chiaro, modulare e scalabile.
L’obiettivo principale — replicare e arricchire le API di ZeroC Green con il calcolo della media ponderata — è pienamente raggiunto, mantenendo un design moderno e leggibile.

In futuro prevedo di:

 Aggiungere un grafico a linee interattivo per la metrica selezionata (con Recharts),

 Implementare un aggiornamento automatico dei dati in tempo reale,

 Espandere il backend con un sistema di caching o database leggero per storicizzare le misurazioni.

 L’obiettivo finale è creare una dashboard completa, efficiente e mantenibile, utile sia a livello didattico che operativo.

 
# Installazione

###  Backend (Flask)
```bash
cd backend
pip install flask flask-cors requests
python server.app.py


##  Installazione Frontend (Nuxt 4 + Tailwind 4) ##

Il frontend è sviluppato in **Nuxt 4** (basato su Vue 3) e utilizza **Tailwind CSS v4** per lo stile.  
Segue un’architettura moderna e completamente *responsive* per visualizzare le stazioni e i dettagli sulla qualità dell’aria.

---

###  Installazione pacchetti

Apri un terminale nella cartella `frontend` e installa le dipendenze:

```bash
cd frontend
npm install

Avvia il server di sviluppo:

npm run dev

accedi al server locale:

http://localhost:3000


#Troubleshoting#

Configurazione corretta di Tailwind v4 (molto importante)
 Problema comune

Se usi Tailwind 4 ma mantieni la vecchia sintassi (@tailwind base; @tailwind components; @tailwind utilities;),
otterrai questo errore:

 Missing "./components" specifier in "tailwindcss" package

 e nessun colore/stile verrà applicato.

 Soluzione (Tailwind v4 + Nuxt 4)
 Installa i pacchetti aggiornati
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest @tailwindcss/postcs


File assets/css/tailwind.css

@import "tailwindcss";

Non usare più @tailwind base o @tailwind components.




#Note tecniche#

La nuova sintassi di Tailwind 4 utilizza un singolo @import "tailwindcss" e il plugin @tailwindcss/postcss.

Nuxt non necessita più di postcss.config.js: la configurazione è integrata in nuxt.config.js.

Il progetto è 100% compatibile con Nuxt 4.x e Vite.

Se cloni il repo, basta eseguire:

cd frontend && npm install && npm run dev
