import html
import pathlib
import textwrap

INK = "#14141a"
LINE = "#2c2c3a"
TEXT = "#d7d7e0"
DIM = "#8a8a9a"
ACCENT = "#8f8fff"
MONO = "Consolas, 'SF Mono', Menlo, 'DejaVu Sans Mono', monospace"
SANS = "'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"

cards = [
    ("pyrodisc", "pyrodisc", "A community platform and client for Trove: a desktop launcher, in-game Lua scripting, leaderboards, a market and a forum.", "C++ / Rust / TypeScript / Lua", True),
    ("trove-network-client", "trove-network-client", "A fully standalone client that connects to Trove's servers and sends packets.", "C++", False),
    ("rose-launcher", "rose-launcher", "A lightweight, fully local Trove launcher.", "TypeScript / Tauri / React", False),
    ("exe-diff", "exe-diff", "Compares two builds of a Windows binary, with decompiled C and assembly diffs.", "Python / IDA Pro", False),
    ("cpp-base64", "cpp-base64", "Fast Base64 encoding and decoding for C++20.", "C++", False),
    ("sq-playerhud", "sq-playerhud", "A player HUD mod for Trove, first posted in August 2023.", "ActionScript", False),
    ("library-of-babel-lua", "library-of-babel-lua", "A recreation of the Library of Babel.", "Lua / SDL2", False),
]

# share of the code in the public repositories, from the github languages api
stack = [("C++", 33), ("TypeScript", 21), ("Python", 21), ("C", 6), ("Lua", 5), ("ActionScript", 5)]

here = pathlib.Path(__file__).parent


def frame(width, height, label, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{html.escape(label)}">\n'
        f'  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="12" fill="{INK}" stroke="{LINE}" stroke-width="2"/>\n'
        f"{body}</svg>\n"
    )


def card(name, description, tags, wide):
    width, wrap = (860, 125) if wide else (420, 50)
    lines = textwrap.wrap(description, wrap)
    body = f'  <text x="24" y="42" fill="{ACCENT}" style="font: 700 19px {MONO}"><tspan fill="{DIM}">~/</tspan>{html.escape(name)}</text>\n'
    for index, line in enumerate(lines):
        body += f'  <text x="24" y="{72 + index * 21}" fill="{TEXT}" style="font: 14px {SANS}">{html.escape(line)}</text>\n'
    body += f'  <rect x="24" y="123" width="8" height="8" rx="2" fill="{ACCENT}"/>\n'
    body += f'  <text x="40" y="132" fill="{DIM}" style="font: 13px {MONO}">{html.escape(tags)}</text>\n'
    body += f'  <path d="M{width - 38} 132 l10 -10 m-7 0 h7 v7" fill="none" stroke="{DIM}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>\n'
    return frame(width, 152, f"{name}: {description}", body)


def chips(names):
    x, body = 0, ""
    for name, share in names:
        text_width = (len(name) + len(str(share)) + 2) * 9
        width = text_width + 32
        body += f'  <rect x="{x + 1}" y="1" width="{width - 2}" height="36" rx="9" fill="{INK}" stroke="{LINE}" stroke-width="2"/>\n'
        body += f'  <text x="{x + 16}" y="25" fill="{TEXT}" textLength="{text_width}" lengthAdjust="spacing" style="font: 15px {MONO}">{html.escape(name)} <tspan fill="{DIM}">{share}%</tspan></text>\n'
        x += width + 10
    total = x - 10
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total} 38" width="{total}" height="38" role="img" aria-label="{html.escape(", ".join(f"{name} {share}%" for name, share in names))}">\n{body}</svg>\n'


for slug, name, description, tags, wide in cards:
    (here / "cards" / f"{slug}.svg").write_text(card(name, description, tags, wide), encoding="utf-8", newline="\n")
(here / "stack.svg").write_text(chips(stack), encoding="utf-8", newline="\n")
