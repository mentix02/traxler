<script lang="ts">
import { defineComponent } from "vue";
import { RouterLink } from "vue-router";

export default defineComponent({
  name: "NotFoundView",
  components: { RouterLink },
});
</script>

<template>
  <div class="text-center">
    <h1>404</h1>
    <p>Page not found</p>
    <router-link class="btn btn-primary" to="/">Home</router-link>
  </div>
</template>
