import raw from '@configs/topology.json';
import type { Topology } from './types';

export const staticTopology: Topology = {
  site: raw.site,
  vantage: raw.vantage,
  nodes: raw.nodes.map((n) => ({
    ...n,
    type: n.type as Topology['nodes'][number]['type'],
    interfaces: n.interfaces.map((i) => ({
      ...i,
      side: i.side as Topology['nodes'][number]['interfaces'][number]['side'],
    })),
    status: 'healthy',
    metrics: {},
  })),
  links: raw.links.map((l) => ({
    ...l,
    role: l.role as Topology['links'][number]['role'],
    speedMbps: 1000,
    status: 'healthy',
    utilization: 0,
    latencyMs: 0,
    packetLoss: 0,
  })),
  services: raw.services.map((s) => ({
    ...s,
    status: 'healthy',
    metrics: {},
  })),
};
