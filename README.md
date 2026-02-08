# WheelEats

WheelEats ist eine serverseitig gerenderte Web-Applikation zur Suche und Bewertung von Restaurants mit Fokus auf Barrierefreiheit in Berlin-Mitte.  
Die Anwendung richtet sich insbesondere an Menschen mit Mobilitätseinschränkungen und ermöglicht das Finden, Bewerten und Ergänzen barrierefreundlicher Gastronomie.

--- 

### Voraussetzungen
- Python 3.11
- pip (wird mit Python installiert)
- virtuelle Python-Umgebung (venv empfohlen)


---

## Setup

1. Virtuelle Umgebung erstellen und aktivieren
   python -m venv venv
   venv\Scripts\activate   (Windows)

2. Abhängigkeiten installieren
   pip install -r requirements.txt

3. Datenbank initialisieren
   flask --app app init-db

4. Beispieldaten laden
   flask --app app seed-db

5. App starten
   flask --app app run


---
### Demo-Zugangsdaten für Adminfunktion 

# Admin-Account:
- E-Mail: batool@gmail.com
- Passwort: 12345678

# Admin-Account:
- E-mail: esma.gbsc@gmail.com
- Passwort: Demo12345

