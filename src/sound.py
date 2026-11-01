"""Original score and sound effects, all synthesised here, mixed under the voice.
Gentle folk: plucked strings over soft pads, a new colour per chapter, ducked under the narration."""
import os
import numpy as np
import soundfile as sf
from stage import WORK, load_beats
from beats import END_SCREEN_SECONDS

SR = 44100
rng = np.random.default_rng(11)
beats, voice_end = load_beats()
TOTAL = beats[-1].start + beats[-1].dur + END_SCREEN_SECONDS
N = int(TOTAL * SR) + SR
A4 = 440.0


def midi(n):
    return A4 * 2 ** ((n - 69) / 12)


def pluck(freq, dur, bright=0.5):
    """Karplus-Strong string."""
    period = int(SR / freq)
    n = int(dur * SR)
    buf = rng.uniform(-1, 1, period)
    for _ in range(2):
        buf = 0.5 * (buf + np.roll(buf, 1))
    out = np.zeros(n)
    damp = 0.992 + bright * 0.006
    # run the loop over blocks of one period; much faster than sample by sample
    pos = 0
    while pos < n:
        m = min(period, n - pos)
        out[pos:pos + m] = buf[:m]
        buf = damp * (0.5 * (buf + np.roll(buf, 1)) * (1 - bright * .5) + buf * (bright * .5))
        pos += m
    out *= np.minimum(1, np.arange(n) / 40)
    return out


def pad(freqs, dur):
    t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)
    s = sum(np.sin(2 * np.pi * f * t + i) + .4 * np.sin(2 * np.pi * f * 2.003 * t) for i, f in enumerate(freqs))
    return s * env / len(freqs)


CHORDS = {  # root-position triads as MIDI notes, in G major
    "G": (55, 59, 62), "C": (48, 55, 60, 64), "D": (50, 57, 62, 66), "Em": (52, 59, 64, 67), "Am": (57, 60, 64), "Bm": (47, 54, 59, 62),
}
# Chapters by the scene that opens them: progression and tempo
SECTIONS = [
    ("cinema", ["G", "Em", "C", "D"], 88, .7),
    ("yourfarm_road", ["Em", "C", "G", "D"], 76, .45),
    ("title", ["G", "C", "G", "D"], 92, .85),
    ("belief", ["C", "G", "Am", "D"], 88, .6),
    ("kansas", ["G", "D", "Em", "C"], 92, .75),
    ("iceland_map", ["Em", "Bm", "C", "G"], 72, .5),
    ("gate2008", ["G", "D", "C", "G"], 84, .7),
    ("count180", ["C", "G", "D", "Em"], 96, .95),
    ("move1card", ["G", "C", "D", "G"], 100, .9),
    ("move2card", ["C", "G", "Am", "D"], 104, .9),
    ("move3card", ["Em", "C", "G", "D"], 96, .85),
    ("hours", ["Em", "C", "Am", "D"], 80, .55),
    ("back1989", ["G", "Em", "C", "D"], 84, .75),
    ("guide", ["G", "C", "D", "G"], 96, .8),
    ("final", ["G", "D", "C", "G"], 84, .9),
]


def score():
    out = np.zeros((N, 2))
    starts = {b.scene: b.start for b in beats}
    marks = [(starts[s[0]], s) for s in SECTIONS] + [(TOTAL, None)]
    notes = {}

    def note(m, dur, br):
        k = (m, round(dur, 1), round(br, 1))
        if k not in notes:
            notes[k] = pluck(midi(m), dur, br)
        return notes[k]

    for i, (t0, sec) in enumerate(marks[:-1]):
        t1 = marks[i + 1][0]
        _, chords, bpm, lift = sec
        bar = 240 / bpm
        eighth = bar / 8
        t = t0
        bar_i = 0
        while t < t1 - 0.1:
            ch = CHORDS[chords[bar_i % len(chords)]]
            bass = ch[0] - 12 if ch[0] > 50 else ch[0]
            pattern = [0, 2, 1, 3, 2, 1, 3, 2] if bar_i % 4 != 3 else [0, 3, 2, 1, 3, 2, 1, 0]
            for j, p in enumerate(pattern):
                when = t + j * eighth + rng.uniform(-.006, .006)
                if when >= t1:
                    break
                m = (ch[p % len(ch)] + 12) if p else bass
                if p == 0 and j:
                    m = bass + 12
                w = note(m, 2.2, .35)
                a = int(when * SR)
                b_ = min(N, a + len(w))
                g = (.5 if j % 4 == 0 else .3) * (0.65 + lift * .5)
                pan = -.25 + .5 * ((j * 3) % 5) / 4
                out[a:b_, 0] += w[:b_ - a] * g * (1 - pan)
                out[a:b_, 1] += w[:b_ - a] * g * (1 + pan)
            p_ = pad([midi(x + 12) for x in ch[:3]], bar + 1.0) * .1
            a = int(t * SR)
            b_ = min(N, a + len(p_))
            out[a:b_, 0] += p_[:b_ - a]
            out[a:b_, 1] += p_[:b_ - a]
            t += bar
            bar_i += 1
    return out


def tone(f, dur, decay=6.0, partials=(1, 2.4, 4.1)):
    t = np.arange(int(dur * SR)) / SR
    s = sum(np.sin(2 * np.pi * f * p * t) / (i + 1) for i, p in enumerate(partials))
    return s * np.exp(-t * decay)


def noise(dur, lo=200, hi=4000):
    n = rng.normal(0, 1, int(dur * SR))
    spec = np.fft.rfft(n)
    fr = np.fft.rfftfreq(len(n), 1 / SR)
    spec[(fr < lo) | (fr > hi)] = 0
    return np.fft.irfft(spec, len(n))


def creak(dur=1.1):
    t = np.arange(int(dur * SR)) / SR
    f = 150 + 90 * np.sin(2 * np.pi * 1.6 * t) + 40 * np.sin(2 * np.pi * 37 * t)
    ph = np.cumsum(f) / SR
    s = np.sign(np.sin(2 * np.pi * ph)) * .5 + np.sin(2 * np.pi * 3 * ph) * .4
    return s * np.minimum(1, t / .1) * np.minimum(1, (dur - t) / .2)


def whoosh(dur=.5):
    n = noise(dur, 300, 2600)
    return n * np.hanning(len(n)) * 1.6


FX = {
    "chime": tone(1046, 1.6, 3.5) * .7, "ding": tone(1568, .9, 6) * .55,
    "tick": tone(1800, .08, 60) * .6, "thud": tone(120, .3, 16, (1, 1.5)) * 1.3,
    "gate": creak() * .45, "pop": tone(660, .16, 26, (1, 2)) * .7, "whoosh": whoosh() * .6,
    "stamp": tone(90, .3, 12, (1, 2.1, 3.3)) * 1.1, "bell": tone(880, 1.6, 2.6) * .55,
}
# (scene, words the sound lands on or a time in seconds, sound)
CUES = [
    ("cinema", .2, "chime"), ("stranger_arrive", "Two weeks", "whoosh"), ("stranger_first", .2, "chime"),
    ("title", .05, "whoosh"), ("title", "Let's find", "gate"), ("stay3", "found", "pop"), ("stay3", "forgotten", "pop"),
    ("people_drive", "How far", "whoosh"), ("real_question", "What's", "whoosh"), ("notthis1", "will pull", "stamp"),
    ("notthis2", "theme park", "stamp"), ("notthis2", "town", "stamp"), ("iceland_map", .1, "chime"),
    ("gate2008", "opened the gate", "gate"), ("menu", "Tomato soup", "pop"), ("menu", "Tomato ice cream", "pop"),
    ("menu", "Even tomato beer", "pop"), ("same", "No.", "stamp"), ("same", "Same farm", "ding"), ("same", "Same village", "ding"),
    ("same", "Same road", "ding"), ("fixed", "They made", "chime"), ("subscribe", "subscribe", "pop"), ("subscribe", "so the next", "bell"),
    ("move1card", .05, "chime"), ("sold_one", "Neither", "stamp"), ("test", "it will not", "stamp"), ("sentence", "Only at", "whoosh"),
    ("move2card", .05, "chime"), ("dotoeat", "Something to do.", "pop"), ("dotoeat", "Something to eat.", "pop"),
    ("dotoeat", "Something to take home.", "pop"), ("move3card", .05, "chime"), ("relevance", "A complete profile", "ding"),
    ("relevance", "the right category", "ding"), ("relevance", "real photos", "ding"), ("relevance", "your opening hours", "ding"),
    ("found_forgot", "That is the difference", "whoosh"), ("cabin", "Tents.", "pop"), ("cabin", "A cabin.", "pop"), ("cabin", "A farm stay.", "pop"),
    ("bar_gate", "It does not", "gate"), ("doing", "Doing will", "stamp"), ("inside", "the three farms", "ding"), ("inside", "a farm category", "ding"),
    ("inside", "a fifteen-shot", "ding"), ("inside", "scripts for", "ding"), ("inside", "reply templates", "ding"), ("inside", "a thirty-day plan", "ding"),
    ("final", "Make it", "gate"),
]


def effects():
    out = np.zeros(N)
    by = {b.scene: b for b in beats}
    for scene, when, fx in CUES:
        b = by[scene]
        t = b.start + (when if isinstance(when, (int, float)) else b.cue(when))
        w = FX[fx]
        a = int(t * SR)
        e = min(N, a + len(w))
        out[a:e] += w[:e - a]
    return out


def main():
    voice, sr = sf.read(os.path.join(WORK, "voice_master.wav"))
    assert sr == SR
    v = np.zeros(N)
    v[:len(voice)] = voice

    music = score()
    music /= np.abs(music).max()
    # gentle saturation brings the sustained strings up towards the plucked peaks
    music = np.tanh(music * 3.0) / np.tanh(3.0)
    # Voice envelope drives the ducking: 16 dB down with a soft attack and release.
    win = int(.03 * SR)
    env = np.convolve(np.abs(v), np.ones(win) / win, mode="same")
    speaking = np.minimum(1, env / (np.percentile(env[env > 0], 60) * .5))
    hold = int(.25 * SR)
    block = speaking[::441]
    held = np.array([block[max(0, i - hold // 441):i + hold // 441 + 1].max() for i in range(len(block))])
    smooth = np.convolve(held, np.ones(25) / 25, mode="same")
    duck_db = -16 * np.interp(np.arange(N), np.arange(len(smooth)) * 441, smooth)
    gain = 10 ** (duck_db / 20)
    # Open with a soft swell, close the end screen with a fade.
    fade = np.minimum(1, np.arange(N) / (1.5 * SR)) * np.minimum(1, (TOTAL - np.arange(N) / SR) / 4).clip(0)
    base = 10 ** (-7 / 20)
    m = music * (gain * fade * base)[:, None]
    fx = effects() * 10 ** (-17 / 20)
    mix = m + np.stack([v + fx, v + fx], 1)
    sf.write(os.path.join(WORK, "mix_raw.wav"), mix[: int(TOTAL * SR)], SR, subtype="FLOAT")
    print("mix seconds", TOTAL, "peak", np.abs(mix).max())


if __name__ == "__main__":
    main()
