import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import SignUpView from "@/views/SignUpView.vue";
import TaxListView from "@/views/TaxListView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import CreateTaxView from "@/views/CreateTaxView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/taxpayer/:username",
      name: "taxpayer",
      component: () => import("@/views/EditTaxpayerView.vue"),
    },
    {
      path: "/tax/:id",
      name: "tax",
      component: () => import("@/views/EditTaxView.vue"),
    },
    {
      path: "/taxes",
      name: "taxes",
      component: TaxListView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/create",
      name: "create",
      component: CreateTaxView,
    },
    {
      path: "/:pathMatch(.*)*",
      component: NotFoundView,
    },
  ],
});

export default router;
