import os
import pickle

import us

from elections.models.seats import HouseSeat, SenateSeat
from elections.models.elections import GeneralElection, PrimaryElection

PWD = os.path.abspath(os.path.dirname(__file__))


class InvalidYear(Exception):
    pass


def load_years():
    from pkg_resources import resource_stream

    years = []
    # load state data from pickle file
    with resource_stream(__name__, "data/years.pkl") as pklfile:
        for d in pickle.load(pklfile):
            years.append(d)
    return years


def load_seats(year):
    from pkg_resources import resource_stream

    seats = []
    # load state data from pickle file
    with resource_stream(
        __name__, "data/{}/seats.pkl".format(year)
    ) as pklfile:
        for d in pickle.load(pklfile):
            if d["seat_type"] == "house":
                seats.append(HouseSeat(**d))
            elif d["seat_type"] == "senate":
                seats.append(SenateSeat(**d))
    return seats


def load_elections(year):
    from pkg_resources import resource_stream

    elections = []
    # load state data from pickle file
    with resource_stream(
        __name__, "data/{}/elections.pkl".format(year)
    ) as pklfile:
        for d in pickle.load(pklfile, encoding="latin1"):
            if d["election_type"] == "general":
                elections.append(GeneralElection(**d))
            elif d["election_type"] == "primary":
                elections.append(PrimaryElection(**d))
    return elections


class ElectionYear(object):
    def __init__(self, year):
        year = str(year)
        if year not in load_years():
            raise InvalidYear(
                "No data available for the {} election cycle".format(year)
            )
        self.year = year
        self.seats = load_seats(year)
        self.elections = load_elections(year)

    @property
    def general_elections(self):
        return [
            election
            for election in self.elections
            if isinstance(election, GeneralElection)
        ]

    @property
    def primary_elections(self):
        return [
            election
            for election in self.elections
            if isinstance(election, PrimaryElection)
        ]

    @property
    def senate_seats(self):
        return [seat for seat in self.seats if isinstance(seat, SenateSeat)]

    @property
    def house_seats(self):
        return [seat for seat in self.seats if isinstance(seat, HouseSeat)]

    def seats_for_state(self, state):
        state = us.states.lookup(state)
        return [seat for seat in self.seats if seat.state == state]

    def elections_for_state(self, state):
        state = us.states.lookup(state)
        return [
            election for election in self.elections if election.state == state
        ]
