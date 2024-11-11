import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import * as echarts from 'echarts'

const app = createApp(App)
app.use(router)
app.mount('#app')