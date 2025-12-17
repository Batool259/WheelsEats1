from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME='pulse'
)

bootstrap = Bootstrap5(app)

# --- Platzhalter-Daten für die Startseite ------------------------------

@app.route("/")
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
    # Platzhalter-Liste
    return render_template("we_index.html", restaurants=restaurants)

# --- Detailseite mit Platzhalter ---------------------------------------

@app.route("/restaurants/<int:restaurant_id>")
def restaurant_detail(restaurant_id):
    # aktuell nur Platzhalter: wir geben die ID an das Template weiter
    return render_template("we_detail.html", restaurant_id=restaurant_id)

# --- Formular "Restaurant hinzufügen" (Platzhalter) --------------------

@app.route("/restaurants/new", methods=["GET", "POST"])
def restaurant_new():
    if request.method == "POST":
        # später würden wir hier die Formulardaten speichern
        flash("Vielen Dank, dein Restaurant wurde eingereicht (Platzhalter).", "success")
        return redirect(url_for("index"))
    return render_template("we_new.html")

# --- Karte (Platzhalter) -----------------------------------------------

@app.route("/map")
def restaurant_map():
    # später: Marker anhand von Koordinaten, aktuell nur Platzhalter
    return render_template("we_map.html")

# --- Fehlerseiten -------------------------------------------

@app.errorhandler(404)
def http_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def http_internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001) 
