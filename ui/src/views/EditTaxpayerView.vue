<script setup lang="ts"></script>

<script lang="ts">
import { defineComponent } from "vue";

import { getStates } from "@/api/tax";
import type { State } from "@/api/types/tax";
import type { UserEditData } from "@/api/types/auth";
import { editTaxPayer, getTaxPayerData } from "@/api/taxpayer";

export default defineComponent({
  name: "EditTaxpayerView",
  data: () => ({
    loading: true,
    states: [] as State[],
    userData: {} as UserEditData,
  }),
  methods: {
    async handleEdit(_: Event) {
      const username = this.$route.params.username as string;
      this.loading = true;
      await editTaxPayer(username, this.userData);
      window.location.reload();
    },
  },
  async mounted() {
    const username = this.$route.params.username as string;
    document.title = `Edit ${username}`;
    this.states = await getStates();
    this.userData = await getTaxPayerData(username);
    this.loading = false;
    await this.$nextTick(() => {
      (this.$refs.first_name as HTMLInputElement).focus();
    });
  },
});
</script>

<template>
  <h1 class="text-center">
    Update <i>{{ $route.params.username }}</i>
  </h1>
  <hr />
  <div class="text-center" v-if="loading">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <form v-if="!loading" @submit.prevent="handleEdit" class="row">
    <div class="col-sm-12 col-md-12 col-lg-3 offset-lg-3 mb-3">
      <label for="first_name" class="form-label">First Name</label>
      <input
        required
        type="text"
        id="first_name"
        ref="first_name"
        class="form-control"
        v-model="userData.first_name"
      />
    </div>
    <div class="col-sm-12 col-md-12 col-lg-3 mb-3">
      <label for="last_name" class="form-label">Last Name</label>
      <input
        required
        type="text"
        id="last_name"
        class="form-control"
        v-model="userData.last_name"
      />
    </div>
    <div class="col-sm-12 col-md-12 col-lg-6 offset-lg-3 mb-3">
      <label for="username" class="form-label">Username</label>
      <input
        required
        type="text"
        id="username"
        class="form-control"
        v-model="userData.username"
      />
    </div>
    <div class="col-sm-12 col-md-12 col-lg-3 offset-lg-3 mb-3">
      <label for="email" class="form-label">Email</label>
      <input
        required
        type="email"
        id="email"
        class="form-control"
        v-model="userData.email"
      />
    </div>
    <div class="col-sm-12 col-md-12 col-lg-3 mb-3">
      <label for="company_name" class="form-label">Company name</label>
      <input
        required
        type="text"
        id="company_name"
        class="form-control"
        v-model="userData.info.business_name"
      />
    </div>
    <div class="col-sm-12 col-md-12 col-lg-3 offset-lg-3 mb-3">
      <label class="form-label" for="gstin">GST No.</label>
      <input
        required
        id="gstin"
        type="text"
        maxlength="15"
        class="form-control"
        v-model="userData.info.gstin"
      />
    </div>
    <div class="col-sm-12 col-md-12 col-lg-3 mb-3">
      <label class="form-label" for="pan">PAN No.</label>
      <input
        required
        id="pan"
        type="text"
        maxlength="15"
        class="form-control"
        v-model="userData.info.pan"
      />
    </div>
    <div class="col-sm-12 col-md-12 col-lg-3 offset-lg-3 mb-3">
      <label for="address" class="form-label">Address</label>
      <textarea
        rows="4"
        id="address"
        class="form-control"
        v-model="userData.info.address"
      ></textarea>
    </div>
    <div class="col-sm-12 col-md-12 col-lg-3 mb-3">
      <label for="city" class="form-label">State</label>
      <select
        required
        id="state"
        class="form-select"
        v-model="userData.info.state"
      >
        <option v-for="state in states" :value="state.id">
          {{ state.name }} - {{ state.tax }}%
        </option>
      </select>
    </div>
    <div class="col-sm-12 col-md-12 col-lg-4 offset-lg-4 mt-3">
      <div class="d-grid gap-2">
        <button type="submit" class="btn btn-outline-primary">Update</button>
        <button
          type="button"
          class="btn btn-outline-secondary"
          @click="$router.push({ name: 'home' })"
        >
          Cancel
        </button>
      </div>
    </div>
  </form>
</template>
