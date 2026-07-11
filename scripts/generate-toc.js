#!/usr/bin/env node
import fs from 'fs/promises'
import path from 'path'

const ROOT = process.cwd()
const DOCS = path.join(ROOT, 'docs')
const IGNORE_DIRS = new Set(['.vitepress', 'generated', 'public', 'node_modules', '.git'])

function readFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/)
  if (!match) return {}
  return Object.fromEntries(
    match[1]
      .split(/\r?\n/)
      .map((line) => line.split(':'))
      .filter((parts) => parts.length >= 2)
      .map(([key, ...value]) => [key.trim(), value.join(':').trim()])
  )
}

function humanize(value) {
  return value
    .replace(/[-_]/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase())
}

const iconByDir = {
  AI: '\u{1F916}',
  computer: '\u{1F4BB}',
  database: '\u{1F5C4}\uFE0F',
  developer: '\u{1F6E0}\uFE0F',
  devops: '\u{1F500}',
  git: '\u{1F33F}',
  'organization-file': '\u{1F4C2}',
  software: '\u{1F4D0}',
  'utilities-script': '\u{26A1}',
}

function getCategoryLabel(dir) {
  const map = {
    about: 'About',
    AI: 'AI',
    computer: 'Computer',
    database: 'Database',
    developer: 'Developer',
    devops: 'DevOps',
    git: 'Git',
    organization: 'Organization',
    software: 'Software Engineering',
    utilities: 'Utilities',
  }
  const icon = iconByDir[dir] || ''
  const label = map[dir] || humanize(dir)
  return icon ? `${icon} ${label}` : label
}

async function walk(dir) {
  const files = []
  const entries = await fs.readdir(dir, { withFileTypes: true })
  for (const ent of entries) {
    if (IGNORE_DIRS.has(ent.name)) continue
    if (ent.name.startsWith('.')) continue
    const full = path.join(dir, ent.name)
    if (ent.isDirectory()) {
      files.push(...(await walk(full)))
    } else {
      files.push(full)
    }
  }
  return files
}

async function main() {
  const files = await walk(DOCS)

  const pages = []
  for (const f of files) {
    if (!f.toLowerCase().endsWith('.md')) continue

    const rel = path.relative(DOCS, f).replace(/\\/g, '/')
    if (rel === 'index.md') continue

    const content = await fs.readFile(f, 'utf-8')
    const meta = readFrontmatter(content)

    let route
    if (rel.endsWith('/index.md')) {
      route = '/' + rel.replace(/\/index\.md$/, '')
    } else {
      route = '/' + rel.replace(/\.md$/, '')
    }

    const parts = rel.split('/')
    const category = parts.length === 1 ? parts[0].replace(/\.md$/, '') : parts[0]
    const title = meta.title || humanize(path.basename(rel, '.md'))
    const description = meta.description || ''
    const order = meta.order !== undefined ? Number(meta.order) : 999

    pages.push({ route, title, description, order, category, rel })
  }

  pages.sort((a, b) => {
    if (a.order !== b.order) return a.order - b.order
    return a.title.localeCompare(b.title, undefined, { numeric: true, sensitivity: 'base' })
  })

  const grouped = {}
  for (const p of pages) {
    if (!grouped[p.category]) grouped[p.category] = []
    grouped[p.category].push(p)
  }

  const categoryOrder = Object.keys(grouped).sort((a, b) =>
    a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' })
  )

  const lines = []
  lines.push('---')
  lines.push('title: "REMEMBER — Personal Knowledge Base"')
  lines.push('description: "Bảng mục lục toàn bộ kiến thức"')
  lines.push('---')
  lines.push('')
  lines.push('# MỤC LỤC')

  for (const cat of categoryOrder) {
    const items = grouped[cat]
    lines.push('---')
    lines.push('')
    lines.push(`## ${getCategoryLabel(cat)}`)
    lines.push('')

    const subGroups = {}
    for (const item of items) {
      const parts = item.rel.split('/')
      if (parts.length <= 2) {
        if (!subGroups.__root__) subGroups.__root__ = []
        subGroups.__root__.push(item)
      } else {
        const sub = parts[1]
        if (!subGroups[sub]) subGroups[sub] = []
        subGroups[sub].push(item)
      }
    }

    const subKeys = Object.keys(subGroups).sort((a, b) => {
      if (a === '__root__') return -1
      if (b === '__root__') return 1
      return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' })
    })

    if (subKeys.length === 1 && subKeys[0] === '__root__') {
      for (const item of subGroups.__root__) {
        const desc = item.description ? ' -- ' + item.description : ''
        lines.push(`- [${item.title}](${item.route})${desc}`)
      }
    } else {
      for (const sub of subKeys) {
        if (sub === '__root__') {
          for (const item of subGroups[sub]) {
            const desc = item.description ? ' -- ' + item.description : ''
            lines.push(`- [${item.title}](${item.route})${desc}`)
          }
        } else {
          const items = subGroups[sub]
          const subTitle = items[0].category === cat
            ? humanize(sub)
            : humanize(sub)
          lines.push(`- **${subTitle}**`)
          for (const item of items) {
            const desc = item.description ? ' -- ' + item.description : ''
            lines.push(`  - [${item.title}](${item.route})${desc}`)
          }
        }
      }
    }
    lines.push('')
  }

  const outputPath = path.join(DOCS, 'index.md')
  await fs.writeFile(outputPath, lines.join('\n'), 'utf-8')
  console.log('Generated TOC:', outputPath)
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
