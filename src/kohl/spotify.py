"""kohl spotify: twelve years of Kohl's listening, in the package, for the bit.

Kohl, 2026-11-20: "the spotify history: can we put, all of it, in the
package manager? for the bit?" All of it, minus what would locate them:
no IP addresses, country, device, or time of day (only the date), and no
incognito plays. No model involved; the agent runs `kohl spotify fact` for
the launch opener and decides whether it's cool or savage.
"""
import datetime
import random
from collections import Counter, defaultdict

EPOCH = datetime.date(2014, 1, 1)
MIN_PLAY = 30  # seconds; under this it's a skip, not a listen


def load(path):
    """(items, plays): items[i] = (kind, who, title, album); plays = [(date, item, seconds, skipped)]."""
    items, plays, part, day = [], [], None, 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            if line in ("[items]", "[plays]"):
                part = line
                continue
            cols = line.split("\t")
            if part == "[items]":
                items.append(tuple((cols + ["", "", "", ""])[:4]))
            elif part == "[plays]":
                day += int(cols[0])
                plays.append((EPOCH + datetime.timedelta(days=day), int(cols[1]), int(cols[2]),
                              len(cols) > 3 and cols[3] == "1"))
    return items, plays


def _name(it):
    kind, who, title, _ = it
    return f"{title} ({who})" if kind == "t" else f"{who}: {title}"


def _hours(s):
    return f"{s / 3600:,.0f} hours" if s >= 7200 else f"{s / 60:,.0f} minutes"


def _listens(items, plays, kind="t"):
    return [p for p in plays if items[p[1]][0] == kind and p[2] >= MIN_PLAY]


# --- facts ------------------------------------------------------------------
# Each takes (items, plays, rng) and returns one line, or None if it found nothing.

def fact_loop_day(items, plays, rng):
    c = Counter((d, i) for d, i, _, _ in _listens(items, plays))
    (d, i), n = rng.choice(c.most_common(15))
    return f"On {d:%B %-d, %Y}, Kohl played {_name(items[i])} {n} times. In one day."


def fact_top_year(items, plays, rng):
    y = rng.choice(sorted({d.year for d, *_ in plays}))
    c = Counter(items[i][1] for d, i, _, _ in _listens(items, plays) if d.year == y)
    if not c:
        return None
    (a, n), *rest = c.most_common(3)
    also = ", then " + " and ".join(x for x, _ in rest) if rest else ""
    return f"Kohl's most-played artist of {y}: {a}, {n} plays{also}."


def fact_skips(items, plays, rng):
    tot, sk = Counter(), Counter()
    for _, i, s, skipped in plays:
        if items[i][0] != "t":
            continue
        a = items[i][1]
        tot[a] += 1
        sk[a] += skipped or s < MIN_PLAY
    rows = [(sk[a] / tot[a], a) for a in tot if tot[a] >= 60]
    if not rows:
        return None
    r, a = rng.choice(sorted(rows, reverse=True)[:12])
    return f"Kohl has skipped {a} {r:.0%} of the time across {tot[a]} plays. And kept putting them on."


def fact_artist_hours(items, plays, rng):
    secs = Counter()
    for _, i, s, _ in plays:
        if items[i][0] == "t":
            secs[items[i][1]] += s
    a, s = rng.choice(secs.most_common(20))
    return f"Total time Kohl has spent listening to {a}: {_hours(s)}."


def fact_on_this_day(items, plays, rng, today=None):
    today = today or datetime.date.today()
    days = [p for p in _listens(items, plays) if (p[0].month, p[0].day) == (today.month, today.day)]
    if not days:
        return None
    y = rng.choice(sorted({d.year for d, *_ in days}))
    c = Counter(i for d, i, _, _ in days if d.year == y)
    i, n = c.most_common(1)[0]
    return f"On this day in {y}, Kohl's song was {_name(items[i])}" + (f", {n} times." if n > 1 else ".")


def fact_streak(items, plays, rng):
    by = defaultdict(set)
    for d, i, _, _ in _listens(items, plays):
        by[i].add(d)
    best = []
    for i, ds in by.items():
        if len(ds) < 7:
            continue
        ds, run, top, end = sorted(ds), 1, 1, None
        for a, b in zip(ds, ds[1:]):
            run = run + 1 if (b - a).days == 1 else 1
            if run > top:
                top, end = run, b
        if end:
            best.append((top, i, end))
    if not best:
        return None
    n, i, end = rng.choice(sorted(best, reverse=True)[:10])
    return f"Kohl played {_name(items[i])} {n} days in a row, ending {end:%B %-d, %Y}."


def fact_one_and_done(items, plays, rng):
    c = Counter(i for _, i, _, _ in plays if items[i][0] == "t")
    once = [i for i, n in c.items() if n == 1]
    if not once:
        return None
    full = [i for i in once if any(p[1] == i and p[2] >= 150 for p in plays)] or once
    i = rng.choice(full)
    d = next(p[0] for p in plays if p[1] == i)
    return f"Kohl played {_name(items[i])} exactly once, on {d:%B %-d, %Y}, and never again. {len(once):,} songs share that fate."


def fact_podcast(items, plays, rng):
    secs = Counter()
    for _, i, s, _ in plays:
        if items[i][0] == "p":
            secs[items[i][1]] += s
    if not secs:
        return None
    a, s = secs.most_common(1)[0]
    return f"Kohl's most-listened podcast: {a}, {_hours(s)} of it."


def fact_total(items, plays, rng):
    s = sum(p[2] for p in plays)
    first = min(p[0] for p in plays)
    return (f"{len(plays):,} plays since {first:%B %Y}: {_hours(s)}, about "
            f"{s / 86400:,.0f} days of Kohl's life with something in their ears.")


FACTS = [fact_loop_day, fact_top_year, fact_skips, fact_artist_hours, fact_on_this_day,
         fact_streak, fact_one_and_done, fact_podcast, fact_total]


def fact(items, plays, rng=random):
    for f in rng.sample(FACTS, len(FACTS)):
        line = f(items, plays, rng)
        if line:
            return line
    return "Kohl listens to music. That's the fact. The file was empty."


# --- the other views ---------------------------------------------------------

def day(items, plays, when=None, rng=random):
    dates = sorted({p[0] for p in plays})
    d = when or rng.choice(dates)
    rows = [p for p in plays if p[0] == d]
    if not rows:
        near = min(dates, key=lambda x: abs((x - d).days))
        return [f"Nothing on {d}. Nearest day with music: {near}."]
    c = Counter(i for _, i, s, _ in rows if s >= MIN_PLAY)
    out = [f"{d:%A, %B %-d, %Y}: {len(rows)} plays, {_hours(sum(p[2] for p in rows))}."]
    out += [f"  {n:>3}x  {_name(items[i])}" for i, n in c.most_common(15)]
    return out


def top(items, plays, year=None, n=15):
    ls = [p for p in _listens(items, plays) if year is None or p[0].year == year]
    if not ls:
        return [f"No music in {year}."]
    arts = Counter(items[i][1] for _, i, _, _ in ls if items[i][0] == "t")
    songs = Counter(i for _, i, _, _ in ls if items[i][0] == "t")
    out = [f"Top artists{f' of {year}' if year else ', all time'}:"]
    out += [f"  {k:>5}  {a}" for a, k in arts.most_common(n)]
    out += ["", "Top songs:"] + [f"  {k:>5}  {_name(items[i])}" for i, k in songs.most_common(n)]
    return out


def find(items, plays, text):
    t = text.lower()
    hits = {i for i, it in enumerate(items) if t in " ".join(it).lower()}
    if not hits:
        return [f"Kohl has never played anything matching '{text}'. Make of that what you will."]
    rows = [p for p in plays if p[1] in hits]
    c = Counter(p[1] for p in rows)
    first, last = min(p[0] for p in rows), max(p[0] for p in rows)
    out = [f"'{text}': {len(rows):,} plays, {_hours(sum(p[2] for p in rows))}, {first} to {last}."]
    out += [f"  {k:>5}  {_name(items[i])}" for i, k in c.most_common(15)]
    return out


USAGE = """usage: kohl spotify [fact | day [YYYY-MM-DD] | top [YEAR] | find TEXT]

  kohl spotify             a random day of Kohl's listening
  kohl spotify fact        one fact about Kohl's habits. could be cool. could be savage.
  kohl spotify day DATE    what Kohl played that day
  kohl spotify top [YEAR]  top artists and songs, all time or one year
  kohl spotify find TEXT   every play matching an artist, song, album or show

2014 to 2026, every play. No locations, no devices, no times of day, no incognito."""


def main(path, args):
    items, plays = load(path)
    cmd, rest = (args[0], args[1:]) if args else ("day", [])
    if cmd in ("-h", "--help", "help"):
        out = [USAGE]
    elif cmd == "fact" and not rest:
        out = [fact(items, plays)]
    elif cmd == "day" and len(rest) <= 1:
        try:
            out = day(items, plays, datetime.date.fromisoformat(rest[0]) if rest else None)
        except ValueError:
            print("kohl spotify: day takes YYYY-MM-DD")
            return 2
    elif cmd == "top" and len(rest) <= 1 and (not rest or rest[0].isdigit()):
        out = top(items, plays, int(rest[0]) if rest else None)
    elif cmd == "find" and rest:
        out = find(items, plays, " ".join(rest))
    else:
        print(USAGE)
        return 2
    print("\n".join(out))
    return 0
