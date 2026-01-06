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

    u1 = Nutzer(benutzername="Lisa Müller", email="lisa@example.com", passwort_hash="demo", rolle="user")
    u2 = Nutzer(benutzername="Tim K.", email="tim@example.com", passwort_hash="demo", rolle="user")
    db.session.add_all([u1, u2])
    db.session.commit()

    r1 = Restaurant(
        erstellt_von_nutzer_id=u1.id,
        name="Café am Neuen See",
        strasse="Lichtensteinallee",
        hausnummer="2",
        postleitzahl="10787",
        stadt="Berlin",
        breitengrad=52.5109,
        laengengrad=13.3477,
        beschreibung="Beliebtes Café im Tiergarten mit guter Zugänglichkeit.",
        oeffnungszeiten="Mo–So: 10:00–22:00",
        status="approved",
        geprueft_am=datetime.utcnow(),
    )
    r1.merkmale = BarrierefreieMerkmale(
        stufenloser_eingang=True,
        barrierefreies_wc=True,
        rampe=True,
    )

    r1.fotos = [Foto(
        dateipfad="static/images/restaurant_demo_1.jpeg",
        titelbild=True
    )]

    r2 = Restaurant(
        erstellt_von_nutzer_id=u2.id,
        name="Pizzeria Napoli",
        strasse="Hauptstraße",
        hausnummer="45",
        postleitzahl="10969",
        stadt="Berlin",
        breitengrad=52.5049,
        laengengrad=13.4030,
        beschreibung="Italienische Klassiker, freundlich und zentral.",
        oeffnungszeiten="Di–So: 12:00–23:00",
        status="approved",
        geprueft_am=datetime.utcnow(),
    )

    r2.fotos = [Foto(
    dateipfad="static/images/restaurant_demo_1.jpeg",
    titelbild=True
)]
    r2.merkmale = BarrierefreieMerkmale(rampe=True, breite_tueren=True)

    db.session.add_all([r1, r2])
    db.session.commit()

    db.session.add_all([
        Bewertung(restaurant_id=r1.id, nutzer_id=u1.id, sterne=5, text="Fantastisch! Rampe sehr gut nutzbar."),
        Bewertung(restaurant_id=r1.id, nutzer_id=u2.id, sterne=4, text="WC ist barrierefrei, Spiegel etwas hoch."),
    ])
    db.session.commit()
