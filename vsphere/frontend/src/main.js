import { createApp } from 'vue'
import { createPinia } from 'pinia';
import App from './App.vue'
import Emitter from 'tiny-emitter';
import router from './router'

const app = createApp(App);

// Importing BootStrap
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-vue/dist/bootstrap-vue.css"
import "bootswatch/dist/flatly/bootstrap.min.css";
//Importing FontAwesome
import '@fortawesome/fontawesome-free/js/all'

app.config.globalProperties.$msalInstance = {};
app.config.globalProperties.$emitter = new Emitter();

app.use(createPinia());
app.use(router);
  app.mount("#app");

