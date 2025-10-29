// SpiralOS® Service Worker — minimal offline cache
// Author: Carey G. Butler / Heurist GmbH

const CACHE_NAME = 'spiralos-cache-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/docs/seo/style.css',
  '/docs/seo/banner.png',
  '/docs/seo/icon.png',
  '/manifest.webmanifest'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(resp => 
      resp || fetch(event.request).catch(() => caches.match('/index.html'))
    )
  );
});
