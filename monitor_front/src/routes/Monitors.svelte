<script lang="ts">
  import { Progress } from '@skeletonlabs/skeleton-svelte';
  import { push } from 'svelte-spa-router';
  import { onMount } from 'svelte';
  import { monitorsApi, securityApi } from '../lib/services/api';
  import type { SecurityAuditResponse } from '../lib/services/api';

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

  type SecurityAudit = SecurityAuditResponse;

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

  const statusMap: Record<MonitorStatus, { label: string; value: number }> = {
    healthy: { label: 'Operational', value: 100 },
    degraded: { label: 'Degraded', value: 65 },
    down: { label: 'Down', value: 0 },
    unknown: { label: 'Unknown', value: 40 },
  };

  const securityMap: Record<SecurityStatus, { label: string }> = {
    pass: { label: 'Secure' },
    warning: { label: 'Warnings' },
    critical: { label: 'Critical' },
  };

  function getStatusMeta(status: MonitorStatus) {
    return statusMap[status] ?? statusMap.unknown;
  }

  function getSecurityMeta(status: SecurityStatus) {
    return securityMap[status] ?? securityMap.pass;
  }

  function formatTimestamp(timestamp?: string | null) {
    if (!timestamp) return 'n/a';
    return new Date(timestamp).toLocaleDateString();
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

<div class="p-6 space-y-6">
  <!-- Header -->
  <div class="flex justify-between items-center">
    <h1 class="text-2xl font-bold text-black dark:text-white">Monitors</h1>
    <button class="btn btn-sm bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
      </svg>
      <span>Add Monitor</span>
    </button>
  </div>

  <!-- Stats Overview -->
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Monitors</p>
      <p class="text-2xl font-bold text-black dark:text-white">{monitors.length}</p>
    </div>
    <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Operational</p>
      <p class="text-2xl font-bold text-black dark:text-white">{monitors.filter((m) => m.status === 'healthy').length}</p>
    </div>
    <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Down</p>
      <p class="text-2xl font-bold text-black dark:text-white">{monitors.filter((m) => m.status === 'down').length}</p>
    </div>
    <div class="card bg-white dark:bg-neutral-950 p-5 border border-gray-200 dark:border-neutral-800">
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Avg Interval</p>
      <p class="text-2xl font-bold text-black dark:text-white">{avgInterval()}s</p>
    </div>
  </div>

  {#if error}
    <div class="p-4 rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950 text-red-600 dark:text-red-400">
      {error}
    </div>
  {/if}

  {#if auditError}
    <div class="p-4 rounded-lg border border-yellow-200 dark:border-yellow-800 bg-yellow-50 dark:bg-yellow-950 text-yellow-600 dark:text-yellow-400">
      {auditError}
    </div>
  {/if}

  {#if isLoading}
    <div class="text-center text-gray-600 dark:text-gray-400">Loading monitors...</div>
  {:else if !monitors.length}
    <div class="text-center text-gray-600 dark:text-gray-400">No monitors available. Create one to get started.</div>
  {:else}
    <!-- Monitors Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      {#each monitors as monitor}
        <div
          class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 overflow-hidden hover:shadow-lg transition-all cursor-pointer"
          role="button"
          tabindex="0"
          onclick={() => push(`/monitors/${monitor.id}`)}
          onkeydown={(e) => e.key === 'Enter' && push(`/monitors/${monitor.id}`)}
        >
          <!-- Monitor Header -->
          <div class="p-4 bg-gray-50 dark:bg-neutral-900 border-b border-gray-200 dark:border-neutral-800">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg font-bold text-black dark:text-white">{monitor.name}</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 truncate">{monitor.target}</p>
              </div>
              <span class="px-2 py-1 bg-black/10 dark:bg-white/10 rounded text-xs text-black dark:text-white capitalize">
                {monitor.monitor_type}
              </span>
            </div>
          </div>

          <!-- Monitor Content -->
          <div class="p-4 space-y-4">
            <!-- Status Bar -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-medium text-gray-600 dark:text-gray-400">Health</span>
                <span class="text-sm font-bold text-black dark:text-white capitalize">
                  {monitor.status}
                </span>
              </div>
              <Progress value={getStatusMeta(monitor.status).value} max={100}>
                <Progress.Track class="bg-gray-200 dark:bg-neutral-800 h-2 rounded-full">
                  <Progress.Range class="bg-black dark:bg-white h-2 rounded-full" />
                </Progress.Track>
              </Progress>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200 dark:border-neutral-800">
              <div class="text-center">
                <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Interval</p>
                <p class="text-sm font-bold text-black dark:text-white">{monitor.interval_seconds}s</p>
              </div>
              <div class="text-center">
                <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Timeout</p>
                <p class="text-sm font-bold text-black dark:text-white">{monitor.timeout_seconds}s</p>
              </div>
              <div class="text-center">
                <p class="text-xs text-gray-600 dark:text-gray-400 mb-1">Updated</p>
                <p class="text-xs font-bold text-black dark:text-white">{formatTimestamp(monitor.updated_at)}</p>
              </div>
            </div>

            <!-- Security Section -->
            <div class="p-3 rounded-lg border border-gray-200 dark:border-neutral-800 bg-gray-50 dark:bg-neutral-900 space-y-2">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-xs text-gray-600 dark:text-gray-400">Security Posture</p>
                  <p class="text-xs font-semibold text-black dark:text-white">Last: {formatTimestamp(monitor.last_security_check_at)}</p>
                </div>
                <span class="px-2 py-1 bg-black dark:bg-white text-white dark:text-black rounded text-xs capitalize">
                  {getSecurityMeta(monitor.security_status).label}
                </span>
              </div>
              {#if securityAudits[monitor.id]}
                <p class="text-xs text-gray-600 dark:text-gray-400">
                  Checked {formatTimestamp(securityAudits[monitor.id]?.created_at || '')}
                </p>
              {:else}
                <p class="text-xs text-gray-600 dark:text-gray-400">No audits recorded yet</p>
              {/if}
              <button
                class="btn btn-sm bg-gray-200 dark:bg-neutral-800 hover:bg-gray-300 dark:hover:bg-neutral-700 text-black dark:text-white w-full"
                disabled={auditLoading[monitor.id]}
                onclick={(event) => {
                  event.stopPropagation();
                  runAudit(monitor.id);
                }}
              >
                {auditLoading[monitor.id] ? 'Running...' : 'Run Security Check'}
              </button>
            </div>

            <!-- Action Button -->
            <button class="btn bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200 w-full">
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
