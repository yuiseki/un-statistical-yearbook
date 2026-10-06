#!/usr/bin/env python3
"""Fetch the CSV tables of the United Nations Statistical Yearbook from UNdata.

UNdata (https://data.un.org/Default.aspx) lists the yearbook tables under
"Popular statistical tables, country (area) and regional profiles", each as a
PDF and a CSV link below a short label, grouped under a topic, with an
"Updated: <date>" note. This script reads that page and takes every CSV link
in its lists (links inside HTML comments are not links and are ignored). The
PDFs are the same tables laid out for print and are not taken.

The file names carry the edition: SYB68_314_202511_Internet Usage.csv is
table 314 of the 68th edition (SYB68), prepared in November 2025 (202511).
Each edition is a separate publication and goes to its own directory,
data/raw/<edition>/ (syb68, syb61, ...). The page still links one table of an
older edition (SYB61_253, urban and capital city population), which lands in
data/raw/syb61/. Editions the page does not link are not fetched: their file
names could only be guessed, and the server refuses directory listings.

data/raw/<edition>/MANIFEST.json records for each file its URL, bytes,
sha256, Last-Modified, fetch time (UTC) and what the page states about it:
label, topic, "Updated" date, table number and edition month, and the
encoding (Windows-1252). The page's statements are refreshed on every run. It is written
after every file, so an interrupted run resumes where it stopped; a file
whose manifest entry has the same URL and whose sha256 still matches is not
fetched again.

    uv run python scripts/01_download.py                  # everything the page links
    uv run python scripts/01_download.py --only 314 253   # by table number
    uv run python scripts/01_download.py --limit 3        # the first three links
    uv run python scripts/01_download.py --dry-run        # the estimate only
"""

import argparse
import hashlib
import json
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PAGE_URL = "https://data.un.org/Default.aspx"
TERMS_URL = "https://data.un.org/Host.aspx?Content=UNdataUse"
UA = "un-statistical-yearbook/1 (+https://github.com/yuiseki/un-statistical-yearbook)"
DELAY = 1.0
RETRIES = 5
NAME = re.compile(r"SYB([0-9]+)_([0-9]+)(?:_([0-9]{6}))?_(.+)\.csv")
# UNdata states no encoding. The files fail as UTF-8 (0x92, 0xF4) and differ
# from Latin-1 in 0x91/0x92 (curly quotes); all decode strictly as Windows-1252.
ENCODING = "windows-1252"
PAGE_FIELDS = ("label", "topic", "page_updated", "table", "month", "title")
UPDATED = re.compile(r"Updated:\s*([0-9]{1,2}-[A-Za-z]{3}-[0-9]{4})")

_last_request = 0.0


class _Listing(HTMLParser):
    """Walk <div class="DataSourceList">: <p>topic</p>, <li>label</li>, <li><a>PDF</a> | <a>CSV</a> <span>Updated</span></li>."""

    def __init__(self, base: str):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.depth = 0  # div depth inside the list, 0 = outside
        self.tag: str | None = None  # 'p', 'li' or 'span' whose text is being read
        self.text: list[str] = []
        self.topic = self.label = ""
        self.links: list[dict] = []
        self.pending: list[dict] = []  # CSV links of the current <li>, waiting for its Updated span

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div":
            if self.depth:
                self.depth += 1
            elif "DataSourceList" in (a.get("class") or "").split():
                self.depth = 1
            return
        if not self.depth:
            return
        if tag == "p" or tag == "span" or (tag == "li" and "NoBullets" not in (a.get("class") or "")):
            self.tag, self.text = tag, []
        elif tag == "li":
            self.pending = []
        elif tag == "a" and a.get("href"):
            path = urllib.parse.unquote(urllib.parse.urlparse(a["href"]).path)
            if path.lower().endswith(".csv"):
                url = urllib.parse.urljoin(self.base, urllib.parse.quote(path))
                link = {"url": url, "file": Path(path).name, "label": self.label,
                        "topic": self.topic, "page_updated": None}  # fmt: skip
                self.links.append(link)
                self.pending.append(link)

    def handle_endtag(self, tag):
        if tag == "div" and self.depth:
            self.depth -= 1
        elif tag == self.tag:
            text = " ".join("".join(self.text).split())
            if tag == "p":
                self.topic = text
            elif tag == "li":
                self.label = text
            elif tag == "span":
                mt = UPDATED.search(text)
                for link in self.pending:
                    link["page_updated"] = mt.group(1) if mt else None
            self.tag = None

    def handle_data(self, data):
        if self.tag:
            self.text.append(data)


def parse_listing(html: str, base: str) -> list[dict]:
    """Every CSV link of the page's table lists, in page order, with label, topic and Updated date."""
    p = _Listing(base)
    p.feed(html)
    out, seen = [], set()
    for link in p.links:
        if link["url"] in seen:
            continue
        seen.add(link["url"])
        edition, table, month, title = parse_name(link["file"])
        out.append({**link, "edition": edition, "table": table, "month": month, "title": title})
    return out


def parse_name(name: str) -> tuple[str, int, str | None, str]:
    """SYB68_314_202511_Internet Usage.csv -> ('syb68', 314, '202511', 'Internet Usage')."""
    mt = NAME.fullmatch(name)
    if not mt:
        raise SystemExit(f"a CSV name outside the SYB<edition>_<table>[_<yyyymm>]_<title> pattern: {name}")
    return "syb" + mt.group(1), int(mt.group(2)), mt.group(3), mt.group(4)


def select(tables: list[dict], only=None, editions=None, limit=None) -> list[dict]:
    out = [
        t for t in tables
        if (not only or t["table"] in only) and (not editions or t["edition"] in editions)
    ]  # fmt: skip
    return out[:limit] if limit else out


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def plan(tables: list[dict], manifests: dict, raw: Path) -> list[dict]:
    """The tables still to fetch: not in their edition's manifest, another URL, or another sha256."""
    todo = []
    for t in tables:
        e = manifests.get(t["edition"], {}).get("files", {}).get(t["file"])
        p = raw / t["edition"] / t["file"]
        if e and e["url"] == t["url"] and p.exists() and sha256(p) == e["sha256"]:
            continue
        todo.append(t)
    return todo


def annotate(entry: dict, t: dict) -> bool:
    """Write what the page states about a file, and its encoding, into its entry; True if anything changed."""
    want = {**{k: t[k] for k in PAGE_FIELDS}, "encoding": ENCODING}
    changed = any(entry.get(k) != v for k, v in want.items())
    entry.update(want)
    return changed


def should_retry(status: int) -> bool:
    return status in (429, 503)


def _open(url: str, method: str = "GET"):
    """One request, at least DELAY after the previous one; 429 and 503 back off and retry."""
    global _last_request
    for attempt in range(RETRIES):
        wait = DELAY - (time.monotonic() - _last_request)
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(url, headers={"User-Agent": UA}, method=method)
        try:
            r = urllib.request.urlopen(req, timeout=300)
            _last_request = time.monotonic()
            return r
        except urllib.error.HTTPError as ex:
            _last_request = time.monotonic()
            if not should_retry(ex.code) or attempt == RETRIES - 1:
                raise
            after = ex.headers.get("Retry-After", "")
            pause = int(after) if after.isdigit() else 30 * 2**attempt
            print(f"{ex.code} on {url}; waiting {pause} s", file=sys.stderr, flush=True)
            time.sleep(pause)
    raise AssertionError("unreachable")


def get_text(url: str) -> str:
    with _open(url) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8")


def head_length(url: str) -> int | None:
    with _open(url, "HEAD") as r:
        v = r.headers.get("Content-Length")
    return int(v) if v else None


def fetch(url: str, dest: Path) -> dict:
    tmp = dest.with_suffix(dest.suffix + ".part")
    with _open(url) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f, 1 << 20)
        length = r.headers.get("Content-Length")
        lm = r.headers.get("Last-Modified", "")
    got = tmp.stat().st_size
    if length is not None and got != int(length):
        tmp.unlink()
        raise SystemExit(f"{url}: got {got} bytes, the server stated {length}")
    tmp.replace(dest)
    return {
        "url": url,
        "bytes": got,
        "sha256": sha256(dest),
        "last_modified": lm,
        "fetched_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def load_manifest(edition: str) -> dict:
    p = RAW / edition / "MANIFEST.json"
    return json.loads(p.read_text()) if p.exists() else {"files": {}}


def write_manifest(edition: str, manifest: dict) -> None:
    d = RAW / edition
    d.mkdir(parents=True, exist_ok=True)
    manifest.update(
        {
            "edition": edition,
            "source_page": PAGE_URL,
            "terms_of_use": TERMS_URL,
            "files": dict(sorted(manifest["files"].items())),
        }
    )
    tmp = d / "MANIFEST.json.part"
    tmp.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    tmp.replace(d / "MANIFEST.json")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", type=int, nargs="+", help="table numbers, e.g. 314 253")
    ap.add_argument("--edition", nargs="+", help="editions, e.g. syb68")
    ap.add_argument("--limit", type=int, help="at most N links, in page order")
    ap.add_argument("--dry-run", action="store_true", help="print the estimate and stop")
    a = ap.parse_args()

    html = get_text(PAGE_URL)
    listed = parse_listing(html, PAGE_URL)
    tables = select(listed, set(a.only or ()), set(a.edition or ()), a.limit)
    editions = sorted({t["edition"] for t in tables})
    manifests = {e: load_manifest(e) for e in editions}
    todo = plan(tables, manifests, RAW)

    stated = [head_length(t["url"]) for t in todo]
    total = sum(n or 0 for n in stated)
    print(
        f"{len(listed)} CSV links on the page, {len(tables)} selected, {len(todo)} to fetch: "
        f"{len(todo)} GET requests to come (1 page + {len(todo)} HEAD made), "
        f"{total:,} bytes stated, about {2 * len(todo) * DELAY:.0f} s",
        flush=True,
    )
    if a.dry_run:
        return 0

    for t in todo:
        e = t["edition"]
        (RAW / e).mkdir(parents=True, exist_ok=True)
        entry = fetch(t["url"], RAW / e / t["file"])
        annotate(entry, t)
        manifests[e]["files"][t["file"]] = entry
        write_manifest(e, manifests[e])
        print(f"{e}/{t['file']}: {entry['bytes']:,} bytes, {entry['last_modified']}", flush=True)
    # the page's label, topic or Updated date may change while the file does not
    for e in editions:
        files = manifests[e]["files"]
        stale = [annotate(files[t["file"]], t) for t in tables if t["edition"] == e and t["file"] in files]
        if any(stale) or not (RAW / e / "MANIFEST.json").exists():
            write_manifest(e, manifests[e])
    print(f"{len(tables)} selected, {len(todo)} fetched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
