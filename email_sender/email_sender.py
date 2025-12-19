"""
DEMO

Visto che questa è una demo non mi andava di mettere le mie credenziali nei secrets,

Inserisci in queste variabili le TUE credenziali Gmail (se vuoi usare lo script):

SENDER_EMAIL
> il tuo indirizzo Gmail (es. nome@gmail.com)

APP_PASSWORD
> NON è la password di Gmail.
> Devi creare una App Password da Google:

1. Vai su https://myaccount.google.com/security
2. Attiva la verifica in due passaggi (obbligatoria)
3. Vai su https://myaccount.google.com/apppasswords
4. In "Nome dell'app" inserisci un nome qualsiasi
5. Copia la password generata (16 caratteri)
6. Incollala nella variabile APP_PASSWORD

NOTE:
- Il file `email_list.txt` contiene la lista degli indirizzi email che riceveranno l’email
- Il file `email_template.html` contiene il contenuto della email
"""


import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "LA_TUA_EMAIL_GMAIL"
APP_PASSWORD = "LA_TUA_APP_PASSWORD"
SURVEY_URL = "http://127.0.0.1:5000"

with open("test/email_list.txt", "r") as f:
    recipients = [line.strip() for line in f if line.strip()]

with open("test/email_template.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Invia email a ciascun destinatario
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, APP_PASSWORD)
    for recipient in recipients:
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        msg["Subject"] = "Dopo il corso, condividi il tuo feedback"
        msg.set_content(f"Ciao! Partecipa al nostro sondaggio anonimo: {SURVEY_URL}\n\nGrazie!")
        msg.add_alternative(html_content, subtype="html")
        server.send_message(msg)
        print(f"Email inviata a {recipient}")