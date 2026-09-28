export type Health = 'healthy' | 'warning' | 'degraded' | 'critical' | 'unknown';
export type NodeType = 'router' | 'switch' | 'server' | 'collector';
export type Side = 'top' | 'bottom' | 'left' | 'right';

export interface Iface {
  name: string;
  ifIndex?: number;
  side: Side;
  speedMbps: number;
  description?: string;
  operState?: 'up' | 'down';
  utilization?: number;
}

export interface TopoNode {
  id: string;
  type: NodeType;
  label: string;
  vendor?: string;
  managementIp: string;
  position: { x: number; y: number };
  interfaces: Iface[];
  status: Health;
  metrics: Record<string, number>;
}

export interface TopoLink {
  id: string;
  source: string;
  sourcePort: string;
  target: string;
  targetPort: string;
  role: 'uplink' | 'access' | 'backup';
  speedMbps: number;
  status: Health;
  utilization: number;
  latencyMs: number;
  packetLoss: number;
}

export interface Service {
  id: string;
  label: string;
  host: string;
  port: number;
  dependsOn: string[];
  status: Health;
  metrics: Record<string, number>;
}

export interface Topology {
  site: string;
  vantage: string;
  nodes: TopoNode[];
  links: TopoLink[];
  services: Service[];
}

export type IncidentStatus =
  | 'open'
  | 'investigating'
  | 'recommendation_ready'
  | 'awaiting_approval'
  | 'approved'
  | 'rejected'
  | 'resolved';

export type ScoreKey =
  | 'metric_anomaly'
  | 'dependency_overlap'
  | 'temporal_proximity'
  | 'blast_radius'
  | 'historical_support';

export interface Evidence {
  id: string;
  entityId: string;
  metric: string;
  value: number;
  baseline: number;
  unit: string;
  ts: string;
  text: string;
}

export interface Candidate {
  entityId: string;
  label: string;
  score: number;
  components: Record<ScoreKey, number>;
  evidence: string[];
  suppressedBy?: string | null;
}

export interface Action {
  id: string;
  incidentId: string;
  actionType: string;
  description: string;
  riskLevel: 'low' | 'medium' | 'high';
  approvalStatus: 'pending' | 'approved' | 'rejected' | 'executed' | 'failed';
  decidedBy?: string;
  reason?: string;
  decidedAt?: string;
  executedAt?: string;
}

export interface Incident {
  id: string;
  title: string;
  status: IncidentStatus;
  severity: 'low' | 'medium' | 'high' | 'critical';
  openedAt: string;
  resolvedAt?: string;
  rootCause?: { entityId: string; label: string; confidence: number };
  needsInvestigation: boolean;
  candidates: Candidate[];
  evidence: Evidence[];
  affectedServices: string[];
  causePath: string[];
  impactPath: string[];
  explanation?: { en: string; ar: string; source: 'template' | 'llm' };
  action?: Action;
  rawAlertCount: number;
  timings: {
    injectedAt?: string;
    firstAnomalyAt?: string;
    detectedAt?: string;
    analyzedAt?: string;
    decidedAt?: string;
    executedAt?: string;
    recoveredAt?: string;
  };
}

export interface RawAlert {
  id: string;
  sourceId: string;
  metric: string;
  value: number;
  severity: 'warning' | 'critical';
  ts: string;
}

export interface DemoState {
  mode: 'live' | 'sim';
  scenario: string | null;
  state: 'idle' | 'injected' | 'remediating' | 'recovered';
  injectedAt?: string;
}

export interface Snapshot {
  topology: Topology;
  incidents: Incident[];
  alerts: RawAlert[];
  demo: DemoState;
}

export type WsMessage =
  | { type: 'snapshot'; ts: number; data: Snapshot }
  | { type: 'link'; ts: number; data: Pick<TopoLink, 'id' | 'status' | 'utilization' | 'latencyMs' | 'packetLoss'> }
  | { type: 'node'; ts: number; data: { id: string; status: Health; metrics: Record<string, number> } }
  | { type: 'service'; ts: number; data: { id: string; status: Health; metrics: Record<string, number> } }
  | { type: 'alert'; ts: number; data: RawAlert }
  | { type: 'incident'; ts: number; data: Incident }
  | { type: 'demo'; ts: number; data: DemoState };
