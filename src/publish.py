#!/usr/bin/env python3
"""Push the card, the licence, the provenance, the Parquet and the raw files to the Hub.

Every raw file goes up unchanged after its sha256 is checked against
data/raw/<edition>/MANIFEST.json, and the card must declare every Parquet
file under data/parquet/ as a subset: '<edition>.<table>' for a table,
'tables' and 'sources' for the two lists. A new edition is added beside the
others.

A raw CSV goes up only when every row of it is published: a table with any
row left out for its originating agency's terms (rows_excluded in
parquet/tables.parquet) keeps its raw file local. The manifests go up whole,
so the withheld files stay listed with their hashes.

    uv run python src/publish.py             # dry run: list the files and their total size
    uv run python src/publish.py --push
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPO = "yuiseki/un-statistical-yearbook"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def subset_entry(path: str) -> str:
    """'syb68/314_internet_usage' -> its configs entry, named 'syb68.314_internet_usage'."""
    return f"- config_name: '{path.replace('/', '.')}'\n  data_files: parquet/{path}.parquet\n"


def withheld(data: Path) -> set[str]:
    """Raw files (relative to data/) of tables with any row left out of the Parquet."""
    import duckdb

    tables = data / "parquet" / "tables.parquet"
    if not tables.exists():
        raise SystemExit("no parquet/tables.parquet; run scripts/03_export_parquet.py")
    rows = duckdb.sql(f"select raw from '{tables}' where rows_excluded > 0").fetchall()
    return {r for (r,) in rows}


def collect(data: Path) -> list[str]:
    """The files to upload, relative to data/; stops on anything the card or a manifest refutes."""
    card = (data / "README.md").read_text(encoding="utf-8")
    files = ["README.md", "LICENSE", "provenance.yaml"]
    parquet = sorted((data / "parquet").rglob("*.parquet"))
    if not parquet:
        raise SystemExit("no Parquet under data/parquet/; run scripts/03_export_parquet.py")
    for p in parquet:
        rel = p.relative_to(data / "parquet").with_suffix("").as_posix()
        if subset_entry(rel) not in card:
            raise SystemExit(f"the card does not declare the subset {rel.replace('/', '.')}")
        files.append(p.relative_to(data).as_posix())
    for declared in re.findall(r"^  data_files: (parquet/\S+\.parquet)$", card, re.M):
        if not (data / declared).exists():
            name = declared.removeprefix("parquet/").removesuffix(".parquet").replace("/", ".")
            raise SystemExit(f"the card declares the subset {name}, which has no Parquet")
    hold = withheld(data)
    for mpath in sorted((data / "raw").glob("*/MANIFEST.json")):
        d = mpath.parent
        for name, m in json.loads(mpath.read_text())["files"].items():
            if f"raw/{d.name}/{name}" in hold:
                continue
            if sha256(d / name) != m["sha256"]:
                raise SystemExit(f"raw/{d.name}/{name} is not the file in its manifest")
            files.append(f"raw/{d.name}/{name}")
        files.append(f"raw/{d.name}/MANIFEST.json")
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=REPO)
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()

    files = collect(DATA)
    total = 0
    for f in files:
        size = (DATA / f).stat().st_size
        total += size
        print(f"  {size:>12,}  {f}")
    print(f"{a.repo}\n  {len(files)} files, {total:,} bytes ({total / 1e6:.1f} MB)")
    if not a.push:
        print("\ndry run. pass --push to upload")
        return 0

    from huggingface_hub import HfApi

    api = HfApi()
    api.create_repo(a.repo, repo_type="dataset", exist_ok=True, private=False)
    api.upload_folder(
        folder_path=str(DATA), repo_id=a.repo, repo_type="dataset", allow_patterns=files
    )
    print(f"\npushed to https://huggingface.co/datasets/{a.repo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
