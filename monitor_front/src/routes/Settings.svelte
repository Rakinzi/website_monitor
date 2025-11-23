<script lang="ts">

  let emailNotifications = true;
  let slackNotifications = false;
  let pushNotifications = true;
  let webhookUrl = 'https://hooks.example.com/webhook';
  let checkInterval = 60;
  let retryAttempts = 3;
  let timeout = 30;
  let sslVerification = true;
  let followRedirects = true;

  const escalationRules = [
    {
      id: '1',
      name: 'Critical Incidents → #ops-team',
      description: 'Immediate notification for all critical incidents',
      severity: 'critical',
      channel: '#ops-team',
    },
    {
      id: '2',
      name: 'Warning Alerts → #monitoring',
      description: 'Send warnings to monitoring channel',
      severity: 'warning',
      channel: '#monitoring',
    },
  ];

  function handleSave() {
    alert('Settings saved successfully!');
  }
</script>

<div class="p-8 space-y-8 bg-gradient-to-br from-surface-50 to-surface-100 dark:from-surface-950 dark:to-surface-900 min-h-screen">
  <!-- Header -->
  <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
    <div>
      <h1 class="text-4xl font-bold bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent">
        Settings
      </h1>
      <p class="text-surface-600-400 mt-1">Configure monitoring preferences and notifications</p>
    </div>
    <div class="flex gap-3">
      <button class="btn variant-ghost-surface">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
        <span>Reset to Defaults</span>
      </button>
      <button class="btn variant-filled-primary shadow-lg shadow-primary-500/20" onclick={handleSave}>
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        <span>Save Settings</span>
      </button>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <!-- Notifications Card -->
    <div class="card preset-filled-surface-50-950 border border-surface-200-800 p-6 hover:shadow-xl transition-shadow">
      <div class="flex items-center gap-3 mb-6">
        <div class="p-3 rounded-lg bg-gradient-to-br from-primary-500 to-secondary-500">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
          </svg>
        </div>
        <div>
          <h2 class="text-xl font-bold">Notifications</h2>
          <p class="text-sm text-surface-600-400">Manage alert preferences</p>
        </div>
      </div>
      <div class="space-y-5">
        <div class="flex items-center justify-between p-4 rounded-lg bg-surface-100-900 border border-surface-200-800">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            <div>
              <p class="font-semibold">Email Notifications</p>
              <p class="text-xs text-surface-600-400">Receive alerts via email</p>
            </div>
          </div>
          <input type="checkbox" class="checkbox" bind:checked={emailNotifications} />
        </div>

        <div class="flex items-center justify-between p-4 rounded-lg bg-surface-100-900 border border-surface-200-800">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-secondary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
            <div>
              <p class="font-semibold">Slack Notifications</p>
              <p class="text-xs text-surface-600-400">Send alerts to Slack</p>
            </div>
          </div>
          <input type="checkbox" class="checkbox" bind:checked={slackNotifications} />
        </div>

        <div class="flex items-center justify-between p-4 rounded-lg bg-surface-100-900 border border-surface-200-800">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-tertiary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/>
            </svg>
            <div>
              <p class="font-semibold">Push Notifications</p>
              <p class="text-xs text-surface-600-400">Browser push alerts</p>
            </div>
          </div>
          <input type="checkbox" class="checkbox" bind:checked={pushNotifications} />
        </div>

        <div>
          <label class="label mb-2" for="email-address">
            <span class="font-semibold">Email Address</span>
          </label>
          <input
            id="email-address"
            type="email"
            class="input variant-form-material"
            placeholder="admin@example.com"
            value="admin@example.com"
          />
        </div>
      </div>
    </div>

    <!-- Webhooks Card -->
    <div class="card preset-filled-surface-50-950 border border-surface-200-800 p-6 hover:shadow-xl transition-shadow">
      <div class="flex items-center gap-3 mb-6">
        <div class="p-3 rounded-lg bg-gradient-to-br from-secondary-500 to-tertiary-500">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
          </svg>
        </div>
        <div>
          <h2 class="text-xl font-bold">Webhooks</h2>
          <p class="text-sm text-surface-600-400">Configure webhook endpoints</p>
        </div>
      </div>
      <div class="space-y-4">
        <div>
          <label class="label mb-2" for="webhook-url">
            <span class="font-semibold">Webhook URL</span>
          </label>
          <input
            id="webhook-url"
            type="url"
            class="input variant-form-material"
            placeholder="https://hooks.example.com/webhook"
            bind:value={webhookUrl}
          />
          <p class="text-xs text-surface-600-400 mt-1">Receive incident notifications via webhook</p>
        </div>
        <button class="btn variant-filled-secondary w-full shadow-lg shadow-secondary-500/20">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          Test Webhook
        </button>
      </div>
    </div>

    <!-- Check Settings Card -->
    <div class="card preset-filled-surface-50-950 border border-surface-200-800 p-6 hover:shadow-xl transition-shadow">
      <div class="flex items-center gap-3 mb-6">
        <div class="p-3 rounded-lg bg-gradient-to-br from-tertiary-500 to-primary-500">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <h2 class="text-xl font-bold">Check Settings</h2>
          <p class="text-sm text-surface-600-400">Configure monitoring intervals</p>
        </div>
      </div>
      <div class="space-y-4">
        <div>
          <label class="label mb-2" for="check-interval">
            <span class="font-semibold">Check Interval (seconds)</span>
          </label>
          <input
            id="check-interval"
            type="number"
            class="input variant-form-material"
            min="10"
            max="3600"
            bind:value={checkInterval}
          />
          <p class="text-xs text-surface-600-400 mt-1">How often to check monitor status</p>
        </div>
        <div>
          <label class="label mb-2" for="retry-attempts">
            <span class="font-semibold">Retry Attempts</span>
          </label>
          <input
            id="retry-attempts"
            type="number"
            class="input variant-form-material"
            min="1"
            max="10"
            bind:value={retryAttempts}
          />
          <p class="text-xs text-surface-600-400 mt-1">Number of retries before marking as down</p>
        </div>
        <div>
          <label class="label mb-2" for="timeout">
            <span class="font-semibold">Timeout (seconds)</span>
          </label>
          <input
            id="timeout"
            type="number"
            class="input variant-form-material"
            min="5"
            max="120"
            bind:value={timeout}
          />
          <p class="text-xs text-surface-600-400 mt-1">Maximum wait time for response</p>
        </div>
      </div>
    </div>

    <!-- Advanced Settings Card -->
    <div class="card preset-filled-surface-50-950 border border-surface-200-800 p-6 hover:shadow-xl transition-shadow">
      <div class="flex items-center gap-3 mb-6">
        <div class="p-3 rounded-lg bg-gradient-to-br from-warning-500 to-error-500">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
        </div>
        <div>
          <h2 class="text-xl font-bold">Advanced Settings</h2>
          <p class="text-sm text-surface-600-400">Fine-tune monitoring behavior</p>
        </div>
      </div>
      <div class="space-y-5">
        <div class="flex items-center justify-between p-4 rounded-lg bg-surface-100-900 border border-surface-200-800">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-success-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
            <div>
              <p class="font-semibold">SSL Verification</p>
              <p class="text-xs text-surface-600-400">Verify SSL certificates</p>
            </div>
          </div>
          <input type="checkbox" class="checkbox" bind:checked={sslVerification} />
        </div>

        <div class="flex items-center justify-between p-4 rounded-lg bg-surface-100-900 border border-surface-200-800">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 9l3 3m0 0l-3 3m3-3H8m13 0a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <div>
              <p class="font-semibold">Follow Redirects</p>
              <p class="text-xs text-surface-600-400">Auto-follow HTTP redirects</p>
            </div>
          </div>
          <input type="checkbox" class="checkbox" bind:checked={followRedirects} />
        </div>
      </div>
    </div>
  </div>

  <!-- Escalation Rules Section -->
  <div class="card preset-filled-surface-50-950 border border-surface-200-800 p-6 hover:shadow-xl transition-shadow">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-3">
        <div class="p-3 rounded-lg bg-gradient-to-br from-error-500 to-warning-500">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <div>
          <h2 class="text-xl font-bold">Escalation Rules</h2>
          <p class="text-sm text-surface-600-400">Configure incident escalation workflows</p>
        </div>
      </div>
      <button class="btn variant-filled-primary shadow-lg shadow-primary-500/20">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        <span>Add Rule</span>
      </button>
    </div>

    <div class="space-y-3">
      {#each escalationRules as rule}
        <div class="p-5 rounded-lg bg-surface-100-900 border border-surface-200-800 hover:border-primary-500 transition-colors group">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4 flex-1">
              <span class="badge variant-filled-{rule.severity === 'critical' ? 'error' : 'warning'} text-xs font-semibold uppercase">
                {rule.severity}
              </span>
              <div class="flex-1">
                <p class="font-semibold text-lg group-hover:text-primary-500 transition-colors">{rule.name}</p>
                <p class="text-sm text-surface-600-400 mt-1">{rule.description}</p>
              </div>
            </div>
            <div class="flex gap-2">
              <button class="btn variant-ghost-surface btn-sm">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
                Edit
              </button>
              <button class="btn variant-ghost-error btn-sm">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
                Delete
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>
