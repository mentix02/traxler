<script setup lang="ts">
import { ref } from "vue";

import type { TaxDueInfo } from "@/api/types/tax";
import { INTERSTATE_TRANSACTION } from "@/api/types/tax";

const props = defineProps<{
  history?: TaxDueInfo[];
}>();

const selfHistory = ref<TaxDueInfo[]>([]);

const intv = setInterval(() => {
  if (props.history !== undefined) {
    selfHistory.value = JSON.parse(JSON.stringify(props.history));
    clearInterval(intv);
  }
}, 200);
</script>

<template>
  <ul class="timeline">
    <li
      class="event"
      :data-date="taxDue.issued_on"
      v-for="taxDue in selfHistory"
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
        Due Date : <strong>{{ taxDue.due_date }}</strong>
        <br />
        Salary Income : ₹<strong>{{ taxDue.salary_income }}</strong>
        <br />
        Share Market Income: ₹<strong>{{ taxDue.share_market_income }}</strong>
      </p>
    </li>
  </ul>
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
