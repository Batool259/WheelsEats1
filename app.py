from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    session
)
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY="secret_key_just_for_dev_environment",
    BOOTSTRAP_BOOTSWATCH_THEME="pulse",
)

bootstrap = Bootstrap5(app)

# ---------------------------------------------------------
# Start: "/" -> Login
# ---------------------------------------------------------
@app.route("/")
def home():
    return redirect(url_for("index"))

# ---------------------------------------------------------
# Login (Demo, ohne DB)
# ---------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Demo-Login: einfach merken, dass User "eingeloggt" ist
        session["logged_in"] = True
        flash("Login erfolgreich (Demo).", "success")
        return redirect(url_for("index"))

    return render_template("login.html")

# ---------------------------------------------------------
# Registrierung (Demo, ohne Speicherung)
# ---------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        flash(
            "Registrierung erfolgreich (Demo – Daten werden noch nicht gespeichert). "
            "Bitte jetzt einloggen.",
            "success",
        )
        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------------------------------------------------
# Logout
# ---------------------------------------------------------
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Du wurdest ausgeloggt (Demo).", "info")
    return redirect(url_for("login"))

# ---------------------------------------------------------
# Startseite (Restaurants-Liste)
# ---------------------------------------------------------
@app.route("/index")
def index():
    restaurants = [
        {
            "id": 1,
            "name": 'Restaurant "Zur alten Laterne"',
            "address": "Kantstraße 123, 10625 Berlin",
            "features": ["Ebenerdig", "WC"],
        },
        {
            "id": 2,
            "name": "Pizzeria Bella Italia",
            "address": "Friedrichstraße 45, 10117 Berlin",
            "features": ["Ebenerdig", "WC", "Rampe", ">90cm Tür"],
        },
    ]
    return render_template("index.html", restaurants=restaurants)

# ---------------------------------------------------------
# Detailseite
# ---------------------------------------------------------
@app.route("/restaurants/<int:restaurant_id>")
def restaurant_detail(restaurant_id):
    return render_template("detail.html", restaurant_id=restaurant_id)

@app.route("/restaurants/<int:restaurant_id>/reviews", methods=["POST"])
def restaurant_review_create(restaurant_id):
    if not session.get("logged_in"):
        flash("Bitte einloggen, um eine Bewertung abzugeben.", "warning")
        return redirect(url_for("login"))

    # Demo: wir speichern noch nichts
    sterne = request.form.get("sterne")
    text = request.form.get("text")

    flash("Danke! Deine Bewertung wurde gespeichert (Demo – noch ohne Datenbank).", "success")
    return redirect(url_for("restaurant_detail", restaurant_id=restaurant_id))


# ---------------------------------------------------------
# Restaurant hinzufügen (nur wenn "eingeloggt")
# ---------------------------------------------------------
@app.route("/restaurants/new", methods=["GET", "POST"])
def restaurant_new():
    if not session.get("logged_in"):
        flash("Bitte einloggen, um ein Restaurant einzureichen.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        flash(
            "Vielen Dank, dein Restaurant wurde eingereicht (Platzhalter).",
            "success",
        )
        return redirect(url_for("index"))

    return render_template("new.html")

# ---------------------------------------------------------
# Karte
# ---------------------------------------------------------
@app.route("/map")
def restaurant_map():
    return render_template("map.html")

# ---------------------------------------------------------
# Fehlerseiten
# ---------------------------------------------------------
@app.errorhandler(404)
def http_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def http_internal_server_error(e):
    return render_template("500.html"), 500

# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
