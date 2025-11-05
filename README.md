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
Cos’è la “media ponderata” e perché serve?

L’API ufficiale di ZeroC Green restituisce, per ogni metrica (es. PM10, NO2, ecc.), una lista con 10 giorni di dati.

esempio :
"PM10": [
  { "date": "2025-10-25", "average": 10.5, "sample_size": 250 },
  { "date": "2025-10-26", "average": 5.3,  "sample_size": 200 },
  { "date": "2025-10-27", "average": 0.0,  "sample_size": 0 },
  ...
]

Ma non tutti i giorni sono “uguali”: un giorno con più misurazioni (sample_size alto) è più affidabile di un giorno con poche.
Per questo si usa una media ponderata, che tiene conto del “peso” di ogni giorno.

Formula della media ponderata:

Esempio pratico
Giorno	average	sample_size	Prodotto
25/10	10.5	250	2625
26/10	5.3	200	1060
27/10	0	0	(escluso)

Totale:
weighted_average = (2625 + 1060) / (250 + 200) = 3685 / 450 = 8.18




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
- il browser non chiama direttamente l’API esterna (evitando problemi di CORS),
- Flask controlla e filtra i dati prima di inviarli al frontend,
- Nuxt si occupa solo della presentazione grafica e dell’esperienza utente.

---

In sintesi:  
**Flask** = cervello e sicurezza  
**Nuxt** = interfaccia e interazione 

# Installazione

###  Backend (Flask)
```bash
cd backend
pip install flask flask-cors requests
python server.app.py


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




 
