import fs from 'fs'
import path from 'path'
import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import { createNav, createSidebar } from './sidebar.js'

const repository = process.env.GITHUB_REPOSITORY || ''
const base = process.env.VITEPRESS_BASE || (repository ? `/${repository.split('/')[1]}/` : '/')

export default withMermaid(
  defineConfig({
    base,
    lang: 'en-US',
    title: 'REMEMBER — Personal Knowledge Base',
    description: 'A Markdown-first personal knowledge base built with VitePress.',
    head: [
      ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }],
      ['meta', { name: 'theme-color', content: '#4f46e5' }],
      ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
      ['link', { rel: 'alternate icon', type: 'image/png', href: '/favicon.png' }],
    ],
    themeConfig: {
      logo: '/favicon.svg',
      siteTitle: 'REMEMBER',
      nav: createNav(),
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
