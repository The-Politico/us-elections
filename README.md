![POLITICO](https://www.politico.com/interactives/cdn/images/badge.svg)

# us-elections 🇺🇸

A package for working with US elections metadata. Like [python-us](https://github.com/unitedstates/python-us), but for elections!

[![PyPI version](https://badge.fury.io/py/us-elections.svg)](https://badge.fury.io/py/us-elections)


### Quickstart

```
$ pip install us-elections
```


### Exploring election data

```python
from elections import ElectionYear


# GET A SPECIFIC YEAR'S ELECTIONS AND DATA:
election_year = ElectionYear(2020)
election_year
# <ElectionYear: 2020 (Presidential cycle)>


# GET ELECTIONS IN THIS YEAR:
election_year.elections
# [
#   <DemocraticPrimaryElection: Iowa (Feb. 03, 2020)>,
#   <RepublicanPrimaryElection: Iowa (Feb. 03, 2020)>,
#   ...
#   <GeneralElection: Alabama Nov. 03, 2020>,
#   <GeneralElection: Alaska Nov. 03, 2020>,
#   ...
# ]

election_year.elections.primaries
# [
#   <DemocraticPrimaryElection: Iowa (Feb. 03, 2020)>,
#   <RepublicanPrimaryElection: Iowa (Feb. 03, 2020)>,
#   <DemocraticPrimaryElection: New Hampshire (Feb. 11, 2020)>,
#   <RepublicanPrimaryElection: New Hampshire (Feb. 11, 2020)>,
#   ...
# ]

election_year.elections.primaries.republican
# [
#   <RepublicanPrimaryElection: Iowa (Feb. 03, 2020)>,
#   <RepublicanPrimaryElection: New Hampshire (Feb. 11, 2020)>,
#   <RepublicanPrimaryElection: Alabama (Mar. 03, 2020)>,
#   <RepublicanPrimaryElection: Arkansas (Mar. 03, 2020)>,
#   ...
# ]

election_year.elections.general_elections
# [
#   <GeneralElection: Alabama (Nov. 03, 2020)>,
#   <GeneralElection: Alaska (Nov. 03, 2020)>,
#   <GeneralElection: Arizona (Nov. 03, 2020)>,
#   <GeneralElection: Arkansas (Nov. 03, 2020)>,
#   ...
# ]


# You can also filter by type of primary:

# election_year.elections.presidential_primaries
# election_year.elections.presidential_primaries.democratic
# election_year.elections.downticket_primaries
# election_year.elections.downticket_primaries.republican


# GET GOVERNMENTS BY LEVEL:
election_year.federal
# <FederalGovernment: United States of America>

election_year.states
# [
#   <StateGovernment: Alabama>,
#   <StateGovernment: Alaska>,
#   <StateGovernment: Arizona>,
#   <StateGovernment: Arkansas>,
#   ...
# ]

election_year.states.alabama
# <StateGovernment: Alabama>

election_year.states.new_jersey
# <StateGovernment: New Jersey>


# GET A BRANCH WITHIN A GOVERNMENT:
election_year.federal.legislative
# <LegislativeBranch: U.S. Congress>

election_year.states.delaware.executive
# <ExecutiveBranch: Delaware>


# GET SEATS UP FOR ELECTION:
election_year.federal.legislative.seats
# [
#   <HouseSeat: Alaska U.S. House seat, at-large district>,
#   ...
#   <SenateSeat: Alaska U.S. Senate seat, class II>,
#   ...
# ]

election_year.states.delaware.executive.seats
# [
#   <ExecutiveSeat: Delaware Governor>,
#   <ExecutiveSeat: Delaware Lieutenant Governor>,
#   ...
# ]


# GET SEATS FROM A SPECIFIC LEGISLATIVE CHAMBER:
election_year.federal.legislative.seats.senate
# [
#   <SenateSeat: Alabama U.S. Senate seat, class II>,
#   <SenateSeat: Alaska U.S. Senate seat, class II>,
#   <SenateSeat: Arizona U.S. Senate seat, class III>,
#   <SenateSeat: Arkansas U.S. Senate seat, class II>,
#   ...
# ]

election_year.federal.legislative.seats.house
# [
#   <HouseSeat: Alaska U.S. House seat, at-large district>,
#   <HouseSeat: Alabama U.S. House seat, 1st district>,
#   <HouseSeat: Alabama U.S. House seat, 2nd district>,
#   <HouseSeat: Alabama U.S. House seat, 3rd district>,
#   ...
# ]


# FILTER BY STATE:
election_year.elections_for_state('TX')
# [
#   <DemocraticPrimaryElection: Texas (Mar. 03, 2020)>,
#   <RepublicanPrimaryElection: Texas (Mar. 03, 2020)>,
#   <GeneralElection: Texas (Nov. 03, 2020)>
# ]

election_year.federal.legislative.seats_for_state('TX')
# [
#   <SenateSeat: Texas U.S. Senate seat, class II>,
#   <HouseSeat: Texas U.S. House seat, 1st district>,
#   <HouseSeat: Texas U.S. House seat, 2nd district>,
#   <HouseSeat: Texas U.S. House seat, 3rd district>,
#   ...
# ]

election_year.federal.legislative.seats_for_state('GA').senate
# [
#   <SenateSeat: Georgia U.S. Senate seat, class II>,
#   <SenateSeat: Georgia U.S. Senate seat, class III>
# ]
```

### Class-by-class reference

#### `ElectionYear`

Model docs TK.


#### `GovernmentLevel`

**Variants:** `FederalGovernment` and `StateGovernment` (for now).

Model docs TK.


#### `GovernmentBranch`

**Variants:** `LegislativeBranch` and  `ExecutiveBranch` (for now).

Model docs TK.


#### `PrimaryElection`

**Party-specific variants:** `DemocraticPrimaryElection` and `RepublicanPrimaryElection`.

Model docs TK.


#### `PrimaryRunoffElection`

**Party-specific variants:** `DemocraticPrimaryRunoffElection` and `RepublicanPrimaryRunoffElection`.

Model docs TK.


#### `GeneralElection`

Model docs TK.


#### `ElectoralZone`

**Variants:** `DistrictElectoralZone` and `StateElectoralZone`.

Model docs TK.


#### `SenateSeat`

Model docs TK.


#### `HouseSeat`

 Model docs TK.


#### `ExecutiveSeat`

**Variants:** `HeadOfGovernmentSeat`.

Model docs TK.


#### `Party`

Model docs TK.


### Contributing data

1. Add data to one of the CSVs in the `db/` directory.
2. Build the package data files: `$ python build.py`
3. Submit a pull request!


### Influences

This project borrows most of its software design from [python-us](https://github.com/unitedstates/python-us).

Its data models are also heavily inspired by the [DNC election data project](https://github.com/democrats/data).


### Testing

```
$ pipenv install -d
$ pipenv run pytest
```
