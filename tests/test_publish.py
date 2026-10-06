import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "publish", Path(__file__).parents[1] / "src" / "publish.py"
)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


def _data(tmp_path, card=("syb68/1_t", "tables", "sources"), raw=b"x", manifest_raw=b"x"):
    d = tmp_path / "data"
    (d / "parquet" / "syb68").mkdir(parents=True)
    for p in ("syb68/1_t", "tables", "sources"):
        (d / "parquet" / f"{p}.parquet").write_bytes(b"PAR1")
    (d / "raw" / "syb68").mkdir(parents=True)
    (d / "raw" / "syb68" / "f.csv").write_bytes(raw)
    files = {"f.csv": {"sha256": hashlib.sha256(manifest_raw).hexdigest()}}
    (d / "raw" / "syb68" / "MANIFEST.json").write_text(json.dumps({"files": files}))
    text = "---\nconfigs:\n" + "".join(m.subset_entry(p) for p in card) + "---\n"
    (d / "README.md").write_text(text)
    for f in ("LICENSE", "provenance.yaml"):
        (d / f).write_text("x")
    return d


def test_subset_entry_names_edition_and_table():
    assert m.subset_entry("syb68/314_internet_usage") == (
        "- config_name: 'syb68.314_internet_usage'\n"
        "  data_files: parquet/syb68/314_internet_usage.parquet\n"
    )
    assert m.subset_entry("tables") == "- config_name: 'tables'\n  data_files: parquet/tables.parquet\n"


def test_collect_lists_card_parquet_and_raw(tmp_path):
    assert m.collect(_data(tmp_path)) == [
        "README.md", "LICENSE", "provenance.yaml", "parquet/sources.parquet",
        "parquet/syb68/1_t.parquet", "parquet/tables.parquet",
        "raw/syb68/f.csv", "raw/syb68/MANIFEST.json",
    ]  # fmt: skip


def test_a_parquet_the_card_does_not_declare_stops_it(tmp_path):
    with pytest.raises(SystemExit, match="syb68.1_t"):
        m.collect(_data(tmp_path, card=("tables", "sources")))


def test_a_raw_file_unlike_its_manifest_stops_it(tmp_path):
    with pytest.raises(SystemExit, match="raw/syb68/f.csv"):
        m.collect(_data(tmp_path, raw=b"changed"))
