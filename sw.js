self.addEventListener('install', (e) => {
  console.log('App Installed');
});
self.addEventListener('fetch', (e) => {
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});