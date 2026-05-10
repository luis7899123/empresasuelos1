from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# =========================
# CONFIGURACIÓN EMAIL
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
# RUTAS
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

            return redirect("/contacto")

        except Exception as e:
            print("ERROR AL ENVIAR CORREO:", e)
            return f"Error al enviar correo: {e}", 500

    return render_template("contacto.html")


if __name__ == "__main__":
    app.run(debug=True)