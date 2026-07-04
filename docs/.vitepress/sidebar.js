import fs from 'fs'
import path from 'path'

const docsRoot = path.resolve(__dirname, '..')
const ignoredDirs = new Set(['.vitepress', 'generated'])

function readFrontmatter(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8')
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

function normalizeLink(value) {
  return value.replace(/\/+/g, '/').replace(/\/\s*$/, '/')
}

function buildSidebar(directory, route = '') {
  const entries = fs.readdirSync(directory, { withFileTypes: true })
    .filter((entry) => !entry.name.startsWith('.') && !ignoredDirs.has(entry.name))
    .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: 'base' }))

  const groups = []

  for (const entry of entries) {
    const entryPath = path.join(directory, entry.name)

    if (entry.isDirectory()) {
      const childItems = buildSidebar(entryPath, path.posix.join(route, entry.name))
      if (childItems.length === 0) continue

      const indexFile = path.join(entryPath, 'index.md')
      const metadata = fs.existsSync(indexFile) ? readFrontmatter(indexFile) : {}
      const text = metadata.title || humanize(entry.name)
      const group = {
        text,
        items: childItems,
      }
      if (fs.existsSync(indexFile)) {
        group.link = normalizeLink(`/${route}/${entry.name}/`)
      }
      groups.push(group)
      continue
    }

    if (!entry.name.endsWith('.md')) continue
    if (entry.name === 'index.md' && route === '') continue

    const metadata = readFrontmatter(entryPath)
    const text = metadata.title || humanize(entry.name.replace(/\.md$/, ''))
    const link = normalizeLink(`/${route}/${entry.name.replace(/\.md$/, '')}/`)
    groups.push({ text, link })
  }

  return groups
}

export function createSidebar() {
  return buildSidebar(docsRoot)
}

export function createNav() {
  const rootEntries = fs.readdirSync(docsRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && !ignoredDirs.has(entry.name))
    .filter((entry) => fs.existsSync(path.join(docsRoot, entry.name, 'index.md')))
    .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: 'base' }))

  return [
    { text: 'Home', link: '/' },
    ...rootEntries.map((entry) => {
      const metadata = readFrontmatter(path.join(docsRoot, entry.name, 'index.md'))
      return {
        text: metadata.title || humanize(entry.name),
        link: `/${entry.name}/`,
      }
    }),
  ]
}
