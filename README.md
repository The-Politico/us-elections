![POLITICO](https://www.politico.com/interactives/cdn/images/badge.svg)

# us-elections 🇺🇸

A package for working with US elections metadata. Like [python-us](https://github.com/unitedstates/python-us), but for elections!

[![PyPI version](https://badge.fury.io/py/us-elections.svg)](https://badge.fury.io/py/us-elections)

### Quickstart

```
$ pip install us-elections
```

### Classes

#### `ElectionYear`

```python
from elections import ElectionYear

election_year = ElectionYear(2018)

# GET ELECTIONS IN THIS YEAR
election_year.elections
# [<GeneralElection: Alabama Nov. 06, 2018>, ... ]

election_year.elections.general
election_year.elections.primary


# GET SEATS UP FOR ELECTION
election_year.seats
# [<HouseSeat: Alaska U.S. House seat, at-large district>, ... ]

election_year.seats.senate
election_year.seats.house


# FILTER BY STATE
election_year.elections_for_state('TX')
# [<GeneralElection: Texas Nov. 06, 2018>, ... ]

election_year.seats_for_state('TX')
# [<HouseSeat: Texas U.S. House seat, 1st district>, ... ]
```

#### `SenateSeat`

```python
from elections import ElectionYear

election_year = ElectionYear(2018)
seat = election_year.seats.senate[0]

seat.state
# <State:Arizona>

seat.incumbent
# 'Flake, Jeff'

seat.incumbent_party
# <Party: Republican Party>

seat.senate_class
# 'I'

# etc.
```

#### `HouseSeat`

```python
from elections import ElectionYear

election_year = ElectionYear(2018)
seat = election_year.seats.senate[0]

seat.state
# <State:Alaska>

seat.district
#

seat.district_name
# 'at-large district'

seat.incumbent
# 'Young, Don'

seat.incumbent_party
# <Party: Republican Party>

# etc.
```
#### `GeneralElection`

```python
from elections import ElectionYear

election_year = ElectionYear(2018)
election = election_year.elections.general[0]

election.state
# <State:Alabama>

election.election_date
# datetime.datetime(2018, 11, 6, 0, 0)

election.registration_deadline
# datetime.datetime(2018, 10, 22, 0, 0)

# etc.
```
#### `PrimaryElection`

```python
from elections import ElectionYear

election_year = ElectionYear(2018)
election = election_year.elections.primary[0]

election.state
# <State:Alabama>

election.election_date
# datetime.datetime(2018, 6, 5, 0, 0)

election.gop_election_type
# 'open'

election.runoff_election_date
# datetime.datetime(2018, 7, 17, 0, 0)

# etc.
```

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
