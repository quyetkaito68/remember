#!/usr/bin/env node
import fs from 'fs/promises'
import path from 'path'
import {spawnSync} from 'child_process'

const ROOT = process.cwd()
const DOCS = path.join(ROOT, 'docs')
const OUT_DIR = path.join(DOCS, '.vitepress', 'generated')
const OUT_FILE = path.join(OUT_DIR, 'assets-manifest.json')
// also write to public so VitePress will copy to site root at /generated/
const PUBLIC_OUT_DIR = path.join(DOCS, '.vitepress', 'public', 'generated')
const PUBLIC_OUT_FILE = path.join(PUBLIC_OUT_DIR, 'assets-manifest.json')

const IGNORE_DIRS = new Set(['.vitepress', '.git'])

function isMarkdown(name) {
  return name.toLowerCase().endsWith('.md')
}

function isHidden(name) {
  return name.startsWith('.')
}

function detectType(ext) {
  const e = ext.toLowerCase()
  const map = {
    '.png':'image', '.jpg':'image', '.jpeg':'image', '.gif':'image', '.svg':'image', '.webp':'image',
    '.pdf':'pdf',
    '.mp4':'video', '.webm':'video',
    '.mp3':'audio', '.wav':'audio',
    '.zip':'archive', '.rar':'archive', '.7z':'archive', '.exe':'binary', '.msi':'binary', '.iso':'binary',
    '.ps1':'powershell', '.bat':'batch', '.cmd':'batch', '.sh':'shell', '.sql':'sql', '.json':'json', '.xml':'xml', '.yml':'yaml', '.yaml':'yaml', '.ini':'ini', '.reg':'registry', '.env':'env', '.env.example':'env'
  }
  return map[e] || 'file'
}

async function walk(dir) {
  const res = []
  const entries = await fs.readdir(dir, {withFileTypes:true})
  for (const ent of entries) {
    if (IGNORE_DIRS.has(ent.name)) continue
    const full = path.join(dir, ent.name)
    if (ent.isDirectory()) {
      res.push(...await walk(full))
    } else {
      res.push(full)
    }
  }
  return res
}

function gitLastCommitInfo(filePath) {
  try {
    const rel = path.relative(process.cwd(), filePath).replace(/\\/g, '/')
    const out = spawnSync('git', ['log','-1','--format=%ct|%H','--', rel], {encoding:'utf8'})
    if (out.status === 0 && out.stdout) {
      const [ts, sha] = out.stdout.trim().split('|')
      return {lastModified: Number(ts)||null, sha: sha||null}
    }
  } catch (e) {
    // ignore
  }
  return {lastModified:null, sha:null}
}

function toUrl(relPath) {
  // Convert file path under docs to a URL path
  let p = relPath.replace(/\\/g, '/')
  if (!p.startsWith('/')) p = '/' + p
  // remove leading /docs
  if (p.startsWith('/docs')) p = p.slice(5)
  return p
}

async function main(){
  const files = await walk(DOCS)
  const byDir = new Map()
  for (const f of files) {
    const rel = path.relative(DOCS, f)
    const parts = rel.split(/[/\\]/)
    if (parts[0] === '.vitepress') continue
    const dir = path.dirname(rel)
    const name = path.basename(rel)
    if (!byDir.has(dir)) byDir.set(dir, [])
    byDir.get(dir).push({full:f, rel, name})
  }

  const manifest = {}
  for (const [dir, entries] of byDir.entries()) {
    // find markdowns in this dir
    const mdFiles = entries.filter(e=>isMarkdown(e.name)).map(e=>e)
    if (mdFiles.length === 0) continue
    // identify assets: any non-md files in the same dir
    const assets = entries.filter(e=>!isMarkdown(e.name) && !isHidden(e.name))
    if (assets.length === 0) {
      // still emit entry with markdown but empty assets
      const key = '/' + dir.replace(/\\/g,'/').replace(/(^\.|^$)/,'').replace(/\\/g,'/')
      manifest[key] = {
        markdown: mdFiles.map(m=>m.name),
        assets: []
      }
      continue
    }
    const list = []
    // compute baseRoute for the folder (clean route)
    let baseRoute
    if (dir === '.' || dir === ''){
      // use first markdown filename as base
      const md = mdFiles[0]
      baseRoute = '/' + md.name.replace(/\.md$/i, '')
    } else {
      baseRoute = '/' + dir.replace(/\\/g,'/')
    }

    for (const a of assets) {
      try {
        const st = await fs.stat(a.full)
        const ext = path.extname(a.name)
        const type = detectType(ext)
        const git = gitLastCommitInfo(a.full)
        const assetRoute = `${baseRoute}/assets/${encodeURIComponent(a.name)}/`
        list.push({
          name: a.name,
          path: a.rel.replace(/\\/g,'/'),
          url: assetRoute,
          rawUrl: toUrl(a.rel),
          type,
          size: st.size,
          lastModified: git.lastModified,
          sha: git.sha
        })
      } catch (e) {
        // ignore per-file errors
      }
    }
    const key = baseRoute
    manifest[key] = {
      markdown: mdFiles.map(m=>m.name),
      assets: list
    }
  }

  await fs.mkdir(OUT_DIR, {recursive:true})
  await fs.writeFile(OUT_FILE, JSON.stringify(manifest, null, 2), 'utf8')
  await fs.mkdir(PUBLIC_OUT_DIR, {recursive:true})
  await fs.writeFile(PUBLIC_OUT_FILE, JSON.stringify(manifest, null, 2), 'utf8')
  console.log('Generated', OUT_FILE)
  console.log('Public copy', PUBLIC_OUT_FILE)

  // Generate per-asset markdown pages under docs/.generated/assets
  // create clean route pages under docs/<topic>/assets/<filename>/index.md
  for (const key of Object.keys(manifest)){
    const rec = manifest[key]
    if (!rec.assets || rec.assets.length===0) continue
    // key is baseRoute like '/topic' or '/index'
    const base = key.replace(/^\//,'') // '' for root
    for (const a of rec.assets){
      // output folder: docs/<base>/assets/<filename>/index.md
      const outDir = path.join(DOCS, base || '', 'assets', a.name)
      await fs.mkdir(outDir, {recursive:true})
      const outPath = path.join(outDir, 'index.md')
      const title = a.name
      // find siblings for prev/next
      const siblings = rec.assets.map(x=>x.name).sort()
      const idx = siblings.indexOf(a.name)
      const prev = idx>0 ? `${key}/assets/${encodeURIComponent(siblings[idx-1])}/` : ''
      const next = idx < siblings.length-1 ? `${key}/assets/${encodeURIComponent(siblings[idx+1])}/` : ''
      const md = `---\ntitle: "${title}"\nassetPath: "${a.rawUrl}"\nassetUrl: "${a.url}"\nprev: "${prev}"\nnext: "${next}"\n---\n\n<AssetViewer assetPath="${a.url}" />\n`
      await fs.writeFile(outPath, md, 'utf8')
      console.log('Generated page', outPath)
    }
  }
}

main().catch(err=>{ console.error(err); process.exit(1) })
