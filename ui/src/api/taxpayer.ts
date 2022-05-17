import useAuthStore from "@/stores/auth";
import configureEndpoint from "@/api/host";
import type { TaxPayer, TaxpayerUsernameId } from "@/api/types/taxpayer";

const BASE_URL = configureEndpoint("api/v1/users");

export const getTaxpayerUsernames = async (): Promise<TaxpayerUsernameId[]> => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated || authStore.user!.role < 1)
    throw new Error("Unauthorized.");

  const response = await fetch(`${BASE_URL}/usernames/`, {
    headers: { Authorization: `Token ${authStore.token}` },
  });

  return await response.json();
};

export const editTaxPayer = async (username: string, updatedData: TaxPayer) => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated || authStore.user!.role < 1)
    throw new Error("Unauthorized.");

  const formData = new FormData();

  const response = await fetch(`${BASE_URL}/taxpayers/${username}/`, {
    method: "PUT",
    headers: { Authorization: `Token ${authStore.token}` },
  });
};

export const getTaxPayer = async (username: string): Promise<TaxPayer> => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated || authStore.user!.role < 1)
    throw new Error("Unauthorized.");

  const response = await fetch(`${BASE_URL}/taxpayers/${username}/`, {
    headers: { Authorization: `Token ${authStore.token}` },
  });

  return await response.json();
};

export const getTaxPayers = async (): Promise<TaxPayer[]> => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated || authStore.user!.role < 1)
    throw new Error("Unauthorized.");

  const response = await fetch(`${BASE_URL}/taxpayers/`, {
    headers: { Authorization: `Token ${authStore.token}` },
  });

  return await response.json();
};
