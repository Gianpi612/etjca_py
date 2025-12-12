from flask import Flask, render_template, request, session, redirect, url_for
import csv

app = Flask(__name__)
app.secret_key = 'sdfjodfghdfgh'

DOMANDE = [
    {"id": "q1", "text": "domanda test 1."},
    {"id": "q2", "text": "domanda tst 2."},
    {"id": "q3", "text": "domanda test 3."},
    {"id": "q4", "text": "domanda test 4."},
    {"id": "q5", "text": "domanda test 5."},
    {"id": "q6", "text": "domanda test 6."},
    {"id": "q7", "text": "domanda test 7."},
    {"id": "q8", "text": "domanda test 8."},
]

OPZIONI = [
    {"valore": "molto_daccordo", "label": "Molto d'accordo"},
    {"valore": "daccordo", "label": "D'accordo"},
    {"valore": "neutrale", "label": "Neutrale"},
    {"valore": "disaccordo", "label": "In disaccordo"},
    {"valore": "molto_disaccordo", "label": "Molto in disaccordo"}
]

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
        risposte_temp = session.get('risposte', {})
        risposte_temp[domanda_corrente['id']] = risposta
        session['risposte'] = risposte_temp
        next_idx = idx + 1
        if next_idx < len(DOMANDE):
            return redirect(url_for('step', idx=next_idx))
        else:
            # Se le domande sono finite, vai al salvataggio finale
            return redirect(url_for('fine'))

    # calcolo progresso 
    progresso = int((idx / len(DOMANDE)) * 100)
    
    return render_template(
        'step.html', 
        domanda=domanda_corrente, 
        opzioni=OPZIONI, 
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
    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "text", "risposta"])
        writer.writeheader()
        writer.writerows(summary)
    
    return render_template('success.html', risultati=summary)

if __name__ == '__main__':
    app.run(debug=True)