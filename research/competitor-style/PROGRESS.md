# Paper Billion research progress

Status: extraction complete for the four source MP4s. Visual study and style guide are available. The shot logs are partial.

The input is D:\Test Video. This is the approved research subfolder. FFmpeg and FFprobe did the media work. Node.js handled data because the Python aliases would not run. No installation, repository change or video export was performed.

| Source | Baseline JPGs | Candidate-neighbor JPGs | Motion bursts | Candidate sheets |
|---|---:|---:|---:|---:|
| How a Chinese Spy Got Inside Nvidia | 2,376 | 1,512 | 12 × 60 frames | 31 |
| Why Nvidia Would Fail Without Jensen Huang | 1,721 | 975 | 12 × 60 frames | 20 |
| Why the AI Bubble Is Finally Popping | 3,303 | 1,679 | 12 × 60 frames | 33 |
| Why the Stock Market Just Crashed | 1,800 | 838 | 12 × 60 frames | 17 |

All candidates above 0.12 were extracted with their immediate source-frame neighbors, sharing files when triplets overlap. The candidate manifest also flags scores above 0.25. Each manifest reference was checked against the extracted files. A score candidate can represent animation inside a shot, and a gradual transition may not score above either threshold.

Baseline sheets use resampled 2 fps times. The overview sheets show 10-second sampling bins. The survey sheets sample native frames at exact 10-second positions. Hook sheets contain every native frame from the first 10 seconds. Candidate sheets contain before/at/after triplets at native frame times. Burst sheets summarize each native burst with six frames.

## Review completed

- Spy: opening, whole-duration overview, all burst strips and a mid-video cut sequence.
- Jensen: opening, whole-duration overview, all burst strips and a mid-video cut sequence.
- AI: opening, whole-duration overview, all burst strips and a mid-video cut sequence.
- Crash: opening, whole-duration overview, all burst strips and a mid-video cut sequence.

All four folders have analysis notes, WAV, EBU R128 summary and a 100 ms full-mix measurement trace. The shot CSV and JSON cover the first 10 seconds of each file and selected mid-video spans. The last opening row in each video ends at the review boundary. There are 36 reviewed rows in total. Additional examined sequences appear in the analysis documents.

## Remaining review

The full-duration editorial boundaries, exact text and narration per shot, shot-type totals, and transition counts still require manual review. No local audio input was available to the analysis interface, and Windows speech recognition failed to instantiate its listed recognizer. No timed transcript was available. Voice pace, music and SFX identification, beat alignment and isolated loudness remain unresolved. The full-mix meters are available for inspection.

See STYLE_BIBLE.md for observed references and proposed implementation parameters. See EFFECTS_CATALOG.md for original Remotion examples. The code examples were documented and have not been rendered.

