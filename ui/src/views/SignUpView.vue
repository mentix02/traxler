<script lang="ts">
import { defineComponent } from "vue";

import { createUser } from "@/api/auth";
import useAuthStore from "@/stores/auth";
import type { UserData } from "@/api/types/auth";

export default defineComponent({
  data: () => ({
    loading: false,
    authStore: useAuthStore(),
    userData: {
      email: "",
      username: "",
      password: "",
      last_name: "",
      first_name: "",
    } as UserData,
  }),
  mounted() {
    document.title = "Sign Up";
    (this.$refs.first_name as HTMLInputElement).focus();
  },
  methods: {
    async handleSubmit(_: Event) {
      this.loading = true;
      try {
        const authState = await createUser(this.userData);
        this.authStore.logIn(authState);
        this.loading = false;
        await this.$router.push({ name: "home" });
      } catch (error: any) {
        alert(error.message);
        this.loading = false;
      }
    },
  },
});
</script>

<template>
  <div class="text-center">
    <h1>Sign Up</h1>
    <p class="text-muted">Sign up today and start paying taxes!</p>
  </div>
  <hr />
  <form @submit.prevent="handleSubmit">
    <div class="row">
      <div class="col-sm-12 col-md-12 col-lg-3 offset-lg-3 mb-3">
        <div class="form-group">
          <label for="first_name" class="form-label">First Name</label>
          <input
            required
            type="text"
            id="first_name"
            ref="first_name"
            placeholder="John"
            :disabled="loading"
            class="form-control"
            v-model="userData.first_name"
          />
        </div>
      </div>
      <div class="col-sm-12 col-md-12 col-lg-3 mb-3">
        <div class="form-group">
          <label for="last_name" class="form-label">Last Name</label>
          <input
            required
            type="text"
            id="last_name"
            placeholder="Doe"
            :disabled="loading"
            class="form-control"
            v-model="userData.last_name"
          />
        </div>
      </div>
      <div class="col-sm-12 col-md-12 col-lg-6 offset-lg-3 mb-3">
        <div class="form-group">
          <label for="username" class="form-label">Username</label>
          <input
            required
            type="text"
            id="username"
            :disabled="loading"
            class="form-control"
            placeholder="johnny"
            v-model="userData.username"
          />
        </div>
      </div>
      <div class="col-sm-12 col-md-12 col-lg-6 offset-lg-3 mb-3">
        <div class="form-group">
          <label for="email" class="form-label">Email</label>
          <input
            required
            id="email"
            type="email"
            :disabled="loading"
            class="form-control"
            v-model="userData.email"
            placeholder="john@doe.com"
          />
        </div>
      </div>
      <div class="col-sm-12 col-md-12 col-lg-6 offset-lg-3 mb-3">
        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <input
            required
            id="password"
            type="password"
            :disabled="loading"
            class="form-control"
            v-model="userData.password"
            placeholder="************"
          />
        </div>
      </div>
      <div class="col-sm-12 col-md-12 col-lg-4 offset-lg-4 mt-3">
        <div class="d-grid gap-2">
          <button :disabled="loading" class="btn btn-primary" type="submit">
            <span
              role="status"
              v-if="loading"
              aria-hidden="true"
              class="spinner-border spinner-border-sm"
            />
            Register
          </button>
        </div>
      </div>
    </div>
  </form>
</template>
