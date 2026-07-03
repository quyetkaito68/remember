<script setup>
import { computed } from 'vue'
import { useRoute } from 'vitepress'

const route = useRoute()

const breadcrumbs = computed(() => {
  const segments = route.path.split('/').filter(Boolean)
  const crumbs = [{ text: 'Home', link: '/' }]
  let current = ''

  for (const segment of segments) {
    current += `/${segment}`
    crumbs.push({
      text: segment.replace(/[-_]/g, ' ').replace(/\b\w/g, (char) => char.toUpperCase()),
      link: `${current}/`,
    })
  }

  return crumbs
})
</script>

<template>
  <nav class="vp-breadcrumbs" aria-label="Breadcrumb">
    <ul>
      <li v-for="(crumb, index) in breadcrumbs" :key="crumb.link">
        <template v-if="index + 1 < breadcrumbs.length">
          <a :href="crumb.link">{{ crumb.text }}</a>
          <span class="separator">/</span>
        </template>
        <template v-else>
          <span aria-current="page">{{ crumb.text }}</span>
        </template>
      </li>
    </ul>
  </nav>
</template>

<style>
.vp-breadcrumbs {
  margin-bottom: 1.1rem;
  font-size: 0.95rem;
}
.vp-breadcrumbs ul {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  list-style: none;
  padding: 0;
  margin: 0;
}
.vp-breadcrumbs li {
  display: flex;
  align-items: center;
  color: var(--vp-c-text);
}
.vp-breadcrumbs a {
  color: var(--vp-c-link);
  text-decoration: none;
}
.vp-breadcrumbs a:hover {
  text-decoration: underline;
}
.vp-breadcrumbs .separator {
  margin: 0 0.4rem;
  color: var(--vp-c-muted);
}
</style>
