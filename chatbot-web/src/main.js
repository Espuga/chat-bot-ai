import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/router'
import {i18n} from './i18n/i18n'
import { createPinia } from 'pinia'

import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import Ripple from 'primevue/ripple'

import '/node_modules/primeflex/primeflex.css'
import 'primeicons/primeicons.css'

import Menu from 'primevue/menu';
import Popover from 'primevue/popover';
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog';
import ContextMenu from 'primevue/contextmenu';
import FileUpload from 'primevue/fileupload';

const pinia = createPinia();
const app = createApp(App);

app.component('Menu', Menu);
app.component('Popover', Popover);
app.component('InputText', InputText);
app.component('Button', Button);
app.component('Dialog', Dialog);
app.component('ContextMenu', ContextMenu);
app.component('FileUpload', FileUpload);

app.use(i18n);
app.use(router);
app.use(pinia);

app.use(PrimeVue, {
  theme: {
    preset: Aura
  }, 
  ripple: true
});

app.directive('ripple', Ripple)


app.mount('#app');