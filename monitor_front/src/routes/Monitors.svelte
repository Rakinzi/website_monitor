<script lang="ts">
  import { Progress } from '@skeletonlabs/skeleton-svelte';
  import { push } from 'svelte-spa-router';
  import { onMount } from 'svelte';
  import { monitorsApi, securityApi } from '../lib/services/api';

  type MonitorStatus = 'healthy' | 'degraded' | 'down' | 'unknown';
  type SecurityStatus = 'pass' | 'warning' | 'critical';

  interface Monitor {
    id: number;
    name: string;
    target: string;
    monitor_type: string;
    status: MonitorStatus;
    interval_seconds: number;
    timeout_seconds: number;
    failure_threshold: number;
    success_threshold: number;
    regions?: string[];
    tags?: string[];
    created_at: string;
    updated_at: string;
    security_status: SecurityStatus;
    last_security_check_at?: string | null;
  }

  interface SecurityAudit {
    id: number;
    status: SecurityStatus;
    findings: Record<string, any>;
    created_at: string;
  }

  let monitors: Monitor[] = [];
  let isLoading = true;
  let error = '';
  let auditError = '';
  let securityAudits: Record<number, SecurityAudit | null> = {};
  let auditLoading: Record<number, boolean> = {};

  onMount(async () => {
    try {
      monitors = await monitorsApi.getAll();
      await fetchAuditSnapshots();
    } catch (err: any) {
      error = err?.message || 'Unable to load monitors';
    } finally {
      isLoading = false;
    }
  });

  async function fetchAuditSnapshots() {
    const results = await Promise.all(
      monitors.map(async (monitor) => {
        try {
          const audit = await securityApi.latestMonitorSecurityCheck(monitor.id);
          return { id: monitor.id, audit };
        } catch (err: any) {
          return { id: monitor.id, audit: null };
        }
      })
    );
    const next: Record<number, SecurityAudit | null> = {};
    results.forEach(({ id, audit }) => {
      next[id] = audit;
    });
    securityAudits = next;
  }

  const statusMap: Record<MonitorStatus, { label: string; color: string; value: number }> = {
    healthy: { label: 'Operational', color: 'success', value: 100 },
    degraded: { label: 'Degraded', color: 'warning', value: 65 },
    down: { label: 'Down', color: 'error', value: 0 },
    unknown: { label: 'Unknown', color: 'surface', value: 40 },
  };

  const securityMap: Record<SecurityStatus, { label: string; color: string }> = {
    pass: { label: 'Secure', color: 'success' },
    warning: { label: 'Warnings', color: 'warning' },
    critical: { label: 'Critical', color: 'error' },
  };

  function getStatusMeta(status: MonitorStatus) {
    return statusMap[status] ?? statusMap.unknown;
  }

  function getSecurityMeta(status: SecurityStatus) {
    return securityMap[status] ?? securityMap.pass;
  }

  function formatTimestamp(timestamp?: string | null) {
    if (!timestamp) return 'n/a';
    return new Date(timestamp).toLocaleString();
  }

  function avgInterval() {
    if (!monitors.length) return 0;
    const total = monitors.reduce((acc, monitor) => acc + monitor.interval_seconds, 0);
    return Math.round(total / monitors.length);
  }

  async function runAudit(monitorId: number) {
    auditError = '';
    auditLoading = { ...auditLoading, [monitorId]: true };
    try {
      const audit = (await securityApi.runMonitorSecurityCheck(monitorId)) as SecurityAudit;
      securityAudits = { ...securityAudits, [monitorId]: audit };
      monitors = monitors.map((m) =>
        m.id === monitorId
          ? { ...m, security_status: audit.status, last_security_check_at: audit.created_at }
          : m
      );
    } catch (err: any) {
      auditError = err?.message || 'Unable to trigger security check';
    } finally {
      auditLoading = { ...auditLoading, [monitorId]: false };
    }
  }
</script>

<div class="p-8 space-y-8 bg-linear-to-br from-surface-50 to-surface-100 dark:from-surface-950 dark:to-surface-900 min-h-screen">
  <!-- Header -->
  <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
    <div>
      <h1 class="text-4xl font-bold bg-linear-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent">
        Monitors
      </h1>
      <p class="text-surface-600-400 mt-1">Manage and track all your monitoring endpoints</p>
    </div>
    <div class="flex gap-3">
      <button class="btn variant-ghost-surface">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
        </svg>
        <span>Filter</span>
      </button>
      <button class="btn variant-filled-primary shadow-lg shadow-primary-500/20">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        <span>Add Monitor</span>
      </button>
    </div>
  </div>

  <!-- Stats Overview -->
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <div class="card preset-filled-surface-50-950 p-4 border border-surface-200-800">
      <p class="text-sm text-surface-600-400 mb-1">Total Monitors</p>
      <p class="text-2xl font-bold">{monitors.length}</p>
    </div>
    <div class="card preset-filled-surface-50-950 p-4 border border-surface-200-800">
      <p class="text-sm text-surface-600-400 mb-1">Operational</p>
      <p class="text-2xl font-bold text-success-500">{monitors.filter((m) => m.status === 'healthy').length}</p>
    </div>
    <div class="card preset-filled-surface-50-950 p-4 border border-surface-200-800">
      <p class="text-sm text-surface-600-400 mb-1">Down</p>
      <p class="text-2xl font-bold text-error-500">{monitors.filter((m) => m.status === 'down').length}</p>
    </div>
    <div class="card preset-filled-surface-50-950 p-4 border border-surface-200-800">
      <p class="text-sm text-surface-600-400 mb-1">Avg Interval</p>
      <p class="text-2xl font-bold">{avgInterval()}s</p>
    </div>
  </div>

  {#if error}
    <div class="p-4 rounded border border-error-500/30 bg-error-500/10 text-error-500">
      {error}
    </div>
  {/if}

  {#if auditError}
    <div class="p-4 rounded border border-warning-500/30 bg-warning-500/10 text-warning-600">
      {auditError}
    </div>
  {/if}

  {#if isLoading}
    <div class="text-center text-surface-600-400">Loading monitors...</div>
  {:else if !monitors.length}
    <div class="text-center text-surface-600-400">No monitors available. Create one to get started.</div>
  {:else}
    <!-- Monitors Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {#each monitors as monitor}
        <div
          class="card preset-filled-surface-50-950 border border-surface-200-800 overflow-hidden hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 cursor-pointer group"
          role="button"
          tabindex="0"
          onclick={() => push(`/monitors/${monitor.id}`)}
          onkeydown={(e) => e.key === 'Enter' && push(`/monitors/${monitor.id}`)}
        >
          <!-- Monitor Header -->
          <div class="relative h-32 overflow-hidden bg-linear-to-r from-primary-500/80 to-secondary-500/80 text-white flex items-end p-4">
            <div>
              <p class="uppercase text-xs tracking-wide opacity-80">Status</p>
              <p class="text-xl font-semibold">{getStatusMeta(monitor.status).label}</p>
            </div>
            <div class="absolute top-3 right-3 badge variant-soft text-xs capitalize">
              {monitor.monitor_type}
            </div>
          </div>

        <!-- Monitor Content -->
        <div class="p-6 space-y-4">
          <div>
            <h3 class="text-xl font-bold mb-1 group-hover:text-primary-500 transition-colors">{monitor.name}</h3>
            <p class="text-sm text-surface-600-400 truncate">{monitor.target}</p>
          </div>

            <!-- Status Bar -->
            <div>
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-medium text-surface-600-400">Health</span>
              <span class={`text-sm font-bold text-${getStatusMeta(monitor.status).color}-500 capitalize`}>
                {monitor.status}
              </span>
              </div>
              <Progress value={getStatusMeta(monitor.status).value} max={100}>
                <Progress.Track class="bg-surface-200-800 h-2 rounded-full">
                  <Progress.Range class={`bg-${getStatusMeta(monitor.status).color}-500 h-2 rounded-full`} />
                </Progress.Track>
              </Progress>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-3 gap-4 pt-2 border-t border-surface-200-800">
              <div class="text-center">
                <p class="text-xs text-surface-600-400 mb-1">Interval</p>
                <p class="text-sm font-bold">{monitor.interval_seconds}s</p>
              </div>
              <div class="text-center">
                <p class="text-xs text-surface-600-400 mb-1">Timeout</p>
                <p class="text-sm font-bold">{monitor.timeout_seconds}s</p>
              </div>
              <div class="text-center">
                <p class="text-xs text-surface-600-400 mb-1">Updated</p>
                <p class="text-sm font-bold">{formatTimestamp(monitor.updated_at)}</p>
              </div>
            </div>

          <div class="p-4 rounded-lg border border-surface-200-800 bg-surface-100-900/50 space-y-2">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs text-surface-600-400">Security Posture</p>
                <p class="text-sm font-semibold">Last check: {formatTimestamp(monitor.last_security_check_at)}</p>
              </div>
              <span class={`badge variant-filled-${getSecurityMeta(monitor.security_status).color} capitalize`}>
                {getSecurityMeta(monitor.security_status).label}
              </span>
            </div>
            {#if securityAudits[monitor.id]}
              <p class="text-xs text-surface-600-400">
                Findings captured {new Date(securityAudits[monitor.id]?.created_at || '').toLocaleString()}
              </p>
            {:else}
              <p class="text-xs text-surface-600-400">No security audits recorded yet.</p>
            {/if}
            <button
              class="btn btn-sm variant-ghost-primary"
              disabled={auditLoading[monitor.id]}
              onclick={(event) => {
                event.stopPropagation();
                runAudit(monitor.id);
              }}
            >
              {auditLoading[monitor.id] ? 'Running check...' : 'Run security check'}
            </button>
          </div>

          <!-- Action Button -->
          <button class="btn variant-ghost-primary w-full group-hover:variant-filled-primary transition-all">
            View Details
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
              </svg>
            </button>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
