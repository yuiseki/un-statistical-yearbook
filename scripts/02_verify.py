#!/usr/bin/env python3
"""Check every edition under data/raw/ against its MANIFEST.json, and the Parquet against the CSVs.

For each raw file: size and sha256 as in the manifest, decoded strictly in
the encoding the manifest records, read to the end with the csv module, and
every record (rows after the title and header rows) has as many cells as the
header. Prints its record count.

For each Parquet file scripts/03_export_parquet.py made, against the records
of its CSV, read with the csv module, whose Source export.source_status()
publishes (a table with none must have no Parquet file):
  - as many rows as those records, the column names column_names()
    gives for the CSV's header, in order, each of the type its name gives
  - every cell equal to the CSV's, row by row in order: text as text (an
    empty cell as NULL), area_code and year as Python's int reads them, value
    as Python's float reads it once its thousands separators are removed
  - a plain DuckDB with extension autoloading turned off opens it
  - no row group carries a bloom filter
And tables.parquet has one row per CSV with its record count and published
record count, sources.parquet the per-Source counts of the CSV with the
agency and decision source_status() gives.

Prints one ok/FAIL line per check and exits non-zero on any failure.

    uv run python scripts/02_verify.py
"""

import collections
import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PQ = ROOT / "data" / "parquet"

_spec = importlib.util.spec_from_file_location("export", ROOT / "scripts" / "03_export_parquet.py")
export = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(export)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_csv(path: Path, encoding: str) -> tuple[list[str], list[list[str]]]:
    """(header, records): the title row dropped, decoded strictly; ValueError on a ragged record."""
    with open(path, newline="", encoding=encoding, errors="strict") as f:
        rows = list(csv.reader(f))
    header, records = rows[1], rows[2:]
    for i, r in enumerate(records, start=3):
        if len(r) != len(header):
            raise ValueError(f"line {i} has {len(r)} cells, the header {len(header)}")
    return header, records


def count_records(path: Path, encoding: str) -> int:
    return len(read_csv(path, encoding)[1])


def typed(name: str, raw: str):
    """What the Parquet should hold for one CSV cell."""
    t = export.column_type(name)
    if t == "INTEGER":
        return int(raw)
    if t == "DOUBLE":
        return float(raw.replace(",", ""))
    return raw if raw != "" else None


def published_records(records: list[list[str]]) -> list[list[str]]:
    """The records whose Source the export publishes, in order."""
    return [r for r in records if export.source_status(typed("source", r[-1]))[1]]


def verify_parquet(edition: str, name: str, e: dict, header, records, tables, sources) -> int:
    import duckdb

    failures = 0

    def check(ok: bool, what: str) -> None:
        nonlocal failures
        print(("ok   " if ok else "FAIL ") + what)
        failures += not ok

    stem = f"{e['table']}_{export.slug(e['title'])}"
    subset = f"{edition}.{stem}"
    p = PQ / edition / f"{stem}.parquet"
    everything, records = records, published_records(records)
    t = tables.get(subset)
    check(t == (len(everything), len(records)),
          f"{subset}: tables.parquet says {t} rows (all, published)")  # fmt: skip
    want = collections.Counter(r[-1] for r in everything)
    status = {s: export.source_status(typed("source", s)) for s in want}
    got_sources = sources.get(subset, {})
    check(got_sources == {s: (*status[s][:2], n) for s, n in want.items()},
          f"{subset}: sources.parquet has the {len(want)} Source value(s), their agency, "
          "decision and counts")  # fmt: skip
    if not records:
        check(not p.exists(), f"{subset}: no published rows and no Parquet file")
        return failures
    if not p.exists():
        check(False, f"{subset}: {p} missing")
        return failures
    names = export.column_names(header)
    con = duckdb.connect()
    rel = con.sql(f"select * from '{p}'")
    check(rel.columns == names, f"{subset}: columns {', '.join(rel.columns)}")
    wrong = {c: str(t) for c, t in zip(rel.columns, rel.types, strict=True)
             if str(t) != export.column_type(c)}  # fmt: skip
    check(not wrong, f"{subset}: every column of the type its name gives ({wrong or 'all'})")
    got = rel.fetchall()
    check(len(got) == len(records), f"{subset}: {len(got):,} rows, the CSV has {len(records):,}")
    diff = [
        (i, c, raw, g)
        for i, (r, prow) in enumerate(zip(records, got, strict=False))
        for c, raw, g in zip(names, r, prow, strict=True)
        if typed(c, raw) != g
    ]
    cells = len(records) * len(names)
    check(not diff, f"{subset}: all {cells:,} cells equal the CSV ({diff[:3] or 'none differ'})")

    plain = duckdb.connect(
        config={"autoload_known_extensions": False, "autoinstall_known_extensions": False}
    )
    try:
        n = plain.sql(f"select count(*) from '{p}' where area_code = 392").fetchone()[0]
        check(True, f"{subset}: a DuckDB without extensions opens it ({n:,} rows for Japan)")
    except duckdb.Error as ex:
        check(False, f"{subset}: a DuckDB without extensions fails on it: {ex}")
    bloom = con.sql(
        "select count(*) filter (where bloom_filter_offset is not null) "
        f"from parquet_metadata('{p}')"
    ).fetchone()[0]
    check(bloom == 0, f"{subset}: no bloom filters")

    return failures


def verify(d: Path, tables: dict, sources: dict) -> tuple[int, int]:
    failures = records_total = 0
    files = json.loads((d / "MANIFEST.json").read_text())["files"]
    for name, e in files.items():
        p = d / name
        tag = f"{d.name}/{name}"
        if not p.exists():
            print(f"FAIL {tag}: missing")
            failures += 1
            continue
        if p.stat().st_size != e["bytes"] or sha256(p) != e["sha256"]:
            print(f"FAIL {tag}: size or sha256 differs from the manifest")
            failures += 1
            continue
        print(f"ok   {tag}: sha256")
        enc = e.get("encoding", "utf-8")
        try:
            header, records = read_csv(p, enc)
            export.column_names(header)
        except (OSError, UnicodeDecodeError, csv.Error, ValueError) as ex:
            print(f"FAIL {tag}: {ex}")
            failures += 1
            continue
        print(f"ok   {tag}: {len(records):,} records ({enc})")
        records_total += len(records)
        failures += verify_parquet(d.name, name, e, header, records, tables, sources)
    return failures, records_total


def main() -> int:
    import duckdb

    dirs = sorted(p.parent for p in RAW.glob("*/MANIFEST.json"))
    if not dirs:
        print("FAIL no MANIFEST.json under data/raw/")
        return 1
    tl, sl = PQ / "tables.parquet", PQ / "sources.parquet"
    if not (tl.exists() and sl.exists()):
        print("FAIL tables.parquet or sources.parquet missing; run scripts/03_export_parquet.py")
        return 1
    con = duckdb.connect()
    tables = {s: (n, k) for s, n, k in
              con.sql(f"select subset, rows, rows_published from '{tl}'").fetchall()}  # fmt: skip
    sources: dict = collections.defaultdict(dict)
    q = f"select subset, source, agency, published, rows from '{sl}'"
    for subset, source, agency, published, n in con.sql(q).fetchall():
        sources[subset][source or ""] = (agency, published, n)
    failures = total = files = 0
    for d in dirs:
        f, n = verify(d, tables, sources)
        failures, total = failures + f, total + n
        files += len(json.loads((d / "MANIFEST.json").read_text())["files"])
    extra = len(tables) != files
    if extra:
        print(f"FAIL tables.parquet lists {len(tables)} tables, the manifests {files} files")
    failures += extra
    print(f"{len(dirs)} edition(s), {files} files, {total:,} records")
    print("all ok" if not failures else f"{failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
