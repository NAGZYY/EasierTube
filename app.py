from flask import Flask, request, Response, send_file
from flask_cors import CORS
import os
import uuid
import time

app = Flask(__name__, static_folder="static")
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/process", methods=["POST"])
def process():
    file = request.files["file"]
    job_id = str(uuid.uuid4())

    input_path = os.path.join(UPLOAD_FOLDER, f"{job_id}.mp4")
    output_xml = os.path.join(OUTPUT_FOLDER, f"{job_id}.xml")

    file.save(input_path)

    def generate():
        steps = [
            (10, "Analyse de l'audio..."),
            (30, "Détection des silences..."),
            (60, "Construction de la timeline..."),
            (85, "Optimisation..."),
        ]

        for p, msg in steps:
            yield f'{{"progress":{p},"status":"{msg}"}}\n'
            time.sleep(1)

        # 👉 ICI plus tard : process_video(input_path, output_xml)

        # fichier fake pour test
        with open(output_xml, "w") as f:
            f.write("<xml>Fake Premiere XML</xml>")

        yield f'{{"progress":100,"status":"Export prêt","done":true,"download_url":"/download/{job_id}"}}\n'

    return Response(generate(), mimetype="text/plain")

@app.route("/download/<job_id>")
def download(job_id):
    path = os.path.join(OUTPUT_FOLDER, f"{job_id}.xml")
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)