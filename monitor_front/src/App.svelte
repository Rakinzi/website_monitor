<script lang="ts">
  import Router, { replace, location } from 'svelte-spa-router';
  import { wrap } from 'svelte-spa-router/wrap';
  import { authStore } from './stores/authStore';
  import { themeStore } from './stores/themeStore';
  import { onMount } from 'svelte';

  import DashboardLayout from './lib/layouts/DashboardLayout.svelte';
  import Dashboard from './routes/Dashboard.svelte';
  import Monitors from './routes/Monitors.svelte';
  import MonitorDetail from './routes/MonitorDetail.svelte';
  import Incidents from './routes/Incidents.svelte';
  import Settings from './routes/Settings.svelte';
import Login from './routes/Login.svelte';
import Register from './routes/Register.svelte';
  import Test from './routes/Test.svelte';



  let isAuthenticated = $state(false);

  authStore.subscribe((state) => {
    isAuthenticated = state.isAuthenticated;
  });

  onMount(() => {
    authStore.initialize();
    themeStore.init();
  });

  $effect(() => {
    if (typeof window === 'undefined') return;
    if ($location === '/login' || $location === '/register') {
      document.body.classList.add('no-scroll');
    } else {
      document.body.classList.remove('no-scroll');
    }
  });

  // Protected route wrapper
  function protectedRoute(component: any) {
    return wrap({
      component,
      conditions: [
        () => {
          if (!isAuthenticated) {
            replace('/login');
            return false;
          }
          return true;
        },
      ],
    });
  }

  // Route definitions
  const routes = {
    '/': protectedRoute(Dashboard),
    '/monitors': protectedRoute(Monitors),
    '/monitors/:id': protectedRoute(MonitorDetail),
    '/incidents': protectedRoute(Incidents),
    '/incidents/:id': protectedRoute(Incidents), // Will create detail page later
    '/settings': protectedRoute(Settings),
    '/test': protectedRoute(Test),
    '/login': Login,
    '/register': Register,
  };

  // Conditional layout wrapper
  function conditionalLayout(routeLoaded: any) {
    if (isAuthenticated && routeLoaded.route !== '/login' && routeLoaded.route !== '/register') {
      return {
        component: DashboardLayout,
      };
    }
    return null;
  }
</script>

{#if isAuthenticated && $authStore.user}
  <DashboardLayout>
    <Router {routes} />
  </DashboardLayout>
{:else}
  <Router {routes} />
{/if}
