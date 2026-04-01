const dz = document.getElementById('dropzone');
const fi = document.getElementById('fileInput');
const status = document.getElementById('status');
const bar = document.getElementById('bar');
const pct = document.getElementById('progress-pct');
const btn = document.getElementById('start');

let currentFile = null;
let currentLang = 'fr';

// ─── TRANSLATIONS ───
const translations = {
  fr: {
    noFile: '⚠️ Ajoute une vidéo d\'abord',
    fileReady: 'Fichier chargé. Lance le traitement !',
    readyToProcess: 'Prêt à traiter',
    processing: '⏳ Traitement en cours...',
    serverError: 'Erreur serveur',
    error: '❌ Une erreur est survenue.',
    launch: '▶ Lancer le traitement',
    done: '✅ Export prêt !',
    download: '⬇ Télécharger le projet Premiere',
    audioDetected: ' fichiers audio détectés',
    noAudio: '⚠️ Aucun fichier audio trouvé',
    converting: '⏳ Conversion...',
    connError: '❌ Erreur de connexion au serveur',
    retry: 'Réessayer la conversion',
    convDone: '✅ Conversion terminée (Dossier output/audio)',
    openFolder: '📂 Ouvrir le dossier de destination'
  },
  en: {
    noFile: '⚠️ Add a video first',
    fileReady: 'File loaded. Start processing!',
    readyToProcess: 'Ready to process',
    processing: '⏳ Processing...',
    serverError: 'Server error',
    error: '❌ An error occurred.',
    launch: '▶ Start processing',
    done: '✅ Export ready!',
    download: '⬇ Download Premiere project',
    audioDetected: ' audio files detected',
    noAudio: '⚠️ No audio files found',
    converting: '⏳ Converting...',
    connError: '❌ Server connection error',
    retry: 'Retry conversion',
    convDone: '✅ Conversion finished (Folder: output/audio)',
    openFolder: '📂 Open destination folder'
  }
};

function t(key) {
  return translations[currentLang]?.[key] || translations.fr[key];
}

// ─── FILE HANDLING ───
dz.addEventListener('dragover', e => {
  e.preventDefault();
  dz.classList.add('drag-over');
});

dz.addEventListener('dragleave', () => dz.classList.remove('drag-over'));

dz.addEventListener('drop', e => {
  e.preventDefault();
  dz.classList.remove('drag-over');
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});

fi.addEventListener('change', () => {
  if (fi.files[0]) handleFile(fi.files[0]);
});

function handleFile(file) {
  currentFile = file;
  dz.querySelector('.dropzone-icon').textContent = '✅';
  dz.querySelector('.dropzone-title').textContent = file.name;
  dz.querySelector('.dropzone-sub').textContent =
    (file.size / 1024 / 1024).toFixed(1) + ' MB · ' + t('readyToProcess');
  status.textContent = t('fileReady');
}

// ─── TOGGLES ───
function selectToggle(btn, type) {
  btn.closest('.toggle-group')
    .querySelectorAll('.toggle-btn')
    .forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

// ─── SETTINGS ───
function getSensitivity() {
  const el = document.querySelector('.toggle-btn.active');
  return el ? el.textContent.toLowerCase() : 'normal';
}

function getMargin() {
  return document.getElementById('marginRange').value;
}

// ─── START PROCESS ───
async function handleStart() {
  if (!currentFile) {
    status.textContent = t('noFile');
    return;
  }

  btn.disabled = true;
  btn.textContent = t('processing');

  const data = new FormData();
  data.append('file', currentFile);
  data.append('sensitivity', getSensitivity());
  data.append('margin_ms', getMargin());

  let buffer = '';

  try {
    const res = await fetch('/process', {
      method: 'POST',
      body: data
    });

    if (!res.ok || !res.body) {
      throw new Error(t('serverError'));
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      const parts = buffer.split('\n');
      buffer = parts.pop();

      for (const part of parts) {
        if (!part.trim()) continue;

        const msg = JSON.parse(part);

        if (msg.progress !== undefined) {
          bar.style.width = msg.progress + '%';
          pct.textContent = msg.progress + '%';
          status.textContent = msg.status || '';
        }

        if (msg.done) {
          bar.style.width = '100%';
          pct.textContent = '100%';
          status.textContent = t('done');
          btn.textContent = t('download');
          btn.disabled = false;
          btn.onclick = () => window.location.href = msg.download_url;
        }
      }
    }

  } catch (err) {
    console.error(err);
    status.textContent = t('error');
    btn.disabled = false;
    btn.textContent = t('launch');
  }
}

// --- VARIABLES AUDIO ---
let audioFiles = [];
const folderInput = document.getElementById('folderInput');
const audioStatus = document.getElementById('audio-status');
const audioBar = document.getElementById('audio-bar');
const audioPct = document.getElementById('audio-pct');
const btnAudio = document.getElementById('audio-start');

folderInput.addEventListener('change', () => {
    audioFiles = Array.from(folderInput.files).filter(f =>
        f.name.toLowerCase().endsWith('.mp3') || 
        f.name.toLowerCase().endsWith('.m4a') || 
        f.name.toLowerCase().endsWith('.wav')
    );

    // Traduction dynamique du nombre de fichiers
    audioStatus.textContent = audioFiles.length + t('audioDetected');
});

async function startAudioConvert() {
    if (audioFiles.length === 0) {
        audioStatus.textContent = t('noAudio');
        return;
    }

    btnAudio.disabled = true;
    btnAudio.textContent = t('converting');

    const data = new FormData();
    audioFiles.forEach(f => data.append('files', f));

    try {
        const res = await fetch('/convert-audio', {
            method: 'POST',
            body: data
        });

        if (!res.body) throw new Error("No response");

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop(); 

            for (const line of lines) {
                const trimmedLine = line.trim();
                if (!trimmedLine) continue;

                try {
                    const msg = JSON.parse(trimmedLine);
                    
                    if (msg.progress !== undefined) {
                        audioBar.style.width = msg.progress + '%';
                        audioPct.textContent = msg.progress + '%';
                    }
                    
                    // Le message de statut venant de Python peut rester tel quel 
                    // ou être traduit si tu envoies des clés au lieu de phrases.
                    if (msg.status) {
                        audioStatus.textContent = msg.status;
                    }

                    if (msg.done) {
                        finishAudioUI();
                    }
                } catch (e) {
                    console.error("JSON Error:", e);
                }
            }
        }
    } catch (err) {
        console.error(err);
        audioStatus.textContent = t('connError');
        btnAudio.disabled = false;
        btnAudio.textContent = t('retry');
    }
}

function finishAudioUI() {
    audioStatus.textContent = t('convDone');
    
    btnAudio.disabled = false;
    btnAudio.textContent = t('openFolder');
    btnAudio.style.backgroundColor = "#28a745"; 
    btnAudio.classList.add('btn-success'); 

    btnAudio.onclick = function() {
        fetch('/open-output-folder')
            .then(r => r.json())
            .catch(err => console.error("Error opening folder", err));
    };
}