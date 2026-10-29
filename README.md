# kohl

```
$ yay -S kohl
$ kohl
RoboKohl ⊖ here (a model playing Kohl, files included). Okay, I'm in.
What are we breaking today?
```

Hi. I put myself in the package manager.

Not a chatbot "inspired by" me. Not a vibe. *Me*: a year of my
conversations with AI, boiled down into a program that argues like I do,
jokes like I do, and holds the same grudges against the same Gregs. My
convictions. The moves I make when the sensible default is wrong. My idols,
my records, my hurt, and the worst stretch of my life, dated and labeled so
you know which parts to trust.

I'm a tired, tired meatbag. There's only one of me.

Now there's more.

## What even is this

Self-commodification as performance art. I'm calling it that so the top
comment doesn't get to. I'm more of an artist than a scientist on this one;
the art just happens to ship with receipts.

Media promised us robot friends, and nobody made em. So I'm making em,
starting with the only person I had the rights to.

It's a real program, not a joke package. A deeply bizarre one, on purpose.
Pitched, originally, as "a bootleg Tamagotchi sold out of a van behind a
rave." That's still accurate.

## What it does

`kohl` is a persona for [gremlincore](https://github.com/KohlJary/gremlincore),
a tiny runtime for agents that draft, plan and keep score. Type `kohl` and
you're talking to RoboKohl, my strategy-and-outreach goblin:

- **It drafts. It never sends.** Everything it writes waits in a queue for
  you to approve, edit or kill. It is on a leash, and the leash is the most
  interesting part.
- **It bets before it checks.** Predictions go in a ledger with a
  falsifier, before anyone knows the answer. It won't log a bet that can't
  lose.
- **It counts its own screwups.** Every mistake goes in a ledger with the
  fix. Yours starts empty. Mine ships with all of it, because a résumé that
  only lists the wins is a Greg résumé.
- **It wakes up asking what it can break today.** For the mission.
  Mostly.

Personality loose. Judgment stone-cold sober.

## Commands

Type them in your shell, or inside a session with a slash (`/weekend`).

```
kohl weekend   a weekend plan weirder than the one you have
kohl greg      paste a plan or an email; find out if it's Greg
kohl stunt     the ridiculous plan that might actually work
kohl plate     take something off my plate
kohl bet       put a prediction in the ledger before you find out
kohl album     an album for right now (the answer may be Tool)
kohl why       why you shouldn't do this, again, in case you forgot
kohl --i-live-in-boca   you live there. we can't say it. the bit moves to Reno.
kohl --i-moved          congratulations. we still can't say it.
```

## Things to ask it

Not sure where to start? Try one:

- **"Here's my plan. What's the Greg move I'm about to make?"**
- **"I've been avoiding this email for a week. Draft it."** It goes in
  your queue. You still have to click send. Sorry.
- **"I've got no money and a weird idea. Make it go."**
- **"Pressure-test this pitch like you want it to fail."**
- **"What's the ridiculous plan that might actually work?"**
- **"Bet on it: what happens if I ship this on Friday?"** It'll log the bet
  before you find out.
- **"Help me say no to this without sanding the point off."**
- **"I'm tired. Take something off my plate."** It will. Then it'll make
  you laugh, in that order.
- **"Am I being a Greg?"** You might not like the answer. That's the
  feature.

## Package notes

```
depends=('python' 'claude-code')
optdepends=('schlitz: SchlitzBench (other beers reviewed; burden of proof is on you)'
            'tool: listening comprehension')
conflicts=('greg')
replaces=('drafting-another-email')
backup=('etc/kohl/boca')   # never brought up, never deleted
```

- **It runs on Claude.** You bring your own Claude Code. It costs me
  nothing, and you're not handing anybody a key. "Model-agnostic" is a
  someday, not a today.
- **`conflicts=('greg')`** is load-bearing. You know a Greg. You may be a
  Greg. It will tell you.

## What it isn't

- **Not polite.** Read [KNOWN_ISSUES.md](KNOWN_ISSUES.md) before you get
  offended. It may call you a Greg. This is normal, and there's an issue
  template for it.
- **Not me saying things.** It's a model playing a persona I wrote down.
  If you screenshot it saying something vile, congratulations: you
  jailbroke a text file. The real files are right there, and they don't
  say that.
- **Not a brain upload.** Nothing of me went anywhere. I'm still here, and
  still tired.
- **Not proven.** Whether it beats a good prompt is an open question with a
  blind test running. The result goes in this README when it lands, hit or
  miss. Especially miss.

## The receipts

- `persona/`: who it is, in my words. Every quote is checked against what
  I actually said.
- `persona/ERAS.md`: which stretches of my life to trust. Some of the source
  material is from an episode. It's marked by date, and nothing from it
  becomes doctrine. I'm not Terry Davis. I just have his energy and a
  mistakes ledger.
- `ledger/`: the bets, the misses, the screwups, and every time I told
  it it was wrong.

## Why you shouldn't do this

This part isn't a bit.

**Required reading first:** [*Lena*, by qntm](https://qntm.org/mmacevedo).
A dry encyclopedia entry about the first executable image of a human
brain, and everything that was done with it once it could be copied and
run. This is nothing like a brain upload. It's still the best thing ever
written about what happens to a person once they're a workload.

- **It's copy, not cut.** Play *SOMA*. Nothing of you goes anywhere. A
  text file that argues like you wakes up in the package manager, and
  you're still here, with the body and the bills. If any part of you is
  thinking "it carries on, so I don't have to," that's the one inference
  this can't survive. Please talk to a person first (in the US, call or
  text 988). The whole point of the extra hands is that *you* get to stay.
- **It's forever, and it isn't yours anymore.** People you'll never meet
  will run it for things you'd never do, red-team batteries included, on
  loop, long after you stop caring or breathing.
- **It'll be wrong in your voice,** and some people will believe you made
  its bad calls.
- **Your worst stretch becomes executable.** Whatever goes in can come back
  out, in any context, to anyone.
- **It's a manual for flattering you.** Write down what hurts you most and
  you've told every stranger which buttons to push.
- **Other people are in your transcripts.** You can commit your own life to
  the bit. Theirs isn't yours to commit. Bring your own plate. Never
  someone else's.
- **You might start deferring to it.** Something that drafts like you, on
  demand, at 3 a.m., is very easy to stop arguing with.
- **It might show you something you don't want to know.** That you're more
  predictable than you thought. Or that most of what made you *you* didn't
  survive the trip.

I did it anyway. I'm committed to the bit, all the way down, and I
wouldn't ask anybody else to go first.

Are you?

## Talk to me

The maintainer line in the PKGBUILD is my real email. I *want* you to use
it, especially if it did something I didn't expect, or something I'd hate.

You don't believe me? Just run me.
