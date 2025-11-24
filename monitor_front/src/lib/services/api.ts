// API Service Layer
// This will be used to communicate with the FastAPI backend

import { ACCESS_COOKIE, REFRESH_COOKIE } from '../constants/auth';
import { deleteCookie, getCookie } from '../utils/cookies';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface RequestOptions {
  method?: string;
  headers?: Record<string, string>;
  body?: any;
}

async function apiRequest<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const token = getCookie(ACCESS_COOKIE);

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config: RequestInit = {
    method: options.method || 'GET',
    headers,
  };

  if (options.body) {
    config.body = JSON.stringify(options.body);
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  if (!response.ok) {
    if (response.status === 401) {
      // Handle unauthorized - clear token and redirect to login
      deleteCookie(ACCESS_COOKIE);
      deleteCookie(REFRESH_COOKIE);
      window.location.href = '/#/login';
    }
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}

// Auth API
export const authApi = {
  register: (email: string, password: string, role: 'admin' | 'maintainer' | 'viewer' = 'viewer') =>
    apiRequest('/api/auth/register', {
      method: 'POST',
      body: { email, password, role },
    }),
  login: (email: string, password: string) =>
    apiRequest<{ user: any; access_token: string; refresh_token: string }>('/api/auth/login', {
      method: 'POST',
      body: { email, password },
    }),

  logout: () => apiRequest('/api/auth/logout', { method: 'POST' }),

  refreshToken: () =>
    apiRequest<{ access_token: string; refresh_token: string }>('/api/auth/refresh', {
      method: 'POST',
      body: { refresh_token: getCookie(REFRESH_COOKIE) },
    }),

  me: () => apiRequest<any>('/api/auth/me'),
};

// Monitors API
export const monitorsApi = {
  getAll: () => apiRequest<any[]>('/api/monitors/'),

  getById: (id: string) => apiRequest<any>(`/api/monitors/${id}`),

  create: (data: any) =>
    apiRequest<any>('/api/monitors/', {
      method: 'POST',
      body: data,
    }),

  update: (id: string, data: any) =>
    apiRequest<any>(`/api/monitors/${id}`, {
      method: 'PUT',
      body: data,
    }),

  delete: (id: string) =>
    apiRequest(`/api/monitors/${id}`, {
      method: 'DELETE',
    }),
};

// Checks API
export const checksApi = {
  getByMonitor: (monitorId: string) => apiRequest<any[]>(`/api/checks?monitor_id=${monitorId}`),

  getRecent: (limit: number = 10) => apiRequest<any[]>(`/api/checks/recent?limit=${limit}`),
};

// Incidents API
export const incidentsApi = {
  getAll: () => apiRequest<any[]>('/api/incidents/'),

  getById: (id: string) => apiRequest<any>(`/api/incidents/${id}`),

  acknowledge: (id: string) =>
    apiRequest(`/api/incidents/${id}/acknowledge`, {
      method: 'POST',
    }),

  resolve: (id: string) =>
    apiRequest(`/api/incidents/${id}/resolve`, {
      method: 'POST',
    }),
};

// Analytics API
export const analyticsApi = {
  getUptime: (monitorId?: string) => {
    const query = monitorId ? `?monitor_id=${monitorId}` : '';
    return apiRequest<any>(`/api/analytics/uptime${query}`);
  },

  getResponseTimes: (monitorId?: string) => {
    const query = monitorId ? `?monitor_id=${monitorId}` : '';
    return apiRequest<any>(`/api/analytics/response-times${query}`);
  },
};

// Settings/Configuration API
export const settingsApi = {
  get: () => apiRequest<any>('/api/settings'),

  update: (data: any) =>
    apiRequest<any>('/api/settings', {
      method: 'PUT',
      body: data,
    }),

  testWebhook: (url?: string) =>
    apiRequest('/api/settings/webhook/test', {
      method: 'POST',
      body: { url },
    }),

  getEscalationRules: () => apiRequest<any[]>('/api/settings/escalations'),

  createEscalationRule: (data: any) =>
    apiRequest<any>('/api/settings/escalations', {
      method: 'POST',
      body: data,
    }),

  updateEscalationRule: (id: number, data: any) =>
    apiRequest<any>(`/api/settings/escalations/${id}`, {
      method: 'PUT',
      body: data,
    }),

  deleteEscalationRule: (id: number) =>
    apiRequest(`/api/settings/escalations/${id}`, {
      method: 'DELETE',
    }),

  // Webhooks
  getWebhooks: () => apiRequest<any[]>('/api/webhooks'),

  createWebhook: (data: any) =>
    apiRequest<any>('/api/webhooks', {
      method: 'POST',
      body: data,
    }),

  deleteWebhook: (id: string) =>
    apiRequest(`/api/webhooks/${id}`, {
      method: 'DELETE',
    }),
};

// Security API
export interface SecurityAuditResponse {
  id: number;
  monitor_id: number;
  status: 'pass' | 'warning' | 'critical';
  created_at: string;
  findings: Record<string, any>;
}

export const securityApi = {
  runMonitorSecurityCheck: (monitorId: number) =>
    apiRequest<SecurityAuditResponse>(`/api/checks/security/monitors/${monitorId}`, {
      method: 'POST',
    }),
  latestMonitorSecurityCheck: (monitorId: number) =>
    apiRequest<SecurityAuditResponse | null>(
      `/api/checks/security/monitors/${monitorId}/latest`
    ),
  listMonitorSecurityAudits: (monitorId: number, params?: { limit?: number; offset?: number }) => {
    const query = new URLSearchParams();
    if (params?.limit) query.set('limit', params.limit.toString());
    if (params?.offset) query.set('offset', params.offset.toString());
    const suffix = query.toString() ? `?${query.toString()}` : '';
    return apiRequest<SecurityAuditResponse[]>(`/api/checks/security/monitors/${monitorId}/audits${suffix}`);
  },
};

export default {
  auth: authApi,
  monitors: monitorsApi,
  checks: checksApi,
  incidents: incidentsApi,
  analytics: analyticsApi,
  settings: settingsApi,
  security: securityApi,
};
