<script lang="ts">
  import { onMount } from 'svelte';
  import { monitorsApi, incidentsApi, checksApi, analyticsApi } from '../lib/services/api';
  import { push } from 'svelte-spa-router';

  let isLoading = $state(true);
  let error = $state('');

  let monitors = $state<any[]>([]);
  let incidents = $state<any[]>([]);
  type RecentCheck = {
    id: number;
    monitor_id: number;
    check_type: string;
    status: 'passed' | 'failed' | 'degraded';
    region?: string | null;
    response_ms?: number | null;
    details?: Record<string, any> | null;
    created_at: string;
  };
  let recentChecks = $state<RecentCheck[]>([]);
  let uptimeStats = $state({
    overall: 0,
    today: 0,
    week: 0,
    month: 0,
  });

  const activeMonitorsCount = $derived(Array.isArray(monitors) ? monitors.filter(m => m.status === 'healthy').length : 0);
  const activeIncidentsCount = $derived(Array.isArray(incidents) ? incidents.filter(i => i.status === 'open' || i.status === 'investigating').length : 0);

  onMount(async () => {
    await loadDashboardData();
  });

  async function loadDashboardData() {
    isLoading = true;
    error = '';
    try {
      // Load all data in parallel
      const [monitorsData, incidentsData, checksData, uptimeData] = await Promise.all([
        monitorsApi.getAll().catch(() => []),
        incidentsApi.getAll().catch(() => []),
        checksApi.getRecent(5).catch(() => []),
        analyticsApi.getUptime().catch(() => ({ overall: 0, today: 0, week: 0, month: 0 })),
      ]);

      monitors = Array.isArray(monitorsData) ? monitorsData : [];
      incidents = Array.isArray(incidentsData) ? incidentsData : [];
      recentChecks = Array.isArray(checksData) ? checksData : [];
      uptimeStats = uptimeData || { overall: 0, today: 0, week: 0, month: 0 };
    } catch (err: any) {
      error = err?.message || 'Failed to load dashboard data';
      monitors = [];
      incidents = [];
      recentChecks = [];
    } finally {
      isLoading = false;
    }
  }

  let timezone = $state('local');
  const timezones = ['local', 'UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo'];

  function formatTimestamp(timestamp: string) {
    const date = new Date(timestamp);
    const tz = timezone === 'local' ? undefined : timezone;
    return date.toLocaleString(undefined, { timeZone: tz });
  }

  function getStatusColor(status: string) {
    switch (status) {
      case 'healthy':
      case 'pass':
      case 'success':
        return 'bg-black dark:bg-white text-white dark:text-black';
      case 'warning':
      case 'degraded':
        return 'bg-gray-300 dark:bg-neutral-700 text-black dark:text-white';
      case 'critical':
      case 'down':
      case 'error':
        return 'bg-black dark:bg-white text-white dark:text-black';
      default:
        return 'bg-gray-200 dark:bg-neutral-800 text-black dark:text-white';
    }
  }

  function getSeverityLabel(severity: string) {
    switch (severity) {
      case 'critical': return 'Critical';
      case 'warning': return 'Warning';
      case 'info': return 'Info';
      default: return severity;
    }
  }
</script>

<div class="p-6 space-y-6">
  {#if isLoading}
    <div class="text-center py-12 text-gray-600 dark:text-gray-400">
      <div class="w-8 h-8 border-2 border-black dark:border-white border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
      Loading dashboard...
    </div>
  {:else if error}
    <div class="p-4 border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950 rounded text-red-600 dark:text-red-400">
      {error}
    </div>
  {:else}
    <!-- Header -->
    <div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-black dark:text-white">Dashboard</h1>
        <p class="text-sm text-gray-600 dark:text-gray-400">Monitor timeline uses your selected timezone</p>
      </div>
      <div class="flex items-center gap-3">
        <label for="timezone" class="text-sm text-gray-600 dark:text-gray-400">Timezone</label>
        <select id="timezone" class="input" bind:value={timezone}>
          {#each timezones as tz}
            <option value={tz}>{tz === 'local' ? 'Local Browser Time' : tz}</option>
          {/each}
        </select>
        <button class="btn btn-sm bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200" onclick={() => push('/monitors')}>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          <span>Add Monitor</span>
        </button>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Overall Uptime -->
      <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
        <div class="flex items-center gap-3 mb-3">
          <div class="p-2 bg-black/10 dark:bg-white/10 rounded-lg">
            <svg class="w-5 h-5 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
            </svg>
          </div>
          <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Overall Uptime</p>
        </div>
        <p class="text-3xl font-bold text-black dark:text-white">{(uptimeStats.overall || 0).toFixed(1)}%</p>
      </div>

      <!-- Active Monitors -->
      <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
        <div class="flex items-center gap-3 mb-3">
          <div class="p-2 bg-black/10 dark:bg-white/10 rounded-lg">
            <svg class="w-5 h-5 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
          </div>
          <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Active Monitors</p>
        </div>
        <p class="text-3xl font-bold text-black dark:text-white">{activeMonitorsCount}<span class="text-lg text-gray-500 dark:text-gray-400">/{monitors.length}</span></p>
      </div>

      <!-- Active Incidents -->
      <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
        <div class="flex items-center gap-3 mb-3">
          <div class="p-2 bg-black/10 dark:bg-white/10 rounded-lg">
            <svg class="w-5 h-5 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Active Incidents</p>
        </div>
        <p class="text-3xl font-bold text-black dark:text-white">
          {activeIncidentsCount}
        </p>
      </div>

      <!-- Today's Uptime -->
      <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
        <div class="flex items-center gap-3 mb-3">
          <div class="p-2 bg-black/10 dark:bg-white/10 rounded-lg">
            <svg class="w-5 h-5 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Today's Uptime</p>
        </div>
        <p class="text-3xl font-bold text-black dark:text-white">{(uptimeStats.today || 0).toFixed(1)}%</p>
      </div>
    </div>

    <!-- Activity Sections -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Recent Checks -->
      <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800">
        <div class="p-4 border-b border-gray-200 dark:border-neutral-800 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-black dark:text-white">Recent Checks</h2>
          <a href="#/monitors" class="text-sm text-black dark:text-white hover:underline">View All</a>
        </div>
        <div class="p-4 space-y-2">
          {#if recentChecks.length === 0}
            <div class="flex flex-col items-center justify-center py-8">
              <div class="w-12 h-12 rounded-full bg-black/10 dark:bg-white/10 flex items-center justify-center mb-2">
                <svg class="w-6 h-6 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
              </div>
              <p class="text-sm font-medium text-black dark:text-white">No recent checks</p>
              <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">Add monitors to see check results</p>
            </div>
          {:else}
            {#each recentChecks as check}
              <div
                class="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-neutral-900 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors cursor-pointer"
                role="button"
                tabindex="0"
                onclick={() => check.monitor_id && push(`/monitors/${check.monitor_id}`)}
                onkeydown={(event) => event.key === 'Enter' && check.monitor_id && push(`/monitors/${check.monitor_id}`)}
              >
                <div class="w-8 h-8 rounded-lg bg-black/10 dark:bg-white/10 flex items-center justify-center">
                  {#if check.status === 'passed'}
                    <svg class="w-4 h-4 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                  {:else}
                    <svg class="w-4 h-4 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  {/if}
                </div>
                <div class="flex-1 min-w-0">
                  <p class="font-medium text-sm truncate text-black dark:text-white">{check.details?.monitor_name || `Monitor #${check.monitor_id}`}</p>
                  <p class="text-xs text-gray-600 dark:text-gray-400">{check.check_type} · {check.region || 'global'}</p>
                  <p class="text-xs text-gray-600 dark:text-gray-400">{formatTimestamp(check.created_at)}</p>
                </div>
                <div class="text-right">
                  <span class={`text-xs px-2 py-1 ${getStatusColor(check.status === 'passed' ? 'success' : check.status === 'degraded' ? 'warning' : 'error')} rounded`}>{check.status}</span>
                  {#if check.response_ms}
                    <p class="text-xs text-gray-500 dark:text-gray-400">{check.response_ms}ms</p>
                  {/if}
                </div>
              </div>
            {/each}
          {/if}
        </div>
      </div>

      <!-- Active Incidents -->
      <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800">
        <div class="p-4 border-b border-gray-200 dark:border-neutral-800 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-black dark:text-white">Active Incidents</h2>
          <a href="#/incidents" class="text-sm text-black dark:text-white hover:underline">View All</a>
        </div>
        <div class="p-4 space-y-2">
          {#if activeIncidentsCount === 0}
            <div class="flex flex-col items-center justify-center py-8">
              <div class="w-12 h-12 rounded-full bg-black/10 dark:bg-white/10 flex items-center justify-center mb-2">
                <svg class="w-6 h-6 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <p class="text-sm font-medium text-black dark:text-white">All Systems Operational</p>
            </div>
          {:else}
            {#each incidents.filter(i => i.status === 'open' || i.status === 'investigating').slice(0, 3) as incident}
              <div
                class="p-3 rounded-lg bg-gray-100 dark:bg-neutral-900 border border-gray-300 dark:border-neutral-700 cursor-pointer hover:bg-gray-200 dark:hover:bg-neutral-800 transition-colors"
                role="button"
                tabindex="0"
                onclick={() => push(`/incidents/${incident.id}`)}
                onkeydown={(event) => event.key === 'Enter' && push(`/incidents/${incident.id}`)}
              >
                <div class="flex items-start gap-3">
                  <div class="w-8 h-8 rounded-lg bg-black/10 dark:bg-white/10 flex items-center justify-center">
                    <svg class="w-4 h-4 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-1">
                      <p class="font-semibold text-sm text-black dark:text-white">{incident.title || 'Incident'}</p>
                      <span class="text-xs px-2 py-1 {getStatusColor(incident.severity)} rounded">{getSeverityLabel(incident.severity)}</span>
                    </div>
                    <p class="text-xs text-gray-600 dark:text-gray-400">{formatTimestamp(incident.created_at)}</p>
                  </div>
                </div>
              </div>
            {/each}
          {/if}
        </div>
      </div>
    </div>
  {/if}
</div>
