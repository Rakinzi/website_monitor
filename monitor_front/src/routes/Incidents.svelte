<script lang="ts">
  import { onMount } from 'svelte';
  import { push } from 'svelte-spa-router';
  import { incidentsApi } from '../lib/services/api';

  let incidents = $state<any[]>([]);
  let isLoading = $state(true);
  let error = $state('');

  // Derived values for stats
  let openIncidents = $derived(incidents.filter(i => i.status === 'open' || i.status === 'investigating'));
  let acknowledgedIncidents = $derived(incidents.filter(i => i.status === 'acknowledged'));
  let resolvedIncidents = $derived(incidents.filter(i => i.status === 'resolved'));

  onMount(async () => {
    await loadIncidents();
  });

  async function loadIncidents() {
    isLoading = true;
    error = '';
    try {
      const response = await incidentsApi.getAll();
      // Ensure we always have an array
      incidents = Array.isArray(response) ? response : [];
    } catch (err: any) {
      error = err?.message || 'Failed to load incidents';
      incidents = []; // Reset to empty array on error
    } finally {
      isLoading = false;
    }
  }

  function formatDate(dateString: string) {
    const date = new Date(dateString);
    return date.toLocaleString();
  }

  function getStatusBadgeClass(status: string) {
    switch (status) {
      case 'open':
      case 'investigating':
        return 'bg-black dark:bg-white text-white dark:text-black';
      case 'acknowledged':
        return 'bg-gray-300 dark:bg-neutral-700 text-black dark:text-white';
      case 'resolved':
        return 'bg-black/10 dark:bg-white/10 text-black dark:text-white';
      default:
        return 'bg-gray-200 dark:bg-neutral-800 text-black dark:text-white';
    }
  }

  function getSeverityBadgeClass(severity: string) {
    switch (severity) {
      case 'critical':
        return 'bg-black dark:bg-white text-white dark:text-black';
      case 'warning':
        return 'bg-gray-300 dark:bg-neutral-700 text-black dark:text-white';
      case 'info':
        return 'bg-black/10 dark:bg-white/10 text-black dark:text-white';
      default:
        return 'bg-gray-200 dark:bg-neutral-800 text-black dark:text-white';
    }
  }
</script>

<div class="p-6 space-y-6">
  <!-- Header -->
  <div class="flex justify-between items-center">
    <h1 class="text-2xl font-bold text-black dark:text-white">Incidents</h1>
    <button class="btn btn-sm bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
      </svg>
      <span>Alert Settings</span>
    </button>
  </div>

  {#if isLoading}
    <div class="text-center py-12 text-gray-600 dark:text-gray-400">
      <div class="w-8 h-8 border-2 border-black dark:border-white border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
      Loading incidents...
    </div>
  {:else if error}
    <div class="p-4 border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950 rounded text-red-600 dark:text-red-400">
      {error}
    </div>
  {:else}
    <!-- Stats Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Incidents</p>
        <p class="text-2xl font-bold text-black dark:text-white">{incidents.length}</p>
      </div>
      <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Open</p>
        <p class="text-2xl font-bold text-black dark:text-white">{openIncidents.length}</p>
      </div>
      <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Acknowledged</p>
        <p class="text-2xl font-bold text-black dark:text-white">{acknowledgedIncidents.length}</p>
      </div>
      <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Resolved</p>
        <p class="text-2xl font-bold text-black dark:text-white">{resolvedIncidents.length}</p>
      </div>
    </div>

    <!-- Incidents List -->
    <div class="grid grid-cols-1 gap-4">
      {#if incidents.length === 0}
        <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-12 text-center">
          <div class="w-16 h-16 rounded-full bg-black/10 dark:bg-white/10 flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <p class="text-lg font-semibold text-black dark:text-white mb-2">No Incidents</p>
          <p class="text-gray-600 dark:text-gray-400">All systems are operating normally</p>
        </div>
      {:else}
        {#each incidents as incident}
          <div
            class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 overflow-hidden hover:shadow-lg transition-all cursor-pointer"
            role="button"
            tabindex="0"
            onclick={() => push(`/incidents/${incident.id}`)}
            onkeydown={(e) => e.key === 'Enter' && push(`/incidents/${incident.id}`)}
          >
            <!-- Header -->
            <div class="p-4 bg-gray-50 dark:bg-neutral-900 border-b border-gray-200 dark:border-neutral-800">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-lg font-bold text-black dark:text-white">{incident.title || 'Incident'}</h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400">{incident.description || 'No description available'}</p>
                </div>
                <span class="px-3 py-1 rounded {getSeverityBadgeClass(incident.severity)} text-xs font-medium uppercase">
                  {incident.severity}
                </span>
              </div>
            </div>

            <!-- Content -->
            <div class="p-4 space-y-4">
              <div class="flex items-center gap-2 text-sm">
                <span class="text-gray-600 dark:text-gray-400">Monitor:</span>
                <span class="font-semibold text-black dark:text-white">{incident.monitor_name || `Monitor #${incident.monitor_id}`}</span>
                <span class="text-gray-600 dark:text-gray-400">•</span>
                <span class="px-2 py-1 rounded {getStatusBadgeClass(incident.status)} text-xs font-medium capitalize">
                  {incident.status}
                </span>
              </div>

              <!-- Stats Grid -->
              <div class="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200 dark:border-neutral-800">
                <div class="text-center">
                  <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Started</p>
                  <p class="text-sm font-bold text-black dark:text-white">{formatDate(incident.created_at)}</p>
                </div>
                <div class="text-center">
                  <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Last Update</p>
                  <p class="text-sm font-bold text-black dark:text-white">{formatDate(incident.updated_at)}</p>
                </div>
                <div class="text-center">
                  <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Status</p>
                  <p class="text-sm font-bold text-black dark:text-white capitalize">{incident.status}</p>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex gap-2">
                <button class="btn btn-sm bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200 flex-1">
                  View Details
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                  </svg>
                </button>
                {#if incident.status === 'open' || incident.status === 'investigating'}
                  <button class="btn btn-sm bg-gray-200 dark:bg-neutral-800 hover:bg-gray-300 dark:hover:bg-neutral-700 text-black dark:text-white" onclick={(e) => { e.stopPropagation(); /* TODO: Acknowledge incident */ }}>
                    Acknowledge
                  </button>
                {/if}
                {#if incident.status === 'acknowledged'}
                  <button class="btn btn-sm bg-gray-200 dark:bg-neutral-800 hover:bg-gray-300 dark:hover:bg-neutral-700 text-black dark:text-white" onclick={(e) => { e.stopPropagation(); /* TODO: Resolve incident */ }}>
                    Resolve
                  </button>
                {/if}
              </div>
            </div>
          </div>
        {/each}
      {/if}
    </div>
  {/if}
</div>
