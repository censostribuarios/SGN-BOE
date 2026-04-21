"""
API web - Gestoría SGN
Recibe peticiones del formulario web, lanza la búsqueda en el BOE
y devuelve el resultado en formato JSON.
Se despliega en Railway, Render o similar (gratuito).
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from boe_motor import consultar

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el formulario web


@app.route("/consultar", methods=["POST"])
def endpoint_consultar():
    datos = request.get_json()
    matricula = datos.get("matricula", "").strip().upper()
    nif = datos.get("nif", "").strip().upper()

    if not matricula:
        return jsonify({"error": "Matrícula requerida"}), 400

    resultado = consultar(matricula, nif)
    return jsonify(resultado)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"estado": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
