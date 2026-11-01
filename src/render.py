"""Frame renderer. `render.py sheet` draws contact sheets; `render.py film` renders
the picture in parallel chunks, each piped straight into ffmpeg."""
import multiprocessing as mp, os, subprocess, sys, traceback
import cairo
import numpy as np
from toon import *
from stage import SCENES, WORK, FPS, load_beats, Beat
from beats import END_SCREEN_SECONDS
import scenes_a, scenes_b, scenes_c  # noqa: F401 (they register the scenes)

BEATS, VOICE_END = load_beats()
END = Beat({"scene": "endscreen", "start": BEATS[-1].start + BEATS[-1].dur,
            "dur": END_SCREEN_SECONDS, "text": "", "phrases": []})
ALL = BEATS + [END]
TOTAL = END.start + END.dur
FRAMES = int(TOTAL * FPS)
OUT = os.path.join(WORK, "chunks")
_grain = None


def grain():
    """A faint paper tooth and soft vignette, to keep the flats from looking digital."""
    global _grain
    if _grain is None:
        rng = np.random.default_rng(3)
        small = rng.normal(0, 1, (H // 2, W // 2))
        n = np.kron(small, np.ones((2, 2)))
        yy, xx = np.mgrid[0:H, 0:W]
        v = ((xx / W - .5) ** 2 + (yy / H - .5) ** 2) * 2
        alpha = np.clip(np.abs(n) * 5 + v ** 1.6 * 60, 0, 70).astype(np.uint8)
        arr = np.zeros((H, W, 4), np.uint8)
        arr[..., 0], arr[..., 1], arr[..., 2] = (alpha * .16).astype(np.uint8), (alpha * .12).astype(np.uint8), (alpha * .12).astype(np.uint8)
        arr[..., 3] = alpha
        _grain = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_ARGB32, W, H)
        globals()["_grain_arr"] = arr  # cairo borrows this buffer, so it must stay alive
    return _grain


def beat_at(t):
    lo, hi = 0, len(ALL) - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if ALL[m].start <= t:
            lo = m
        else:
            hi = m - 1
    return ALL[lo]


def draw(ctx, t):
    b = beat_at(t)
    local = max(0.0, t - b.start)
    ctx.save()
    # a slow push-in on every shot
    z = 1 + 0.03 * smooth(local / max(b.dur, 1.0))
    ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2)
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    SCENES[b.scene](ctx, b, local)
    ctx.restore()
    ctx.set_source_surface(grain(), 0, 0)
    ctx.paint()


def still(t):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    draw(ctx, t)
    return s


def chunk(args):
    idx, f0, f1 = args
    path = os.path.join(OUT, f"c{idx:03d}.mp4")
    if os.path.exists(path + ".done"):
        return idx
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-threads", "2", path], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    for f in range(f0, f1):
        ctx.save()
        draw(ctx, f / FPS)
        ctx.restore()
        s.flush()
        p.stdin.write(bytes(s.get_data()))
    p.stdin.close()
    p.wait()
    open(path + ".done", "w").close()
    print("chunk", idx, flush=True)
    return idx


def film():
    os.makedirs(OUT, exist_ok=True)
    step = 450
    jobs = [(i, f, min(f + step, FRAMES)) for i, f in enumerate(range(0, FRAMES, step))]
    with mp.Pool(12) as pool:
        for _ in pool.imap_unordered(chunk, jobs):
            pass
    with open(os.path.join(OUT, "list.txt"), "w") as f:
        for i, *_ in jobs:
            f.write(f"file 'c{i:03d}.mp4'\n")
    print("frames", FRAMES, "seconds", TOTAL)


def sheet_job(a):
    i, b, f, path = a
    try:
        s = still(b.start + b.dur * f if b.scene != "endscreen" else b.start + 3)
        s.write_to_png(path)
    except Exception:
        print("FAIL", b.scene, f)
        traceback.print_exc()
    return path


def stress_job(f):
    still(f / FPS)


def sheets(names=None, fracs=(0.45, 0.97), out="sheet"):
    d = os.path.join(WORK, "stills")
    os.makedirs(d, exist_ok=True)
    jobs = []
    for i, b in enumerate(ALL):
        if names and b.scene not in names:
            continue
        for j, f in enumerate(fracs):
            jobs.append((i, b, f, os.path.join(d, f"{out}_{i:03d}_{j}.png")))
    with mp.Pool(12) as pool:
        paths = pool.map(sheet_job, jobs)
    return paths


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "film":
        film()
    elif mode == "sheet":
        names = sys.argv[3].split(",") if len(sys.argv) > 3 and sys.argv[3] != "-" else None
        fracs = tuple(float(x) for x in sys.argv[2].split(","))
        print(len(sheets(names, fracs)))
    elif mode == "thumbs":
        import thumbs
        thumbs.main()
    elif mode == "stress":
        import time
        t0 = time.time()
        with mp.Pool(12) as pool:
            pool.map(stress_job, range(0, FRAMES, 5), chunksize=40)
        print("frames", FRAMES, "ok; seconds", round(time.time() - t0, 1))
