# 🎬 EasierTube

**EasierTube** is a Python-powered automation tool designed to streamline video editing workflows by automatically detecting silences and generating ready-to-use timelines.

**EasierTube** est un outil d'automatisation en Python conçu pour simplifier le flux de travail de montage vidéo en détectant automatiquement les silences et en générant des timelines prêtes à l'emploi.

---

## 🚀 Features | Fonctionnalités

* 🔍 **Silence Detection:** Automatically identify quiet parts in your footage using `pydub`.
* ✂️ **Auto-Cutting:** Generate instant clips from your raw videos.
* 📂 **XML Export:** Create `XMEML` or `FCPXML` files compatible with **Adobe Premiere Pro** and **Final Cut Pro**.
* 🌐 **Web Interface:** Manage your assets via a simple local dashboard.

---

## 🛠 Prerequisites | Prérequis

Before starting, ensure you have the following installed:
Avant de commencer, assurez-vous d'avoir installé :

* **Python 3.12
* **FFmpeg** (Must be in your system PATH / Doit être dans le PATH système)
* **Libraries:** `pydub`, `lxml`, `Flask`, `requests`

---

## 📥 Installation

### 1. Clone the Project | Cloner le projet
```bash
git clone <URL_OF_THE_REPO> EasierTube
cd EasierTube
```

### 2. Install FFmpeg
| OS | Command / Link |
| :--- | :--- |
| **Windows** | [Download ffmpeg](https://ffmpeg.org/download.html) & add `/bin` to PATH OR use `winget install ffmpeg` |
| **macOS** | `brew install ffmpeg` |
| **Linux** | `sudo apt install ffmpeg` |

### 3. Install Python Dependencies | Dépendances Python
```bash
pip install pydub lxml flask requests
```

---

## ⚙️ Configuration

1.  **Uploads:** Create a folder named `uploads/` in the root directory. Place your raw videos there.
    * *Créez un dossier `uploads/` à la racine et déposez-y vos vidéos.*
2.  **Paths:** Ensure your scripts use absolute paths to avoid "Media Offline" issues in your DAW.
    * *Vérifiez que vos scripts utilisent des chemins absolus pour éviter les fichiers hors-ligne.*

---

## 🖥 Usage | Utilisation

### Step 1: Start the Interface | Démarrer l'interface
Run the local server of your choice:
```bash
# Option A: Flask (Recommended)
python app.py

# Option B: Python HTTP Server
python -m http.server 8000
```
> 🌐 **Access:** `http://localhost:5000` (Flask) or `http://localhost:8000/index.html`

### Step 2: Process & Export | Traitement & Export
1.  Run the Python scripts to detect silences and generate the XML.
2.  Import the resulting XML into your editor:
    * **Premiere Pro:** `File > Import > Select XML`
    * **Final Cut Pro:** `File > Import > XML`

---

## 💡 Notes & Support

> [!IMPORTANT]
> **Keep your files organized:** Do not move video files after generating the XML, or the link between the timeline and the media will break.

* **FFmpeg check:** Run `ffmpeg -version` to verify installation.
* **Errors:** If XML parsing fails, check `lxml` installation and your file paths.

---

## ⚖️ License
Personal / Open-source project for internal use.
*Projet personnel / open-source pour usage interne.*

---

### 🛠 Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Adobe Premiere Pro](https://img.shields.io/badge/Adobe%20Premiere%20Pro-9999FF?style=for-the-badge&logo=adobe-premiere-pro&logoColor=white)
