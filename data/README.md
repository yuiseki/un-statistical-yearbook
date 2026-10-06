---
license: other
license_name: undata-terms-of-use
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
- config_name: 'syb68.125_balance_of_payments'
  data_files: parquet/syb68/125_balance_of_payments.parquet
- config_name: 'syb68.128_consumer_price_index'
  data_files: parquet/syb68/128_consumer_price_index.parquet
- config_name: 'syb68.130_exchange_rates'
  data_files: parquet/syb68/130_exchange_rates.parquet
- config_name: 'syb68.145_land'
  data_files: parquet/syb68/145_land.parquet
- config_name: 'syb68.153_gross_value_added_by_economic_activity'
  data_files: parquet/syb68/153_gross_value_added_by_economic_activity.parquet
- config_name: 'syb68.154_health_personnel'
  data_files: parquet/syb68/154_health_personnel.parquet
- config_name: 'syb68.176_tourist_visitors_arrival_and_expenditure'
  data_files: parquet/syb68/176_tourist_visitors_arrival_and_expenditure.parquet
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
- config_name: 'syb68.264_patents'
  data_files: parquet/syb68/264_patents.parquet
- config_name: 'syb68.285_research_and_development_expenditure_and_staff'
  data_files: parquet/syb68/285_research_and_development_expenditure_and_staff.parquet
- config_name: 'syb68.309_education'
  data_files: parquet/syb68/309_education.parquet
- config_name: 'syb68.310_carbon_dioxide_emission_estimates'
  data_files: parquet/syb68/310_carbon_dioxide_emission_estimates.parquet
- config_name: 'syb68.313_threatened_species'
  data_files: parquet/syb68/313_threatened_species.parquet
- config_name: 'syb68.314_internet_usage'
  data_files: parquet/syb68/314_internet_usage.parquet
- config_name: 'syb68.315_water_and_sanitation_services'
  data_files: parquet/syb68/315_water_and_sanitation_services.parquet
- config_name: 'syb68.317_seats_held_by_women_in_parliament'
  data_files: parquet/syb68/317_seats_held_by_women_in_parliament.parquet
- config_name: 'syb68.319_ratio_of_girls_to_boys_in_education'
  data_files: parquet/syb68/319_ratio_of_girls_to_boys_in_education.parquet
- config_name: 'syb68.323_teaching_staff_in_education'
  data_files: parquet/syb68/323_teaching_staff_in_education.parquet
- config_name: 'syb68.325_expenditure_on_health'
  data_files: parquet/syb68/325_expenditure_on_health.parquet
- config_name: 'syb68.327_international_migrants_and_refugees'
  data_files: parquet/syb68/327_international_migrants_and_refugees.parquet
- config_name: 'syb68.328_intentional_homicides_and_other_crimes'
  data_files: parquet/syb68/328_intentional_homicides_and_other_crimes.parquet
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
column naming where its value comes from (the ITU for internet use, the WHO
for health personnel, UN Comtrade for trade, and so on). UNdata's terms of
use allow free copying and redistribution with UNdata cited; the
originating agencies' own terms may be stricter. See Licence and the
per-table Sources section before you use a table.

Every CSV is here unchanged, and as one Parquet file per table, typed and
in UTF-8, with two lists: `tables` (one row per table) and `sources` (rows
per Source value per table).

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

One subset per table and edition, named `<edition>.<table number>_<title>`.
The table number is UNdata's, from the file name (internet use is 314 in
SYB67 as in SYB68). The yearbook's own table code (`T30`) is in the first row of each
CSV and in `tables`; it is renumbered between editions (T03 is a different
table in SYB61 and SYB68).

| subset | yearbook code | title (first row of the CSV) | topic on the page | rows |
|---|---|---|---|---:|
| `syb68.1_population_surface_area_and_density` | T02 | Population, density and surface area | Population | 7,727 |
| `syb68.12_agricultural_index` | T20 | Agricultural production indices | Price and production indices | 3,564 |
| `syb68.123_total_imports_exports_and_balance_of_trade` | T21 | Total imports, exports and balance of trade | International merchandise trade | 4,995 |
| `syb68.125_balance_of_payments` | T15 | Balance of payments summary | Finance | 3,305 |
| `syb68.128_consumer_price_index` | T19 | Consumer Price Index | Price and production indices | 2,045 |
| `syb68.130_exchange_rates` | T16 | Exchange rates | Finance | 3,516 |
| `syb68.145_land` | T24 | Land | Environment | 6,297 |
| `syb68.153_gross_value_added_by_economic_activity` | T14 | Gross value added by kind of economic activity | National accounts | 4,432 |
| `syb68.154_health_personnel` | T10 | Health personnel | Nutrition and health | 6,260 |
| `syb68.176_tourist_visitors_arrival_and_expenditure` | T31 | Tourist/visitor arrivals and tourism expenditure | Tourism and transport | 2,154 |
| `syb68.200_employment` | T18 | Employment by economic activity | Labour market | 8,037 |
| `syb68.223_net_disbursements_from_official_oda_from_donors` | T33 | Net disbursements of official development assistance from donors | Development Assistance | 632 |
| `syb68.226_net_disbursements_from_official_oda_to_recipients` | T32 | Net disbursements of official development assistance to recipients | Development Assistance | 5,199 |
| `syb68.230_gdp_and_gdp_per_capita` | T13 | Gross domestic product and gross domestic product per capita | National accounts | 6,768 |
| `syb68.245_public_expenditure_on_education_and_access_to_computers` | T09 | Public expenditure on education (as of 2021) | Education | 2,365 |
| `syb68.246_population_growth_fertility_and_mortality_indicators` | T03 | Population growth and indicators of fertility and mortality | Population | 7,161 |
| `syb68.263_production_trade_and_supply_of_energy` | T23 | Production, trade and supply of energy | Energy | 8,700 |
| `syb68.264_patents` | T29 | Patents | Science and technology | 1,973 |
| `syb68.285_research_and_development_expenditure_and_staff` | T28 | Research and development (R&D) expenditure and researchers (full time equivalent) | Science and technology | 1,039 |
| `syb68.309_education` | T07 | Enrollment in primary, lower secondary and upper secondary education levels | Education | 7,934 |
| `syb68.310_carbon_dioxide_emission_estimates` | T26 | CO2 emission estimates | Environment | 3,488 |
| `syb68.313_threatened_species` | T25 | Threatened species | Environment | 6,916 |
| `syb68.314_internet_usage` | T30 | Internet Usage | Communication | 1,520 |
| `syb68.315_water_and_sanitation_services` | T27 | Water supply and sanitation services | Environment | 3,519 |
| `syb68.317_seats_held_by_women_in_parliament` | T05 | Proportion of seats held by women in national parliament | Gender | 1,952 |
| `syb68.319_ratio_of_girls_to_boys_in_education` | T06 | Ratio of girls to boys in primary, lower secondary and upper secondary education | Gender | 3,347 |
| `syb68.323_teaching_staff_in_education` | T08 | Teaching staff at the primary, lower secondary and upper secondary levels | Education | 3,685 |
| `syb68.325_expenditure_on_health` | T11 | Expenditure on health | Nutrition and health | 2,292 |
| `syb68.327_international_migrants_and_refugees` | T04 | International migrants and refugees | Population | 6,966 |
| `syb68.328_intentional_homicides_and_other_crimes` | T12 | Intentional homicides and other crimes | Crime | 6,046 |
| `syb68.329_labour_force_and_unemployment` | T17 | Labour force participation and unemployment | Labour market | 5,486 |
| `syb68.330_major_trading_partners` | T22 | Major trading partners | International merchandise trade | 3,541 |
| `syb61.253_population_growth_rates_in_urban_areas_and_capital_cities` | T03 | Population and rates of growth in urban areas and capital cities | Population | 4,165 |

`tables` has, per table: `edition`, `table_number`, `subset`, `parquet`
(path), `raw` (path of the CSV), `table_code` and `title` (the CSV's first
row), `page_label` and `topic` (as the UNdata page lists the table),
`edition_month` (the `yyyymm` of the file name, NULL for SYB61),
`page_updated` (the page's "Updated" date as written, NULL when the page
states none), `rows`, `columns` and `sources` (the number of distinct
Source values).

`sources` has `edition`, `table_number`, `subset`, `source` (the Source
text exactly as in the CSV) and `rows`.

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

These are text, as published: `system_of_trade` is a code (`G`, `S`),
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
-- DuckDB, straight off the Hub: internet use in Japan, SYB68
SELECT year, series, value, footnotes
FROM 'hf://datasets/yuiseki/un-statistical-yearbook/parquet/syb68/314_internet_usage.parquet'
WHERE area_code = 392
ORDER BY year;

-- which agencies a table's values come from
SELECT subset, source, rows
FROM 'hf://datasets/yuiseki/un-statistical-yearbook/parquet/sources.parquet'
ORDER BY subset, rows DESC;
```

## Sources per table

The Source value of every row, counted per table. The text is as written
in the CSV; the agency is named at its start.

| subset | rows | Source (as written in the CSV) |
|---|---:|---|
| `syb68.1_population_surface_area_and_density` | 4,252 (55%) | United Nations Population Division, New York, World Population Prospects: The 2024 Revision, last accessed June 2025. |
| `syb68.1_population_surface_area_and_density` | 3,192 (41%) | United Nations Population Division, New York, World Population Prospects: The 2024 Revision; supplemented by data from the United Nations Statistics Division, New York, Demographic Yearbook 2023, last accessed June 2025. |
| `syb68.1_population_surface_area_and_density` | 254 (3%) | United Nations Statistics Division, New York, "Demographic Yearbook 2023" and the demographic statistics database, last accessed June 2025. |
| `syb68.1_population_surface_area_and_density` | 29 (0%) | United Nations Population Division, New York, World Population Prospects: The 2024 Revision - interim update for Togo, last accessed February 2026. |
| `syb68.12_agricultural_index` | 3,564 (100%) | Food and Agriculture Organization of the United Nations (FAO), Rome, FAOSTAT database, last accessed May 2025. |
| `syb68.123_total_imports_exports_and_balance_of_trade` | 4,995 (100%) | United Nations Statistics Division, New York, Commodity Trade Statistics Database (UN COMTRADE), last accessed June 2025. |
| `syb68.125_balance_of_payments` | 3,305 (100%) | International Monetary Fund (IMF), Washington, D.C., Balance of Payment (BOP) Statistics database, last accessed June 2025. |
| `syb68.128_consumer_price_index` | 2,045 (100%) | United Nations Statistics Division (UNSD), New York, Monthly Bulletin of Statistics (MBS), last accessed June 2025. |
| `syb68.130_exchange_rates` | 3,516 (100%) | International Monetary Fund (IMF), Washington, D.C., the database on International Financial Statistics supplemented by operational rates of exchange for United Nations programmes, last accessed June 2025. |
| `syb68.145_land` | 5,283 (84%) | Food and Agriculture Organization of the United Nations (FAO), Rome, FAOSTAT data last accessed December 2024. |
| `syb68.145_land` | 1,014 (16%) | United Nations Environment Programme (UNEP) World Conservation Monitoring Centre (WCMC) and World Conservation Union (IUCN) and BirdLife International, Cambridge, Sustainable Development Goals database, March 2025. |
| `syb68.153_gross_value_added_by_economic_activity` | 4,432 (100%) | United Nations Statistics Division, New York, National Accounts Statistics: Analysis of Main Aggregates (AMA) database, last accessed April 2025. |
| `syb68.154_health_personnel` | 6,260 (100%) | World Health Organisation (WHO), Geneva, WHO Global Health Workforce statistics database, last accessed April 2025. |
| `syb68.176_tourist_visitors_arrival_and_expenditure` | 2,154 (100%) | World Tourism Organization (UNWTO), Madrid, the UNWTO Statistics Database, last accessed December 2023. |
| `syb68.200_employment` | 8,037 (100%) | International Labour Organization (ILO), Geneva, Key Indicators of the Labour Market (KILM 9th edition) and the ILOSTAT database, last accessed April 2025. |
| `syb68.223_net_disbursements_from_official_oda_from_donors` | 632 (100%) | Organisation for Economic Co-operation and Development (OECD), Paris, the OECD Development Assistance Committee (DAC) database, last accessed July 2025. |
| `syb68.226_net_disbursements_from_official_oda_to_recipients` | 5,199 (100%) | Organisation for Economic Co-operation and Development (OECD), Paris, the OECD Development Assistance Committee (DAC) database, last accessed July 2025. |
| `syb68.230_gdp_and_gdp_per_capita` | 6,768 (100%) | United Nations Statistics Division, New York, National Accounts Statistics: Analysis of Main Aggregates (AMA) database, last accessed April 2025. |
| `syb68.245_public_expenditure_on_education_and_access_to_computers` | 2,365 (100%) | United Nations Educational, Scientific and Cultural Organization (UNESCO), Montreal, the UNESCO Institute for Statistics (UIS) statistics database, last accessed April 2025. |
| `syb68.246_population_growth_fertility_and_mortality_indicators` | 4,336 (61%) | United Nations Population Division, New York, World Population Prospects: The 2024 Revision; supplemented by data from the United Nations Statistics Division, New York, Demographic Yearbook 2023, last accessed June 2025. |
| `syb68.246_population_growth_fertility_and_mortality_indicators` | 2,164 (30%) | United Nations Population Division, New York, World Population Prospects: The 2024 Revision, last accessed June 2025. |
| `syb68.246_population_growth_fertility_and_mortality_indicators` | 657 (9%) | World Health Organization (WHO), the United Nations Children's Fund (UNICEF), the United Nations Population Fund (UNFPA), the World Bank and the United Nations Population Division, "Trends in Maternal Mortality 2000 - 2020." |
| `syb68.246_population_growth_fertility_and_mortality_indicators` | 4 (0%) | United Nations Population Division, New York, World Population Prospects: The 2024 Revision  - interim update, last accessed February 2026. |
| `syb68.263_production_trade_and_supply_of_energy` | 8,700 (100%) | United Nations Statistics Division, New York, Energy Statistics Yearbook 2022, last accessed April 2025. |
| `syb68.264_patents` | 1,973 (100%) | World Intellectual Property Organization (WIPO), Geneva, WIPO statistics database, last accessed May 2025. |
| `syb68.285_research_and_development_expenditure_and_staff` | 1,039 (100%) | United Nations Educational, Scientific and Cultural Organization (UNESCO), Montreal, the UNESCO Institute for Statistics (UIS) statistics database, last accessed April 2025. |
| `syb68.309_education` | 7,934 (100%) | United Nations Educational, Scientific and Cultural Organization (UNESCO), Montreal, the UNESCO Institute for Statistics (UIS) statistics database, last accessed April 2025. |
| `syb68.310_carbon_dioxide_emission_estimates` | 3,488 (100%) | United Nations Statistics Division, New York, Energy Statistics Section, last accessed Feb. 2025. |
| `syb68.313_threatened_species` | 6,916 (100%) | World Conservation Union (IUCN), Gland and Cambridge, IUCN Red List of Threatened Species publication, last accessed June 2025. |
| `syb68.314_internet_usage` | 1,520 (100%) | International Telecommunication Union (ITU), Geneva, the ITU database, last accessed March 2025. |
| `syb68.315_water_and_sanitation_services` | 3,519 (100%) | World Health Organization (WHO) and United Nations Children's Fund (UNICEF), Geneva and New York, the WHO/UNICEF Joint Monitoring Programme for the Water and Sanitation database, last accessed July 2025. |
| `syb68.317_seats_held_by_women_in_parliament` | 1,952 (100%) | Inter-Parliamentary Union (IPU), Geneva, the database on "Women in National Parliament", last accessed March 2025. |
| `syb68.319_ratio_of_girls_to_boys_in_education` | 3,347 (100%) | United Nations Educational, Scientific and Cultural Organization (UNESCO), Montreal, the UNESCO Institute for Statistics (UIS) statistics database, last accessed April 2025. |
| `syb68.323_teaching_staff_in_education` | 3,685 (100%) | United Nations Educational, Scientific and Cultural Organization (UNESCO), Montreal, the UNESCO Institute for Statistics (UIS) statistics database, last accessed April 2025. |
| `syb68.325_expenditure_on_health` | 2,292 (100%) | World Health Organization (WHO), Geneva, WHO Global Health Expenditure database, last accessed May 2025. |
| `syb68.327_international_migrants_and_refugees` | 4,200 (60%) | United Nations Population Division, New York, International migrant stock: The 2024 Revision, last accessed April 2025. |
| `syb68.327_international_migrants_and_refugees` | 2,766 (40%) | United Nations High Commissioner for Refugees (UNHCR), Geneva, UNHCR Population Statistics Database, last accessed May 2025. |
| `syb68.328_intentional_homicides_and_other_crimes` | 6,046 (100%) | United Nations Office on Drugs and Crime (UNODC), Vienna, UNODC Statistics database, last accessed May 2025. |
| `syb68.329_labour_force_and_unemployment` | 5,486 (100%) | International Labour Organization (ILO), Geneva, Key Indicators of the Labour Market (KILM 9th edition) and the ILOSTAT database, last accessed April 2025. |
| `syb68.330_major_trading_partners` | 3,541 (100%) | United Nations Statistics Division, New York, Commodity Trade Statistics Database (UN COMTRADE), last accessed June 2025. |
| `syb61.253_population_growth_rates_in_urban_areas_and_capital_cities` | 4,165 (100%) | United Nations Population Division, New York, World Urbanization Prospects: The 2018 Revision, last accessed May 2018. |

In short, by originating agency: UNSD itself for national accounts (153,
230), energy (263, 310), consumer prices (128) and, with UN Comtrade, trade
(123, 330); the UN Population Division for population (1, 246, 327 in part,
and SYB61 253); UNESCO for education and R&D (245, 285, 309, 319, 323); the
WHO for health personnel (154) and health expenditure (325), with UNICEF for
water and sanitation (315) and with others for maternal mortality in 246;
the ILO for labour (200, 329); the IMF for balance of payments (125) and
exchange rates (130); the FAO for agriculture (12) and most of land (145);
the OECD for development assistance (223, 226); the ITU for internet use
(314); the IUCN for threatened species (313); UNWTO for tourism (176); WIPO
for patents (264); the IPU for women in parliament (317); UNODC for crime
(328); UNHCR for refugees (327 in part).

## Things to know

- `area_code` is the M49 code (392 Japan, 1 "Total, all countries or
  areas", 2 Africa, 199 least developed countries, 722 small island
  developing States), and the rows mix countries, areas and aggregates.
  Some aggregate names carry a mark from the source (`LDC§`); they are kept
  as published. `0` is "Total" in the donor table.
- `series` names the measure and its unit ("Percentage of individuals using
  the internet"); a table holds several series. Filter on it before
  comparing values.
- `footnotes` is filled in 49,449 of the 147,026 rows. Read it: it says
  when a value is an estimate, covers a different population or period, or
  breaks the series.
- Years are not continuous. Most tables give selected years (for example
  1995, 2005, 2010, 2015 and the two or three latest; table 330 only 2015,
  2020 and 2024). Tables 154, 200, 245, 285, 309, 323, 328 and 329 have 15
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
- every table's Parquet has as many rows as its CSV has records, the
  column names above in order, each of the type its name gives
- every cell equals the CSV's, row by row: text as text (empty as NULL),
  `area_code` and `year` as Python's int reads them, `value` as Python's
  float reads it once the thousands separators are removed
- `tables` gives each table's row count and `sources` each table's
  Source counts as counted in the CSV
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
  modification or derived works. The card therefore declares
  `license: other`.
- Each row's `source` names the agency the value comes from. The terms do
  not mention those agencies' rights, and their own terms may differ from
  UNdata's. Among the agencies here, these were found stricter (read on
  2026-10-06, not legal advice):
  - ITU: its site terms allow use "for personal, educational, or
    non-commercial purposes" and require prior written permission for
    commercial use and redistribution. Table 314 (internet use) is
    entirely from the ITU.
  - WHO: its datasets are licensed "for public health purposes", with
    alteration only by prior written authorization. Tables 154 and 325 are
    entirely from the WHO, 315 entirely from WHO/UNICEF, and 657 of 7,161
    rows of 246 (maternal mortality) from the WHO with others.
  - UN Comtrade: "UN Comtrade data are provided for internal use only and
    may not be re-disseminated in any form without UNSD's permission."
    Tables 123 and 330 are entirely from UN Comtrade.
  - IMF: its current terms require permission for commercial use. Tables
    125 and 130 are entirely from the IMF.
  - The terms of the IUCN (313), UNWTO (176), WIPO (264), IPU (317) and
    UNODC (328) were not checked.

  Check the table's Source counts above and the agency's terms for your
  use.

This dataset is not made or endorsed by the United Nations. What was
changed: each CSV was decoded from Windows-1252, its title row moved to
`tables`, its columns renamed and typed as above (thousands separators
removed from `value`), and written as Parquet; no value was changed. The
raw files are unchanged. `LICENSE` beside this file says the same.

## Citation

As the terms require, cite UNdata, for example:

> United Nations Statistics Division, UNdata, Statistical Yearbook tables
> (edition SYB68, 2025), https://data.un.org/, accessed 2026-10-06.

and, for the values of a table, the source named in its `source` column.
