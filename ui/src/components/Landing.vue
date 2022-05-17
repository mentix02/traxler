<script setup lang="ts">
import { RouterLink } from "vue-router";
document.title = "Traxler";
</script>

<template>
  <div class="row">
    <div class="col">
      <div class="text-end">
        <h1>Old user?</h1>
        <p class="text-muted">Log back in to start managing your own taxes!</p>
        <RouterLink :to="{ name: 'login' }" class="btn btn-primary btn-lg">
          Login Here
        </RouterLink>
      </div>
    </div>
    <div class="col-1">
      <div class="text-center"><span class="vertical-line"></span></div>
    </div>
    <div class="col">
      <div class="text-start">
        <h1>New user?</h1>
        <p class="text-muted">Sign up today and start paying taxes!</p>
        <RouterLink :to="{ name: 'signup' }" class="btn btn-primary btn-lg">
          Register Now
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.vertical-line {
  margin: 0 10px;
  height: 150px;
  display: inline-block;
  border-left: 1px solid #ccc;
}
</style>
