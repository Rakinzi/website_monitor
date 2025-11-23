<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { Progress } from '@skeletonlabs/skeleton-svelte';

  const incidents = [
    {
      id: '1',
      title: 'Payment Gateway Timeout',
      monitor: 'Payment Gateway',
      severity: 'critical',
      status: 'open',
      startedAt: '2025-01-15 09:45:00',
      duration: '45 minutes',
      affectedChecks: 15,
      description: 'Multiple timeout errors detected on payment processing endpoint',
      image: 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=400&h=300&fit=crop',
      durationMinutes: 45,
      totalMinutes: 60,
    },
    {
      id: '2',
      title: 'EU Region High Latency',
      monitor: 'CDN Endpoint',
      severity: 'warning',
      status: 'open',
      startedAt: '2025-01-15 08:30:00',
      duration: '2 hours',
      affectedChecks: 24,
      description: 'Response times exceeding 2000ms across EU data centers',
      image: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&h=300&fit=crop',
      durationMinutes: 120,
      totalMinutes: 180,
    },
    {
      id: '3',
      title: 'SSL Certificate Expiring Soon',
      monitor: 'Main Website',
      severity: 'info',
      status: 'acknowledged',
      startedAt: '2025-01-14 14:00:00',
      duration: '20 hours',
      affectedChecks: 1,
      description: 'SSL certificate expires in 7 days - renewal required',
      image: 'https://images.unsplash.com/photo-1633265486064-086b219458ec?w=400&h=300&fit=crop',
      durationMinutes: 1200,
      totalMinutes: 1440,
    },
    {
      id: '4',
      title: 'API Downtime',
      monitor: 'Production API',
      severity: 'critical',
      status: 'resolved',
      startedAt: '2025-01-13 16:20:00',
      duration: '15 minutes',
      affectedChecks: 5,
      description: 'Complete service outage - database connection failure',
      image: 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400&h=300&fit=crop',
      durationMinutes: 15,
      totalMinutes: 15,
    },
  ];

  function getSeverityColor(severity: string) {
    const colors: Record<string, string> = {
      critical: 'error',
      warning: 'warning',
      info: 'primary',
    };
    return colors[severity] || 'surface';
  }

  function getStatusColor(status: string) {
    const colors: Record<string, string> = {
      open: 'error',
      acknowledged: 'warning',
      resolved: 'success',
    };
    return colors[status] || 'surface';
  }

  function getSeverityIcon(severity: string) {
    if (severity === 'critical') {
      return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`;
    }
    if (severity === 'warning') {
      return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;
    }
    return `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;
  }

  function getStatusIcon(status: string) {
    if (status === 'open') {
      return `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;
    }
    if (status === 'acknowledged') {
      return `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>`;
    }
    return `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;
  }
</script>

<div class="p-8 space-y-8 bg-linear-to-br from-surface-50 to-surface-100 dark:from-surface-950 dark:to-surface-900 min-h-screen">
  <!-- Header -->
  <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
    <div>
      <h1 class="text-4xl font-bold bg-linear-to-r from-error-500 to-warning-500 bg-clip-text text-transparent">
        Incidents
      </h1>
      <p class="text-surface-600-400 mt-1">Monitor and respond to service incidents</p>
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
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
        </svg>
        <span>Alert Settings</span>
      </button>
    </div>
  </div>

  <!-- Stats Overview -->
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <div class="card preset-filled-surface-50-950 p-4 border border-surface-200-800">
      <p class="text-sm text-surface-600-400 mb-1">Total Incidents</p>
      <p class="text-2xl font-bold">{incidents.length}</p>
    </div>
    <div class="card preset-filled-surface-50-950 p-4 border border-error-200-800 bg-error-50/50 dark:bg-error-950/20">
      <p class="text-sm text-surface-600-400 mb-1">Open</p>
      <p class="text-2xl font-bold text-error-500">{incidents.filter(i => i.status === 'open').length}</p>
    </div>
    <div class="card preset-filled-surface-50-950 p-4 border border-warning-200-800 bg-warning-50/50 dark:bg-warning-950/20">
      <p class="text-sm text-surface-600-400 mb-1">Acknowledged</p>
      <p class="text-2xl font-bold text-warning-500">{incidents.filter(i => i.status === 'acknowledged').length}</p>
    </div>
    <div class="card preset-filled-surface-50-950 p-4 border border-success-200-800 bg-success-50/50 dark:bg-success-950/20">
      <p class="text-sm text-surface-600-400 mb-1">Resolved</p>
      <p class="text-2xl font-bold text-success-500">{incidents.filter(i => i.status === 'resolved').length}</p>
    </div>
  </div>

  <!-- Incidents List -->
  <div class="grid grid-cols-1 gap-6">
    {#each incidents as incident}
      <div
        class="card preset-filled-surface-50-950 border border-surface-200-800 overflow-hidden hover:shadow-2xl hover:scale-[1.01] transition-all duration-300 cursor-pointer group"
        role="button"
        tabindex="0"
        onclick={() => push(`/incidents/${incident.id}`)}
        onkeydown={(e) => e.key === 'Enter' && push(`/incidents/${incident.id}`)}
      >
        <div class="flex flex-col md:flex-row">
          <!-- Image Section -->
          <div class="relative md:w-64 h-48 md:h-auto overflow-hidden shrink-0">
            <img
              src={incident.image}
              alt={incident.title}
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            />
            <div class="absolute inset-0 bg-linear-to-r from-{getSeverityColor(incident.severity)}-900/90 to-transparent"></div>
            <div class="absolute top-4 left-4">
              <div class="p-2 rounded-lg bg-{getSeverityColor(incident.severity)}-500/20 backdrop-blur-sm text-{getSeverityColor(incident.severity)}-500 border border-{getSeverityColor(incident.severity)}-500/30">
                {@html getSeverityIcon(incident.severity)}
              </div>
            </div>
            <div class="absolute bottom-4 left-4 right-4">
              <span class="badge variant-filled-{getSeverityColor(incident.severity)} text-xs font-semibold uppercase shadow-lg">
                {incident.severity}
              </span>
            </div>
          </div>

          <!-- Content Section -->
          <div class="flex-1 p-6 space-y-4">
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <h3 class="text-xl font-bold group-hover:text-{getSeverityColor(incident.severity)}-500 transition-colors">{incident.title}</h3>
                  <span class="badge variant-soft-{getStatusColor(incident.status)} text-xs font-medium flex items-center gap-1">
                    {@html getStatusIcon(incident.status)}
                    {incident.status}
                  </span>
                </div>
                <p class="text-sm text-surface-600-400 mb-1">{incident.description}</p>
                <p class="text-xs text-surface-600-400">Monitor: <span class="font-semibold text-surface-700-300">{incident.monitor}</span></p>
              </div>
            </div>

            <!-- Duration Progress -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-medium text-surface-600-400">Incident Duration</span>
                <span class="text-sm font-bold text-{getSeverityColor(incident.severity)}-500">
                  {incident.duration}
                </span>
              </div>
              <Progress value={incident.durationMinutes} max={incident.totalMinutes}>
                <Progress.Track class="bg-surface-200-800 h-2 rounded-full">
                  <Progress.Range class={`bg-${getSeverityColor(incident.severity)}-500 h-2 rounded-full`} />
                </Progress.Track>
              </Progress>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-3 gap-4 pt-4 border-t border-surface-200-800">
              <div class="text-center">
                <p class="text-xs text-surface-600-400 mb-1">Started At</p>
                <p class="text-sm font-bold">{incident.startedAt.split(' ')[1]}</p>
                <p class="text-xs text-surface-600-400">{incident.startedAt.split(' ')[0]}</p>
              </div>
              <div class="text-center">
                <p class="text-xs text-surface-600-400 mb-1">Affected Checks</p>
                <p class="text-sm font-bold">{incident.affectedChecks}</p>
              </div>
              <div class="text-center">
                <p class="text-xs text-surface-600-400 mb-1">Status</p>
                <p class="text-sm font-bold capitalize text-{getStatusColor(incident.status)}-500">{incident.status}</p>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-2 pt-2">
              <button class="btn variant-ghost-primary flex-1 group-hover:variant-filled-primary transition-all">
                View Details
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                </svg>
              </button>
              {#if incident.status === 'open'}
                <button class="btn variant-filled-warning btn-sm">
                  Acknowledge
                </button>
              {/if}
              {#if incident.status === 'acknowledged'}
                <button class="btn variant-filled-success btn-sm">
                  Resolve
                </button>
              {/if}
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>
