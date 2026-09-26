"""Combine the catalogue with a probe result into STATUS.md (+ status.json for the website).

  python evaluate.py ../results/<run>.json
"""
import json
import sys
from collections import OrderedDict

LABEL = {"verified": "✅ Verified", "documented": "⚙️ Config documented", "expected": "🟢 Expected to work",
         "blocked": "🔴 Blocked"}


def status_for(project, results):
    failing = [n for n in project["needs"] if results.get(n, {}).get("status") != "pass"]
    if project["verification"] in ("verified", "documented"):
        return project["verification"], failing
    return ("blocked", failing) if failing else ("expected", [])


def main():
    run_path = sys.argv[1] if len(sys.argv) > 1 else "../results/latest.json"
    with open("projects.json", encoding="utf-8") as f:
        catalog = json.load(f)
    with open(run_path, encoding="utf-8") as f:
        run = json.load(f)
    results = run["results"]

    rows, by_cat = [], OrderedDict()
    for p in catalog["projects"]:
        status, failing = status_for(p, results)
        row = {**p, "status": status, "failing": failing}
        rows.append(row)
        by_cat.setdefault(p["category"], []).append(row)

    counts = {k: sum(1 for r in rows if r["status"] == k) for k in LABEL}
    lines = [
        "# Works with AI Server — status", "",
        f"Generated from probe run `{run_path.split('/')[-1]}`: AI Server {run.get('server_version') or '?'}, "
        f"model `{run.get('model')}`, {run.get('run_utc')}.", "",
        f"**{len(rows)} permissively licensed projects:** " + " · ".join(f"{LABEL[k]} {v}" for k, v in counts.items()), "",
        "Status meanings: **Verified** = run end to end against AI Server by us (evidence linked). "
        "**Config documented** = configuration published, tool not yet exercised by us. "
        "**Expected to work** = every protocol check the tool depends on passes. "
        "**Blocked** = a check the tool depends on currently fails (named).", "",
        "## Protocol checks in this run", "", "| Check | Result | Detail |", "| --- | --- | --- |",
    ]
    for sid, r in results.items():
        lines.append(f"| `{sid}` | {'✅' if r['status'] == 'pass' else ('➖' if r['status'] == 'skip' else '❌')} | {r['reason']} |")
    for cat, items in by_cat.items():
        lines += ["", f"## {cat}", "", "| Project | Licence | Status | How to point it at AI Server |", "| --- | --- | --- | --- |"]
        for r in items:
            st = LABEL[r["status"]]
            if r["status"] == "blocked":
                st += " by " + ", ".join(f"`{x}`" for x in r["failing"])
            if r.get("evidence"):
                st += f" ([evidence]({r['evidence']}))"
            if r.get("note"):
                st += f" — {r['note']}"
            lines.append(f"| [{r['name']}]({r['repo']}) | {r['license']} | {st} | `{r['config']}` |")
    lines += ["", "## Check the licence first", "", "| Project | Licence | Note |", "| --- | --- | --- |"]
    for c in catalog["caution"]:
        lines.append(f"| [{c['name']}]({c['repo']}) | {c['license']} | {c['note']} |")
    lines += ["", catalog["excluded_note"], ""]

    with open("STATUS.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open("status.json", "w", encoding="utf-8") as f:
        json.dump({"server_version": run.get("server_version"), "model": run.get("model"), "run_utc": run.get("run_utc"),
                   "checks": results, "projects": rows, "caution": catalog["caution"]}, f, indent=2, ensure_ascii=False)
    print(f"STATUS.md written: " + ", ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
