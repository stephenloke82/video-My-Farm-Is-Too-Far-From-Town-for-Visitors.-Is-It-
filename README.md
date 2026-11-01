# My Farm Is Too Far From Town for Visitors. Is It?

A 9:09 cartoon explainer for the Agritourism Success YouTube channel: AI narration in Midwest Female Warm, animation drawn in code, and an original score. Everything is generated. There is no stock footage or sampled music.

## In this repo

| File | What it is |
|---|---|
| `output/my-farm-is-too-far-from-town-repo.mp4` | The film, 1920x1080, 30 fps. This copy is compressed to fit GitHub's 100 MB limit. |
| `output/my-farm-is-too-far-from-town.srt` | Captions, word for word from the script |
| `output/my-farm-is-too-far-from-town-narration.mp3` | Narration on its own, 192 kbps mono |
| `output/thumbnail-a.png`, `output/thumbnail-b.png` | 1280x720 thumbnails |
| `output/contact-sheet.jpg` | One still every 11 seconds |
| `src/script.txt` | The script as supplied |
| `src/beats.py` | The same words split into 92 timed beats, with pronunciations |

## Rebuild

Needs Python 3.12 with pycairo, numpy, fonttools, pillow, onnxruntime, soundfile and `misaki[en]`, plus FFmpeg on the path. It also needs these files under `%LOCALAPPDATA%\farvid` (they are not committed):

- `models\kokoro-v1.0.onnx`, `models\voices-v1.0.bin` and `models\config.json`, from thewh1teagle/kokoro-onnx
- `fonts\Fredoka-bold.ttf` and `fonts\Fredoka-reg.ttf`, made from Google Fonts' Fredoka at weights 600 and 450

Run these from `src`, after mastering the voice as `work\voice_master.wav` using the settings in `VOICE.md` of the agritourismvideos1 repo:

```
python check_script.py       # beats match the script word for word
python voice.py              # narration and timing.json
python render.py film        # picture, in parallel chunks
python sound.py              # score, effects and ducking
python render.py thumbs      # thumbnails
python finish.py             # captions, loudness, final MP4
```

`render.py sheet 0.7` draws one still per scene for review. `qc.py` measures the music balance.
