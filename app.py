from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_bootstrap import Bootstrap

from db import db, Restaurant, Bewertung, register_commands

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY="secret_key_just_for_dev_environment",
    BOOTSTRAP_BOOTSWATCH_THEME="pulse",
    SQLALCHEMY_DATABASE_URI="sqlite:///wheeleats.sqlite",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# DB an Flask-App binden
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
@app.route("/restaurants/new", methods=["GET", "POST"])
def restaurant_new():
    if not session.get("logged_in"):
        flash("Bitte einloggen, um ein Restaurant einzureichen.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        flash("Vielen Dank, dein Restaurant wurde eingereicht (Platzhalter).", "success")
        return redirect(url_for("index"))

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
