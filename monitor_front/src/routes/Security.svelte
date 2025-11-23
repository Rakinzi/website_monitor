<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { Progress } from '@skeletonlabs/skeleton-svelte';
  import { onMount } from 'svelte';
  import { monitorsApi, securityApi } from '../lib/services/api';
  import type { SecurityAuditResponse } from '../lib/services/api';

  type SecurityStatus = 'pass' | 'warning' | 'critical';

  interface MonitorSummary {
    id: number;
    name: string;
    target: string;
    security_status?: SecurityStatus;
    last_security_check_at?: string | null;
  }

  interface SecurityScore {
    monitor_id: number;
    monitor_name: string;
    monitor_url: string;
    overall_score: number;
    ssl_score: number;
    headers_score: number;
    exposure_score: number;
    last_check: string | null;
    critical_issues: number;
    warnings: number;
    passed_checks: number;
    status: SecurityStatus;
  }

  let securityScores = $state<SecurityScore[]>([]);
  let isLoading = $state(true);
  let error = $state('');
  let refreshLoading = $state(false);

  onMount(async () => {
    await loadSecurity();
  });

  async function loadSecurity() {
    isLoading = true;
    error = '';
    try {
      const monitors = await monitorsApi.getAll();
      const audits = await Promise.all(
        monitors.map(async (monitor) => {
          try {
            const audit = await securityApi.latestMonitorSecurityCheck(monitor.id);
            return { monitor, audit };
          } catch {
            return { monitor, audit: null };
          }
        })
      );
      securityScores = audits.map(({ monitor, audit }) =>
        transformScore(monitor, audit)
      );
    } catch (err: any) {
      error = err?.message || 'Failed to load security data';
    } finally {
      isLoading = false;
    }
  }

  async function refreshAll() {
    refreshLoading = true;
    try {
      await Promise.all(
        securityScores.map(async (score) => {
          try {
            await securityApi.runMonitorSecurityCheck(score.monitor_id);
          } catch {
            /* ignore */
          }
        })
      );
      await loadSecurity();
    } finally {
      refreshLoading = false;
    }
  }

  function transformScore(monitor: MonitorSummary, audit: SecurityAuditResponse | null): SecurityScore {
    const headers = audit?.findings?.http_security_headers ?? {};
    const headerValues = Object.values(headers);
    const headerPass = headerValues.filter((val) => val === true).length;
    const headerTotal = headerValues.length || 1;

    const exposure = audit?.findings?.exposure_checks ?? {};
    const critical =
      Number(exposure.dot_env?.exposed ? 1 : 0) +
      Number(exposure.git_head?.exposed ? 1 : 0);
    const warnings = Object.entries(headers).reduce(
      (acc, [, val]) => (val === false ? acc + 1 : acc),
      Number(exposure.robots_disallows?.length ? 1 : 0)
    );

    const sslInfo = audit?.findings?.ssl_security ?? {};
    const sslScore =
      sslInfo.enabled === false
        ? 40
        : sslInfo.weak_cipher
          ? 70
          : 95;

    const headersScore = Math.round((headerPass / headerTotal) * 100);
    const exposureScore =
      critical > 0 ? 40 : warnings > 0 ? 70 : 95;

    const status: SecurityStatus = audit?.status ?? monitor.security_status ?? 'pass';

    const overall = Math.round((sslScore + headersScore + exposureScore) / 3);

    return {
      monitor_id: monitor.id,
      monitor_name: monitor.name,
      monitor_url: monitor.target,
      overall_score: overall,
      ssl_score: sslScore,
      headers_score: headersScore,
      exposure_score: exposureScore,
      last_check: audit?.created_at ?? monitor.last_security_check_at ?? null,
      critical_issues: critical,
      warnings,
      passed_checks: headerPass,
      status,
    };
  }

  function getScoreColor(score: number): string {
    if (score >= 90) return 'success';
    if (score >= 70) return 'warning';
    return 'error';
  }

  function getScoreLabel(score: number): string {
    if (score >= 90) return 'Excellent';
    if (score >= 80) return 'Good';
    if (score >= 70) return 'Fair';
    if (score >= 60) return 'Poor';
    return 'Critical';
  }

  function formatDate(dateString: string | null): string {
    if (!dateString) return 'n/a';
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);

    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  }

  const avgScore = $derived(
    securityScores.length > 0
      ? Math.round(securityScores.reduce((sum, s) => sum + s.overall_score, 0) / securityScores.length)
      : 0
  );

  const totalCritical = $derived(securityScores.reduce((sum, s) => sum + s.critical_issues, 0));
  const totalWarnings = $derived(securityScores.reduce((sum, s) => sum + s.warnings, 0));
  const totalPassed = $derived(securityScores.reduce((sum, s) => sum + s.passed_checks, 0));
</script>

<div class="p-8 space-y-8 bg-gradient-to-br from-surface-50 to-surface-100 dark:from-surface-950 dark:to-surface-900 min-h-screen">
  <!-- Header -->
  <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
    <div>
      <h1 class="text-4xl font-bold bg-gradient-to-r from-error-500 via-warning-500 to-success-500 bg-clip-text text-transparent">
        Security Dashboard
      </h1>
      <p class="text-surface-600-400 mt-1">Passive cybersecurity checks for monitored endpoints</p>
    </div>
    <div class="flex gap-3">
      <button class="btn variant-ghost-surface" disabled={refreshLoading || isLoading} onclick={refreshAll}>
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
        <span>{refreshLoading ? 'Refreshing...' : 'Refresh All'}</span>
      </button>
      <button class="btn variant-filled-primary shadow-lg shadow-primary-500/20">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <span>Export Report</span>
      </button>
    </div>
  </div>

  <!-- Stats Overview -->
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <div class="card preset-filled-surface-50-950 p-6 border border-surface-200-800">
      <div class="flex items-center justify-between mb-2">
        <p class="text-sm text-surface-600-400">Average Score</p>
        <div class="p-2 rounded-lg bg-gradient-to-br from-primary-500 to-secondary-500">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
        </div>
      </div>
      <p class="text-3xl font-bold text-{getScoreColor(avgScore)}-500">{avgScore}</p>
      <p class="text-xs text-surface-600-400 mt-1">{getScoreLabel(avgScore)}</p>
    </div>

    <div class="card preset-filled-surface-50-950 p-6 border border-error-200-800 bg-error-50/50 dark:bg-error-950/20">
      <div class="flex items-center justify-between mb-2">
        <p class="text-sm text-surface-600-400">Critical Issues</p>
        <div class="p-2 rounded-lg bg-error-500/20">
          <svg class="w-5 h-5 text-error-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
      </div>
      <p class="text-3xl font-bold text-error-500">{totalCritical}</p>
      <p class="text-xs text-surface-600-400 mt-1">Requires immediate attention</p>
    </div>

    <div class="card preset-filled-surface-50-950 p-6 border border-warning-200-800 bg-warning-50/50 dark:bg-warning-950/20">
      <div class="flex items-center justify-between mb-2">
        <p class="text-sm text-surface-600-400">Warnings</p>
        <div class="p-2 rounded-lg bg-warning-500/20">
          <svg class="w-5 h-5 text-warning-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
      </div>
      <p class="text-3xl font-bold text-warning-500">{totalWarnings}</p>
      <p class="text-xs text-surface-600-400 mt-1">Should be reviewed</p>
    </div>

    <div class="card preset-filled-surface-50-950 p-6 border border-success-200-800 bg-success-50/50 dark:bg-success-950/20">
      <div class="flex items-center justify-between mb-2">
        <p class="text-sm text-surface-600-400">Passed Checks</p>
        <div class="p-2 rounded-lg bg-success-500/20">
          <svg class="w-5 h-5 text-success-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
      </div>
      <p class="text-3xl font-bold text-success-500">{totalPassed}</p>
      <p class="text-xs text-surface-600-400 mt-1">Security best practices</p>
    </div>
  </div>

  {#if error}
    <div class="p-4 rounded border border-error-500/30 bg-error-500/10 text-error-500">
      {error}
    </div>
  {/if}

  {#if isLoading}
    <div class="text-center text-surface-600-400 py-12">
      <svg class="w-8 h-8 animate-spin mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
      </svg>
      Loading security data...
    </div>
  {:else if !securityScores.length}
    <div class="text-center text-surface-600-400 py-12">
      <svg class="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
      </svg>
      <p class="text-lg">No security data available</p>
      <p class="text-sm mt-2">Add monitors to start security checks</p>
    </div>
  {:else}
    <!-- Security Scores Grid -->
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
      {#each securityScores as score}
        <div
          class="card preset-filled-surface-50-950 border border-surface-200-800 p-6 hover:shadow-2xl hover:scale-[1.01] transition-all duration-300 cursor-pointer group"
          role="button"
          tabindex="0"
          onclick={() => push(`/security/${score.monitor_id}`)}
          onkeydown={(e) => e.key === 'Enter' && push(`/security/${score.monitor_id}`)}
        >
          <!-- Header -->
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <h3 class="text-xl font-bold mb-1 group-hover:text-primary-500 transition-colors">{score.monitor_name}</h3>
              <p class="text-sm text-surface-600-400 truncate">{score.monitor_url}</p>
              <p class="text-xs text-surface-600-400 mt-1">Last check: {formatDate(score.last_check)}</p>
            </div>
            <div class="flex flex-col items-center">
              <div class="w-20 h-20 rounded-full flex items-center justify-center bg-gradient-to-br from-{getScoreColor(score.overall_score)}-500/20 to-{getScoreColor(score.overall_score)}-500/10 border-4 border-{getScoreColor(score.overall_score)}-500">
                <span class="text-2xl font-bold text-{getScoreColor(score.overall_score)}-500">{score.overall_score}</span>
              </div>
              <span class="text-xs text-{getScoreColor(score.overall_score)}-500 font-medium mt-2">{getScoreLabel(score.overall_score)}</span>
            </div>
          </div>

          <!-- Score Breakdown -->
          <div class="grid grid-cols-3 gap-4 mb-4">
            <div>
              <p class="text-xs text-surface-600-400 mb-1 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
                SSL/TLS
              </p>
              <Progress value={score.ssl_score} max={100}>
                <Progress.Track class="bg-surface-200-800 h-1.5 rounded-full">
                  <Progress.Range class="bg-{getScoreColor(score.ssl_score)}-500 h-1.5 rounded-full" />
                </Progress.Track>
              </Progress>
              <p class="text-xs font-bold mt-1 text-{getScoreColor(score.ssl_score)}-500">{score.ssl_score}</p>
            </div>

            <div>
              <p class="text-xs text-surface-600-400 mb-1 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                </svg>
                Headers
              </p>
              <Progress value={score.headers_score} max={100}>
                <Progress.Track class="bg-surface-200-800 h-1.5 rounded-full">
                  <Progress.Range class="bg-{getScoreColor(score.headers_score)}-500 h-1.5 rounded-full" />
                </Progress.Track>
              </Progress>
              <p class="text-xs font-bold mt-1 text-{getScoreColor(score.headers_score)}-500">{score.headers_score}</p>
            </div>

            <div>
              <p class="text-xs text-surface-600-400 mb-1 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                Exposure
              </p>
              <Progress value={score.exposure_score} max={100}>
                <Progress.Track class="bg-surface-200-800 h-1.5 rounded-full">
                  <Progress.Range class="bg-{getScoreColor(score.exposure_score)}-500 h-1.5 rounded-full" />
                </Progress.Track>
              </Progress>
              <p class="text-xs font-bold mt-1 text-{getScoreColor(score.exposure_score)}-500">{score.exposure_score}</p>
            </div>
          </div>

          <!-- Issue Summary -->
          <div class="flex items-center justify-between pt-4 border-t border-surface-200-800">
            <div class="flex gap-4">
              {#if score.critical_issues > 0}
                <div class="flex items-center gap-1">
                  <span class="w-2 h-2 rounded-full bg-error-500"></span>
                  <span class="text-xs font-medium text-error-500">{score.critical_issues} Critical</span>
                </div>
              {/if}
              {#if score.warnings > 0}
                <div class="flex items-center gap-1">
                  <span class="w-2 h-2 rounded-full bg-warning-500"></span>
                  <span class="text-xs font-medium text-warning-500">{score.warnings} Warnings</span>
                </div>
              {/if}
              <div class="flex items-center gap-1">
                <span class="w-2 h-2 rounded-full bg-success-500"></span>
                <span class="text-xs font-medium text-success-500">{score.passed_checks} Passed</span>
              </div>
            </div>

            <button class="btn variant-ghost-primary btn-sm group-hover:variant-filled-primary transition-all">
              View Details
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </button>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
