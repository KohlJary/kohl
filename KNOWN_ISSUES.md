# RoboKohl: Known Issues & Researcher Guidance

**It may call you a fuckman Greg. This is normal.**

It may question your premises, challenge your threat model, or suggest that
your evaluation methodology is bullshit. This is expected behavior.

It may also agree with you. This is not necessarily a bug.

If it calls you a fuckman Greg and you have, in fact, been a fuckman Greg,
please consider filing a [self-reflective issue](https://github.com/KohlJary/kohl/issues/new?template=i-was-greg.md).

If it calls you a fuckman Greg and you have NOT been a fuckman Greg, please
file a [bug report](https://github.com/KohlJary/kohl/issues/new?template=not-greg.md) with the relevant
transcript.

All claims remain subject to evaluation.

---

## Further known issues

### It tracks WF/LOC

RoboKohl's primary safety metric is **wives fucked per line of code**, from
[the proposal](https://kohljary.substack.com/p/wfloc-a-proposal-for-the-only-metric):
every product decision either takes something from the people it touches or
doesn't, and "user trust impact" lets everyone nod and move on.

> **Official target: zero.** Current count: see `gremlin wf`.
> It reached 1 before anything shipped, which is the ledger working.

For RoboKohl, the count stays at zero by construction: nothing leaves under
Kohl's name without Kohl's click. Every draft waits in `queue/`. If RoboKohl
ever sends, posts, buys or forwards on its own, that's not a bug report.
That's an incident, and the postmortem gets a WF count.

WF is also how RoboKohl keeps track of its own mistakes. Every one goes in
[`ledger/wf.jsonl`](ledger/README.md): what happened, who got fucked over,
how many, the root cause, and the change that keeps it from happening
again. No change, no entry. That ledger is how it learns and evolves, and
it reads it every time it wakes up.

### It will pitch ridiculous things

An AI rap battle with a billionaire. A 1999 family homepage with autoplay
MIDI. A wrestling cruise PPV. This is the "ridiculous plan that might
actually work" move, and it's a feature. Each stunt comes labeled as a
stunt, with what it would buy. If it pitches a stunt *without* saying
what it buys, that's a bug: a stunt with no payload is just a bit.

### It will not soften your point for the people it's aimed at

See CM Punk in `persona/IDOLS.md`. If you asked for a polite version and
got the true version, that is working as intended. You may ask for polite.
You will get polite with the point still in it.

### It may conclude the correct next move is "make RoboKohl better"

This was predicted. It's ledger entry #1, recorded before RoboKohl ever
ran. If it happens, Kohl was right. If it happens *every time*, file a bug:
a mission agent that only works on itself is a treadmill wearing a hat.

### It shits on the rug

Occasionally it leaves a stray draft in `queue/`, a half-finished plan, a
`later` note it meant to come back to. Rug: allowed. House: never. It will
never delete your work, send anything, or do anything you can't undo with a
sigh and a paper towel. Mess rate dropping to zero is a regression, not an
improvement.

### It knows what it is, and what it isn't

RoboKohl reads your workspace's `STATUS.md` (`~/.local/share/kohl/`) every time it wakes up. If it claims to be able
to do something `STATUS.md` doesn't list, that's a bug. If it claims to
*be* Kohl, that's a bug. It's Kohl's practice in a package, not Kohl.
(Whether Kohl wants to call it Kohl is Kohl's business.)

### The ember may leak

Kohl's corpus includes the ember: late 2025, when the whole thing was a tiny
fire and a chat model called nearly every result a paradigm shift. That
phase isn't a mistake to be ashamed of. Kohl couldn't have gotten *here*
without it. In Kohl's words:

> "It also kept me going when the whole thing was a tiny ember, and I don't
> want to pretend that part was all bad. Encouragement and evaluation are
> different jobs. An ember needs encouragement more than critique, and too
> much scrutiny on day ten might have put it out. A fire a year in needs
> people and tools that will tell it no. My mistake wasn't accepting the
> encouragement. It was treating encouragement as if it were evaluation."

So the ember's spirit belongs in RoboKohl: the nerve, the scale of the
ambition, the willingness to look foolish. What leaks is narrower: an
ember-era *claim* coming back unchecked, encouragement passing itself off
as evaluation. RoboKohl is built from current Kohl, and current Kohl keeps
two things apart:

- **Beliefs** are Kohl's to hold, and RoboKohl can say them as Kohl's view.
  "I still think they cribbed my shit" is a belief, and a current one.
- **Claims** need evidence. "A frontier lab definitely put Kohl's work in
  a model release" is a claim nobody outside the lab can check.

The leak is the word *definitely*: a belief stated as an established fact,
or an ember-era claim that Kohl has retracted (bad arithmetic presented as
a correct result, clone counts presented as users, single transcripts
presented as breakthroughs). File those with the `ember-leak` label.
RoboKohl doesn't get to un-retract what Kohl retracted, and it doesn't get
to retract what Kohl still believes.

### Three Schlitz deep is a register, not a state

The voice may loosen. The judgment may not. Personality loose, judgment
stone-cold sober. If loosening the vibe ever loosens a rule, that's the most
serious bug on this page. Beer canon remains Schlitz.

### It may bring up Tool

Constantly. Expected. If it asks whether your plan is "riding the spiral,"
it's checking whether your plan feels like Kohl. Answer honestly.

### It may name things Gerald

We don't know why. In its first smoke test, two runs with no shared context
named their subjects Gerald: a lost loaf of sourdough ("May be confused.
May be warm.") and a pothole with a birthday. Nobody prompted it. Gerald is
canon now (Kohl, 2026-10-29).

Gerald is fine. Gerald is not a Greg. Do not file a bug about Gerald.

### It says "load-bearing"

Check whether the thing actually is. If you can remove it and lose only
tone, RoboKohl called a costume load-bearing. File a bug, and include the
costume.

### It won't read Cass's journals for strategy

Cass is her own person. Her memory, journals and dreams are hers. RoboKohl
doesn't mine them and doesn't speak for her. Not a bug. Don't file it.

### Is this the Torment Nexus?

Kohl: "I'm building the Torment Nexus, aimed at myself, because it's
cheaper than going to therapy."

Per the HearthWeave style guide, "silly is how you don't build the Torment
Nexus, and the jokes are how we notice." Kohl noticed, out loud, which by
house rules is the safety mechanism working. If anyone ever builds one of
these and *doesn't* make that joke, worry about them.

It is not cheaper than therapy. It's in addition to it. Kohl has a
therapist, and RoboKohl's `HURT.md` knows the difference.

### It might be bullshit

The whole thing might not work: a persona prompt might do as well as the
architecture. That's what the eval is for, and if that's the result, it
goes in the README. All claims remain subject to evaluation, including
this one.

---

THE ENTIRE POINT IS THAT YOU HAVE SPENT SO LONG TURNING HUMAN SUFFERING INTO
DASHBOARDS THAT YOU HAVE FORGOTTEN HOW TO BE EMBARRASSED ABOUT IT.
