from flask import Flask, render_template, request, session, redirect, url_for
import csv

app = Flask(__name__)
app.secret_key = 'sdfjodfghdfgh'

DOMANDE = [
    {"id": "q1", "text": "Ritengo di avere ben chiaro chi sono professionalmente."},
    {"id": "q2", "text": "Le parole che uso per descrivermi al lavoro sono coerenti con ciò che faccio."},
    {"id": "q3", "text": "Mi è facile definire il mio stile professionale."},
    {"id": "q4", "text": "Conosco molto bene i miei punti di forza."},
    {"id": "q5", "text": "Ho identificato chiaramente le competenze che devo sviluppare."},
    {"id": "q6", "text": "Sto già investendo tempo per imparare nuove skill."},
    {"id": "q7", "text": "Ho chiaro come voglio essere percepito professionalmente."},
    {"id": "q8", "text": "Mi preparo regolarmente per i colloqui."},
]

OPZIONI = [
    {"valore": "molto_daccordo", "label": "5"},
    {"valore": "daccordo", "label": "4"},
    {"valore": "neutrale", "label": "3"},
    {"valore": "disaccordo", "label": "2"},
    {"valore": "molto_disaccordo", "label": "1"}
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

    # GET → visualizzazione domanda
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