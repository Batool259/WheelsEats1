from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME='pulse'
)

bootstrap = Bootstrap5(app)

# WheelEats – Startseite
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
        {
            "id": 3,
            "name": "Curry 36",
            "address": "Mehringdamm 36, 10961 Berlin",
            "features": ["Ebenerdig"],
        },
    ]
    return render_template("we_index.html", restaurants=restaurants)


# WheelEats – Detailseite
@app.route("/restaurants/<int:restaurant_id>")
def restaurant_detail(restaurant_id):
    return render_template("we_detail.html", restaurant_id=restaurant_id)


# WheelEats – Formular „Restaurant hinzufügen“
@app.route("/restaurants/new", methods=["GET", "POST"])
def restaurant_new():
    if request.method == "POST":
        flash("Vielen Dank, dein Restaurant wurde eingereicht (Platzhalter).", "success")
        return redirect(url_for("index"))
    return render_template("we_new.html")


# WheelEats – Map-Seite
@app.route("/map")
def restaurant_map():
    return render_template("we_map.html")


# Fehlerseiten
@app.errorhandler(404)
def http_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def http_internal_server_error(e):
    return render_template("500.html"), 500


# Beispielseiten
@app.get("/faq/<css>")
@app.get("/faq/", defaults={"css": "default"})
def faq(css):
    return render_template("faq.html", css=css)


@app.get("/ex/<int:id>")
@app.get("/ex/", defaults={"id": 1})
def ex(id):
    if id == 1:
        return render_template("ex1.html")
    elif id == 2:
        return render_template("ex2.html")
    else:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
