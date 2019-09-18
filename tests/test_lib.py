from datetime import datetime
import pytest
from elections import ElectionYear, InvalidYear
import us


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


def test_senate_seat():
    election_year = ElectionYear(2018)
    seat = election_year.seats.senate[0]
    assert seat.state == us.states.lookup("AZ")
    assert seat.incumbent == "Flake, Jeff"
    assert seat.incumbent_party.name == "Republican Party"
    assert seat.senate_class == "I"


def test_house_seat():
    election_year = ElectionYear(2018)
    seat = election_year.seats.house[0]
    assert seat.state == us.states.lookup("AK")
    assert seat.district is None
    assert seat.district_name == "at-large district"
    assert seat.incumbent == "Young, Don"
    assert seat.incumbent_party.name == "Republican Party"


def test_general_election():
    election_year = ElectionYear(2018)
    election = election_year.elections.general[0]
    assert election.state == us.states.lookup("AL")
    assert election.election_date == datetime(2018, 11, 6, 0, 0)
    assert election.registration_deadline == datetime(2018, 10, 22, 0, 0)


def test_primary_election():
    election_year = ElectionYear(2018)
    election = election_year.elections.primary[0]
    assert election.state == us.states.lookup("AL")
    assert election.election_date == datetime(2018, 6, 5, 0, 0)
    assert election.gop_election_type == "open"
    assert election.runoff_election_date == datetime(2018, 7, 17, 0, 0)
