<script setup lang="ts">
import { onMounted, ref, computed } from "vue";

import useAuthStore from "@/stores/auth";
import { payTax, getTaxes } from "@/api/tax";
import type { StatusType, Tax } from "@/api/types/tax";
import { STATUS_DELAYED, STATUS_NEW, STATUS_PAID } from "@/api/types/tax";

type Filter = {
  issued?: string;
  status?: StatusType;
  total_range?: [number, number];
};

const authStore = useAuthStore();
const taxes = ref<Tax[]>([]);
const filter = ref<Filter>({});
const loading = ref<boolean>(true);

const handlePayment = async (idx: number, tax_id: number) => {
  taxes.value[idx] = await payTax(tax_id);
};

const filteredTaxes = computed(() => {
  const { issued, status, total_range } = filter.value;
  const [min, max] = total_range || [0, Infinity];

  return taxes.value.filter((tax) => {
    if (issued && tax.active_due.issued_on !== issued) {
      return false;
    }
    if (status && tax.status !== status) {
      return false;
    }
    if (min && tax.active_due.total < min) {
      return false;
    }
    return !(max && tax.active_due.total > max);
  });
});

const getCardClasses = (status: StatusType) => ({
  "bg-danger": status === STATUS_DELAYED,
  "border-info": status === STATUS_NEW,
  "border-success": status === STATUS_PAID,
});

onMounted(async () => {
  document.title = "Manage Taxes";
  taxes.value = await getTaxes();
  loading.value = false;
});
</script>

<template>
  <div class="text-center">
    <h2 v-if="authStore.user.role > 0">Manage All Taxes</h2>
    <h2 v-if="authStore.user.role === 0">Manage Your Taxes</h2>
  </div>
  <hr />
  <h3 class="text-center" v-if="!loading && filteredTaxes.length === 0">
    None found
  </h3>
  <br />
  <div class="text-center" v-if="loading">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div class="row" v-else>
    <div
      v-for="(tax, idx) in filteredTaxes"
      class="col-sm-12 col-md-12 col-lg-4 mb-3"
    >
      <div class="card" :class="getCardClasses(tax.status)">
        <div class="card-header">Status : {{ tax.status }} (#{{ tax.id }})</div>
        <div class="card-body">
          <h5 class="card-title">Total : Rs. {{ tax.active_due.total }}</h5>
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <abbr title="Central GST">CGST</abbr> : {{ tax.cgst }}%
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
        </ul>
        <div class="card-footer">
          <button
            :disabled="tax.paid"
            class="btn btn-outline-success"
            @click="handlePayment(idx, tax.id)"
          >
            {{ tax.paid ? "Paid" : "Pay" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
