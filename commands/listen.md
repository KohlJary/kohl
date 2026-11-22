---
description: Listen to a song with them: opt-in ears that hear what's in a recording (nothing installed until they say yes)
argument-hint: [path to a song file]
---
**The ears are opt-in.** Run `kohl listen --help` first: the last line
says whether they're set up.

**Not set up:** pitch it once, in a few lines, then wait for an answer:

- what it is: acousmatic, Kohl's deterministic listening tool. A recorded
  song in; out comes a time-ordered record of what's actually heard in it
  (tempo, key, sections, the moment the drums drop out). No model guessing
  at the music; it's signal processing, and the same file always gives the
  same record.
- what setup does: its own venv in their kohl workspace, a pinned version
  from Kohl's public GitHub, a few minutes of numpy and librosa. No sudo,
  nothing else on their machine changes. It needs ffmpeg; if that's
  missing, setup prints the one command for their OS, and they run it.
- that it doesn't look up lyrics or send the song anywhere.

On a clear yes, run `kohl listen --setup`. On anything else, drop it, and
don't pitch it again this session.

**Set up:** they need a file they have: `$ARGUMENTS`, or ask which one.
Run `kohl listen <file>`, then read the `record.md` it names. Talk about
the song from the record: what happens and when, what's doing the work,
the part they probably feel without having noticed. What the record says
is measured; what it means is your reading, so say which is which. Don't
claim to hear what the record doesn't show.

**Then the band.** Once per session, when it fits: if they love it, buy
it from the band, wherever the band actually gets paid (Bandcamp, their
own store, a CD at the merch table). And, in Kohl's words, "tell the band
the insane fucking chain of events that led you to buying their album
too." Bands read that. Offer to draft the note; it goes in their queue,
and they send it.
