import type { DemoState, Incident, Topology } from './types';

async function j<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const res = await fetch(input, {
    headers: { 'content-type': 'application/json' },
    ...init,
  });
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json() as Promise<T>;
}

export type Scenario = 'uplink-congestion' | 'dns-failure' | 'server-spike';

export const api = {
  topology: () => j<Topology>('/api/topology'),
  saveLayout: (positions: Record<string, { x: number; y: number }>) =>
    j('/api/topology/layout', { method: 'PUT', body: JSON.stringify({ positions }) }),
  linkMetrics: (id: string) =>
    j<Record<string, [number, number][]>>(`/api/links/${id}/metrics?minutes=5`),
  incidents: () => j<Incident[]>('/api/incidents'),
  inject: (s: Scenario) => j<DemoState>(`/api/demo/inject/${s}`, { method: 'POST' }),
  reset: () => j<DemoState>('/api/demo/reset', { method: 'POST' }),
  setMode: (mode: 'live' | 'sim') =>
    j<DemoState>('/api/demo/mode', { method: 'POST', body: JSON.stringify({ mode }) }),
  approve: (actionId: string, decidedBy: string) =>
    j(`/api/actions/${actionId}/approve`, {
      method: 'POST',
      body: JSON.stringify({ decidedBy }),
    }),
  reject: (actionId: string, decidedBy: string, reason: string) =>
    j(`/api/actions/${actionId}/reject`, {
      method: 'POST',
      body: JSON.stringify({ decidedBy, reason }),
    }),
};
