// API Service Layer
// This will be used to communicate with the FastAPI backend

import { ACCESS_COOKIE, REFRESH_COOKIE } from '../constants/auth';
import { deleteCookie, getCookie } from '../utils/cookies';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

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
  login: (email: string, password: string) =>
    apiRequest<{ user: any; access_token: string; refresh_token: string }>('/auth/login', {
      method: 'POST',
      body: { email, password },
    }),

  logout: () => apiRequest('/auth/logout', { method: 'POST' }),

  refreshToken: () =>
    apiRequest<{ access_token: string; refresh_token: string }>('/auth/refresh', {
      method: 'POST',
      body: { refresh_token: getCookie(REFRESH_COOKIE) },
    }),

  me: () => apiRequest<any>('/auth/me'),
};

// Monitors API
export const monitorsApi = {
  getAll: () => apiRequest<any[]>('/monitors'),

  getById: (id: string) => apiRequest<any>(`/monitors/${id}`),

  create: (data: any) =>
    apiRequest<any>('/monitors', {
      method: 'POST',
      body: data,
    }),

  update: (id: string, data: any) =>
    apiRequest<any>(`/monitors/${id}`, {
      method: 'PUT',
      body: data,
    }),

  delete: (id: string) =>
    apiRequest(`/monitors/${id}`, {
      method: 'DELETE',
    }),
};

// Checks API
export const checksApi = {
  getByMonitor: (monitorId: string) => apiRequest<any[]>(`/checks?monitor_id=${monitorId}`),

  getRecent: (limit: number = 10) => apiRequest<any[]>(`/checks/recent?limit=${limit}`),
};

// Incidents API
export const incidentsApi = {
  getAll: () => apiRequest<any[]>('/incidents'),

  getById: (id: string) => apiRequest<any>(`/incidents/${id}`),

  acknowledge: (id: string) =>
    apiRequest(`/incidents/${id}/acknowledge`, {
      method: 'POST',
    }),

  resolve: (id: string) =>
    apiRequest(`/incidents/${id}/resolve`, {
      method: 'POST',
    }),
};

// Analytics API
export const analyticsApi = {
  getUptime: (monitorId?: string) => {
    const query = monitorId ? `?monitor_id=${monitorId}` : '';
    return apiRequest<any>(`/analytics/uptime${query}`);
  },

  getResponseTimes: (monitorId?: string) => {
    const query = monitorId ? `?monitor_id=${monitorId}` : '';
    return apiRequest<any>(`/analytics/response-times${query}`);
  },
};

// Settings/Configuration API
export const settingsApi = {
  get: () => apiRequest<any>('/settings'),

  update: (data: any) =>
    apiRequest<any>('/settings', {
      method: 'PUT',
      body: data,
    }),

  // Webhooks
  getWebhooks: () => apiRequest<any[]>('/webhooks'),

  createWebhook: (data: any) =>
    apiRequest<any>('/webhooks', {
      method: 'POST',
      body: data,
    }),

  deleteWebhook: (id: string) =>
    apiRequest(`/webhooks/${id}`, {
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
    apiRequest<SecurityAuditResponse>(`/checks/security/monitors/${monitorId}`, {
      method: 'POST',
    }),
  latestMonitorSecurityCheck: (monitorId: number) =>
    apiRequest<SecurityAuditResponse>(`/checks/security/monitors/${monitorId}/latest`),
  listMonitorSecurityAudits: (monitorId: number, params?: { limit?: number; offset?: number }) => {
    const query = new URLSearchParams();
    if (params?.limit) query.set('limit', params.limit.toString());
    if (params?.offset) query.set('offset', params.offset.toString());
    const suffix = query.toString() ? `?${query.toString()}` : '';
    return apiRequest<SecurityAuditResponse[]>(`/checks/security/monitors/${monitorId}/audits${suffix}`);
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
