import { acceptHMRUpdate, defineStore } from "pinia";
import type { TokenResponse } from "@/api/types/auth";

const ROLE_TAXPAYER = 0;
const ROLE_ADMIN = 2;
const ROLE_TAXACCOUNTANT = 1;

export type Role =
  | typeof ROLE_TAXPAYER
  | typeof ROLE_ADMIN
  | typeof ROLE_TAXACCOUNTANT;

export type User = {
  role: Role;
  username: string;
};

export type AuthState = {
  user?: User;
  token?: string;
};

const useAuthStore = defineStore("auth", {
  state: () =>
    ({
      user: undefined,
      token: undefined,
    } as AuthState),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    logIn(tokenResponse: TokenResponse) {
      const { token, username, role } = tokenResponse;
      this.$state = { token, user: { username, role } };
    },
    logOut() {
      this.$reset();
    },
  },
  persist: {
    enabled: true,
    strategies: [{ storage: localStorage }],
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}

export default useAuthStore;
