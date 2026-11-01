"""Spot checks on the finished file: music balance, longest static shots, and stills
pulled from the encoded MP4 itself."""
import os, subprocess, sys
import numpy as np
import soundfile as sf
from stage import WORK, load_beats

beats, _ = load_beats()
mix, sr = sf.read(os.path.join(WORK, "mix_final.wav"))
voice, _ = sf.read(os.path.join(WORK, "voice_master.wav"))
mono = mix.mean(axis=1)
hop = sr // 10
n = len(voice) // hop
vr = np.sqrt(np.mean(voice[:n * hop].reshape(n, hop) ** 2, axis=1))
mr = np.sqrt(np.mean(mono[:n * hop].reshape(n, hop) ** 2, axis=1))
db = lambda x: 20 * np.log10(np.maximum(x, 1e-7))
speech = vr > 0.02
quiet = vr < 1e-4
print(f"voice-active level {db(mr[speech]).mean():.1f} dB, gaps level {db(mr[quiet]).mean():.1f} dB")
# what remains under speech once the voice is taken out of the mix
scale = np.median(mono[:len(voice)] @ voice / (voice @ voice))
rest = mono[:len(voice)] - scale * voice
rr = np.sqrt(np.mean(rest[:n * hop].reshape(n, hop) ** 2, axis=1))
print(f"voice sits {db(mr[speech]).mean() - db(rr[speech]).mean():.1f} dB above the music while speaking")
print("end-screen level", round(float(db(np.sqrt(np.mean(mono[int(sr * (len(mono) / sr - 12)):] ** 2)))), 1), "dB")
long_ = sorted(beats, key=lambda b: -b.dur)[:8]
print("longest beats:", [(b.scene, round(b.dur, 1)) for b in long_])
f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "my-farm-is-too-far-from-town.mp4")
out = os.path.join(WORK, "qc")
os.makedirs(out, exist_ok=True)
times = {"lip1": beats[9].start, "doing": next(b for b in beats if b.scene == "doing").start + 1.0,
         "end": beats[-1].start + beats[-1].dur + 10, "firstframe": 0.05}
for k, t in times.items():
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", f, "-frames:v", "1", "-vf", "scale=960:-1", os.path.join(out, k + ".png")], check=True)
print("frames saved")
