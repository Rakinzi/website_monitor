<script lang="ts">
  import { AppBar, Avatar } from '@skeletonlabs/skeleton-svelte';
  import { authStore } from '../../stores/authStore';
  import { themeStore } from '../../stores/themeStore';
  import { push } from 'svelte-spa-router';
  import { location } from 'svelte-spa-router';
  import { onMount } from 'svelte';

  let { children } = $props<{ children?: import('svelte').Snippet }>();

  let user = $state<any>(null);
  let theme = $state<'light' | 'dark'>('dark');

  authStore.subscribe((state) => {
    user = state.user;
  });

  themeStore.subscribe((value) => {
    theme = value;
  });

  onMount(() => {
    themeStore.init();
  });

  function handleLogout() {
    authStore.logout();
    push('/login');
  }

  function toggleTheme() {
    themeStore.toggle();
  }

  function isActive(path: string) {
    return $location === path || $location.startsWith(path + '/');
  }

  const navItems = [
    {
      path: '/',
      label: 'Dashboard',
      icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>`
    },
    {
      path: '/monitors',
      label: 'Monitors',
      icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>`
    },
    {
      path: '/security',
      label: 'Security',
      icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>`
    },
    {
      path: '/incidents',
      label: 'Incidents',
      icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`
    },
    {
      path: '/settings',
      label: 'Settings',
      icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>`
    },
  ];
</script>

<div class="min-h-screen bg-surface-50-950">
  <!-- Modern App Bar -->
  <AppBar class="border-b border-surface-200-800 bg-surface-100-900/95 backdrop-blur-sm sticky top-0 z-50">
    <AppBar.Lead>
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center font-bold text-white shadow-lg">
          W
        </div>
        <div class="hidden md:block">
          <h1 class="text-xl font-bold">WebHealth</h1>
          <p class="text-xs text-surface-600-400">Monitor Dashboard</p>
        </div>
      </div>
    </AppBar.Lead>

    <AppBar.Trail>
      <div class="flex items-center gap-4">
        <!-- Navigation -->
        <nav class="hidden lg:flex gap-1">
          {#each navItems as item}
            <a
              href="#{item.path}"
              class="flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 {isActive(item.path)
                ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/20'
                : 'hover:bg-surface-200-800 text-surface-600-400 hover:text-surface-900-50'}"
            >
              {@html item.icon}
              <span class="text-sm font-medium">{item.label}</span>
            </a>
          {/each}
        </nav>

        <!-- Theme Toggle -->
        <button
          class="btn variant-ghost-surface btn-sm"
          onclick={toggleTheme}
          title="Toggle theme"
        >
          {#if theme === 'dark'}
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
          {:else}
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
          {/if}
        </button>

        <!-- User Menu -->
        {#if user}
          <div class="hidden md:flex items-center gap-3 pl-4 border-l border-surface-200-800">
            <div class="text-right">
              <p class="text-sm font-semibold">{user.email}</p>
              <p class="text-xs text-surface-600-400">{user.role}</p>
            </div>
            <Avatar class="w-10 h-10">
              <Avatar.Image src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop" alt={user.email} />
              <Avatar.Fallback>{user.email.charAt(0)}</Avatar.Fallback>
            </Avatar>
          </div>
          <button
            class="btn variant-ghost-surface btn-sm"
            onclick={handleLogout}
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            <span class="hidden md:inline">Logout</span>
          </button>
        {/if}
      </div>
    </AppBar.Trail>
  </AppBar>

  <!-- Mobile Navigation -->
  <nav class="lg:hidden bg-surface-100-900 border-b border-surface-200-800 px-4 py-2">
    <div class="flex gap-1 overflow-x-auto">
      {#each navItems as item}
        <a
          href="#{item.path}"
          class="flex items-center gap-2 px-3 py-2 rounded-lg whitespace-nowrap transition-all {isActive(item.path)
            ? 'bg-primary-500 text-white'
            : 'hover:bg-surface-200-800 text-surface-600-400'}"
        >
          {@html item.icon}
          <span class="text-sm">{item.label}</span>
        </a>
      {/each}
    </div>
  </nav>

  <!-- Main Content -->
  <main>
    {#if children}
      {@render children()}
    {/if}
  </main>
</div>
