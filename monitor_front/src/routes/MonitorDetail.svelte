<script lang="ts">
  import { onMount } from 'svelte';
  import { pop } from 'svelte-spa-router';
  import { monitorsApi, securityApi, type SecurityAuditResponse } from '../lib/services/api';

let { params } = $props<{ params: { id: string } }>();

  type MonitorStatus = 'healthy' | 'degraded' | 'down' | 'unknown';
  type SecurityStatus = 'pass' | 'warning' | 'critical';

  interface MonitorDetail {
    id: number;
    name: string;
    target: string;
    monitor_type: string;
    status: MonitorStatus;
    interval_seconds: number;
    timeout_seconds: number;
    failure_threshold: number;
    success_threshold: number;
    created_at: string;
    updated_at: string;
    security_status: SecurityStatus;
    last_security_check_at?: string | null;
  }

  let isLoading = $state(true);
  let error = $state('');
  let monitor = $state<MonitorDetail | null>(null);
  let audits = $state<SecurityAuditResponse[]>([]);
  let auditError = $state('');
  let auditLoading = $state(false);
  let hasMoreAudits = $state(true);
  let auditOffset = $state(0);
  const PAGE_SIZE = 5;

  onMount(() => {
    loadMonitor();
  });

  async function loadMonitor() {
    isLoading = true;
    error = '';
    try {
      monitor = await monitorsApi.getById(params.id);
      auditOffset = 0;
      audits = [];
      hasMoreAudits = true;
      await loadMoreAudits();
    } catch (err: any) {
      error = err?.message || 'Failed to load monitor';
    } finally {
      isLoading = false;
    }
  }

  async function loadMoreAudits() {
    if (!monitor || !hasMoreAudits) return;
    auditLoading = true;
    auditError = '';
    try {
      const results = await securityApi.listMonitorSecurityAudits(monitor.id, {
        limit: PAGE_SIZE,
        offset: auditOffset,
      });
      audits = [...audits, ...results];
      auditOffset += results.length;
      hasMoreAudits = results.length === PAGE_SIZE;
    } catch (err: any) {
      auditError = err?.message || 'Unable to load security audits';
      hasMoreAudits = false;
    } finally {
      auditLoading = false;
    }
  }

  async function runSecurityCheck() {
    if (!monitor) return;
    auditLoading = true;
    auditError = '';
    try {
      const latest = await securityApi.runMonitorSecurityCheck(monitor.id);
      audits = [latest, ...audits];
      monitor = { ...monitor, security_status: latest.status, last_security_check_at: latest.created_at };
    } catch (err: any) {
      auditError = err?.message || 'Failed to run security check';
    } finally {
      auditLoading = false;
    }
  }

  function formatDate(value?: string | null) {
    if (!value) return 'N/A';
    return new Date(value).toLocaleString();
  }

  const latestAudit = $derived(audits[0] || null);
  const latestFindings = $derived(latestAudit?.findings || {});
</script>

<div class="p-6 space-y-6">
  {#if isLoading}
    <div class="text-center text-gray-600 dark:text-gray-400">Loading monitor...</div>
  {:else if error}
    <div class="p-4 border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950 rounded text-red-600 dark:text-red-400">{error}</div>
  {:else if monitor}
    <div class="flex justify-between items-center">
      <div class="flex items-center gap-4">
        <button class="btn btn-sm bg-gray-200 dark:bg-neutral-800 hover:bg-gray-300 dark:hover:bg-neutral-700 text-black dark:text-white" onclick={() => pop()}>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
          Back
        </button>
        <div>
          <h1 class="text-2xl font-bold text-black dark:text-white">{monitor.name}</h1>
          <p class="text-gray-600 dark:text-gray-400">{monitor.target}</p>
        </div>
      </div>
      <div class="flex gap-2">
        <button class="btn btn-sm bg-gray-200 dark:bg-neutral-800 hover:bg-gray-300 dark:hover:bg-neutral-700 text-black dark:text-white">Edit</button>
        <button class="btn btn-sm bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200">Delete</button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="card p-5 bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Status</p>
        <span class="px-3 py-1 rounded bg-black dark:bg-white text-white dark:text-black text-sm font-medium capitalize">
          {monitor.status}
        </span>
      </div>
      <div class="card p-5 bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Security</p>
        <div class="flex items-center gap-2">
          <span class="px-3 py-1 rounded bg-black/10 dark:bg-white/10 text-black dark:text-white text-sm font-medium capitalize">{monitor.security_status}</span>
          <span class="text-xs text-gray-600 dark:text-gray-400">{formatDate(monitor.last_security_check_at)}</span>
        </div>
      </div>
      <div class="card p-5 bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Interval</p>
        <p class="text-2xl font-bold text-black dark:text-white">{monitor.interval_seconds}s</p>
      </div>
    </div>

    <div class="card p-6 bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-black dark:text-white">Security Findings</h2>
        <button class="btn btn-sm bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200" disabled={auditLoading} onclick={runSecurityCheck}>
          {auditLoading ? 'Running...' : 'Run Security Check'}
        </button>
      </div>
      {#if auditError}
        <div class="p-3 border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950 rounded text-sm text-red-600 dark:text-red-400">{auditError}</div>
      {/if}
      {#if latestAudit}
        <p class="text-sm text-gray-600 dark:text-gray-400">Captured {formatDate(latestAudit.created_at)}</p>
        <pre class="bg-gray-100 dark:bg-neutral-900 text-xs rounded p-4 overflow-auto max-h-80 text-black dark:text-white">{JSON.stringify(latestFindings, null, 2)}</pre>
      {:else}
        <p class="text-sm text-gray-600 dark:text-gray-400">No security audits recorded yet.</p>
      {/if}
    </div>

    <div class="card p-6 bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-black dark:text-white">Security Audit History</h2>
        <button class="btn btn-sm bg-gray-200 dark:bg-neutral-800 hover:bg-gray-300 dark:hover:bg-neutral-700 text-black dark:text-white" disabled={auditLoading || !hasMoreAudits} onclick={loadMoreAudits}>
          {auditLoading ? 'Loading...' : hasMoreAudits ? 'Load More' : 'No More'}
        </button>
      </div>
      <div class="space-y-3">
        {#each audits as auditItem}
          <div class="border border-gray-200 dark:border-neutral-800 rounded-lg p-4 flex items-center justify-between bg-gray-50 dark:bg-neutral-900">
            <div>
              <p class="text-sm font-semibold text-black dark:text-white">{formatDate(auditItem.created_at)}</p>
              <p class="text-xs text-gray-600 dark:text-gray-400">Status: {auditItem.status}</p>
            </div>
            <span class="px-3 py-1 rounded bg-black dark:bg-white text-white dark:text-black text-sm font-medium capitalize">{auditItem.status}</span>
          </div>
        {/each}
        {#if !audits.length}
          <p class="text-sm text-gray-600 dark:text-gray-400">No audits yet.</p>
        {/if}
      </div>
    </div>
  {/if}
</div>
