---
title: Designentscheidungen
nav_order: 4
---

{: .label }
[Batool, Esma]

## Überblick

In diesem Abschnitt werden zentrale Designentscheidungen dokumentiert, die während der Entwicklung von WheelEats getroffen wurden.  
Ziel war es, eine verständliche, barrierearme und technisch überschaubare Anwendung zu entwickeln, die den Fokus klar auf Nutzbarkeit und Zugänglichkeit legt.

---

## Entscheidung 1: Reduziertes, übersichtliches UI

**Problem:**  
Viele bestehende Plattformen sind visuell überladen und schwer bedienbar, insbesondere für Nutzer:innen mit Mobilitätseinschränkungen.

**Entscheidung:**  
Wir haben uns für ein reduziertes, klares Benutzerinterface mit wenigen Farben, klaren Strukturen und großen, gut lesbaren Elementen entschieden.

**Begründung:**  
Eine einfache Oberfläche senkt die Einstiegshürde und verbessert die Bedienbarkeit. Die Umsetzung orientiert sich an den in den UI-Designs und Wireframes entwickelten Entwürfen.

---

## Entscheidung 2: Restaurants als zentrales Datenobjekt

**Problem:**  
Die Daten müssen so strukturiert sein, dass Bewertungen, Fotos und Barrierefreiheitsinformationen eindeutig zugeordnet werden können.

**Entscheidung:**  
Restaurant ist das zentrale Objekt des Datenmodells. Alle weiteren Entitäten (Bewertung, Foto, Barrierefreie Merkmale) beziehen sich direkt darauf.

**Begründung:**  
Diese Struktur ist übersichtlich, leicht erweiterbar und ermöglicht einfache Abfragen (z. B. Detailansicht eines Restaurants).

---

## Entscheidung 3: Barrierefreiheitsmerkmale als eigene 1:1-Entität

**Problem:**  
Barrierefreiheitsinformationen sollen strukturiert, eindeutig und erweiterbar gespeichert werden.

**Entscheidung:**  
Barrierefreie Merkmale werden in einer eigenen Tabelle gespeichert und sind 1:1 mit einem Restaurant verknüpft.

**Begründung:**  
Die Trennung verhindert unübersichtliche Restaurant-Tabellen und erlaubt es, neue Merkmale später unkompliziert hinzuzufügen.

---

## Entscheidung 4: Statische Kartenansicht ohne JavaScript

**Problem:**  
Interaktive Kartenlösungen erfordern JavaScript und externe APIs, was die Komplexität erhöht.

**Entscheidung:**  
Wir verwenden eine statische Kartenansicht auf Basis von OpenStreetMap Static Maps.

**Begründung:**  
Die Lösung ist technisch einfach, barrierearm, schnell ladend und erfüllt dennoch den Zweck der räumlichen Orientierung.

---

## Entscheidung 5: Rollenmodell mit Administratoren

**Problem:**  
Nicht alle Nutzer:innen sollen die gleichen Rechte haben (z. B. Löschen oder Freigeben von Restaurants).

**Entscheidung:**  
Es wurde ein einfaches Rollenmodell mit normalen Nutzer:innen und Administratoren eingeführt.

**Begründung:**  
Admins können Inhalte prüfen, bearbeiten oder löschen, während normale Nutzer:innen Restaurants einreichen und bewerten können. Dies erhöht die Datenqualität.

---

## Entscheidung 6: Status `pending` / `approved` für Restaurants

**Problem:**  
Neu eingereichte Restaurants sollen nicht automatisch öffentlich sichtbar sein.

**Entscheidung:**  
Restaurants werden zunächst mit dem Status `pending` gespeichert und erst nach Prüfung auf `approved` gesetzt.

**Begründung:**  
Dies ermöglicht eine inhaltliche Kontrolle und stellt sicher, dass nur geprüfte Einträge öffentlich angezeigt werden.

---

## Zusammenfassung

Die getroffenen Designentscheidungen unterstützen das übergeordnete Ziel von WheelEats:  
eine leicht verständliche, barrierearme Plattform bereitzustellen, die relevante Informationen klar strukturiert darstellt und eine aktive Beteiligung der Nutzer:innen ermöglicht.