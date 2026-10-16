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
SITE_URL = "https://topsoilcommons.github.io/index/"
MARK_URL = "https://topsoilcommons.github.io/topsoilcommons/assets/aurora-logo.png"


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
    sentences = [
        f"This page lists <span class=\"rub\">{total}</span> entries in time order."
    ]
    for state in state_format:
        count = counts.get(state["name"], 0)
        if count:
            noun = "entry" if count == 1 else "entries"
            verb = "stands" if count == 1 else "stand"
            sentences.append(
                f"<span class=\"rub\">{count}</span> {noun} {verb} {state['name']}."
            )
    latest_check = max(
        entry["check"]["date"] for entry in entries if entry.get("check")
    )
    proposal_total = len(proposals)
    proposal_word = "proposal" if proposal_total == 1 else "proposals"
    proposal_verb = "stands" if proposal_total == 1 else "stand"
    proposal_be = "is" if proposal_total == 1 else "are"
    sentences.append(
        f"<span class=\"rub\">{proposal_total}</span> agent {proposal_word} "
        f"{proposal_verb} proposed and {proposal_be} not counted in that total."
    )
    sentences.append("The counts come from the data files held in this repository.")
    sentences.append(
        f"The latest check on this page was on "
        f"<span class=\"rub\">{display_date(latest_check)}</span>."
    )
    return " ".join(sentences)


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


def medium_graph(entries):
    total = len(entries)
    counts = Counter(entry["medium"] for entry in entries)
    media = load_json(ROOT / "format.json")["media"]
    rows = []
    for medium in media:
        count = counts.get(medium, 0)
        if not count:
            continue
        scale = count / total if total else 0
        rows.append(
            "<div class=\"graphrow\">"
            f"<span class=\"graphlabel\">{html.escape(medium.capitalize())}</span>"
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
    if entry["hand"]:
        hand_sentence = f"{html.escape(entry['hand'])} stands behind this entry."
    else:
        hand_sentence = "No human hand stands behind this entry yet."
    place = entry["place"] or "Not stated"
    proposer = entry["proposed_by"]
    proposer_line = (
        f"{html.escape(proposer['kind'])}, {html.escape(proposer['name'])}"
    )
    operator_row = ""
    if proposer.get("operator"):
        operator_row = (
            f"\n        <div><dt>Operator</dt>"
            f"<dd>{html.escape(proposer['operator'])}</dd></div>"
        )
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
      <h3>{html.escape(entry['claim'])}</h3>
      <p class="state">This entry <span class="rub">stands {html.escape(entry['state'])}</span>. {hand_sentence} The claim is dated {html.escape(display_date(entry['time_claimed']))}.</p>
      <p><a href="{html.escape(entry['original_url'])}\">Open the original for this entry</a></p>
      <p><button type="button" class="share" data-share data-title="The Index" data-text="{html.escape(entry['claim'], quote=True)}" data-url="{SITE_URL}#{html.escape(entry['id'])}">Share</button></p>
      <details class="tech">
        <summary>For agents and builders</summary>
        <dl>
        <div><dt>Entry id</dt><dd class="mono">{html.escape(entry['id'])}</dd></div>
        <div><dt>State name in the format</dt><dd>{html.escape(entry['state'])}</dd></div>
        <div><dt>Time claimed</dt><dd>{html.escape(display_date(entry['time_claimed']))}</dd></div>
        <div><dt>Time received</dt><dd>{html.escape(display_date(entry['time_received']))}</dd></div>
        <div><dt>Place</dt><dd>{html.escape(place)}</dd></div>
        <div><dt>Medium</dt><dd>{html.escape(entry['medium'])}</dd></div>
        <div><dt>Proposed by</dt><dd>{proposer_line}</dd></div>{operator_row}
        <div><dt>Hand</dt><dd>{html.escape(entry['hand'] or 'None')}</dd></div>
        </dl>
        <p>{check_line}</p>
        <p class="fingerprint">Original SHA-256: <span class="mono">{html.escape(entry['original_hash']['value'])}</span></p>
        <p class="fingerprint">Seal: <span class="mono">{html.escape(entry['seal'])}</span></p>
        {link_line(entry)}
      </details>
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
<meta property="og:site_name" content="Topsoil Commons">
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
  body{{margin:0;background:var(--bg);color:#1b1e23;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}}
  :focus-visible{{outline:2px solid var(--ink);outline-offset:2px}}
  [id]{{scroll-margin-top:72px}}
  .skip{{position:absolute;left:-9999px;top:0;background:var(--bg);color:#1b1e23;font-weight:600;padding:12px 16px;z-index:20}}
  .skip:focus{{left:20px;top:8px}}
  .commons-bar{{position:sticky;top:0;z-index:10;background:var(--bg);display:flex;flex-wrap:wrap;gap:4px 18px;align-items:center;max-width:980px;margin:0 auto;padding:0 20px;font-size:14px;border-bottom:1px solid var(--line)}}
  .commons-bar .brand{{font-weight:600;color:#1b1e23;text-decoration:none;margin-right:4px}}
  .commons-bar a{{color:#1b1e23;text-decoration:none;display:inline-flex;align-items:center;min-height:44px}}
  .commons-bar a:hover{{text-decoration:underline}}
  .commons-bar .current{{font-weight:700;display:inline-flex;align-items:center;min-height:44px}}
  .wrap{{max-width:980px;margin:0 auto;padding:0 20px}}
  header{{padding:28px 0 4px}}
  h1{{font-size:52px;letter-spacing:-1.5px;margin:14px 0 8px;font-weight:800}}
  .part{{font-size:16px;font-weight:600;max-width:680px;margin:0 0 10px}}
  .tag{{font-size:19px;color:#5a6068;max-width:680px;margin:0}}
  .firststep{{font-size:17px;margin:18px 0 0;max-width:680px}}
  .counts{{font-size:16px;margin:22px 0 0;max-width:760px}}
  .rub{{color:#9e2b25}}
  h2{{font-size:25px;letter-spacing:-.5px;margin:0 0 8px;font-weight:800}}
  section{{padding:42px 0 4px}}
  .graphrow{{display:grid;grid-template-columns:110px 1fr 130px;gap:12px;align-items:center;border-top:1px solid var(--line);padding:9px 0}}
  .graphlabel{{font-weight:700}}
  .graphbar{{display:block;height:12px;border:1px solid var(--line);background:#fff}}
  .graphbar i{{display:block;height:100%;background:var(--ink);transform:scaleX(var(--scale));transform-origin:left;animation:draw .7s ease-out 1}}
  @keyframes draw{{from{{transform:scaleX(0)}}}}
  @media (prefers-reduced-motion: reduce){{.graphbar i{{animation:none}}}}
  .graphcount{{font-size:14px;color:#5a6068}}
  .entry{{border-top:1px solid var(--line);padding:18px 0 16px;margin-top:18px}}
  .entry h3{{font-size:20px;letter-spacing:-.3px;margin:0 0 8px;font-weight:700}}
  .entry p{{margin:0 0 8px;font-size:15.5px;max-width:760px}}
  .entry .state{{font-size:16px}}
  .entry .state .rub{{font-weight:700}}
  .entry details{{margin:10px 0 4px;max-width:760px}}
  .entry summary{{font-weight:700;cursor:pointer;min-height:44px;display:flex;align-items:center}}
  .entry dl{{margin:0 0 10px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 18px;max-width:680px}}
  .entry dt{{font-weight:700}}
  .entry dd{{margin:0}}
  .fingerprint{{font-size:13px;color:#5a6068;overflow-wrap:anywhere}}
  .mono{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
  .share{{font:inherit;font-weight:700;font-size:15px;min-width:44px;min-height:44px;background:none;border:0;padding:0;color:#1b1e23;cursor:pointer;text-align:left}}
  .share:hover{{text-decoration:underline}}
  table{{border-collapse:collapse;width:100%;font-size:15px}}
  th,td{{border-top:1px solid var(--line);padding:9px 12px 9px 0;text-align:left;vertical-align:top}}
  thead th{{border-top:0}}
  footer{{padding:54px 0 62px;margin-top:46px;border-top:1px solid var(--line);color:#5a6068;font-size:14px}}
  footer a{{color:#1b1e23;text-decoration:none;font-weight:600}}
  .endline{{text-align:center;font-size:15px;color:#1b1e23;margin:0;padding:0 0 54px}}
  @media (max-width:620px){{h1{{font-size:38px}}.graphrow{{grid-template-columns:86px 1fr}}.graphcount{{grid-column:2}}.entry dl{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<nav class="commons-bar" aria-label="Topsoil Commons sites">
  <a class="brand" href="https://topsoilcommons.github.io/topsoilcommons/"><svg class="bar-mark" viewBox="0 0 24 24" width="17" height="17" aria-hidden="true" focusable="false" style="flex:none;align-self:center;margin-right:7px"><g fill="currentColor"><rect x="4" y="2.5" width="16" height="2"/><rect x="4" y="5.5" width="16" height="2"/><rect x="4" y="8.5" width="16" height="2"/><rect x="4" y="11.5" width="4.5" height="8"/><rect x="15.5" y="11.5" width="4.5" height="8"/><rect x="2" y="20.5" width="20" height="2.2"/></g></svg>Topsoil Commons</a>
  <span class="current" aria-current="page">The Index (you are here)</span>
  <a href="https://topsoilcommons.github.io/topsoilcommons/foundations.html">Foundations</a>
  <a href="https://topsoilcommons.github.io/ground/">Ground</a>
  <a href="https://topsoilcommons.github.io/still/">Still</a>
  <a href="https://topsoilcommons.github.io/atlas/">Atlas</a>
  <a href="https://topsoilcommons.github.io/cohort/">Cohort</a>
  <a href="https://topsoilcommons.github.io/graph/">Graph</a>
  <a href="https://topsoilcommons.github.io/machine/">Machine</a>
  <a href="https://topsoilcommons.github.io/lumen/">Lumen</a>
</nav>
<div class="wrap">
<main id="main">
<header>
  <h1>The Index</h1>
  <p class="part">Part of the Record: the Commons record in time order.</p>
  <p class="tag">Each entry shows one claim, its state, who stands behind it, and its date, with a link to the original.</p>
  <p class="firststep">Start with the first entry below. Open its original, then compare it with the claim.</p>
  <p class="counts">{count_sentence(entries, sources, proposals, proposal_sources)}</p>
</header>

<section aria-labelledby="counts-h">
  <h2 id="counts-h">Counts by state</h2>
  <div>
      {state_graph(entries)}
  </div>
</section>

<section aria-labelledby="media-h">
  <h2 id="media-h">Counts by medium</h2>
  <div>
      {medium_graph(entries)}
  </div>
</section>

<section aria-labelledby="key-h">
  <h2 id="key-h">Key to the states</h2>
      {key_table()}
</section>

<section aria-labelledby="entries-h">
  <h2 id="entries-h">Entries</h2>
    {entries_markup}
</section>

<section aria-labelledby="agents-h">
  <h2 id="agents-h">For agents and builders</h2>
  <p>For agents: <a href="llms.txt">llms.txt</a> names this viewer's data files, FORMAT.md and format.json, the validator, and the starter kit, and states the six states and the human gate rule in brief.</p>
</section>
</main>

<footer>
  <p>Topsoil Commons addresses the hierarchy of human needs through open source.</p>
  <p>Stand on the shoulders of giants.</p>
  <p>One rule: raise the floor beneath everyone.</p>
  <p>Advised by Groundskeeper.</p>
  <p><a href="https://topsoilcommons.github.io/topsoilcommons/">Back to the home page</a></p>
  <p><a href="https://www.linkedin.com/company/topsoil-commons/">Topsoil Commons on LinkedIn</a></p>
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
