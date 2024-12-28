"""API Module"""

import os
import tempfile
from flask import Flask, json, render_template, request, jsonify, send_file
from cifraclub import CifraClub
from get_pdf import create_pdf_with_columns_portrait as gen_pdf

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    """Home route"""
    return app.response_class(
        response=json.dumps({'api': 'Cifra Club API'}),
        status=200,
        mimetype='application/json'
    )


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    items = data["items"]
    file_name = data["fileName"]

    # Criando um arquivo temporário para armazenar o PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_file_path = temp_pdf.name  # Caminho do arquivo temporário

        # Gerar o PDF no arquivo temporário
        gen_pdf(items, temp_file_path)

        # Enviar o arquivo para o cliente
        try:
            return send_file(
                temp_file_path, as_attachment=True, download_name=f"{file_name}.pdf"
            )
        finally:
            # Após o envio, deletar o arquivo temporário
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


@app.route('/artists/<artist>/songs/<song>')
def get_cifra(artist, song):
    """Get cifra by artist and song"""
    cifrablub = CifraClub()
    musica = cifrablub.cifra(artist, song)

    saida = f"Artista: {musica['artist']}\nMusica: {musica['name']}\nYoutube: {musica['youtube_url']}\n\n"
    for cifra in musica['cifra']:
        saida = saida + "\n "+cifra
    return app.response_class(
        response=saida,
        status=200,
        mimetype="application/json",
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT', '3000'), debug=True)
