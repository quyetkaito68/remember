<template>
  <button
    v-show="visible"
    class="back-to-top"
    aria-label="Back to top"
    title="Lên đầu trang"
    @click="scrollToTop"
  >
    ↑
  </button>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const visible = ref(false)
const threshold = 400

function onScroll() {
  visible.value = window.scrollY > threshold
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style>
.back-to-top{position:fixed;right:1.5rem;bottom:1.5rem;z-index:60;width:2.75rem;height:2.75rem;border:none;border-radius:50%;background-color:var(--vp-c-brand-1);color:var(--vp-c-bg);font-size:1.25rem;font-weight:700;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.25);transition:opacity .2s,transform .2s}
.back-to-top:hover{transform:translateY(-2px);background-color:var(--vp-c-brand-2)}
.back-to-top:focus-visible{outline:2px solid var(--vp-c-brand-3);outline-offset:2px}
</style>
