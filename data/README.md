---
license: other
license_name: undata-terms-of-use-and-originating-agency-terms
license_link: https://data.un.org/Host.aspx?Content=UNdataUse
language:
- en
task_categories:
- tabular-regression
- time-series-forecasting
tags:
- united-nations
- unsd
- statistical-yearbook
- undata
- official-statistics
- country-statistics
size_categories:
- 100K<n<1M
configs:
- config_name: 'tables'
  data_files: parquet/tables.parquet
  default: true
- config_name: 'sources'
  data_files: parquet/sources.parquet
- config_name: 'syb68.1_population_surface_area_and_density'
  data_files: parquet/syb68/1_population_surface_area_and_density.parquet
- config_name: 'syb68.12_agricultural_index'
  data_files: parquet/syb68/12_agricultural_index.parquet
- config_name: 'syb68.123_total_imports_exports_and_balance_of_trade'
  data_files: parquet/syb68/123_total_imports_exports_and_balance_of_trade.parquet
- config_name: 'syb68.128_consumer_price_index'
  data_files: parquet/syb68/128_consumer_price_index.parquet
- config_name: 'syb68.145_land'
  data_files: parquet/syb68/145_land.parquet
- config_name: 'syb68.153_gross_value_added_by_economic_activity'
  data_files: parquet/syb68/153_gross_value_added_by_economic_activity.parquet
- config_name: 'syb68.200_employment'
  data_files: parquet/syb68/200_employment.parquet
- config_name: 'syb68.223_net_disbursements_from_official_oda_from_donors'
  data_files: parquet/syb68/223_net_disbursements_from_official_oda_from_donors.parquet
- config_name: 'syb68.226_net_disbursements_from_official_oda_to_recipients'
  data_files: parquet/syb68/226_net_disbursements_from_official_oda_to_recipients.parquet
- config_name: 'syb68.230_gdp_and_gdp_per_capita'
  data_files: parquet/syb68/230_gdp_and_gdp_per_capita.parquet
- config_name: 'syb68.245_public_expenditure_on_education_and_access_to_computers'
  data_files: parquet/syb68/245_public_expenditure_on_education_and_access_to_computers.parquet
- config_name: 'syb68.246_population_growth_fertility_and_mortality_indicators'
  data_files: parquet/syb68/246_population_growth_fertility_and_mortality_indicators.parquet
- config_name: 'syb68.263_production_trade_and_supply_of_energy'
  data_files: parquet/syb68/263_production_trade_and_supply_of_energy.parquet
- config_name: 'syb68.285_research_and_development_expenditure_and_staff'
  data_files: parquet/syb68/285_research_and_development_expenditure_and_staff.parquet
- config_name: 'syb68.309_education'
  data_files: parquet/syb68/309_education.parquet
- config_name: 'syb68.310_carbon_dioxide_emission_estimates'
  data_files: parquet/syb68/310_carbon_dioxide_emission_estimates.parquet
- config_name: 'syb68.319_ratio_of_girls_to_boys_in_education'
  data_files: parquet/syb68/319_ratio_of_girls_to_boys_in_education.parquet
- config_name: 'syb68.323_teaching_staff_in_education'
  data_files: parquet/syb68/323_teaching_staff_in_education.parquet
- config_name: 'syb68.327_international_migrants_and_refugees'
  data_files: parquet/syb68/327_international_migrants_and_refugees.parquet
- config_name: 'syb68.329_labour_force_and_unemployment'
  data_files: parquet/syb68/329_labour_force_and_unemployment.parquet
- config_name: 'syb68.330_major_trading_partners'
  data_files: parquet/syb68/330_major_trading_partners.parquet
- config_name: 'syb61.253_population_growth_rates_in_urban_areas_and_capital_cities'
  data_files: parquet/syb61/253_population_growth_rates_in_urban_areas_and_capital_cities.parquet
---

# un-statistical-yearbook

The tables of the United Nations Statistical Yearbook as CSV files, as the
United Nations Statistics Division (UNSD) publishes them on UNdata
(https://data.un.org/Default.aspx, under "Popular statistical tables,
country (area) and regional profiles"). Each table gathers one theme
(population, national accounts, education, trade, energy, environment,
internet use, development assistance and others) for countries, areas and
regional aggregates, over several years. UNdata describes them as "produced
as part of the UN Statistical Yearbook publication; but unlike the Yearbook
which is published once a year, these 'live' tables are released as soon as
possible after new data becomes available."

UNSD compiles the tables from other agencies. Every row carries a `source`
column naming where its value comes from (the FAO for agriculture, the ILO
for labour, UNESCO for education, and so on). UNdata's terms of use allow
free copying and redistribution with UNdata cited, but they do not speak for
those agencies, so this dataset publishes a row only when its originating
agency's own terms allow redistribution, commercial use included. Rows from
the WHO, ITU, IMF, IUCN, UNEP-WCMC, UNODC, UN Tourism, WIPO and the IPU are
left out; Licence below gives each agency's terms and the reason.

Of the 147,026 records in the 33 CSVs, 105,902 are published, in 22
tables; 11 tables come entirely from agencies whose rows are left out and
are not here. Each published table is one Parquet file, typed and in
UTF-8. The CSVs of the 20 tables published whole are here unchanged; the
CSVs of tables with any row left out are not uploaded. Two lists cover all
33 tables: `tables` (one row per table, with its published and excluded
row counts) and `sources` (rows per Source value per table, with the
agency, whether its rows are published and why).

## Editions

The file names carry the yearbook edition: `SYB68_314_202511_Internet
Usage.csv` is table 314 of the 68th edition (SYB68), dated November 2025
(`202511`). Each edition is a separate publication and has its own
directory; a new edition will be added beside the others, not over them.

| edition | files | rows | bytes | Last-Modified | "Updated" on the page |
|---|---:|---:|---:|---|---|
| `syb68` | 32 | 142,861 | 33,575,186 | 2026-02-02, and 2026-02-24 for table 1 | 22-Dec-2025, and 2-Mar-2026 for tables 1 and 246 |
| `syb61` | 1 | 4,165 | 974,684 | 2018-08-31 | none stated |

The page links 32 tables of SYB68 and, for "Population in the capital city,
urban and rural areas", the table of SYB61 (2018), which has had no newer
edition. Older editions of the other tables may still be on the server
(for example `SYB67_314_202411_Internet Usage.csv`), but the page does not
link them and the server refuses directory listings, so their names could
only be guessed; they are not included. The files were fetched on
2026-10-06.

## Tables

One subset per published table and edition, named `<edition>.<table
number>_<title>`. A table with 0 published rows has no subset; "raw CSV"
says whether its CSV is uploaded (only when every row is published).
The table number is UNdata's, from the file name (internet use is 314 in
SYB67 as in SYB68). The yearbook's own table code (`T30`) is in the first row of each
CSV and in `tables`; it is renumbered between editions (T03 is a different
table in SYB61 and SYB68).

| subset | yearbook code | title (first row of the CSV) | topic on the page | rows | published | raw CSV |
|---|---|---|---|---:|---:|---|
| `syb68.1_population_surface_area_and_density` | T02 | Population, density and surface area | Population | 7,727 | 7,727 | included |
| `syb68.12_agricultural_index` | T20 | Agricultural production indices | Price and production indices | 3,564 | 3,564 | included |
| `syb68.123_total_imports_exports_and_balance_of_trade` | T21 | Total imports, exports and balance of trade | International merchandise trade | 4,995 | 4,995 | included |
| `syb68.125_balance_of_payments` | T15 | Balance of payments summary | Finance | 3,305 | 0 | withheld |
| `syb68.128_consumer_price_index` | T19 | Consumer Price Index | Price and production indices | 2,045 | 2,045 | included |
| `syb68.130_exchange_rates` | T16 | Exchange rates | Finance | 3,516 | 0 | withheld |
| `syb68.145_land` | T24 | Land | Environment | 6,297 | 5,283 | withheld |
| `syb68.153_gross_value_added_by_economic_activity` | T14 | Gross value added by kind of economic activity | National accounts | 4,432 | 4,432 | included |
| `syb68.154_health_personnel` | T10 | Health personnel | Nutrition and health | 6,260 | 0 | withheld |
| `syb68.176_tourist_visitors_arrival_and_expenditure` | T31 | Tourist/visitor arrivals and tourism expenditure | Tourism and transport | 2,154 | 0 | withheld |
| `syb68.200_employment` | T18 | Employment by economic activity | Labour market | 8,037 | 8,037 | included |
| `syb68.223_net_disbursements_from_official_oda_from_donors` | T33 | Net disbursements of official development assistance from donors | Development Assistance | 632 | 632 | included |
| `syb68.226_net_disbursements_from_official_oda_to_recipients` | T32 | Net disbursements of official development assistance to recipients | Development Assistance | 5,199 | 5,199 | included |
| `syb68.230_gdp_and_gdp_per_capita` | T13 | Gross domestic product and gross domestic product per capita | National accounts | 6,768 | 6,768 | included |
| `syb68.245_public_expenditure_on_education_and_access_to_computers` | T09 | Public expenditure on education (as of 2021) | Education | 2,365 | 2,365 | included |
| `syb68.246_population_growth_fertility_and_mortality_indicators` | T03 | Population growth and indicators of fertility and mortality | Population | 7,161 | 6,504 | withheld |
| `syb68.263_production_trade_and_supply_of_energy` | T23 | Production, trade and supply of energy | Energy | 8,700 | 8,700 | included |
| `syb68.264_patents` | T29 | Patents | Science and technology | 1,973 | 0 | withheld |
| `syb68.285_research_and_development_expenditure_and_staff` | T28 | Research and development (R&D) expenditure and researchers (full time equivalent) | Science and technology | 1,039 | 1,039 | included |
| `syb68.309_education` | T07 | Enrollment in primary, lower secondary and upper secondary education levels | Education | 7,934 | 7,934 | included |
| `syb68.310_carbon_dioxide_emission_estimates` | T26 | CO2 emission estimates | Environment | 3,488 | 3,488 | included |
| `syb68.313_threatened_species` | T25 | Threatened species | Environment | 6,916 | 0 | withheld |
| `syb68.314_internet_usage` | T30 | Internet Usage | Communication | 1,520 | 0 | withheld |
| `syb68.315_water_and_sanitation_services` | T27 | Water supply and sanitation services | Environment | 3,519 | 0 | withheld |
| `syb68.317_seats_held_by_women_in_parliament` | T05 | Proportion of seats held by women in national parliament | Gender | 1,952 | 0 | withheld |
| `syb68.319_ratio_of_girls_to_boys_in_education` | T06 | Ratio of girls to boys in primary, lower secondary and upper secondary education | Gender | 3,347 | 3,347 | included |
| `syb68.323_teaching_staff_in_education` | T08 | Teaching staff at the primary, lower secondary and upper secondary levels | Education | 3,685 | 3,685 | included |
| `syb68.325_expenditure_on_health` | T11 | Expenditure on health | Nutrition and health | 2,292 | 0 | withheld |
| `syb68.327_international_migrants_and_refugees` | T04 | International migrants and refugees | Population | 6,966 | 6,966 | included |
| `syb68.328_intentional_homicides_and_other_crimes` | T12 | Intentional homicides and other crimes | Crime | 6,046 | 0 | withheld |
| `syb68.329_labour_force_and_unemployment` | T17 | Labour force participation and unemployment | Labour market | 5,486 | 5,486 | included |
| `syb68.330_major_trading_partners` | T22 | Major trading partners | International merchandise trade | 3,541 | 3,541 | included |
| `syb61.253_population_growth_rates_in_urban_areas_and_capital_cities` | T03 | Population and rates of growth in urban areas and capital cities | Population | 4,165 | 4,165 | included |

`tables` has, per table: `edition`, `table_number`, `subset`, `parquet`
(path), `raw` (path of the CSV), `table_code` and `title` (the CSV's first
row), `page_label` and `topic` (as the UNdata page lists the table),
`edition_month` (the `yyyymm` of the file name, NULL for SYB61),
`page_updated` (the page's "Updated" date as written, NULL when the page
states none), `rows` (records in the CSV), `rows_published` and
`rows_excluded`, `columns` and `sources` (the number of distinct Source
values). `parquet` is NULL for a table with no published rows.

`sources` has `edition`, `table_number`, `subset`, `source` (the Source
text exactly as in the CSV), `agency`, `published` (whether its rows are
in the table's Parquet), `reason` (the agency's terms in a sentence, with
their URL) and `rows`.

## Files and columns

Every CSV has the same layout: the yearbook table code and title in the
first row (`T30,Internet Usage,,,,,`), a header in the second, then one
record per row. In the Parquet, the header becomes:

| CSV header | column | type |
|---|---|---|
| `Region/Country/Area` | `area_code` | INTEGER |
| (no name) | `area` | VARCHAR |
| `Year` | `year` | INTEGER |
| `Series` | `series` | VARCHAR |
| `Value` | `value` | DOUBLE |
| `Footnotes` | `footnotes` | VARCHAR |
| `Source` | `source` | VARCHAR |

Six tables have one attribute column and its footnote between `Series`
and `Value`, named after the header in snake case (`%` as `pct`):

| subset | CSV header | columns |
|---|---|---|
| `syb68.123_total_imports_exports_and_balance_of_trade` | `System of trade`, `System of trade footnote` | `system_of_trade`, `system_of_trade_footnote` |
| `syb68.130_exchange_rates` | `National currency`, ... footnote | `national_currency`, `national_currency_footnote` |
| `syb68.176_tourist_visitors_arrival_and_expenditure` | `Tourism arrivals series type`, ... footnote | `tourism_arrivals_series_type`, `tourism_arrivals_series_type_footnote` |
| `syb68.317_seats_held_by_women_in_parliament` | `Last Election Date`, ... footnote | `last_election_date`, `last_election_date_footnote` |
| `syb68.330_major_trading_partners` | `Major trading partner 1 (% of exports)`, ... footnote | `major_trading_partner_1_pct_of_exports`, `major_trading_partner_1_pct_of_exports_footnote` |
| `syb61.253_population_growth_rates_in_urban_areas_and_capital_cities` | `Capital City`, ... footnote | `capital_city`, `capital_city_footnote` |

Tables 130, 176 and 317 are not published (IMF, UN Tourism and IPU rows);
they are listed because `tables` still describes them. The columns are
text, as published: `system_of_trade` is a code (`G`, `S`),
`tourism_arrivals_series_type` a code (`TF`, `VF`, `TCE`, ...),
`last_election_date` a `yyyy-mm` string. In
`syb68.330_major_trading_partners` the column holds the partner named by
each row's `series` (partner 1, 2 or 3, of exports or imports), although
its header names only the first.

The type comes from the column name, never from inference. Each value was
checked with a regular expression before the cast (`[0-9]+` for
`area_code`, `[0-9]{4}` for `year`, `-?([0-9]+|[0-9]{1,3}(,[0-9]{3})+)(\.[0-9]+)?`
for `value`), and a value that did not fit, or was empty, would have
stopped the build; none did. `value` is written with thousands separators
in the CSV (`"1,030.5"`); they were removed before the cast. An empty text
cell is NULL. Rows keep the order of the CSV.

```sql
-- DuckDB, straight off the Hub: GDP and GDP per capita of Japan, SYB68
SELECT year, series, value, footnotes
FROM 'hf://datasets/yuiseki/un-statistical-yearbook/parquet/syb68/230_gdp_and_gdp_per_capita.parquet'
WHERE area_code = 392
ORDER BY series, year;

-- which agencies a table's values come from, and which are published
SELECT subset, agency, published, rows, reason
FROM 'hf://datasets/yuiseki/un-statistical-yearbook/parquet/sources.parquet'
ORDER BY subset, rows DESC;
```

## Sources per table

The Source value of every row, counted per table, with the agency it was
matched to and whether its rows are published. The text is as written in
the CSV; the agency is named at its start.

| subset | rows | agency | published | Source (as written in the CSV) |
|---|---:|---|---|---|
| `syb68.1_population_surface_area_and_density` | 4,252 (55%) | UN Population Division | yes | United Nations Population Division, New York, World Population Prospects: The 2024 Revision, last accessed June 2025. |
| `syb68.1_population_surface_area_and_density` | 3,192 (41%) | UN Population Division | yes | United Nations Population Division, New York, World Population Prospects: The 2024 Revision; supplemented by data from the United Nations Statistics Division, New York, Demographic Yearbook 2023, last accessed June 2025. |
| `syb68.1_population_surface_area_and_density` | 254 (3%) | UNSD | yes | United Nations Statistics Division, New York, "Demographic Yearbook 2023" and the demographic statistics database, last accessed June 2025. |
| `syb68.1_population_surface_area_and_density` | 29 (0%) | UN Population Division | yes | United Nations Population Division, New York, World Population Prospects: The 2024 Revision - interim update for Togo, last accessed February 2026. |
| `syb68.12_agricultural_index` | 3,564 (100%) | FAO | yes | Food and Agriculture Organization of the United Nations (FAO), Rome, FAOSTAT database, last accessed May 2025. |
| `syb68.123_total_imports_exports_and_balance_of_trade` | 4,995 (100%) | UN Comtrade | yes | United Nations Statistics Division, New York, Commodity Trade Statistics Database (UN COMTRADE), last accessed June 2025. |
| `syb68.125_balance_of_payments` | 3,305 (100%) | IMF | no | International Monetary Fund (IMF), Washington, D.C., Balance of Payment (BOP) Statistics database, last accessed June 2025. |
| `syb68.128_consumer_price_index` | 2,045 (100%) | UNSD | yes | United Nations Statistics Division (UNSD), New York, Monthly Bulletin of Statistics (MBS), last accessed June 2025. |
| `syb68.130_exchange_rates` | 3,516 (100%) | IMF | no | International Monetary Fund (IMF), Washington, D.C., the database on International Financial Statistics supplemented by operational rates of exchange for United Nations programmes, last accessed June 2025. |
| `syb68.145_land` | 5,283 (84%) | FAO | yes | Food and Agriculture Organization of the United Nations (FAO), Rome, FAOSTAT data last accessed December 2024. |
| `syb68.145_land` | 1,014 (16%) | UNEP-WCMC | no | United Nations Environment Programme (UNEP) World Conservation Monitoring Centre (WCMC) and World Conservation Union (IUCN) and BirdLife International, Cambridge, Sustainable Development Goals database, March 2025. |
| `syb68.153_gross_value_added_by_economic_activity` | 4,432 (100%) | UNSD | yes | United Nations Statistics Division, New York, National Accounts Statistics: Analysis of Main Aggregates (AMA) database, last accessed April 2025. |
| `syb68.154_health_personnel` | 6,260 (100%) | WHO | no | World Health Organisation (WHO), Geneva, WHO Global Health Workforce statistics database, last accessed April 2025. |
| `syb68.176_tourist_visitors_arrival_and_expenditure` | 2,154 (100%) | UN Tourism | no | World Tourism Organization (UNWTO), Madrid, the UNWTO Statistics Database, last accessed December 2023. |
| `syb68.200_employment` | 8,037 (100%) | ILO | yes | International Labour Organization (ILO), Geneva, Key Indicators of the Labour Market (KILM 9th edition) and the ILOSTAT database, last accessed April 2025. |
| `syb68.223_net_disbursements_from_official_oda_from_donors` | 632 (100%) | OECD | yes | Organisation for Economic Co-operation and Development (OECD), Paris, the OECD Development Assistance Committee (DAC) database, last accessed July 2025. |
| `syb68.226_net_disbursements_from_official_oda_to_recipients` | 5,199 (100%) | OECD | yes | Organisation for Economic Co-operation and Development (OECD), Paris, the OECD Development Assistance Committee (DAC) database, last accessed July 2025. |
| `syb68.230_gdp_and_gdp_per_capita` | 6,768 (100%) | UNSD | yes | United Nations Statistics Division, New York, National Accounts Statistics: Analysis of Main Aggregates (AMA) database, last accessed April 2025. |
| `syb68.245_public_expenditure_on_education_and_access_to_computers` | 2,365 (100%) | UIS | yes | United Nations Educational, Scientific and Cultural Organization (UNESCO), Montreal, the UNESCO Institute for Statistics (UIS) statistics database, last accessed April 2025. |
| `syb68.246_population_growth_fertility_and_mortality_indicators` | 4,336 (61%) | UN Population Division | yes | United Nations Population Division, New York, World Population Prospects: The 2024 Revision; supplemented by data from the United Nations Statistics Division, New York, Demographic Yearbook 2023, last accessed June 2025. |
| `syb68.246_population_growth_fertility_and_mortality_indicators` | 2,164 (30%) | UN Population Division | yes | United Nations Population Division, New York, World Population Prospects: The 2024 Revision, last accessed June 2025. |
| `syb68.246_population_growth_fertility_and_mortality_indicators` | 657 (9%) | WHO | no | World Health Organization (WHO), the United Nations Children's Fund (UNICEF), the United Nations Population Fund (UNFPA), the World Bank and the United Nations Population Division, "Trends in Maternal Mortality 2000 - 2020." |
| `syb68.246_population_growth_fertility_and_mortality_indicators` | 4 (0%) | UN Population Division | yes | United Nations Population Division, New York, World Population Prospects: The 2024 Revision  - interim update, last accessed February 2026. |
| `syb68.263_production_trade_and_supply_of_energy` | 8,700 (100%) | UNSD | yes | United Nations Statistics Division, New York, Energy Statistics Yearbook 2022, last accessed April 2025. |
| `syb68.264_patents` | 1,973 (100%) | WIPO | no | World Intellectual Property Organization (WIPO), Geneva, WIPO statistics database, last accessed May 2025. |
| `syb68.285_research_and_development_expenditure_and_staff` | 1,039 (100%) | UIS | yes | United Nations Educational, Scientific and Cultural Organization (UNESCO), Montreal, the UNESCO Institute for Statistics (UIS) statistics database, last accessed April 2025. |
| `syb68.309_education` | 7,934 (100%) | UIS | yes | United Nations Educational, Scientific and Cultural Organization (UNESCO), Montreal, the UNESCO Institute for Statistics (UIS) statistics database, last accessed April 2025. |
| `syb68.310_carbon_dioxide_emission_estimates` | 3,488 (100%) | UNSD | yes | United Nations Statistics Division, New York, Energy Statistics Section, last accessed Feb. 2025. |
| `syb68.313_threatened_species` | 6,916 (100%) | IUCN | no | World Conservation Union (IUCN), Gland and Cambridge, IUCN Red List of Threatened Species publication, last accessed June 2025. |
| `syb68.314_internet_usage` | 1,520 (100%) | ITU | no | International Telecommunication Union (ITU), Geneva, the ITU database, last accessed March 2025. |
| `syb68.315_water_and_sanitation_services` | 3,519 (100%) | WHO | no | World Health Organization (WHO) and United Nations Children's Fund (UNICEF), Geneva and New York, the WHO/UNICEF Joint Monitoring Programme for the Water and Sanitation database, last accessed July 2025. |
| `syb68.317_seats_held_by_women_in_parliament` | 1,952 (100%) | IPU | no | Inter-Parliamentary Union (IPU), Geneva, the database on "Women in National Parliament", last accessed March 2025. |
| `syb68.319_ratio_of_girls_to_boys_in_education` | 3,347 (100%) | UIS | yes | United Nations Educational, Scientific and Cultural Organization (UNESCO), Montreal, the UNESCO Institute for Statistics (UIS) statistics database, last accessed April 2025. |
| `syb68.323_teaching_staff_in_education` | 3,685 (100%) | UIS | yes | United Nations Educational, Scientific and Cultural Organization (UNESCO), Montreal, the UNESCO Institute for Statistics (UIS) statistics database, last accessed April 2025. |
| `syb68.325_expenditure_on_health` | 2,292 (100%) | WHO | no | World Health Organization (WHO), Geneva, WHO Global Health Expenditure database, last accessed May 2025. |
| `syb68.327_international_migrants_and_refugees` | 4,200 (60%) | UN Population Division | yes | United Nations Population Division, New York, International migrant stock: The 2024 Revision, last accessed April 2025. |
| `syb68.327_international_migrants_and_refugees` | 2,766 (40%) | UNHCR | yes | United Nations High Commissioner for Refugees (UNHCR), Geneva, UNHCR Population Statistics Database, last accessed May 2025. |
| `syb68.328_intentional_homicides_and_other_crimes` | 6,046 (100%) | UNODC | no | United Nations Office on Drugs and Crime (UNODC), Vienna, UNODC Statistics database, last accessed May 2025. |
| `syb68.329_labour_force_and_unemployment` | 5,486 (100%) | ILO | yes | International Labour Organization (ILO), Geneva, Key Indicators of the Labour Market (KILM 9th edition) and the ILOSTAT database, last accessed April 2025. |
| `syb68.330_major_trading_partners` | 3,541 (100%) | UN Comtrade | yes | United Nations Statistics Division, New York, Commodity Trade Statistics Database (UN COMTRADE), last accessed June 2025. |
| `syb61.253_population_growth_rates_in_urban_areas_and_capital_cities` | 4,165 (100%) | UN Population Division | yes | United Nations Population Division, New York, World Urbanization Prospects: The 2018 Revision, last accessed May 2018. |

## Things to know

- `area_code` is the M49 code (392 Japan, 1 "Total, all countries or
  areas", 2 Africa, 199 least developed countries, 722 small island
  developing States), and the rows mix countries, areas and aggregates.
  Some aggregate names carry a mark from the source (`LDC§`); they are kept
  as published. `0` is "Total" in the donor table.
- `series` names the measure and its unit ("Percentage of individuals using
  the internet"); a table holds several series. Filter on it before
  comparing values.
- `footnotes` is filled in 43,395 of the 105,902 published rows. Read it: it says
  when a value is an estimate, covers a different population or period, or
  breaks the series.
- Years are not continuous. Most tables give selected years (for example
  1995, 2005, 2010, 2015 and the two or three latest; table 330 only 2015,
  2020 and 2024). Tables 200, 245, 285, 309, 323 and 329 have 15
  to 25 distinct years, which differ from one area to the next. Use
  `tables` and a `group by year` before assuming a year is there.
- Values are those UNSD took from each source on the date the Source text
  states ("last accessed June 2025"). The source agency may have revised
  them since; for current figures go to the agency.
- The SYB61 table is from 2018 (World Urbanization Prospects 2018).
- The CSVs are Windows-1252, not UTF-8 or Latin-1 (curly quotes such as
  "Côte d’Ivoire"). The Parquet holds the text as UTF-8; the raw files are
  unchanged.

## Checked before upload

`scripts/02_verify.py` in the source repository checks, with Python's csv
module reading each CSV in Windows-1252 and DuckDB reading the Parquet:

- every raw file has the size and sha256 in its edition's `MANIFEST.json`
- every CSV decodes strictly, and every record has as many cells as its
  header (147,026 records in 33 files)
- every table's Parquet has as many rows as its CSV has records whose
  Source is published, and a table with none has no Parquet; the column
  names above in order, each of the type its name gives
- every cell equals the CSV's published records', row by row: text as text (empty as NULL),
  `area_code` and `year` as Python's int reads them, `value` as Python's
  float reads it once the thousands separators are removed
- `tables` gives each table's record count and published record count,
  and `sources` each table's Source counts as counted in the CSV, with
  the agency and decision the export's rule gives
- a DuckDB with extension autoloading turned off opens every file, and no
  row group has a bloom filter

## Licence

UNdata, Terms and Conditions of use
(https://data.un.org/Host.aspx?Content=UNdataUse, read on 2026-10-06):

> Terms of Use
>
> All data and metadata provided on UNdata’s website are available free of
> charge and may be copied freely, duplicated and further distributed
> provided that UNdata is cited as the reference.

> Disclaimers
>
> The data and metadata presented on UNdata are supplied as contained in
> the source database without any addition, subtraction, amendment, or
> modification by the United Nations Statistics Division.

> Information about the quality or limitations of the data and metadata
> should be obtained from the organization responsible for the source
> database.

What this does and does not say:

- Copying and redistribution are allowed, on the condition that UNdata is
  cited.
- Commercial use is not mentioned: the terms neither allow nor forbid it.
- No licence name (such as CC BY) is given, and nothing is said about
  modification or derived works.
- The terms speak for UNdata's website as a whole, not table by table, and
  do not mention the rights of the agencies the values come from.

So each row is also read under the terms of the agency its `source`
names, and published only when those terms allow redistribution,
commercial use included. The agencies, read on 2026-10-06 (not legal
advice):

| agency | published | tables | rows | reason (terms read on 2026-10-06) |
|---|---|---|---:|---|
| UNSD | yes | 1, 128, 153, 230, 263, 310 | 25,687 | UNSD's own data under the UNdata terms of use |
| UN Population Division | yes | 1, 246, 253, 327 | 22,342 | World Population and Urbanization Prospects are CC BY 3.0 IGO |
| UIS | yes | 245, 285, 309, 319, 323 | 18,370 | UIS data are CC BY-SA 4.0 (share-alike); https://databrowser.uis.unesco.org/terms-and-conditions |
| ILO | yes | 200, 329 | 13,523 | ILOSTAT is CC BY 4.0 |
| FAO | yes | 12, 145 | 8,847 | FAOSTAT is CC BY 4.0 |
| UN Comtrade | yes | 123, 330 | 8,536 | UN Comtrade lets a database of fewer than 100,000 records in total be re-disseminated, commercially too, without a distribution licence; https://uncomtrade.org/docs/faqs-on-use-and-re-dissemination/ |
| OECD | yes | 223, 226 | 5,831 | OECD terms allow reuse, including commercial, with attribution |
| UNHCR | yes | 327 | 2,766 | UNHCR population statistics are CC BY 4.0 |
| WHO | no | 154, 246, 315, 325 | 12,728 | WHO datasets are licensed for public health purposes only, and any other alteration needs WHO's prior written authorization; https://www.who.int/about/policies/publishing/data-policy/terms-and-conditions |
| IUCN | no | 313 | 6,916 | The IUCN Red List needs prior written permission for commercial use and for republishing or redistributing its data, derived works included; https://www.iucnredlist.org/terms/terms-of-use |
| IMF | no | 125, 130 | 6,821 | IMF data need permission for commercial reuse and for re-publishing a substantial amount; https://www.imf.org/en/about/copyright-and-terms |
| UNODC | no | 328 | 6,046 | The UNODC data portal points to the UN terms of use: personal, non-commercial use without any right to redistribute; https://www.un.org/en/about-us/copyright |
| UN Tourism | no | 176 | 2,154 | UN Tourism content is for personal, non-commercial use, without any right to redistribute it or create derivative works; https://www.untourism.int/copyright |
| WIPO | no | 264 | 1,973 | WIPO's statistics terms forbid republishing or commercially re-selling its statistical datasets; https://www.wipo.int/en/web/ip-statistics/about |
| IPU | no | 317 | 1,952 | IPU Parline data are CC BY-NC-SA 4.0 (non-commercial); https://www.ipu.org/terms-use |
| ITU | no | 314 | 1,520 | ITU content is for personal, educational or non-commercial use; distributing it or any commercial use needs ITU's prior written permission; https://www.itu.int/en/about/Pages/terms-of-use.aspx |
| UNEP-WCMC | no | 145 | 1,014 | The WDPA and the Key Biodiversity Areas data forbid commercial use of derived works, and KBA needs written permission to redistribute them; https://www.protectedplanet.net/en/legal https://www.keybiodiversityareas.org/termsofservice |

Notes:

- UIS rows (education and R&D, tables 245, 285, 309, 319 and 323) are
  CC BY-SA 4.0: share-alike applies to those tables and what you derive
  from them.
- UN Comtrade's FAQ allows a database of fewer than 100,000 Comtrade
  records in total to be re-disseminated, commercially too, without a
  distribution licence. This dataset holds 8,536; the build stops if the
  published Comtrade rows ever reach 100,000.
- The World Population Prospects and World Urbanization Prospects are
  CC BY 3.0 IGO; FAOSTAT, ILOSTAT and UNHCR's statistics CC BY 4.0; the
  OECD's terms allow reuse with attribution. UNSD's own data are under the
  UNdata terms above.
- Rows of the agencies marked "no" are left out of the Parquet, and the
  CSVs of tables with any such row are not uploaded. `sources` keeps the
  Source text, agency, row count and reason for every one of them, so what
  was left out stays visible.

This dataset is not made or endorsed by the United Nations. What was
changed: each CSV was decoded from Windows-1252, its title row moved to
`tables`, its columns renamed and typed as above (thousands separators
removed from `value`), the rows of the agencies above that are not
published left out, and written as Parquet; no value was changed. The
uploaded raw files are unchanged. `LICENSE` beside this file says the same.

## Citation

As the terms require, cite UNdata, for example:

> United Nations Statistics Division, UNdata, Statistical Yearbook tables
> (edition SYB68, 2025), https://data.un.org/, accessed 2026-10-06.

and, for the values of a table, the source named in its `source` column
(for UIS rows, as CC BY-SA 4.0 asks: the UNESCO Institute for Statistics
and the licence).
