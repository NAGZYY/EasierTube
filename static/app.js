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
    download: '⬇ Télécharger le projet Premiere'
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
    download: '⬇ Download Premiere project'
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