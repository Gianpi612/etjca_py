import csv
import random

# Importazione delle domande
from domande import DOMANDE

# Numero di record da generare
num_records = 2000

# Nome del file CSV
filename = 'dataset_quiz.csv'

# Estrazione delle intestazioni dalle domande
fieldnames = [domanda['id'] for domanda in DOMANDE]

# Creazione di un dizionario per mappare id domanda -> possibili valori
opzioni_per_domanda = {}
for domanda in DOMANDE:
    opzioni_per_domanda[domanda['id']] = [opt['valore'] for opt in domanda['opzioni']]

# Generazione del dataset
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Scrittura intestazione
    writer.writeheader()
    
    # Generazione record casuali
    for i in range(num_records):
        record = {}
        for domanda_id in fieldnames:
            # Selezione casuale di un valore tra le opzioni disponibili
            record[domanda_id] = random.choice(opzioni_per_domanda[domanda_id])
        writer.writerow(record)

print(f"Dataset generato con successo: {filename}")
print(f"Numero di record: {num_records}")
print(f"Numero di colonne: {len(fieldnames)}")
print("\nColonne del dataset:")
for i, domanda in enumerate(DOMANDE, 1):
    print(f"{i}. {domanda['id']}: {domanda['text']}")

print("\n" + "="*80)
print("Prime 5 righe del dataset:")
print("="*80)

# Lettura e visualizzazione delle prime righe
with open(filename, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        if i < 5:
            print(f"\nRecord {i+1}:")
            for key, value in row.items():
                print(f"  {key}: {value}")
        else:
            break