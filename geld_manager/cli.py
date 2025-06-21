import time
import os
from datetime import datetime
import signal
import sys

from adnade import Adnade
from mysterium import Mysterium
from honeygain import Honeygain
from packetshare import PacketShare
from simple_sources import *


def clear_screen():
    # Bildschirm löschen basierend auf Betriebssystem
    os.system('cls' if os.name == 'nt' else 'clear')


def format_bytes(bytes_value):
    """Formatiert Bytes in lesbaren Größen (KB, MB, GB)"""
    if bytes_value < 1024:
        return f"{bytes_value} B"
    elif bytes_value < 1024**2:
        return f"{bytes_value/1024:.2f} KB"
    elif bytes_value < 1024**3:
        return f"{bytes_value/(1024**2):.2f} MB"
    else:
        return f"{bytes_value/(1024**3):.2f} GB"


def get_sources_data():
    """Sammelt Daten von allen Quellen"""
    sources = {}

    # Währungsumrechnungskurse
    currency_exchange_rates = {
        "MYST": 0.20,  # MYST zu USD Kurs (Stand: Juni 2025)
        "€": 1.15
    }

    # Liste aller zu initialisierenden Quellen
    source_classes = {
        "Mysterium": Mysterium,
        "Honeygain": Honeygain,
        "Pawns": Pawns,
        "Earnapp": EarnApp,
        "PacketStream": PacketStream,
        "Traffmonetizer": Traffmonetizer,
        "RePocket": RePocket,
        "EarnFM": EarnFM,
        "PacketShare": PacketShare,
        "Adnade": Adnade
    }

    # Versuchen, jede Quelle zu initialisieren
    for name, source_class in source_classes.items():
        try:
            sources[name] = source_class()
        except Exception as e:
            print(f"Fehler beim Initialisieren von {name}: {e}")
    
    result = {}
    
    for name, source in sources.items():
        try:
            try:
                status = source.get_status().value
            except:
                status = "ERROR"

            total_earned = 0
            today_earned = 0
            data_total = 0
            data_today = 0
            
            try:
                total_earned = source.get_balance()
            except:
                pass
                
            try:
                today_earned = source.get_balance_today()
            except:
                pass
                
            try:
                data_total = source.get_data_usage()
            except:
                pass
                
            try:
                data_today = source.get_data_usage_today()
            except:
                pass
            
            payout_rate = getattr(source, 'payout_rate', 1)

            # Umrechnung in USD für Nicht-USD-Währungen
            usd_conversion_rate = 1.0  # Standardwert für USD
            if source.currency in currency_exchange_rates:
                usd_conversion_rate = currency_exchange_rates[source.currency]

            result[name] = {
                "name": name,
                "status": status,
                "total_earned": total_earned,
                "today_earned": today_earned,
                "data_total": data_total,
                "data_today": data_today,
                "currency": source.currency,
                "payout_rate": payout_rate,
                "payout_amount": total_earned * payout_rate,
                "usd_value": total_earned * usd_conversion_rate  # USD-Wert für Zusammenfassung
            }
        except Exception as e:
            print(f"Fehler beim Verarbeiten von {name}: {e}")
            result[name] = {
                "name": name,
                "status": Status.ERROR.value,
                "total_earned": 0,
                "today_earned": 0,
                "data_total": 0,
                "data_today": 0,
                "currency": "$",
                "payout_rate": 1,
                "payout_amount": 0,
                "usd_value": 0  # USD-Wert für Fehlerfälle
            }
    
    return result


def display_data(data):
    """Zeigt die gesammelten Daten formatiert auf der Konsole an"""
    clear_screen()
    print(f"=== GELD MANAGER CLI === (Aktualisiert: {datetime.now().strftime('%H:%M:%S')})")
    print("=" * 110)
    
    # Mysterium-Daten separat prüfen
    if "Mysterium" in data and data["Mysterium"]["status"] == "ERROR":
        print("⚠️  MYSTERIUM VERBINDUNG FEHLGESCHLAGEN - API NICHT ERREICHBAR  ⚠️")

    # Header
    print(f"{'QUELLE':<15} {'STATUS':<10} {'HEUTE':<13} {'GESAMT':<11} {'AUSZAHL.RATE':<12} {'AUSZAHLG.':<11} {'DATEN HEUTE':<14} {'DATEN GESAMT':<15}")
    print("-" * 110)
    
    # Gesamtwerte für Zusammenfassung
    total_today = 0
    total_all = 0
    total_payout = 0
    total_data_today = 0
    total_data_all = 0
    
    # Daten für jede Quelle anzeigen
    for name, source_data in data.items():
        status_symbol = "✅" if source_data["status"] == "OK" else "❌"
        currency = source_data["currency"]
        
        today_earned = source_data["today_earned"]
        total_earned = source_data["total_earned"]
        
        # Datennutzung summieren
        total_data_today += source_data["data_today"]
        total_data_all += source_data["data_total"]
        
        # USD-basierte Summen für einheitliche Gesamtberechnung
        if currency == "$":
            # Bei USD direkt addieren
            total_today += today_earned
            total_all += total_earned
            total_payout += source_data["payout_amount"]
        else:
            # Bei anderen Währungen den USD-Wert verwenden
            total_today += source_data.get("usd_value", 0) * (today_earned / total_earned if total_earned > 0 else 0)
            total_all += source_data.get("usd_value", 0)
            total_payout += source_data["payout_amount"] * source_data.get("usd_value", 0) / total_earned if total_earned > 0 else 0

        # Formatierte Ausgabe mit korrekter Währungsdarstellung für alle Quellen
        payout_rate = source_data["payout_rate"]
        payout_amount = source_data["payout_amount"]
        print(f"{name:<15} {status_symbol:<10} {today_earned:.4f} {currency:<5} {total_earned:.4f} {currency:<5} "
              f"{payout_rate:.2f} {'':>7} {payout_amount:.4f} {currency:<5} "
              f"{format_bytes(source_data['data_today']):<15} {format_bytes(source_data['data_total']):<15}")
    
    print("-" * 110)
    print(f"{'GESAMT (USD)':<15} {'':<10} {total_today:.4f} ${'':>4} {total_all:.4f} ${'':>4} "
          f"{'':>12} {total_payout:.4f} ${'':>4} "
          f"{format_bytes(total_data_today):<15} {format_bytes(total_data_all):<15}")

    # Zeige an, dass Währungen in USD umgerechnet wurden
    if any(data[name]["currency"] != "$" for name in data):
        print(f"\nHinweis: Nicht-USD Währungen wurden zum aktuellen Kurs in USD umgerechnet.")

    # Statusprüfung für alle Dienste
    error_services = [name for name, source_data in data.items() if source_data["status"] != "OK"]
    if error_services:
        print(f"\n⚠️  DIENSTE MIT FEHLERN: {', '.join(error_services)}")

    print("\nDrücken Sie CTRL+C zum Beenden.")


def signal_handler(sig, frame):
    """Handler für CTRL+C-Abbruch"""
    print("\nProgramm wird beendet. Auf Wiedersehen!")
    sys.exit(0)


def main():
    """Hauptfunktion für die CLI-Anwendung"""
    signal.signal(signal.SIGINT, signal_handler)
    
    update_interval = 60  # Aktualisierung alle 60 Sekunden
    
    try:
        while True:
            data = get_sources_data()
            display_data(data)
            time.sleep(update_interval)
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
