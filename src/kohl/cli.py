"""kohl: a model playing Kohl, files included. https://github.com/KohlJary/kohl

  kohl                 talk to it
  kohl <command> [..]  start with /<command> (see `kohl --help`)
  kohl why             the warnings, printed; no model involved
  kohl --i-live-in-boca   for Boca residents: Reno becomes the thing nobody brings up

The persona ships read-only with the package (the share directory). Your
workspace (queue, ledger, STATUS) is ${XDG_DATA_HOME:-~/.local/share}/kohl,
made by `gremlin init` on first run. It drafts; it never sends: no web
tools, no MCP servers.
"""
import os
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

  kohl --i-live-in-boca   you live in Boca: Reno is the one nobody brings up now
  kohl --i-moved          undo that
  kohl --version    print the version
  kohl --help       this

Workspace: {workspace()}""")


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


def claude_args(sh, first_message=None, boca=False):
    """The session's arguments. The first message goes before the options:
    --allowedTools and friends take every word after them, and would swallow it."""
    s = str(sh)
    return [*([first_message] if first_message else []),
            "--append-system-prompt", wake_prompt(sh) + (boca_note() if boca else ""),
            "--plugin-dir", s, "--add-dir", s,
            "--strict-mcp-config",
            "--tools", "Read", "Glob", "Grep", "Edit", "Write", "Bash",
            "--allowedTools", f"Read({s}/**)", "Read(./**)", "Glob", "Grep",
            "Bash(gremlin queue:*)", "Bash(gremlin ledger:*)", "Bash(gremlin wf:*)",
            "Bash(gremlin lessons:*)", "Bash(gremlin wake:*)",
            # Edit(path) rules cover every file-editing tool, Write included; Claude Code
            # warns on Write(path) rules and doesn't match them.
            "Edit(./queue/**)",
            "--disallowedTools", "WebFetch", "WebSearch", f"Edit({s}/**)"]


def session(sh, first_message=None):
    claude = shutil.which("claude")
    if not claude:
        raise SystemExit(f"kohl: Claude Code (`claude`) isn't on PATH. Install it first: {CLAUDE_INSTALL}")
    ws = workspace()
    first_run(ws, sh)
    os.chdir(ws)
    banner()
    # ANTHROPIC_API_KEY is dropped so the session uses your Claude login, same as `gremlin talk`.
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    os.execve(claude, [claude, *claude_args(sh, first_message, lives_in_boca(ws))], env)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    sh = share()
    if not argv:
        return session(sh)
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
    if a == "--i-live-in-boca":
        if argv[1:]:
            print("kohl: it's Reno. It's only ever Reno.", file=sys.stderr)
            return 2
        ws = workspace()
        ws.mkdir(parents=True, exist_ok=True)
        (ws / BOCA_FILE).write_text(BOCA_STANDIN + "\n")
        print(f"kohl: noted. For you, the thing nobody brings up is {BOCA_STANDIN}. Boca is just home.")
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
