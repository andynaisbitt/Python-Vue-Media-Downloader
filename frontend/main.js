import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import './index.css'  // if you're using this for Tailwind

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')