import os
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, flash, session, abort
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from db import db, Restaurant, Bewertung, BarrierefreieMerkmale, Foto, Nutzer, register_commands


# Upload-Sicherheit
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

def is_admin() -> bool:
    return session.get("role") == "admin"

def require_admin():
    if not session.get("logged_in"):
        abort(403)
    if not is_admin():
        abort(403)

app.config.from_mapping(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
    BOOTSTRAP_BOOTSWATCH_THEME=None,
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

# Regsiter
@app.route("/register", methods=["GET", "POST"])
def register():
    # ✅ CHANGED: next kann aus POST oder GET kommen
    next_url = request.form.get("next") or request.args.get("next")

    # Sicherheitscheck: nur interne Pfade erlauben
    if next_url and not next_url.startswith("/"):
        next_url = None

    if request.method == "POST":
        benutzername = request.form.get("benutzername", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")

        if not benutzername or not email:
            flash("Bitte Benutzername und E-Mail angeben.", "warning")
            return render_template("register.html", next=next_url)

        if len(password) < 8:
            flash("Passwort muss mindestens 8 Zeichen haben.", "warning")
            return render_template("register.html", next=next_url)

        if password != password2:
            flash("Passwörter stimmen nicht überein.", "warning")
            return render_template("register.html", next=next_url)

        if Nutzer.query.filter_by(email=email).first():
            flash("Diese E-Mail ist bereits registriert.", "warning")
            return render_template("register.html", next=next_url)

        user = Nutzer(
            benutzername=benutzername,
            email=email,
            passwort_hash=generate_password_hash(password),
            rolle="user"
        )
        db.session.add(user)
        db.session.commit()

        # ✅ Direkt einloggen, damit du danach sofort "Restaurant hinzufügen" nutzen kannst
        session["logged_in"] = True
        session["user_id"] = user.id
        session["username"] = user.benutzername
        session["role"] = user.rolle

        flash("Registrierung erfolgreich! Du bist jetzt eingeloggt ✅", "success")
        return redirect(next_url or url_for("index"))

    return render_template("register.html", next=next_url)


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = Nutzer.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.passwort_hash, password):
            flash("E-Mail oder Passwort falsch.", "danger")
            return render_template("login.html")

        session["logged_in"] = True
        session["user_id"] = user.id
        session["username"] = user.benutzername
        session["role"] = user.rolle



        flash(f"Willkommen, {user.benutzername}!", "success")

        # ✅ CHANGED: next nutzen (POST oder GET)
        next_url = request.form.get("next") or request.args.get("next")
        if next_url and not next_url.startswith("/"):
            next_url = None

        return redirect(next_url or url_for("index"))

    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Du wurdest ausgeloggt.", "info")
    return redirect(url_for("login"))

@app.route("/index")
def index():
    q = request.args.get("q", "").strip()

    # Filter aus Querystring (Checkboxen)
    filters = {
        "stufenloser_eingang": request.args.get("stufenloser_eingang") == "1",
        "rampe": request.args.get("rampe") == "1",
        "barrierefreies_wc": request.args.get("barrierefreies_wc") == "1",
        "breite_tueren": request.args.get("breite_tueren") == "1",
        "unterfahrbare_tische": request.args.get("unterfahrbare_tische") == "1",
        "behindertenparkplatz": request.args.get("behindertenparkplatz") == "1",
    }

    query = Restaurant.query

    # Suche (Name/Adresse)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (Restaurant.name.ilike(like))
            | (Restaurant.strasse.ilike(like))
            | (Restaurant.postleitzahl.ilike(like))
            | (Restaurant.stadt.ilike(like))
        )

    # Wenn irgendein Filter aktiv ist → join auf Merkmale
    if any(filters.values()):
        query = query.join(Restaurant.merkmale)

        # Nur Restaurants, die das jeweilige Merkmal wirklich haben
        for key, enabled in filters.items():
            if enabled:
                query = query.filter(getattr(BarrierefreieMerkmale, key).is_(True))

    restaurants = query.order_by(Restaurant.name.asc()).all()

    return render_template("index.html", restaurants=restaurants, q=q, filters=filters)


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



@app.route("/restaurants/<int:id>/edit", methods=["GET", "POST"])
def restaurant_edit(id):
    # 🔒 Nur eingeloggte Admins
    if not session.get("logged_in"):
        abort(403)
    if not is_admin():
        abort(403)

    restaurant = Restaurant.query.get_or_404(id)

    if request.method == "POST":
        # Koordinaten
        bg = (request.form.get("breitengrad") or "").strip()
        lg = (request.form.get("laengengrad") or "").strip()

        try:
            restaurant.breitengrad = float(bg) if bg else None
            restaurant.laengengrad = float(lg) if lg else None
        except ValueError:
            flash("Bitte gültige Koordinaten eingeben.", "danger")
            return render_template("edit_restaurant.html", restaurant=restaurant)

        # Öffnungszeiten
        restaurant.oeffnungszeiten = (request.form.get("oeffnungszeiten") or "").strip() or None

        # Status setzen
        status = (request.form.get("status") or "").strip()
        if status in ("pending", "approved"):
            restaurant.status = status
            if status == "approved" and not restaurant.geprueft_am:
                restaurant.geprueft_am = datetime.utcnow()
        
        # Merkmale speichern / aktualisieren
        if restaurant.merkmale:
            m = restaurant.merkmale
        else:
            m = BarrierefreieMerkmale()
            restaurant.merkmale = m

        m.stufenloser_eingang = request.form.get("stufenloser_eingang") == "on"
        m.rampe = request.form.get("rampe") == "on"
        m.barrierefreies_wc = request.form.get("barrierefreies_wc") == "on"
        m.breite_tueren = request.form.get("breite_tueren") == "on"
        m.unterfahrbare_tische = request.form.get("unterfahrbare_tische") == "on"
        m.behindertenparkplatz = request.form.get("behindertenparkplatz") == "on"


        # Titelbild löschen?
        delete_flag = request.form.get("delete_titelbild") == "1"

        # Upload (optional)
        file = request.files.get("titelbild")

        upload_dir = app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)

        def get_current_cover():
            if not restaurant.fotos:
                return None
            for f in restaurant.fotos:
                if f.titelbild:
                    return f
            return None

        current_cover = get_current_cover()

        # 1) Löschen hat Priorität
        if delete_flag and current_cover:
            if file and file.filename:
                flash("Hinweis: Du hast gleichzeitig 'Titelbild löschen' und eine neue Datei gewählt. Es wurde nur gelöscht.", "warning")

            # Datei auf Platte löschen
            # current_cover.dateipfad ist z.B. "static/uploads/xyz.jpg"
            abs_path = os.path.join(app.root_path, current_cover.dateipfad)
            if os.path.exists(abs_path):
                os.remove(abs_path)

            # DB-Eintrag löschen
            db.session.delete(current_cover)
            current_cover = None


        # 2) Ersetzen, wenn neue Datei hochgeladen wurde
        elif file and file.filename:
            if not allowed_file(file.filename):
                flash("Nur Bilddateien (png, jpg, jpeg, webp) sind erlaubt.", "danger")
                return render_template("edit_restaurant.html", restaurant=restaurant)

            filename = secure_filename(file.filename)

            save_path = os.path.join(upload_dir, filename)
            if os.path.exists(save_path):
                filename = f"{int(datetime.utcnow().timestamp())}_{filename}"
                save_path = os.path.join(upload_dir, filename)

            file.save(save_path)

            # altes Titelbild entfernen (Datei + DB)
            if current_cover:
                old_abs_path = os.path.join(app.root_path, current_cover.dateipfad)
                if os.path.exists(old_abs_path):
                    os.remove(old_abs_path)
                db.session.delete(current_cover)

            # neues Titelbild speichern
            rel_path = f"static/uploads/{filename}"
            restaurant.fotos.append(Foto(dateipfad=rel_path, titelbild=True))


        db.session.commit()
        flash("Änderungen gespeichert.", "success")
        return redirect(url_for("detail", id=restaurant.id))

    return render_template("edit_restaurant.html", restaurant=restaurant)



@app.route("/restaurants/<int:id>/reviews", methods=["POST"])
def restaurant_review_create(id):
    if not session.get("logged_in"):
        flash("Bitte einloggen, um eine Bewertung abzugeben.", "warning")
        return redirect(url_for("login"))

    sterne = int(request.form.get("sterne", "0"))
    text = (request.form.get("text") or "").strip() or None

    if sterne < 1 or sterne > 5:
        flash("Bitte Sterne von 1 bis 5 wählen.", "danger")
        return redirect(url_for("detail", id=id))

    review = Bewertung(
        restaurant_id=id,
        nutzer_id=session["user_id"],
        sterne=sterne,
        text=text,
    )

    db.session.add(review)
    db.session.commit()

    flash("Danke! Deine Bewertung wurde gespeichert", "success")
    return redirect(url_for("detail", id=id))


# Bewertung Löschen
@app.route("/reviews/<int:id>/delete", methods=["POST"])
def review_delete(id):
    require_admin()

    b = Bewertung.query.get_or_404(id)
    restaurant_id = b.restaurant_id

    db.session.delete(b)
    db.session.commit()

    flash("Bewertung wurde gelöscht.", "success")
    return redirect(url_for("detail", id=restaurant_id))



# Restaurant hinzufügen (nur wenn "eingeloggt")
def _to_bool(name: str) -> bool:
    return request.form.get(name) == "on"


@app.route("/restaurants/new", methods=["GET", "POST"])
def restaurant_new():
    if not session.get("logged_in"):
        flash("Bitte einloggen, um ein Restaurant einzureichen.", "warning")
        return redirect(url_for("login", next=request.path))

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("Bitte gib einen Namen für das Restaurant an.", "danger")
            return render_template("new.html")

        r = Restaurant(
            name=name,
            strasse=(request.form.get("strasse") or "").strip() or None,
            hausnummer=(request.form.get("hausnummer") or "").strip() or None,
            postleitzahl=(request.form.get("postleitzahl") or "").strip() or None,
            stadt=(request.form.get("stadt") or "").strip() or None,
            beschreibung=(request.form.get("beschreibung") or "").strip() or None,
            status="pending",
            erstellt_von_nutzer_id=session["user_id"],
        )

        # optional: Koordinaten (robust)
        bg = (request.form.get("breitengrad") or "").strip()
        lg = (request.form.get("laengengrad") or "").strip()
        try:
            r.breitengrad = float(bg) if bg else None
            r.laengengrad = float(lg) if lg else None
        except ValueError:
            flash("Bitte gültige Koordinaten eingeben (z.B. 52.5200 und 13.4050).", "danger")
            return render_template("new.html")

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
            if not allowed_file(file.filename):
                flash("Nur Bilddateien (png, jpg, jpeg, webp) sind erlaubt.", "danger")
                return redirect(request.url)

            filename = secure_filename(file.filename)

            upload_dir = app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_dir, exist_ok=True)

            save_path = os.path.join(upload_dir, filename)
            if os.path.exists(save_path):
                filename = f"{int(datetime.utcnow().timestamp())}_{filename}"
                save_path = os.path.join(upload_dir, filename)

            file.save(save_path)

            rel_path = f"static/uploads/{filename}"
            r.fotos = [Foto(dateipfad=rel_path, titelbild=True)]

        db.session.commit()

        flash("Restaurant wurde gespeichert ✅", "success")
        return redirect(url_for("detail", id=r.id))

    return render_template("new.html")



# Restaurant löschen (nur Admin)
@app.route("/restaurants/<int:id>/delete", methods=["POST"])
def restaurant_delete(id):
    require_admin()

    r = Restaurant.query.get_or_404(id)

    # Optional: Fotos-Dateien löschen (nur wenn ihr das wirklich wollt)
    # (wir können das auch später machen)

    db.session.delete(r)
    db.session.commit()

    flash("Restaurant wurde gelöscht.", "success")
    return redirect(url_for("index"))



# Karte
@app.route("/map")
def restaurant_map():
    restaurants = (
        Restaurant.query
        .filter(Restaurant.breitengrad.isnot(None), Restaurant.laengengrad.isnot(None))
        .order_by(Restaurant.name.asc())
        .all()
    )

    # in "normale" dicts umwandeln (JSON-serialisierbar)
    restaurants_data = []
    for r in restaurants:
        restaurants_data.append({
            "id": r.id,
            "name": r.name,
            "lat": r.breitengrad,
            "lng": r.laengengrad,
            "adresse": " ".join([x for x in [r.strasse, r.hausnummer, r.postleitzahl, r.stadt] if x]),
            "detail_url": url_for("detail", id=r.id),
        })

    return render_template("map.html", restaurants=restaurants_data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

