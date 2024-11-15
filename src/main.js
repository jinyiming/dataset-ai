import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import VueOffice from '@vue-office/docx'
import VueOfficePdf from '@vue-office/pdf'
import VueOfficeExcel from '@vue-office/excel'

const app = createApp(App)

app.use(router)
app.use(ElementPlus)
app.use(VueOffice)
app.use(VueOfficePdf)
app.use(VueOfficeExcel)

app.mount('#app')