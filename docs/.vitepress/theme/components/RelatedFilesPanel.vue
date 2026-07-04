<template>
  <div v-if="assets && assets.length" class="related-files">
    <h3>Related Files</h3>
    <ul>
      <li v-for="a in assets" :key="a.path" class="asset-item">
        <span class="asset-name">📄 {{ a.name }}</span>
        <span class="asset-meta">{{ a.type }} · {{ formatSize(a.size) }}</span>
        <span class="asset-actions">
          <a :href="a.rawUrl" target="_blank" rel="noopener" download>Download</a>
          <a :href="a.url" target="_blank" rel="noopener">Raw</a>
        </span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vitepress'
import { getAssetsForRoute } from '../utils/assetRegistry'

const route = useRoute()
const assets = ref([])

function formatSize(n){ if (!n && n !== 0) return ''
  const kb = 1024
  if (n < kb) return n + ' B'
  if (n < kb*kb) return Math.round(n/kb) + ' KB'
  return Math.round(n/(kb*kb)) + ' MB'
}

async function loadAssetsForCurrentRoute() {
  assets.value = []
  const list = await getAssetsForRoute(route.path)
  assets.value = list
}

onMounted(() => {
  loadAssetsForCurrentRoute()
})

watch(() => route.path, () => {
  loadAssetsForCurrentRoute()
})
</script>

<style>
.related-files{margin-top:2rem;padding:1rem;border-top:1px solid var(--vp-c-divider)}
.related-files h3{margin:0 0 .5rem}
.asset-item{display:flex;gap:1rem;align-items:center;padding:.25rem 0}
.asset-name{font-weight:600}
.asset-meta{color:var(--vp-c-muted);font-size:.9rem}
.asset-actions a{margin-left:.75rem}
</style>
