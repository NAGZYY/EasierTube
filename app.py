from flask import Flask, request, Response, send_file
from flask_cors import CORS
import os, uuid, json, time

from processor import process_video
from utils import extract_audio

from werkzeug.utils import secure_filename # Ajoute cet import en haut

import platform
import subprocess

app = Flask(__name__, static_folder="static")
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
AUDIO_UPLOAD = "uploads/audio"
AUDIO_OUTPUT = "output/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(AUDIO_UPLOAD, exist_ok=True)
os.makedirs(AUDIO_OUTPUT, exist_ok=True)


# ─────────────────────────────
# PAGE PRINCIPALE
# ─────────────────────────────
@app.route("/")
def index():
    return app.send_static_file("index.html")


# ─────────────────────────────
# XML VIDEO (INCHANGÉ)
# ─────────────────────────────
@app.route("/process", methods=["POST"])
def process():
    if "file" not in request.files:
        return {"error": "Aucun fichier"}, 400

    file = request.files["file"]
    job_id = str(uuid.uuid4())

    sensitivity = request.form.get("sensitivity", "normal")
    margin_ms = int(request.form.get("margin_ms", 120))

    input_path = os.path.join(UPLOAD_FOLDER, f"{job_id}.mp4")
    output_xml = os.path.join(OUTPUT_FOLDER, f"{job_id}.xml")

    file.save(input_path)

    def stream():
        for progress, status in process_video(
            input_path, output_xml, job_id, sensitivity, margin_ms
        ):
            yield json.dumps({
                "progress": progress,
                "status": status
            }) + "\n"

        yield json.dumps({
            "progress": 100,
            "done": True,
            "download_url": f"/download/{job_id}"
        }) + "\n"

    return Response(stream(), mimetype="text/plain")


# ─────────────────────────────
# TÉLÉCHARGEMENT XML
# ─────────────────────────────
@app.route("/download/<job_id>")
def download(job_id):
    path = os.path.join(OUTPUT_FOLDER, f"{job_id}.xml")
    if not os.path.exists(path):
        return {"error": "Introuvable"}, 404

    return send_file(path, as_attachment=True)


# ─────────────────────────────
# ROUTE POUR OUVRIR LE DOSSIER (Nouveau)
# ─────────────────────────────
@app.route("/open-output-folder", methods=["GET"])
def open_output_folder():
    # On force le chemin absolu vers ton dossier de sortie
    folder_path = os.path.abspath(AUDIO_OUTPUT)
    
    print(f"Tentative d'ouverture du dossier : {folder_path}") # Vérifie ta console Python !

    if not os.path.exists(folder_path):
        return {"error": "Le dossier n'existe pas encore"}, 404

    try:
        if platform.system() == "Windows":
            # Correction spécifique Windows : on utilise explorer avec le chemin
            os.startfile(folder_path)
        elif platform.system() == "Darwin": # macOS
            subprocess.Popen(["open", folder_path])
        else: # Linux
            subprocess.Popen(["xdg-open", folder_path])
        
        return {"status": "success"}, 200
    except Exception as e:
        print(f"Erreur lors de l'ouverture : {e}")
        return {"error": str(e)}, 500

# ─────────────────────────────
# CONVERTISSEUR AUDIO (SSE-like)
# ─────────────────────────────
@app.route("/convert-audio", methods=["POST"])
def convert_audio():
    files = request.files.getlist("files")
    if not files:
        return {"error": "Aucun fichier"}, 400

    # ÉTAPE 1 : On sauvegarde tout immédiatement sur le disque
    # Cela évite l'erreur "read of closed file"
    saved_files = []
    for f in files:
        safe_name = secure_filename(os.path.basename(f.filename))
        if not safe_name:
            continue
        input_path = os.path.join(AUDIO_UPLOAD, safe_name)
        f.save(input_path) # Sauvegarde réelle sur le disque
        saved_files.append(safe_name)

    def generate():
        high_quality = True
        total = len(saved_files)
        
        for i, safe_name in enumerate(saved_files):
            input_path = os.path.join(AUDIO_UPLOAD, safe_name)
            name_without_ext = os.path.splitext(safe_name)[0]
            output_path = os.path.abspath(os.path.join(AUDIO_OUTPUT, f"{name_without_ext}.wav"))

            try:
                # ÉTAPE 2 : Conversion
                extract_audio(input_path, output_path, high_quality=high_quality)
                status = f"✅ Convert : {safe_name}"
            except Exception as e:
                status = f"❌ Error : {str(e)}"

            progress = int(((i + 1) / total) * 100)
            
            yield json.dumps({
                "progress": progress,
                "status": status,
                "done": (i + 1 == total)
            }) + "\n"
            
            # Nettoyage de l'input après conversion
            if os.path.exists(input_path):
                os.remove(input_path)

    return Response(generate(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True, port=5000)