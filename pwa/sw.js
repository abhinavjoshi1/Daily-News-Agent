const CACHE_NAME = 'ai-digest-v1';
const ASSETS = [
  '/Daily-News-Agent/pwa/',
  '/Daily-News-Agent/pwa/index.html',
  '/Daily-News-Agent/pwa/style.css',
  '/Daily-News-Agent/pwa/app.js',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(e.request)
      .then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
        return response;
      })
      .catch(() => caches.match(e.request))
  );
});
