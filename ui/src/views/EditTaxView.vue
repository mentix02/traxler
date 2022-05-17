<script lang="ts">
import { defineComponent } from "vue";

import { getTax, editTax } from "@/api/tax";
import type { CreateUpdateTaxData } from "@/api/types/tax";
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
      const id = this.$route.params.id as string;
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
      <ul class="timeline">
        <li
          class="event"
          :data-date="taxDue.issued_on"
          v-for="taxDue in tax.history"
        >
          <h1>Total : ₹{{ taxDue.total }}</h1>
          <p>
            CGST : <strong>{{ taxDue.cgst }}%</strong>
            <br />
            Transaction Type :
            <strong>{{
              taxDue.transaction_type === INTERSTATE_TRANSACTION
                ? "Interstate"
                : "Intrastate"
            }}</strong>
            <br />
            Salary Income : ₹<strong>{{ taxDue.salary_income }}</strong>
            <br />
            Share Market Income: ₹<strong>{{
              taxDue.share_market_income
            }}</strong>
          </p>
        </li>
      </ul>
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
              v-model="tax.due_date"
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
                  !tax.due_date ||
                  !tax.active_due.cgst ||
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

<style scoped>
.timeline {
  border-left: 3px solid #727cf5;
  border-bottom-right-radius: 4px;
  border-top-right-radius: 4px;
  background: rgba(114, 124, 245, 0.09);
  margin: 0 auto;
  letter-spacing: 0.2px;
  position: relative;
  line-height: 1.4em;
  font-size: 1.03em;
  padding: 50px;
  list-style: none;
  text-align: left;
  max-width: 100%;
}

@media (max-width: 767px) {
  .timeline {
    max-width: 98%;
    padding: 25px;
  }
}

.timeline h1 {
  font-weight: 300;
  font-size: 1.4em;
}

.timeline h2,
.timeline h3 {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 10px;
}

.timeline .event {
  border-bottom: 1px dashed #e8ebf1;
  padding-bottom: 25px;
  margin-bottom: 25px;
  position: relative;
}

@media (max-width: 767px) {
  .timeline .event {
    padding-top: 30px;
  }
}

.timeline .event:last-of-type {
  padding-bottom: 0;
  margin-bottom: 0;
  border: none;
}

.timeline .event:before,
.timeline .event:after {
  position: absolute;
  display: block;
  top: 0;
}

.timeline .event:before {
  left: -207px;
  content: attr(data-date);
  text-align: right;
  font-weight: 100;
  font-size: 0.9em;
  min-width: 120px;
}

@media (max-width: 767px) {
  .timeline .event:before {
    left: 0;
    text-align: left;
  }
}

.timeline .event:after {
  -webkit-box-shadow: 0 0 0 3px #727cf5;
  box-shadow: 0 0 0 3px #727cf5;
  left: -55.8px;
  background: #fff;
  border-radius: 50%;
  height: 9px;
  width: 9px;
  content: "";
  top: 5px;
}

@media (max-width: 767px) {
  .timeline .event:after {
    left: -31.8px;
  }
}

.rtl .timeline {
  border-left: 0;
  text-align: right;
  border-radius: 4px 0 0 4px;
  border-right: 3px solid #727cf5;
}

.rtl .timeline .event::before {
  left: 0;
  right: -170px;
}

.rtl .timeline .event::after {
  left: 0;
  right: -55.8px;
}
</style>
