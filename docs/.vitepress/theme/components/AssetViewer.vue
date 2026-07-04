<template>
  <div class="asset-viewer" v-if="asset">
    <div class="asset-header">
      <h2>{{ asset.name }}</h2>
      <div class="meta">{{ asset.type }} · {{ formatSize(asset.size) }} · <a :href="githubRawUrl" target="_blank">Open on GitHub</a>
        <button @click="copyLink">Copy Link</button>
      </div>
      <div class="meta">Last updated: {{ formatDate(asset.lastModified) }} <span v-if="asset.sha">· <code>{{ asset.sha.slice(0,7) }}</code></span></div>
    </div>
    <div class="asset-body">
      <template v-if="isImage">
        <img :src="asset.url" :alt="asset.name" style="max-width:100%" />
      </template>
      <template v-else-if="isPdf">
        <embed :src="asset.url" type="application/pdf" width="100%" height="600px" />
      </template>
      <template v-else-if="isVideo">
        <video controls style="max-width:100%"><source :src="asset.url"></video>
      </template>
      <template v-else-if="isAudio">
        <audio controls style="width:100%"><source :src="asset.url"></audio>
      </template>
      <template v-else-if="isText">
        <pre class="code-block"><code ref="codeEl">{{ content }}</code></pre>
      </template>
      <template v-else>
        <p>No preview available. <a :href="asset.rawUrl || asset.url" download>Download</a></p>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getAssetByUrl } from '../utils/assetRegistry'

const props = defineProps({ assetPath: String })
const asset = ref(null)
const content = ref('')

function formatSize(n){ if (!n && n !==0) return ''
  const kb=1024
  if (n<kb) return n+' B'
  if (n<kb*kb) return Math.round(n/kb)+' KB'
  return Math.round(n/(kb*kb))+' MB'
}

const isTextExt = ext => ['.ps1','.bat','.cmd','.sh','.sql','.json','.xml','.yml','.yaml','.ini','.reg','.env','.txt','.js','.ts','.py','.java','.c','.cpp','.css','.html','.md'].includes(ext)

onMounted(async ()=>{
  const a = await getAssetByUrl(props.assetPath || '')
  if (!a) return
  asset.value = a
  const ext = a.name.includes('.') ? '.' + a.name.split('.').pop().toLowerCase() : ''
  if (isTextExt(ext)){
    try {
      const res = await fetch(a.rawUrl || a.url)
      if (res.ok) content.value = await res.text()
    } catch(e){}
  }
})

const isImage = computed(()=> asset.value && asset.value.type === 'image')
const isPdf = computed(()=> asset.value && asset.value.type === 'pdf')
const isVideo = computed(()=> asset.value && asset.value.type === 'video')
const isAudio = computed(()=> asset.value && asset.value.type === 'audio')
const isText = computed(()=> asset.value && ['powershell','batch','shell','sql','json','xml','yaml','ini','registry','env','file'].includes(asset.value.type) || (asset.value && asset.value.name && asset.value.name.match(/\.(txt|md|js|ts|py|java|c|cpp|css|html)$/i)))

const githubRawUrl = computed(()=> asset.value ? asset.value.rawUrl || asset.value.url : '')

function copyLink(){
  const u = asset.value ? location.origin + (asset.value.rawUrl || asset.value.url) : ''
  if (!u) return
  navigator.clipboard?.writeText(u)
}

function formatDate(ts){ if (!ts) return ''
  const d = new Date(ts*1000)
  return d.toISOString().replace('T',' ').slice(0,19)
}
</script>

<style>
.asset-header h2{margin:.25rem 0}
.meta{color:var(--vp-c-muted);font-size:.9rem}
.code-block{background:var(--vp-canvas-subtle);padding:1rem;overflow:auto}
</style>
