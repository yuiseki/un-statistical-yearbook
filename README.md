# un-statistical-yearbook

A reproducible copy of the United Nations Statistical Yearbook tables that
the United Nations Statistics Division (UNSD) publishes as CSV files on
UNdata, with each table converted to Parquet.

- Source page: <https://data.un.org/Default.aspx> ("Popular statistical
  tables, country (area) and regional profiles")
- Producer: United Nations Statistics Division, UN DESA

## What is fetched

Every CSV link in the table lists of the source page: 32 tables of the
68th edition (SYB68, files named `SYB68_<table>_202511_<title>.csv`) and
one table of the 61st (`SYB61_253_...`, urban and capital city population,
2018), which the page still links. Each edition is a separate publication
and goes to its own directory, `data/raw/syb68/`, `data/raw/syb61/`. About
34.5 MB, 33 files.

Not fetched: the PDF version of each table (the same table laid out for
print), and editions the page does not link. Older files such as
`SYB67_314_202411_Internet Usage.csv` may still be on the server, but only
a guessed name would reach them and the server refuses directory listings.

The CSVs are Windows-1252, not UTF-8; the manifest records this.

## Licence

UNdata's terms of use (<https://data.un.org/Host.aspx?Content=UNdataUse>)
allow the data to be "copied freely, duplicated and further distributed
provided that UNdata is cited as the reference"; they do not mention
commercial use. Every row names its originating agency in a Source column,
and some agencies' own terms are stricter (ITU, WHO, UN Comtrade, IMF); see
`data/README.md` and `data/LICENSE`.

## How to run

```sh
uv run python scripts/01_download.py --dry-run   # list what would be fetched, with its size
uv run python scripts/01_download.py             # the full collection into data/raw/<edition>/
uv run python scripts/03_export_parquet.py       # CSV -> data/parquet/
uv run python scripts/02_verify.py               # raw files against MANIFEST.json, Parquet against the CSVs
uv run python -m pytest                          # unit tests
uv run python src/publish.py                     # dry run: the files that would go to the Hub
uv run python src/publish.py --push              # upload to huggingface.co/datasets/yuiseki/un-statistical-yearbook
```

`01_download.py` takes `--only <table numbers>` (e.g. `--only 314 253`),
`--edition <edition>` and `--limit N` to fetch a slice, and prints the
number of requests and the bytes the server states before fetching. It uses
the Python standard library only, waits at least one second between
requests, and backs off on 429 and 503. Each file is written to `.part`,
checked against Content-Length and renamed; the manifest is written after
every file. To resume an interrupted run, run the same command again:
files whose manifest entry still has the same URL and sha256 are skipped.
The page's labels and "Updated" dates are refreshed in the manifest on
every run.

`03_export_parquet.py` writes one Parquet per table and edition,
`data/parquet/<edition>/<table>_<title>.parquet`, plus
`data/parquet/tables.parquet` (one row per table) and
`data/parquet/sources.parquet` (rows per Source value per table). Column
types come from the column names (see the script's docstring); a value that
does not fit its type stops the run.

`02_verify.py` re-hashes every raw file, reads every CSV with the csv
module, and compares every cell of every Parquet with it.

`publish.py` refuses to run if the dataset card `data/README.md` does not
declare every Parquet file as a subset, or a raw file's sha256 differs from
its manifest. It uploads `data/README.md`, `data/LICENSE`,
`data/provenance.yaml`, `data/parquet/**` and the raw files unchanged.

## Layout

```
scripts/01_download.py         read the source page, fetch the CSVs, write MANIFEST.json
scripts/03_export_parquet.py   CSV -> Parquet, and the table and source lists
scripts/02_verify.py           check raw files against MANIFEST.json and Parquet against the CSVs
src/publish.py                 upload to the Hugging Face Hub (dry run by default)
tests/                         unit tests; tests/fixtures/ holds a trimmed page and trimmed CSVs
data/README.md                 the dataset card (tracked)
data/LICENSE                   terms of use and what the Parquet changes (tracked)
data/provenance.yaml           source, files, counts, checks, modifications (tracked)
data/raw/<edition>/            files as served, plus MANIFEST.json (not in git)
data/parquet/                  the Parquet (not in git)
data/work/                     CSVs transcoded to UTF-8 while exporting (not in git)
```

`MANIFEST.json` records, for each file, its URL, bytes, sha256,
Last-Modified, fetch time (UTC), encoding, and what the page states: its
label, topic and "Updated" date, and the table number, edition month and
title from the file name. The page states no row counts.
