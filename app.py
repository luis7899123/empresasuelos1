from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# =========================
# SECRET KEY
# =========================
app.secret_key = "super_secret_key_cambiar_en_produccion"

# =========================
# CONFIG EMAIL
# =========================
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_TIMEOUT"] = 15

mail = Mail(app)

# =========================
# USUARIOS SIMULADOS
# =========================
USUARIOS = {
    "admin": "1234",
    "usuario": "1234",
    "demo": "demo"
}

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USUARIOS and USUARIOS[username] == password:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            error = "Credenciales incorrectas"

    return render_template("login.html", error=error)


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# =========================
# WEB PÚBLICA (LIBRE)
# =========================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")


@app.route("/servicios")
def servicios():
    return render_template("servicios.html")


@app.route("/proyectos")
def proyectos():
    return render_template("proyectos.html")


# =========================
# CONTACTO (EMAIL)
# =========================
@app.route("/contacto", methods=["GET", "POST"])
def contacto():

    if request.method == "POST":
        try:
            nombre = request.form["nombre"]
            correo = request.form["correo"]
            telefono = request.form["telefono"]
            mensaje = request.form["mensaje"]

            msg = Message(
                subject="Nuevo mensaje desde la página web",
                recipients=["luiscm530@gmail.com"]
            )

            msg.body = f"""
NUEVO MENSAJE WEB

Nombre:
{nombre}

Correo:
{correo}

Teléfono:
{telefono}

Mensaje:
{mensaje}
"""

            mail.send(msg)
            return redirect(url_for("contacto"))

        except Exception as e:
            print("ERROR AL ENVIAR CORREO:", e)
            return f"Error al enviar correo: {e}", 500

    return render_template("contacto.html")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)