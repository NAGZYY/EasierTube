from flask import Flask, request, Response, send_file, stream_with_context
from flask_cors import CORS
import os
import uuid
import json
from processor import process_video

app = Flask(__name__, static_folder="static")
# CORS est essentiel si ton frontend et backend ne sont pas sur le même port
CORS(app)

# Configuration des dossiers
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    """Sert la page d'accueil de l'application."""
    return app.send_static_file("index.html")

@app.route("/process", methods=["POST"])
def process():
    """Gère l'upload, le traitement et le retour de progression en temps réel."""
    if 'file' not in request.files:
        return {"error": "Aucun fichier envoyé"}, 400
    
    file = request.files["file"]
    if file.filename == '':
        return {"error": "Nom de fichier vide"}, 400

    # Création d'un ID unique pour cette session de montage
    job_id = str(uuid.uuid4())
    
    # Récupération des réglages envoyés par le frontend
    sensitivity = request.form.get('sensitivity', 'normal')
    try:
        margin_ms = int(request.form.get('margin_ms', 120))
    except (ValueError, TypeError):
        margin_ms = 120

    # Définition des chemins de fichiers
    # On garde l'extension .mp4 pour que Premiere reconnaisse le média source
    input_path = os.path.join(UPLOAD_FOLDER, f"{job_id}.mp4")
    # L'output est maintenant un .xml standard (XMEML)
    output_xml = os.path.join(OUTPUT_FOLDER, f"{job_id}.xml")
    
    # Sauvegarde du fichier uploadé
    file.save(input_path)

    @stream_with_context
    def generate():
        try:
            # Appel du processeur qui analyse l'audio et génère les segments
            # On yield chaque étape pour mettre à jour la barre de progression en JS
            for progress, status in process_video(input_path, output_xml, job_id, sensitivity, margin_ms):
                yield json.dumps({"progress": progress, "status": status}) + "\n"

            # Message final indiquant que le lien de téléchargement est prêt
            yield json.dumps({
                "progress": 100, 
                "status": "Montage terminé !", 
                "done": True, 
                "download_url": f"/download/{job_id}"
            }) + "\n"
            
        except Exception as e:
            # En cas d'erreur (ffmpeg manquant, etc.), on prévient le JS
            yield json.dumps({"error": True, "message": str(e)}) + "\n"

    return Response(generate(), mimetype="application/json")

@app.route("/download/<job_id>")
def download(job_id):
    path = os.path.join(OUTPUT_FOLDER, f"{job_id}.xml")
    
    # On récupère le nom passé dans l'URL, sinon "Project" par défaut
    # Exemple d'URL : /download/123?filename=mon_super_film.mp4
    original_filename = request.args.get('filename', 'Project')
    
    friendly_name = f"EasierTube - {original_filename}.xml"

    if os.path.exists(path):
        return send_file(
            path, 
            as_attachment=True, 
            download_name=friendly_name
        )
    return {"error": "Fichier introuvable"}, 404

@app.route('/demo.mp4')
def demo_video():
    demo_path = os.path.join(app.root_path, 'demo.mp4')
    if os.path.exists(demo_path):
        return send_file(demo_path, mimetype='video/mp4')
    return {"error": "Demo video introuvable"}, 404

if __name__ == "__main__":
    # threaded=True est crucial pour que le streaming JSON fonctionne bien
    app.run(debug=True, port=5000, threaded=True)