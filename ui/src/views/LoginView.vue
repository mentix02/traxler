<script lang="ts">
import { defineComponent } from "vue";
import { getTokenResponse } from "@/api/auth";
import useAuthStore from "@/stores/auth";

export default defineComponent({
  data: () => ({
    username: "",
    password: "",
    loading: false,
    authStore: useAuthStore(),
  }),
  mounted() {
    (this.$refs.username as HTMLInputElement).focus();
    document.title = "Sign In";
  },
  methods: {
    async handleSubmit(_: Event) {
      this.loading = true;
      try {
        const tokenResponse = await getTokenResponse(
          this.username,
          this.password
        );
        this.loading = false;
        this.authStore.logIn(tokenResponse);
        await this.$router.push({ name: "home" });
      } catch (e: any) {
        alert(e.message);
        this.loading = false;
      }
    },
  },
});
</script>

<template>
  <div class="text-center">
    <h1>Sign In</h1>
    <p class="text-muted">Log back in to start managing your own taxes!</p>
    <hr />
  </div>

  <form @submit.prevent="handleSubmit">
    <div class="row">
      <div class="col-sm-12 col-md-12 col-lg-6 offset-lg-3 mb-3">
        <div class="form-group">
          <label for="username" class="form-label">Username</label>
          <input
            required
            type="text"
            id="username"
            ref="username"
            v-model="username"
            :disabled="loading"
            class="form-control"
            placeholder="johnny"
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
            v-model="password"
            :disabled="loading"
            class="form-control"
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
            Log In
          </button>
        </div>
      </div>
    </div>
  </form>
</template>
