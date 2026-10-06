#!/usr/bin/env python3
"""Turn every yearbook CSV into one Parquet file, and list the tables and their sources.

    data/parquet/<edition>/<table>_<slug>.parquet   one per CSV, e.g. syb68/314_internet_usage.parquet
    data/parquet/tables.parquet                     one row per table and edition
    data/parquet/sources.parquet                    rows per Source value, per table and edition

Every yearbook CSV has the same layout. The first row is the yearbook's own
table code and title ("T30,Internet Usage,,,,,"), the second the header, and
then one record per row:

    Region/Country/Area,,Year,Series,Value,Footnotes,Source

Seven tables have one more pair of columns between Series and Value, an
attribute of the row and its footnote ("National currency", "National
currency footnote"; "Capital City", ...). Any other header stops the run.

The CSVs are Windows-1252 (curly quotes 0x91/0x92, "Côte d’Ivoire", "LDC§"),
not UTF-8 and not Latin-1. Each is decoded strictly in the encoding its
MANIFEST.json records and written as UTF-8 to data/work/<edition>/, which
DuckDB reads with every column as text and no type inference.

Column names: Region/Country/Area is area_code (the M49 code), the unnamed
column beside it is area (its name), Year, Series, Value, Footnotes and
Source become year, series, value, footnotes and source, and an attribute
column is its header in snake case ("%" as "pct") with "_footnote" for its
footnote. Types come from those names: area_code and year are INTEGER, value
is DOUBLE, everything else VARCHAR. Each value is checked with a regular
expression before the cast, and a value that does not fit, or is empty,
stops the run with the file, the column and the value. Value is written with
thousands separators ("1,030.5"); they are removed before the cast. An empty
text cell is NULL. Rows keep the order of the CSV.

    uv run python scripts/03_export_parquet.py
"""

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "parquet"
WORK = ROOT / "data" / "work"

LEFT = ["Region/Country/Area", "", "Year", "Series"]
RIGHT = ["Value", "Footnotes", "Source"]
FIXED = {
    "Region/Country/Area": "area_code", "": "area", "Year": "year", "Series": "series",
    "Value": "value", "Footnotes": "footnotes", "Source": "source",
}  # fmt: skip
TYPES = {"area_code": "INTEGER", "year": "INTEGER", "value": "DOUBLE"}
PATTERNS = {
    "area_code": ("[0-9]+", "an integer"),
    "year": ("[0-9]{4}", "a year"),
    "value": (r"-?([0-9]+|[0-9]{1,3}(,[0-9]{3})+)(\.[0-9]+)?", "a number"),
}
NUMBER_RE = PATTERNS["value"][0]
COPY = "format parquet, compression zstd, write_bloom_filter false"


def snake(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower().replace("%", "pct")).strip("_")


slug = snake


def column_names(header: list[str]) -> list[str]:
    """Parquet column names for a yearbook header; ValueError on any other shape."""
    if header[:4] != LEFT or header[-3:] != RIGHT or len(header) not in (7, 9):
        raise ValueError(f"not a yearbook header: {header}")
    names = [FIXED[h] for h in header[:4]]
    if len(header) == 9:
        attr, note = header[4], header[5]
        if not attr or note != f"{attr} footnote":
            raise ValueError(f"not an attribute column and its footnote: {header[4:6]}")
        names += [snake(attr), snake(attr) + "_footnote"]
    return names + [FIXED[h] for h in RIGHT]


def column_type(name: str) -> str:
    return TYPES.get(name, "VARCHAR")


def read_title(path: Path, encoding: str = "utf-8") -> tuple[str, str]:
    with open(path, newline="", encoding=encoding, errors="strict") as f:
        row = next(csv.reader(f))
    return row[0], row[1]


def read_header(path: Path, encoding: str = "utf-8") -> list[str]:
    with open(path, newline="", encoding=encoding, errors="strict") as f:
        r = csv.reader(f)
        next(r)
        return next(r)


def transcode(src: Path, dst: Path, encoding: str) -> None:
    """Decode strictly (a byte the encoding does not define stops the run), write UTF-8."""
    with open(src, newline="", encoding=encoding, errors="strict") as f:
        text = f.read()
    with open(dst, "w", newline="", encoding="utf-8") as f:
        f.write(text)


def _expr(label: str, name: str) -> str:
    c, t = f'"{name}"', column_type(name)
    if t == "VARCHAR":
        return c
    pattern, what = PATTERNS[name]
    cast = f"replace({c}, ',', '')" if name == "value" else c
    return (
        f"case when regexp_full_match({c}, '{pattern}') then cast({cast} as {t}) "
        f"else error('{label}: {name} is not {what}: ' || coalesce({c}, '(empty)')) end"
    )


def select_sql(path: Path, names: list[str], label: str) -> str:
    """Every record of the CSV (title and header rows skipped), typed by column name, in order."""
    label = label.replace("'", "''")
    cols = ", ".join(f"'{n}': 'VARCHAR'" for n in names)
    src = (
        f"read_csv('{path}', columns = {{{cols}}}, header = false, skip = 2, delim = ',', "
        "quote = '\"', escape = '\"', auto_detect = false, strict_mode = true)"
    )
    exprs = ", ".join(f'{_expr(label, n)} as "{n}"' for n in names)
    return f"select {exprs} from {src}"


def main() -> int:
    import duckdb

    con = duckdb.connect()
    con.execute("set memory_limit = '8GB'")
    con.execute("set preserve_insertion_order = true")
    manifests = sorted(RAW.glob("*/MANIFEST.json"))
    if not manifests:
        raise SystemExit("no data/raw/<edition>/MANIFEST.json")
    tables, sources = [], []
    for mpath in manifests:
        edition = mpath.parent.name
        files = json.loads(mpath.read_text())["files"]
        work, out = WORK / edition, OUT / edition
        work.mkdir(parents=True, exist_ok=True)
        out.mkdir(parents=True, exist_ok=True)
        for name, e in sorted(files.items(), key=lambda kv: kv[1]["table"]):
            enc = e.get("encoding", "utf-8")
            utf8 = work / name
            transcode(mpath.parent / name, utf8, enc)
            code, title = read_title(utf8)
            names = column_names(read_header(utf8))
            stem = f"{e['table']}_{slug(e['title'])}"
            dest = out / f"{stem}.parquet"
            con.execute(f"copy ({select_sql(utf8, names, name)}) to '{dest}' ({COPY})")
            utf8.unlink()
            subset = f"{edition}.{stem}"
            counts = con.sql(
                f"select source, count(*) from '{dest}' group by source order by 2 desc, 1"
            ).fetchall()
            n = sum(c for _, c in counts)
            tables.append(
                (edition, e["table"], subset, f"parquet/{edition}/{stem}.parquet",
                 f"raw/{edition}/{name}", code, title, e.get("label"), e.get("topic"),
                 e.get("month"), e.get("page_updated"), n, len(names), len(counts))
            )  # fmt: skip
            sources += [(edition, e["table"], subset, s, c) for s, c in counts]
            print(f"{subset}: {n:,} rows, {len(counts)} source(s), {dest.stat().st_size:,} bytes",
                  flush=True)  # fmt: skip
        work.rmdir()

    con.execute(
        "create table tables (edition varchar, table_number integer, subset varchar, "
        "parquet varchar, raw varchar, table_code varchar, title varchar, page_label varchar, "
        "topic varchar, edition_month varchar, page_updated varchar, rows bigint, "
        "columns integer, sources integer)"
    )
    con.executemany(f"insert into tables values ({', '.join(['?'] * 14)})", tables)
    con.execute(
        "create table sources (edition varchar, table_number integer, subset varchar, "
        "source varchar, rows bigint)"
    )
    con.executemany("insert into sources values (?, ?, ?, ?, ?)", sources)
    con.execute(
        f"copy (select * from tables order by edition, table_number) "
        f"to '{OUT / 'tables.parquet'}' ({COPY})"
    )
    con.execute(
        f"copy (select * from sources order by edition, table_number, rows desc, source) "
        f"to '{OUT / 'sources.parquet'}' ({COPY})"
    )
    print(f"tables.parquet: {len(tables)} tables; sources.parquet: {len(sources)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
