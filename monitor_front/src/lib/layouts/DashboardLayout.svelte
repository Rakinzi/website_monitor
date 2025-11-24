<script lang="ts">
  import { Avatar } from '@skeletonlabs/skeleton-svelte';
  import { authStore } from '../../stores/authStore';
  import { themeStore } from '../../stores/themeStore';
  import { push } from 'svelte-spa-router';
  import { location } from 'svelte-spa-router';
  import { onMount } from 'svelte';

  let { children } = $props<{ children?: import('svelte').Snippet }>();

  let user = $state<any>(null);
  let theme = $state<'light' | 'dark'>('dark');
  let sidebarCollapsed = $state(false);

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
    return $location === path || ($location.startsWith(path + '/') && path !== '/');
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

<div class="flex h-screen bg-white dark:bg-black overflow-hidden">
  <!-- Sidebar -->
  <aside class="hidden md:flex flex-col bg-gray-50 dark:bg-neutral-950 border-r border-gray-200 dark:border-neutral-800 {sidebarCollapsed ? 'w-20' : 'w-64'} transition-all duration-300">
    <!-- Logo -->
    <div class="p-6 border-b border-gray-200 dark:border-neutral-800">
      <div class="flex items-center {sidebarCollapsed ? 'justify-center' : 'gap-3'}">
        <div class="w-10 h-10 rounded-lg bg-black dark:bg-white flex items-center justify-center font-bold text-white dark:text-black shrink-0">
          W
        </div>
        {#if !sidebarCollapsed}
          <div>
            <h1 class="text-lg font-bold text-black dark:text-white">WebHealth</h1>
          </div>
        {/if}
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 p-4 space-y-2">
      {#each navItems as item}
        <a
          href="#{item.path}"
          class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 {isActive(item.path)
            ? 'bg-black dark:bg-white text-white dark:text-black shadow-lg'
            : 'hover:bg-gray-200 dark:hover:bg-neutral-800 text-gray-600 dark:text-gray-400 hover:text-black dark:hover:text-white'} {sidebarCollapsed ? 'justify-center' : ''}"
          title={sidebarCollapsed ? item.label : ''}
        >
          {@html item.icon}
          {#if !sidebarCollapsed}
            <span class="text-sm font-medium">{item.label}</span>
          {/if}
        </a>
      {/each}
    </nav>

    <!-- User Section -->
    {#if user}
      <div class="p-4 border-t border-gray-200 dark:border-neutral-800">
        {#if !sidebarCollapsed}
          <div class="flex items-center gap-3 mb-3">
            <Avatar class="w-10 h-10 shrink-0">
              <Avatar.Image src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop" alt={user.email} />
              <Avatar.Fallback>{user.email.charAt(0).toUpperCase()}</Avatar.Fallback>
            </Avatar>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold truncate text-black dark:text-white">{user.email}</p>
              <p class="text-xs text-gray-600 dark:text-gray-400">{user.role}</p>
            </div>
          </div>
        {:else}
          <div class="flex justify-center mb-3">
            <Avatar class="w-10 h-10">
              <Avatar.Image src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop" alt={user.email} />
              <Avatar.Fallback>{user.email.charAt(0).toUpperCase()}</Avatar.Fallback>
            </Avatar>
          </div>
        {/if}

        <div class="flex gap-2 {sidebarCollapsed ? 'flex-col' : ''}">
          <button
            class="btn btn-sm flex-1 bg-gray-200 dark:bg-neutral-800 hover:bg-gray-300 dark:hover:bg-neutral-700 text-black dark:text-white {sidebarCollapsed ? 'px-2' : ''}"
            onclick={toggleTheme}
            title="Toggle theme"
          >
            {#if theme === 'dark'}
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
              </svg>
            {:else}
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
              </svg>
            {/if}
          </button>
          <button
            class="btn btn-sm flex-1 bg-gray-200 dark:bg-neutral-800 hover:bg-gray-300 dark:hover:bg-neutral-700 text-black dark:text-white {sidebarCollapsed ? 'px-2' : ''}"
            onclick={handleLogout}
            title="Logout"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    {/if}
  </aside>

  <!-- Mobile Bottom Nav -->
  <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-gray-50 dark:bg-neutral-950 border-t border-gray-200 dark:border-neutral-800 z-50">
    <div class="flex justify-around p-2">
      {#each navItems as item}
        <a
          href="#{item.path}"
          class="flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-all {isActive(item.path)
            ? 'text-black dark:text-white'
            : 'text-gray-600 dark:text-gray-400'}"
        >
          {@html item.icon}
          <span class="text-xs">{item.label}</span>
        </a>
      {/each}
    </div>
  </nav>

  <!-- Main Content -->
  <main class="flex-1 overflow-auto pb-20 md:pb-0 bg-white dark:bg-black">
    {#if children}
      {@render children()}
    {/if}
  </main>
</div>
