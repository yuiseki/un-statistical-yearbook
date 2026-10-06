import importlib.util
from pathlib import Path

import pytest

HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location(
    "download", HERE.parent / "scripts" / "01_download.py"
)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

PAGE = (HERE / "fixtures" / "Default.aspx.html").read_text(encoding="utf-8")
CSV = "https://data.un.org/_Docs/SYB/CSV/"


def test_listing_has_every_csv_link_and_no_pdf_or_commented_link():
    tables = m.parse_listing(PAGE, m.PAGE_URL)
    names = [t["file"] for t in tables]
    assert names == [
        "SYB68_1_202511_Population, Surface Area and Density.csv",
        "SYB68_327_202511_International Migrants and Refugees.csv",
        "SYB68_246_202511_Population Growth, Fertility and Mortality Indicators.csv",
        "SYB61_253_Population Growth Rates in Urban areas and Capital cities.csv",
        "SYB68_230_202511_GDP and GDP Per Capita.csv",
        "SYB68_153_202511_Gross Value Added by Economic Activity.csv",
        "SYB68_314_202511_Internet Usage.csv",
    ]


def test_listing_quotes_the_url_and_keeps_label_topic_and_updated():
    t = {t["file"]: t for t in m.parse_listing(PAGE, m.PAGE_URL)}
    iu = t["SYB68_314_202511_Internet Usage.csv"]
    assert iu["url"] == CSV + "SYB68_314_202511_Internet%20Usage.csv"
    assert iu["label"] == "Internet usage"
    assert iu["topic"] == "Communication"
    assert iu["page_updated"] == "22-Dec-2025"
    pop = t["SYB68_1_202511_Population, Surface Area and Density.csv"]
    assert pop["url"] == CSV + "SYB68_1_202511_Population%2C%20Surface%20Area%20and%20Density.csv"
    assert pop["page_updated"] == "2-Mar-2026"
    assert pop["topic"] == "Population"


@pytest.mark.parametrize(
    ("name", "want"),
    [
        ("SYB68_314_202511_Internet Usage.csv", ("syb68", 314, "202511", "Internet Usage")),
        ("SYB68_1_202511_Population, Surface Area and Density.csv",
         ("syb68", 1, "202511", "Population, Surface Area and Density")),
        ("SYB61_253_Population Growth Rates in Urban areas and Capital cities.csv",
         ("syb61", 253, None, "Population Growth Rates in Urban areas and Capital cities")),
    ],
)  # fmt: skip
def test_file_name_gives_edition_table_month_and_title(name, want):
    assert m.parse_name(name) == want


def test_a_name_outside_the_pattern_stops_the_run():
    with pytest.raises(SystemExit, match="Population.csv"):
        m.parse_name("Population.csv")


def test_select_by_table_number_and_limit():
    tables = m.parse_listing(PAGE, m.PAGE_URL)
    assert [t["table"] for t in m.select(tables, only={314, 253})] == [253, 314]
    assert len(m.select(tables, limit=2)) == 2
    assert len(m.select(tables)) == 7
    assert [t["table"] for t in m.select(tables, editions={"syb61"})] == [253]


def test_planning_skips_files_whose_manifest_entry_still_matches(tmp_path):
    tables = m.select(m.parse_listing(PAGE, m.PAGE_URL), only={314, 253})
    d61, d68 = tmp_path / "syb61", tmp_path / "syb68"
    d68.mkdir()
    f = d68 / "SYB68_314_202511_Internet Usage.csv"
    f.write_bytes(b"T30,Internet Usage\r\n")
    manifests = {
        "syb68": {"files": {f.name: {"url": CSV + "SYB68_314_202511_Internet%20Usage.csv",
                                      "sha256": m.sha256(f)}}},
        "syb61": {"files": {}},
    }  # fmt: skip
    todo = m.plan(tables, manifests, tmp_path)
    assert [t["table"] for t in todo] == [253]
    f.write_bytes(b"changed")
    assert [t["table"] for t in m.plan(tables, manifests, tmp_path)] == [253, 314]
    assert not d61.exists()


def test_retry_waits_on_429_and_503_only():
    assert m.should_retry(429) and m.should_retry(503)
    assert not m.should_retry(404) and not m.should_retry(403)


def test_annotate_records_what_the_page_states_and_the_encoding():
    t = {t["file"]: t for t in m.parse_listing(PAGE, m.PAGE_URL)}["SYB68_314_202511_Internet Usage.csv"]
    entry = {"url": t["url"], "sha256": "x", "page_updated": "1-Jan-2025"}
    assert m.annotate(entry, t) is True
    assert entry == {
        "url": t["url"], "sha256": "x", "label": "Internet usage", "topic": "Communication",
        "page_updated": "22-Dec-2025", "table": 314, "month": "202511",
        "title": "Internet Usage", "encoding": "windows-1252",
    }  # fmt: skip
    assert m.annotate(entry, t) is False
