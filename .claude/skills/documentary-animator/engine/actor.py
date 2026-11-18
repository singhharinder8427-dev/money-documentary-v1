"""Actor = a character placed in a shot with the standard animation built in:
idle bob, blink every ~2.7 s, squash when the shot starts, poses that snap with overshoot, optional walk,
lip-sync from its voice lines. Use: a = Actor('ceo', x, y, s); a.pose(0, ('down','down')); a.pose(1.2, ('present','hip'))
a.say(tl, 'n014'); then in the shot's draw(c, t): a.draw(c, t, abs_t)."""
import math
from engine import kit
from engine.cast import CAST

class Actor:
    def __init__(self, who, x, y, s=1.0, face=0.0, light=-1, rim='#9FB8F0', hat=False, spec=None, **expr):
        self.spec = spec or CAST[who]; self.who = who; self.x, self.y, self.s = x, y, s; self.face = face; self.light, self.rim, self.hat = light, rim, hat
        self.expr = dict(eyes='dot', mouth='smile', brow=0.0, brow_tilt=0.0, sweat=-1.0); self.expr.update(expr)
        self.poses = [(0.0, ('down', 'down'))]; self.exprs = []; self.walk = None; self.lines = []; self.phase = (hash(who) % 100) / 37
    def pose(self, t, arms): self.poses.append((t, arms)); self.poses.sort(key=lambda p: p[0]); return self
    def expression(self, t, **kw): self.exprs.append((t, kw)); self.exprs.sort(key=lambda e: e[0]); return self
    def walk_to(self, t0, t1, x1, y1=None): self.walk = (t0, t1, self.x, self.y, x1, self.y if y1 is None else y1); return self
    def say(self, timeline, lid, mouths): self.lines.append((timeline, lid, mouths)); return self
    def _arms(self, t):
        cur = self.poses[0][1]; prev = cur; tc = -1e9
        for tp, a in self.poses:
            if tp <= t: prev, cur, tc = cur, a, tp
        k = min(max((t - tc) / 0.28, 0), 1)
        if k >= 1 or prev == cur: return cur
        return tuple(((p if isinstance(p, str) else p[1]), (c_ if isinstance(c_, str) else c_[1]), k) for p, c_ in zip(prev, cur))
    def draw(self, c, t, abs_t=None):
        abs_t = t if abs_t is None else abs_t; e = dict(self.expr)
        for te, kw in self.exprs:
            if te <= t: e.update(kw)
        x, y, legs, bob = self.x, self.y, None, 1.6 * math.sin(t * 2.2 + self.phase)
        if self.walk:
            t0, t1, x0, y0, x1, y1 = self.walk
            if t0 <= t <= t1:
                k = (t - t0) / max(t1 - t0, 1e-3); x, y = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k; ph = (t - t0) * 11
                legs = kit.walk_legs(ph); bob = 7 * abs(math.sin(ph))
            elif t > t1: x, y = x1, y1
        squash = 0.06 * max(0, 1 - t / 0.25) * math.sin(t / 0.25 * math.pi) if t < 0.25 else 0.0
        for tl, lid, mouths in self.lines:
            m = tl.mouth_at(mouths, lid, abs_t)
            if m: e['mouth'] = {'open': 'open', 'mid': 'mid', 'closed': 'flat'}[m]
        eyes = 'closed' if kit.blink(t, 2.7, self.phase) and e['eyes'] in ('dot', 'wide') else e['eyes']
        kit.draw_char(c, x, y, self.s, self.spec, face=self.face, eyes=eyes, mouth=e['mouth'], brow=e['brow'], brow_tilt=e['brow_tilt'],
                      arms=self._arms(t), bob=bob, squash=squash, sweat=(t % 1.0) if e['sweat'] >= 0 else -1.0, light=self.light, rim=self.rim,
                      hat=self.hat, legs=legs, sparkle=e.get('sparkle', 0.0))
