<script lang="ts">
import { defineComponent } from "vue";
import type { CreateUpdateTaxData } from "@/api/types/tax";
import {
  INTERSTATE_TRANSACTION,
  INTRASTATE_TRANSACTION,
} from "@/api/types/tax";
import type { TaxpayerUsernameId } from "@/api/types/taxpayer";
import { getTaxpayerUsernames } from "@/api/taxpayer";

export default defineComponent({
  name: "CreateTaxView",
  data: () => ({
    loading: true,
    usernames: [] as TaxpayerUsernameId[],
    tax: {
      cgst: 0,
      payer: 0,
      transaction_type: INTERSTATE_TRANSACTION,
      due_date: new Date().toISOString().substring(0, 10),
      active_due: {
        salary_income: 0,
        share_market_income: 0,
      },
    } as CreateUpdateTaxData,
  }),
  methods: {
    async handleSubmit(_: Event) {
      console.log(this.tax);
    },
  },
  mounted() {
    getTaxpayerUsernames().then((usernames) => {
      this.usernames = usernames;
      this.loading = false;
    });
  },
});
</script>

<template>
  <div class="text-center">
    <h2>Create Tax</h2>
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
          <label for="tax-payer">Tax Payer</label>
          <select
            class="form-control"
            id="tax-payer"
            v-model="tax.payer"
            required
          >
            <option v-for="username in usernames" :value="username.id">
              {{ username.username }}
            </option>
          </select>
        </div>
      </div>

      <div class="col-sm-12 col-md-12 col-lg-3 offset-lg-3 mb-3">
        <label for="salary_income" class="form-label">Salary Income</label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text">₹</span>
          </div>
          <input
            required
            type="number"
            class="form-control"
            id="salary_income"
            v-model="tax.active_due.salary_income"
          />
        </div>
      </div>
      <div class="col-sm-12 col-md-12 col-lg-3 mb-3">
        <label for="share_market_income" class="form-label">
          Share market Income
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
    </div>
  </form>
</template>
