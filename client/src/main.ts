import { createApp } from "vue";
import { createPinia } from "pinia";
import { dialogStore } from "./stores";

import App from "./App.vue";
import router from "./router";

import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "@mdi/font/css/materialdesignicons.css";

const vuetify = createVuetify({
  components,
  directives,
});

import axios from "axios";

axios.defaults.baseURL = "http://localhost:8888/";

const app = createApp(App);

app.use(createPinia());
app.provide("dialog", dialogStore);
app.use(router);
app.use(vuetify);

app.mount("#app");
