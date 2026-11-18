"""Servidor Flask: entrega o site e responde /api/ordenar. Rode: python servidor.py"""
from flask import Flask, jsonify, request, send_from_directory
from algoritmo import ALGORITMOS, gerar_vetor

app = Flask(__name__, static_folder="demo", static_url_path="")


@app.get("/")
def index():
    return send_from_directory("demo", "index.html")


@app.post("/api/ordenar")
def ordenar():
    d = request.get_json(force=True)
    algoritmo = d.get("algoritmo", "quick")
    if algoritmo not in ALGORITMOS:
        return jsonify(erro="algoritmo inválido"), 400
    vetor = d.get("vetor")                       # reaproveita o array ao trocar de algoritmo
    if not vetor:
        n = max(4, min(50, int(d.get("n", 20))))
        vetor = gerar_vetor(n, d.get("cenario", "aleatorio"))
    return jsonify(ALGORITMOS[algoritmo](vetor))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
