import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toast from "vue-toastification";
import App from './App.vue'
import router from './router'

import './assets/styles/base.css'
import '@formkit/themes/genesis'
import "vue-toastification/dist/index.css";

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast)

app.mount('#app')
