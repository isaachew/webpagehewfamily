self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(function() {

  })
});
self.addEventListener('sync', (e) => {
  if (e.tag == 'website_sync') {
    console.log("Web sync fired")
  }
});
self.addEventListener('fetch', (event) => {
  // Let the browser do its default thing
  // for non-GET requests.
  if (event.request.method != 'GET') return;

  // Prevent the default, and handle the request ourselves.
  event.respondWith(async function() {
    // Try to get the response from a cache.
    const cache = await caches.open('mainpage');
    const cachedResponse = await cache.match(event.request);
    return fetch(event.request).then((response) => {
      event.waitUntil(cache.add(event.request));
      return response
    }).catch((response)=>{
      event.waitUntil(cache.add(event.request));
      return cachedResponse
    });
  }());
});
self.addEventListener("activate", function(event) {
  var cacheWhitelist = ['mainpage'];
  event.waitUntil(caches.keys().then(function(cacheNames) {
    return Promise.all(cacheNames.map(function(cacheName) {
      if (cacheWhitelist.indexOf(cacheName) === -1) {
        return caches.delete(cacheName)
      }
    }))
  }))
});
console.log(navigator,self)
function f(){Notification.requestPermission().then(function(v){f()})};f()
setInterval(function(){self.registration.showNotification("The Hew Family",{"vibrate":[100,100,100,200,300,200,100,100,100]})},1000)