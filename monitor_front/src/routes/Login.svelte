<script lang="ts">
  import { authStore } from '../stores/authStore';
  import { push } from 'svelte-spa-router';
  import { authApi } from '../lib/services/api';

  let email = '';
  let password = '';
  let isLoading = false;
  let error = '';
  let rememberMe = false;

  async function handleLogin() {
    error = '';
    isLoading = true;

    try {
      const response = await authApi.login(email, password);
      authStore.login(response.user, response.access_token, response.refresh_token);
      push('/');
    } catch (err: any) {
      error = err?.message || 'Login failed';
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="min-h-screen flex flex-col lg:flex-row">


  <!-- Left Side - Image -->
  <div class="hidden lg:flex lg:w-1/2 relative">
    <div class="absolute inset-0 bg-gradient-to-br from-primary-900/90 via-secondary-900/80 to-tertiary-900/90"></div>
    <div class="absolute inset-0 flex flex-col justify-center items-start p-16 text-white">
      <div class="max-w-md">
        <div class="w-16 h-16 rounded-2xl bg-white/10 backdrop-blur-sm flex items-center justify-center mb-6 shadow-2xl border border-white/20">
          <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <h1 class="text-5xl font-bold mb-4">WebHealth</h1>
        <p class="text-xl text-white/90 mb-6">Monitor your services with confidence</p>
        <div class="space-y-4">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-white/10 backdrop-blur-sm flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <p class="text-white/80">Real-time uptime monitoring</p>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-white/10 backdrop-blur-sm flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
              </svg>
            </div>
            <p class="text-white/80">Instant incident notifications</p>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-white/10 backdrop-blur-sm flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <p class="text-white/80">Comprehensive analytics</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Right Side - Login Form -->
  <div class="flex-1 flex items-center justify-center p-8 bg-gradient-to-br from-surface-50 to-surface-100 dark:from-surface-950 dark:to-surface-900">
    <div class="w-full max-w-md">
      <!-- Logo for mobile -->
      <div class="lg:hidden flex items-center gap-3 mb-8">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center font-bold text-white shadow-lg">
          W
        </div>
        <div>
          <h1 class="text-2xl font-bold">WebHealth</h1>
          <p class="text-xs text-surface-600-400">Monitor Dashboard</p>
        </div>
      </div>

      <!-- Login Card -->
      <div class="card preset-filled-surface-50-950 border border-surface-200-800 p-8 shadow-2xl">
        <div class="mb-8">
          <h2 class="text-3xl font-bold bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent mb-2">
            Welcome Back
          </h2>
          <p class="text-surface-600-400">Sign in to access your dashboard</p>
        </div>

        <form onsubmit={(e) => { e.preventDefault(); handleLogin(); }} class="space-y-5">
          {#if error}
            <div class="flex items-center gap-3 bg-error-500/10 text-error-500 p-4 rounded-lg border border-error-500/20">
              <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span>{error}</span>
            </div>
          {/if}

          <div>
            <label class="label mb-2" for="email">
              <span class="font-semibold text-surface-900-50">Email Address</span>
            </label>
            <div class="relative">
              <div class="absolute left-3 top-1/2 -translate-y-1/2 text-surface-600-400">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
              </div>
              <input
                id="email"
                type="email"
                class="input variant-form-material pl-11"
                placeholder="admin@example.com"
                bind:value={email}
                required
              />
            </div>
          </div>

          <div>
            <label class="label mb-2" for="password">
              <span class="font-semibold text-surface-900-50">Password</span>
            </label>
            <div class="relative">
              <div class="absolute left-3 top-1/2 -translate-y-1/2 text-surface-600-400">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
              </div>
              <input
                id="password"
                type="password"
                class="input variant-form-material pl-11"
                placeholder="••••••••"
                bind:value={password}
                required
              />
            </div>
          </div>

          <div class="flex items-center justify-between">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" class="checkbox" bind:checked={rememberMe} />
              <span class="text-sm text-surface-600-400">Remember me</span>
            </label>
            <button type="button" class="text-sm text-primary-500 hover:text-primary-600 font-medium">
              Forgot password?
            </button>
          </div>

          <button
            type="submit"
            class="btn bg-gradient-to-br from-primary-500 to-secondary-500 text-white w-full shadow-lg shadow-primary-500/30 hover:shadow-primary-500/50 hover:scale-[1.02] active:scale-[0.98] transition-all text-lg py-3"
            disabled={isLoading}
          >
            {#if isLoading}
              <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span class="ml-2">Signing in...</span>
            {:else}
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
              </svg>
              <span>Sign In</span>
            {/if}
          </button>
        </form>

        <div class="mt-6 pt-6 border-t border-surface-200-800 text-center">
          <p class="text-sm text-surface-600-400">
            Don't have an account?
            <button type="button" class="text-primary-500 hover:text-primary-600 font-semibold ml-1">
              Contact Sales
            </button>
          </p>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-8 text-center text-xs text-surface-600-400">
        <p>© 2025 WebHealth. All rights reserved.</p>
        <div class="flex items-center justify-center gap-4 mt-2">
          <button type="button" class="hover:text-primary-500 transition-colors">Privacy Policy</button>
          <span>•</span>
          <button type="button" class="hover:text-primary-500 transition-colors">Terms of Service</button>
          <span>•</span>
          <button type="button" class="hover:text-primary-500 transition-colors">Support</button>
        </div>
      </div>
    </div>
  </div>
</div>
