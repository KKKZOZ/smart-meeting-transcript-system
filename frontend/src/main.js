import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import router from './router';
import './assets/css/nucleo-icons.css';
import './assets/css/nucleo-svg.css';
import ArgonDashboard from './argon-dashboard';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'; // 引入样式

const appInstance = createApp(App);
appInstance.use(store);
appInstance.use(router);
appInstance.use(ElementPlus);
appInstance.use(ArgonDashboard);
appInstance.mount('#app');
