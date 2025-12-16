import csv
import random

# Definizione dei valori possibili
generi = ['M', 'F']
zone = ['Centro', 'Nord', 'Sud']
fasce_eta = ['18-30', '30-50', '50+']
obiettivi = ['Rafforzare le tue competenze', 'Acquisirne nuove']

# Numero di record da generare
num_records = 2000

# Nome del file CSV
filename = 'dataset_corsi.csv'

# Generazione del dataset
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Genere', 'Zona_Residenza', 'Fascia_Eta', 'Obiettivo_Corso']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Scrittura intestazione
    writer.writeheader()
    
    # Generazione record casuali
    for i in range(num_records):
        record = {
            'Genere': random.choice(generi),
            'Zona_Residenza': random.choice(zone),
            'Fascia_Eta': random.choice(fasce_eta),
            'Obiettivo_Corso': random.choice(obiettivi)
        }
        writer.writerow(record)

print(f"Dataset generato con successo: {filename}")
print(f"Numero di record: {num_records}")
print("\nPrime 5 righe del dataset:")

# Lettura e visualizzazione delle prime righe
with open(filename, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        if i < 5:
            print(row)
        else:
            break