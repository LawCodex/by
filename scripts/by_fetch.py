#!/usr/bin/env python3
"""Collect the Constitution, codes and laws of Belarus from ETALONLINE (etalonline.by),
the official legal information system of the National Center of Legislation and Legal
Information (NCLI).

etalonline.by has no public list of all laws: its search runs through /local/ajax/call.php,
which robots.txt disallows. So we discover laws by following references:
  seeds = the Constitution + every code linked from https://etalonline.by/kodeksy/
  then every law (register number H...) or code (HK...) referenced by a fetched document
  that is in force is fetched too (links from repealed documents are not followed).
Obeys robots.txt Crawl-delay: 5. Only the document part of each page is cached in
../_raw/by/docs/<regnum>.html."""
import json, os, re, sys, time, requests
from bs4 import BeautifulSoup

UA = "LawCodex/1.0 (+https://github.com/LawCodex)"
BASE = "https://etalonline.by"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(os.path.dirname(REPO), "_raw", "by")
DOCS = os.path.join(RAW, "docs")
DELAY = 15.0  # robots.txt asks for 5 s; slowed down after the server stopped answering at 5 s
S = requests.Session()
S.headers["User-Agent"] = UA
_last = [0.0]
LAW_RE = re.compile(r"(?:RN=|regnum=)(h[k1][0-9][0-9a-z_]{6,7})\b", re.I)


def get(url):
    for attempt in range(6):
        wait = _last[0] + DELAY - time.time()
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            r = S.get(url, timeout=180)
            if r.status_code == 200:
                return r.text
            print("HTTP", r.status_code, url, file=sys.stderr)
            if r.status_code == 404:
                return None
        except requests.RequestException as e:
            print("ERR", e, url, file=sys.stderr)
        time.sleep(30 * (attempt + 1))
    return None


def trim(html):
    soup = BeautifulSoup(html, "lxml")
    uc = soup.select_one("#userContent")
    if uc is None:
        return None
    head = soup.select_one("#docTitlePrint")
    return f"<!-- retrieved {time.strftime('%Y-%m-%d')} -->\n{head or ''}\n{uc}"


def main():
    os.makedirs(DOCS, exist_ok=True)
    state_p = os.path.join(RAW, "crawl_state.json")
    if os.path.exists(state_p):
        st = json.load(open(state_p))
    else:
        kod = get(f"{BASE}/kodeksy/")
        codes = sorted({m.lower() for m in re.findall(r"regnum=(hk[0-9]{7})", kod, re.I)})
        st = {"queue": ["v19402875"] + codes, "seen": [], "missing": []}
    queue, seen = st["queue"], set(st["seen"])
    seen.update(queue)
    n = 0
    while queue:
        rn = queue.pop(0)
        path = os.path.join(DOCS, f"{rn}.html")
        if os.path.exists(path):
            doc = open(path, encoding="utf-8").read()
        else:
            html = get(f"{BASE}/document/?regnum={rn}")
            doc = trim(html) if html else None
            if doc is None:
                st["missing"].append(rn)
                continue
            open(path, "w", encoding="utf-8").write(doc)
            n += 1
        in_force = 'data-aktinforce="1"' in doc
        if in_force:
            for m in LAW_RE.findall(doc):
                m = m.lower()
                if m not in seen:
                    seen.add(m)
                    queue.append(m)
        if n % 20 == 0:
            st["seen"] = sorted(seen)
            json.dump(st, open(state_p, "w"))
        print(rn, "in_force" if in_force else "-", "queue", len(queue), "seen", len(seen), flush=True)
    st["seen"] = sorted(seen)
    json.dump(st, open(state_p, "w"))


if __name__ == "__main__":
    main()
