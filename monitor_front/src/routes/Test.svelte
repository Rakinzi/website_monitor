<script lang="ts">
  import { Avatar } from '@skeletonlabs/skeleton-svelte';
  import { themeStore } from '../stores/themeStore';

  let theme = $state<'light' | 'dark'>('dark');

  themeStore.subscribe((value) => {
    theme = value;
  });

  function toggleTheme() {
    console.log('Before toggle, current theme:', theme);
    console.log('HTML classes before:', document.documentElement.className);
    themeStore.toggle();
    setTimeout(() => {
      console.log('After toggle, new theme:', theme);
      console.log('HTML classes after:', document.documentElement.className);
    }, 100);
  }
</script>

<div class="p-6 space-y-6">
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-black dark:text-white">Theme Test Page</h1>
        <p class="text-gray-600 dark:text-gray-400">This page tests all components with light/dark mode</p>
      </div>
      <button
        onclick={toggleTheme}
        class="btn bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200 px-6 py-3"
      >
        {#if theme === 'dark'}
          <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
          Switch to Light
        {:else}
          <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
          </svg>
          Switch to Dark
        {/if}
      </button>
    </div>
  </div>

  <!-- Cards Section -->
  <div class="space-y-4">
    <h2 class="text-2xl font-semibold text-black dark:text-white">Cards</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-4">
        <h3 class="text-lg font-semibold mb-2 text-black dark:text-white">Card Title 1</h3>
        <p class="text-sm text-gray-600 dark:text-gray-400">This is a test card with standard styling.</p>
      </div>

      <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-4">
        <h3 class="text-lg font-semibold mb-2 text-black dark:text-white">Card Title 2</h3>
        <p class="text-sm text-gray-600 dark:text-gray-400">Another card to test consistency.</p>
      </div>

      <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-4">
        <h3 class="text-lg font-semibold mb-2 text-black dark:text-white">Card Title 3</h3>
        <p class="text-sm text-gray-600 dark:text-gray-400">Third card for testing.</p>
      </div>
    </div>
  </div>

  <!-- Buttons Section -->
  <div class="space-y-4">
    <h2 class="text-2xl font-semibold text-black dark:text-white">Buttons</h2>
    <div class="flex flex-wrap gap-3">
      <button class="btn bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200">
        Primary Button
      </button>

      <button class="btn bg-gray-200 dark:bg-neutral-800 text-black dark:text-white hover:bg-gray-300 dark:hover:bg-neutral-700">
        Secondary Button
      </button>

      <button class="btn border border-gray-300 dark:border-neutral-700 bg-transparent text-black dark:text-white hover:bg-gray-100 dark:hover:bg-neutral-900">
        Outline Button
      </button>

      <button class="btn bg-transparent text-black dark:text-white hover:bg-gray-100 dark:hover:bg-neutral-900">
        Ghost Button
      </button>
    </div>
  </div>

  <!-- Badges/Tags Section -->
  <div class="space-y-4">
    <h2 class="text-2xl font-semibold text-black dark:text-white">Badges</h2>
    <div class="flex flex-wrap gap-2">
      <span class="px-3 py-1 rounded-full bg-black dark:bg-white text-white dark:text-black text-sm font-medium">
        Primary Badge
      </span>

      <span class="px-3 py-1 rounded-full bg-gray-200 dark:bg-neutral-800 text-black dark:text-white text-sm font-medium">
        Secondary Badge
      </span>

      <span class="px-3 py-1 rounded-full border border-gray-300 dark:border-neutral-700 text-black dark:text-white text-sm font-medium">
        Outline Badge
      </span>

      <span class="px-3 py-1 rounded-full bg-gray-100 dark:bg-neutral-900 text-black dark:text-white text-sm">
        Light Badge
      </span>
    </div>
  </div>

  <!-- Avatar Section -->
  <div class="space-y-4">
    <h2 class="text-2xl font-semibold text-black dark:text-white">Avatars</h2>
    <div class="flex items-center gap-4">
      <Avatar class="w-12 h-12">
        <Avatar.Image src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop" alt="User" />
        <Avatar.Fallback>JD</Avatar.Fallback>
      </Avatar>

      <Avatar class="w-12 h-12">
        <Avatar.Fallback>AB</Avatar.Fallback>
      </Avatar>

      <Avatar class="w-12 h-12">
        <Avatar.Fallback>XY</Avatar.Fallback>
      </Avatar>
    </div>
  </div>

  <!-- List Section -->
  <div class="space-y-4">
    <h2 class="text-2xl font-semibold text-black dark:text-white">Lists</h2>
    <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-4">
      <ul class="space-y-2">
        <li class="p-3 rounded-lg bg-gray-50 dark:bg-neutral-900 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors">
          <div class="flex items-center justify-between">
            <span class="text-black dark:text-white font-medium">List Item 1</span>
            <span class="text-sm text-gray-500 dark:text-gray-400">Active</span>
          </div>
        </li>

        <li class="p-3 rounded-lg bg-gray-50 dark:bg-neutral-900 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors">
          <div class="flex items-center justify-between">
            <span class="text-black dark:text-white font-medium">List Item 2</span>
            <span class="text-sm text-gray-500 dark:text-gray-400">Pending</span>
          </div>
        </li>

        <li class="p-3 rounded-lg bg-gray-50 dark:bg-neutral-900 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors">
          <div class="flex items-center justify-between">
            <span class="text-black dark:text-white font-medium">List Item 3</span>
            <span class="text-sm text-gray-500 dark:text-gray-400">Completed</span>
          </div>
        </li>
      </ul>
    </div>
  </div>

  <!-- Form Elements Section -->
  <div class="space-y-4">
    <h2 class="text-2xl font-semibold text-black dark:text-white">Form Elements</h2>
    <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-6 max-w-md">
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-black dark:text-white mb-2" for="test-input">Input Field</label>
          <input
            id="test-input"
            type="text"
            placeholder="Enter text here"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-black dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-black dark:text-white mb-2" for="test-textarea">Textarea</label>
          <textarea
            id="test-textarea"
            placeholder="Enter description"
            rows="3"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-black dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white"
          ></textarea>
        </div>

        <div class="flex items-center gap-2">
          <input
            type="checkbox"
            id="test-checkbox"
            class="w-4 h-4 rounded border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900"
          />
          <label for="test-checkbox" class="text-sm text-black dark:text-white">
            Checkbox option
          </label>
        </div>
      </div>
    </div>
  </div>

  <!-- Table Section -->
  <div class="space-y-4">
    <h2 class="text-2xl font-semibold text-black dark:text-white">Table</h2>
    <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-neutral-900 border-b border-gray-200 dark:border-neutral-800">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-semibold text-black dark:text-white">Name</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-black dark:text-white">Status</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-black dark:text-white">Value</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-neutral-800">
          <tr class="hover:bg-gray-50 dark:hover:bg-neutral-900">
            <td class="px-4 py-3 text-sm text-black dark:text-white">Item 1</td>
            <td class="px-4 py-3 text-sm">
              <span class="px-2 py-1 rounded bg-black/10 dark:bg-white/10 text-black dark:text-white text-xs">Active</span>
            </td>
            <td class="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">100</td>
          </tr>
          <tr class="hover:bg-gray-50 dark:hover:bg-neutral-900">
            <td class="px-4 py-3 text-sm text-black dark:text-white">Item 2</td>
            <td class="px-4 py-3 text-sm">
              <span class="px-2 py-1 rounded bg-black/10 dark:bg-white/10 text-black dark:text-white text-xs">Active</span>
            </td>
            <td class="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">200</td>
          </tr>
          <tr class="hover:bg-gray-50 dark:hover:bg-neutral-900">
            <td class="px-4 py-3 text-sm text-black dark:text-white">Item 3</td>
            <td class="px-4 py-3 text-sm">
              <span class="px-2 py-1 rounded bg-gray-300 dark:bg-neutral-700 text-black dark:text-white text-xs">Inactive</span>
            </td>
            <td class="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">50</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Alert/Message Section -->
  <div class="space-y-4">
    <h2 class="text-2xl font-semibold text-black dark:text-white">Alerts</h2>
    <div class="space-y-3">
      <div class="p-4 rounded-lg bg-black/5 dark:bg-white/5 border border-gray-300 dark:border-neutral-700">
        <p class="text-sm text-black dark:text-white">
          <strong>Info:</strong> This is an informational message.
        </p>
      </div>

      <div class="p-4 rounded-lg bg-gray-100 dark:bg-neutral-900 border border-gray-300 dark:border-neutral-700">
        <p class="text-sm text-black dark:text-white">
          <strong>Warning:</strong> This is a warning message.
        </p>
      </div>

      <div class="p-4 rounded-lg bg-black dark:bg-white border border-black dark:border-white">
        <p class="text-sm text-white dark:text-black">
          <strong>Critical:</strong> This is a critical message.
        </p>
      </div>
    </div>
  </div>
</div>
