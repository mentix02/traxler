<script setup lang="ts">
import useAuthStore from "@/stores/auth";
import Landing from "@/components/Landing.vue";
import UserList from "@/components/UserList.vue";
import TaxListView from "@/views/TaxListView.vue";

const authStore = useAuthStore();
</script>

<template>
  <Landing v-if="!authStore.isAuthenticated" />
  <UserList v-else-if="authStore.user.role > 0" />
  <TaxListView v-else />
</template>
