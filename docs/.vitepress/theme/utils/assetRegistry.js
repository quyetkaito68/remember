let manifestCache = null

function getSiteBaseUrl() {
  if (typeof document === 'undefined' || typeof location === 'undefined') return '/'

  const explicitBase = typeof __VP_SITE_DATA__ !== 'undefined' && __VP_SITE_DATA__?.base
    ? __VP_SITE_DATA__.base
    : document.querySelector('base')?.getAttribute('href')

  const baseHref = explicitBase || '/'
  return new URL(baseHref, location.origin).href
}

async function loadManifest(){
  if (manifestCache) return manifestCache
  if (typeof document === 'undefined') {
    manifestCache = {}
    return manifestCache
  }

  const manifestUrl = new URL('generated/assets-manifest.json', getSiteBaseUrl()).href
  try {
    const res = await fetch(manifestUrl)
    if (res.ok) {
      manifestCache = await res.json()
      return manifestCache
    }
  } catch (e) {
    // ignore
  }
  manifestCache = {}
  return manifestCache
}

function normalizeRoute(routePath){
  if (!routePath) return '/'
  let p = routePath
  if (!p.startsWith('/')) p = '/' + p
  if (p.endsWith('/') && p.length > 1) p = p.slice(0,-1)
  if (p === '') p = '/'
  return p
}

export async function getAssetsForRoute(routePath){
  const manifest = await loadManifest()
  const norm = normalizeRoute(routePath)
  if (manifest[norm] && (manifest[norm].assets || []).length) return manifest[norm].assets
  const parts = norm.split('/')
  while (parts.length > 1) {
    parts.pop()
    const parent = parts.join('/') || '/'
    if (manifest[parent] && (manifest[parent].assets || []).length) return manifest[parent].assets
  }
  return []
}

export async function getAssetByUrl(url){
  const manifest = await loadManifest()
  const norm = normalizeRoute(url)
  for (const key of Object.keys(manifest)){
    const rec = manifest[key]
    for (const a of rec.assets || []){
      const au = normalizeRoute(a.url || '')
      const araw = normalizeRoute('/' + (a.path||''))
      if (au === norm || araw === norm) return a
    }
  }
  return null
}

export default { loadManifest, getAssetsForRoute }
