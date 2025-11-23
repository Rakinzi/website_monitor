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
    <div class="text-center text-surface-600-400">Loading monitor...</div>
  {:else if error}
    <div class="p-4 border border-error-500/30 bg-error-500/10 rounded">{error}</div>
  {:else if monitor}
    <div class="flex justify-between items-center">
      <div class="flex items-center gap-4">
        <button class="btn variant-ghost-surface" onclick={() => pop()}>
          ← Back
        </button>
        <div>
          <h1 class="text-3xl font-bold">{monitor.name}</h1>
          <p class="text-surface-600-400">{monitor.target}</p>
        </div>
      </div>
      <div class="flex gap-2">
        <button class="btn variant-ghost-surface">Edit</button>
        <button class="btn variant-filled-error">Delete</button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="card p-6 preset-filled-surface-100-900">
        <p class="text-sm text-surface-600-400 mb-2">Status</p>
        <span class={`badge variant-filled-${monitor.status === 'down' ? 'error' : 'success'}`}>
          {monitor.status}
        </span>
      </div>
      <div class="card p-6 preset-filled-surface-100-900">
        <p class="text-sm text-surface-600-400 mb-2">Security</p>
        <div class="flex items-center gap-2">
          <span class={`badge variant-soft-${monitor.security_status}`}>{monitor.security_status}</span>
          <span class="text-xs text-surface-600-400">Last: {formatDate(monitor.last_security_check_at)}</span>
        </div>
      </div>
      <div class="card p-6 preset-filled-surface-100-900">
        <p class="text-sm text-surface-600-400 mb-2">Interval</p>
        <p class="text-2xl font-bold">{monitor.interval_seconds}s</p>
      </div>
    </div>

    <div class="card p-6 preset-filled-surface-100-900 space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold">Security Findings</h2>
        <button class="btn btn-sm" disabled={auditLoading} onclick={runSecurityCheck}>
          {auditLoading ? 'Running...' : 'Run security check'}
        </button>
      </div>
      {#if auditError}
        <div class="p-3 border border-error-500/20 bg-error-500/10 rounded text-sm text-error-600">{auditError}</div>
      {/if}
      {#if latestAudit}
        <p class="text-sm text-surface-600-400">Captured {formatDate(latestAudit.created_at)}</p>
        <pre class="bg-surface-900/5 text-xs rounded p-4 overflow-auto max-h-80">{JSON.stringify(latestFindings, null, 2)}</pre>
      {:else}
        <p class="text-sm text-surface-600-400">No security audits have been recorded yet.</p>
      {/if}
    </div>

    <div class="card p-6 preset-filled-surface-100-900 space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold">Security Audit History</h2>
        <button class="btn btn-sm variant-ghost-surface" disabled={auditLoading || !hasMoreAudits} onclick={loadMoreAudits}>
          {auditLoading ? 'Loading...' : hasMoreAudits ? 'Load more' : 'No more audits'}
        </button>
      </div>
      <div class="space-y-3">
        {#each audits as auditItem}
          <div class="border border-surface-200-800 rounded-lg p-4 flex items-center justify-between">
            <div>
              <p class="text-sm font-semibold">{formatDate(auditItem.created_at)}</p>
              <p class="text-xs text-surface-600-400">Status: {auditItem.status}</p>
            </div>
            <span class={`badge variant-filled-${auditItem.status}`}>{auditItem.status}</span>
          </div>
        {/each}
        {#if !audits.length}
          <p class="text-sm text-surface-600-400">No audits yet.</p>
        {/if}
      </div>
    </div>
  {/if}
</div>
