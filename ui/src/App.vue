<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

import Navigation from "@/components/Navigation.vue";

export default defineComponent({
  name: "Traxler",
  components: {
    Navigation,
    RouterView,
  },
});
</script>

<template>
  <Navigation />
  <main class="container lg-padding-top">
    <RouterView />
  </main>
</template>

<style>
@import "assets/bootstrap.min.css";
.lg-padding-top {
  padding-top: 7.5rem;
}
</style>
