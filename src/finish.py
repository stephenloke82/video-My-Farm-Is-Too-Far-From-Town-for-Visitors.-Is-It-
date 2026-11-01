"""Caption file, two-pass loudness on the mix, and the final mux."""
import json, os, re, subprocess
from stage import WORK, load_beats

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "output")
NAME = "my-farm-is-too-far-from-town"
os.makedirs(OUT, exist_ok=True)


def stamp(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def captions():
    beats, _ = load_beats()
    cues = []
    for b in beats:
        run, start, end = "", None, None
        for p in b.phrases:
            t0, t1 = b.start + p["start"], b.start + p["start"] + p["dur"]
            if run and len(run) + len(p["text"]) > 74:
                cues.append((start, end, run)); run = ""
            if not run:
                start = t0
            run = (run + " " + p["text"]).strip()
            end = t1
        cues.append((start, end, run))
    with open(os.path.join(OUT, f"{NAME}.srt"), "w", encoding="utf8") as f:
        for i, (a, b_, s) in enumerate(cues, 1):
            words, l1 = s.split(), ""
            if len(s) > 42:
                half = len(s) / 2
                while words and len(l1) + len(words[0]) / 2 < half:
                    l1 = (l1 + " " + words.pop(0)).strip()
                s = l1 + "\n" + " ".join(words)
            f.write(f"{i}\n{stamp(a)} --> {stamp(b_)}\n{s}\n\n")
    print("captions", len(cues))


def mix_and_mux():
    raw = os.path.join(WORK, "mix_raw.wav")
    first = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", raw, "-af",
                            "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
    m = json.loads(re.search(r"\{[^{}]+\}", first, re.S).group(0))
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    mix = os.path.join(WORK, "mix_final.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", af, "-ar", "44100", "-c:a", "pcm_s16le", mix], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(WORK, "chunks", "list.txt"),
                    "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", os.path.join(OUT, f"{NAME}.mp4")], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(WORK, "voice_master.wav"), "-b:a", "192k",
                    os.path.join(OUT, f"{NAME}-narration.mp3")], check=True)


if __name__ == "__main__":
    captions()
    mix_and_mux()
    print("done")
