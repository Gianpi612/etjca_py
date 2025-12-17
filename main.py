from flask import Flask, render_template, request, session, redirect, url_for, send_file
from domande import DOMANDE
from datetime import datetime
import uuid
import csv
import os

app = Flask(__name__)
app.secret_key = 'sdfjodfghdfgh'

# Credenziali Admin (hardcoded per ora)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

@app.route('/')
def intro():
    # pulisce la sessione per un nuovo utente
    session.clear()
    session['risposte'] = {}
    return render_template('intro.html')

@app.route('/domanda/<int:idx>', methods=['GET', 'POST'])
def step(idx):
    # se l'indice non esiste o è uguale al numero delle domande, reindirizza all'intro
    if idx < 0 or idx >= len(DOMANDE):
        return redirect(url_for('intro'))

    domanda_corrente = DOMANDE[idx]

    if request.method == 'POST':
        risposta = request.form.get('risposta')
        action = request.form.get('action')

        # Salva sempre la risposta se presente 
        risposte_temp = session.get('risposte', {})
        if risposta:
            risposte_temp[domanda_corrente['id']] = risposta
            session['risposte'] = risposte_temp

        # Pulsante "Indietro"
        if action == "back":
            return redirect(url_for('step', idx=idx - 1))

        # Pulsante "Avanti"
        next_idx = idx + 1
        if next_idx < len(DOMANDE):
            return redirect(url_for('step', idx=next_idx))
        else:
            return redirect(url_for('fine'))
        
    progresso = int((idx / len(DOMANDE)) * 100)

    return render_template(
        'step.html',
        domanda=domanda_corrente,
        opzioni=domanda_corrente['opzioni'],
        idx=idx,
        totale=len(DOMANDE),
        progresso=progresso
    )

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('admin_login.html', error=True)
    
    return render_template('admin_login.html', error=False)

@app.route('/admin')
def admin():
    # Controlla se l'admin è loggato
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    dati = []

    if os.path.isfile("output.csv"):
        with open("output.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dati.append(row)

    return render_template("admin.html", dati=dati)

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('intro'))

@app.route('/reset-data', methods=['POST'])
def reset_data():
    # Controlla se l'admin è loggato
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    # Cancella il file CSV
    if os.path.isfile("output.csv"):
        os.remove("output.csv")
    
    return redirect(url_for('admin'))

@app.route('/export-csv')
def export_csv():
    # Controlla se l'admin è loggato
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    from flask import send_file
    
    # Verifica che il file esista
    if not os.path.isfile("output.csv"):
        return "Nessun dato da esportare", 404
    
    # Invia il file CSV per il download
    return send_file(
        "output.csv",
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'risposte_questionario_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/fine')
def fine():
    dati_finali = session.get('risposte', {})
    
    # Genera un ID univoco per questo utente
    user_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    summary = []
    for d in DOMANDE:
        risposta = dati_finali.get(d['id'])
        if risposta:  # Salva solo se ha risposto
            summary.append({
                "user_id": user_id,
                "timestamp": timestamp,
                "id": d['id'],
                "text": d['text'],
                "risposta": risposta
            })
    
    print(f"Utente {user_id} - {len(summary)} risposte salvate")

    file_exists = os.path.isfile("output.csv")

    with open("output.csv", "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "timestamp", "id", "text", "risposta"])
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(summary)
    
    return render_template('success.html', risultati=summary)

if __name__ == '__main__':
    app.run(debug=True)