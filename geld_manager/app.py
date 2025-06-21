from flask import Flask, jsonify, render_template

from geld_manager.adnade import Adnade
from mysterium import Mysterium
from honeygain import Honeygain
from packetshare import PacketShare
from simple_sources import *


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/sources', methods=['GET'])
def get_sources():
    # Alle Quellen in einem Dictionary für einfachen Zugriff
    sources = {
        "Mysterium": Mysterium(),
        "Honeygain": Honeygain(),
        "Pawns": Pawns(),
        "Earnapp": EarnApp(),
        "PacketStream": PacketStream(),
        "Traffmonetizer": Traffmonetizer(),
        "RePocket": RePocket(),
        "EarnFM": EarnFM(),
        "PacketShare": PacketShare(),
        "Adnade": Adnade()
    }
    
    result = {}
    
    # Sammle Daten für jede Quelle
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
            
            result[name] = {
                "name": name,
                "status": status,
                "total_earned": total_earned,
                "today_earned": today_earned,
                "data_total": data_total,
                "data_today": data_today,
                "currency": source.currency
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
                "currency": "$"
            }
    
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6868)
