<script lang="ts">
import { defineComponent } from "vue";

import { getTaxpayerUsernames } from "@/api/taxpayer";
import type { CreateUpdateTaxData } from "@/api/types/tax";
import type { TaxpayerUsernameId } from "@/api/types/taxpayer";
import {
  INTERSTATE_TRANSACTION,
  INTRASTATE_TRANSACTION,
} from "@/api/types/tax";
import { createTax } from "@/api/tax";

export default defineComponent({
  name: "CreateTaxView",
  data: () => ({
    INTERSTATE_TRANSACTION,
    INTRASTATE_TRANSACTION,
    loading: true,
    taxpayers: [] as TaxpayerUsernameId[],
    tax: {
      payer: 0,
      active_due: {
        cgst: 0,
        salary_income: 0,
        share_market_income: 0,
        transaction_type: INTERSTATE_TRANSACTION,
        due_date: new Date().toISOString().substring(0, 10),
      },
    } as CreateUpdateTaxData,
  }),
  methods: {
    async handleSubmit(_: Event) {
      createTax(this.tax)
        .then(() => {
          this.$router.push({ name: "taxes" });
        })
        .catch((e: any) => {
          alert(e.message);
        });
    },
  },
  mounted() {
    document.title = "Create Tax";
    getTaxpayerUsernames().then((taxpayers) => {
      this.taxpayers = taxpayers;
      this.loading = false;
    });
  },
});
</script>

<template>
  <div class="text-center">
    <h1>Create Tax</h1>
  </div>
  <hr />
  <br />
  <div class="text-center" v-if="loading">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <form v-if="!loading" @submit.prevent="handleSubmit">
    <div class="row">
      <div class="col-sm-12 col-md-12 col-lg-6 offset-lg-3 mb-3">
        <div class="form-group">
          <label class="form-label" for="tax-payer">Tax Payer</label>
          <select
            required
            id="tax-payer"
            class="form-select"
            v-model="tax.payer"
          >
            <option :value="taxpayer.id" v-for="taxpayer in taxpayers">
              {{ taxpayer.name }} ({{ taxpayer.username }})
            </option>
          </select>
        </div>
      </div>

      <div class="col-sm-12 col-md-12 col-lg-6 offset-lg-3 mb-3">
        <label class="form-label" for="cgst">Central GST (%)</label>
        <div class="input-group">
          <input
            id="cgst"
            type="number"
            v-model="tax.active_due.cgst"
            class="form-control"
          />
          <div class="input-group-append">
            <span class="input-group-text">%</span>
          </div>
        </div>
      </div>

      <div class="col-sm-12 col-md-12 col-lg-3 offset-lg-3 mb-3">
        <label for="salary_income" class="form-label">Salary income</label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">₹</span>
          </div>
          <input
            required
            type="number"
            id="salary_income"
            class="form-control"
            v-model="tax.active_due.salary_income"
          />
        </div>
      </div>
      <div class="col-sm-12 col-md-12 col-lg-3 mb-3">
        <label for="share_market_income" class="form-label">
          Share market income
        </label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">₹</span>
          </div>
          <input
            required
            type="number"
            id="share_market_income"
            class="form-control"
            v-model="tax.active_due.share_market_income"
          />
        </div>
      </div>
      <div class="col-sm-12 col-md-12 col-lg-3 offset-lg-3 mb-3">
        <label for="due_date" class="form-label">Due Date</label>
        <input
          required
          type="date"
          id="due_date"
          class="form-control"
          v-model="tax.active_due.due_date"
        />
      </div>
      <div class="col-sm-12 col-md-12 col-lg-3 mb-3">
        <label for="transaction_type" class="form-label">
          Transaction Type
        </label>
        <select
          required
          class="form-select"
          id="transaction_type"
          v-model="tax.active_due.transaction_type"
        >
          <option :value="INTERSTATE_TRANSACTION">Interstate</option>
          <option :value="INTRASTATE_TRANSACTION">Intrastate</option>
        </select>
      </div>
      <div class="col-sm-12 col-md-12 col-lg-4 offset-lg-4 mt-3">
        <div class="d-grid gap-2">
          <button
            type="submit"
            class="btn btn-primary btn-block"
            :disabled="
              !tax.payer ||
              !tax.active_due.cgst ||
              !tax.active_due.due_date ||
              !tax.active_due.salary_income ||
              !tax.active_due.share_market_income
            "
          >
            Create Tax
          </button>
          <button
            type="button"
            class="btn btn-outline-secondary"
            @click="$router.push({ name: 'home' })"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </form>
</template>
