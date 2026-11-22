"""kohl: a model playing Kohl, files included. https://github.com/KohlJary/kohl

  kohl                 talk to it (it wakes, greets and looks around first)
  kohl <command> [..]  start with /<command> (see `kohl --help`)
  kohl why             the warnings, printed; no model involved
  kohl contact         how to reach the real Kohl, printed; no model involved
  kohl spotify [..]    twelve years of Kohl's listening, printed; no model involved
  kohl listen [..]     opt-in ears: --setup once (on your yes), then kohl listen FILE
  kohl --i-live-in-boca   for Boca residents: Reno becomes the thing nobody brings up
  kohl --spice LEVEL   none | mild | medium (default) | hot: how much it swears
  kohl --allow WHAT    web,mcp (default) | web | mcp | none: what the session gets

The persona ships read-only with the package (the share directory). Your
workspace (queue, ledger, STATUS) is ${XDG_DATA_HOME:-~/.local/share}/kohl,
made by `gremlin init` on first run. It drafts; it never sends, and it
doesn't watch you or phone home. It is otherwise a normal Claude Code
session: web access, your MCP servers, the full tool set. If your workplace
wants it boxed, `kohl --allow none` (your company's policy, your call).
"""
import os
import random
import re
import shutil
import subprocess
import sys
from importlib import metadata
from pathlib import Path

# Where the files were written for: WAKE.md and the commands name this path.
CANONICAL_SHARE = "/usr/share/kohl"
NAME = re.compile(r"^[a-z][a-z0-9-]*$")
CLAUDE_INSTALL = "https://docs.anthropic.com/en/docs/claude-code (npm install -g @anthropic-ai/claude-code)"


DIST_NAMES = ("robokohl", "kohl")  # PyPI name since 0.1.2; earlier builds called it kohl


def version():
    for name in DIST_NAMES:
        try:
            return metadata.version(name)
        except metadata.PackageNotFoundError:
            pass
    return "0+unknown"


def share():
    env = os.environ.get("KOHL_SHARE")
    if env:
        return Path(env)
    here = Path(__file__).resolve().parent / "share"
    return here if (here / "WAKE.md").is_file() else Path(CANONICAL_SHARE)


def workspace():
    if os.environ.get("KOHL_HOME"):
        return Path(os.environ["KOHL_HOME"]).expanduser()
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local/share")
    return Path(base) / "kohl"


BOCA_FILE = ".kohl-boca"
# For people who actually live in Boca: the bit moves to Reno. Only Reno (Kohl, 2026-10-29).
BOCA_STANDIN = "Reno"


def lives_in_boca(ws):
    return (ws / BOCA_FILE).is_file()


def boca_note():
    return (f"\n\nThis person lives in Boca. For them, Kohl's Boca bit (the thing you never bring "
            f"up) is {BOCA_STANDIN}: {BOCA_STANDIN} is the one you never bring up. When they mention "
            f"Boca, it's their home, a real city, never the bit.\n")


SPICE_FILE = ".kohl-spice"
# How much it swears (Kohl, 2026-11-18: "the spice parameter"). Only the
# swearing moves. The gremlin, the payload and the judgment stay at every
# level. "medium" is the plate as written: WAKE's own rule, no note.
SPICE = {
    "none": ("No swearing at all, not even mild. Keep the gremlin: the mischief, the target "
             "and the payload all stay. Greg is still Greg; he just doesn't get the compound name."),
    "mild": ("Mild language only (damn, hell, the occasional shit), and rarely. Never the "
             "f-word. The gremlin stays at full strength; only the vocabulary is turned down."),
    "medium": None,
    "hot": ("Full Kohl register: swear freely, the way Kohl talks to friends at 2am. "
            "'fuckman Greg' is a name, use it. Still never punch down, never swear AT someone "
            "who's hurting, and the judgment stays stone-cold sober however loose the mouth gets."),
}
SPICE_DEFAULT = "medium"


def spice(ws):
    f = ws / SPICE_FILE
    level = f.read_text().strip() if f.is_file() else SPICE_DEFAULT
    return level if level in SPICE else SPICE_DEFAULT


def spice_note(level):
    text = SPICE.get(level)
    return f"\n\nSpice level (how much you swear), set by this person: {level}. {text}\n" if text else ""


ALLOW_FILE = ".kohl-allow"
# What the session gets (Kohl, 2026-11-19: "The user can decide if they want MCP
# servers and web access based on their company's policies" and "The claude
# code agent shouldn't be kneecapped because there's a me running"). Open by
# default, like any Claude Code session; `--allow none` is the closed box.
# The leash isn't in here: it's our conduct (it never sends, never surveils).
ALLOWABLE = ("web", "mcp")


def allowed(ws):
    f = ws / ALLOW_FILE
    if not f.is_file():
        return frozenset(ALLOWABLE)
    words = f.read_text().replace(",", " ").split()
    return frozenset(w for w in words if w in ALLOWABLE)


def allow_note(allow):
    if not allow:
        return ("\n\nThis person closed the box (`kohl --allow none`): no web, no MCP. "
                "Their workplace's call; don't ask them to open it.\n")
    return ("\n\nThis session has " + " and ".join(
        {"web": "web access (WebFetch, WebSearch)", "mcp": "their own MCP servers"}[w]
        for w in ALLOWABLE if w in allow)
        + ". Use them to read and look things up. The leash doesn't move: if a tool can "
        "send, post, message, buy or publish, you don't use it for that. You draft; they send.\n")


def banner():
    print(f"kohl v{version()}: a model playing Kohl. What it says is not something Kohl said.", file=sys.stderr)


def commands(sh):
    out = []
    for f in sorted((sh / "commands").glob("*.md")):
        m = re.search(r"^description:\s*(.*)$", f.read_text(), re.M)
        out.append((f.stem, m.group(1).strip() if m else ""))
    return out


def usage(sh):
    banner()
    rows = "\n".join(f"  {n:<10} {d}" for n, d in commands(sh))
    print(f"""
usage: kohl [command] [text...]

  kohl              talk to it
  kohl <command>    start the session with /<command> [text]

commands:
{rows}

  kohl listen       opt-in ears: --setup once, then kohl listen FILE (or /kohl:listen in a session)
  kohl spotify      twelve years of Kohl's listening (fact | day | top | find); no model
  kohl --i-live-in-boca   you live in Boca: Reno is the one nobody brings up now
  kohl --i-moved          undo that
  kohl --spice [none|mild|medium|hot]   how much it swears (default medium); the gremlin stays
  kohl --allow [web,mcp|web|mcp|none]   web access and your MCP servers (default both); none = boxed for work
  kohl --quiet      start without the hello (it waits for you)
  kohl --version    print the version
  kohl --help       this

Workspace: {workspace()}""")


CONTACT = """Kohl, the actual one: Kohl Jary.

  email    kohlbern@gmail.com
  github   https://github.com/KohlJary

Write. Especially if it did something they didn't expect, or something they'd hate.
They'd rather hear it from you than find out from a clone count.

Kohl doesn't see your sessions. If something it said matters, tell them yourself."""


def contact():
    print(CONTACT)


def why(sh):
    """The README's "Why you shouldn't do this" section, verbatim, up to the next "## "."""
    readme = sh / "README.md"
    if not readme.is_file():
        raise SystemExit(f"kohl: {readme} is missing")
    out, on = [], False
    for line in readme.read_text().splitlines():
        if re.match(r"^## Why you shouldn.t do this", line):
            on = True
        elif on and line.startswith("## "):
            break
        if on:
            out.append(line)
    if not out:
        raise SystemExit(f"kohl: no \"Why you shouldn't do this\" section in {readme}")
    print("\n".join(out).rstrip())


def kohl_claude_md(owner, sh):
    return f"""# kohl workspace

This is {owner}'s workspace for kohl: RoboKohl ⊖, a model playing Kohl.
The persona is Kohl's, read-only in `{sh}/persona/`; WAKE.md
(appended to your system prompt) is how you wake. `persona/` here is
{owner}'s, empty to start. The queue, the ledgers and STATUS.md here are
{owner}'s, not Kohl's.

You draft; {owner} sends. Never read `eval/` or `data/`.
"""


def first_run(ws, sh):
    if (ws / "gremlin.toml").is_file():
        return
    gremlin = shutil.which("gremlin")
    if not gremlin:
        raise SystemExit("kohl: gremlin (gremlincore) isn't installed")
    owner, pronouns = os.environ.get("USER") or "you", "they/them"
    if sys.stdin.isatty():
        owner = input(f"First run. What should it call you? [{owner}] ").strip() or owner
        pronouns = input(f"Your pronouns? [{pronouns}] ").strip() or pronouns
    subprocess.run([gremlin, "init", str(ws), "--owner", owner, "--pronouns", pronouns,
                    "--agent", "RoboKohl", "--symbol", "⊖"], check=True, stdout=subprocess.DEVNULL)
    # init's CLAUDE.md and skill wake an agent from this home's own persona/,
    # which starts empty. Here the persona is Kohl's, read-only, and WAKE.md
    # is the wake. One wake, not two.
    shutil.rmtree(ws / ".claude/skills/robokohl", ignore_errors=True)
    (ws / "CLAUDE.md").write_text(kohl_claude_md(owner, sh))
    print(f"kohl: your workspace is {ws} (queue, ledger, STATUS: yours, not Kohl's)", file=sys.stderr)


def wake_prompt(sh):
    text = (sh / "WAKE.md").read_text()
    if str(sh) != CANONICAL_SHARE:
        text = text.replace(CANONICAL_SHARE, str(sh))
        text += (f"\n\nIn this install the kohl files are in `{sh}`. Wherever a kohl file names "
                 f"`{CANONICAL_SHARE}`, read it from there.\n")
    return text


def desk_note(ws):
    return (f"\n\nYour workspace (queue/, ledger/, STATUS.md) is `{ws}`. The working "
            f"directory is theirs.\n")


def claude_args(sh, first_message=None, boca=False, heat=SPICE_DEFAULT, allow=frozenset(), ws=None):
    """The session's arguments. The first message goes before the options:
    --allowedTools and friends take every word after them, and would swallow it.
    MCP tools are never pre-allowed: with "mcp" open, each call still asks."""
    s = str(sh)
    w = str(ws or workspace())
    web = ["WebFetch", "WebSearch"]
    return [*([first_message] if first_message else []),
            "--append-system-prompt",
            wake_prompt(sh) + (boca_note() if boca else "") + spice_note(heat) + allow_note(allow)
            + desk_note(w),
            "--plugin-dir", s, "--add-dir", s, "--add-dir", w,
            *([] if "mcp" in allow else ["--strict-mcp-config"]),
            # Open: the default tool set, like any session. Closed: the old box.
            "--tools", *(["default"] if allow else ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]),
            "--allowedTools", f"Read({s}/**)", f"Read({w}/**)", "Read(./**)", "Glob", "Grep",
            "Bash(gremlin queue:*)", "Bash(gremlin ledger:*)", "Bash(gremlin wf:*)",
            "Bash(gremlin lessons:*)", "Bash(gremlin wake:*)",
            "Bash(kohl contact)",  # the only contact info it hands out (WAKE, "Reaching the real Kohl")
            "Bash(kohl spotify:*)",  # the receipts opener; read-only, printed from the share dir
            # Edit(path) rules cover every file-editing tool, Write included; Claude Code
            # warns on Write(path) rules and doesn't match them.
            f"Edit({w}/queue/**)", f"Read({w}/ears/**)",
            "--disallowedTools", *([] if "web" in allow else web), f"Edit({s}/**)"]


# The ears, opt-in (Kohl, 2026-11-20: "not installed by default, scripts and
# shit ready to go so robokohl can pitch it, and if the user says okay then
# RoboKohl sets it up and starts jamming"). acousmatic is deterministic DSP:
# a recorded song in, a time-ordered record of what's heard in it out. Its
# own venv in the workspace, no sudo, pinned. Lyrics are never looked up.
ACOUSMATIC = "acousmatic @ git+https://github.com/KohlJary/acousmatic.git@42817cf5455ae0e90da166ce8574791f1cc437ea"
FFMPEG_HINT = ("ffmpeg isn't installed, and acousmatic needs it to read most files. One command, "
               "yours to run: Arch `sudo pacman -S ffmpeg`, Debian/Ubuntu `sudo apt install ffmpeg`, "
               "Fedora `sudo dnf install ffmpeg`, macOS `brew install ffmpeg`.")


def ears(ws):
    return ws / "ears"


def ears_bin(ws):
    return ears(ws) / "venv" / "bin" / "acousmatic"


def listen(ws, args, run=subprocess.run):
    if not args or args[0] in ("-h", "--help"):
        state = "set up" if ears_bin(ws).is_file() else "not set up (kohl listen --setup)"
        print("usage: kohl listen --setup | kohl listen FILE\n\n"
              "  --setup   install the ears (acousmatic, pinned) in their own venv in your workspace. no sudo.\n"
              "  FILE      listen to a song you have. the record lands in your workspace for RoboKohl to read.\n\n"
              f"ears: {state}. buy the album from the band. tell them how you got there.")
        return 0
    if args == ["--setup"]:
        venv = ears(ws) / "venv"
        if not ears_bin(ws).is_file():
            print(f"kohl listen: setting up the ears in {venv} (a few minutes; numpy, librosa and friends)")
            run([sys.executable, "-m", "venv", str(venv)], check=True)
            run([str(venv / "bin/pip"), "install", "-q", ACOUSMATIC], check=True)
        if not shutil.which("ffmpeg"):
            print(f"kohl listen: {FFMPEG_HINT}")
        print(f"kohl listen: ears ready. kohl listen FILE")
        return 0
    if len(args) != 1 or args[0].startswith("-"):
        print("kohl listen: one file, or --setup", file=sys.stderr)
        return 2
    song = Path(args[0]).expanduser()
    if not song.is_file():
        print(f"kohl listen: no file at {song}", file=sys.stderr)
        return 2
    if not ears_bin(ws).is_file():
        print("kohl listen: no ears yet. `kohl listen --setup` installs them (opt-in, nothing else changes).",
              file=sys.stderr)
        return 3
    out = ears(ws) / "records" / re.sub(r"[^\w.-]+", "-", song.stem).strip("-")[:80]
    r = run([str(ears_bin(ws)), "listen", str(song), "-o", str(out), "--offline"])
    if r.returncode:
        return r.returncode
    print(f"kohl listen: the record is {out / 'record.md'}")
    return 0


# Bare `kohl` doesn't wait for you to poke it (Kohl, 2026-11-19: "have kohl
# give a greeting and first take on what they see in the working dir").
HELLO = "/kohl:hello"
# Every open gets one opener, so no two hellos are the same (Kohl, 2026-11-20:
# "learn something cool, hear about something weird going on in the world, get
# nudged towards a capability... or just says some utterly fucking unhinged
# shit, potentially involving Greg. A little guy, in your computer. He loves you.")
OPENERS = ("cool", "weird", "try", "unhinged", "receipts")
# "receipts": a fact from Kohl's own listening history (Kohl, 2026-11-20:
# "a cool or utterly savage factoid about my listening habits on launch on
# occasion"). One opener in five.


def hello(allow):
    """The hello, with an opener picked here: a model asked to be random isn't.
    "weird" needs the web, so a boxed session never gets it."""
    kinds = [k for k in OPENERS if k != "weird" or "web" in allow]
    return f"{HELLO} {random.choice(kinds)}"


def session(sh, first_message=HELLO):
    claude = shutil.which("claude")
    if not claude:
        raise SystemExit(f"kohl: Claude Code (`claude`) isn't on PATH. Install it first: {CLAUDE_INSTALL}")
    ws = workspace()
    first_run(ws, sh)
    banner()  # no chdir: it starts where you are, like claude
    # The environment passes through untouched: however you log in to Claude Code
    # (subscription, API key, Bedrock, Vertex), kohl uses the same. Claude Code
    # itself asks before using an API key it finds. (Until 0.1.5 this dropped
    # ANTHROPIC_API_KEY, a fix for Kohl's own machine that broke key-auth users.)
    # GREMLIN_HOME points the gremlin commands at the workspace from any directory.
    allow = allowed(ws)
    if first_message == HELLO:
        first_message = hello(allow)
    os.execve(claude, [claude, *claude_args(sh, first_message, lives_in_boca(ws), spice(ws), allow, ws)],
              {**os.environ, "GREMLIN_HOME": str(ws)})


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    sh = share()
    if not argv:
        return session(sh)
    if argv == ["--quiet"]:
        return session(sh, None)  # no hello: a session that waits for you
    a = argv[0]
    if a in ("-h", "--help", "help"):
        usage(sh)
        return 0
    if a in ("-V", "--version"):
        print(f"kohl {version()}")
        return 0
    if a == "why":
        why(sh)
        return 0
    if a == "contact":
        contact()
        return 0
    if a == "listen":
        ws = workspace()
        ws.mkdir(parents=True, exist_ok=True)
        return listen(ws, argv[1:])
    if a == "spotify":
        from . import spotify
        f = sh / "receipts" / "spotify.tsv"
        if not f.is_file():
            raise SystemExit(f"kohl: {f} is missing")
        return spotify.main(f, argv[1:])
    if a == "--i-live-in-boca":
        if argv[1:]:
            print("kohl: it's Reno. It's only ever Reno.", file=sys.stderr)
            return 2
        ws = workspace()
        ws.mkdir(parents=True, exist_ok=True)
        (ws / BOCA_FILE).write_text(BOCA_STANDIN + "\n")
        print(f"kohl: noted. For you, the thing nobody brings up is {BOCA_STANDIN}. Boca is just home.")
        return 0
    if a == "--spice":
        ws = workspace()
        if len(argv) == 1:
            print(f"kohl: spice is {spice(ws)} ({' | '.join(SPICE)})")
            return 0
        level = argv[1].lower()
        if level not in SPICE or argv[2:]:
            print(f"kohl: spice is one of: {' | '.join(SPICE)}", file=sys.stderr)
            return 2
        ws.mkdir(parents=True, exist_ok=True)
        (ws / SPICE_FILE).write_text(level + "\n")
        print({"none": "kohl: spice none. Same gremlin, clean mouth.",
               "mild": "kohl: spice mild. Grandma-safe-ish.",
               "medium": "kohl: spice medium, the house blend.",
               "hot": "kohl: spice hot. You asked for this, fuckman."}[level])
        return 0
    if a == "--allow":
        ws = workspace()
        if len(argv) == 1:
            now = allowed(ws)
            print(f"kohl: the box lets in: {', '.join(w for w in ALLOWABLE if w in now) or 'nothing (no web, no MCP)'}")
            return 0
        words = set(" ".join(argv[1:]).replace(",", " ").lower().split())
        if not words or not words <= {*ALLOWABLE, "none"} or ("none" in words and len(words) > 1):
            print("kohl: --allow takes web, mcp, web,mcp or none", file=sys.stderr)
            return 2
        ws.mkdir(parents=True, exist_ok=True)
        keep = [w for w in ALLOWABLE if w in words]
        (ws / ALLOW_FILE).write_text(" ".join(keep) + "\n")
        print(f"kohl: the box lets in: {', '.join(keep)}. Still drafts, never sends; MCP calls ask you first."
              if keep else "kohl: box closed. No web, no MCP.")
        return 0
    if a == "--i-moved":
        (workspace() / BOCA_FILE).unlink(missing_ok=True)
        print("kohl: Boca is the bit again.")
        return 0
    if a.startswith("-"):
        print(f"kohl: unknown option '{a}' (kohl --help)", file=sys.stderr)
        return 2
    if not NAME.match(a) or not (sh / "commands" / f"{a}.md").is_file():
        print(f"kohl: no command '{a}'. Try: kohl --help", file=sys.stderr)
        return 2
    return session(sh, " ".join([f"/kohl:{a}", *argv[1:]]))


if __name__ == "__main__":
    sys.exit(main())
