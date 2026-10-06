import importlib.util
import shutil
from pathlib import Path

import duckdb
import pytest

HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location(
    "export", HERE.parent / "scripts" / "03_export_parquet.py"
)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

IU = HERE / "fixtures" / "SYB68_314_202511_Internet Usage.csv"
XR = HERE / "fixtures" / "SYB68_130_202511_Exchange Rates.csv"
ITU = "International Telecommunication Union (ITU), Geneva, the ITU database, last accessed March 2025."


def test_the_seven_column_header_gets_plain_names():
    header = ["Region/Country/Area", "", "Year", "Series", "Value", "Footnotes", "Source"]
    assert m.column_names(header) == [
        "area_code", "area", "year", "series", "value", "footnotes", "source",
    ]  # fmt: skip


@pytest.mark.parametrize(
    ("extra", "want"),
    [
        ("Capital City", "capital_city"),
        ("National currency", "national_currency"),
        ("System of trade", "system_of_trade"),
        ("Tourism arrivals series type", "tourism_arrivals_series_type"),
        ("Last Election Date", "last_election_date"),
        ("Major trading partner 1 (% of exports)", "major_trading_partner_1_pct_of_exports"),
    ],
)
def test_the_attribute_column_and_its_footnote_keep_their_names(extra, want):
    header = ["Region/Country/Area", "", "Year", "Series", extra, f"{extra} footnote",
              "Value", "Footnotes", "Source"]  # fmt: skip
    assert m.column_names(header)[4:6] == [want, f"{want}_footnote"]


@pytest.mark.parametrize(
    "header",
    [
        ["Region/Country/Area", "", "Year", "Series", "Value", "Footnotes"],
        ["Country", "", "Year", "Series", "Value", "Footnotes", "Source"],
        ["Region/Country/Area", "", "Year", "Series", "Unit", "Value", "Footnotes", "Source"],
        ["Region/Country/Area", "", "Year", "Series", "A", "B footnote", "Value", "Footnotes", "Source"],
    ],
)
def test_a_header_of_another_shape_stops_the_run(header):
    with pytest.raises(ValueError):
        m.column_names(header)


@pytest.mark.parametrize(
    ("name", "sql"),
    [
        ("area_code", "INTEGER"),
        ("year", "INTEGER"),
        ("value", "DOUBLE"),
        ("area", "VARCHAR"),
        ("series", "VARCHAR"),
        ("footnotes", "VARCHAR"),
        ("source", "VARCHAR"),
        ("national_currency", "VARCHAR"),
        ("last_election_date", "VARCHAR"),
    ],
)
def test_column_type_comes_from_the_name(name, sql):
    assert m.column_type(name) == sql


@pytest.mark.parametrize(
    ("title", "slug"),
    [
        ("Internet Usage", "internet_usage"),
        ("Population, Surface Area and Density", "population_surface_area_and_density"),
        ("Tourist-Visitors Arrival and Expenditure", "tourist_visitors_arrival_and_expenditure"),
    ],
)
def test_table_slug(title, slug):
    assert m.slug(title) == slug


def test_title_row_gives_the_yearbook_table_code_and_title():
    assert m.read_title(IU, "windows-1252") == ("T30", "Internet Usage")
    assert m.read_title(XR, "windows-1252") == ("T16", "Exchange rates")


def _export(tmp_path, src):
    utf8 = tmp_path / "u.csv"
    m.transcode(src, utf8, "windows-1252")
    names = m.column_names(m.read_header(utf8))
    con = duckdb.connect()
    return con.sql(m.select_sql(utf8, names, src.name))


def test_export_types_and_keeps_every_row_in_order(tmp_path):
    rel = _export(tmp_path, IU)
    assert rel.columns == ["area_code", "area", "year", "series", "value", "footnotes", "source"]
    assert [str(t) for t in rel.types] == [
        "INTEGER", "VARCHAR", "INTEGER", "VARCHAR", "DOUBLE", "VARCHAR", "VARCHAR",
    ]  # fmt: skip
    rows = rel.fetchall()
    assert len(rows) == 5
    assert rows[0] == (1, "Total, all countries or areas", 2005,
                       "Percentage of individuals using the internet", 15.6, None, ITU)  # fmt: skip
    assert rows[1][1] == "LDC§"
    assert rows[2][1] == "Côte d’Ivoire" and rows[2][5] == "Estimate."


def test_export_reads_thousands_separators_and_the_attribute_columns(tmp_path):
    rows = _export(tmp_path, XR).fetchall()
    assert rows[0][4:7] == ("E. Caribbean Dollar (XCD)", "East Caribbean Dollar.", 2.7)
    assert rows[1][1] == "Åland Islands" and rows[1][5] is None
    assert rows[2][1] == "Argentina" and rows[2][6] == 1030.5


@pytest.mark.parametrize(
    ("good", "bad", "column"),
    [
        (",15.6,", ",n/a,", "value"),
        (",15.6,", ",1.5.6,", "value"),
        (",15.6,,", ",,,", "value"),
        (",2005,", ",2005a,", "year"),
    ],
)
def test_a_value_that_does_not_fit_its_type_stops_the_export(tmp_path, good, bad, column):
    src = tmp_path / "bad.csv"
    lines = IU.read_bytes().split(b"\r\n")
    lines[2] = lines[2].replace(good.encode(), bad.encode(), 1)
    src.write_bytes(b"\r\n".join(lines))
    with pytest.raises(duckdb.Error, match=f"bad.csv: {column} is not"):
        _export(tmp_path, src).fetchall()


def test_value_regex_accepts_only_plain_or_grouped_numbers():
    import re

    for ok in ("0", "15.6", "-1,084", "1,030.5", "120,771", "-0.3"):
        assert re.fullmatch(m.NUMBER_RE, ok), ok
    for bad in ("1,03", "1,0300", ",100", "1.", ".5", "1e5", "", "1 000"):
        assert not re.fullmatch(m.NUMBER_RE, bad), bad


def test_main_writes_one_parquet_per_table_and_the_lists(tmp_path, monkeypatch):
    raw = tmp_path / "raw" / "syb68"
    raw.mkdir(parents=True)
    # both fixtures come from agencies whose rows are not published (ITU, IMF),
    # so their sources are rewritten to UNSD for this test
    for f in (IU, XR):
        data = f.read_bytes()
        for agency in (b"International Telecommunication Union (ITU)", b"International Monetary Fund (IMF)"):
            data = data.replace(agency, b"United Nations Statistics Division")
        (raw / f.name).write_bytes(data)
    files = {
        IU.name: {"table": 314, "title": "Internet Usage", "label": "Internet usage",
                  "topic": "Communication", "page_updated": "22-Dec-2025", "month": "202511",
                  "encoding": "windows-1252"},
        XR.name: {"table": 130, "title": "Exchange Rates", "label": "Exchange rates",
                  "topic": "Finance", "page_updated": "22-Dec-2025", "month": "202511",
                  "encoding": "windows-1252"},
    }  # fmt: skip
    (raw / "MANIFEST.json").write_text(__import__("json").dumps({"files": files}))
    monkeypatch.setattr(m, "RAW", tmp_path / "raw")
    monkeypatch.setattr(m, "OUT", tmp_path / "parquet")
    monkeypatch.setattr(m, "WORK", tmp_path / "work")
    assert m.main() == 0
    out = tmp_path / "parquet"
    assert sorted(p.relative_to(out).as_posix() for p in out.rglob("*.parquet")) == [
        "sources.parquet", "syb68/130_exchange_rates.parquet",
        "syb68/314_internet_usage.parquet", "tables.parquet",
    ]  # fmt: skip
    con = duckdb.connect()
    t = con.sql(
        f"select edition, table_number, subset, table_code, title, rows, rows_published, sources "
        f"from '{out / 'tables.parquet'}' order by table_number"
    ).fetchall()
    assert t == [
        ("syb68", 130, "syb68.130_exchange_rates", "T16", "Exchange rates", 3, 3, 1),
        ("syb68", 314, "syb68.314_internet_usage", "T30", "Internet Usage", 5, 5, 1),
    ]
    s = con.sql(
        f"select subset, agency, published, rows from '{out / 'sources.parquet'}'"
    ).fetchall()
    assert ("syb68.314_internet_usage", "UNSD", True, 5) in s
    bloom = con.sql(
        "select count(*) filter (where bloom_filter_offset is not null) "
        f"from parquet_metadata('{out / 'syb68' / '314_internet_usage.parquet'}')"
    ).fetchone()[0]
    assert bloom == 0

COMTRADE = ("United Nations Statistics Division, New York, Commodity Trade Statistics Database "
            "(UN COMTRADE), last accessed June 2025.")  # fmt: skip
MATERNAL = ("World Health Organization (WHO), the United Nations Children's Fund (UNICEF), the "
            "United Nations Population Fund (UNFPA), the World Bank and the United Nations "
            "Population Division, Trends in Maternal Mortality")  # fmt: skip
WPP = ("United Nations Population Division, New York, World Population Prospects: The 2024 "
       "Revision, last accessed June 2025.")  # fmt: skip
AMA = ("United Nations Statistics Division, New York, National Accounts Statistics: Analysis of "
       "Main Aggregates (AMA) database, last accessed April 2025.")  # fmt: skip


@pytest.mark.parametrize(
    ("source", "agency", "published"),
    [
        (WPP, "UN Population Division", True),
        (AMA, "UNSD", True),
        (COMTRADE, "UN Comtrade", True),
        (ITU, "ITU", False),
        (MATERNAL, "WHO", False),
        ("World Health Organisation (WHO), Geneva, WHO Global Health Workforce", "WHO", False),
        ("International Monetary Fund (IMF), Washington, D.C., Balance of Payment", "IMF", False),
        ("Food and Agriculture Organization of the United Nations (FAO), Rome", "FAO", True),
    ],
)
def test_source_status_names_the_agency_and_whether_its_rows_are_published(
    source, agency, published
):
    got = m.source_status(source)
    assert (got[0], got[1]) == (agency, published)
    assert got[2]


@pytest.mark.parametrize("source", [None, "", "Some Agency Nobody Checked, Geneva"])
def test_a_source_whose_terms_were_not_checked_is_not_published(source):
    agency, published, reason = m.source_status(source)
    assert agency == "unchecked" and published is False and "not checked" in reason


def test_main_leaves_out_the_rows_and_tables_of_excluded_sources(tmp_path, monkeypatch):
    raw = tmp_path / "raw" / "syb68"
    raw.mkdir(parents=True)
    shutil.copy(IU, raw / IU.name)
    mixed = raw / "SYB68_246_202511_Mixed.csv"
    lines = XR.read_bytes().split(b"\r\n")
    lines[2] = lines[2].replace(b'"International Monetary Fund', b'"United Nations Population Division')
    assert b"United Nations Population Division" in lines[2]
    mixed.write_bytes(b"\r\n".join(lines))
    files = {
        IU.name: {"table": 314, "title": "Internet Usage", "encoding": "windows-1252"},
        mixed.name: {"table": 246, "title": "Mixed", "encoding": "windows-1252"},
    }
    (raw / "MANIFEST.json").write_text(__import__("json").dumps({"files": files}))
    monkeypatch.setattr(m, "RAW", tmp_path / "raw")
    monkeypatch.setattr(m, "OUT", tmp_path / "parquet")
    monkeypatch.setattr(m, "WORK", tmp_path / "work")
    assert m.main() == 0
    out = tmp_path / "parquet"
    assert not (out / "syb68" / "314_internet_usage.parquet").exists()
    con = duckdb.connect()
    t = con.sql(
        f"select table_number, parquet, rows, rows_published, rows_excluded "
        f"from '{out / 'tables.parquet'}' order by table_number"
    ).fetchall()
    assert t == [(246, "parquet/syb68/246_mixed.parquet", 3, 1, 2),
                 (314, None, 5, 0, 5)]  # fmt: skip
    kept = con.sql(f"select source from '{out / 'syb68' / '246_mixed.parquet'}'").fetchall()
    assert [m.source_status(s)[1] for (s,) in kept] == [True]
    s = con.sql(
        f"select agency, published, rows from '{out / 'sources.parquet'}' "
        "where table_number = 314"
    ).fetchall()
    assert s == [("ITU", False, 5)]


def test_comtrade_rows_stay_under_the_limit_its_faq_allows(monkeypatch):
    monkeypatch.setattr(m, "COMTRADE_LIMIT", 10)
    sources = [("syb68", 123, "s", COMTRADE, *m.source_status(COMTRADE), 6),
               ("syb68", 330, "s", COMTRADE, *m.source_status(COMTRADE), 4)]  # fmt: skip
    with pytest.raises(SystemExit, match="UN Comtrade"):
        m.check_comtrade_limit(sources)
    m.check_comtrade_limit(sources[:1])
