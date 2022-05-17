import configureEndpoint from "./host";

import useAuthStore from "@/stores/auth";
import type { Tax, State } from "@/api/types/tax";
import type { CreateUpdateTaxData } from "@/api/types/tax";

const BASE_URL = configureEndpoint("api/v1/tax");

export const getStates = async (): Promise<State[]> => {
  const response = await fetch(`${BASE_URL}/states/`);
  return await response.json();
};

export const getTax = async (taxId: string): Promise<CreateUpdateTaxData> => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated || authStore.user!.role < 1)
    throw new Error("Unauthorized.");

  const response = await fetch(`${BASE_URL}/taxes/view/${taxId}/`, {
    headers: { Authorization: `Token ${authStore.token}` },
  });

  return await response.json();
};

export const payTax = async (taxId: number): Promise<Tax> => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated || authStore.user!.role > 1)
    throw new Error("Unauthorized.");

  const response = await fetch(`${BASE_URL}/pay/${taxId}/`, {
    method: "POST",
    headers: { Authorization: `Token ${authStore.token}` },
  });

  return await response.json();
};

export const editTax = async (
  taxId: number,
  updatedTaxData: CreateUpdateTaxData
): Promise<Tax> => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated || authStore.user!.role < 1)
    throw new Error("Unauthorized.");

  const response = await fetch(`${BASE_URL}/taxes/view/${taxId}/`, {
    method: "PUT",
    body: JSON.stringify(updatedTaxData),
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${authStore.token}`,
    },
  });

  return await response.json();
};

export const getTaxes = async (): Promise<Tax[]> => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) throw new Error("Unauthorized.");

  const response = await fetch(`${BASE_URL}/taxes/`, {
    headers: { Authorization: `Token ${authStore.token}` },
  });

  return await response.json();
};

export const createTax = async (tax: CreateUpdateTaxData) => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) throw new Error("Unauthorized.");

  await fetch(`${BASE_URL}/taxes/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${authStore.token}`,
    },
    body: JSON.stringify(tax),
  });
};
