import { useEffect } from 'react';
import { connectOps } from '@/lib/ws';
import { useOps } from '@/store/useOps';

export function useOpsSocket() {
  useEffect(() => connectOps(useOps.getState().apply, useOps.getState().setWs), []);
}
