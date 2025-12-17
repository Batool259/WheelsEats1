---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
[Batool, Esma]

{: .no_toc }
## Data model

![datamodel](../assets/images/data-model.jpeg)

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Datenmodell – Beschreibung

Das Datenmodell der WheelEats-App bildet alle zentralen Informationen ab, die für das Auffinden, Bewerten und Ergänzen barrierefreier Restaurants notwendig sind. Es besteht aus mehreren miteinander verknüpften Entitäten, die klar definierte Aufgaben haben.

# Restaurant

Die zentrale Entität des Modells ist Restaurant. Sie speichert grundlegende Informationen zu einem Restaurant, darunter Name, Adresse (Straße, Hausnummer, Postleitzahl, Stadt), geografische Koordinaten (Breiten- und Längengrad), Beschreibung, Öffnungszeiten sowie Metadaten wie Erstellungs-, Aktualisierungs- und Prüfdatum.
Jedes Restaurant wird von einem Nutzer erstellt (erstellt_von_nutzer_id) und kann mehrere Bewertungen, Fotos und barrierefreie Merkmale besitzen.

# Nutzer

Die Entität Nutzer repräsentiert registrierte Benutzer der App. Gespeichert werden Benutzername, E-Mail-Adresse (eindeutig), Passwort-Hash sowie eine Rolle (z. B. normaler Nutzer oder Administrator).
Ein Nutzer kann mehrere Restaurants erstellen und mehrere Bewertungen abgeben.

# Bewertung

Die Entität Bewertung ermöglicht es Nutzern, Restaurants zu bewerten. Jede Bewertung ist genau einem Restaurant und einem Nutzer zugeordnet. Sie enthält eine Sternebewertung, einen Textkommentar sowie den Zeitpunkt der Erstellung.
Ein Restaurant kann mehrere Bewertungen haben, während jede Bewertung nur von einem Nutzer stammt.

# Barrierefreie Merkmale

Die Entität Barrierefreie Merkmale ergänzt ein Restaurant um detaillierte Informationen zur Zugänglichkeit. Dazu zählen unter anderem stufenloser Eingang, barrierefreies WC, breite Türen, Behindertenparkplätze, unterfahrbare Tische und eine Rampe.
Zwischen Restaurant und barrierefreien Merkmalen besteht eine 1:1-Beziehung, da jedes Restaurant genau einen Satz an Barrierefreiheitsinformationen besitzt.

# Foto

Die Entität Foto speichert Bilder zu Restaurants. Jedes Foto ist einem Restaurant zugeordnet und enthält einen Dateipfad sowie ein Flag, das angibt, ob es sich um das Titelbild handelt.
Ein Restaurant kann mehrere Fotos haben, ein Foto gehört jedoch immer genau zu einem Restaurant.

# Beziehungen im Überblick

Ein Nutzer kann mehrere Restaurants erstellen (1:n).

Ein Restaurant kann mehrere Bewertungen haben (1:n).

Ein Nutzer kann mehrere Bewertungen abgeben (1:n).

Ein Restaurant besitzt genau einen Satz barrierefreier Merkmale (1:1).

Ein Restaurant kann mehrere Fotos haben (1:n).

Dieses Datenmodell stellt sicher, dass Restaurants übersichtlich dargestellt, barrierefreie Informationen strukturiert erfasst und Nutzerbeiträge eindeutig zugeordnet werden können. Es bildet damit die technische Grundlage für die Kernfunktionen der WheelEats-Website.