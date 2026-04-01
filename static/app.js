const dz = document.getElementById('dropzone');
const fi = document.getElementById('fileInput');
const status = document.getElementById('status');
const bar = document.getElementById('bar');
const pct = document.getElementById('progress-pct');
const btn = document.getElementById('start');

let currentFile = null;

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
    (file.size / 1024 / 1024).toFixed(1) + ' MB · Prêt à traiter';
  status.textContent = 'Fichier chargé. Lance le traitement !';
}

// ─── TOGGLES ───
function selectToggle(btn) {
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
    status.textContent = '⚠️ Ajoute une vidéo d\'abord';
    return;
  }

  btn.disabled = true;
  btn.textContent = '⏳ Traitement en cours...';

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
      throw new Error('Erreur serveur');
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
          status.textContent = '✅ Export prêt !';
          btn.textContent = '⬇ Télécharger le projet Premiere';
          btn.disabled = false;
          btn.onclick = () => window.location.href = msg.download_url;
        }
      }
    }

  } catch (err) {
    console.error(err);
    status.textContent = '❌ Une erreur est survenue.';
    btn.disabled = false;
    btn.textContent = '▶ Lancer le traitement';
  }
}