import importlib.util
from pathlib import Path

import pytest

HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location(
    "verify", HERE.parent / "scripts" / "02_verify.py"
)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

IU = HERE / "fixtures" / "SYB68_314_202511_Internet Usage.csv"


def test_records_are_counted_without_the_title_and_header_rows():
    assert m.count_records(IU, "windows-1252") == 5


def test_a_file_in_the_wrong_encoding_fails():
    with pytest.raises(UnicodeDecodeError):
        m.count_records(IU, "utf-8")


def test_records_with_a_wrong_number_of_cells_fail(tmp_path):
    p = tmp_path / "t.csv"
    p.write_bytes(IU.read_bytes() + b"4,Afghanistan,2010\r\n")
    with pytest.raises(ValueError, match="3 cells"):
        m.count_records(p, "windows-1252")


@pytest.mark.parametrize(
    ("name", "raw", "want"),
    [
        ("area_code", "392", 392),
        ("year", "2005", 2005),
        ("value", "15.6", 15.6),
        ("value", "1,030.5", 1030.5),
        ("value", "-1,084", -1084.0),
        ("value", "7", 7.0),
        ("area", "Japan", "Japan"),
        ("footnotes", "", None),
    ],
)
def test_a_csv_cell_is_read_as_the_parquet_should_hold_it(name, raw, want):
    got = m.typed(name, raw)
    assert got == want and type(got) is type(want)
