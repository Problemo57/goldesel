// Globale Variablen
let sourcesData = null;

// Hilfsfunktionen
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function formatCurrency(amount, currency = '$') {
    // Mapping von Währungszeichen zu ISO-Währungscodes
    const currencyCodeMap = {
        '$': 'USD',
        '€': 'EUR',
        '£': 'GBP',
        '¥': 'JPY',
        'MYST': 'MYST',  // Eigener Währungscode
        'HG': 'HG'       // Eigener Währungscode
    };
    
    // Standardmäßig USD verwenden, wenn es keine Zuordnung gibt
    const currencyCode = currencyCodeMap[currency] || 'USD';
    
    // Für Kryptowährungen und eigene Währungen
    if (!['USD', 'EUR', 'GBP', 'JPY'].includes(currencyCode)) {
        return amount.toFixed(2) + ' ' + currencyCode;
    }
    
    // Für Standard-Währungen
    return new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: currencyCode,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

function getStatusClass(status) {
    switch(status) {
        case 'OK':
            return 'status-ok';
        case 'ERROR':
            return 'status-error';
        default:
            return 'status-unknown';
    }
}

function updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('de-DE');
    document.getElementById('update-time').textContent = timeString;
}

// Holt Daten von der API
async function fetchSourcesData() {
    try {
        const response = await fetch('/sources');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fehler beim Abrufen der Daten:', error);
        document.getElementById('sources-container').innerHTML = `
            <div class="error-message">
                <p>Fehler beim Laden der Daten. Bitte versuchen Sie es später erneut.</p>
                <p class="error-details">${error.message}</p>
            </div>
        `;
        return null;
    }
}

// Zeigt die Daten auf dem Dashboard an
function renderDashboard(data) {
    if (!data) return;
    
    sourcesData = data;
    
    // Berechne Gesamtstatistiken
    let totalEarned = 0;
    let todayEarned = 0;
    let totalData = 0;
    let todayData = 0;
    let activeSources = 0;
    let totalSources = 0;
    
    // Konvertiere Objekt in Array und sortiere nach heutigen Einnahmen (absteigend)
    const sourcesArray = Object.values(data).sort((a, b) => 
        b.today_earned - a.today_earned
    );
    
    // Aktualisiere Gesamtstatistiken
    // Hier nehmen wir an, dass alle Werte in USD sind oder
    // bei alternativen Währungen eine Umrechnung erfolgt ist
    sourcesArray.forEach(source => {
        totalSources++;
        
        // Nur Werte mit Standard-Währung ($) addieren
        // Für eine vollständige Lösung müsste hier eine Währungsumrechnung erfolgen
        if (source.currency === '$') {
            totalEarned += source.total_earned;
            todayEarned += source.today_earned;
        }
        
        totalData += source.data_total;
        todayData += source.data_today;
        
        if (source.status === 'OK') {
            activeSources++;
        }
    });
    
    // Aktualisiere die Zusammenfassung (Gesamt immer in USD)
    document.getElementById('total-earned').textContent = formatCurrency(totalEarned);
    document.getElementById('today-earned').textContent = formatCurrency(todayEarned);
    document.getElementById('total-data').textContent = formatBytes(totalData);
    document.getElementById('today-data').textContent = formatBytes(todayData);
    document.getElementById('active-sources').textContent = `${activeSources}/${totalSources}`;
    
    // Rendere die einzelnen Quellen
    const sourcesContainer = document.getElementById('sources-container');
    sourcesContainer.innerHTML = '';
    
    sourcesArray.forEach(source => {
        const sourceCard = document.createElement('div');
        sourceCard.className = 'source-card';
        sourceCard.innerHTML = `
            <div class="source-header">
                <div class="source-name">${source.name}</div>
                <div class="status ${getStatusClass(source.status)}">${source.status}</div>
            </div>
            <div class="source-stats">
                <div class="source-stat-item">
                    <div class="source-stat-label">Gesamt verdient</div>
                    <div class="source-stat-value">${formatCurrency(source.total_earned, source.currency)}</div>
                </div>
                <div class="source-stat-item">
                    <div class="source-stat-label">Heute verdient</div>
                    <div class="source-stat-value">${formatCurrency(source.today_earned, source.currency)}</div>
                </div>
                <div class="source-stat-item">
                    <div class="source-stat-label">Gesamt Daten</div>
                    <div class="source-stat-value">${formatBytes(source.data_total)}</div>
                </div>
                <div class="source-stat-item">
                    <div class="source-stat-label">Heutige Daten</div>
                    <div class="source-stat-value">${formatBytes(source.data_today)}</div>
                </div>
            </div>
        `;
        sourcesContainer.appendChild(sourceCard);
    });
    
    // Aktualisiere den Zeitstempel
    updateLastUpdateTime();
}

// Initialisiere das Dashboard
async function initDashboard() {
    const data = await fetchSourcesData();
    renderDashboard(data);
    
    // Event-Listener für den Aktualisieren-Button
    document.getElementById('refresh-btn').addEventListener('click', async () => {
        document.getElementById('sources-container').innerHTML = '<div class="loading">Aktualisiere Daten...</div>';
        const refreshedData = await fetchSourcesData();
        renderDashboard(refreshedData);
    });
}

// Starte die Dashboard-Initialisierung, wenn das DOM geladen ist
document.addEventListener('DOMContentLoaded', initDashboard);

// Automatische Aktualisierung alle 5 Minuten
setInterval(async () => {
    const refreshedData = await fetchSourcesData();
    renderDashboard(refreshedData);
}, 5 * 60 * 1000);
