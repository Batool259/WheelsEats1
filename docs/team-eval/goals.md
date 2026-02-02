---
title: Goals
parent: Team Evaluation
nav_order: 1
---

{: .label }
[Batool, Esma]

{: .no_toc }

# Erreichte und nicht erreichte Ziele

## Ursprüngliche Projektziele

Zu Beginn des Projekts war unser zentrales Ziel, eine Webanwendung zu entwickeln, die Menschen dabei unterstützt, barrierefreie Restaurants in Berlin-Mitte zu finden.  
Dabei wollten wir insbesondere strukturierte, verlässliche und vergleichbare Informationen zur Barrierefreiheit bereitstellen.

Unsere wichtigsten Ziele waren:

- Übersichtliche Darstellung barrierefreier Restaurants  
- Strukturierte Modellierung von Barrierefreiheitsmerkmalen (keine Freitexte)  
- Such- und Filterfunktionen für Nutzer:innen  
- Community-basierte Beiträge und Bewertungen  
- Rollenbasiertes System (Admin vs. normale Nutzer:innen)  
- Umsetzung einer vollständigen Full-Stack-Webanwendung (Frontend, Backend, Datenbank)


## Erreichte Ziele

Den Großteil unserer Kernziele konnten wir erfolgreich umsetzen.

### Funktionale Ziele

- Wir haben eine funktionierende Full-Stack-Webanwendung mit Flask, SQLAlchemy und Bootstrap implementiert.
- Restaurants können angelegt, angezeigt, bearbeitet und gelöscht werden.
- Barrierefreiheitsmerkmale sind als strukturierte Attribute modelliert (z. B. stufenloser Eingang, barrierefreies WC, breite Türen).
- Nutzer:innen können Restaurants anhand dieser Merkmale filtern.
- Jedes Restaurant besitzt eine Detailansicht mit:
  - Beschreibung  
  - Öffnungszeiten  
  - Standort  
  - externer Website  
  - optioanl Titelbild 
- Community-Bewertungen sind möglich.
- Ein Admin-System ist vorhanden, mit dem wir:
  - Restaurants freigeben oder ablehnen, sowei Status setzten können
  - alle Restaurantdaten bearbeiten können  
  - Titelbilder verwalten können  


### Technische Ziele

- Wir haben ein relationales Datenbankschema entworfen und umgesetzt.
- Die Anwendung nutzt serverseitiges Rendering mit Jinja-Templates.
- Datei-Uploads für Restauranttitelbilder sind implementiert.
- Grundlegende Validierung erfolgt im Backend.
- Rollenbasierte Zugriffskontrolle schützt administrative Funktionen.


## Teilweise oder nicht erreichte Ziele

Einige Ziele konnten wir nur eingeschränkt oder nicht vollständig umsetzen.

### Nicht oder nur teilweise erreichte Punkte

- Keine automatische Geokodierung:  
  Koordinaten müssen manuell eingegeben werden, statt automatisch aus der Adresse berechnet zu werden.
- Keine interaktive Kartenintegration:  
  Die Karte ist statisch und zeigt keine dynamischen Marker.
- Begrenzte Validierung der Barrierefreiheit:  
  Die Angaben basieren auf Nutzer:innen-Eingaben und werden nicht extern überprüft.
- Keine Nutzerprofile:  
  Nutzer:innen können keine Profile oder persönliche Bewertungsverläufe einsehen.


## Gründe für nicht erreichte Ziele

Die Hauptgründe für die nicht umgesetzten Funktionen waren:

- Begrenzte Entwicklungszeit im Semester.
- Fokussierung auf Kernfunktionalität statt Zusatzfeatures.
- Technische Komplexität externer APIs (z. B. Karten- und Geokodierungsdienste).
- Priorisierung von Stabilität und Verständlichkeit gegenüber Feature-Vielfalt.



## Gesamtbewertung

Insgesamt haben wir das Hauptziel unseres Projekts erreicht:  
Wir haben eine funktionierende Plattform entwickelt, die strukturierte Informationen zu barrierefreien Restaurants bereitstellt.

Auch wenn einige weiterführende Funktionen fehlen, ist das System stabil, logisch aufgebaut und gut nutzbar.  
Das Projekt zeigt aus unserer Sicht eine solide Umsetzung von Full-Stack-Webentwicklung, Datenmodellierung und nutzerzentriertem Design.

Die nicht erreichten Ziele betreffen vor allem optionale Erweiterungen und beeinträchtigen die grundlegende Nutzbarkeit der Anwendung nicht.


<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>
