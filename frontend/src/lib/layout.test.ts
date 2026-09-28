import { toFlow } from './layout';
import { staticTopology } from './staticTopology';

test('كل رابط مربوط بالمنفذ الصحيح', () => {
  const { edges } = toFlow(staticTopology);
  const e = edges.find((x) => x.id === 'link-r1-sw1')!;
  expect(e.sourceHandle).toBe('Gi0/0');
  expect(e.targetHandle).toBe('Gi0/1');
});

test('كل منفذ في رابط موجود فعلًا على الجهاز', () => {
  for (const l of staticTopology.links) {
    const s = staticTopology.nodes.find((n) => n.id === l.source)!;
    const t = staticTopology.nodes.find((n) => n.id === l.target)!;
    expect(s.interfaces.map((i) => i.name)).toContain(l.sourcePort);
    expect(t.interfaces.map((i) => i.name)).toContain(l.targetPort);
  }
});
