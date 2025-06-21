# Goldesel

Goldesel ist eine Sammlung von Automatisierungs Scripts in Docker Containern,
um verschiedene online Geldverdienstmöglichkeiten zu benutzen.

Es hat außerdem noch ein Web und CLI Dashboard und die Gewinne der verschiedenen Dienste zu überwachen.


## Dienste
Die folgenden Dienste werden unterstützt.

 - [eBesucher](https://www.ebesucher.de/?ref=Problemo1)
 - [Adnade](https://adnade.net/?ref=problemo)
 - [Mysterium](https://mystnodes.co/?referral_code=c33FxuedB3KczaVmOcUIKk79K2Er0rIvJRW9qXgg)
 - [Honeygain](https://r.honeygain.me/PROBLB3084)
 - [EarnFM](https://earn.fm/ref/JANEOHPV)
 - [EarnApp](https://earnapp.com/i/FM4GqAK9)
 - [Pawns](https://pawns.app/?r=14966712)
 - [Traffmonetizer](https://traffmonetizer.com/?aff=1369505)
 - [PacketStream](https://packetstream.io/?psr=5cAF)
 - [RePocket](https://link.repocket.com/Cn55)
 - [PacketShare](https://www.packetshare.io/?code=06E2D47A46481CEA)


## Installation
Zuerst müssen docker und docker compose installiert werden: https://docs.docker.com/engine/install/

Danach das repo clonen:
```bash
git clone https://github.com/Problemo57/goldesel
cd goldesel
```

### .env
Ändere die .env Datei zu deinen eigenden Werten.
```
NETWORK_MEASURE_MOUNT="/var/lib/goldesel"

# Name your Device however you want.
DEVICE_NAME="CHANGE ME"

EBESUCHER_SURFBAR_NAME="CHANGE ME"
ADNADE_USERNAME="CHANGE ME"

HONEYGAIN_EMAIL="CHANGE ME"
HONEYGAIN_PASSWORD="CHANGE ME"

PAWNS_EMAIL="CHANGE ME"
PAWNS_PASSWORD="CHANGE ME"

TRAFFMONETIZER_TOKEN='CHANGE ME'

#PACKETSTREAM
CID="CHANGE ME"

#Repocket
RP_EMAIL="CHANGE ME"
RP_API_KEY="CHANGE ME"

EARNFM_TOKEN="CHANGE ME"

PACKETSHARE_USERNAME="CHANGE ME"
PACKETSHARE_PASSWORD="CHANGE ME"
```

### Starten
```bash
bash start.sh
```

## Configuration nach dem Starten

Nach dem Starten müssen noch für Mysterium und earnapp Sachen gemacht werden.

### earnapp
```bash
docker compose logs earnapp
```
Klicke auf den Link, um das Gerät mit deinem Konto zu verbinden.

### Mysterium
Bei Mysterium musst du die Weboberfläche aufruffen und die Node konfigurieren.

http://<your-ip>:4449


## Dashboard
Das Web Dashboard mit der Übersicht über die Dienste ist hier zu finden:

http://<your-ip>:6868

Das CLI Dashboard ist via diesem Befehl aufrufbar:
```bash
docker compose exec -it geld_manager python3 cli.py
```
