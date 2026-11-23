# Effects catalog for original Remotion scenes

All parameters below are suggested starting points for a 1920×1080, 30 fps composition. The references identify the visual effect. Source implementation and exact parameters are uncertain.

## Layered push and depth

At 00:06.2–00:08.6 in the spy video the change in framing emphasizes the face and green chest accent, with practical lights and rear window still legible. Use three overscanned plates. Author the rear drift at 12 px, middle at 26 px, nearest at 42 px over 75 frames. Their average speeds are 4.8, 10.4 and 16.8 px/s. This is a recipe, and the reference layer offsets remain uncertain.

```tsx
import type { ReactNode } from 'react';
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from 'remotion';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

export function DepthPlate({children, distance}: {children: ReactNode; distance: 12 | 26 | 42}) {
  const f = useCurrentFrame();
  const t = interpolate(f, [0, 75], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  return <AbsoluteFill style={{transform: `translateX(${-distance * t}px) scale(${1.05 + 0.07 * t})`}}>{children}</AbsoluteFill>;
}
```

## Practical light spill

The table in the spy hook at 00:00.000 uses a warm practical and separate green spill. Its map around 00:03.600 repeats the hue. Author separate tight and broad masks so the highlight does not flatten the scene.

```tsx
<AbsoluteFill style={{
  pointerEvents: 'none', mixBlendMode: 'screen',
  background: 'radial-gradient(ellipse 14% 10% at 51% 69%, #ffd28288, transparent), radial-gradient(ellipse 19% 10% at 45% 91%, #67d53b70, transparent)',
}} />
```

## Lateral whip

Spy video at 00:02.000–00:02.400 and 00:08.600–00:09.200. Give both plates a shared travel direction and cross them at peak apparent motion. Suggested duration 12 frames. This component expects two full-frame scenes and internal clipping.

```tsx
export function Whip({outgoing, incoming}: {outgoing: ReactNode; incoming: ReactNode}) {
  const f = useCurrentFrame();
  const x = interpolate(f, [0, 12], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const smear = 24 * Math.sin(Math.PI * x);
  return <AbsoluteFill style={{overflow: 'hidden'}}>
    {[outgoing, incoming].map((scene, i) => (
      <AbsoluteFill key={i} style={{transform: `translateX(${(i - x) * 100}%)`, filter: `blur(${smear}px)`}}>
        {scene}
      </AbsoluteFill>
    ))}
  </AbsoluteFill>;
}
```

For primarily horizontal blur, replace CSS blur with an SVG filter using feGaussianBlur and stdDeviation equal to “horizontal vertical”, such as “24 2”.

## Phrase reveal on black

Spy opening card is partially visible at 00:04.200 and complete at 00:05.800. Reserve a stable left edge so text never shifts as characters are revealed. Use character timing from the narration markers in your own script.

```tsx
export function Phrase({text}: {text: string}) {
  const f = useCurrentFrame();
  const glyphs = Array.from(text);
  const count = Math.floor(interpolate(f, [0, 48], [0, glyphs.length], clamp));
  return <AbsoluteFill style={{background: '#090a0b', color: '#faf9f5', justifyContent: 'center'}}>
    <div style={{marginLeft: '9%', maxWidth: '82%', font: '112px Caveat'}}>
      {glyphs.slice(0, count).join('')}
    </div>
  </AbsoluteFill>;
}
```

## Sequential quantitative reveal

The spy map adds geographical columns over the course of 00:02.400–00:03.600. Jensen's video uses a board, price labels and a central prop to organize its comparisons in the opening minute. Animate one measure at a time, and keep the label and baseline stable.

```tsx
import { spring, useVideoConfig } from 'remotion';

export function Column({height, order}: {height: number; order: number}) {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rise = spring({frame: f - order * 5, fps, durationInFrames: 14, config: {damping: 22}});
  return <div style={{alignSelf: 'end', width: 72, height, transform: `scaleY(${rise})`,
    transformOrigin: 'bottom', background: 'linear-gradient(0deg,#459343,#c3f679)'}} />;
}
```

## Small facial action

In the spy opening the held pose around 00:06.2–00:07.6 changes mouth at 00:07.8. Author original mouth shapes, and key a short blink to punctuation. Avoid making the entire cutout move for each expression.

```tsx
const blink = interpolate(f, [18, 20, 22], [1, 0.1, 1], clamp);
const mouthPose = f < 45 ? 'open-smile' : 'closed-smile';
// Apply scaleY(blink) to the eyes and choose your authored mouth layer by mouthPose.
```

## Spotlight on an artifact

The spy video's filing, photo and label imagery in the 05:20–05:50 region makes records readable by placing the highest contrast at the active item. The Jensen budget sequence around 05:00 uses a tabletop to place quantities in context.

```css
.artifact-light {
  background: radial-gradient(ellipse 35% 40% at 58% 50%, transparent 35%, #050912b3 100%);
  pointer-events: none;
}
```

## Settling counter

In the crash hook the loss label moves from −$90B at 00:02.8 to −$400B by 00:04.0. Keep the text location fixed and use tabular numerals.

```tsx
const amount = Math.round(interpolate(f, [0, 36], [0, 400], {
  ...clamp, easing: Easing.out(Easing.cubic),
}));
return <span style={{color: '#e14b57', fontVariantNumeric: 'tabular-nums'}}>{'−$' + amount + 'B'}</span>;
```

In JSX, use the expression form below if the literal dollar sign is needed in the label.

```tsx
const label = '−$' + amount + 'B';
```

## Optional damped shake

This is an original implementation proposal. Shake amplitude in the videos is uncertain. Apply to the world plates independently of the type and keep 12 px overscan.

```tsx
export function ImpactLayer({children}: {children: ReactNode}) {
  const f = useCurrentFrame();
  const falloff = interpolate(f, [0, 10], [1, 0], clamp);
  const offset = 6 * falloff * Math.sin(2 * Math.PI * 8 * f / 30);
  return <AbsoluteFill style={{transform: `translateX(${offset}px)`}}>{children}</AbsoluteFill>;
}
```


## Graphic impact

Crash, frames 60–66 on hook_003.jpg. The frame at 61 is predominantly bright, frame 62 alternates to dark with radial streaks, and frames 63–65 retain fading rays over the scene. For an original implementation, a single reduced-amplitude exposure lift and a decaying ray overlay communicate the same emphasis with less contrast reversal. Keep the graphic local to the active object.

```tsx
const impact = interpolate(f, [0, 1, 5], [0.28, 0.22, 0], clamp);
return <AbsoluteFill style={{
  opacity: impact,
  pointerEvents: 'none',
  mixBlendMode: 'screen',
  background: 'repeating-conic-gradient(from 7deg at 64% 40%, #e5ffb2 0deg 0.55deg, transparent 0.55deg 9deg)',
  maskImage: 'radial-gradient(ellipse at 64% 40%, transparent 0 9%, black 17%, transparent 68%)',
}} />;
```

## Nameplate reveal

Spy portrait at 00:06.6–00:07.0. Keep the nameplate visually attached to the subject, with enough inset for a 16:9 crop. Suggested first pass is a 12 px rise and 12-frame mask reveal. Use original names and label proportions.

```tsx
export function Nameplate({name}: {name: string}) {
  const f = useCurrentFrame();
  const reveal = interpolate(f, [0, 12], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  return <div style={{
    position: 'absolute', right: '9%', bottom: '11%',
    background: '#0c1222', color: '#f6ead2', borderLeft: '4px solid #8cf53b',
    padding: '12px 20px', font: '36px Archivo Narrow',
    transform: `translateY(${12 * (1 - reveal)}px)`,
    clipPath: `inset(0 ${100 * (1 - reveal)}% 0 0)`,
  }}>{name}</div>;
}
```

## Focus handoff

The crash candidate triplet at 09:24.600 shows an incoming soft trading floor. The exact defocus duration is uncertain. As a starting point, key a 10 px blur to zero over 8 frames and use a small overscan to cover the softened edges.

```tsx
const blur = interpolate(f, [0, 8], [10, 0], {...clamp, easing: Easing.out(Easing.cubic)});
return <AbsoluteFill style={{transform: 'scale(1.025)', filter: `blur(${blur}px)`}}>{children}</AbsoluteFill>;
```

## Duck keyed to original narration

The measured target across the four source mixes is close to −14.5 LUFS integrated. The following is a starting envelope for your separately authored music. Apply the returned scalar to your Remotion audio component's volume callback using sequence-relative frame numbers. Set the reference bed gain from listening and metering.

```tsx
function bedVolume(frame: number, voiceIn: number, voiceOut: number, baseGain: number) {
  const attack = interpolate(frame, [voiceIn - 4, voiceIn], [0, 1], clamp);
  const release = interpolate(frame, [voiceOut, voiceOut + 12], [1, 0], clamp);
  const duckDb = 5 * Math.min(attack, release);
  return baseGain * 10 ** (-duckDb / 20);
}
```

