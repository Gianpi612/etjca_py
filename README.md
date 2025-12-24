# 📊 Questionario Post-Corso

Sistema web per la raccolta e analisi di questionari follow-up post-corso. Permette agli utenti di compilare questionari anonimi e agli amministratori di visualizzare statistiche dettagliate con grafici interattivi.

---

## 🎯 Caratteristiche Principali

### **Per gli Utenti**
- ✅ Questionario interattivo step-by-step
- ✅ Design moderno e responsive
- ✅ Barra di progresso dinamica
- ✅ Navigazione avanti/indietro
- ✅ Raccolta dati anonima
- ✅ Pagina di ringraziamento animata

### **Per gli Amministratori**
- ✅ Dashboard admin protetta con login
- ✅ 16 grafici interattivi con percentuali
- ✅ Modalità chiara/scura (Dark Mode)
- ✅ Upload dataset esterni per confronti
- ✅ Export dati in CSV
- ✅ Visualizzazione tabellare delle risposte
- ✅ Statistiche aggregate in tempo reale


---

## 🚀 Installazione

### **Prerequisiti**
- Python 3.8+
- pip (gestore pacchetti Python)

### **1. Clona il Repository**
```bash
git clone https://github.com/Gianpi612/etjca_py.git
cd etjca_py
```

### **2. Installa le Dipendenze**
```bash
pip install flask
```

### **3. Avvia l'Applicazione**
```bash
python main.py
```

L'applicazione sarà disponibile su: `http://localhost:5000`

---

## 📖 Utilizzo

### **Compilazione Questionario (Utenti)**

1. Apri il browser e vai su `http://localhost:5000`
2. Leggi l'introduzione e clicca "Partecipa alla ricerca"
3. Rispondi alle domande navigando con i pulsanti
4. Completa il questionario
5. Le risposte vengono salvate automaticamente in `output.csv`

### **Dashboard Admin**

1. Clicca su "Admin" in fondo alla homepage
2. Effettua il login:
   - **Username:** `admin`
   - **Password:** `admin123`
3. Visualizza statistiche e grafici
4. (Opzionale) Carica dataset esterni per confronti
5. Esporta dati in CSV

---

## 🎨 Funzionalità Dashboard

### **Tab "Risposte Raccolte"**
- 📊 3 card con statistiche (totale, stato, export)
- 📈 16 grafici interattivi raggruppati per categoria:
  - Dati Demografici (4 grafici)
  - Autoconsapevolezza Professionale (4 grafici)
  - Obiettivi e Competenze (4 grafici)
  - Ricerca Lavoro e Supporto (4 grafici)
- 📋 Tabella completa con tutte le risposte

### **Tab "Dataset Caricato"**
- 📁 Upload di dataset esterni (formato CSV)
- 📊 Stessi 16 grafici per analisi comparative
- 🗑️ Eliminazione dataset caricato

### **Altre Funzionalità**
- 🌙 **Dark Mode** - Toggle chiaro/scuro persistente
- 📊 **Percentuali sui grafici** - Visualizzazione automatica
- 📥 **Export CSV** - Download dati con timestamp
- 🔄 **Reset dati** - Cancellazione database (con conferma)

---

## 🔧 Configurazione

### **Modificare le Domande**

Modifica il file `domande.py`:

```python
DOMANDE = [
    {
        "id": "q1",
        "text": "La tua domanda qui?",
        "opzioni": [
            {"valore": "opzione1", "label": "Opzione 1"},
            {"valore": "opzione2", "label": "Opzione 2"},
        ]
    },
    # Aggiungi altre domande...
]
```

### **Cambiare Credenziali Admin**

In `main.py` modifica:

```python
ADMIN_USERNAME = 'admin'      # ← Cambia username
ADMIN_PASSWORD = 'admin123'   # ← Cambia password
```

⚠️ **Importante:** In produzione, usa hash delle password invece di testo in chiaro!

### **Cambiare Porta**

In `main.py` alla fine del file:

```python
if __name__ == '__main__':
    app.run(debug=True, port=8080)  # ← Cambia porta
```

---

## 📊 Formato Dataset per Upload

Il dataset caricato deve avere questo formato CSV:

```csv
q1,q2,q3,q_titolo,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15
femmina,sud,30-50,diploma,si,si,no,si,no,si,si,no,si,no,si,no
maschio,nord,18-30,laurea_triennale,no,si,si,no,si,no,si,si,no,si,no,si
...
```

- **Una riga per utente**
- **16 colonne** (una per domanda)
- **Header obbligatorio** con gli ID delle domande
- **Encoding:** UTF-8

---

## 🗂️ Gestione Dati

### **File Generati**

| File | Descrizione | Formato |
|------|-------------|---------|
| `output.csv` | Risposte dal questionario | user_id, timestamp, id, text, risposta |
| `uploaded_dataset.csv` | Dataset caricato dall'admin | q1, q2, q3, ..., q15 |

### **Privacy**

- ✅ Dati anonimi (nessun dato personale)
- ✅ `user_id` generato casualmente (non tracciabile)
- ✅ CSV escluso da Git (vedi `.gitignore`)
- ✅ Solo admin può accedere ai dati

### **Backup**

Per salvare i dati:

```bash
# Copia il file CSV
cp output.csv backup_$(date +%Y%m%d).csv

# Oppure usa il pulsante "Export CSV" nella dashboard
```

---

## 🎨 Tecnologie Utilizzate

### **Backend**
- **Flask 3.x** - Framework web Python
- **Python 3.13** - Linguaggio di programmazione

### **Frontend**
- **HTML5** - Struttura
- **Tailwind CSS 3.x** - Styling (via CDN)
- **JavaScript ES6** - Interattività
- **Jinja2** - Template engine

### **Visualizzazioni**
- **Chart.js 4.x** - Grafici interattivi
- **ChartJS DataLabels** - Plugin percentuali

### **Storage**
- **CSV** - Database semplice basato su file

---

## 🏗️ Architettura

### **Pattern MVC**
```
Model (domande.py)
   ↓
Controller (main.py)
   ↓
View (templates/*.html)
```

### **Flusso Dati**

```
Utente → Questionario → Flask → CSV
                                  ↓
Admin → Login → Dashboard → Legge CSV → Grafici
```

### **Principi Applicati**

- ✅ **DRY (Don't Repeat Yourself)** - Template riusabili
- ✅ **Separation of Concerns** - HTML/CSS/JS separati
- ✅ **RESTful Routes** - Route logiche e intuitive
- ✅ **Responsive Design** - Funziona su tutti i dispositivi

---

## 🔒 Sicurezza

### **Implementato**
- ✅ Sessioni Flask per autenticazione
- ✅ CSRF protection (implicito in Flask forms)
- ✅ Validazione lato server
- ✅ Encoding UTF-8 per prevenire injection

### **Da Implementare in Produzione**
- ⚠️ Hash password (bcrypt/argon2)
- ⚠️ HTTPS/SSL
- ⚠️ Rate limiting
- ⚠️ Database reale (SQLite/PostgreSQL)
- ⚠️ Variabili d'ambiente per credenziali

---
## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per dettagli.

---

*Ultimo aggiornamento: Dicembre 2025*