---
title: Architektur
nav_order: 1
parent: Technische Dokumentation
---

## Überblick

WheelEats ist eine webbasierte Anwendung auf Basis von **Flask** (Backend) mit **Jinja2 Templates** (Server-side Rendering) und einer **SQLite-Datenbank** über **SQLAlchemy ORM**. Nutzer:innen können Restaurants anlegen, Details einsehen, Fotos hochladen und Bewertungen abgeben. Zusätzlich gibt es eine Kartenansicht zur Orientierung.

Die Anwendung ist bewusst schlank gehalten: keine komplexen Frontend-Frameworks, sondern klare Seiten und Formulare, damit die Bedienung möglichst einfach bleibt.

## Komponenten

### Backend (Flask)
- Routing und Request-Handling (z. B. Listenansicht, Detailansicht, Login/Logout)
- Validierung von Formulardaten
- Zugriff auf Datenbank über SQLAlchemy
- Upload-Handling für Bilder (Speichern im `static/uploads/`-Ordner)

### Datenhaltung (SQLite + SQLAlchemy)
- Persistenz aller Kernobjekte: Nutzer, Restaurants, Bewertungen, Fotos, Barrierefreiheitsmerkmale
- Beziehungen werden über Foreign Keys und ORM-Relations abgebildet

### Frontend (Templates + CSS)
- HTML-Templates in `templates/`
- Styles in `static/css/`
- Bilder in `static/uploads/` bzw. `static/images/`

### Dokumentation
- Projektdokumentation im Ordner `docs/`
- Navigation und Seitenstruktur über YAML-Frontmatter (`title`, `nav_order`, `parent`)

## Ordnerstruktur (Kurzüberblick)

- `app.py`: Einstieg, Flask-App, Routen, Business-Logik
- `db.py`: SQLAlchemy-Setup und Datenmodelle
- `templates/`: HTML-Templates (z. B. Start, Login, Detailseiten)
- `static/css/`: Stylesheets
- `static/uploads/`: hochgeladene Bilder
- `instance/`: SQLite-Datenbank (lokale Instanz)
- `docs/`: Projektdokumentation

## Typische Abläufe (Request-Flows)

### (1) Login
1. Nutzer:in sendet Login-Formular (E-Mail/Passwort)
2. Backend prüft Zugangsdaten (Passwort-Hash)
3. Bei Erfolg: Session wird gesetzt, Nutzer:in gelangt zur Übersicht

### (2) Restaurant anlegen
1. Formular „Restaurant hinzufügen“ wird ausgefüllt
2. Backend validiert Eingaben (Pflichtfelder)
3. Restaurant wird in DB gespeichert
4. Optionale Barrierefreiheitsmerkmale werden gespeichert (1:1)
5. Rückleitung zur Detailseite

### (3) Restaurant anzeigen (Detail)
1. Nutzer:in öffnet Detailseite eines Restaurants
2. Backend lädt:
   - Restaurantdaten
   - Barrierefreiheitsmerkmale
   - Fotos
   - Bewertungen
3. Anzeige im Template

### (4) Bewertung abgeben
1. Formular (Sterne + Text) wird abgesendet
2. Backend speichert Bewertung mit Zeitstempel
3. Detailseite zeigt neue Bewertung

### (5) Foto hochladen
1. Nutzer:in wählt Bild und lädt hoch
2. Backend speichert Datei im Upload-Ordner
3. DB speichert Pfad + Zuordnung zum Restaurant
4. Optional kann ein Foto als Titelbild markiert werden (Anwendungslogik)

## Sicherheit & Zugriff
- Passwörter werden als Hash gespeichert
- Bestimmte Aktionen (z. B. hinzufügen/bewerten) sind nur nach Login möglich
- Eingaben werden serverseitig geprüft (Pflichtfelder, Datentypen)