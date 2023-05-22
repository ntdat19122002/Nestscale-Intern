import {createApp, h} from 'vue/dist/vue.esm-bundler';
import App from './App.vue'
import router from './router'

import './css/reset.css'
import './css/main.css'

var app = createApp({
    name: 'App',
    render: () => {
        return <App/>
    }
})

app.use(router)
app.mount('#app-id')

