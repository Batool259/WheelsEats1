import os
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from db import db, Restaurant, Bewertung, register_commands, BarrierefreieMerkmale, Foto

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY="secret_key_just_for_dev_environment",
    BOOTSTRAP_BOOTSWATCH_THEME="pulse",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    UPLOAD_FOLDER="static/uploads",
    MAX_CONTENT_LENGTH=6 * 1024 * 1024,
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)
DB_PATH = os.path.join(INSTANCE_DIR, "wheeleats.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

db.init_app(app)

# CLI Commands registrieren: flask init-db / seed-db
register_commands(app)

# Bootstrap (optional)
bootstrap = Bootstrap(app)


# Start: "/" -> Index
@app.route("/")
def home():
    return redirect(url_for("index"))


# Login (Demo, ohne DB)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["logged_in"] = True
        flash("Login erfolgreich (Demo).", "success")
        return redirect(url_for("index"))
    return render_template("login.html")


# Registrierung (Demo, ohne Speicherung)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        flash(
            "Registrierung erfolgreich (Demo – Daten werden noch nicht gespeichert). Bitte jetzt einloggen.",
            "success",
        )
        return redirect(url_for("login"))
    return render_template("register.html")


# Logout
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Du wurdest ausgeloggt (Demo).", "info")
    return redirect(url_for("login"))


# Startseite (Restaurants-Liste) + Suche
@app.route("/index")
def index():
    q = request.args.get("q", "").strip()

    query = Restaurant.query

    if q:
        like = f"%{q}%"
        query = query.filter(
            (Restaurant.name.ilike(like))
            | (Restaurant.strasse.ilike(like))
            | (Restaurant.postleitzahl.ilike(like))
            | (Restaurant.stadt.ilike(like))
        )

    restaurants = query.order_by(Restaurant.name.asc()).all()
    return render_template("index.html", restaurants=restaurants, q=q)


# Detailseite
@app.route("/restaurants/<int:id>")
def detail(id):
    restaurant = Restaurant.query.get_or_404(id)

    # Bewertungen laden (neueste zuerst)
    bewertungen = Bewertung.query.filter_by(restaurant_id=id).order_by(Bewertung.erstellt_am.desc()).all()

    # Durchschnitt (für Anzeige)
    if bewertungen:
        avg = sum(b.sterne for b in bewertungen) / len(bewertungen)
    else:
        avg = None

    return render_template("detail.html", restaurant=restaurant, bewertungen=bewertungen, avg=avg)


@app.route("/restaurants/<int:id>/reviews", methods=["POST"])
def restaurant_review_create(id):
    if not session.get("logged_in"):
        flash("Bitte einloggen, um eine Bewertung abzugeben.", "warning")
        return redirect(url_for("login"))

    # Demo: wir speichern noch nichts
    sterne = request.form.get("sterne")
    text = request.form.get("text")

    flash("Danke! Deine Bewertung wurde gespeichert (Demo – noch ohne Datenbank).", "success")
    return redirect(url_for("detail", id=id))


# Restaurant hinzufügen (nur wenn "eingeloggt")
def _to_bool(name: str) -> bool:
    return request.form.get(name) == "on"


@app.route("/restaurants/new", methods=["GET", "POST"])
def restaurant_new():
    if not session.get("logged_in"):
        flash("Bitte einloggen, um ein Restaurant einzureichen.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("Bitte gib einen Namen für das Restaurant an.", "danger")
            return render_template("new.html")

        r = Restaurant(
            # solange du nur Demo-Login hast, lass das weg:
            # erstellt_von_nutzer_id=session.get("user_id"),
            name=name,
            strasse=(request.form.get("strasse") or "").strip() or None,
            hausnummer=(request.form.get("hausnummer") or "").strip() or None,
            postleitzahl=(request.form.get("postleitzahl") or "").strip() or None,
            stadt=(request.form.get("stadt") or "").strip() or None,
            beschreibung=(request.form.get("beschreibung") or "").strip() or None,
            status="pending",
        )

        # optional: Koordinaten
        bg = (request.form.get("breitengrad") or "").strip()
        lg = (request.form.get("laengengrad") or "").strip()
        r.breitengrad = float(bg) if bg else None
        r.laengengrad = float(lg) if lg else None

        r.merkmale = BarrierefreieMerkmale(
            stufenloser_eingang=_to_bool("stufenloser_eingang"),
            rampe=_to_bool("rampe"),
            barrierefreies_wc=_to_bool("barrierefreies_wc"),
            breite_tueren=_to_bool("breite_tueren"),
            unterfahrbare_tische=_to_bool("unterfahrbare_tische"),
            behindertenparkplatz=_to_bool("behindertenparkplatz"),
        )

        db.session.add(r)
        db.session.flush()  # damit r.id existiert

        file = request.files.get("titelbild")
        if file and file.filename:
            filename = secure_filename(file.filename)

            upload_dir = app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_dir, exist_ok=True)

            save_path = os.path.join(upload_dir, filename)
            if os.path.exists(save_path):
                filename = f"{int(datetime.utcnow().timestamp())}_{filename}"
                save_path = os.path.join(upload_dir, filename)

            file.save(save_path)

            r.fotos = [Foto(dateipfad=save_path.replace("\\", "/"), titelbild=True)]

        db.session.commit()

        flash("Restaurant wurde gespeichert ✅", "success")
        return redirect(url_for("detail", id=r.id))

    return render_template("new.html")

# Karte
@app.route("/map")
def restaurant_map():
    return render_template("map.html")


# Fehlerseiten
@app.errorhandler(404)
def http_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def http_internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
