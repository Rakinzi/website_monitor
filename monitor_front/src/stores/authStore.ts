import { writable } from 'svelte/store';
import { authApi } from '../lib/services/api';
import { ACCESS_COOKIE, REFRESH_COOKIE } from '../lib/constants/auth';
import { deleteCookie, getCookie, setCookie } from '../lib/utils/cookies';

export interface User {
  id: number;
  email: string;
  role: 'admin' | 'maintainer' | 'viewer';
}

export interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const initialAccess = getCookie(ACCESS_COOKIE);
const initialRefresh = getCookie(REFRESH_COOKIE);

const initialState: AuthState = {
  user: null,
  accessToken: initialAccess,
  refreshToken: initialRefresh,
  isAuthenticated: !!initialAccess,
  isLoading: false,
};

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>(initialState);

  return {
    subscribe,
    initialize: async () => {
      if (!initialAccess || !initialRefresh) {
        return;
      }
      update((state) => ({ ...state, isLoading: true }));
      try {
        const user = await authApi.me();
        set({
          user,
          accessToken: initialAccess,
          refreshToken: initialRefresh,
          isAuthenticated: true,
          isLoading: false,
        });
      } catch {
        deleteCookie(ACCESS_COOKIE);
        deleteCookie(REFRESH_COOKIE);
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          isAuthenticated: false,
          isLoading: false,
        });
      }
    },
    login: (user: User, accessToken: string, refreshToken: string) => {
      setCookie(ACCESS_COOKIE, accessToken);
      setCookie(REFRESH_COOKIE, refreshToken);
      set({
        user,
        accessToken,
        refreshToken,
        isAuthenticated: true,
        isLoading: false,
      });
    },
    logout: () => {
      deleteCookie(ACCESS_COOKIE);
      deleteCookie(REFRESH_COOKIE);
      set({
        user: null,
        accessToken: null,
        refreshToken: null,
        isAuthenticated: false,
        isLoading: false,
      });
    },
    setLoading: (isLoading: boolean) => {
      update((state) => ({ ...state, isLoading }));
    },
    updateUser: (user: User) => {
      update((state) => ({ ...state, user }));
    },
  };
}

export const authStore = createAuthStore();
