from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests

app = Flask(__name__)
app.secret_key = "clinica_secret"

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")

# --- PACIENTES ---


@app.route("/")
def index():
    try:
        response = requests.get(f"{API_GATEWAY_URL}/api/v1/pacientes/pacientes/")
        response.raise_for_status()
        pacientes = response.json()
    except requests.exceptions.RequestException:
        pacientes = []
    return render_template("index.html", title="Pacientes", pacientes=pacientes)


@app.route("/pacientes/nuevo", methods=["GET", "POST"])
def nuevo_paciente():
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "cedula": request.form.get("cedula"),
            "email": request.form.get("email"),
            "telefono": request.form.get("telefono"),
        }
        try:
            response = requests.post(
                f"{API_GATEWAY_URL}/api/v1/pacientes/pacientes/", json=data
            )
            response.raise_for_status()
            flash("Paciente registrado exitosamente.", "success")
            return redirect(url_for("index"))
        except requests.exceptions.RequestException:
            flash("Error al registrar el paciente.", "danger")
    return render_template("form_paciente.html", title="Nuevo Paciente")


# --- CITAS ---


@app.route("/citas")
def citas():
    try:
        response = requests.get(f"{API_GATEWAY_URL}/api/v1/citas/citas/")
        response.raise_for_status()
        citas = response.json()
    except requests.exceptions.RequestException:
        citas = []
    return render_template("citas.html", title="Citas", citas=citas)


@app.route("/citas/nueva", methods=["GET", "POST"])
def nueva_cita():
    if request.method == "POST":
        data = {
            "paciente_id": int(request.form.get("paciente_id")),
            "fecha": request.form.get("fecha"),
            "medico": request.form.get("medico"),
            "estado": "programada",
        }
        try:
            response = requests.post(
                f"{API_GATEWAY_URL}/api/v1/citas/citas/", json=data
            )
            response.raise_for_status()
            flash("Cita agendada exitosamente.", "success")
            return redirect(url_for("citas"))
        except requests.exceptions.RequestException:
            flash("Error al agendar la cita.", "danger")
    return render_template("form_cita.html", title="Nueva Cita")


# --- HISTORIAL ---


@app.route("/historial")
def historial():
    try:
        response = requests.get(f"{API_GATEWAY_URL}/api/v1/historial/historial/")
        response.raise_for_status()
        registros = response.json()
    except requests.exceptions.RequestException:
        registros = []
    return render_template("historial.html", title="Historial", registros=registros)


@app.route("/historial/nuevo", methods=["GET", "POST"])
def nuevo_historial():
    if request.method == "POST":
        data = {
            "paciente_id": int(request.form.get("paciente_id")),
            "diagnostico": request.form.get("diagnostico"),
            "notas": request.form.get("notas"),
        }
        try:
            response = requests.post(
                f"{API_GATEWAY_URL}/api/v1/historial/historial/", json=data
            )
            response.raise_for_status()
            flash("Historial registrado exitosamente.", "success")
            return redirect(url_for("historial"))
        except requests.exceptions.RequestException:
            flash("Error al registrar el historial.", "danger")
    return render_template("form_historial.html", title="Nuevo Historial")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
