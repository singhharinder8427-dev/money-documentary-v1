"""Timeline: every line is cued from its measured voice length, in script order.
script.json lines: {"id", "beat", "chapter", "speaker", "text", "card", "counter", "dramatised", "sources", "shot_hint"}
Rules (from the aivxer pipeline): shot start + 0.3 s, each line + 0.26 s gap; cards with no voice 1.5 s."""
import json, numpy as np, soundfile as sf
from engine import audio as A
from engine.kit import mouth_track

BEAT_MOOD = {'HOOK': 'suspense', 'CH1': 'suspense', 'CH2': 'suspense', 'CH3': 'suspense', 'TWIST': 'twist',
             'CH4': 'suspense', 'CH5': 'suspense', 'END': 'ending', 'TITLE': 'silence', 'CHAPTER': 'silence'}
GAP, LEAD, CARD = 0.26, 0.3, 1.5

def load_script(path): return json.load(open(path))['lines'] if path.endswith('.json') else path
def build(lines, clips, shot_breaks=(), title_after=None, title_dur=2.5, chapter_dur=2.2, ending=True, hold=1.8, outro_dur=3.0, end_screen=18.0):
    """lines: script lines (dicts). clips: {id: (wav, seconds)} for every voiced line.
    shot_breaks: ids that start a new shot (+0.3 s lead). title_after: id of the last hook line (title card follows).
    Chapter cards are inserted automatically when the chapter name changes. Returns a Timeline."""
    t = 0.0; cues = {}; events = []; last_ch = None
    for ln in lines:
        ch = ln.get('chapter')
        if ch and ch != last_ch and ln.get('beat', '').startswith('CH'):
            events.append(dict(kind='chapter', t0=t, t1=t + chapter_dur, title=ch, n=int(ln['beat'][2:]) if ln['beat'][2:].isdigit() else None)); t += chapter_dur + LEAD
        last_ch = ch or last_ch
        if ln['id'] in shot_breaks: t += LEAD
        d = clips[ln['id']][1] if ln['id'] in clips else CARD
        cues[ln['id']] = (t, d); t += d + GAP
        if ln['id'] == title_after: events.append(dict(kind='title', t0=t, t1=t + title_dur)); t += title_dur + LEAD
    if ending:   # owner: the end must be obvious - hold the final card, outro card, then the end screen
        t += hold; events.append(dict(kind='outro', t0=t, t1=t + outro_dur)); t += outro_dur
        events.append(dict(kind='endscreen', t0=t, t1=t + end_screen)); t += end_screen
        tl = Timeline(lines, clips, cues, events, t)
    else: tl = Timeline(lines, clips, cues, events, t + 1.0)
    tl.breaks = set(shot_breaks); return tl

class Timeline:
    def __init__(self, lines, clips, cues, events, total):
        self.lines, self.clips, self.cues, self.events, self.total = lines, clips, cues, events, total
        self.by_id = {l['id']: l for l in lines}
    def start(self, lid): return self.cues[lid][0]
    def at(self, marker):
        """Time of a shot boundary: a line id (a shot starting there begins 0.3 s early), 'title', 'chapter:N' or 'end'."""
        if marker == 'end': return self.total
        if marker in ('title', 'outro', 'endscreen'): return next(e['t0'] for e in self.events if e['kind'] == marker)
        if marker.startswith('chapter:'): return next(e['t0'] for e in self.events if e['kind'] == 'chapter' and str(e['n']) == marker[8:])
        return self.cues[marker][0] - (LEAD if marker in self.breaks else 0.0)
    def dur(self, a, b):
        """Length of the shot from boundary a to boundary b (consecutive shots tile the timeline with no gaps)."""
        return self.at(b) - self.at(a)
    def end(self, lid): return sum(self.cues[lid])
    def mood_segments(self):
        """Music mood per stretch, from the beats; title + chapter cards are silent (sound logo / boom on top)."""
        segs = []; items = [(self.cues[l['id']][0], BEAT_MOOD.get(l.get('beat', 'CH1'), 'suspense')) for l in self.lines]
        items += [(e['t0'], {'outro': 'endscreen', 'endscreen': 'endscreen'}.get(e['kind'], 'silence')) for e in self.events]; items.sort()
        ends = {e['t0']: e['t1'] for e in self.events}
        for i, (t0, m) in enumerate(items):
            t1 = items[i + 1][0] if i + 1 < len(items) else self.total
            if m == 'silence': t1 = ends.get(t0, t1)
            if m == 'endscreen' and segs and segs[-1][2] == 'endscreen': segs[-1] = (segs[-1][0], t1, m); continue
            if segs and segs[-1][2] == m and abs(segs[-1][1] - t0) < .6: segs[-1] = (segs[-1][0], t1, m)
            else: segs.append((t0, t1, m))
        return segs
    def voice_track(self, ref_rms=None):
        """All voice clips placed at their cues, cleaned (narrator vs character chain, level-matched)."""
        out = np.zeros(int(self.total * A.SR) + A.SR)
        for lid, (wav, _) in self.clips.items():
            sp = self.by_id[lid].get('speaker', 'NARRATOR').lower(); y = A.load(wav)
            y = A.voice_chain(y, 'narrator' if sp == 'narrator' else 'character', None if sp == 'narrator' else ref_rms); A.add(out, y, self.start(lid))
        return out[:int(self.total * A.SR)]
    def mouths(self):
        """{id: per-frame mouth states ('open'/'mid'/'closed')} for lip-sync of speaking characters."""
        return {lid: mouth_track(wav) for lid, (wav, _) in self.clips.items() if self.by_id[lid].get('speaker', 'NARRATOR') != 'NARRATOR'}
    def mouth_at(self, mouths, lid, t):
        from engine.core import FPS
        if lid not in mouths: return None
        f = int((t - self.start(lid)) * FPS); m = mouths[lid]
        return m[f] if 0 <= f < len(m) else None
