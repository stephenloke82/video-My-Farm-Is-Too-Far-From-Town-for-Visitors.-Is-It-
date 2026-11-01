"""Beat timing, the scene registry, and the mouth envelope."""
import json, os
import numpy as np
import soundfile as sf

WORK = os.path.join(os.environ["LOCALAPPDATA"], "farvid", "work")
FPS = 30
SCENES = {}


def scene(name):
    def reg(fn):
        SCENES[name] = fn
        return fn
    return reg


class Beat:
    def __init__(self, d):
        self.scene, self.start, self.dur = d["scene"], d["start"], d["dur"]
        self.text, self.phrases = d["text"], d["phrases"]

    def cue(self, s):
        """Seconds into the beat at which the words s are spoken."""
        low = s.lower()
        for p in self.phrases:
            i = p["text"].lower().find(low)
            if i >= 0:
                return p["start"] + p["dur"] * i / max(1, len(p["text"]))
        raise KeyError(f"{s!r} not in {self.scene}")


_env = None


def env():
    global _env
    if _env is None:
        path = os.path.join(WORK, "mouth.npy")
        if not os.path.exists(path):
            wav, sr = sf.read(os.path.join(WORK, "voice_master.wav"))
            hop = sr // FPS
            n = len(wav) // hop
            rms = np.sqrt(np.mean(wav[: n * hop].reshape(n, hop) ** 2, axis=1))
            rms = rms / np.percentile(rms, 97)
            # A fast opening and a slower close reads as speech rather than chatter.
            out = np.zeros(n)
            v = 0.0
            for i in range(n):
                v = max(rms[i], v * 0.62)
                out[i] = min(1.0, v)
            np.save(path, out)
        _env = np.load(path)
    return _env


def mouth_at(abs_t):
    e = env()
    i = int(abs_t * FPS)
    return float(e[i]) if 0 <= i < len(e) else 0.0


def load_beats():
    data = json.load(open(os.path.join(WORK, "timing.json"), encoding="utf8"))
    return [Beat(d) for d in data["beats"]], data["voice_end"]
