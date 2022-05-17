import type { Role } from "@/stores/auth";

export type UserData = {
  email: string;
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  [key: string]: string;
};

export type UserEditData = {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  info: {
    pan: string;
    state: number;
    gstin: string;
    address: string;
    business_name: string;
  };
};

export type TokenResponse = {
  role: Role;
  token: string;
  username: string;
};
