<script lang="ts">
import { defineComponent } from "vue";

import { getTax, editTax } from "@/api/tax";
import type { CreateUpdateTaxData } from "@/api/types/tax";
import TaxEditHistory from "@/components/TaxEditHistory.vue";
import {
  INTERSTATE_TRANSACTION,
  INTRASTATE_TRANSACTION,
} from "@/api/types/tax";

export default defineComponent({
  name: "EditTaxView",
  data: () => ({
    loading: true,
    INTERSTATE_TRANSACTION,
    INTRASTATE_TRANSACTION,
    tax: {} as CreateUpdateTaxData,
  }),
  methods: {
    async handleEdit(_: Event) {
      this.loading = true;
      await editTax(this.tax.id!, this.tax);
      await this.$router.push({ name: "taxes" });
    },
  },
  mounted() {
    document.title = `Edit Tax ${this.$route.params.id}`;
    getTax(this.$route.params.id as string).then((taxData) => {
      this.tax = taxData;
      this.$nextTick(() => {
        this.loading = false;
      });
    });
  },
  components: { TaxEditHistory },
});
</script>

<template>
  <h1 class="text-center">Edit Tax #{{ $route.params.id }}</h1>
  <hr />
  <div class="text-center" v-if="loading">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div class="row">
    <div class="col-sm-12 col-md-12 col-lg-5 mb-sm-4 mb-md-4">
      <h3>Edit History</h3>
      <TaxEditHistory :history="tax.history" />
    </div>
    <div class="col-sm-12 col-md-12 col-lg-6">
      <form v-if="!loading" @submit.prevent="handleEdit">
        <div class="col-sm-12 col-md-12 col-lg-12 mb-3">
          <div class="form-group">
            <label class="form-label" for="tax-payer">Tax Payer</label>
            <select required disabled id="tax-payer" class="form-select">
              <option selected>
                {{ tax.payer_name }}
              </option>
            </select>
          </div>
        </div>

        <div class="row">
          <div class="col-sm-12 col-md-12 col-lg-12 mb-3">
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

          <div class="col-sm-12 col-md-12 col-lg-6 mb-3">
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
                v-model="tax.history[tax.history.length - 1].salary_income"
              />
            </div>
          </div>

          <div class="col-sm-12 col-md-12 col-lg-6 mb-3">
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

          <div class="col-sm-12 col-md-12 col-lg-6 mb-3">
            <label for="due_date" class="form-label">Due Date</label>
            <input
              required
              type="date"
              id="due_date"
              class="form-control"
              v-model="tax.active_due.due_date"
            />
          </div>

          <div class="col-sm-12 col-md-12 col-lg-6 mb-3">
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
                Update Tax #{{ $route.params.id }}
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
    </div>
  </div>
</template>
