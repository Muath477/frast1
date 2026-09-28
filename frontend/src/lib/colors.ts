import type { Health } from './types';

export const STATUS_COLOR: Record<Health, string> = {
  healthy: '#22c55e',
  warning: '#eab308',
  degraded: '#f97316',
  critical: '#ef4444',
  unknown: '#64748b',
};

export const CAUSE_COLOR = '#ef4444';
export const IMPACT_COLOR = '#f59e0b';
export const BACKUP_COLOR = '#38bdf8';
