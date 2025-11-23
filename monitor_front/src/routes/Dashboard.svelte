<script lang="ts">
  // Mock data - will be replaced with API calls
  const uptimeStats = {
    overall: 99.8,
    today: 100,
    week: 99.9,
    month: 99.8,
  };

  const activeIncidents = 2;
  const totalMonitors = 15;
  const activeMonitors = 13;
</script>

<div class="p-8 space-y-8 bg-gradient-to-br from-surface-50 to-surface-100 dark:from-surface-950 dark:to-surface-900 min-h-screen">
  <!-- Header -->
  <div class="flex justify-between items-center">
    <div>
      <h1 class="text-4xl font-bold bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent">
        Dashboard
      </h1>
      <p class="text-surface-600-400 mt-1">Welcome back, here's your overview</p>
    </div>
    <div class="flex gap-3">
      <button class="btn variant-ghost-surface">
        <span>📊</span>
        <span>View Reports</span>
      </button>
      <button class="btn variant-filled-primary">
        <span>+</span>
        <span>Add Monitor</span>
      </button>
    </div>
  </div>

  <!-- Stats Grid - Modern Cards -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <!-- Overall Uptime -->
    <div class="card preset-filled-surface-50-950 p-6 border border-surface-200-800 hover:shadow-xl transition-all duration-300 group">
      <div class="flex items-start justify-between mb-4">
        <div class="p-3 bg-primary-500/10 rounded-xl group-hover:bg-primary-500/20 transition-colors">
          <svg class="w-6 h-6 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
          </svg>
        </div>
        <span class="text-xs font-semibold text-success-500 bg-success-500/10 px-2 py-1 rounded-full">+2.3%</span>
      </div>
      <p class="text-sm font-medium text-surface-600-400 mb-1">Overall Uptime</p>
      <p class="text-3xl font-bold text-primary-500 mb-1">{uptimeStats.overall}%</p>
      <p class="text-xs text-surface-500">Last 30 days</p>
    </div>

    <!-- Active Monitors -->
    <div class="card preset-filled-surface-50-950 p-6 border border-surface-200-800 hover:shadow-xl transition-all duration-300 group">
      <div class="flex items-start justify-between mb-4">
        <div class="p-3 bg-secondary-500/10 rounded-xl group-hover:bg-secondary-500/20 transition-colors">
          <svg class="w-6 h-6 text-secondary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
        </div>
        <span class="text-xs font-semibold text-surface-600-400 bg-surface-200-800 px-2 py-1 rounded-full">{totalMonitors} total</span>
      </div>
      <p class="text-sm font-medium text-surface-600-400 mb-1">Active Monitors</p>
      <p class="text-3xl font-bold mb-1">{activeMonitors}<span class="text-lg text-surface-500">/{totalMonitors}</span></p>
      <p class="text-xs text-surface-500">{totalMonitors - activeMonitors} inactive</p>
    </div>

    <!-- Active Incidents -->
    <div class="card preset-filled-surface-50-950 p-6 border border-surface-200-800 hover:shadow-xl transition-all duration-300 group">
      <div class="flex items-start justify-between mb-4">
        <div class="p-3 {activeIncidents > 0 ? 'bg-error-500/10' : 'bg-success-500/10'} rounded-xl group-hover:{activeIncidents > 0 ? 'bg-error-500/20' : 'bg-success-500/20'} transition-colors">
          <svg class="w-6 h-6 {activeIncidents > 0 ? 'text-error-500' : 'text-success-500'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        {#if activeIncidents > 0}
          <span class="text-xs font-semibold text-error-500 bg-error-500/10 px-2 py-1 rounded-full animate-pulse">Critical</span>
        {:else}
          <span class="text-xs font-semibold text-success-500 bg-success-500/10 px-2 py-1 rounded-full">All Clear</span>
        {/if}
      </div>
      <p class="text-sm font-medium text-surface-600-400 mb-1">Active Incidents</p>
      <p class="text-3xl font-bold {activeIncidents > 0 ? 'text-error-500' : 'text-success-500'} mb-1">
        {activeIncidents}
      </p>
      <p class="text-xs text-surface-500">{activeIncidents > 0 ? 'Requires attention' : 'No issues'}</p>
    </div>

    <!-- Today's Uptime -->
    <div class="card preset-filled-surface-50-950 p-6 border border-surface-200-800 hover:shadow-xl transition-all duration-300 group">
      <div class="flex items-start justify-between mb-4">
        <div class="p-3 bg-success-500/10 rounded-xl group-hover:bg-success-500/20 transition-colors">
          <svg class="w-6 h-6 text-success-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <span class="text-xs font-semibold text-success-500 bg-success-500/10 px-2 py-1 rounded-full">Perfect</span>
      </div>
      <p class="text-sm font-medium text-surface-600-400 mb-1">Today's Uptime</p>
      <p class="text-3xl font-bold text-success-500 mb-1">{uptimeStats.today}%</p>
      <p class="text-xs text-surface-500">All systems operational</p>
    </div>
  </div>

  <!-- Activity Sections -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <!-- Recent Checks - Modern Design -->
    <div class="card preset-filled-surface-50-950 border border-surface-200-800 overflow-hidden">
      <div class="p-6 border-b border-surface-200-800 bg-gradient-to-r from-primary-500/5 to-transparent">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-bold">Recent Checks</h2>
            <p class="text-sm text-surface-600-400 mt-1">Latest monitoring results</p>
          </div>
          <button class="btn btn-sm variant-ghost-primary">View All →</button>
        </div>
      </div>
      <div class="p-6 space-y-3">
        <div class="flex items-center gap-4 p-4 rounded-xl bg-surface-100-900 hover:bg-surface-200-800 transition-colors border border-transparent hover:border-success-500/20">
          <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-success-500/10 flex items-center justify-center">
            <svg class="w-5 h-5 text-success-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-semibold text-sm truncate">api.example.com</p>
            <p class="text-xs text-surface-600-400">HTTP Check • 2 minutes ago</p>
          </div>
          <div class="flex flex-col items-end gap-1">
            <span class="badge variant-soft-success text-xs">200 OK</span>
            <span class="text-xs text-surface-500">142ms</span>
          </div>
        </div>

        <div class="flex items-center gap-4 p-4 rounded-xl bg-surface-100-900 hover:bg-surface-200-800 transition-colors border border-transparent hover:border-success-500/20">
          <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-success-500/10 flex items-center justify-center">
            <svg class="w-5 h-5 text-success-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-semibold text-sm truncate">www.example.com</p>
            <p class="text-xs text-surface-600-400">SSL Check • 3 minutes ago</p>
          </div>
          <div class="flex flex-col items-end gap-1">
            <span class="badge variant-soft-success text-xs">Valid</span>
            <span class="text-xs text-surface-500">89ms</span>
          </div>
        </div>

        <div class="flex items-center gap-4 p-4 rounded-xl bg-surface-100-900 hover:bg-surface-200-800 transition-colors border border-transparent hover:border-warning-500/20">
          <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-warning-500/10 flex items-center justify-center">
            <svg class="w-5 h-5 text-warning-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-semibold text-sm truncate">cdn.example.com</p>
            <p class="text-xs text-surface-600-400">Regional Probe • 5 minutes ago</p>
          </div>
          <div class="flex flex-col items-end gap-1">
            <span class="badge variant-soft-warning text-xs">Slow</span>
            <span class="text-xs text-surface-500">856ms</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Incidents - Modern Design -->
    <div class="card preset-filled-surface-50-950 border border-surface-200-800 overflow-hidden">
      <div class="p-6 border-b border-surface-200-800 {activeIncidents > 0 ? 'bg-gradient-to-r from-error-500/5 to-transparent' : 'bg-gradient-to-r from-success-500/5 to-transparent'}">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-bold">Active Incidents</h2>
            <p class="text-sm text-surface-600-400 mt-1">{activeIncidents > 0 ? 'Requires immediate attention' : 'All systems normal'}</p>
          </div>
          <button class="btn btn-sm variant-ghost-{activeIncidents > 0 ? 'error' : 'success'}">View All →</button>
        </div>
      </div>
      <div class="p-6 space-y-3">
        {#if activeIncidents > 0}
          <div class="p-4 rounded-xl bg-error-500/5 border border-error-500/20 hover:border-error-500/40 transition-colors">
            <div class="flex items-start gap-3 mb-3">
              <div class="flex-shrink-0 w-8 h-8 rounded-lg bg-error-500/10 flex items-center justify-center animate-pulse">
                <svg class="w-4 h-4 text-error-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-2">
                  <p class="font-semibold">Payment Gateway Timeout</p>
                  <span class="badge variant-filled-error text-xs">Critical</span>
                </div>
                <p class="text-sm text-surface-600-400 mb-2">Started 15 minutes ago</p>
                <div class="flex items-center gap-2 text-xs text-surface-500">
                  <span class="flex items-center gap-1">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    15m downtime
                  </span>
                  <span>•</span>
                  <span>23 failed checks</span>
                </div>
              </div>
            </div>
            <button class="btn btn-sm variant-filled-error w-full">Acknowledge & Investigate</button>
          </div>

          <div class="p-4 rounded-xl bg-warning-500/5 border border-warning-500/20 hover:border-warning-500/40 transition-colors">
            <div class="flex items-start gap-3 mb-3">
              <div class="flex-shrink-0 w-8 h-8 rounded-lg bg-warning-500/10 flex items-center justify-center">
                <svg class="w-4 h-4 text-warning-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-2">
                  <p class="font-semibold">EU Region Latency</p>
                  <span class="badge variant-filled-warning text-xs">Warning</span>
                </div>
                <p class="text-sm text-surface-600-400 mb-2">Started 2 hours ago</p>
                <div class="flex items-center gap-2 text-xs text-surface-500">
                  <span class="flex items-center gap-1">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                    </svg>
                    Avg 856ms
                  </span>
                  <span>•</span>
                  <span>48 slow responses</span>
                </div>
              </div>
            </div>
            <button class="btn btn-sm variant-soft-warning w-full">View Details</button>
          </div>
        {:else}
          <div class="flex flex-col items-center justify-center py-12">
            <div class="w-16 h-16 rounded-full bg-success-500/10 flex items-center justify-center mb-4">
              <svg class="w-8 h-8 text-success-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <p class="text-lg font-semibold mb-1">All Systems Operational</p>
            <p class="text-sm text-surface-600-400">No active incidents to display</p>
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>
