from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests

app = Flask(__name__)
app.secret_key = "clinica_secret"

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")


def obtener_pacientes():
    try:
        response = requests.get(f"{API_GATEWAY_URL}/api/v1/pacientes/pacientes/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []


def obtener_citas():
    try:
        response = requests.get(f"{API_GATEWAY_URL}/api/v1/citas/citas/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []


def obtener_historial():
    try:
        response = requests.get(f"{API_GATEWAY_URL}/api/v1/historial/historial/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []


# --- DASHBOARD ---


@app.route("/")
def index():
    pacientes = obtener_pacientes()
    citas = obtener_citas()
    historial = obtener_historial()
    citas_programadas = [c for c in citas if c.get("estado") == "programada"]
    return render_template(
        "index.html",
        title="Dashboard",
        total_pacientes=len(pacientes),
        total_citas=len(citas),
        total_historial=len(historial),
        citas_programadas=len(citas_programadas),
        ultimos_pacientes=pacientes[-5:][::-1],
        ultimas_citas=citas[-5:][::-1],
    )


# --- PACIENTES ---


@app.route("/pacientes")
def pacientes():
    lista = obtener_pacientes()
    return render_template("pacientes.html", title="Pacientes", pacientes=lista)


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
            return redirect(url_for("pacientes"))
        except requests.exceptions.RequestException:
            flash("Error al registrar el paciente.", "danger")
    return render_template("form_paciente.html", title="Nuevo Paciente")


@app.route("/pacientes/<int:paciente_id>")
def detalle_paciente(paciente_id):
    try:
        p = requests.get(
            f"{API_GATEWAY_URL}/api/v1/pacientes/pacientes/{paciente_id}"
        ).json()
        citas = requests.get(f"{API_GATEWAY_URL}/api/v1/citas/citas/").json()
        historial = requests.get(
            f"{API_GATEWAY_URL}/api/v1/historial/historial/"
        ).json()
        citas_paciente = [c for c in citas if c.get("paciente_id") == paciente_id]
        historial_paciente = [
            h for h in historial if h.get("paciente_id") == paciente_id
        ]
    except requests.exceptions.RequestException:
        flash("Error al cargar el paciente.", "danger")
        return redirect(url_for("pacientes"))
    return render_template(
        "detalle_paciente.html",
        title=f"Paciente: {p.get('nombre')}",
        paciente=p,
        citas=citas_paciente,
        historial=historial_paciente,
    )


@app.route("/pacientes/<int:paciente_id>/eliminar", methods=["POST"])
def eliminar_paciente(paciente_id):
    try:
        requests.delete(f"{API_GATEWAY_URL}/api/v1/pacientes/pacientes/{paciente_id}")
        flash("Paciente eliminado.", "success")
    except requests.exceptions.RequestException:
        flash("Error al eliminar el paciente.", "danger")
    return redirect(url_for("pacientes"))


# --- CITAS ---


@app.route("/citas")
def citas():
    lista = obtener_citas()
    return render_template("citas.html", title="Citas", citas=lista)


@app.route("/citas/nueva", methods=["GET", "POST"])
def nueva_cita():
    pacientes = obtener_pacientes()
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
    return render_template("form_cita.html", title="Nueva Cita", pacientes=pacientes)


@app.route("/citas/<int:cita_id>/estado", methods=["POST"])
def cambiar_estado_cita(cita_id):
    nuevo_estado = request.form.get("estado")
    try:
        requests.patch(
            f"{API_GATEWAY_URL}/api/v1/citas/citas/{cita_id}",
            json={"estado": nuevo_estado},
        )
        flash(f"Estado actualizado a '{nuevo_estado}'.", "success")
    except requests.exceptions.RequestException:
        flash("Error al actualizar el estado.", "danger")
    return redirect(url_for("citas"))


@app.route("/citas/<int:cita_id>/eliminar", methods=["POST"])
def eliminar_cita(cita_id):
    try:
        requests.delete(f"{API_GATEWAY_URL}/api/v1/citas/citas/{cita_id}")
        flash("Cita eliminada.", "success")
    except requests.exceptions.RequestException:
        flash("Error al eliminar la cita.", "danger")
    return redirect(url_for("citas"))


# --- HISTORIAL ---


@app.route("/historial")
def historial():
    lista = obtener_historial()
    return render_template("historial.html", title="Historial", registros=lista)


@app.route("/historial/nuevo", methods=["GET", "POST"])
def nuevo_historial():
    pacientes = obtener_pacientes()
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
    return render_template(
        "form_historial.html", title="Nuevo Historial", pacientes=pacientes
    )


@app.route("/historial/<int:historial_id>/eliminar", methods=["POST"])
def eliminar_historial(historial_id):
    try:
        requests.delete(f"{API_GATEWAY_URL}/api/v1/historial/historial/{historial_id}")
        flash("Registro eliminado.", "success")
    except requests.exceptions.RequestException:
        flash("Error al eliminar el registro.", "danger")
    return redirect(url_for("historial"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
