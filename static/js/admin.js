// admin.js - JavaScript per Dashboard Admin

// Nota: datiGrezzi e datiUploaded vengono passati dal template
// e devono essere definiti prima di caricare questo script

// Funzione per contare le risposte (formato lungo: user_id, timestamp, id, text, risposta)
function contaRisposte(idDomanda, dataset) {
    const conteggio = {};
    dataset.forEach(item => {
        if (item.id === idDomanda && item.risposta) {
            const risposta = item.risposta;
            conteggio[risposta] = (conteggio[risposta] || 0) + 1;
        }
    });
    return conteggio;
}

// Funzione per contare risposte da dataset largo (una riga = un utente, colonne = domande)
function contaRisposteDataset(colonnaId, dataset) {
    const conteggio = {};
    dataset.forEach(item => {
        const risposta = item[colonnaId];
        if (risposta) {
            conteggio[risposta] = (conteggio[risposta] || 0) + 1;
        }
    });
    return conteggio;
}

// Configurazione colori
const coloriPalette = [
    'rgba(79, 70, 229, 0.8)',   // Indigo
    'rgba(59, 130, 246, 0.8)',  // Blue
    'rgba(16, 185, 129, 0.8)',  // Green
    'rgba(245, 158, 11, 0.8)',  // Orange
    'rgba(239, 68, 68, 0.8)',   // Red
    'rgba(139, 92, 246, 0.8)',  // Purple
    'rgba(236, 72, 153, 0.8)',  // Pink
];

// Funzione per creare grafico
function creaGrafico(canvasId, dati, titolo) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const labels = Object.keys(dati);
    const values = Object.values(dati);
    const totale = values.reduce((a, b) => a + b, 0);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Numero Risposte',
                data: values,
                backgroundColor: coloriPalette.slice(0, labels.length),
                borderColor: coloriPalette.slice(0, labels.length).map(c => c.replace('0.8', '1')),
                borderWidth: 2,
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    top: 30  // Spazio sopra per le percentuali
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    padding: 12,
                    titleFont: { size: 14, weight: 'bold' },
                    bodyFont: { size: 13 },
                    borderColor: 'rgba(100, 116, 139, 0.2)',
                    borderWidth: 1,
                    callbacks: {
                        // Mostra valore e percentuale nel tooltip
                        label: function(context) {
                            const valore = context.parsed.y;
                            const percentuale = ((valore / totale) * 100).toFixed(1);
                            return `${valore} risposte (${percentuale}%)`;
                        }
                    }
                },
                // Plugin per mostrare percentuali sulle barre
                datalabels: {
                    display: true,
                    color: '#1e293b',
                    font: {
                        weight: 'bold',
                        size: 11
                    },
                    formatter: function(value, context) {
                        const percentuale = ((value / totale) * 100).toFixed(1);
                        return percentuale + '%';
                    },
                    anchor: 'end',
                    align: 'end',
                    offset: -2
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: { size: 12 }
                    },
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        font: { size: 11 }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        },
        plugins: [ChartDataLabels] // Abilita il plugin per le percentuali
    });
}

// Gestione Tab
function showTab(tabName) {
    // Nascondi tutti i contenuti
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.tab-button').forEach(el => {
        el.classList.remove('text-indigo-600', 'border-b-2', 'border-indigo-600');
        el.classList.add('text-slate-500');
    });

    // Mostra il tab selezionato
    document.getElementById('content-' + tabName).classList.remove('hidden');
    const button = document.getElementById('tab-' + tabName);
    button.classList.add('text-indigo-600', 'border-b-2', 'border-indigo-600');
    button.classList.remove('text-slate-500');
}

// Dark Mode Toggle
function toggleDarkMode() {
    const html = document.documentElement;
    const isDark = html.classList.toggle('dark');
    
    // Salva preferenza in localStorage
    localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
    
    // Aggiorna icona
    updateDarkModeIcon(isDark);
}

function updateDarkModeIcon(isDark) {
    const moonIcon = document.getElementById('moon-icon');
    const sunIcon = document.getElementById('sun-icon');
    
    if (isDark) {
        moonIcon.classList.add('hidden');
        sunIcon.classList.remove('hidden');
    } else {
        moonIcon.classList.remove('hidden');
        sunIcon.classList.add('hidden');
    }
}

// Carica preferenza dark mode all'avvio
function loadDarkModePreference() {
    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'enabled') {
        document.documentElement.classList.add('dark');
        updateDarkModeIcon(true);
    }
}

// Inizializzazione quando il DOM è carico
document.addEventListener('DOMContentLoaded', function() {
    // Carica preferenza dark mode
    loadDarkModePreference();
    
    // Crea i grafici per risposte raccolte (formato lungo)
    if (typeof datiGrezzi !== 'undefined' && datiGrezzi.length > 0) {
        creaGrafico('chart_q1', contaRisposte('q1', datiGrezzi), 'Genere');
        creaGrafico('chart_q2', contaRisposte('q2', datiGrezzi), 'Area Italia');
        creaGrafico('chart_q3', contaRisposte('q3', datiGrezzi), 'Fascia Età');
        creaGrafico('chart_q_titolo', contaRisposte('q_titolo', datiGrezzi), 'Titolo di Studio');
        creaGrafico('chart_q4', contaRisposte('q4', datiGrezzi), 'Chiaro chi sono');
        creaGrafico('chart_q5', contaRisposte('q5', datiGrezzi), 'Punti di forza');
        creaGrafico('chart_q6', contaRisposte('q6', datiGrezzi), 'Colmare lacune');
        creaGrafico('chart_q7', contaRisposte('q7', datiGrezzi), 'Rispecchiare valori');
        creaGrafico('chart_q8', contaRisposte('q8', datiGrezzi), 'Obiettivi chiari');
        creaGrafico('chart_q9', contaRisposte('q9', datiGrezzi), 'Competenze tecniche');
        creaGrafico('chart_q10', contaRisposte('q10', datiGrezzi), 'Soft skills');
        creaGrafico('chart_q11', contaRisposte('q11', datiGrezzi), 'Nuove skill');
        creaGrafico('chart_q12', contaRisposte('q12', datiGrezzi), 'Esploro opportunità');
        creaGrafico('chart_q13', contaRisposte('q13', datiGrezzi), 'Percorso con HR');
        creaGrafico('chart_q14', contaRisposte('q14', datiGrezzi), 'Monitoro offerte');
        creaGrafico('chart_q15', contaRisposte('q15', datiGrezzi), 'Trovato lavoro');
    }

    // Crea i grafici per dataset caricato (formato largo: una riga per utente)
    if (typeof datiUploaded !== 'undefined' && datiUploaded.length > 0) {
        creaGrafico('chart_ds_q1', contaRisposteDataset('q1', datiUploaded), 'Genere');
        creaGrafico('chart_ds_q2', contaRisposteDataset('q2', datiUploaded), 'Area Italia');
        creaGrafico('chart_ds_q3', contaRisposteDataset('q3', datiUploaded), 'Fascia Età');
        creaGrafico('chart_ds_q_titolo', contaRisposteDataset('q_titolo', datiUploaded), 'Titolo di Studio');
        creaGrafico('chart_ds_q4', contaRisposteDataset('q4', datiUploaded), 'Chiaro chi sono');
        creaGrafico('chart_ds_q5', contaRisposteDataset('q5', datiUploaded), 'Punti di forza');
        creaGrafico('chart_ds_q6', contaRisposteDataset('q6', datiUploaded), 'Colmare lacune');
        creaGrafico('chart_ds_q7', contaRisposteDataset('q7', datiUploaded), 'Rispecchiare valori');
        creaGrafico('chart_ds_q8', contaRisposteDataset('q8', datiUploaded), 'Obiettivi chiari');
        creaGrafico('chart_ds_q9', contaRisposteDataset('q9', datiUploaded), 'Competenze tecniche');
        creaGrafico('chart_ds_q10', contaRisposteDataset('q10', datiUploaded), 'Soft skills');
        creaGrafico('chart_ds_q11', contaRisposteDataset('q11', datiUploaded), 'Nuove skill');
        creaGrafico('chart_ds_q12', contaRisposteDataset('q12', datiUploaded), 'Esploro opportunità');
        creaGrafico('chart_ds_q13', contaRisposteDataset('q13', datiUploaded), 'Percorso con HR');
        creaGrafico('chart_ds_q14', contaRisposteDataset('q14', datiUploaded), 'Monitoro offerte');
        creaGrafico('chart_ds_q15', contaRisposteDataset('q15', datiUploaded), 'Trovato lavoro');
    }
});