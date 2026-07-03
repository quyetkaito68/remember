import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import Breadcrumbs from './components/Breadcrumbs.vue'
import RelatedFilesPanel from './components/RelatedFilesPanel.vue'

export default {
  ...DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'page-top': () => h(Breadcrumbs),
      'page-bottom': () => h(RelatedFilesPanel)
    })
  },
}
