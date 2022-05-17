<script setup lang="ts">
import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";

import { formatTaxpayerName } from "@/utils";
import { getTaxPayers } from "@/api/taxpayer";
import type { TaxPayer } from "@/api/types/taxpayer";

const taxpayers = ref<TaxPayer[]>();
const loading = ref<boolean>(true);

onMounted(async () => {
  document.title = "Manage Users";
  taxpayers.value = await getTaxPayers();
  loading.value = false;
});
</script>

<template>
  <div class="text-center">
    <h2>Manage Taxpayers</h2>
  </div>
  <hr />
  <h3 class="text-center" v-if="!loading && taxpayers.length === 0">
    None found
  </h3>
  <br />
  <div class="row justify-content-center">
    <div class="text-center" v-if="loading">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div
      v-if="!loading"
      v-for="payer in taxpayers"
      class="col-sm-12 col-md-12 col-lg-4 mb-3"
    >
      <div
        class="card"
        :class="{
          'border-danger': payer.total_taxes > payer.paid_taxes,
        }"
      >
        <div class="card-header">
          {{ formatTaxpayerName(payer.username) }} (#{{ payer.info.pan }})
          <span
            class="badge rounded-pill"
            :class="{
              'bg-danger': payer.total_taxes > payer.paid_taxes,
              'bg-success': payer.paid_taxes <= payer.total_taxes,
            }"
            style="float: right"
          >
            {{ payer.paid_taxes }} / {{ payer.total_taxes }}
          </span>
        </div>
        <div class="card-body">
          <h5 class="card-title">
            {{ payer.first_name }} {{ payer.last_name }}
          </h5>
          <h6 class="card-subtitle mb-2 text-muted">
            {{ payer.info.address }}, {{ payer.info.state }}
          </h6>
          <p class="card-text">
            Company: {{ payer.info.business_name }}
            <br />
            Email: {{ payer.email }}
          </p>
        </div>
        <div class="card-footer">
          <div class="btn-group">
            <RouterLink
              :to="{ name: 'taxpayer', params: { username: payer.username } }"
              class="btn btn-outline-primary"
            >
              view
            </RouterLink>
            <RouterLink
              :to="{ name: 'taxpayer', params: { username: payer.username } }"
              class="btn btn-outline-success"
            >
              edit
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
