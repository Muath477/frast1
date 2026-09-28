import type { WsMessage } from './types';

export type WsStatus = 'connecting' | 'open' | 'closed';

export function connectOps(
  onMessage: (m: WsMessage) => void,
  onStatus: (s: WsStatus) => void,
) {
  let ws: WebSocket | null = null;
  let retry = 0;
  let stopped = false;
  const url = `${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/ws/operations`;

  const open = () => {
    onStatus('connecting');
    ws = new WebSocket(url);
    ws.onopen = () => {
      retry = 0;
      onStatus('open');
    };
    ws.onmessage = (e) => onMessage(JSON.parse(e.data) as WsMessage);
    ws.onclose = () => {
      onStatus('closed');
      if (!stopped) setTimeout(open, Math.min(5000, 500 * 2 ** retry++));
    };
  };
  open();
  return () => {
    stopped = true;
    ws?.close();
  };
}
