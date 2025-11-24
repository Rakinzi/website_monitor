<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { authStore } from '../stores/authStore';
  import { authApi } from '../lib/services/api';

  let email = '';
  let password = '';
  let confirmPassword = '';
  let role: 'admin' | 'maintainer' | 'viewer' = 'viewer';
  let isLoading = false;
  let error = '';

  async function handleRegister() {
    error = '';
    if (password !== confirmPassword) {
      error = 'Passwords do not match';
      return;
    }
    isLoading = true;
    try {
      await authApi.register(email, password, role);
      const loginResponse = await authApi.login(email, password);
      authStore.login(loginResponse.user, loginResponse.access_token, loginResponse.refresh_token);
      push('/');
    } catch (err: any) {
      error = err?.message || 'Registration failed';
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="min-h-screen flex flex-col lg:flex-row bg-white dark:bg-black">
  <!-- Left Side - Image -->
  <div class="hidden lg:flex lg:w-1/2 relative bg-black dark:bg-white">
    <div class="absolute inset-0 flex flex-col justify-center items-start p-16 text-white dark:text-black">
      <div class="max-w-md">
        <div class="w-16 h-16 rounded-2xl bg-white/10 backdrop-blur-sm flex items-center justify-center mb-6 shadow-2xl border border-white/20">
          <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <h1 class="text-5xl font-bold mb-4">WebHealth</h1>
        <p class="text-xl mb-6 opacity-90">Monitor your services with confidence</p>
        <div class="space-y-4">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-white/10 dark:bg-black/10 backdrop-blur-sm flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <p class="opacity-80">Real-time uptime monitoring</p>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-white/10 dark:bg-black/10 backdrop-blur-sm flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
              </svg>
            </div>
            <p class="opacity-80">Instant incident notifications</p>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-white/10 dark:bg-black/10 backdrop-blur-sm flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <p class="opacity-80">Comprehensive analytics</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Right Side - Register Form -->
  <div class="flex-1 flex items-center justify-center p-8">
    <div class="w-full max-w-md">
      <!-- Logo for mobile -->
      <div class="lg:hidden flex items-center gap-3 mb-8">
        <div class="w-12 h-12 rounded-xl bg-black dark:bg-white flex items-center justify-center font-bold text-white dark:text-black shadow-lg">
          W
        </div>
        <div>
          <h1 class="text-2xl font-bold text-black dark:text-white">WebHealth</h1>
          <p class="text-xs text-gray-600 dark:text-gray-400">Monitor Dashboard</p>
        </div>
      </div>

      <!-- Register Card -->
      <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-8 shadow-2xl">
        <div class="mb-8">
          <h2 class="text-3xl font-bold text-black dark:text-white mb-2">
            Create Account
          </h2>
          <p class="text-gray-600 dark:text-gray-400">Sign up to start monitoring your services</p>
        </div>

        <form onsubmit={(e) => { e.preventDefault(); handleRegister(); }} class="space-y-5">
          {#if error}
            <div class="flex items-center gap-3 bg-red-50 dark:bg-red-950 text-red-600 dark:text-red-400 p-4 rounded-lg border border-red-200 dark:border-red-800">
              <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span>{error}</span>
            </div>
          {/if}

          <div>
            <label class="label mb-2" for="email">
              <span class="font-semibold text-black dark:text-white">Email Address</span>
            </label>
            <div class="relative">
              <div class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-600 dark:text-gray-400">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
              </div>
              <input
                id="email"
                type="email"
                class="w-full px-4 py-3 pl-11 rounded-lg border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-black dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white"
                placeholder="you@example.com"
                bind:value={email}
                required
              />
            </div>
          </div>

          <div>
            <label class="label mb-2" for="password">
              <span class="font-semibold text-black dark:text-white">Password</span>
            </label>
            <div class="relative">
              <div class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-600 dark:text-gray-400">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
              </div>
              <input
                id="password"
                type="password"
                class="w-full px-4 py-3 pl-11 rounded-lg border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-black dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white"
                placeholder="••••••••"
                bind:value={password}
                required
                minlength={8}
              />
            </div>
          </div>

          <div>
            <label class="label mb-2" for="confirmPassword">
              <span class="font-semibold text-black dark:text-white">Confirm Password</span>
            </label>
            <div class="relative">
              <div class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-600 dark:text-gray-400">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
              </div>
              <input
                id="confirmPassword"
                type="password"
                class="w-full px-4 py-3 pl-11 rounded-lg border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-black dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white"
                placeholder="••••••••"
                bind:value={confirmPassword}
                required
                minlength={8}
              />
            </div>
          </div>

          <div>
            <label class="label mb-2" for="role">
              <span class="font-semibold text-black dark:text-white">Role</span>
            </label>
            <div class="relative">
              <div class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-600 dark:text-gray-400">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
              </div>
              <select
                id="role"
                class="w-full px-4 py-3 pl-11 rounded-lg border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-black dark:text-white focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white appearance-none"
                bind:value={role}
              >
                <option value="viewer">Viewer</option>
                <option value="maintainer">Maintainer</option>
                <option value="admin">Admin</option>
              </select>
              <div class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-600 dark:text-gray-400 pointer-events-none">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </div>
            </div>
          </div>

          <button
            type="submit"
            class="btn bg-black dark:bg-white text-white dark:text-black w-full hover:bg-gray-800 dark:hover:bg-gray-200 hover:scale-[1.02] active:scale-[0.98] transition-all text-lg py-3"
            disabled={isLoading}
          >
            {#if isLoading}
              <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span class="ml-2">Creating Account...</span>
            {:else}
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
              </svg>
              <span>Create Account</span>
            {/if}
          </button>
        </form>

        <div class="mt-6 pt-6 border-t border-gray-200 dark:border-neutral-800 text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Already have an account?
            <button
              type="button"
              class="text-black dark:text-white hover:underline font-semibold ml-1"
              onclick={() => push('/login')}
            >
              Sign In
            </button>
          </p>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-8 text-center text-xs text-gray-600 dark:text-gray-400">
        <p>© 2025 WebHealth. All rights reserved.</p>
        <div class="flex items-center justify-center gap-4 mt-2">
          <button type="button" class="hover:text-black dark:hover:text-white transition-colors">Privacy Policy</button>
          <span>•</span>
          <button type="button" class="hover:text-black dark:hover:text-white transition-colors">Terms of Service</button>
          <span>•</span>
          <button type="button" class="hover:text-black dark:hover:text-white transition-colors">Support</button>
        </div>
      </div>
    </div>
  </div>
</div>
