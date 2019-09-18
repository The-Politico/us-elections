from datetime import datetime
import pytest
from elections import ElectionYear, InvalidYear


def test_invalid_year():
    with pytest.raises(InvalidYear):
        ElectionYear(2222)


def test_elections():
    election_year = ElectionYear(2018)
    elections = election_year.elections
    assert len(elections) == 102
    assert len(elections.general) == 51
    assert len(elections.primary) == 51


def test_seats():
    election_year = ElectionYear(2018)
    seats = election_year.seats
    assert len(seats) == 468
    assert len(seats.house) == 435
    assert len(seats.senate) == 33


def test_seats_for_state():
    election_year = ElectionYear(2018)
    seats = election_year.seats_for_state("TX")
    assert len(seats.senate) == 1
    assert len(seats.house) == 36


def test_elections_for_state():
    election_year = ElectionYear(2018)
    elections = election_year.elections_for_state("TX")
    assert elections[0].election_date == datetime(2018, 11, 6, 0, 0)
    assert elections[1].election_date == datetime(2018, 3, 6, 0, 0)
