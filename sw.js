const CACHE_NAME = 'nit-cache-v13.0'; // Updated version to force refresh
const ASSETS = [
  './',
  './index.html',
  './HR_Portal.html',
  './manifest.json',
  './manifest_hr.json',
  './assets/logo.png',
  './assets/employees.json',
  './assets/icons/icon-192.png',
  './assets/icons/icon-512.png'
];

self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
});

self.addEventListener('activate', e => {
  // FORCE DELETE ALL OLD CACHES
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  
  // For navigation requests, try network first
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).catch(() => caches.match(req))
    );
    return;
  }

  e.respondWith(
    caches.match(req).then(cached => {
      return cached || fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE_NAME).then(c => c.put(req, copy));
        return res;
      });
    })
  );
});
