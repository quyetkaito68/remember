let manifestCache = null

async function loadManifest(){
  if (manifestCache) return manifestCache
  const paths = ['/generated/assets-manifest.json','/.vitepress/generated/assets-manifest.json']
  for (const p of paths) {
    try {
      const res = await fetch(p)
      if (!res.ok) continue
      manifestCache = await res.json()
      return manifestCache
    } catch (e) {
      // try next
    }
  }
  manifestCache = {}
  return manifestCache
}

function normalizeRoute(routePath){
  if (!routePath) return ''
  let p = routePath
  if (p.endsWith('/')) p = p.slice(0,-1)
  if (p === '') p = '/'
  return p
}

export async function getAssetsForRoute(routePath){
  const manifest = await loadManifest()
  const norm = normalizeRoute(routePath)
  // exact match
  if (manifest[norm]) return manifest[norm].assets || []
  // try parent
  const parts = norm.split('/')
  while (parts.length>1) {
    parts.pop()
    const parent = parts.join('/') || '/'
    if (manifest[parent]) return manifest[parent].assets || []
  }
  return []
}

export async function getAssetByUrl(url){
  const manifest = await loadManifest()
  // normalize
  const norm = (u=>{ if (!u) return '/'; let s=u; if (!s.startsWith('/')) s='/'+s; if (s.endsWith('/') && s.length>1) s=s.slice(0,-1); return s })(url)
  for (const key of Object.keys(manifest)){
    const rec = manifest[key]
    for (const a of rec.assets || []){
      const au = a.url || ''
      const araw = ('/' + (a.path||'')).replace(/\\/g,'/')
      const an = au.endsWith('/') && au.length>1 ? au.slice(0,-1) : au
      if (an === norm || araw === norm) return a
    }
  }
  return null
}

export default { loadManifest, getAssetsForRoute }
