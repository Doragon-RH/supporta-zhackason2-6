import { createRouter, createWebHistory } from "vue-router";
import SignIn from "@/views/SignIn.vue";
import SignUp from "@/views/SignUp.vue";
import ProfileRegister from "@/views/ProfileRegister.vue";
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
      path: "/profile/register",
      name: "ProfileRegister",
      component: ProfileRegister,
    },
    {
      path: "/signin",
      name: "SignIn",
      component: SignIn,
    },
    {
      path: "/",
      name: "Home",
      component: Home,
    },
  ],
});

export default router;
