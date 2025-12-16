from flask import Flask, render_template, request, session, redirect, url_for
from domande import DOMANDE
import csv
import os

app = Flask(__name__)
app.secret_key = 'sdfjodfghdfgh'

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


@app.route('/fine')
def fine():
    dati_finali = session.get('risposte', {})
    print(DOMANDE)
    summary = []
    for d in DOMANDE:
        summary.append({
            "id": d['id'],
            "text": d['text'],
            "risposta": dati_finali.get(d['id'])
        })
    print(summary)

    file_exists = os.path.isfile("output.csv")

    with open("output.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "text", "risposta"])
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(summary)
    
    return render_template('success.html', risultati=summary)

if __name__ == '__main__':
    app.run(debug=True)