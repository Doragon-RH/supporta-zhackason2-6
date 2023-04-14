import { createRouter, createWebHistory } from "vue-router";
import SignUp from "@/views/SignUp.vue";
import Home from "@/views/Home.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/signup",
      name: "SignUp",
      component: SignUp,
    },
    {
      path: "/",
      name: "Home",
      component: Home,
    },
  ],
});

export default router;
