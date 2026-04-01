from flask import Flask, request, Response, send_file
from flask_cors import CORS
import os
import uuid
from processor import process_video

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
        try:
            def callback(progress, status):
                yield_data = f'{{"progress":{progress},"status":"{status}"}}\n'
                print("sending:", yield_data.strip())
                yield yield_data

            # Cette fonction va générer des messages pour Flask
            for msg in process_video_generator(input_path, output_xml):
                yield msg

            # À la fin, on renvoie le lien de téléchargement
            yield f'{{"progress":100,"status":"Export prêt","done":true,"download_url":"/download/{job_id}"}}\n'
        except Exception as e:
            yield f'{{"error":true,"message":"{str(e)}"}}\n'

    # Wrapping generator correctement
    def process_video_generator(input_path, output_xml):
        buffer = []

        def progress_callback(progress, status):
            buffer.append(f'{{"progress":{progress},"status":"{status}"}}\n')

        process_video(input_path, output_xml, progress_callback)

        for msg in buffer:
            yield msg

    return Response(generate(), mimetype="text/plain")

@app.route("/download/<job_id>")
def download(job_id):
    path = os.path.join(OUTPUT_FOLDER, f"{job_id}.xml")
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)