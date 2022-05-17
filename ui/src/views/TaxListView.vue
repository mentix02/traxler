<script setup lang="ts">
import { onMounted, ref, computed, watch } from "vue";

import useAuthStore from "@/stores/auth";
import { payTax, getTaxes } from "@/api/tax";
import { formatTaxpayerName } from "@/utils";
import type { StatusType, Tax } from "@/api/types/tax";
import {
  STATUS_NEW,
  STATUS_PAID,
  STATUS_DELAYED,
  INTERSTATE_TRANSACTION,
} from "@/api/types/tax";

type Filter = {
  issued?: string;
  status?: StatusType | "All";
  total_range: [number, number];
};

const authStore = useAuthStore();
const taxes = ref<Tax[]>([]);
const loading = ref<boolean>(true);
const minimumTotalTax = ref<number>(0);
const maximumTotalTax = ref<number>(0);
const filter = ref<Filter>({
  status: "All",
  total_range: [0, Infinity],
});

const resetFilters = () => {
  filter.value = {
    status: "All",
    total_range: [minimumTotalTax.value, maximumTotalTax.value],
  };
};

const filteredTaxes = computed(() => {
  const { issued, status, total_range } = filter.value;
  const [min, max] = total_range;

  return taxes.value.filter((tax) => {
    if (issued && tax.active_due.issued_on !== issued) {
      return false;
    }
    if (status && status !== "All" && tax.status !== status) {
      return false;
    }
    if (min && tax.active_due.total < min) {
      return false;
    }
    return !(max && tax.active_due.total > max);
  });
});

const getCardClasses = (status: StatusType) => ({
  "border-info": status === STATUS_NEW,
  "border-success": status === STATUS_PAID,
  "border-danger": status === STATUS_DELAYED,
});

const handlePayment = async (idx: number, tax_id: number) => {
  taxes.value[idx] = await payTax(tax_id);
};

watch(
  () => taxes.value,
  () => {
    minimumTotalTax.value = taxes.value.reduce(
      (acc, t) => Math.min(acc, t.active_due.total),
      Infinity
    );
    maximumTotalTax.value = taxes.value.reduce(
      (acc, t) => Math.max(acc, t.active_due.total),
      -Infinity
    );
    filter.value.total_range = [minimumTotalTax.value, maximumTotalTax.value];
  }
);

onMounted(async () => {
  document.title = "Manage Taxes";
  taxes.value = await getTaxes();
  loading.value = false;
});
</script>

<template>
  <div class="text-center">
    <h1 v-if="authStore.user.role > 0">Manage All Taxes</h1>
    <h1 v-if="authStore.user.role === 0">Manage Your Taxes</h1>
  </div>
  <div class="text-center" v-if="loading">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div class="row" v-else>
    <div class="col-sm-12 col-md-12 col-lg-8 offset-lg-2 my-2 py-3 bg-light">
      <h3>Filters</h3>
      <hr />
      <form class="row">
        <div class="col-sm-12 col-md-12 col-lg-6 mb-sm-2">
          <label class="form-label" for="minimum">Minimum total tax</label>
          <input
            type="number"
            class="form-control"
            :min="minimumTotalTax"
            :max="maximumTotalTax"
            v-model="filter.total_range[0]"
          />
          <input
            id="minimum"
            type="range"
            class="form-range"
            :min="minimumTotalTax"
            :max="maximumTotalTax"
            v-model.number="filter.total_range[0]"
          />
        </div>
        <div class="col-sm-12 col-md-12 col-lg-6 mb-sm-2">
          <label class="form-label" for="maximum">Maximum total tax</label>
          <input
            type="number"
            class="form-control"
            :min="minimumTotalTax"
            :max="maximumTotalTax"
            v-model="filter.total_range[1]"
          />
          <input
            id="maximum"
            type="range"
            class="form-range"
            :min="minimumTotalTax"
            :max="maximumTotalTax"
            v-model.number="filter.total_range[1]"
          />
        </div>
        <div class="col-sm-12 col-md-12 col-lg-6 mb-sm-2">
          <label class="form-label" for="issued">Issued on</label>
          <input type="date" class="form-control" v-model="filter.issued" />
        </div>
        <div class="col-sm-12 col-md-12 col-lg-6 mb-sm-2">
          <label class="form-label" for="status">Status</label>
          <select id="status" class="form-select" v-model="filter.status">
            <option selected value="All">All</option>
            <option value="New">New</option>
            <option value="Paid">Paid</option>
            <option value="Delayed">Delayed</option>
          </select>
        </div>
        <div class="col-sm-12 col-md-12 col-lg-4 offset-4 mt-3">
          <div class="d-grid">
            <button
              type="button"
              @click="resetFilters"
              class="btn btn-outline-primary"
            >
              Reset
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
  <h3 class="text-center" v-if="!loading && filteredTaxes.length === 0">
    0 results found
  </h3>
  <div class="row justify-content-center">
    <div
      v-for="(tax, idx) in filteredTaxes"
      class="col-sm-12 col-md-12 col-lg-4 mb-sm-3 mb-md-3 mb-lg-4"
    >
      <div class="card" :class="getCardClasses(tax.status)">
        <div class="card-header">Status : {{ tax.status }} (#{{ tax.id }})</div>
        <div class="card-body">
          <h5 class="card-title">Total : ₹ {{ tax.active_due.total }}</h5>
          <div class="text-body">
            {{
              tax.active_due.transaction_type === INTERSTATE_TRANSACTION
                ? "Interstate"
                : "Intrastate"
            }}
            tax for {{ formatTaxpayerName(tax.payer) }}
          </div>
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <abbr title="Central GST">CGST</abbr> : {{ tax.active_due.cgst }}%
            <span style="float: right">
              <abbr title="State GST">SGST</abbr> : {{ tax.sgst }}%
            </span>
          </li>
          <li class="list-group-item">
            Due : {{ tax.due_date }}
            <span style="float: right">
              Issued : {{ tax.active_due.issued_on }}
            </span>
          </li>
          <li class="list-group-item">
            Salary : ₹{{ tax.active_due.salary_income }}
            <span style="float: right">
              Share market : ₹{{ tax.active_due.share_market_income }}
            </span>
          </li>
        </ul>
        <div class="card-footer" v-if="authStore.user.role === 0">
          <button
            :disabled="tax.paid"
            class="btn btn-outline-success"
            @click="handlePayment(idx, tax.id)"
          >
            {{ tax.paid ? "Paid" : "Pay" }}
          </button>
        </div>
        <div class="card-footer" v-if="authStore.user.role > 0">
          <button
            :disabled="tax.paid"
            class="btn btn-outline-primary"
            @click="$router.push({ name: 'tax', params: { id: tax.id } })"
          >
            {{ tax.paid ? "Paid" : "Edit" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
