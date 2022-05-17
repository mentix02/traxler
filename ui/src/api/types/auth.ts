import type { Role } from "@/stores/auth";

export type UserData = {
  email: string;
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  [key: string]: string;
};

export type TokenResponse = {
  role: Role;
  token: string;
  username: string;
};
