<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";

import useAuthStore from "@/stores/auth";

const showNavigation = ref<boolean>(false);

const authStore = useAuthStore();
const toggleShow = () => {
  showNavigation.value = !showNavigation.value;
};
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark fixed-top bg-primary">
    <div class="container">
      <RouterLink class="navbar-brand" :to="{ name: 'home' }">
        Traxler
      </RouterLink>
      <button
        type="button"
        @click="toggleShow"
        aria-expanded="false"
        class="navbar-toggler"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" :class="{ show: showNavigation }">
        <ul v-if="!authStore.isAuthenticated" class="navbar-nav me-auto">
          <li class="nav-item">
            <RouterLink
              class="nav-link"
              activeClass="active"
              :to="{ name: 'home' }"
            >
              Home
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink
              class="nav-link"
              activeClass="active"
              :to="{ name: 'login' }"
            >
              Login
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink
              class="nav-link"
              activeClass="active"
              :to="{ name: 'signup' }"
            >
              Register
            </RouterLink>
          </li>
        </ul>

        <ul v-else class="navbar-nav me-auto">
          <li class="nav-item" v-if="authStore.user.role > 0">
            <RouterLink
              class="nav-link"
              activeClass="active"
              :to="{ name: 'home' }"
            >
              Users
            </RouterLink>
          </li>
          <li class="nav-item" v-if="authStore.user.role > 0">
            <RouterLink
              class="nav-link"
              activeClass="active"
              :to="{ name: 'taxes' }"
            >
              Taxes
            </RouterLink>
          </li>
          <li class="nav-item" v-if="authStore.user.role > 0">
            <RouterLink
              class="nav-link"
              activeClass="active"
              :to="{ name: 'create' }"
            >
              Create Tax
            </RouterLink>
          </li>
          <li class="nav-item">
            <a href="#" @click="authStore.logOut()" class="nav-link">
              Sign Out
            </a>
          </li>
        </ul>

        <span v-if="authStore.isAuthenticated" class="navbar-text">
          signed in as {{ authStore.user.username }}
        </span>
      </div>
    </div>
  </nav>
</template>

<style></style>
