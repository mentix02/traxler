import useAuthStore from "@/stores/auth";
import configureEndpoint from "@/api/host";

import type { UserEditData } from "@/api/types/auth";
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

export const editTaxPayer = async (
  username: string,
  updatedData: UserEditData
) => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated || authStore.user!.role < 1)
    throw new Error("Unauthorized.");

  await fetch(`${BASE_URL}/taxpayers/${username}/`, {
    method: "PUT",
    body: JSON.stringify(updatedData),
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${authStore.token}`,
    },
  });
};

export const getTaxPayerData = async (
  username: string
): Promise<UserEditData> => {
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
