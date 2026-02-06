---
title: Referenz / API
parent: Technical Docs
nav_order: 3
---

{: .label }
[Batool, Esma]

{: .no_toc }
## Reference documentation

{: .attention }
> This page collects internal functions, routes with their functions, and APIs (if any).
> 
> See [Uber](https://developer.uber.com/docs/drivers/references/api) or [PayPal](https://developer.paypal.com/api/rest/) for exemplary high-quality API reference documentation.
>
> You may delete this `attention` box.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## [Section / module]

### `function_definition()`

**Route:** `/route/`

**Methods:** `POST` `GET` `PATCH` `PUT` `DELETE`

**Purpose:** [Short explanation of what the function does and why]

**Sample output:**

[Show an image, string output, or similar illustration -- or write NONE if function generates no output]

---
## Authentifizierung

### `home()`

**Route:** `/`

**Methods:** `GET`

**Purpose:**  
Einstiegspunkt der Anwendung. Leitet Nutzer automatisch auf die Startseite (`/index`) weiter.

**Sample output:**  
NONE

---

### `login()`

**Route:** `/login`

**Methods:** `GET` `POST`

**Purpose:**  
Zeigt den Login-Screen an und authentifiziert Nutzer im Demo-Modus. Nach erfolgreichem Login erhalten Nutzer Zugriff auf geschützte Funktionen.

**Sample output:**  
Login-Formular (E-Mail, Passwort)

---

### `register()`

**Route:** `/register`

**Methods:** `GET` `POST`

**Purpose:**  
Ermöglicht neuen Nutzern die Registrierung. Die Registrierung ist aktuell als Demo umgesetzt und speichert noch keine Daten dauerhaft.

**Sample output:**  
Registrierungsformular

---

### `logout()`

**Route:** `/logout`

**Methods:** `GET`

**Purpose:**  
Loggt den aktuell eingeloggten Nutzer aus und beendet die Sitzung.

**Sample output:**  
Weiterleitung zur Login-Seite mit Hinweisnachricht

---

## Restaurants

### `index()`

**Route:** `/index`

**Methods:** `GET`

**Purpose:**  
Startseite der Anwendung. Zeigt eine Übersicht barrierefreier Restaurants mit grundlegenden Informationen.

**Sample output:**  
Restaurant-Übersichtsliste

---

### `restaurant_detail(restaurant_id)`

**Route:** `/restaurants/<int:restaurant_id>`

**Methods:** `GET`

**Purpose:**  
Zeigt die Detailseite eines Restaurants anhand der übergebenen Restaurant-ID.

**Sample output:**  
Restaurant-Detailansicht

---

### `restaurant_new()`

**Route:** `/restaurants/new`

**Methods:** `GET` `POST`

**Purpose:**  
Ermöglicht eingeloggten Nutzern, ein neues Restaurant einzureichen. Nicht eingeloggte Nutzer werden zur Login-Seite weitergeleitet.

**Sample output:**  
Formular zum Hinzufügen eines Restaurants

---

## Bewertungen

### `restaurant_review_create(restaurant_id)`

**Route:** `/restaurants/<int:restaurant_id>/reviews`

**Methods:** `POST`

**Purpose:**  
Ermöglicht eingeloggten Nutzern, eine Bewertung für ein Restaurant abzugeben. Bewertungen werden aktuell nur im Demo-Modus verarbeitet.

**Sample output:**  
Erfolgsmeldung nach dem Absenden der Bewertung

---

## Karte

### `restaurant_map()`

**Route:** `/map`

**Methods:** `GET`

**Purpose:**  
Zeigt eine Kartenansicht der Restaurants. Die Funktion ist derzeit als Platzhalter umgesetzt.

**Sample output:**  
Kartenansicht (Platzhalter)

---

## Fehlerbehandlung

### `http_not_found(e)`

**Route:** `*`

**Methods:** `GET`

**Purpose:**  
Wird ausgelöst, wenn eine angeforderte Route nicht existiert.

**Sample output:**  
404-Fehlerseite

---

### `http_internal_server_error(e)`

**Route:** `*`

**Methods:** `GET`

**Purpose:**  
Wird ausgelöst, wenn ein interner Serverfehler auftritt.

**Sample output:**  
500-Fehlerseite
