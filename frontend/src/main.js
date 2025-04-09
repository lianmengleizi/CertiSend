import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vant 组件按需引入
import { 
  Button, Field, CellGroup, Area, 
  Dialog, Form, Toast, Popup 
} from 'vant'
import 'vant/lib/index.css'

// Element Plus 组件
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)

app.use(router)

// Vant 组件注册
app.use(Button)
app.use(Field)
app.use(CellGroup)
app.use(Area)
app.use(Form)
app.use(Dialog)
app.use(Toast)
app.use(Popup)

// Element Plus 注册
app.use(ElementPlus)

app.mount('#app')