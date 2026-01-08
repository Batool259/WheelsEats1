import click
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Models
class Nutzer(db.Model):
    __tablename__ = "nutzer"

    id = db.Column(db.Integer, primary_key=True)
    benutzername = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    passwort_hash = db.Column(db.String(255), nullable=False)
    rolle = db.Column(db.String(50), nullable=False, default="user")

    restaurants = db.relationship("Restaurant", back_populates="erstellt_von", cascade="all, delete-orphan")
    bewertungen = db.relationship("Bewertung", back_populates="nutzer", cascade="all, delete-orphan")


class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)

    erstellt_von_nutzer_id = db.Column(db.Integer, db.ForeignKey("nutzer.id"), nullable=True, index=True)

    name = db.Column(db.String(255), nullable=False, index=True)
    strasse = db.Column(db.String(255), nullable=True)
    hausnummer = db.Column(db.String(50), nullable=True)
    postleitzahl = db.Column(db.String(20), nullable=True, index=True)
    stadt = db.Column(db.String(120), nullable=True, index=True)

    breitengrad = db.Column(db.Float, nullable=True)
    laengengrad = db.Column(db.Float, nullable=True)

    beschreibung = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="pending")
    oeffnungszeiten = db.Column(db.Text, nullable=True)
    quelle = db.Column(db.String(255), nullable=True)

    erstellt_am = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    aktualisiert_am = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    geprueft_am = db.Column(db.DateTime, nullable=True)

    erstellt_von = db.relationship("Nutzer", back_populates="restaurants")
    bewertungen = db.relationship("Bewertung", back_populates="restaurant", cascade="all, delete-orphan")
    fotos = db.relationship("Foto", back_populates="restaurant", cascade="all, delete-orphan")

    merkmale = db.relationship(
        "BarrierefreieMerkmale",
        back_populates="restaurant",
        uselist=False,
        cascade="all, delete-orphan",
    )

    @property
    def adresse_zeile(self) -> str:
        parts = []
        if self.strasse:
            if self.hausnummer:
                parts.append(f"{self.strasse} {self.hausnummer}")
            else:
                parts.append(self.strasse)
        if self.postleitzahl or self.stadt:
            parts.append(f"{self.postleitzahl or ''} {self.stadt or ''}".strip())
        return ", ".join([p for p in parts if p])


class BarrierefreieMerkmale(db.Model):
    __tablename__ = "barrierefreie_merkmale"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False, unique=True, index=True)

    stufenloser_eingang = db.Column(db.Boolean, nullable=False, default=False)
    barrierefreies_wc = db.Column(db.Boolean, nullable=False, default=False)
    breite_tueren = db.Column(db.Boolean, nullable=False, default=False)
    behindertenparkplatz = db.Column(db.Boolean, nullable=False, default=False)
    unterfahrbare_tische = db.Column(db.Boolean, nullable=False, default=False)
    rampe = db.Column(db.Boolean, nullable=False, default=False)

    restaurant = db.relationship("Restaurant", back_populates="merkmale")


class Foto(db.Model):
    __tablename__ = "foto"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False, index=True)

    dateipfad = db.Column(db.String(500), nullable=False)
    titelbild = db.Column(db.Boolean, nullable=False, default=False)

    restaurant = db.relationship("Restaurant", back_populates="fotos")


class Bewertung(db.Model):
    __tablename__ = "bewertung"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False, index=True)
    nutzer_id = db.Column(db.Integer, db.ForeignKey("nutzer.id"), nullable=False, index=True)

    sterne = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=True)
    erstellt_am = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    restaurant = db.relationship("Restaurant", back_populates="bewertungen")
    nutzer = db.relationship("Nutzer", back_populates="bewertungen")



# CLI: init-db / seed-db (werden in app.py registriert)
def register_commands(app):
    @app.cli.command("init-db")
    def init_db_command():
        db.drop_all()
        db.create_all()
        click.echo("✅ Datenbank wurde neu initialisiert (wheeleats.sqlite).")

    @app.cli.command("seed-db")
    def seed_db_command():
        insert_sample()
        click.echo("✅ Demo-Daten wurden eingefügt.")

def insert_sample():
    # Alles leeren
    db.session.query(Bewertung).delete()
    db.session.query(Foto).delete()
    db.session.query(BarrierefreieMerkmale).delete()
    db.session.query(Restaurant).delete()
    db.session.query(Nutzer).delete()
    db.session.commit()



    # Nutzer anlegen
    u1 = Nutzer(benutzername="Admin", email="Wheeleats@example.com", passwort_hash="demo", rolle="admin")
    u2 = Nutzer(benutzername="Tim K.", email="tim@example.com", passwort_hash="demo", rolle="user")
    u3 = Nutzer(benutzername="Gisela Hoffmann", email="gisela@example.com", passwort_hash="demo", rolle="user")
    u4 = Nutzer(benutzername="Karl-Heinz Schneider", email="karlheinz@example.com", passwort_hash="demo", rolle="user")
    u5 = Nutzer(benutzername="Renate Berger", email="renate@example.com", passwort_hash="demo", rolle="user")
    u6 = Nutzer(benutzername="Wolfgang Peters", email="wolfgang@example.com", passwort_hash="demo", rolle="user")
    u7 = Nutzer(benutzername="Ingrid Lehmann", email="ingrid@example.com", passwort_hash="demo", rolle="user")

    db.session.add_all([u1, u2, u3, u4, u5, u6, u7])
    db.session.commit()  # wichtig, damit alle IDs existieren



    # Restaurant 1
    r1 = Restaurant(
        erstellt_von_nutzer_id=u1.id,
        name="Alvis Restaurant",
        strasse="Albrechtstraße",
        hausnummer="8",
        postleitzahl="10117",
        stadt="Berlin",
        breitengrad=52.5235,
        laengengrad=13.3889,
        beschreibung="Modernes Restaurant mit regionaler Küche und guter Barrierefreiheit.",
        oeffnungszeiten="Mo – Sa: 12:00 – 22:00" \
                        "So: Geschlossen", 
        status="approved",
        geprueft_am=datetime.utcnow(),
    )

    r1.merkmale = BarrierefreieMerkmale(
        stufenloser_eingang=True,
        barrierefreies_wc=True,
        breite_tueren=True,
    )

    r1.fotos = [
        Foto(
            dateipfad="static/images/alvis_1.jpeg",
            titelbild=True
        )
    ]

    # Restaurant 2
    r2 = Restaurant(
        erstellt_von_nutzer_id=u1.id,
        name="Fischer und Lustig",
        strasse="Poststraße",
        hausnummer="28",
        postleitzahl="10178",
        stadt="Berlin",
        breitengrad=52.5173,
        laengengrad=13.4059,
        beschreibung=" Wir bringen Fleisch & Fisch auf den Tisch. Regional und traditionell – " 
        "aber quergedacht..",
        oeffnungszeiten="Mo – Sa: 11:30 – 00:00\nSo: Geschlossen", 
        status="approved",
        geprueft_am=datetime.utcnow(),
    )

    r2.merkmale = BarrierefreieMerkmale(
        rampe=True,
        breite_tueren=True
    )

    r2.fotos = [
        Foto(
            dateipfad="static/images/fischer&lustig_1.jpeg",
            titelbild=True
        )
    ]


    # Restaurant 3
    r3 = Restaurant(
        erstellt_von_nutzer_id=u1.id,
        name=" Il Punto",
        strasse="Neustaedtische Kirchstraße",
        hausnummer="6",
        postleitzahl="10117",
        stadt="Berlin",
        breitengrad=52.5189, 
        laengengrad=13.3855,
        beschreibung="Saisonale Speisen aus handerlesenen Zutaten. "
        "Gepaart mit einem Wein oder einem Cocktail werden Sie und Ihre Gäste auf eine " 
        "kulinarische und vinologische Reise geschickt.",
        oeffnungszeiten="Mo – Fr: 12:00 – 23:00\nSa: 17:00 - 20:00\nSo: Geschlossen", 
        status="approved",
        geprueft_am=datetime.utcnow(), 
    )
    

    r3.merkmale = BarrierefreieMerkmale(
        stufenloser_eingang=True,
        unterfahrbare_tische=True,
        rampe=True,
    )

    r3.fotos = [
        Foto(
            dateipfad="static/images/il_punto_1.jpeg",
            titelbild=True
        )
    ]


    
    # Restaurant 4
    r4 = Restaurant(
        erstellt_von_nutzer_id=u3.id,
        name="Nante-Eck",
        strasse="Unter den Linden",
        hausnummer="35",
        postleitzahl="10117",
        stadt="Berlin",
        breitengrad=52.5166, 
        laengengrad=13.3882,
        beschreibung="Urige Altberliner Restauration mit typischem Flair Berlins um 1900 – "
        "direkt an der Ecke Unter den Linden / Friedrichstraße. "
        "Berliner Küche nach alten Rezepten sowie moderne Hausmannskost.",
        oeffnungszeiten="Mo – So: 11:30 – 23:30\n(Warme Speisen bis 22:00)", 
        status="approved",
        geprueft_am=datetime.utcnow(), 
    )
    
    r4.merkmale = BarrierefreieMerkmale(
        unterfahrbare_tische=True,
        rampe=True,
        breite_tueren=True,
        behindertenparkplatz=True,
    )

    r4.fotos = [
        Foto(
            dateipfad="static/images/nante_eck_1.jpeg",
            titelbild=True
        )
    ]


    # Restaurant 5
    r5 = Restaurant(
        erstellt_von_nutzer_id=u2.id,
        name="Schnitzelei Mitte",
        strasse="Friedrichstraße",
        hausnummer="185-190",
        postleitzahl="10117",
        stadt="Berlin",
        breitengrad=52.5287, 
        laengengrad=13.3884,
        beschreibung= "Traditionelles deutsches Lokal mit klassischem Ambiente und "
        "beliebten Gerichten wie Schnitzel, regionaler Küche und freundlichem Service.",
        oeffnungszeiten="Mo – Sa: 11:30 – 23:00\nSo: Geschlossen", 
        status="approved",
        geprueft_am=datetime.utcnow(), 
    )
    
    r5.merkmale = BarrierefreieMerkmale(
        unterfahrbare_tische=True,
        rampe=True,
        behindertenparkplatz=True,
    )

    r5.fotos = [
        Foto(
            dateipfad="static/images/schnitzelei_1.jpeg",
            titelbild=True
        )
    ]


 # Restaurant 6
    r6 = Restaurant(
        erstellt_von_nutzer_id=u1.id,
        name="Käfer – Dachgarten Restaurant",
        strasse="Platz der Republik",
        hausnummer="1",
        postleitzahl="10557",
        stadt="Berlin",
        breitengrad=52.5186, 
        laengengrad=13.3761,
        beschreibung= "Käfer Dachgarten Restaurant am Reichstag mit Panoramablick über Berlin "
        "und kreativer moderner Küche – ein Highlight für Besucher und Einheimische.",
        oeffnungszeiten="Mo – So: 11:30 – 23:00", 
        status="approved",
        geprueft_am=datetime.utcnow(), 
    )
    
    r6.merkmale = BarrierefreieMerkmale(
        unterfahrbare_tische=True,
        rampe=True,
        behindertenparkplatz=True,
    )

    r6.fotos = [
        Foto(
            dateipfad="static/images/kaefer_dachgarten_restaurant_1.jpeg",
            titelbild=True
        )
    ]



 # Restaurant 7
    r7 = Restaurant(
        erstellt_von_nutzer_id=u1.id,
        name="MANI Restaurant",
        strasse="Torstraße",
        hausnummer="4",
        postleitzahl="10119",
        stadt="Berlin",
        breitengrad=52.5295, 
        laengengrad=13.3996,
        beschreibung= "Mediterranes Restaurant in Berlin-Mitte bei Rosenthaler Platz, bekannt "
        "für vielfältige mediterrane Küche und beliebt bei Foodies.",
        oeffnungszeiten="Mo – Sa: 12:00 – 23:00", 
        status="approved",
        geprueft_am=datetime.utcnow(), 
    )
    
    r7.merkmale = BarrierefreieMerkmale(
        unterfahrbare_tische=True,
        rampe=True,
        behindertenparkplatz=True,
        stufenloser_eingang=True,
        barrierefreies_wc=True,
    )

    r7.fotos = [
        Foto(
            dateipfad="static/images/mani_1.jpeg",
            titelbild=True
        )
    ]




    # Speichern
    db.session.add_all([r1, r2, r3, r4, r5, r6, r7])
    db.session.commit()


    # Bewertungen
    db.session.add_all([
        # r1 — Alvis Restaurant (3 Bewertungen)
        Bewertung(restaurant_id=r1.id, nutzer_id=u5.id, sterne=5, text="Sehr gut erreichbar. Stufenloser Eingang und breite Türen machen vieles leichter."),
        Bewertung(restaurant_id=r1.id, nutzer_id=u6.id, sterne=4, text="Barrierefreies WC vorhanden, insgesamt angenehm. Bei viel Betrieb etwas eng."),
        Bewertung(restaurant_id=r1.id, nutzer_id=u7.id, sterne=3, text="Gutes Essen und freundlicher Service. Zur Stoßzeit aber recht voll im Innenraum."),

        # r2 — Fischer und Lustig (2 Bewertungen)
        Bewertung(restaurant_id=r2.id, nutzer_id=u5.id, sterne=4, text="Rampe am Eingang funktioniert gut, Türen sind breit genug."),
        Bewertung(restaurant_id=r2.id, nutzer_id=u6.id, sterne=2, text="Sehr voll und laut. Mit Rollstuhl eher mühsam, auch wenn der Zugang grundsätzlich klappt."),

        # r3 — Il Punto (5 Bewertungen)
        Bewertung(restaurant_id=r3.id, nutzer_id=u3.id, sterne=5, text="Unterfahrbare Tische sind ein großes Plus. Zugang stufenlos und entspannt."),
        Bewertung(restaurant_id=r3.id, nutzer_id=u4.id, sterne=4, text="Rampe und Platzangebot gut. Musik war etwas laut, sonst sehr angenehm."),
        Bewertung(restaurant_id=r3.id, nutzer_id=u5.id, sterne=4, text="Service aufmerksam und hilfsbereit. Man fühlt sich ernst genommen."),
        Bewertung(restaurant_id=r3.id, nutzer_id=u6.id, sterne=3, text="Gutes Konzept, aber zeitweise hektisch."),
        Bewertung(restaurant_id=r3.id, nutzer_id=u7.id, sterne=2, text="Heute recht voll und unruhig. Barrierefreiheit vorhanden, aber nicht ideal nutzbar."),

        # r4 — Nante-Eck (1 Bewertung)
        Bewertung(restaurant_id=r4.id, nutzer_id=u4.id, sterne=3, text="Rampe vorhanden und Türen breit. Innenraum allerdings recht eng bei Betrieb."),

        # r5 — Schnitzelei Mitte (4 Bewertungen)
        Bewertung(restaurant_id=r5.id, nutzer_id=u3.id, sterne=4, text="Rampe vorhanden, unterfahrbarer Tisch möglich. Essen gut."),
        Bewertung(restaurant_id=r5.id, nutzer_id=u5.id, sterne=3, text="Zugang klappt, aber zwischen den Tischen oft eng."),
        Bewertung(restaurant_id=r5.id, nutzer_id=u6.id, sterne=2, text="Sehr voll und wenig Bewegungsfreiheit. Positiv: Personal bemüht."),
        Bewertung(restaurant_id=r5.id, nutzer_id=u7.id, sterne=3, text="Solide Erfahrung. Barrierefreiheit ok, aber nichts Besonderes."),

        # r6 — Käfer – Dachgarten Restaurant (2 Bewertungen)
        Bewertung(restaurant_id=r6.id, nutzer_id=u4.id, sterne=5, text="Sehr gute Organisation. Zugang klappt, Tisch war gut nutzbar."),
        Bewertung(restaurant_id=r6.id, nutzer_id=u5.id, sterne=3, text="Tolle Aussicht, aber sehr touristisch und hektisch bei Andrang."),

        # r7 — MANI Restaurant (4 Bewertungen)
        Bewertung(restaurant_id=r7.id, nutzer_id=u3.id, sterne=5, text="Stufenloser Zugang und barrierefreies WC vorhanden. Sehr gut umgesetzt."),
        Bewertung(restaurant_id=r7.id, nutzer_id=u4.id, sterne=4, text="Unterfahrbare Tische und Rampe vorhanden. Abends sehr voll."),
        Bewertung(restaurant_id=r7.id, nutzer_id=u6.id, sterne=2, text="Heute lange Wartezeit und viel Trubel."),
        Bewertung(restaurant_id=r7.id, nutzer_id=u7.id, sterne=3, text="Gute Küche, aber nur eingeschränkt entspannt bei hoher Auslastung."),
    ])
    db.session.commit()
