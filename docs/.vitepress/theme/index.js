import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import Breadcrumbs from './components/Breadcrumbs.vue'

export default {
  ...DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'page-top': () => h(Breadcrumbs),
    })
  },
}
