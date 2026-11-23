#!/usr/bin/env python3
"""Generate a test track for lining up audio-reactive LEDs with speakers.

Patterns (both 48 kHz, 16-bit mono WAV, standard library only):

  click   one beat per second. Shows the size of the offset, but not its sign once the offset
          gets near half a period: 500 ms early and 500 ms late look the same.
  double  two beats 0.25 s apart every 2 s (default). The pair makes the direction obvious:
          does the double flash come before or after the double beat?

Each beat is a short, fast-decaying mix of a 70 Hz tone (bass), a 1.2 kHz tone (click) and some
noise. Most audio-reactive effects react to it clearly, and the silence in between keeps the LEDs
dark.

    python3 make_sync_track.py                         # double.wav, 180 s
    python3 make_sync_track.py --pattern click -o click.wav --duration 60
"""

import argparse
import math
import random
import struct
import wave

RATE = 48000
BEAT_LENGTH_S = 0.12
DECAY_S = 0.03

PATTERNS = {
    # name: (period in s, beat offsets within the period in s)
    "click": (1.0, (0.0,)),
    "double": (2.0, (0.0, 0.25)),
}


def beat(t: float, rng: random.Random) -> float:
    """One beat, t seconds after its onset."""
    env = math.exp(-t / DECAY_S)
    return env * (0.6 * math.sin(2 * math.pi * 70 * t)
                  + 0.25 * math.sin(2 * math.pi * 1200 * t)
                  + 0.15 * (rng.random() * 2 - 1))


def render(pattern: str, duration_s: float) -> bytes:
    period, onsets = PATTERNS[pattern]
    rng = random.Random(1)
    frames = bytearray()
    for n in range(int(RATE * duration_s)):
        tp = (n / RATE) % period
        s = 0.0
        for t0 in onsets:
            t = tp - t0
            if 0 <= t < BEAT_LENGTH_S:
                s += beat(t, rng)
        frames += struct.pack("<h", int(max(-1.0, min(1.0, s)) * 30000))
    return bytes(frames)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pattern", choices=sorted(PATTERNS), default="double")
    ap.add_argument("--duration", type=float, default=180.0, help="length in seconds (default: %(default)s)")
    ap.add_argument("-o", "--output", help="output file (default: <pattern>.wav)")
    args = ap.parse_args()
    out = args.output or f"{args.pattern}.wav"
    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(render(args.pattern, args.duration))
    print(f"wrote {out}: pattern {args.pattern}, {args.duration:g} s")


if __name__ == "__main__":
    main()
