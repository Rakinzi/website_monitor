<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { Progress } from '@skeletonlabs/skeleton-svelte';
  import { onMount } from 'svelte';
  import { monitorsApi, securityApi } from '../lib/services/api';

  let { params } = $props<{ params: { id: string } }>();

  type Status = 'pass' | 'warning' | 'critical';
  type CheckStatus = 'passed' | 'warning' | 'critical';

  interface SecurityCheck {
    category: string;
    check_name: string;
    status: CheckStatus;
    message: string;
    details?: string;
    recommendation?: string | null;
  }

  interface Monitor {
    id: number;
    name: string;
    target: string;
    security_status?: Status;
  }

  interface SecurityAudit {
    id: number;
    monitor_id: number;
    status: Status;
    created_at: string;
    findings: Record<string, any>;
  }

  let monitor = $state<Monitor | null>(null);
  let audit = $state<SecurityAudit | null>(null);
  let isLoading = $state(true);
  let error = $state('');
  let running = $state(false);

  onMount(loadDetails);

  async function loadDetails() {
    isLoading = true;
    error = '';
    try {
      monitor = await monitorsApi.getById(params.id);
      if (monitor) {
        try {
          audit = await securityApi.latestMonitorSecurityCheck(monitor.id);
        } catch {
          audit = null;
        }
      }
    } catch (err: any) {
      error = err?.message || 'Failed to load security details';
    } finally {
      isLoading = false;
    }
  }

  async function runAudit() {
    if (!monitor) return;
    running = true;
    error = '';
    try {
      audit = await securityApi.runMonitorSecurityCheck(monitor.id);
    } catch (err: any) {
      error = err?.message || 'Unable to run security check';
    } finally {
      running = false;
    }
  }

  const checks = $derived(audit ? buildChecks(audit) : []);
  const sslDetails = $derived(audit?.findings?.ssl_security ?? null);
  const headerEntries = $derived(audit ? Object.entries(audit.findings?.http_security_headers ?? {}) : []);
  const exposure = $derived(audit?.findings?.exposure_checks ?? {});
  const dnsRecords = $derived(audit?.findings?.dns_security ?? {});
  const waf = $derived(audit?.findings?.safe_waf_detection ?? {});
  const technology = $derived(audit?.findings?.technology_fingerprinting ?? {});
  const overallScore = $derived(scoreFromStatus(audit?.status ?? monitor?.security_status ?? 'pass'));

  function buildChecks(current: SecurityAudit): SecurityCheck[] {
    const items: SecurityCheck[] = [];
    const findings = current.findings ?? {};

    const headers = findings.http_security_headers ?? {};
    Object.entries(headers).forEach(([key, value]) => {
      items.push({
        category: 'HTTP Security Headers',
        check_name: key,
        status: value ? 'passed' : 'warning',
        message: value ? 'Header present' : 'Missing header',
      });
    });

    const exposure = findings.exposure_checks ?? {};
    ['dot_env', 'git_head'].forEach((key) => {
      if (exposure[key]) {
        items.push({
          category: 'Exposure Checks',
          check_name: key,
          status: exposure[key].exposed ? 'critical' : 'passed',
          message: exposure[key].exposed ? 'Exposed publicly' : 'Protected',
        });
      }
    });
    if (exposure.robots_disallows?.length) {
      items.push({
        category: 'Exposure Checks',
        check_name: 'robots.txt',
        status: 'warning',
        message: `Sensitive paths blocked: ${exposure.robots_disallows.join(', ')}`,
      });
    }

    if (findings.ssl_security) {
      items.push({
        category: 'SSL/TLS Security',
        check_name: 'Certificate',
        status: findings.ssl_security.enabled === false ? 'warning' : 'passed',
        message: findings.ssl_security.enabled === false ? 'HTTPS disabled' : 'HTTPS enabled',
      });
      if (findings.ssl_security.weak_cipher) {
        items.push({
          category: 'SSL/TLS Security',
          check_name: 'Cipher strength',
          status: 'warning',
          message: `Weak cipher ${findings.ssl_security.cipher_suite}`,
        });
      }
    }

    if (findings.basic_app_security?.downgraded_to_http) {
      items.push({
        category: 'Best Practices',
        check_name: 'HTTPS Redirect',
        status: 'critical',
        message: 'HTTPS downgraded to HTTP',
      });
    }

    return items;
  }

  function scoreFromStatus(status: Status): number {
    switch (status) {
      case 'critical':
        return 50;
      case 'warning':
        return 75;
      default:
        return 95;
    }
  }

  function getStatusIcon(status: string) {
    if (status === 'passed') {
      return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;
    }
    if (status === 'critical') {
      return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`;
    }
    return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;
  }

  function getStatusColor(status: CheckStatus) {
    if (status === 'passed') return 'success';
    if (status === 'warning') return 'warning';
    return 'error';
  }

  function formatDate(value: string | undefined) {
    if (!value) return 'N/A';
    return new Date(value).toLocaleString();
  }

  function statusBadge(status: Status | undefined) {
    if (status === 'critical') return 'error';
    if (status === 'warning') return 'warning';
    return 'success';
  }
</script>

<div class="p-8 space-y-6 bg-gradient-to-br from-surface-50 to-surface-100 dark:from-surface-950 dark:to-surface-900 min-h-screen">
  {#if isLoading}
    <div class="text-center text-surface-600-400">Loading security findings...</div>
  {:else if error}
    <div class="p-4 border border-error-500/30 bg-error-500/10 rounded">{error}</div>
  {:else if !monitor}
    <div class="p-4 border border-warning-500/30 bg-warning-500/10 rounded">Monitor not found.</div>
  {:else}
    <div class="flex flex-col md:flex-row justify-between gap-4">
      <div>
        <button class="text-sm text-primary-500 underline mb-3" onclick={() => push('/security')}>
          ← Back to Security Dashboard
        </button>
        <h1 class="text-3xl font-bold">{monitor.name}</h1>
        <p class="text-surface-600-400">{monitor.target}</p>
        <p class="text-xs text-surface-600-400">Last check: {formatDate(audit?.created_at)}</p>
      </div>
        <div class="card preset-filled-surface-50-950 p-5 border border-surface-200-800 max-w-sm">
          <p class="text-sm text-surface-600-400 mb-1">Overall Score</p>
          <div class="flex items-center gap-3">
            <span class="text-4xl font-bold">{overallScore}</span>
            <span class={`badge variant-filled-${statusBadge(audit?.status ?? monitor.security_status)} capitalize`}>
              {audit?.status ?? monitor.security_status ?? 'pass'}
            </span>
          </div>
        <button class="btn mt-4 w-full" disabled={running} onclick={runAudit}>
          {running ? 'Running security check...' : 'Run security check'}
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="card preset-filled-surface-50-950 border border-surface-200-800 p-5">
        <h2 class="text-lg font-semibold mb-4">SSL/TLS</h2>
        {#if sslDetails}
          <ul class="space-y-2 text-sm text-surface-600-400">
            <li>Issuer: <span class="font-semibold text-surface-900-50">{sslDetails.issuer ?? 'Unknown'}</span></li>
            <li>Expires: <span class="font-semibold text-surface-900-50">{sslDetails.expires_at ?? 'Unknown'}</span></li>
            <li>Protocol: <span class="font-semibold text-surface-900-50">{sslDetails.protocol ?? 'N/A'}</span></li>
            <li>Cipher: <span class="font-semibold text-surface-900-50">{sslDetails.cipher_suite ?? 'N/A'}</span></li>
          </ul>
        {:else}
          <p class="text-sm text-surface-600-400">No SSL data available.</p>
        {/if}
      </div>

      <div class="card preset-filled-surface-50-950 border border-surface-200-800 p-5">
        <h2 class="text-lg font-semibold mb-4">Security Headers</h2>
        <ul class="space-y-2 text-sm">
          {#each headerEntries as [key, value]}
            <li class="flex justify-between">
              <span>{key}</span>
              <span class={`badge variant-soft-${value ? 'success' : 'warning'}`}>{value ? 'Present' : 'Missing'}</span>
            </li>
          {/each}
        </ul>
      </div>

      <div class="card preset-filled-surface-50-950 border border-surface-200-800 p-5">
        <h2 class="text-lg font-semibold mb-4">Exposure & WAF</h2>
        <p class="text-sm text-surface-600-400">.env exposed: <span class="font-semibold text-surface-900-50">{exposure?.dot_env?.exposed ? 'Yes' : 'No'}</span></p>
        <p class="text-sm text-surface-600-400">.git exposed: <span class="font-semibold text-surface-900-50">{exposure?.git_head?.exposed ? 'Yes' : 'No'}</span></p>
        <p class="text-sm text-surface-600-400 mt-3">WAF Headers: {waf?.headers?.length ? waf.headers.join(', ') : 'None detected'}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="card preset-filled-surface-50-950 border border-surface-200-800 p-5">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold">Checks</h2>
          <span class="text-sm text-surface-600-400">{checks.length} total</span>
        </div>
        <div class="space-y-3 max-h-96 overflow-auto pr-2">
          {#each checks as check}
            <div class="border border-surface-200-800 rounded-lg p-3 bg-surface-100-900/40">
              <div class="flex items-center gap-2">
                <span class={`p-1 rounded bg-${getStatusColor(check.status)}-500/15 text-${getStatusColor(check.status)}-500`}>
                  {@html getStatusIcon(check.status)}
                </span>
                <div>
                  <p class="text-sm font-semibold">{check.check_name}</p>
                  <p class="text-xs text-surface-600-400">{check.category}</p>
                </div>
              </div>
              <p class="text-sm mt-2 text-surface-600-400">{check.message}</p>
            </div>
          {/each}
        </div>
      </div>

      <div class="card preset-filled-surface-50-950 border border-surface-200-800 p-5 space-y-3">
        <h2 class="text-lg font-semibold">DNS & Technology</h2>
        <div>
          <p class="text-sm font-semibold">DNS Records</p>
          <ul class="text-sm text-surface-600-400">
            <li>CAA: {dnsRecords.caa?.length ? dnsRecords.caa.join(', ') : 'None'}</li>
            <li>DNSSEC: {dnsRecords.dnskey?.length ? 'Enabled' : 'Disabled'}</li>
            <li>MX: {dnsRecords.mx?.length ? dnsRecords.mx.join(', ') : 'None'}</li>
          </ul>
        </div>
        <div>
          <p class="text-sm font-semibold mt-3">Technology</p>
          <ul class="text-sm text-surface-600-400">
            <li>Server: {technology.server ?? 'Unknown'}</li>
            <li>X-Powered-By: {technology.x_powered_by ?? 'Unknown'}</li>
            <li>CDN: {technology.cdn ?? 'Unknown'}</li>
          </ul>
        </div>
      </div>
    </div>
  {/if}
</div>
