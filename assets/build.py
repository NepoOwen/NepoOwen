import base64
import html
import json
import pathlib
import re

INK = "#14141a"
LINE = "#2c2c3a"
TEXT = "#d7d7e0"
DIM = "#8a8a9a"
ACCENT = "#8f8fff"
SANS = "'Nepo Sans', 'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"

cards = [
    ("pyrodisc", "A community platform and client for Trove: a desktop launcher, in-game Lua scripting, leaderboards, a market and a forum.", "C++ / Rust / TypeScript / Lua", True),
    ("trove-network-client", "A fully standalone client that connects to Trove's servers and sends packets.", "C++", False),
    ("rose-launcher", "A lightweight, fully local Trove launcher.", "TypeScript / Tauri / React", False),
    ("exe-diff", "Compares two builds of a Windows binary, with decompiled C and assembly diffs.", "Python / IDA Pro", False),
    ("cpp-base64", "Fast Base64 encoding and decoding for C++20.", "C++", False),
    ("sq-playerhud", "A player HUD mod for Trove, from August 2023.", "ActionScript", False),
    ("library-of-babel-lua", "A recreation of the Library of Babel.", "Lua / SDL2", False),
]

# share of the code in the public repositories, from the github languages api
stack = [("C++", 33), ("TypeScript", 21), ("Python", 21), ("C", 6), ("Lua", 5), ("ActionScript", 5)]

headings = ["about", "now", "projects", "stack", "contact"]

here = pathlib.Path(__file__).parent
fonts = here / "fonts"
metrics = json.loads((fonts / "metrics.json").read_text(encoding="utf-8"))


def face(key, weight):
    data = base64.b64encode((fonts / f"sans-{key}.woff").read_bytes()).decode()
    return f"@font-face {{ font-family: 'Nepo Sans'; font-weight: {weight}; src: url(data:font/woff;base64,{data}) format('woff'); }}"


BOLD = face("bold", 700)
MEDIUM = face("medium", 500)


def measure(text, key, size):
    return sum(metrics[key].get(char, 0.6) for char in text) * size


def wrap(text, key, size, limit):
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and measure(candidate, key, size) > limit:
            lines.append(current)
            current = word
        else:
            current = candidate
    return lines + [current]


def svg(width, height, label, faces, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{html.escape(label)}">\n'
        f"  <style>{' '.join(faces)}</style>\n"
        f"{body}</svg>\n"
    )


def box(x, width, height, radius):
    return f'  <rect x="{x + 1}" y="1" width="{width - 2}" height="{height - 2}" rx="{radius}" fill="{INK}" stroke="{LINE}" stroke-width="2"/>\n'


def card(name, description, tags, wide):
    width = 860 if wide else 420
    body = box(0, width, 152, 12)
    body += f'  <text x="24" y="42" fill="{ACCENT}" style="font: 700 21px {SANS}"><tspan fill="{DIM}">~/</tspan>{html.escape(name)}</text>\n'
    for index, line in enumerate(wrap(description, "medium", 14.5, width - 52)):
        body += f'  <text x="24" y="{72 + index * 21}" fill="{TEXT}" style="font: 500 14.5px {SANS}">{html.escape(line)}</text>\n'
    body += f'  <rect x="24" y="123" width="8" height="8" rx="2" fill="{ACCENT}"/>\n'
    body += f'  <text x="40" y="132" fill="{DIM}" style="font: 500 13.5px {SANS}">{html.escape(tags)}</text>\n'
    body += f'  <path d="M{width - 38} 132 l10 -10 m-7 0 h7 v7" fill="none" stroke="{DIM}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>\n'
    return svg(width, 152, f"{name}: {description}", [BOLD, MEDIUM], body)


def chips(names):
    x, body = 0, ""
    for name, share in names:
        width = round(measure(f"{name} {share}%", "medium", 16)) + 34
        body += box(x, width, 38, 9)
        body += f'  <text x="{x + 17}" y="25" fill="{TEXT}" style="font: 500 16px {SANS}">{html.escape(name)} <tspan fill="{DIM}">{share}%</tspan></text>\n'
        x += width + 10
    label = ", ".join(f"{name} {share}%" for name, share in names)
    return svg(x - 10, 38, label, [MEDIUM], body)


def heading(name):
    width = round(measure(f"~/{name}", "bold", 24)) + 36
    body = box(0, width, 44, 10)
    body += f'  <text x="18" y="30" fill="{TEXT}" style="font: 700 24px {SANS}"><tspan fill="{ACCENT}">~/</tspan>{html.escape(name)}</text>\n'
    return svg(width, 44, f"~/{name}", [BOLD], body)


for name, description, tags, wide in cards:
    (here / "cards" / f"{name}.svg").write_text(card(name, description, tags, wide), encoding="utf-8", newline="\n")
(here / "headings").mkdir(exist_ok=True)
for name in headings:
    (here / "headings" / f"{name}.svg").write_text(heading(name), encoding="utf-8", newline="\n")
(here / "stack.svg").write_text(chips(stack), encoding="utf-8", newline="\n")

banner = here / "banner.svg"
source = re.sub(r"\n    @font-face \{[^\n]*", "", banner.read_text(encoding="utf-8"))
source = source.replace("<style>", f"<style>\n    {BOLD}", 1)
source = re.sub(r"\.name \{ font: 700 \d+px [^;]*;", f".name {{ font: 700 50px {SANS};", source)
banner.write_text(source, encoding="utf-8", newline="\n")
