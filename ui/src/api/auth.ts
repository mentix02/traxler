import configureEndpoint from "./host";

import type { UserData, TokenResponse } from "@/api/types/auth";

const BASE_URl = configureEndpoint("api/v1/users");

export const getTokenResponse = async (username: string, password: string) => {
  const formData = new FormData();

  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${BASE_URl}/token/`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Invalid username or password");
  }

  return await response.json();
};

export const createUser = async (
  userData: UserData
): Promise<TokenResponse> => {
  const formData = new FormData();

  Object.keys(userData).forEach((key) => {
    const value = userData[key];
    formData.set(key, value);
  });

  const response = await fetch(`${BASE_URl}/taxpayers/`, {
    method: "POST",
    body: formData,
  });

  if (response.status != 201) throw new Error("Something went wrong!");

  return await response.json();
};
