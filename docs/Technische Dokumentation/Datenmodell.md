---
title: Datenmodell
parent: Technische Dokumentation
nav_order: 2
---

{: .label }
[Batool, Esma]

{: .no_toc }
## Datenmodell

![Datenmodell](../assets/images/data-model.png)

<details open markdown="block">
{: .text-delta }
<summary>Inhaltsverzeichnis</summary>
+ ToC
{: toc }
</details>

## Überblick

Das Datenmodell der WheelEats-Anwendung bildet alle zentralen Informationen ab, die für das Auffinden, Bewerten und Ergänzen barrierefreier Restaurants notwendig sind.  
Es basiert auf einer relationalen SQLite-Datenbank und ist so aufgebaut, dass Restaurants als zentrales Objekt fungieren, welches mit Nutzer:innen, Bewertungen, Fotos und Barrierefreiheitsmerkmalen verknüpft ist.

Zur besseren technischen Handhabung werden Feldnamen in der Datenbank ohne Sonderzeichen verwendet (z. B. `strasse`, `oeffnungszeiten`). In der Benutzeroberfläche werden diese Felder jedoch benutzerfreundlich dargestellt.

---

## Restaurant

Die Entität **Restaurant** ist das zentrale Element des Datenmodells. Sie speichert grundlegende Informationen zu einem Restaurant, darunter:

- Name und Adresse (`strasse`, `hausnummer`, `postleitzahl`, `stadt`)
- Geografische Koordinaten (`breitengrad`, `laengengrad`) für die Kartenansicht
- Beschreibung und Öffnungszeiten
- Website und optionale Quellenangabe
- Status (`pending` oder `approved`)
- Zeitstempel für Erstellung, Aktualisierung und Prüfung

Jedes Restaurant kann optional einem Nutzer zugeordnet sein, der es erstellt hat (`erstellt_von_nutzer_id`).  
Ein Restaurant kann mehrere Bewertungen und Fotos besitzen und ist genau einem Datensatz mit Barrierefreiheitsmerkmalen zugeordnet.

---

## Nutzer

Die Entität **Nutzer** repräsentiert registrierte Benutzer:innen der Anwendung. Gespeichert werden:

- Benutzername
- E-Mail-Adresse (eindeutig)
- Passwort-Hash
- Rolle (z. B. `user` oder `admin`)

Ein Nutzer kann mehrere Restaurants erstellen und mehrere Bewertungen verfassen.  
Administratoren besitzen zusätzliche Rechte, wie das Bearbeiten oder Löschen von Restaurants und Bewertungen.

---

## Bewertung

Die Entität **Bewertung** ermöglicht es Nutzer:innen, Restaurants zu bewerten und Feedback zu hinterlassen.  
Jede Bewertung ist genau einem Restaurant und genau einem Nutzer zugeordnet und enthält:

- eine Sternebewertung (1–5)
- einen optionalen Textkommentar
- einen Zeitstempel der Erstellung

Ein Restaurant kann mehrere Bewertungen haben, während jede Bewertung eindeutig einem Nutzer zugeordnet ist.

---

## Barrierefreie Merkmale

Die Entität **Barrierefreie Merkmale** ergänzt ein Restaurant um strukturierte Informationen zur Zugänglichkeit. Dazu zählen unter anderem:

- stufenloser Eingang
- barrierefreies WC
- breite Türen
- Behindertenparkplatz
- unterfahrbare Tische
- Rampe

Zwischen Restaurant und Barrierefreien Merkmalen besteht eine **1:1-Beziehung**.  
Dies wird technisch durch einen eindeutigen Foreign Key (`restaurant_id UNIQUE`) sichergestellt, sodass jedes Restaurant maximal einen Datensatz mit Barrierefreiheitsinformationen besitzt.

---

## Foto

Die Entität **Foto** speichert Bilder zu Restaurants. Jedes Foto ist genau einem Restaurant zugeordnet und enthält:

- den Dateipfad des Bildes
- ein Boolean-Feld `titelbild`, das angibt, ob es sich um das Hauptbild handelt

Ein Restaurant kann mehrere Fotos besitzen.  
Die Regel, dass pro Restaurant nur ein Titelbild existieren soll, wird durch die Anwendungslogik umgesetzt.

---

## Beziehungen im Überblick

- Ein Nutzer kann mehrere Restaurants erstellen (1:n)
- Ein Restaurant kann mehrere Bewertungen besitzen (1:n)
- Ein Nutzer kann mehrere Bewertungen abgeben (1:n)
- Ein Restaurant besitzt genau einen Satz barrierefreier Merkmale (1:1)
- Ein Restaurant kann mehrere Fotos besitzen (1:n)

---

## Zusammenfassung

Das dargestellte Datenmodell stellt sicher, dass Restaurants übersichtlich verwaltet, Barrierefreiheitsinformationen klar strukturiert erfasst und Nutzerbeiträge eindeutig zugeordnet werden können.  
Es bildet damit die technische Grundlage für alle Kernfunktionen der WheelEats-Anwendung.