import configureEndpoint from "./host";

import useAuthStore from "@/stores/auth";
import type { Tax } from "@/api/types/tax";

const BASE_URL = configureEndpoint("api/v1/tax");

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

export const getTaxes = async (): Promise<Tax[]> => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) throw new Error("Unauthorized.");

  const response = await fetch(`${BASE_URL}/taxes/`, {
    headers: { Authorization: `Token ${authStore.token}` },
  });

  return await response.json();
};

export const createTax = async (tax: Tax): Promise<Tax> => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) throw new Error("Unauthorized.");

  const response = await fetch(`${BASE_URL}/taxes/`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      Authorization: `Token ${authStore.token}`,
    },
    body: JSON.stringify(tax),
  });

  return await response.json();
};
