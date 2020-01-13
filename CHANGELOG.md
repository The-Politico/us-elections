# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2020-01-12
### Added
- New `downticket_primaries` filter method to `ElectionTypeFilterableList`.
- New shim for electoral areas that are not listed in the python-us library (for now, just "Democrats Abroad").

### Changed
- Further updates to 2020 primary election data, including merging presidential and other primaries to one file.
- Reformat 2018 primary election data to feature one party and state's primary per line.
- Sort lists of legislative seats by chamber (if any), state name, senate class (if any) and district number (if any).
- Sort lists of elections by earliest to latest date, and then by state name.
- Refactored how primary and primary-runoff election instances are created.
- Updated `README.md` to reflect the latest API structure and output.

### Removed
- Separate data types for presidential primaries are no longer needed.

## [0.3.0] - 2020-01-12
### Added
- This CHANGELOG file to hopefully serve as an evolving example of a
  standardized open source project CHANGELOG.

### Changed
- Major update to 2020 primary data: now including latest known accurate information on all primary elections.
- Updated Georgia's incumbent Class III Senator to reflect Johnny Isakson's resignation in late December 2019.
- Cast "yes" or "no" CSV values to boolean types (previously this only worked for "true" and "false" values).
- Update `ship` command in Makefile to run inside the pipenv.

## [0.2.0] - 2019-11-17
### Added
- Initial commits of 2020 presidential/other primary data.
- New data models for Democratic and Republican primary elections.
- New data models for presidential primary elections, including discrete Democratic and Republican variants.
- New data models for primary runoff elections, including discrete Democratic and Republican variants.

### Changed
- Modify 2018 primaries to allow for different Republican and Democratic primary dates.
- Modify 2020 general election data with correct dates.
- Change filterable election lists to allow for selecting only Democratic or Republican primaries.
- Change filterable election lists to allow for selecting only primary runoffs or presidential primaries, in addition to existing filters for other primaries and general elections.

## [0.1.1] - 2019-10-21
### Changed
- Make districted electoral zones' district data be strings (which are zero-padded), not integers.
- Slight linting changes to source.

### Removed
- Remove empty sections from CHANGELOG, they occupy too much space and
create too much noise in the file. People will have to assume that the
missing sections were intentionally left out because they contained no
notable changes.

## [0.1.0] - 2019-10-18
### Added
- Models, data and API for the Electoral College.
- Models, data and API for the executive and judicial branches.
- Models, data and API for state governments.
- Models, data and API for executive-branch seats.
- Filterable list types: executive branch seats by type, electoral vote areas by type (statewide or districted).
- Utilities to classify election years by type (presidential election, midterm or otherwise).

### Changed
- Major re-organization of main code: move `ElectionYear` model into its own file, leaving only the top-most code in `./elections/__init__.py`.
- Move version number from `./setup.py` into `./elections/__init__.py`.
- Additional modifications to make `./setup.py` more dynamic.
- Re-factor to no longer make this library Congress-specific: add support for other government branches and state-level governments.

## [0.0.2] - 2019-09-18
### Added
- Additional documentation in README for `SenateSeat`, `HouseSeat`, `GeneralElection` and `PrimaryElection`.
- More tests for senate & house seats and primary & general elections.

### Changed
- Rename `seat.party` to `seat.incumbent_party`.
- Better descriptions of the process for contributing data changes.

## [0.0.1] - 2019-09-18
### Added
- `Party` data model.
- Filterable lists: seats by legislative chamber, elections by type.
- Initial tests.

### Changed
- Properly segmented out some development dependencies.
- Re-organized source CSVs (under `./db/*`) by data type and updated pipeline to reflect this.
- Modifications to API, which are reflected in `./README.md`.

## [0.0a1.dev1] - 2019-09-16
### Added
- Initial working commit.
- Initial 2018 and (preliminary) 2020 CSV data (`./db/*`).
- Data pipeline (`./build.py`) and indexed data files (`./elections/data/*`).
- Data models (`./elections/models/*`) that use indexed data files.
- Helper files for module (`./elections/constants.py`, `./elections/exceptions/*` and `./elections/utils/*`).
- Initial documentation (``./docs/*``).
- Additional root-level files, including `README.md`, `Pipfile` and `Pipfile.lock`, `Makefile` and `LICENSE`.

[Unreleased]: https://github.com/The-Politico/us-elections/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/The-Politico/us-elections/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/The-Politico/us-elections/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/The-Politico/us-elections/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/The-Politico/us-elections/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/The-Politico/us-elections/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/The-Politico/us-elections/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/The-Politico/us-elections/compare/v0.0a1.dev1...v0.0.1
[0.0a1.dev1]: https://github.com/The-Politico/us-elections/releases/tag/v0.0a1.dev1
