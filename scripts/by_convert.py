#!/usr/bin/env python3
"""Convert ETALONLINE documents (cached by by_fetch.py in ../_raw/by/docs/) to Markdown.

Kept: documents in force (data-aktinforce="1") whose full text is public. Skipped: amending /
repealing laws (their content is merged into the consolidated texts), repealed documents, and
documents that etalonline only shows in "demo" (truncated) mode to non-subscribers."""
import datetime, json, os, re, sys
from bs4 import BeautifulSoup, NavigableString, Tag

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(os.path.dirname(REPO), "_raw", "by")
RU = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюяіў",
              ["a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t",
               "u", "f", "kh", "ts", "ch", "sh", "shch", "", "y", "", "e", "yu", "ya", "i", "u"]))
MONTHS = {m: i + 1 for i, m in enumerate(["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа",
                                          "сентября", "октября", "ноября", "декабря"])}
HEAD_CLASSES = {"part": "part", "zagrazdel": "section", "razdel": "section", "podrazdel": "subsection",
                "chapter": "chapter", "paragraph": "paragraph"}
ORDER = ["part", "section", "subsection", "chapter", "paragraph"]
AMENDING = re.compile(r"^(О внесении (изменени|дополнени|измен)|Об изменени|О дополнени|О признании утратив|"
                      r"Аб унясенні|О внесении изменения)", re.I)


def slug(title, n=70):
    s = "".join(RU.get(ch, ch) for ch in title.lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if len(s) > n:
        s = s[:n].rsplit("-", 1)[0]
    return s or "untitled"


def text_of(el):
    out = []
    for d in el.descendants:
        if isinstance(d, NavigableString):
            if d.parent.name in ("script", "style"):
                continue
            t = str(d)
            if d.parent.name == "sup" and re.fullmatch(r"\s*\d+\s*", t):
                t = t.strip().translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
            out.append(t)
        elif isinstance(d, Tag) and d.name == "br":
            out.append("\n")
    t = "".join(out).replace("\xa0", " ")
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = "\n".join(x.strip() for x in t.split("\n"))
    return re.sub(r"\n{2,}", "\n", t).strip()


def esc(t):
    return re.sub(r"^(#+|>|[-+*] )", lambda m: "\\" + m.group(0), t)


def table_html(tb):
    rows = []
    for tr in tb.find_all("tr"):
        if tr.find_parent("table") is not tb:
            continue
        cells = []
        for td in tr.find_all(["td", "th"], recursive=False):
            attrs = "".join(f' {a}="{td[a]}"' for a in ("colspan", "rowspan") if td.get(a) and td.get(a) != "1")
            cells.append(f"<{td.name}{attrs}>{text_of(td).replace(chr(10), '<br>')}</{td.name}>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def ru_date(s):
    m = re.search(r"(\d{1,2})\s+([а-я]+)\s+(\d{4})", s or "")
    if m and m.group(2) in MONTHS:
        return f"{m.group(3)}-{MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}"
    return None


def convert(uc):
    items = []
    for el in uc.find_all(["p", "table"]):
        if el.find_parent("table") is not None:
            continue
        if el.name == "table":
            if el.get_text(strip=True):
                # signature blocks are 1-row tables
                rows = el.find_all("tr")
                if len(rows) == 1 and len(el.get_text(" ", strip=True)) < 200:
                    items.append(("para", " — ".join(text_of(td) for td in rows[0].find_all("td") if text_of(td))))
                else:
                    items.append(("table", table_html(el)))
            continue
        cls = (el.get("class") or [""])[0]
        t = text_of(el)
        if not t:
            continue
        if cls in HEAD_CLASSES:
            items.append((HEAD_CLASSES[cls], re.sub(r"\s+", " ", t)))
        elif cls == "article":
            items.append(("article", re.sub(r"\s+", " ", t)))
        elif cls == "articleintext" and el.select_one("span.articlec"):
            # "Статья 1. <text>" in one paragraph (Constitution, amending laws)
            sp = el.select_one("span.articlec")
            head = re.sub(r"\s+", " ", text_of(sp))
            sp.decompose()
            items.append(("article", head))
            rest = text_of(el)
            if rest:
                items.append(("para", rest))
        elif cls in ("title", "titlek", "titlencpi", "titlep", "name", "nonumheader"):
            items.append(("bold", re.sub(r"\s+", " ", t)))
        elif cls in ("changeadd", "changeutrs"):
            items.append(("list", re.sub(r"\s+", " ", t)))
        elif cls in ("comment", "snoski"):
            items.append(("note", t))
        else:
            items.append(("para", t))
    order = [k for k in ORDER if any(i[0] == k for i in items)]
    level = {k: 2 + n for n, k in enumerate(order)}
    art = min(6, 2 + len(order))
    out = []
    for k, t in items:
        if k == "para":
            out.append(esc(t).replace("\n", "  \n"))
        elif k == "list":
            out.append("- " + t)
        elif k == "note":
            out.append("*" + t.replace("\n", " ").replace("*", "\\*") + "*")
        elif k == "bold":
            out.append("**" + t.replace("*", "\\*") + "**")
        elif k == "table":
            out.append(t)
        else:
            out.append("#" * min(art if k == "article" else level[k], 6) + " " + t)
    md = "\n\n".join(out) + "\n"
    return re.sub(r"(\n- [^\n]*)\n\n(?=- )", r"\1\n", md)


def yq(s):
    return '"' + (s or "").replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    today = datetime.date.today().isoformat()
    docs = os.path.join(RAW, "docs")
    counts, skipped = {}, {"repealed": 0, "amending": 0, "demo_only": [], "other": 0}
    for fn in sorted(os.listdir(docs)):
        rn = fn[:-5]
        html = open(os.path.join(docs, fn), encoding="utf-8").read()
        soup = BeautifulSoup(html, "lxml")
        uc = soup.select_one("#userContent")
        if uc is None:
            continue
        if uc.get("data-aktinforce") != "1":
            skipped["repealed"] += 1
            continue
        tnode = uc.select_one("p.title, p.titlek, p.titlencpi, p.name")
        title = re.sub(r"\s+", " ", tnode.get_text(" ", strip=True)) if tnode else rn
        if rn.startswith("v1"):
            cat, typ = "konstitutsiya", "constitution"
        elif rn.startswith("hk"):
            cat, typ = "kodeksy", "code"
        elif rn.startswith("h1"):
            cat, typ = "zakony", "act"
        else:
            skipped["other"] += 1
            continue
        if AMENDING.match(title):
            skipped["amending"] += 1
            continue
        demo = "сокращенном (демонстрационном)" in html
        if not uc.get_text(strip=True):
            skipped.setdefault("empty", []).append(rn)
            continue
        if demo:
            skipped["demo_only"].append(f"{rn}\t{title}")
            continue
        for x in uc.select(".form-access, .popup-captcha, form, script, style, a.dopinfo"):
            x.decompose()
        dp = uc.select_one("span.datepr")
        num = uc.select_one("span.number")
        date = ru_date(dp.get_text(" ", strip=True) if dp else "")
        if rn.startswith("v1"):
            title = "Конституция Республики Беларусь"
            date = date or "1994-03-15"
        chdates = [ru_date(re.sub(r"\s+", " ", x.get_text(" ", strip=True))) for x in uc.select("p.changeadd")]
        chdates = [d for d in chdates if d]
        year = (date or "0000")[:4]
        sub = os.path.join(cat, year) if cat == "zakony" else cat
        fm = ["---", f"title: {yq(title)}",
              f"identifier: {yq(num.get_text(' ', strip=True).replace(chr(160), ' ') if num else '')}",
              f"regnum: {yq(rn.upper())}", f"type: {typ}", "jurisdiction: by",
              f"language: {'be' if re.search(r'Рэспублі|Кодэкс|Закон Рэспублікі', title) else 'ru'}"]
        if date:
            fm.append(f"date: {date}")
        if chdates:
            fm.append(f"last_amended: {max(chdates)}  # date of the latest amending act listed")
        fm += ["status: in_force", f"source: \"https://etalonline.by/document/?regnum={rn}\"",
               f"retrieved: {today}", "---", "", f"# {title}", "", ""]
        out = os.path.join(REPO, sub, f"{rn}-{slug(title)}.md")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write("\n".join(fm) + convert(uc))
        counts[cat] = counts.get(cat, 0) + 1
    print(counts, {k: (len(v) if isinstance(v, list) else v) for k, v in skipped.items()})
    with open(os.path.join(RAW, "demo_only.tsv"), "w") as f:
        f.write("\n".join(skipped["demo_only"]) + "\n")


if __name__ == "__main__":
    main()
