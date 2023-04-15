import { createRouter, createWebHistory } from "vue-router";
import SignIn from "@/views/SignIn.vue";
import SignUp from "@/views/SignUp.vue";
import Home from "@/views/Home.vue";
import ProfileRegister from "@/views/ProfileRegister.vue";
import Friend from "@/views/Friend.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/signup",
      name: "SignUp",
      component: SignUp,
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
    {
      path: "/profile/register",
      name: "ProfileRegister",
      component: ProfileRegister,
    },
    {
      path: "/friend",
      name: "Friend",
      component: Friend,
    },
  ],
});

export default router;
