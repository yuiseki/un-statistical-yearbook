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

Only rows whose originating agency (the Source column) allows redistribution
under its own terms are written. UNdata lets its data be redistributed with
citation, but it does not speak for the agencies it republishes, so each
Source is matched against SOURCES below: the first pattern that matches
names the agency and whether its rows are published. A Source that matches
nothing is left out as unchecked, so a new agency in a new edition is never
published by default. A table with no published rows gets no Parquet file.
tables.parquet counts the published and excluded rows of every table, and
sources.parquet gives each Source its agency, whether it is published and why.

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
# (pattern searched in Source, agency, published, reason); the first match wins,
# so UN Comtrade comes before the rest of UNSD.
SOURCES = [
    (r"UN COMTRADE", "UN Comtrade", False,
     "UN Comtrade: re-dissemination is limited and may need a distribution licence; "
     "https://uncomtrade.org/docs/faqs-on-use-and-re-dissemination/"),
    (r"World Health Organi[sz]ation", "WHO", False,
     "WHO datasets are licensed for public health purposes only, and any other alteration "
     "needs WHO's prior written authorization; "
     "https://www.who.int/about/policies/publishing/data-policy/terms-and-conditions"),
    (r"International Telecommunication Union", "ITU", False,
     "ITU content is for personal, educational or non-commercial use; distributing it or "
     "any commercial use needs ITU's prior written permission; "
     "https://www.itu.int/en/about/Pages/terms-of-use.aspx"),
    (r"International Monetary Fund", "IMF", False,
     "IMF data need permission for commercial reuse and for re-publishing a substantial "
     "amount; https://www.imf.org/en/about/copyright-and-terms"),
    (r"^United Nations Population Division", "UN Population Division", True,
     "World Population and Urbanization Prospects are CC BY 3.0 IGO"),
    (r"^United Nations Statistics Division", "UNSD", True,
     "UNSD's own data under the UNdata terms of use"),
    (r"^Food and Agriculture Organization", "FAO", True, "FAOSTAT is CC BY 4.0"),
    (r"^International Labour Organization", "ILO", True, "ILOSTAT is CC BY 4.0"),
    (r"^Organisation for Economic Co-operation and Development", "OECD", True,
     "OECD terms allow reuse, including commercial, with attribution"),
    (r"^United Nations High Commissioner for Refugees", "UNHCR", True,
     "UNHCR population statistics are CC BY 4.0"),
]  # fmt: skip


def source_status(source: str | None) -> tuple[str, bool, str]:
    """(agency, published, reason) for a Source value; unmatched sources are not published."""
    for pattern, agency, published, reason in SOURCES:
        if source and re.search(pattern, source):
            return agency, published, reason
    return "unchecked", False, "the originating agency's terms are not checked yet"


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
            con.execute(f"create or replace temp table t as {select_sql(utf8, names, name)}")
            utf8.unlink()
            subset = f"{edition}.{stem}"
            counts = con.sql(
                "select source, count(*) from t group by source order by 2 desc, 1"
            ).fetchall()
            status = {s: source_status(s) for s, _ in counts}
            keep = [s for s, _ in counts if status[s][1]]
            n = sum(c for _, c in counts)
            kept = sum(c for s, c in counts if status[s][1])
            if keep:
                con.execute(
                    f"copy (select * from t where source in ?) to '{dest}' ({COPY})", [keep]
                )
            elif dest.exists():
                dest.unlink()
            tables.append(
                (edition, e["table"], subset,
                 f"parquet/{edition}/{stem}.parquet" if keep else None,
                 f"raw/{edition}/{name}", code, title, e.get("label"), e.get("topic"),
                 e.get("month"), e.get("page_updated"), n, kept, n - kept, len(names),
                 len(counts))
            )  # fmt: skip
            sources += [(edition, e["table"], subset, s, *status[s], c) for s, c in counts]
            print(f"{subset}: {kept:,} of {n:,} rows published, {len(counts)} source(s)",
                  flush=True)  # fmt: skip
        work.rmdir()

    con.execute(
        "create table tables (edition varchar, table_number integer, subset varchar, "
        "parquet varchar, raw varchar, table_code varchar, title varchar, page_label varchar, "
        "topic varchar, edition_month varchar, page_updated varchar, rows bigint, "
        "rows_published bigint, rows_excluded bigint, columns integer, sources integer)"
    )
    con.executemany(f"insert into tables values ({', '.join(['?'] * 16)})", tables)
    con.execute(
        "create table sources (edition varchar, table_number integer, subset varchar, "
        "source varchar, agency varchar, published boolean, reason varchar, rows bigint)"
    )
    con.executemany(f"insert into sources values ({', '.join(['?'] * 8)})", sources)
    con.execute(
        f"copy (select * from tables order by edition, table_number) "
        f"to '{OUT / 'tables.parquet'}' ({COPY})"
    )
    con.execute(
        f"copy (select * from sources order by edition, table_number, rows desc, source) "
        f"to '{OUT / 'sources.parquet'}' ({COPY})"
    )
    published = sum(1 for t in tables if t[3])
    print(f"tables.parquet: {len(tables)} tables, {published} with published rows; "
          f"sources.parquet: {len(sources)} rows")  # fmt: skip
    return 0


if __name__ == "__main__":
    sys.exit(main())
