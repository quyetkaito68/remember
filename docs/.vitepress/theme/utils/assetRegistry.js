let manifestCache = null

function getSiteBaseUrl() {
  if (typeof document === 'undefined' || typeof location === 'undefined') return '/'

  const explicitBase = typeof __VP_SITE_DATA__ !== 'undefined' && __VP_SITE_DATA__?.base
    ? __VP_SITE_DATA__.base
    : document.querySelector('base')?.getAttribute('href')

  const baseHref = explicitBase || '/'
  return new URL(baseHref, location.origin).href
}

function getSiteBasePath() {
  if (typeof document === 'undefined' || typeof location === 'undefined') return '/'

  const explicitBase = typeof __VP_SITE_DATA__ !== 'undefined' && __VP_SITE_DATA__?.base
    ? __VP_SITE_DATA__.base
    : document.querySelector('base')?.getAttribute('href')

  const pathname = new URL(explicitBase || '/', location.origin).pathname
  return pathname === '/' ? '/' : pathname.replace(/\/+$/, '')
}

function stripBasePath(routePath) {
  if (!routePath) return '/'

  let p = routePath
  if (!p.startsWith('/')) p = '/' + p

  const basePath = getSiteBasePath()
  if (basePath && basePath !== '/') {
    const normalizedBase = basePath.replace(/\/+$/, '')
    if (normalizedBase && p === normalizedBase) return '/'
    if (normalizedBase && p.startsWith(normalizedBase + '/')) {
      p = p.slice(normalizedBase.length) || '/'
    }
  }

  if (p === '') p = '/'
  if (p.endsWith('/') && p.length > 1) p = p.slice(0, -1)
  return p
}

function withBasePath(urlPath) {
  if (!urlPath) return urlPath

  let p = String(urlPath)
  if (!p.startsWith('/')) p = '/' + p

  const basePath = getSiteBasePath()
  if (!basePath || basePath === '/') return p

  const normalizedBase = basePath.replace(/\/+$/, '')
  if (p.startsWith(normalizedBase + '/')) return p
  return `${normalizedBase}${p}`
}

function normalizeAsset(asset) {
  if (!asset) return asset
  const out = { ...asset }
  if (out.url) out.url = withBasePath(out.url)
  if (out.rawUrl) out.rawUrl = withBasePath(out.rawUrl)
  return out
}

/**
 * Loads the assets manifest.
 * @returns {Promise<Object>} A promise resolving to the assets manifest.
 */
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

/**
 * Normalizes a route path.
 * @param {string} routePath 
 * @returns {string} The normalized route path.
 */
function normalizeRoute(routePath){
  return stripBasePath(routePath)
}

/**
 * Gets the assets for a given route path.
 * @param {string} routePath 
 * @returns {Promise<Array>} A promise resolving to an array of asset objects.
 */
export async function getAssetsForRoute(routePath){
  const manifest = await loadManifest()
  const norm = normalizeRoute(routePath)
  if (manifest[norm] && (manifest[norm].assets || []).length) {
    return (manifest[norm].assets || []).map(normalizeAsset)
  }
  const parts = norm.split('/')
  while (parts.length > 1) {
    parts.pop()
    const parent = parts.join('/') || '/'
    if (manifest[parent] && (manifest[parent].assets || []).length) {
      return (manifest[parent].assets || []).map(normalizeAsset)
    }
  }
  return []
}

/**
 * Gets an asset by its URL.
 * @param {string} url 
 * @returns {Promise<Object|null>} A promise resolving to the asset object or null if not found.
 */
export async function getAssetByUrl(url){
  const manifest = await loadManifest()
  const norm = normalizeRoute(url)
  for (const key of Object.keys(manifest)){
    const rec = manifest[key]
    for (const a of rec.assets || []){
      const au = normalizeRoute(a.url || '')
      const araw = normalizeRoute('/' + (a.path || ''))
      if (au === norm || araw === norm) return normalizeAsset(a)
    }
  }
  return null
}

export default { loadManifest, getAssetsForRoute, getAssetByUrl }
