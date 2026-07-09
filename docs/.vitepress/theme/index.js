import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import Breadcrumbs from './components/Breadcrumbs.vue'
import RelatedFilesPanel from './components/RelatedFilesPanel.vue'
import AssetViewer from './components/AssetViewer.vue'

const Layout = DefaultTheme.Layout

export default {
  ...DefaultTheme,
  Layout() {
    return h(Layout, null, {
      'doc-top': () => h(Breadcrumbs),
      'doc-footer-before': () => h(RelatedFilesPanel)
    })
  },
  enhanceApp({ app }) {
    app.component('AssetViewer', AssetViewer)
  },
}
