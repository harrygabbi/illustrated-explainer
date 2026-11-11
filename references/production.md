# Production and export

## Voice and sound

1. Isolate narration from chapter headings, stage directions, and source notes. Count words and characters in the actual speech payload.
2. Estimate narration with the intended voice, model, text, and number of takes if the user asks for a quote. Label estimates and actual generation usage in the units reported by the provider. Wait when the user has made approval of the estimate a condition of recording.
3. Record by chapter or in coherent groups. Use one continuous take per group unless the user requests options. Keep the dry voice, score, and effects as separate assets. This makes later Short edits easier.
4. Align the final narration with the script. Verify ambiguous cut points against the waveform or listen to the edit. Move cuts into nearby quiet gaps. If you trim or retime speech, apply the same timing map to captions and shot cues.
5. Keep the voice clear, with a restrained score and effects that support visible action. Verify full audio coverage, intelligibility, and the final tail. Report a retime if it materially changes the read.

## Still-cut renderer

The helper uses Python 3 and FFmpeg with H.264 and AAC support. Make the artwork the same aspect ratio as the desired video to avoid padding. Use explicit shot durations, include a final hold if needed, and supply a mixed audio track and English SRT when requested. Omitting audio creates a silent export.

Save a JSON manifest beside the artwork or use paths relative to the manifest.

```json
{
  "width": 1600,
  "height": 900,
  "fps": 24,
  "shots": [
    {"image": "frames/01.png", "duration": 3.5},
    {"image": "frames/02.png", "duration": 4.0}
  ],
  "audio": "audio/mix.wav",
  "captions": "English.srt"
}
```

Run `python3 scripts/render_stills.py path/to/cut.json path/to/output.mp4` from the skill folder. The helper rounds shot boundaries to frames, preserves the entire final still, and pads or trims audio to the picture. Captions are selectable. For subtitles visible in a silent review, place the text in the shot artwork or render a separate burned-in review copy.

Use the production's scene renderer when the cut requires within-shot motion. Review a contact sheet at small size, inspect the first and last shots and representative transitions, and probe the final container to verify the duration, dimensions, audio, and caption tracks.
