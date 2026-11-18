"""Voices (LOCKED): narrator = the owner's ElevenLabs recording; characters = Kokoro (free, local), one fixed voice
per character. Speech-to-text (Parakeet) cuts the narration into one clip per script line and checks the final mix.
Setup once per machine (GitHub release URLs; Hugging Face is often blocked):
  pip install sherpa-onnx soundfile scipy numpy skia-python
  R=https://github.com/k2-fsa/sherpa-onnx/releases/download
  curl -L -O $R/tts-models/kokoro-multi-lang-v1_0.tar.bz2 && tar xjf kokoro-multi-lang-v1_0.tar.bz2
  curl -L -O $R/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2 && tar xjf sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2
Models folder: $DOCANIM_MODELS (default ~/models)."""
import os, re, difflib, numpy as np, soundfile as sf
MODELS = os.path.expanduser(os.environ.get('DOCANIM_MODELS', '~/models'))
KOKORO = os.path.join(MODELS, 'kokoro-multi-lang-v1_0')
PARAKEET = os.path.join(MODELS, 'sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8')

# Kokoro v1.0 speaker ids (American voices first - US audience). The final pick per character is made in the first
# short test render, then written here and never changed, so each character sounds the same in every video.
KOKORO_IDS = {'af_heart': 3, 'af_bella': 2, 'af_nicole': 6, 'af_sarah': 9, 'af_sky': 10, 'am_adam': 11, 'am_echo': 12, 'am_eric': 13,
              'am_fenrir': 14, 'am_liam': 15, 'am_michael': 16, 'am_onyx': 17, 'am_puck': 18, 'bm_george': 26, 'bm_lewis': 27}
CHARACTER_VOICES = {   # candidates until the test render; then locked
    'ceo': ('am_onyx', 0.95), 'analyst': ('am_eric', 1.0), 'worker': ('am_adam', 1.0), 'banker': ('am_fenrir', 0.97),
    'investor': ('af_bella', 1.0), 'saver': ('af_sarah', 1.0), 'grad': ('am_liam', 1.05), 'scammer': ('am_puck', 1.0),
    'agent': ('am_echo', 0.97), 'reporter': ('af_nicole', 1.0), 'retiree': ('am_michael', 0.92)}
LEXICON_EXTRA = 'lex_extra.txt'   # add "word IPA" lines for names Kokoro mispronounces (watch for OOV warnings)

_TTS = None
def kokoro():
    global _TTS
    if _TTS is None:
        import sherpa_onnx
        if not os.path.exists(LEXICON_EXTRA): open(LEXICON_EXTRA, 'w').write('')
        M = KOKORO; cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
            model=f'{M}/model.onnx', voices=f'{M}/voices.bin', tokens=f'{M}/tokens.txt', data_dir=f'{M}/espeak-ng-data', dict_dir=f'{M}/dict',
            lexicon=f'{LEXICON_EXTRA},{M}/lexicon-us-en.txt,{M}/lexicon-gb-en.txt', lang='en-us'), num_threads=max(1, (os.cpu_count() or 2) - 1)))
        _TTS = sherpa_onnx.OfflineTts(cfg)
    return _TTS

def character_line(text, who, out):
    """Synthesize one character line with that character's fixed Kokoro voice; trimmed; returns (path, seconds)."""
    name, speed = CHARACTER_VOICES[who]; a = kokoro().generate(text, sid=KOKORO_IDS[name], speed=speed)
    s = np.array(a.samples, dtype=np.float32); idx = np.where(np.abs(s) > 0.012 * np.abs(s).max())[0]
    s = s[max(idx[0] - 300, 0): idx[-1] + 1500]; sf.write(out, s, a.sample_rate); return out, len(s) / a.sample_rate

_ASR = None
def asr():
    global _ASR
    if _ASR is None:
        import sherpa_onnx; M = PARAKEET
        _ASR = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f'{M}/encoder.int8.onnx', decoder=f'{M}/decoder.int8.onnx', joiner=f'{M}/joiner.int8.onnx',
                                                             tokens=f'{M}/tokens.txt', num_threads=max(1, (os.cpu_count() or 2) - 1), model_type='nemo_transducer')
    return _ASR
def _mono16k(path):
    from scipy.signal import resample_poly
    y, sr = sf.read(path); y = y.mean(1) if y.ndim > 1 else y; return resample_poly(y, 16000, sr).astype(np.float32) if sr != 16000 else y.astype(np.float32)
def words_with_times(path, chunk=24.0):
    """Speech-to-text with word timings: [(word, start, end)]. Decodes in 24 s chunks with 1 s overlap."""
    y = _mono16k(path); out = []; step = int((chunk - 1) * 16000); L = int(chunk * 16000); i = 0
    while i < len(y):
        seg = y[i:i + L]; st = asr().create_stream(); st.accept_waveform(16000, seg); asr().decode_stream(st); r = st.result
        toks, ts = list(r.tokens), list(r.timestamps); cur = None
        for tk, t in zip(toks, ts):
            t = t + i / 16000
            if tk.startswith('▁') or tk.startswith(' ') or cur is None:
                if cur: out.append(cur)
                cur = [tk.strip('▁ '), t, t + .2]
            else: cur[0] += tk; cur[2] = t + .2
        if cur: out.append(cur)
        i += step
    out.sort(key=lambda w: w[1]); ded = []
    for w in out:
        if not ded or w[1] > ded[-1][1] + .05: ded.append(w)
    return [(w, a, b) for w, a, b in ded if w]
def norm(s): return re.sub(r"[^a-z0-9$%']+", ' ', s.lower()).split()

def split_narration(narration_wav, lines, outdir):
    """Cut the owner's ElevenLabs narration (one file, narrator lines in script order) into one clip per line.
    lines: [(id, text)] narrator lines only. Returns {id: (clip_path, seconds)}. Aligns speech-to-text words to the
    script with difflib; lines that can't be matched are reported so the owner can check them."""
    os.makedirs(outdir, exist_ok=True); W_ = words_with_times(narration_wav); hyp = [norm(w)[0] if norm(w) else '' for w, _, _ in W_]
    ref, owner = [], []
    for k, (lid, txt) in enumerate(lines):
        for w in norm(txt): ref.append(w); owner.append(k)
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False); hit = {}
    for a, b, n in sm.get_matching_blocks():
        for j in range(n): hit.setdefault(owner[a + j], []).append(b + j)
    y, sr = sf.read(narration_wav); y = y.mean(1) if y.ndim > 1 else y; res, missing = {}, []
    bounds = []
    for k in range(len(lines)):
        if k in hit: bounds.append((W_[min(hit[k])][1], W_[max(hit[k])][2]))
        else: bounds.append(None); missing.append(lines[k][0])
    for k, (lid, _) in enumerate(lines):
        if bounds[k] is None: continue
        a, b = bounds[k]; nxt = next((bb[0] for bb in bounds[k + 1:] if bb), len(y) / sr)
        a = max(0, a - .12); b = min(nxt - .02, b + .35)
        clip = y[int(a * sr):int(b * sr)]; p = os.path.join(outdir, f'{lid}.wav'); sf.write(p, clip, sr); res[lid] = (p, len(clip) / sr)
    if missing: print('NOT MATCHED (check these lines in the narration):', missing)
    return res

def transcript_check(mix_wav, script_text):
    """Transcribe the final mix and compare with the script. Returns similarity 0..1 (aim > 0.9)."""
    hyp = ' '.join(norm(' '.join(w for w, _, _ in words_with_times(mix_wav)))); ref = ' '.join(norm(script_text))
    return difflib.SequenceMatcher(None, ref.split(), hyp.split(), autojunk=False).ratio()
