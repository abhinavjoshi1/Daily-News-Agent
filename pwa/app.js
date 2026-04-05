const GITHUB_USER = 'abhinavjoshi1';
const GITHUB_REPO = 'Daily-News-Agent';
const DIGESTS_PATH = 'digests';
const API_BASE = `https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}/contents/${DIGESTS_PATH}`;
const RAW_BASE = `https://raw.githubusercontent.com/${GITHUB_USER}/${GITHUB_REPO}/main/${DIGESTS_PATH}`;

// Simple markdown to HTML converter
function parseMarkdown(md) {
  return md
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^\- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
    .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
    .replace(/^---$/gm, '<hr>')
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank">$1</a>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/^(?!<[hul]|<hr|<li|<blockquote)(.+)$/gm, '<p>$1</p>')
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    .replace(/<p><\/p>/g, '');
}

// Format filename to readable date
function formatDate(filename) {
  // handles Digest_05_04_26.md and ai_digest_2026-04-05.md
  const name = filename.replace('.md', '');
  
  // Try Digest_DD_MM_YY format
  const match1 = name.match(/Digest_(\d{2})_(\d{2})_(\d{2})/i);
  if (match1) {
    const [_, dd, mm, yy] = match1;
    return `${dd}/${mm}/20${yy}`;
  }
  
  // Try ai_digest_YYYY-MM-DD format
  const match2 = name.match(/ai_digest_(\d{4})-(\d{2})-(\d{2})/i);
  if (match2) {
    const [_, yyyy, mm, dd] = match2;
    return `${dd}/${mm}/${yyyy}`;
  }
  
  return name;
}

// Views
const listView = document.getElementById('list-view');
const readerView = document.getElementById('reader-view');
const headerTitle = document.getElementById('header-title');
const headerSubtitle = document.getElementById('header-subtitle');
const backBtn = document.getElementById('back-btn');

// Load digest list
async function loadDigestList() {
  listView.innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <p>Loading digests...</p>
    </div>`;

  try {
    const res = await fetch(API_BASE);
    const files = await res.json();

    const mdFiles = files
      .filter(f => f.name.endsWith('.md'))
      .sort((a, b) => b.name.localeCompare(a.name)); // newest first

    if (mdFiles.length === 0) {
      listView.innerHTML = `<div class="loading"><p>No digests found yet.</p></div>`;
      return;
    }

    listView.innerHTML = mdFiles.map((file, index) => `
      <div class="digest-card" onclick="loadDigest('${file.name}')">
        <div class="digest-card-left">
          <span class="digest-date">${formatDate(file.name)}</span>
          <span class="digest-label">Daily AI Digest</span>
        </div>
        <div style="display:flex;align-items:center;gap:10px">
          ${index === 0 ? '<span class="latest-badge">Latest</span>' : ''}
          <span class="digest-arrow">›</span>
        </div>
      </div>
    `).join('');

  } catch (err) {
    listView.innerHTML = `<div class="loading"><p>Failed to load. Check connection.</p></div>`;
  }
}

// Load single digest
async function loadDigest(filename) {
  readerView.innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <p>Loading digest...</p>
    </div>`;

  listView.style.display = 'none';
  readerView.style.display = 'block';
  backBtn.style.display = 'block';
  headerTitle.textContent = formatDate(filename);
  headerSubtitle.textContent = 'AI Daily Digest';

  try {
    const res = await fetch(`${RAW_BASE}/${filename}`);
    const md = await res.text();
    readerView.innerHTML = parseMarkdown(md);
  } catch (err) {
    readerView.innerHTML = `<div class="loading"><p>Failed to load digest.</p></div>`;
  }
}

// Back button
backBtn.addEventListener('click', () => {
  readerView.style.display = 'none';
  listView.style.display = 'block';
  backBtn.style.display = 'none';
  headerTitle.textContent = 'AI Digest';
  headerSubtitle.textContent = 'Daily AI News';
  readerView.innerHTML = '';
});

// Register service worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/Daily-News-Agent/pwa/sw.js');
  });
}

// Init
loadDigestList();
