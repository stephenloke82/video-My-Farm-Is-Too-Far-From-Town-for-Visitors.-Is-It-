"""Narration in Midwest Female Warm: Kokoro-82M ONNX, af_heart 0.6 + af_sarah 0.4,
speed 0.97, following VOICE.md. Writes the raw voice track and timing.json."""
import json, os, random, re, sys
import numpy as np
import onnxruntime as ort
import soundfile as sf
from misaki import en
from beats import BEATS, SPOKEN, PHONEMES

WORK = os.path.join(os.environ["LOCALAPPDATA"], "farvid")
MODELS = os.path.join(WORK, "models")
OUT = os.path.join(WORK, "work")
SR = 24000
SPEED = 0.97
TEST = "--test" in sys.argv

vocab = json.load(open(os.path.join(MODELS, "config.json"), encoding="utf8"))["vocab"]
voices = np.load(os.path.join(MODELS, "voices-v1.0.bin"))
blend = 0.6 * voices["af_heart"] + 0.4 * voices["af_sarah"]
sess = ort.InferenceSession(os.path.join(MODELS, "kokoro-v1.0.onnx"),
                            providers=["CPUExecutionProvider"])
names = [i.name for i in sess.get_inputs()]
token_key = "input_ids" if "input_ids" in names else "tokens"
g2p = en.G2P(trf=False, british=False, fallback=None)
random.seed(7)
hand, unknown = set(), set()


def for_voice(text):
    text = text.replace("“", '"').replace("”", '"').replace('"', "")
    text = text.replace("...", ",")
    for digits, words in SPOKEN:
        text = re.sub(rf"(?<![\d,]){re.escape(digits)}(?![\d,])", words, text)
    for word, ph in PHONEMES.items():
        if word in text:
            hand.add(word)
            text = text.replace(word, f"[{word}](/{ph}/)")
    return text


def speak(phrase):
    ph, toks = g2p(phrase)
    for t in toks:
        if not t.phonemes or "❓" in (t.phonemes or ""):
            if re.search(r"\w", t.text):
                unknown.add(t.text)
    ids = [vocab[c] for c in ph if c in vocab]
    # Kokoro takes 510 tokens at most; our phrases are far shorter.
    assert len(ids) < 500, phrase
    style = blend[min(len(ids), len(blend)) - 1]
    feed = {token_key: np.array([[0, *ids, 0]], dtype=np.int64),
            "style": np.array(style, dtype=np.float32),
            "speed": np.array([SPEED], dtype=np.float32)}
    return sess.run(None, feed)[0].squeeze()


def trim(wav):
    env = np.convolve(np.abs(wav), np.ones(240) / 240, mode="same")
    on = np.where(env > env.max() * 0.02)[0]
    pad = int(0.04 * SR)
    return wav[max(0, on[0] - pad):min(len(wav), on[-1] + pad)]


def phrases_of(text):
    """Split at commas and sentence ends, keeping names and quotes whole."""
    parts = re.findall(r'.+?(?:[,.?!]+["”]?(?=\s|$)|$)', text)
    return [p.strip() for p in parts if p.strip()]


def pause_after(raw):
    tail = raw.rstrip('"')
    return random.uniform(0.30, 0.45) if tail[-1] in ".?!" else random.uniform(0.12, 0.20)


def main():
    track = [np.zeros(int(0.25 * SR))]
    t = 0.25
    beats_out = []
    beats = BEATS[:3] if TEST else BEATS
    for i, (scene, text, hold) in enumerate(beats):
        start = t
        ph_out = []
        for raw in phrases_of(text):
            wav = trim(speak(for_voice(raw)))
            wav = wav / max(1e-6, np.abs(wav).max())
            gap = pause_after(raw)
            ph_out.append({"text": raw, "start": t - start, "dur": len(wav) / SR})
            track += [wav, np.zeros(int(gap * SR))]
            t += len(wav) / SR + int(gap * SR) / SR
        if hold:
            track.append(np.zeros(int(hold * SR)))
            t += int(hold * SR) / SR
        beats_out.append({"scene": scene, "start": start, "dur": t - start,
                          "text": text, "phrases": ph_out})
        print(f"{i+1:3d}/{len(beats)} {scene:18s} {t:7.2f}s", flush=True)
    track.append(np.zeros(int(0.30 * SR)))
    audio = np.concatenate(track)
    audio = audio / np.abs(audio).max() * 0.9
    sf.write(os.path.join(OUT, "voice_test.wav" if TEST else "voice_raw.wav"), audio, SR)
    if not TEST:
        json.dump({"beats": beats_out, "voice_end": len(audio) / SR},
                  open(os.path.join(OUT, "timing.json"), "w", encoding="utf8"),
                  ensure_ascii=False, indent=1)
    print("hand phonemes:", sorted(hand))
    print("UNKNOWN WORDS:", sorted(unknown))
    print("seconds:", round(len(audio) / SR, 2))


if __name__ == "__main__":
    main()
