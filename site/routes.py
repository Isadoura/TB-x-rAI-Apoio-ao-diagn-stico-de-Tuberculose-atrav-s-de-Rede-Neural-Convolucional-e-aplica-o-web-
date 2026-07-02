import os
import zipfile
import tempfile

from flask import render_template, request, redirect, flash
from werkzeug.utils import secure_filename

from sitemodelo import app
from sitemodelo.predicoes.predicao import analisar

ALLOWED_EXTENSIONS = {"zip"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("indexboot.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":

        if "file" not in request.files:
            flash("Nenhum arquivo enviado.")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("Nenhum arquivo selecionado.")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            zip_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(zip_path)

            extract_folder = tempfile.mkdtemp()

            try:
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_folder)

            except zipfile.BadZipFile:
                flash("Arquivo .zip inválido")
                return redirect(request.url)

            dados = analisar(extract_folder)

            return render_template(
                "resultadosboot.html",
                resultados=dados["resultados"],
                grafico=dados["grafico"],
                pizza=dados["pizza"],
                estatisticas=dados["estatisticas"]
            )
        
        flash("Envie um arquivo .zip")
        return redirect(request.url)
      
    return render_template("upload.html")

@app.route("/participantes")
def participantes():
    return render_template("participantes.html")

@app.route("/resultados")
def resultados():
    return render_template("resultadosboot.html")
