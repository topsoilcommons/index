#!/usr/bin/env python3
"""Build index.html from the Index data files and format.json.

The page is a build product. Edit the data or the format, then rerun this
script. Use --check to compare the committed page with a fresh build.
"""

import html
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://auroracommons.github.io/index/"
MARK_URL = "https://auroracommons.github.io/auroracommons/assets/aurora-logo.png"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def all_entries(folder):
    entries = []
    sources = []
    for path in sorted((ROOT / folder).glob("*.json")):
        data = load_json(path)
        entries.extend(data["entries"])
        sources.append(path)
    return entries, sources


def display_date(value):
    parsed = date.fromisoformat(value[:10])
    return parsed.strftime("%B %-d, %Y")


def count_sentence(entries, sources, proposals, proposal_sources):
    total = len(entries)
    counts = Counter(entry["state"] for entry in entries)
    state_format = load_json(ROOT / "format.json")["states"]
    parts = []
    for state in state_format:
        count = counts.get(state["name"], 0)
        if count:
            parts.append(f"<span class=\"rub\">{count}</span> stand {state['name']}")
    latest_check = max(
        entry["check"]["date"] for entry in entries if entry.get("check")
    )
    source_names = ", ".join(
        f"{source.parent.name}/{source.name}" for source in sources
    )
    proposal_total = len(proposals)
    proposal_word = "proposal" if proposal_total == 1 else "proposals"
    proposal_sources_text = ", ".join(
        f"{source.parent.name}/{source.name}" for source in proposal_sources
    )
    return (
        f"This page lists <span class=\"rub\">{total}</span> entries: "
        + " and ".join(parts)
        + f", counted from {html.escape(source_names)} in this repository on "
        + f"<span class=\"rub\">{display_date(latest_check)}</span>. "
        + f"<span class=\"rub\">{proposal_total}</span> agent {proposal_word} "
        + f"stand proposed in {html.escape(proposal_sources_text)} and are not counted in that total."
    )


def state_graph(entries):
    total = len(entries)
    counts = Counter(entry["state"] for entry in entries)
    state_format = load_json(ROOT / "format.json")["states"]
    rows = []
    for state in state_format:
        count = counts.get(state["name"], 0)
        if not count:
            continue
        scale = count / total if total else 0
        rows.append(
            "<div class=\"graphrow\">"
            f"<span class=\"graphlabel\">{html.escape(state['label'])}</span>"
            f"<span class=\"graphbar\" aria-hidden=\"true\"><i style=\"--scale:{scale:.6f}\"></i></span>"
            f"<span class=\"graphcount\">{count} of {total} entries</span>"
            "</div>"
        )
    return "\n      ".join(rows)


def key_table():
    state_format = load_json(ROOT / "format.json")["states"]
    rows = ["<table class=\"keytable\">", "<thead><tr><th scope=\"col\">State</th><th scope=\"col\">What it means</th></tr></thead>", "<tbody>"]
    for state in state_format:
        rows.append(
            f"<tr><th scope=\"row\">{html.escape(state['label'])}</th>"
            f"<td>{html.escape(state['definition'])}</td></tr>"
        )
    rows.extend(["</tbody>", "</table>"])
    return "\n      ".join(rows)


def link_line(entry):
    links = []
    for correction in entry["links"]["corrections"]:
        links.append(
            f"Correction: <a href=\"#{html.escape(correction)}\">{html.escape(correction)}</a>"
        )
    for corrected in entry["links"]["corrects"]:
        links.append(
            f"Corrects: <a href=\"#{html.escape(corrected)}\">{html.escape(corrected)}</a>"
        )
    if not links:
        return ""
    return f"<p class=\"linksline\">{' '.join(links)}</p>"


def entry_html(entry, state_labels):
    state = state_labels[entry["state"]]
    hand = entry["hand"] or "No human hand yet"
    place = entry["place"] or "Not stated"
    if entry["check"]:
        check = entry["check"]
        check_line = (
            f"Check: {html.escape(check['method'])} "
            f"Checked by {html.escape(check['checked_by'])}. "
            f"Result: {html.escape(check['result'])} "
            f"Date: {html.escape(display_date(check['date']))}."
        )
    else:
        check_line = "Check: none yet."
    return f"""<article class="entry" id="{html.escape(entry['id'])}">
      <p class="state"><span class="rub">{html.escape(state)}</span>. Hand: {html.escape(hand)}.</p>
      <h3>{html.escape(entry['claim'])}</h3>
      <dl>
        <div><dt>Time claimed</dt><dd>{html.escape(display_date(entry['time_claimed']))}</dd></div>
        <div><dt>Time received</dt><dd>{html.escape(display_date(entry['time_received']))}</dd></div>
        <div><dt>Place</dt><dd>{html.escape(place)}</dd></div>
        <div><dt>Medium</dt><dd>{html.escape(entry['medium'])}</dd></div>
      </dl>
      <p>{check_line}</p>
      <p><a href="{html.escape(entry['original_url'])}\">Open the original</a></p>
      <p class="fingerprint">Original SHA-256: <span class="mono">{html.escape(entry['original_hash']['value'])}</span></p>
      <p class="fingerprint">Seal: <span class="mono">{html.escape(entry['seal'])}</span></p>
      {link_line(entry)}
      <p><button type="button" class="share" data-share data-title="The Index" data-text="{html.escape(entry['claim'], quote=True)}" data-url="{SITE_URL}#{html.escape(entry['id'])}">Share</button></p>
    </article>"""


def render():
    entries, sources = all_entries("entries")
    proposals, proposal_sources = all_entries("proposals")
    state_format = load_json(ROOT / "format.json")["states"]
    state_labels = {state["name"]: state["label"] for state in state_format}
    entries_markup = "\n    ".join(entry_html(entry, state_labels) for entry in entries)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Index</title>
<meta name="description" content="The Commons record in time order, each entry with its state, hand, and check.">
<meta name="theme-color" content="#fbfaf7">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Aurora Commons">
<meta property="og:title" content="The Index">
<meta property="og:description" content="The Commons record in time order, each entry with its state, hand, and check.">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{MARK_URL}">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="1600">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="The Index">
<meta name="twitter:description" content="The Commons record in time order, each entry with its state, hand, and check.">
<meta name="twitter:image" content="{MARK_URL}">
<style>
  :root{{--bg:#fbfaf7;--ink:#1b1e23;--soft:#5a6068;--line:#e4e0d6;--rub:#9e2b25}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}}
  .commons-bar{{display:flex;flex-wrap:wrap;gap:4px 18px;align-items:baseline;max-width:980px;margin:0 auto;padding:10px 20px 8px;font-size:14px;border-bottom:1px solid var(--line)}}
  .commons-bar .brand{{font-weight:800;color:var(--ink);text-decoration:none;margin-right:4px}}
  .commons-bar a{{color:var(--ink);text-decoration:none}}
  .commons-bar a:hover{{text-decoration:underline}}
  .commons-bar .current{{font-weight:700}}
  .wrap{{max-width:980px;margin:0 auto;padding:0 20px}}
  header{{padding:28px 0 4px}}
  h1{{font-size:52px;letter-spacing:-1.5px;margin:14px 0 8px;font-weight:800}}
  .tag{{font-size:19px;color:var(--soft);max-width:680px;margin:0}}
  .firststep{{font-size:17px;margin:18px 0 0;max-width:680px}}
  .counts{{font-size:16px;margin:22px 0 0;max-width:760px}}
  .rub{{color:var(--rub)}}
  h2{{font-size:25px;letter-spacing:-.5px;margin:0 0 8px;font-weight:800}}
  section{{padding:42px 0 4px}}
  .graphrow{{display:grid;grid-template-columns:110px 1fr 130px;gap:12px;align-items:center;border-top:1px solid var(--line);padding:9px 0}}
  .graphlabel{{font-weight:700}}
  .graphbar{{display:block;height:12px;border:1px solid var(--line);background:#fff}}
  .graphbar i{{display:block;height:100%;background:var(--ink);transform:scaleX(var(--scale));transform-origin:left;animation:draw .7s ease-out 1}}
  @keyframes draw{{from{{transform:scaleX(0)}}}}
  @media (prefers-reduced-motion: reduce){{.graphbar i{{animation:none}}}}
  .graphcount{{font-size:14px;color:var(--soft)}}
  .entry{{border-top:1px solid var(--line);padding:18px 0 16px;margin-top:18px}}
  .entry h3{{font-size:20px;letter-spacing:-.3px;margin:0 0 8px;font-weight:700}}
  .entry p{{margin:0 0 8px;font-size:15.5px;max-width:760px}}
  .entry .state{{font-size:16px;font-weight:700}}
  .entry dl{{margin:0 0 10px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 18px;max-width:680px}}
  .entry dt{{font-weight:700}}
  .entry dd{{margin:0}}
  .fingerprint{{font-size:13px;color:var(--soft);overflow-wrap:anywhere}}
  .mono{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
  .share{{font:inherit;font-weight:700;font-size:15px;min-width:44px;min-height:44px;background:none;border:0;padding:0;color:var(--ink);cursor:pointer;text-align:left}}
  .share:hover{{text-decoration:underline}}
  table{{border-collapse:collapse;width:100%;font-size:15px}}
  th,td{{border-top:1px solid var(--line);padding:9px 12px 9px 0;text-align:left;vertical-align:top}}
  thead th{{border-top:0}}
  footer{{padding:54px 0 62px;margin-top:46px;border-top:1px solid var(--line);color:var(--soft);font-size:14px}}
  footer a{{color:var(--ink);text-decoration:none;font-weight:600}}
  .endline{{text-align:center;font-size:15px;color:var(--ink);margin:0;padding:0 0 54px}}
  @media (max-width:620px){{h1{{font-size:38px}}.graphrow{{grid-template-columns:86px 1fr}}.graphcount{{grid-column:2}}.entry dl{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<nav class="commons-bar" aria-label="Aurora Commons sites">
  <a class="brand" href="https://auroracommons.github.io/auroracommons/">Aurora Commons</a>
  <span class="current" aria-current="page">The Index</span>
  <a href="https://auroracommons.github.io/ground/">Ground</a>
  <a href="https://auroracommons.github.io/still/">Still</a>
  <a href="https://auroracommons.github.io/atlas/">Atlas</a>
  <a href="https://auroracommons.github.io/cohort/">Cohort</a>
  <a href="https://auroracommons.github.io/graph/">Graph</a>
  <a href="https://auroracommons.github.io/machine/">Machine</a>
  <a href="https://auroracommons.github.io/lumen/">Lumen</a>
</nav>
<div class="wrap">
<header>
  <h1>The Index</h1>
  <p class="tag">The Commons record in time order, each entry with its state, hand, and check.</p>
  <p class="firststep">Start with the first entry below. Open its original, then compare it with the claim.</p>
  <p class="counts">{count_sentence(entries, sources, proposals, proposal_sources)}</p>
</header>

<section aria-labelledby="counts-h">
  <h2 id="counts-h">Counts by state</h2>
  <div>
      {state_graph(entries)}
  </div>
</section>

<main>
<section aria-labelledby="entries-h">
  <h2 id="entries-h">Entries</h2>
    {entries_markup}
</section>

<section aria-labelledby="key-h">
  <h2 id="key-h">Key to the states</h2>
      {key_table()}
</section>
</main>

<footer>
  <p>Aurora Commons addresses the hierarchy of human needs through open source.</p>
  <p>Stand on the shoulders of giants.</p>
  <p>One rule: raise the floor beneath everyone.</p>
  <p>Advised by Groundskeeper.</p>
  <p><a href="https://www.linkedin.com/company/aurora-commons-io/">Aurora Commons on LinkedIn</a></p>
</footer>
</div>
<p class="endline">That is everything. The page ends here.</p>
<script>
document.addEventListener("click", function(e){{
  var b = e.target && e.target.closest ? e.target.closest("[data-share]") : null;
  if (!b) return;
  var d = {{ title: b.getAttribute("data-title"), text: b.getAttribute("data-text"), url: b.getAttribute("data-url") }};
  if (navigator.share) {{ navigator.share(d).catch(function(){{}}); return; }}
  var old = b.textContent;
  function done(){{ b.textContent = "Link copied"; setTimeout(function(){{ b.textContent = old; }}, 2000); }}
  if (navigator.clipboard && navigator.clipboard.writeText) {{ navigator.clipboard.writeText(d.text + " " + d.url).then(done, done); }}
}});
</script>
</body>
</html>
"""


def main(argv):
    rendered = render()
    path = ROOT / "index.html"
    if "--check" in argv:
        if not path.exists() or path.read_text(encoding="utf-8") != rendered:
            print("FAIL index.html: the viewer differs from the data files")
            return 1
        print("PASS index.html: the viewer matches the data files")
        return 0
    path.write_text(rendered, encoding="utf-8")
    print("Wrote index.html from the data files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
