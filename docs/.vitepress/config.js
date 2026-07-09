import fs from 'fs'
import path from 'path'
import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import { createNav, createSidebar } from './sidebar.js'

const repository = process.env.GITHUB_REPOSITORY || ''
const repoName = repository ? repository.split('/')[1] : 'remember'
const isCI = process.env.CI === 'true' || process.env.CI === '1'
const base = process.env.VITEPRESS_BASE || (isCI ? `/${repoName}/` : '/')

export default withMermaid(
  defineConfig({
    base,
    lang: 'en-US',
    title: 'REMEMBER — Personal Knowledge Base',
    description: 'A Markdown-first personal knowledge base built with VitePress.',
    head: [
      ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }],
      // Force dark mode immediately and persist preference (pre-CSS render)
      ['script', {}, "try{document.documentElement.classList.add('dark');localStorage.setItem('vitepress-theme-appearance','dark')}catch(e){}"],
      ['meta', { name: 'theme-color', content: '#4f46e5' }],
      // Inline SVG (base64) favicon (embedded book icon)
      ['link', { rel: 'icon', type: 'image/svg+xml', href: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAyNCAyNCc+DQogIDxyZWN0IHg9JzInIHk9JzQnIHdpZHRoPScyMCcgaGVpZ2h0PScxNicgcng9JzInIGZpbGw9JyM0ZjQ2ZTUnLz4NCiAgPHBhdGggZD0nTTQgNmg4djFINHpNNCA5aDh2MUg0eicgZmlsbD0nI2ZmZmZmZicgb3BhY2l0eT0nMC45Jy8+DQogIDxwYXRoIGQ9J00xMiA2aDh2MTFhMiAyIDAgMCAxLTIgMkgxMlY2eicgZmlsbD0nIzBlYTVlOScgb3BhY2l0eT0nMC45NScvPg0KPC9zdmc+' }],
      // Keep PNG fallback (optional)
      ['link', { rel: 'alternate icon', type: 'image/png', href: `${base}favicon.png` }],
    ],
    themeConfig: {
      // Use inline SVG (base64) book icon for logo to avoid external file 404s
      logo: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAyNCAyNCc+DQogIDxyZWN0IHg9JzInIHk9JzQnIHdpZHRoPScyMCcgaGVpZ2h0PScxNicgcng9JzInIGZpbGw9JyM0ZjQ2ZTUnLz4NCiAgPHBhdGggZD0nTTQgNmg4djFINHpNNCA5aDh2MUg0eicgZmlsbD0nI2ZmZmZmZicgb3BhY2l0eT0nMC45Jy8+DQogIDxwYXRoIGQ9J00xMiA2aDh2MTFhMiAyIDAgMCAxLTIgMkgxMlY2eicgZmlsbD0nIzBlYTVlOScgb3BhY2l0eT0nMC45NScvPg0KPC9zdmc+' ,
      siteTitle: 'REMEMBER',
      nav: [...createNav(), { text: 'About', link: '/about/' }],
      sidebar: createSidebar(),
      outline: [2, 3],
      search: {
        provider: 'local',
      },
      socialLinks: [
        {
          icon: 'github',
          link: 'https://github.com/quyetkaito68/quyetkaito68',
        },
      ],
      editLink: {
        pattern: '',
      },
      lastUpdated: true,
      docFooter: {
        prev: 'Previous',
        next: 'Next',
      },
      footer: {
        message: 'Static knowledge base built with VitePress.',
        copyright: 'Copyright © 2026',
      },
    },
    markdown: {
      lineNumbers: true,
      theme: 'github-dark',
      anchor: {
        slugify: (str) => {
          return str
            .replace(/&/g, '')
            .replace(/[^\p{L}\p{N}\s]+/gu, '')
            .replace(/ /g, '-')
            .replace(/^-+|-+$/g, '')
            .toLowerCase()
        },
      },
    },
    vite: {
      resolve: {
        alias: {
          '@docs': path.resolve(__dirname, '..'),
        },
      },
      optimizeDeps: {
        include: ['mermaid'],
      },
    },
  })
)
