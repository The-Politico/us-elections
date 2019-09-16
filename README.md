![POLITICO](https://www.politico.com/interactives/cdn/images/badge.svg)

[![PyPI version](https://badge.fury.io/py/us-elections.svg)](https://badge.fury.io/py/us-elections)

# us-elections

A package for working with US elections metadata. Like [python-us](https://github.com/unitedstates/python-us), but for elections!

### Quickstart

```
$ pip install us-elections
```

```python
from elections import ElectionYear

election_year = ElectionYear(2018)

# GET ELECTIONS IN THIS YEAR
election_year.elections
# [<GeneralElection: Alabama Nov. 06, 2018>, ... ]

election_year.general_elections
election_year.primary_elections


# GET SEATS UP FOR ELECTION
election_year.seats
# [<HouseSeat: Alaska U.S. House seat, at-large district>, ... ]

election_year.senate_seats
election_year.house_seats


# FILTER BY STATE
election_year.elections_for_state('TX')
# [<GeneralElection: Texas Nov. 06, 2018>, ... ]

election_year.seats_for_state('TX')
# [<HouseSeat: Texas U.S. House seat, 1st district>, ... ]
```

### Contributing data

1. Add data to a CSV in the `db/` directory.
2. `$ python build.py`
3. Submit a pull request!

### Prior art

This project heavily borrows its software design from [python-us](https://github.com/unitedstates/python-us).

Its data models are also heavily inspired by the [DNC election data project](https://github.com/democrats/data).

### Testing

```
$ pytest
```
