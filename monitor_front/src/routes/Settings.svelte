<script lang="ts">
  import { onMount } from 'svelte';
  import { settingsApi } from '../lib/services/api';

  let emailNotifications = $state(false);
  let slackNotifications = $state(false);
  let pushNotifications = $state(false);
  let webhookUrl = $state('');
  let checkInterval = $state(60);
  let retryAttempts = $state(3);
  let timeout = $state(30);
  let sslVerification = $state(true);
  let followRedirects = $state(true);
  let emailAddress = $state('');

  let escalationRules = $state<any[]>([]);
  let isLoading = $state(true);
  let isSaving = $state(false);
  let error = $state('');
  let successMessage = $state('');

  onMount(async () => {
    await Promise.all([loadSettings(), loadEscalationRules()]);
  });

  async function loadSettings() {
    isLoading = true;
    error = '';
    try {
      const settings = await settingsApi.get();

      // Update all settings from API response
      if (settings) {
        emailNotifications = settings.emailNotifications ?? false;
        slackNotifications = settings.slackNotifications ?? false;
        pushNotifications = settings.pushNotifications ?? false;
        webhookUrl = settings.webhookUrl ?? '';
        checkInterval = settings.checkInterval ?? 60;
        retryAttempts = settings.retryAttempts ?? 3;
        timeout = settings.timeout ?? 30;
        sslVerification = settings.sslVerification ?? true;
        followRedirects = settings.followRedirects ?? true;
        emailAddress = settings.emailAddress ?? '';
      }
    } catch (err: any) {
      error = err?.message || 'Failed to load settings';
    } finally {
      isLoading = false;
    }
  }

  async function loadEscalationRules() {
    try {
      const rules = await settingsApi.getEscalationRules();
      escalationRules = rules.map((rule) => ({
        id: rule.id,
        name: rule.name,
        severity: rule.rules?.severity || 'info',
        description: rule.rules?.description || '',
      }));
    } catch (err: any) {
      console.error('Failed to load escalation rules:', err);
    }
  }

  async function handleSave() {
    isSaving = true;
    error = '';
    successMessage = '';

    try {
      await settingsApi.update({
        emailNotifications,
        slackNotifications,
        pushNotifications,
        webhookUrl,
        checkInterval,
        retryAttempts,
        timeout,
        sslVerification,
        followRedirects,
        emailAddress,
      });

      successMessage = 'Settings saved successfully!';
      setTimeout(() => { successMessage = ''; }, 3000);
    } catch (err: any) {
      error = err?.message || 'Failed to save settings';
    } finally {
      isSaving = false;
    }
  }

  async function handleReset() {
    if (confirm('Are you sure you want to reset all settings to defaults?')) {
      await loadSettings();
    }
  }

  async function handleTestWebhook() {
    try {
      await settingsApi.testWebhook(webhookUrl || undefined);
      successMessage = 'Webhook test sent!';
      setTimeout(() => (successMessage = ''), 3000);
    } catch (err: any) {
      error = err?.message || 'Failed to test webhook';
    }
  }

  async function handleAddRule() {
    const name = prompt('Rule name?');
    if (!name) return;
    const severity = prompt('Severity (info/warning/critical)?', 'info') || 'info';
    const description = prompt('Description?', '') || '';
    const newRule = await settingsApi.createEscalationRule({
      name,
      rules: { severity, description },
    });
    escalationRules = [
      ...escalationRules,
      {
        id: newRule.id,
        name: newRule.name,
        severity,
        description,
      },
    ];
  }

  async function handleDeleteRule(id: number) {
    if (!confirm('Delete this escalation rule?')) return;
    await settingsApi.deleteEscalationRule(id);
    escalationRules = escalationRules.filter((rule) => rule.id !== id);
  }
</script>

<div class="p-6 space-y-6">
  <!-- Header -->
  <div class="flex justify-between items-center">
    <h1 class="text-2xl font-bold text-black dark:text-white">Settings</h1>
    <div class="flex gap-2">
      <button
        class="btn btn-sm bg-gray-200 dark:bg-neutral-800 hover:bg-gray-300 dark:hover:bg-neutral-700 text-black dark:text-white"
        onclick={handleReset}
        disabled={isLoading || isSaving}
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
        <span>Reset</span>
      </button>
      <button
        class="btn btn-sm bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200"
        onclick={handleSave}
        disabled={isLoading || isSaving}
      >
        {#if isSaving}
          <div class="w-4 h-4 border-2 border-white dark:border-black border-t-transparent rounded-full animate-spin"></div>
        {:else}
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        {/if}
        <span>{isSaving ? 'Saving...' : 'Save Settings'}</span>
      </button>
    </div>
  </div>

  <!-- Success/Error Messages -->
  {#if successMessage}
    <div class="p-4 border border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-950 rounded text-green-600 dark:text-green-400">
      {successMessage}
    </div>
  {/if}
  {#if error}
    <div class="p-4 border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950 rounded text-red-600 dark:text-red-400">
      {error}
    </div>
  {/if}

  {#if isLoading}
    <div class="text-center py-12 text-gray-600 dark:text-gray-400">
      <div class="w-8 h-8 border-2 border-black dark:border-white border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
      Loading settings...
    </div>
  {:else}

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
    <!-- Notifications Card -->
    <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-6">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 rounded-lg bg-black dark:bg-white flex items-center justify-center shrink-0">
          <svg class="w-5 h-5 text-white dark:text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
          </svg>
        </div>
        <div>
          <h2 class="text-lg font-bold text-black dark:text-white">Notifications</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Manage alert preferences</p>
        </div>
      </div>
      <div class="space-y-4">
        <div class="flex items-center justify-between p-4 rounded-lg bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            <div>
              <p class="font-semibold text-black dark:text-white">Email Notifications</p>
              <p class="text-xs text-gray-600 dark:text-gray-400">Receive alerts via email</p>
            </div>
          </div>
          <input type="checkbox" class="w-4 h-4 rounded border-gray-300 dark:border-neutral-700" bind:checked={emailNotifications} />
        </div>

        <div class="flex items-center justify-between p-4 rounded-lg bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
            <div>
              <p class="font-semibold text-black dark:text-white">Slack Notifications</p>
              <p class="text-xs text-gray-600 dark:text-gray-400">Send alerts to Slack</p>
            </div>
          </div>
          <input type="checkbox" class="w-4 h-4 rounded border-gray-300 dark:border-neutral-700" bind:checked={slackNotifications} />
        </div>

        <div class="flex items-center justify-between p-4 rounded-lg bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/>
            </svg>
            <div>
              <p class="font-semibold text-black dark:text-white">Push Notifications</p>
              <p class="text-xs text-gray-600 dark:text-gray-400">Browser push alerts</p>
            </div>
          </div>
          <input type="checkbox" class="w-4 h-4 rounded border-gray-300 dark:border-neutral-700" bind:checked={pushNotifications} />
        </div>

        <div>
          <label class="label mb-2" for="email-address">
            <span class="font-semibold text-black dark:text-white">Email Address</span>
          </label>
          <input
            id="email-address"
            type="email"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-black dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white"
            placeholder="admin@example.com"
            bind:value={emailAddress}
          />
        </div>
      </div>
    </div>

    <!-- Webhooks Card -->
    <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-6">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 rounded-lg bg-black dark:bg-white flex items-center justify-center shrink-0">
          <svg class="w-5 h-5 text-white dark:text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
          </svg>
        </div>
        <div>
          <h2 class="text-lg font-bold text-black dark:text-white">Webhooks</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Configure webhook endpoints</p>
        </div>
      </div>
      <div class="space-y-4">
        <div>
          <label class="label mb-2" for="webhook-url">
            <span class="font-semibold text-black dark:text-white">Webhook URL</span>
          </label>
          <input
            id="webhook-url"
            type="url"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-black dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white"
            placeholder="https://hooks.example.com/webhook"
            bind:value={webhookUrl}
          />
          <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">Receive incident notifications via webhook</p>
        </div>
        <button
          class="btn btn-sm bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200 w-full"
          onclick={handleTestWebhook}
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          Test Webhook
        </button>
      </div>
    </div>

    <!-- Check Settings Card -->
    <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-6">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 rounded-lg bg-black dark:bg-white flex items-center justify-center shrink-0">
          <svg class="w-5 h-5 text-white dark:text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <h2 class="text-lg font-bold text-black dark:text-white">Check Settings</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Configure monitoring intervals</p>
        </div>
      </div>
      <div class="space-y-4">
        <div>
          <label class="label mb-2" for="check-interval">
            <span class="font-semibold text-black dark:text-white">Check Interval (seconds)</span>
          </label>
          <input
            id="check-interval"
            type="number"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-black dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white"
            min="10"
            max="3600"
            bind:value={checkInterval}
          />
          <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">How often to check monitor status</p>
        </div>
        <div>
          <label class="label mb-2" for="retry-attempts">
            <span class="font-semibold text-black dark:text-white">Retry Attempts</span>
          </label>
          <input
            id="retry-attempts"
            type="number"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-black dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white"
            min="1"
            max="10"
            bind:value={retryAttempts}
          />
          <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">Number of retries before marking as down</p>
        </div>
        <div>
          <label class="label mb-2" for="timeout">
            <span class="font-semibold text-black dark:text-white">Timeout (seconds)</span>
          </label>
          <input
            id="timeout"
            type="number"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-black dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white"
            min="5"
            max="120"
            bind:value={timeout}
          />
          <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">Maximum wait time for response</p>
        </div>
      </div>
    </div>

    <!-- Advanced Settings Card -->
    <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-6">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 rounded-lg bg-black dark:bg-white flex items-center justify-center shrink-0">
          <svg class="w-5 h-5 text-white dark:text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
        </div>
        <div>
          <h2 class="text-lg font-bold text-black dark:text-white">Advanced Settings</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Fine-tune monitoring behavior</p>
        </div>
      </div>
      <div class="space-y-4">
        <div class="flex items-center justify-between p-4 rounded-lg bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
            <div>
              <p class="font-semibold text-black dark:text-white">SSL Verification</p>
              <p class="text-xs text-gray-600 dark:text-gray-400">Verify SSL certificates</p>
            </div>
          </div>
          <input type="checkbox" class="w-4 h-4 rounded border-gray-300 dark:border-neutral-700" bind:checked={sslVerification} />
        </div>

        <div class="flex items-center justify-between p-4 rounded-lg bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-black dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 9l3 3m0 0l-3 3m3-3H8m13 0a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <div>
              <p class="font-semibold text-black dark:text-white">Follow Redirects</p>
              <p class="text-xs text-gray-600 dark:text-gray-400">Auto-follow HTTP redirects</p>
            </div>
          </div>
          <input type="checkbox" class="w-4 h-4 rounded border-gray-300 dark:border-neutral-700" bind:checked={followRedirects} />
        </div>
      </div>
    </div>
  </div>

  <!-- Escalation Rules Section -->
  <div class="card bg-white dark:bg-neutral-950 border border-gray-200 dark:border-neutral-800 p-6">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-black dark:bg-white flex items-center justify-center shrink-0">
          <svg class="w-5 h-5 text-white dark:text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <div>
          <h2 class="text-lg font-bold text-black dark:text-white">Escalation Rules</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Configure incident escalation workflows</p>
        </div>
      </div>
      <button class="btn btn-sm bg-black dark:bg-white text-white dark:text-black hover:bg-gray-800 dark:hover:bg-gray-200" onclick={handleAddRule}>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        <span>Add Rule</span>
      </button>
    </div>

    <div class="space-y-3">
      {#each escalationRules as rule}
        <div class="p-5 rounded-lg bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4 flex-1">
              <span class="px-3 py-1 rounded bg-black dark:bg-white text-white dark:text-black text-xs font-semibold uppercase">
                {rule.severity}
              </span>
              <div class="flex-1">
                <p class="font-semibold text-black dark:text-white">{rule.name}</p>
                <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">{rule.description}</p>
              </div>
            </div>
            <div class="flex gap-2">
              <button class="btn btn-sm bg-gray-200 dark:bg-neutral-800 hover:bg-gray-300 dark:hover:bg-neutral-700 text-black dark:text-white">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
                Edit
              </button>
              <button class="btn btn-sm bg-gray-200 dark:bg-neutral-800 hover:bg-gray-300 dark:hover:bg-neutral-700 text-black dark:text-white" onclick={() => handleDeleteRule(rule.id)}>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
                Delete
              </button>
            </div>
          </div>
        </div>
      {/each}

      {#if escalationRules.length === 0}
        <div class="p-8 text-center text-gray-600 dark:text-gray-400">
          <p>No escalation rules configured yet.</p>
          <p class="text-sm mt-2">Click "Add Rule" to create your first escalation rule.</p>
        </div>
      {/if}
    </div>
  </div>
  {/if}
</div>
