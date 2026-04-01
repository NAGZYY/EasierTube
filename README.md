ENGLISH:

EasierTube
Description

EasierTube is a Python project designed to simplify video cutting and export for editing.
It allows you to:

Detect silences in your videos
Generate XML files compatible with Premiere Pro and Final Cut Pro
Automatically create timelines from imported videos

The project provides:

index.html: a web interface to select and manage videos
Python scripts for audio/video processing
Generation of XML files (XMEML / FCPXML)
uploads folder to store your videos
Prerequisites
Python 3.10+ installed on your machine
FFmpeg installed and available in the system PATH
Python libraries:
pydub
lxml
Flask (for local server if needed)
requests (optional depending on your scripts)
Installation

Clone the project to your computer:

git clone <URL_OF_THE_REPO> EasierTube
cd EasierTube
Install Python and pip if needed:
Windows: https://www.python.org/downloads/
Mac/Linux: use your package manager
Install FFmpeg:
Windows: https://ffmpeg.org/download.html
 → add ffmpeg/bin to your PATH
Mac: brew install ffmpeg
Linux: sudo apt install ffmpeg

Install the required Python libraries:

pip install pydub lxml flask requests

Check that FFmpeg works:

ffmpeg -version
Configuration
Create an uploads folder in the project directory
This is where you will place your videos to be processed.

Check the paths in your Python scripts
The generated XML files will use the full path to your videos.
Example:

C:/Users/YourName/EasierTube/uploads/video.mp4
(Optional) Modify index.html to point to your videos or adjust the interface.
Running the Project
Start a local server to access the web interface:

With Python 3:

python -m http.server 8000

With Flask:

python app.py

Then, open your browser at:

Python HTTP Server: http://localhost:8000/index.html
Flask: http://127.0.0.1:5000/
Place your videos in the uploads folder
Use the Python scripts to:
Detect silences (pydub)
Automatically cut clips
Generate XML files for Premiere Pro / Final Cut Pro
Import the generated XML files into Premiere Pro 2022 or Final Cut Pro:
Premiere: File > Import > Select XML file
Final Cut: File > Import > XML
Important Notes
All XML files must keep the same path as the video files to avoid "Offline Media" mode
FFmpeg is required to convert or check your videos if necessary
The project runs locally; no remote server is required
Support

If you encounter any issues:

Ensure FFmpeg is installed and accessible
Make sure Python and the required libraries are installed correctly
Check the official documentation of pydub and lxml if you encounter XML parsing errors
License

Personal / open-source project for internal use in managing your videos



FRANÇAIS:

EasierTube
Description

EasierTube est un projet Python destiné à simplifier la découpe et l'export de vidéos pour montage.
Il permet de :

Détecter les silences dans vos vidéos
Générer des fichiers XML compatibles avec Premiere Pro et Final Cut Pro
Créer automatiquement des timelines à partir de vidéos importées

Le projet fournit :

index.html : interface web pour sélectionner et gérer les vidéos
Scripts Python pour traitement audio/vidéo
Génération de fichiers XML (XMEML / FCPXML)
Dossier "uploads" pour stocker vos vidéos
Prérequis
Python 3.10+ installé sur votre machine
FFmpeg installé et disponible dans le PATH système
Librairies Python :
pydub
lxml
Flask (pour le serveur local si nécessaire)
requests (optionnel selon vos scripts)
Installation
Cloner le projet sur votre ordinateur :
git clone <URL_DU_REPO> EasierTube
cd EasierTube
Installer Python et pip si nécessaire :
Windows : https://www.python.org/downloads/
Mac/Linux : utilisez votre gestionnaire de paquets
Installer FFmpeg :
Windows : https://ffmpeg.org/download.html
 → ajouter ffmpeg/bin au PATH
Mac : brew install ffmpeg
Linux : sudo apt install ffmpeg
Installer les librairies Python requises :
pip install pydub lxml flask requests
Vérifier que FFmpeg fonctionne :
ffmpeg -version
Configuration
Créer un dossier "uploads" dans le répertoire du projet
C’est ici que vous déposerez vos vidéos à traiter.
Vérifier les chemins dans vos scripts Python
Les fichiers XML générés utiliseront le chemin complet vers vos vidéos.
Exemple :
C:/Users/YourName/EasierTube/uploads/video.mp4
(Optionnel) Modifier index.html pour pointer vers vos vidéos ou ajuster l’interface.
Exécution du projet

Démarrer un serveur local pour accéder à l’interface web :

Avec Python 3 : python -m http.server 8000
Avec Flask : python app.py

Ensuite, ouvrez votre navigateur à l’adresse :

Python HTTP Server : http://localhost:8000/index.html
Flask : http://127.0.0.1:5000/
Déposer vos vidéos dans le dossier "uploads"
Utiliser les scripts Python pour :
Détecter les silences (pydub)
Découper automatiquement les clips
Générer les fichiers XML pour Premiere Pro / Final Cut Pro
Importer les XML générés dans Premiere Pro 2022 ou Final Cut Pro :
Premiere : Fichier > Importer > Sélectionner le fichier XML
Final Cut : Fichier > Importer > XML
Notes importantes
Tous les fichiers XML doivent conserver le même chemin que les fichiers vidéo pour éviter le mode "Offline Media"
FFmpeg est indispensable pour convertir ou vérifier vos vidéos si besoin
Le projet fonctionne localement, aucun serveur distant n’est requis
Support

Pour toute question ou problème :

Vérifiez que FFmpeg est installé et accessible
Assurez-vous que Python et les librairies sont correctement installés
Consultez la documentation officielle de pydub et lxml si vous rencontrez des erreurs de parsing XML
Licence

Projet personnel / open-source à usage interne pour la gestion de vos vidéos