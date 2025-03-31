//@ts-expect-error types not necessary
import Aura from '@primeuix/themes/aura'

import 'primeicons/primeicons.css'
import PrimeVue from 'primevue/config'
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: '.my-app-dark',
    },
  },
})
app.use(router)

app.mount('#app')
