// Cloudflare Worker для проксирования R2 изображений
// Разместите этот код в Cloudflare Workers

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  
  // Извлекаем путь к изображению
  const imagePath = url.pathname
  
  // URL вашего R2 bucket
  const r2Url = `https://aac274e05c43fa7b57f050551ce13dbb.r2.cloudflarestorage.com/your-site-media${imagePath}`
  
  // Создаем новый запрос к R2
  const r2Request = new Request(r2Url, {
    method: request.method,
    headers: {
      'User-Agent': request.headers.get('User-Agent') || 'Cloudflare-Worker'
    }
  })
  
  try {
    const response = await fetch(r2Request)
    
    // Добавляем CORS заголовки
    const newResponse = new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: {
        ...response.headers,
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
        'Access-Control-Allow-Headers': '*',
        'Cache-Control': 'public, max-age=86400'
      }
    })
    
    return newResponse
  } catch (error) {
    return new Response('Image not found', { status: 404 })
  }
}
